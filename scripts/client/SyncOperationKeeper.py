# Embedded file name: scripts/client/SyncOperationKeeper.py
from gui.Scaleform.Waiting import Waiting

class FLAGS_CODE:
    SAVE_PRESET, INSTALL_PRESET, IN_BATTLE, SELL_PLANE, BUY_PLANE = range(5)


class SyncOperationKeeper(object):
    __FLAGS = [ getattr(FLAGS_CODE, attrname) for attrname in dir(FLAGS_CODE) if not attrname.startswith('__') and not callable(getattr(FLAGS_CODE, attrname)) ]
    __FLAGS_STATUS = dict([ (signal, 0) for signal in __FLAGS ])
    __RULES = {FLAGS_CODE.SAVE_PRESET: [FLAGS_CODE.IN_BATTLE, FLAGS_CODE.SELL_PLANE],
     FLAGS_CODE.INSTALL_PRESET: [FLAGS_CODE.IN_BATTLE, FLAGS_CODE.SELL_PLANE],
     FLAGS_CODE.SELL_PLANE: [FLAGS_CODE.IN_BATTLE, FLAGS_CODE.BUY_PLANE],
     FLAGS_CODE.BUY_PLANE: [FLAGS_CODE.IN_BATTLE, FLAGS_CODE.SELL_PLANE]}
    __WAITING_IDS = {}

    @staticmethod
    def __getProcessedFlags(flagCode):
        if flagCode is not None:
            return SyncOperationKeeper.__RULES[flagCode] + [flagCode]
        else:
            return SyncOperationKeeper.__FLAGS

    @staticmethod
    def start(flagCode = None, waitingMsg = 'LOBBY_LOAD_HANGAR_SPACE_VEHICLE', showWaiting = True):
        if showWaiting and not SyncOperationKeeper.getFlagStatus(flagCode):
            waitingID = Waiting.show(waitingMsg)
            SyncOperationKeeper.__WAITING_IDS[flagCode] = waitingID
        for flag in SyncOperationKeeper.__getProcessedFlags(flagCode):
            SyncOperationKeeper.__FLAGS_STATUS[flag] += 1

    @staticmethod
    def stop(flagCode = None, waitingID = None):
        if SyncOperationKeeper.getFlagStatus(flagCode):
            for flag in SyncOperationKeeper.__getProcessedFlags(flagCode):
                SyncOperationKeeper.__FLAGS_STATUS[flag] -= 1

            if not SyncOperationKeeper.getFlagStatus(flagCode) and flagCode in SyncOperationKeeper.__WAITING_IDS:
                Waiting.hide(SyncOperationKeeper.__WAITING_IDS[flagCode])
                del SyncOperationKeeper.__WAITING_IDS[flagCode]

    @staticmethod
    def getFlagStatus(flagCode):
        return SyncOperationKeeper.__FLAGS_STATUS[flagCode]

    @staticmethod
    def clearAllFlags():
        SyncOperationKeeper.__FLAGS_STATUS = dict([ (signal, 0) for signal in SyncOperationKeeper.__FLAGS ])
        SyncOperationKeeper.__WAITING_IDS = {}