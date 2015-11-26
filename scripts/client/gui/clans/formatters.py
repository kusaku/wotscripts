# Embedded file name: scripts/client/gui/clans/formatters.py
import BigWorld
from gui import makeHtmlString
from helpers.i18n import doesTextExist, makeString
from gui.clans.settings import CLAN_REQUESTED_DATA_TYPE, CLAN_MEMBERS
ERROR_SYS_MSG_TPL = '#system_messages:clans/request/errors/%s'
DUMMY_UNAVAILABLE_DATA = '--'
DUMMY_NULL_DATA = '--'

def _makeHtmlString(style, ctx = None):
    if ctx is None:
        ctx = {}
    return makeHtmlString('html_templates:lobby/clans', style, ctx)


def getHtmlLineDivider(margin = 3):
    return _makeHtmlString('lineDivider', {'margin': margin})


def formatInvitesCount(count):
    if count is None:
        count = DUMMY_UNAVAILABLE_DATA
    elif count <= 999:
        count = str(count)
    elif count <= 99999:
        count = '{}K'.format(int(count / 1000))
    else:
        count = '99K+'
    return count


def formatDataToString(data):
    if data is None:
        return DUMMY_UNAVAILABLE_DATA
    else:
        return str(data)


def formatShortDateShortTimeString(timestamp):
    return str(' ').join((BigWorld.wg_getShortDateFormat(timestamp), '  ', BigWorld.wg_getShortTimeFormat(timestamp)))


_CUSTOM_ERR_MESSAGES = {}

def getRequestErrorMsg(result, ctx):
    msgKey = (ctx.getRequestType(), result.code)
    if msgKey in _CUSTOM_ERR_MESSAGES:
        errorMsg = _CUSTOM_ERR_MESSAGES[msgKey]
    else:
        errorMsg = result.errStr
    key = ERROR_SYS_MSG_TPL % errorMsg
    if doesTextExist(key):
        return makeString(key)
    return ''


def getRequestUserName(rqTypeID):
    return _sysMsg('clan/request/name/%s' % CLAN_REQUESTED_DATA_TYPE.getKeyByValue(rqTypeID))


def getClanRoleString(position):
    if position in CLAN_MEMBERS:
        return makeString('#menu:profile/header/clan/position/%s' % CLAN_MEMBERS[position])
    return ''


def getClanRoleIcon(role):
    if role in CLAN_MEMBERS:
        return '../maps/icons/clans/roles/%s.png' % CLAN_MEMBERS[role]
    return ''


def getClanAbbrevString(clanAbbrev):
    return '[{0:>s}]'.format(clanAbbrev)


def getClanFullName(clanName, clanAbbrev):
    return '{} {}'.format(getClanAbbrevString(clanAbbrev), clanName)


def getAppSentSysMsg(clanName, clanAbbrev):
    clanFullName = '{} {}'.format(getClanAbbrevString(clanAbbrev or ''), clanName or '')
    return _sysMsg('clans/notifications/requestSent', clanName=clanFullName)


def getInvitesSentSysMsg(accountNames):
    count = len(accountNames)
    if count == 1:
        msg = _sysMsg('clans/notifications/inviteSent', userName=accountNames[0])
    else:
        msg = _sysMsg('clans/notifications/invitesSent', userCount=count)
    return msg


def _sysMsg(i18nKey, *args, **kwargs):
    return makeString(('#system_messages:%s' % i18nKey), *args, **kwargs)