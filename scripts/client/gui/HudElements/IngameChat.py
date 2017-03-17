# Embedded file name: scripts/client/gui/HudElements/IngameChat.py
import BigWorld, Settings
import GameEnvironment
from Singleton import singleton
from Helpers.i18n import localizeHUD, convert as convertToLocal
from clientConsts import OBJECTS_INFO, WAIT_TIME_FOR_SEND_CHAT_MSG
from messenger.filters import FilterChain, ObsceneLanguageFilter, DomainNameFilter, SpamFilter, FloodFilter
from encodings import utf_8
from consts import MESSAGE_TYPE, BATTLE_MESSAGE_TYPE
import messenger
from debug_utils import LOG_DEBUG
from EntityHelpers import EntitySupportedClasses
MESSAGE_SAME_COOLDOWN = 2

class COLORS:
    WHITE = 16777215
    GREEN = 8443450
    YELLOW = 16761700
    RED = 14287872
    BLUE = 60159
    GREY = 13224374
    PURPLE = 8616446
    YELLOWBRIGHT = 16776960


ChatMessagesStringID = BATTLE_MESSAGE_TYPE

class CHAT_STATUS:
    INACCESSIBLE = -1
    UNDEFINED = 0
    FRIEND = 1
    IGNORED = 2


class ChatMessageVO:

    def __init__(self, authorName, authorClanAbbrev, message, isOwner, msgType, authorType, senderID, fromQueue, leaderType = -1):
        self.authorName = authorName
        self.authorClanAbbrev = authorClanAbbrev
        self.message = message
        self.isOwner = isOwner
        self.msgType = msgType
        self.authorType = authorType
        self.senderID = senderID
        self.isHistory = fromQueue
        self.leaderType = leaderType
        self.time = BigWorld.time()


class Chat:

    def __init__(self):
        self.__playersChatStatus = {}
        self.__initFilterChain()
        self.__lastSendTime = 0.0
        self.__lastMessage = ChatMessageVO('', '', '', False, 0, 0, 0, False)

    def __initFilterChain(self):
        self._filterChain = FilterChain()
        self._filterChain.addFilter('olFilter', ObsceneLanguageFilter())
        self._filterChain.addFilter('domainFilter', DomainNameFilter())
        self._filterChain.addFilter('spamFilter', SpamFilter())
        self._filterChain.addFilter('floodFilter', FloodFilter())

    def setPlayersChatStatus(self, playersList):
        for playerStatus in playersList:
            self.__playersChatStatus[playerStatus[0]] = playerStatus[1]

    def isPlayerIgnored(self, playerID):
        return self.__playersChatStatus.get(playerID) == CHAT_STATUS.IGNORED

    def broadcastMessage(self, message, messageType, messageStringID = 0, targetID = 0, toUnicode = True):
        dTime = BigWorld.time() - self.__lastSendTime
        if dTime > WAIT_TIME_FOR_SEND_CHAT_MSG:
            self.__lastSendTime = BigWorld.time()
            self.__send(message, messageType, messageStringID, targetID, toUnicode)
        else:
            LOG_DEBUG('broadcastMessage - waiting time=%s' % dTime)

    def __send(self, message, messageType, messageStringID = 0, targetID = 0, toUnicode = True):
        owner = BigWorld.player()
        if len(message) > 0 or messageStringID != 0:
            owner.cell.sendTextMessage(messageType, messageStringID, targetID, message)
            mHandler = messenger.g_xmppChatHandler
            if messageType == MESSAGE_TYPE.BATTLE_SQUAD and mHandler:
                mHandler.sendSquadMessage(message)

    def showTextMessage(self, senderID, messageType, messageStringID, targetID, message, fromQueue, leaderType = -1, isHTML = False):
        owner = BigWorld.player()
        clientArena = GameEnvironment.getClientArena()
        if owner and clientArena:
            avatarInfo = clientArena.getAvatarInfo(senderID)
            if avatarInfo:
                authorType = avatarInfo['settings'].airplane.planeType
                authorName = avatarInfo['playerName']
                if avatarInfo['classID'] == EntitySupportedClasses.AvatarBot:
                    authorName = authorName.replace('>', '&gt;')
                    authorName = authorName.replace('<', '&lt;')
                authorClanAbbrev = avatarInfo['clanAbbrev']
            else:
                LOG_DEBUG('showTextMessage - avatarInfo is None', senderID, messageType, messageStringID, targetID, message, fromQueue, leaderType)
                authorType, authorName, authorClanAbbrev = (-1, '', '')
            isOwner = senderID == owner.id
            if isOwner:
                authorName = localizeHUD('HUD_YOU_MESSAGE')
                authorClanAbbrev = ''
            if messageStringID != 0:
                message = MessagesID().getLocalizedMessage(messageStringID, targetID)
            if message:
                if not isHTML:
                    message = message.replace('>', '&gt;')
                    message = message.replace('<', '&lt;')
                from gui.WindowsManager import g_windowsManager
                if g_windowsManager.getBattleUI():
                    messageT = ChatMessageVO(authorName, authorClanAbbrev, message, isOwner, messageType, authorType, senderID, fromQueue, leaderType)
                    if messageT.senderID == self.__lastMessage.senderID and messageT.msgType == self.__lastMessage.msgType and messageT.message == self.__lastMessage.message and messageT.time - self.__lastMessage.time < MESSAGE_SAME_COOLDOWN:
                        return
                    g_windowsManager.getBattleUI().addChatMessage(ChatMessageVO(authorName, authorClanAbbrev, message, isOwner, messageType, authorType, senderID, fromQueue, leaderType))
                    self.__lastMessage = messageT

    def filterMessage(self, text, userUid):
        owner = BigWorld.player()
        if owner and owner.id != userUid:
            if Settings.g_instance.getXmppChatSettings()['messageFilterEnabled']:
                result = self._filterChain.chainIn(convertToLocal(text), userUid, BigWorld.time())
                return utf_8.encode(result)[0]
        return text


@singleton

class MessagesID(object):

    def __init__(self):
        self.__localize = {ChatMessagesStringID.GOT_IT: 'CHAT_COMMAND_F2',
         ChatMessagesStringID.FAILURE: 'CHAT_COMMAND_F3',
         ChatMessagesStringID.NEED_SHELTER: 'CHAT_COMMAND_F4',
         ChatMessagesStringID.SOS: 'CHAT_COMMAND_F5',
         ChatMessagesStringID.JOIN_ME: 'CHAT_COMMAND_F8',
         ChatMessagesStringID.ENEMY_MY_AIM: 'CHAT_COMMAND_F9'}

    def getLocalizedMessage(self, messageStringID, targetID = 0):
        if messageStringID not in self.__localize:
            return 'ERROR LOCALIZE MESSAGE'
        elif targetID != 0 and messageStringID in [ChatMessagesStringID.JOIN_ME, ChatMessagesStringID.ENEMY_MY_AIM]:
            objectType = GameEnvironment.getClientArena().getTeamObjectType(targetID)
            if objectType is not None and objectType in OBJECTS_INFO:
                objectName = localizeHUD(OBJECTS_INFO[objectType]['LOC_ID'])
            else:
                objectName = GameEnvironment.getClientArena().getObjectName(targetID)
            return localizeHUD(self.__localize[messageStringID]).format(player=objectName)
        else:
            return localizeHUD(self.__localize[messageStringID])
            return