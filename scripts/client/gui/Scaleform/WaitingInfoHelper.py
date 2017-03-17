# Embedded file name: scripts/client/gui/Scaleform/WaitingInfoHelper.py
from consts import WAITING_INFO_TYPE, CLIENT_STATS_TYPE
import wgPickle
import BigWorld
from debug_utils import LOG_DEBUG

class WaitingInfoHelper(object):
    _currentWaiting = {}
    _account = None
    _pending = {}
    _newPendingCount = 0

    def init(self, account):
        self._account = account

    def startWaiting(self, waitingType):
        self._currentWaiting[waitingType] = BigWorld.time()
        self._newPendingCount += 1

    def stopWaiting(self, waitingType):
        if waitingType not in self._currentWaiting:
            return
        self.addWaitingInfo(waitingType, BigWorld.time() - self._currentWaiting[waitingType])
        del self._currentWaiting[waitingType]

    def addWaitingInfo(self, waitingType, waitingTime):
        LOG_DEBUG('Waiting info: waited {0}s on {1}'.format(waitingTime, WAITING_INFO_TYPE.getString(waitingType)))
        if waitingType not in self._pending:
            self._pending[waitingType] = []
        self._pending[waitingType].append(waitingTime)

    def deinit(self):
        self._account = None
        return

    def clearWaitingStats(self):
        self._pending = {}
        self._newPendingCount = 0

    def updateWaitingStats(self):
        if self._account is None or self._newPendingCount == 0:
            return
        else:
            waitData = {}
            for waitingType, info in self._pending.iteritems():
                infoLen = len(info)
                if infoLen > 1:
                    info.sort()
                    if len(info) % 2 == 0:
                        median = info[infoLen // 2]
                    else:
                        median = (info[(infoLen + 1) // 2] + info[(infoLen - 1) // 2]) / 2.0
                    waitData[waitingType] = [infoLen,
                     info[0],
                     info[-1],
                     sum(info) / infoLen,
                     median]
                elif infoLen == 1:
                    waitData[waitingType] = [1,
                     info[0],
                     info[0],
                     info[0],
                     info[0]]

            if waitData:
                player = self.getPlayer()
                if player:
                    waitData = wgPickle.dumps(wgPickle.FromClientToServer, waitData.items())
                    player.base.updateClientStats(CLIENT_STATS_TYPE.CLIENT_WAITING_TIME, waitData)
                    self._newPendingCount = 0
            return

    def getPlayer(self):
        player = BigWorld.player()
        from Account import PlayerAccount
        if player is not None and player.__class__ == PlayerAccount:
            return player
        else:
            return
            return