# Embedded file name: scripts/client/eventhandlers/clanEvents.py
import BWPersonality
import messenger
from gui.WindowsManager import g_windowsManager
from debug_utils import LOG_DEBUG, LOG_NOTE, LOG_INFO
import BigWorld
from Account import PlayerAccount
from consts import EMPTY_IDTYPELIST

def onClanMembersChanged(event):
    LOG_INFO('clan members was changed. Prev: {0}, Now: {1}'.format(event.prevob, event.ob))
    accountUI = g_windowsManager.getAccountUI()
    newMembers = event.ob.get('memberIDs')
    pInfo = BWPersonality.g_initPlayerInfo
    cInfo = BWPersonality.g_clanExtendedInfo
    if len(cInfo.members) == 0:
        if newMembers and len(newMembers) > 0:
            for dbid in newMembers:
                cInfo.members[dbid] = ['', 0]
                if accountUI:
                    accountUI.viewIFace([[{'IClanMember': {}}, [[dbid, 'account']]]])

            if messenger.g_xmppChatHandler:
                messenger.g_xmppChatHandler.onReceiveClanMembersDiff(cInfo.members)
    elif event.ob != event.prevob:
        if newMembers and len(newMembers) > 0:
            removeList = cInfo.members.keys()
            for dbid in newMembers:
                if cInfo.members.get(dbid):
                    removeList.remove(dbid)
                else:
                    _onClanMemberAdded(dbid)

            for rMember in removeList:
                _onClanMemberRemoved(rMember)

        else:
            pInfo.clanAbbrev = ''
            pInfo.clanDBID = 0
            pInfo.clanAttrs = 0
            cInfo.resetAttrs()
            if messenger.g_xmppChatHandler:
                messenger.g_xmppChatHandler.refreshClanInfo()


def onClanMemberInfo(event):
    LOG_INFO('clan member info: ', format(event.ob))
    name = event.ob.get('nickname', '')
    role = event.ob.get('role', 0)
    memberId = event.idTypeList[0][0]
    BWPersonality.g_clanExtendedInfo.members[memberId] = [name, role]
    if name and messenger.g_xmppChatHandler:
        messenger.g_xmppChatHandler.onReceiveClanMembersDiff({memberId: [name, role]})


def onClanMotto(event):
    LOG_INFO('clan motto: ', format(event.ob))
    motto = event.ob.get('clanMotto')
    if motto:
        BWPersonality.g_clanExtendedInfo.clanMotto = motto
    if messenger.g_xmppChatHandler:
        messenger.g_xmppChatHandler.refreshClanInfo()


def onClanShortInfo(event):
    LOG_INFO('clan short info: ', format(event.ob))
    info = event.ob
    BWPersonality.g_initPlayerInfo.clanAbbrev = info['clanAbbrev']
    BWPersonality.g_initPlayerInfo.clanDBID = info['clanDBID']
    BWPersonality.g_initPlayerInfo.clanAttrs = 0
    BWPersonality.g_clanExtendedInfo.clanName = info['clanName']
    BWPersonality.g_clanExtendedInfo.clanMotto = ''
    player = BigWorld.player()
    if player != None and player.__class__ == PlayerAccount and player._lobbyInstance is not None:
        player._lobbyInstance.updatePlayerInfo()
    accountUI = g_windowsManager.getAccountUI()
    if accountUI:
        accountUI.viewIFace([[{'IClanMotto': {}}, EMPTY_IDTYPELIST]])
    return


def _onClanMemberAdded(memberId):
    LOG_INFO('clan member added: ', memberId)
    BWPersonality.g_clanExtendedInfo.members[memberId] = ['', 0]
    accountUI = g_windowsManager.getAccountUI()
    if accountUI:
        accountUI.viewIFace([[{'IClanMember': {}}, [[memberId, 'account']]]])


def _onClanMemberRemoved(memberId):
    LOG_DEBUG('clan member removed: ', memberId)
    BWPersonality.g_clanExtendedInfo.members.pop(memberId)
    if messenger.g_xmppChatHandler:
        messenger.g_xmppChatHandler.onReceiveClanMembersDiff({memberId: None})
    return