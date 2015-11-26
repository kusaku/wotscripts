# Embedded file name: scripts/client/gui/clans/clan_account_profile.py
import weakref
from collections import namedtuple, defaultdict
from adisp import process
from helpers import time_utils
from account_helpers import getAccountDatabaseID
from messenger.ext import passCensor
from shared_utils import CONST_CONTAINER
from debug_utils import LOG_DEBUG
from gui.shared import g_itemsCache
from gui.clans import items, contexts, formatters as clans_fmts
from gui.clans.restrictions import ClanMemberPermissions, DefaultClanMemberPermissions
from gui.clans.settings import CLAN_REQUESTED_DATA_TYPE, COUNT_THRESHOLD, CLAN_INVITE_STATES

class _SYNC_STATE(CONST_CONTAINER):
    INVITES = 1
    APPS = 2
    CLAN_INFO = 4
    ALL = INVITES | APPS | CLAN_INFO


_ClanInfo = namedtuple('_ClanInfo', ['clanName',
 'clanAbbrev',
 'chatChannelDBID',
 'memberFlags',
 'enteringTime'])

class ClanAccountProfile(object):

    def __init__(self, clansCtrl, accountDbID, clanDbID = 0, clanBwInfo = None):
        self._clansCtrl = weakref.proxy(clansCtrl)
        self._accountDbID = accountDbID
        self._clanDbID = clanDbID
        self._clanBwInfo = clanBwInfo
        self._waitForSync = 0
        self._vitalWebInfo = defaultdict(lambda : None)

    def fini(self):
        self._waitForSync = 0
        self._vitalWebInfo.clear()

    def getPermissions(self, clanDossier):
        if clanDossier and clanDossier.getDbID() == self._clanDbID:
            return ClanMemberPermissions(self.getRole())
        return DefaultClanMemberPermissions()

    def getMyClanPermissions(self):
        if self.isInClan():
            return self.getPermissions(self.getClanDossier())
        return DefaultClanMemberPermissions()

    def getClanDossier(self):
        return self._clansCtrl.getClanDossier(self._clanDbID)

    def isSynced(self, key = None):
        if key is None:
            return len(self._vitalWebInfo) and None not in self._vitalWebInfo.values()
        else:
            return self._vitalWebInfo[key] is not None

    def getDbID(self):
        return self._accountDbID

    def getRole(self):
        return self._getClanInfoValue(3, 0)

    def getRoleUserString(self):
        return clans_fmts.getClanRoleString(self.getRole())

    def isInClan(self):
        return self._clanDbID != 0

    def getClanDbID(self):
        return self._clanDbID

    def getClanName(self):
        return passCensor(self._getClanInfoValue(0, ''))

    def getClanFullName(self):
        return '{} {}'.format(clans_fmts.getClanAbbrevString(self.getClanAbbrev()), self.getClanName())

    def getClanAbbrev(self):
        return passCensor(self._getClanInfoValue(1, ''))

    def getJoinedAt(self):
        return self._getClanInfoValue(4, 0)

    def isInClanEnterCooldown(self):
        if self._vitalWebInfo['clanInfo']:
            return time_utils.getCurrentTimestamp() - self._vitalWebInfo['clanInfo'].getClanCooldownTill() <= 0
        return False

    def getInvites(self):
        return self._vitalWebInfo.get('invites', None)

    def getApplications(self):
        return self._vitalWebInfo.get('apps', None)

    def hasClanInvite(self, clanDbID):
        if self._vitalWebInfo['invites'] is not None:
            return clanDbID in self._vitalWebInfo['invites']
        else:
            return False

    def isClanApplicationSent(self, clanDbID):
        if self._vitalWebInfo['apps'] is not None:
            return clanDbID in self._vitalWebInfo['apps']
        else:
            return False

    def getInvitesCount(self):
        self.resyncInvites()
        if self._vitalWebInfo['invites'] is not None:
            return len(self._vitalWebInfo['invites'])
        else:
            return

    def getApplicationsCount(self):
        self.resyncApps()
        if self._vitalWebInfo['apps'] is not None:
            return len(self._vitalWebInfo['apps'])
        else:
            return

    def resync(self, force = False):
        LOG_DEBUG('Full account clan profile resync initiated')
        self.resyncWebClanInfo()
        if not self.isInClan():
            self.resyncInvites(force=force)
            self.resyncApps(force=force)
        else:
            self.getClanDossier().resync(force=force)

    @process
    def resyncWebClanInfo(self, force = False):
        if self._waitForSync & _SYNC_STATE.CLAN_INFO:
            return
        elif self._vitalWebInfo['clanInfo'] is not None and not force:
            return
        else:
            self._waitForSync |= _SYNC_STATE.CLAN_INFO
            ctx = contexts.GetClanInfoCtx(self._accountDbID)
            response = yield self._clansCtrl.sendRequest(ctx)
            if response.isSuccess():
                info = ctx.getDataObj(response.data)
                if self._vitalWebInfo['clanInfo'] != info:
                    self.__changeWebInfo('clanInfo', info, 'onAccountClanInfoReceived')
            self._waitForSync ^= _SYNC_STATE.CLAN_INFO
            return

    @process
    def resyncInvites(self, force = False):
        if self._waitForSync & _SYNC_STATE.INVITES:
            return
        elif self._vitalWebInfo['invites'] is not None and not force:
            return
        else:
            self._waitForSync |= _SYNC_STATE.INVITES
            ctx = contexts.AccountInvitesCtx(self._accountDbID, 0, COUNT_THRESHOLD, [CLAN_INVITE_STATES.ACTIVE])
            response = yield self._clansCtrl.sendRequest(ctx)
            if response.isSuccess():
                invites = dict(((i.getClanDbID(), i) for i in ctx.getDataObj(response.data)))
                if self._vitalWebInfo['invites'] != invites:
                    self.__changeWebInfo('invites', invites, 'onAccountInvitesReceived')
            else:
                self.__changeWebInfo('invites', None, 'onAccountInvitesReceived')
            self._waitForSync ^= _SYNC_STATE.INVITES
            return

    @process
    def resyncApps(self, force = False):
        if self._waitForSync & _SYNC_STATE.APPS:
            return
        elif self._vitalWebInfo['apps'] is not None and not force:
            return
        else:
            self._waitForSync |= _SYNC_STATE.APPS
            ctx = contexts.AccountApplicationsCtx(self._accountDbID, 0, COUNT_THRESHOLD, [CLAN_INVITE_STATES.ACTIVE])
            response = yield self._clansCtrl.sendRequest(ctx)
            if response.isSuccess():
                apps = dict(((a.getClanDbID(), a) for a in ctx.getDataObj(response.data)))
                if self._vitalWebInfo['apps'] != apps:
                    self.__changeWebInfo('apps', apps, 'onAccountAppsReceived')
            else:
                self.__changeWebInfo('apps', None, 'onAccountAppsReceived')
            self._waitForSync ^= _SYNC_STATE.APPS
            return

    def resyncBwInfo(self):
        pass

    def processRequestResponse(self, ctx, response):
        requestType = ctx.getRequestType()
        if response.isSuccess():
            if requestType == CLAN_REQUESTED_DATA_TYPE.CREATE_APPLICATIONS:
                if len(response.data):
                    if self._vitalWebInfo['apps'] is None:
                        self._vitalWebInfo['apps'] = {}
                    for item in ctx.getDataObj(response.data):
                        item = items.ClanInviteData.fromClanCreateInviteData(item)
                        apps = self._vitalWebInfo['apps']
                        apps[item.getClanDbID()] = item
                        self.__changeWebInfo('apps', apps, 'onAccountAppsReceived')

            elif requestType == CLAN_REQUESTED_DATA_TYPE.DECLINE_INVITE:
                self.__changeInvitesState([ctx.getInviteDbID()], CLAN_INVITE_STATES.DECLINED)
            elif requestType == CLAN_REQUESTED_DATA_TYPE.DECLINE_INVITES:
                self.__changeInvitesState([ item.getDbID() for item in ctx.getDataObj(response.data) ], CLAN_INVITE_STATES.DECLINED)
            elif requestType == CLAN_REQUESTED_DATA_TYPE.ACCEPT_INVITE:
                self.__changeInvitesState([ctx.getInviteDbID()], CLAN_INVITE_STATES.ACCEPTED)
        self.getClanDossier().processRequestResponse(ctx, response)
        return

    def _getClanInfoValue(self, index, default):
        if self._clanBwInfo is not None:
            return self._clanBwInfo[index]
        else:
            return default
            return

    def _resyncBwInfo(self, clanDbID = 0, clanBwInfo = None):
        needToRaiseEvent = self._clanDbID != clanDbID or self._clanBwInfo != clanBwInfo
        self._clanDbID, self._clanBwInfo = clanDbID, clanBwInfo
        if needToRaiseEvent:
            self._clansCtrl.notify('onAccountClanProfileChanged', self)

    def __changeWebInfo(self, fieldName, value, eventName):
        self._vitalWebInfo[fieldName] = value
        self._clansCtrl.notify(eventName, value)
        self._clansCtrl.notify('onAccountWebVitalInfoChanged', fieldName, value)

    def __changeInvitesState(self, inviteIDs, state):
        self._clansCtrl.notify('onClanInvitesStateChanged', inviteIDs, state)
        self.__removeInvites(inviteIDs)

    def __removeInvites(self, inviteIDs):
        invites = self._vitalWebInfo['invites']
        if inviteIDs and invites:
            mapping = dict(((invite.getDbID(), clanId) for clanId, invite in invites.iteritems()))
            size = len(invites)
            for invID in inviteIDs:
                if invID in mapping:
                    del invites[mapping[invID]]

            if size != len(invites):
                self.__changeWebInfo('invites', invites, 'onAccountInvitesReceived')

    def __repr__(self):
        args = []
        if self.isInClan():
            args.extend(['dbID = %s' % self._clanDbID, 'abbrev = %s' % self.getClanAbbrev()])
        else:
            args.append('no clan')
        if self._vitalWebInfo['clanInfo']:
            args.append('cooldown = %s' % self._vitalWebInfo['clanInfo'].getClanCooldownTill())
        if self._vitalWebInfo['invites']:
            args.append('invites = %d' % len(self._vitalWebInfo['invites']))
        if self._vitalWebInfo['apps']:
            args.append('apps = %d' % len(self._vitalWebInfo['apps']))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(args))


class MyClanAccountProfile(ClanAccountProfile):

    def __init__(self, clansCtrl):
        stats = g_itemsCache.items.stats
        ClanAccountProfile.__init__(self, clansCtrl, getAccountDatabaseID(), stats.clanDBID, stats.clanInfo)

    def resyncBwInfo(self):
        stats = g_itemsCache.items.stats
        self._resyncBwInfo(stats.clanDBID, stats.clanInfo)