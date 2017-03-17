# Embedded file name: scripts/client/InitPlayerInfo.py
from clientConsts import GUI_TYPES
from debug_utils import LOG_ERROR, LOG_DEBUG
from consts import IGR_TYPE
import wgPickle

class InitPlayerInfo(object):

    def __init__(self, infoMap):
        self.accountName = '<EMPTY>'
        self.isDeveloper = False
        self.isDevelopment = False
        self.databaseID = None
        self.serverLocalTime = 0
        self.premiumExpiryTime = -1
        self.useGUIType = GUI_TYPES.NORMAL
        self.premiumCost = None
        self.disableBuyPremium = False
        self.creditsCost = 0
        self.freeExpCost = 0
        self.captchaEnabled = False
        self.attrs = 0
        self.isAOGASEnabled = False
        self.ver = 0
        self.activeEvents = None
        self.responseSequence = 0
        self.denunciationsLeft = 5
        self.planesToSellLeft = 0
        self.clanAbbrev = ''
        self.clanDBID = 0
        self.clanAttrs = 0
        self.AOGASParams = None
        self.rssUrl = ''
        self.igrRoomID = 0
        self.igrType = IGR_TYPE.NONE
        self.requestStats = 0
        self.serverSessionKey = 0
        self.gameParams = {}
        self.update(infoMap)
        return

    def update(self, infoMap):
        for k, v in infoMap.items():
            if not hasattr(self, k):
                LOG_ERROR('Missing attr %s in InitPlayerInfo' % str(k))
            if k == 'AOGASParams' and isinstance(v, basestring):
                v = wgPickle.loads(wgPickle.FromServerToClient, v)
            setattr(self, k, v)


class ClanExtendedInfo(object):

    def __init__(self):
        self.resetAttrs()

    def resetAttrs(self):
        self.members = {}
        self.clanName = ''
        self.clanMotto = ''
        self.clanDescription = ''
        self.emblemPath64x64 = ''


class CommandsFiredCounter(object):

    def __init__(self):
        self.__commandsFiredCount = dict()

    @property
    def commandsFiredCount(self):
        return self.__commandsFiredCount

    def reset(self):
        self.__commandsFiredCount.clear()

    def update(self, commandsFiredCount):
        """
        @param commandsFiredCount: <dict> cmdID : firedCount
        """
        for cmdID, firedCount in commandsFiredCount.iteritems():
            self.__commandsFiredCount[cmdID] = firedCount + self.__commandsFiredCount.get(cmdID, 0)

    def __debugPrint(self):
        import InputMapping
        for cmdID, firedCount in self.__commandsFiredCount.iteritems():
            LOG_DEBUG('debugPrint', 'cmd=', InputMapping.g_descriptions.getCommandNameByID(cmdID), 'firedCount=', firedCount)