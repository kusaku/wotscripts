# Embedded file name: scripts/client/messenger/XmppChat.py
import BigWorld, Settings
import GameServerMessenger
from ConnectionManager import connectionManager
from Helpers import i18n, html
from encodings import utf_8
from consts import MESSAGE_TYPE
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_WARNING, LOG_ERROR, LOG_INFO, LOG_TRACE
from account_helpers import ClanEmblemsCache
import filters
import messenger
import time
import string
from random import sample
import VOIP
import GameEnvironment
SEARCH_USERS_MAX_COUNT = 50

class ChannelType():
    UNKNOWN = 0
    GROUP_OPEN = 1
    GROUP_CLOSED = 2
    SQUAD = 3
    COMMON = 4
    PRIVATE = 5
    CLAN = 6
    TRAINING = 7

    @staticmethod
    def getType(jidChannel):
        if jidChannel.find('squad_channel_') == 0:
            return ChannelType.SQUAD
        return ChannelType.UNKNOWN


class FilteringType():
    UNKNOWN = -1
    FULL = 0
    SHORT = 1
    ADMIN = 2


class XmppChatHandler():

    def __init__(self):
        connectionManager.onDisconnected += self.__onDisconnected
        self.__resetAttrs()

    def fini(self):
        connectionManager.onDisconnected -= self.__onDisconnected
        self._filterChain = None
        return

    def __resetAttrs(self):
        self.params = {}
        self.requestChatTokenPostponed = False
        self.__initFilterChain()
        self.__curSquadChannel = ''
        self.__curTrainingChannel = ''
        self.__lastFilteringType = None
        self._filterChainAdmin = None
        return

    def __initFilterChain(self):
        self._filterChain = filters.FilterChain()
        self._filterChain.addFilter('olFilter', filters.ObsceneLanguageFilter())
        self._filterChain.addFilter('domainFilter', filters.DomainNameFilter())
        self._filterChain.addFilter('spamFilter', filters.SpamFilter())
        self._filterChain.addFilter('floodFilter', filters.FloodFilter())

    def __initFilterChainAdmin(self):
        self._filterChainAdmin = filters.FilterChain()
        self._filterChainAdmin.addFilter('coloringOlFilter', filters.ColoringObsceneLanguageFilter())

    def getInitParams(self):
        GameServerMessenger.g_instance.getInitParams()

    def runXmppChatCore(self, spaID, token):
        self.params['spaID'] = spaID
        chatConfig = Settings.g_instance.scriptConfig.xmppChatConfig
        connections = []
        testPortStr = chatConfig.get('useTestPort')
        if testPortStr:
            LOG_TRACE("Xmpp chat: using test port for connection... '%s'" % testPortStr)
            try:
                testPort = int(testPortStr)
                for conn in self.params['xmpp_connections']:
                    connections.append((conn[0], testPort))

            except:
                LOG_TRACE("Xmpp chat: can not use test port '%s'" % testPortStr)

        if connections == []:
            connections = self.params['xmpp_connections']
        BigWorld.XMPPChat.startClient(self.params['xmpp_host'], str(spaID), str(token), self.params['xmpp_std_rooms_svc'], self.params['xmpp_user_rooms_svc'], self.params['xmpp_specific_rooms_svc'], self.params['xmpp_clan_rooms_svc'], connections, self.params['xmpp_resource'], Settings.g_instance.clusterID, chatConfig)
        self.onUpdateChatSettings()

    def filterInMessage(self, text, userUid, msgTime, filteringType):
        if filteringType == FilteringType.FULL:
            if self.__lastFilteringType is not None and self.__lastFilteringType != filteringType:
                filters.ObsceneLanguageFilter.applyReplacementFunction()
            result = self._filterChain.chainIn(i18n.convert(text), userUid, msgTime)
        elif filteringType == FilteringType.ADMIN and GameEnvironment.getHUD() is None:
            if not self._filterChainAdmin:
                self.__initFilterChainAdmin()
            if self.__lastFilteringType is not None and self.__lastFilteringType != filteringType:
                filters.ColoringObsceneLanguageFilter.applyReplacementFunction()
            result = self._filterChainAdmin.chainIn(i18n.convert(text), userUid, msgTime)
        elif filteringType == FilteringType.SHORT:
            result = html.escape(i18n.convert(text))
        else:
            result = text
            LOG_TRACE('Xmpp chat: unknown message filtering type ', filteringType)
        self.__lastFilteringType = filteringType
        return utf_8.encode(result)[0]

    def filterOutMessage(self, text):
        return self._filterChain.chainOut(text, False)

    def requestNicknameByID(self, dbid):
        try:
            GameServerMessenger.g_instance.requestNicknameByID(int(dbid))
        except:
            LOG_DEBUG("Xmpp chat: requestNicknameByID can not request non int value '%s'" % dbid)

    def searchUsersByName(self, name, maxCount, callback = None):
        if not 0 < maxCount < SEARCH_USERS_MAX_COUNT:
            maxCount = SEARCH_USERS_MAX_COUNT
        if callback == None:
            callback = self.__onSearchUsersByName
        GameServerMessenger.g_instance.requestUserlistByName(name, maxCount, callback)
        return

    def __onSearchUsersByName(self, args, error):
        if not error:
            res = [ ('%d@%s' % (spaID, self.params['xmpp_host']), nickname, tag) for spaID, nickname, tag in args if spaID != self.params['spaID'] ]
        else:
            res = []
        BigWorld.XMPPChat.onSearchUsersByName(res)

    def __onDisconnected(self):
        self.__resetAttrs()
        BigWorld.XMPPChat.stopClient()

    def onEnterLobbyEvent(self):
        self.__lastFilteringType = FilteringType.UNKNOWN
        if self.params == {}:
            self.getInitParams()
            return
        if self.requestChatTokenPostponed:
            self.requestChatToken()

    def sendSystemMessage(self, message):
        BigWorld.player().base.sendQueueMessage(str(message))

    def onReceiveSystemMessage(self, senderName, message):
        BigWorld.XMPPChat.onReceiveSystemMessage(senderName, message)

    def onReceiveBanInfo(self, restrictionType, isBan, reason, expireTime):
        BigWorld.XMPPChat.onReceiveBanInfo(restrictionType, isBan, reason, expireTime)

    def createChannel(self, type, jid = '', password = ''):
        if not jid:
            prefix = ''
            if type == ChannelType.SQUAD:
                prefix = 'squad_channel_'
            elif type == ChannelType.TRAINING:
                prefix = 'training_channel_'
            if not self.params or 'spaID' not in self.params:
                jid = prefix + '100_test@fake.com'
            else:
                jid = prefix + '%d_%d@%s' % (self.params['spaID'], int(time.time()), self.params['xmpp_specific_rooms_svc'])
        if not password:
            password = ''.join(sample(string.ascii_letters * 8, 8))
        BigWorld.XMPPChat.createChannel(jid, '', type, password)
        cType = ChannelType.getType(jid)
        if cType == ChannelType.SQUAD:
            self.__curSquadChannel = jid
        elif cType == ChannelType.TRAINING:
            self.__curTrainingChannel = jid
        return (jid, password)

    def deleteChannel(self, jid):
        BigWorld.XMPPChat.removeChannel(jid)
        cType = ChannelType.getType(jid)
        if cType == ChannelType.SQUAD:
            self.__curSquadChannel = ''
        elif cType == ChannelType.TRAINING:
            self.__curTrainingChannel = ''

    def joinChannel(self, jid, password = '', name = ''):
        BigWorld.XMPPChat.joinChannel(jid, password, name)
        cType = ChannelType.getType(jid)
        if cType == ChannelType.SQUAD:
            self.__curSquadChannel = jid
        elif cType == ChannelType.TRAINING:
            self.__curTrainingChannel = jid

    def leaveChannel(self, jid):
        BigWorld.XMPPChat.leaveChannel(jid)
        cType = ChannelType.getType(jid)
        if cType == ChannelType.SQUAD:
            self.__curSquadChannel = ''
        elif cType == ChannelType.TRAINING:
            self.__curTrainingChannel = ''

    def kickFromChannel(self, jid, user):
        BigWorld.XMPPChat.kickFromChannel(jid, str(user))

    def sendMessage(self, jid, message):
        BigWorld.XMPPChat.sendMessage(jid, message)

    def sendSquadMessage(self, message):
        if self.__curSquadChannel and message:
            self.sendMessage(self.__curSquadChannel, message)

    def requestChatToken(self):
        player = BigWorld.player()
        from Account import PlayerAccount
        if player != None and player.__class__ == PlayerAccount:
            player.tokenManager.requestToken(self.runXmppChatCore)
            self.requestChatTokenPostponed = False
        else:
            self.requestChatTokenPostponed = True
            LOG_TRACE('Xmpp chat: token request postponed')
        return

    def addUserToSquad(self, userId):
        try:
            dbid = int(userId)
        except:
            LOG_DEBUG("Xmpp chat: addUserToSquad can not use non int value '%s'" % userId)
            return

        LOG_TRACE('Xmpp chat: add user to squad %d' % dbid)
        player = BigWorld.player()
        from Account import PlayerAccount
        if player != None and player.__class__ == PlayerAccount and player._lobbyInstance:
            player._lobbyInstance.addUserToSquad(dbid)
        return

    def showUserGameStatistics(self, userId, userName, clanTag):
        try:
            dbid = int(userId)
        except:
            LOG_DEBUG("Xmpp chat: showUserGameStatistics can not use non int value '%s'" % userId)
            return

        LOG_TRACE('Xmpp chat: show user game statistics %d, %s, %s' % (dbid, userName, clanTag))
        player = BigWorld.player()
        from Account import PlayerAccount
        if player != None and player.__class__ == PlayerAccount and player._lobbyInstance:
            player._lobbyInstance.showUserGameStatistics(dbid, userName, clanTag)
        return

    def setChatSettings(self, settings):
        LOG_DEBUG('Xmpp chat: setChatSettings:', settings)
        for key, value in settings.iteritems():
            Settings.g_instance.setXmppChatValue(key, value)

    def onUpdateChatSettings(self):
        settings = Settings.g_instance.getXmppChatSettings()
        BigWorld.XMPPChat.onUpdateChatSettings(settings)

    def setUserMuted(self, userId, mute):
        try:
            dbid = int(userId)
        except:
            LOG_DEBUG("Xmpp chat: setUserMuted can not request non int value '%s'" % userId)
            return

        VOIP.api().setClientMuted(dbid, mute)

    def getMuteList(self):
        VOIP.api().requestMuteList(self.receiveMuteList)

    def receiveMuteList(self, muteList):
        muteList = [ str(dbid) for dbid in muteList ]
        BigWorld.XMPPChat.onReceiveMuteList(muteList)

    def clanChannelJid(self):
        import BWPersonality
        channelJid = ''
        if int(BWPersonality.g_initPlayerInfo.clanDBID) > 0:
            channelJid = 'clan_channel_%s@%s' % (str(BWPersonality.g_initPlayerInfo.clanDBID), self.params['xmpp_clan_rooms_svc'])
        return channelJid

    def refreshClanInfo(self):
        if not self.params:
            return
        import BWPersonality
        pInfo = BWPersonality.g_initPlayerInfo
        cInfo = BWPersonality.g_clanExtendedInfo
        BigWorld.XMPPChat.onHandleClanInfo(str(pInfo.clanDBID), self.clanChannelJid(), pInfo.clanAbbrev, cInfo.clanName, cInfo.clanMotto, cInfo.clanDescription, cInfo.emblemPath64x64)
        if not cInfo.emblemPath64x64 and pInfo.clanDBID > 0:
            ClanEmblemsCache.g_clanEmblemsCache.get(pInfo.clanDBID, self.__onReceiveClanEmblem, False, ClanEmblemsCache.CLAN_EMBLEM_64X64)

    def __onReceiveClanEmblem(self, id, texture, size):
        if texture:
            LOG_DEBUG('Xmpp chat: received clan emblem:', id, texture, size)
            import BWPersonality
            pInfo = BWPersonality.g_clanExtendedInfo.emblemPath64x64 = texture
            self.refreshClanInfo()

    def clanGetMembers(self):
        import BWPersonality
        self.onReceiveClanMembersDiff(BWPersonality.g_clanExtendedInfo.members)

    def onReceiveClanMembersDiff(self, membersDiff):
        if self.params:
            res = [ ('%d@%s' % (spaID, self.params['xmpp_host']), tuple(data) if data else None) for spaID, data in membersDiff.iteritems() ]
            BigWorld.XMPPChat.onHandleClanMembers(res)
        return

    def syncClanChatChannel(self):
        import BWPersonality
        LOG_TRACE('Xmpp chat: try to sync chat channel for clan: ', BWPersonality.g_initPlayerInfo.clanDBID)
        if int(BWPersonality.g_initPlayerInfo.clanDBID) > 0:
            GameServerMessenger.g_instance.syncClanChatChannel(self.__onSyncClanChatChannel)
        else:
            self.__onSyncClanChatChannel(0, 1)

    def __onSyncClanChatChannel(self, resInt, error):
        result = False
        if not error:
            result = bool(resInt)
        BigWorld.XMPPChat.onSyncClanChatChannel(self.clanChannelJid(), result)

    def editFriendList(self, userId, name, operationType):
        BigWorld.XMPPChat.editFriendList(str(userId), name, operationType)

    def editIgnoreList(self, userId, name, operationType):
        BigWorld.XMPPChat.editIgnoreList(str(userId), name, operationType)

    def getUsersChatStatus(self, usersList):
        usersList = [ str(dbid) for dbid in usersList ]
        BigWorld.XMPPChat.getUsersChatStatus(usersList)

    def setUsersChatStatus(self, usersList):
        LOG_DEBUG('Xmpp chat: setUsersChatStatus:', usersList)
        hud = GameEnvironment.getHUD()
        if hud:
            hud.setUsersChatStatus(usersList)
            return
        else:
            player = BigWorld.player()
            from Account import PlayerAccount
            if player != None and player.__class__ == PlayerAccount and player._lobbyInstance:
                player._lobbyInstance.setUsersChatStatus(usersList)
                return
            LOG_DEBUG('Xmpp chat: no hud and no lobby!')
            return

    def handleMessage(self, toJid, senderId, senderName, message):
        LOG_DEBUG('Xmpp chat: handleMessage:', toJid, senderId, senderName, message)
        hud = GameEnvironment.getHUD()
        if hud and toJid == self.__curSquadChannel:
            hud.showTextMessageFromLobby(int(senderId), MESSAGE_TYPE.BATTLE_SQUAD, message)


class MessengerActionProcessor(GameServerMessenger.ActionProcessor):

    def startClientMessenger(self, params):
        LOG_TRACE('Xmpp chat params received: ', params)
        messenger.g_xmppChatHandler.params = params
        messenger.g_xmppChatHandler.requestChatToken()

    def onNicknameByID(self, id, nickname):
        BigWorld.XMPPChat.onNicknameByID(str(id), nickname)