# Embedded file name: scripts/client/messenger/__init__.py
from debug_utils import LOG_ERROR
import BigWorld
from consts import MESSAGE_MAX_SIZE
from clientConsts import LOBBY_MESSAGE_MAX_SIZE
MESSENGER_OLDICT_FILE_PATH = 'localization/text/messenger_oldictionary.xml'
MESSENGER_DOMAIN_FILE_PATH = 'localization/text/messenger_dndictionary.xml'
MESSAGE_MAX_LENGTH = LOBBY_MESSAGE_MAX_SIZE
MESSAGE_MAX_LENGTH_IN_BATTLE = MESSAGE_MAX_SIZE
MESSAGE_FLOOD_COOLDOWN = 20
COLORING_FOR_BAD_WORD_FORMAT = '<font color="#00FFFF">%s</font>'
from messenger.dictionaries import ObsceneLanguageDictionary, DomainNameDictionary
g_olDictionary = ObsceneLanguageDictionary.load(MESSENGER_OLDICT_FILE_PATH)
g_dnDictionary = DomainNameDictionary.load(MESSENGER_DOMAIN_FILE_PATH)
from XmppChat import XmppChatHandler
g_xmppChatHandler = XmppChatHandler()