# Embedded file name: scripts/client/gui/clans/clan_controller.py
from collections import defaultdict
from gui.clans import contexts
from gui.clans.clan_account_profile import MyClanAccountProfile
from gui.clans.settings import CLAN_INVITE_STATES, CLAN_REQUESTED_DATA_TYPE, CLAN_APPLICATION_STATES
from gui.clans.users import UserCache
from adisp import async, process
from gui import SystemMessages
from gui.LobbyContext import g_lobbyContext
from gui.ClientUpdateManager import g_clientUpdateManager
from gui.clans import formatters as clan_formatters, items
from gui.clans.states import ClanUndefinedState
from gui.clans.subscriptions import ClansListeners

def _showError(result, ctx):
    i18nMsg = clan_formatters.getRequestErrorMsg(result, ctx)
    if i18nMsg:
        SystemMessages.pushMessage(i18nMsg, type=SystemMessages.SM_TYPE.Error)


class _ClanDossier(object):

    def __init__(self, clanDbID, clansCtrl, isMy):
        self._clansCtrl = clansCtrl
        self.__isMy = isMy
        self.__clanDbID = clanDbID
        self.__cache = {}
        self.__processingRequests = defaultdict(list)
        self.__vitalInfo = defaultdict(lambda : None)
        self.__waitForSync = 0
        self.__appsCountWaitForSync = 0

    def fini(self):
        self._clansCtrl = None
        self.__cache.clear()
        self.__vitalInfo.clear()
        self.__waitForSync = 0
        self.__appsCountWaitForSync = 0
        return

    def isSynced(self, key = None):
        if key is None:
            return len(self.__vitalInfo) and None not in self.__vitalInfo.values()
        else:
            return self.__vitalInfo[key] is not None

    def isDataReceived(self, infoID):
        return infoID in self.__cache

    def getDbID(self):
        return self.__clanDbID

    def isMyClan(self):
        return self.__isMy

    def canIHandleClanInvites(self):
        return self.getLimits().canHandleClanInvites(self).success

    def isClanValid(self):
        return self.__clanDbID != 0

    def getLimits(self):
        return self._clansCtrl.getLimits()

    @process
    def resync(self, force = False):
        if self.__cantResync(force, self.__waitForSync):
            return
        else:
            self.__waitForSync = True
            clanInfo = yield self.requestClanInfo()
            self.__changeWebInfo('clanInfo', clanInfo, 'onClanInfoReceived')
            if self.__isMy and self.canIHandleClanInvites():
                invitesCount = yield self.requestInvitationsCount()
                self.__changeWebInfo('invitesCount', invitesCount, 'onClanInvitesCountReceived')
                self.requestAppsCount(force)
            else:
                self.__vitalInfo['invitesCount'] = None
            self.__waitForSync = False
            return

    @process
    def requestAppsCount(self, force = False):
        if self.__cantResync(force, self.__appsCountWaitForSync):
            return
        else:
            if self.__isMy and self.canIHandleClanInvites():
                appsCount = yield self.requestApplicationsCount(isForced=force)
                appsCountName = 'appsCount'
                if self.__vitalInfo[appsCountName] != appsCount:
                    self.__changeWebInfo(appsCountName, appsCount, 'onClanAppsCountReceived')
            else:
                self.__vitalInfo['appsCount'] = None
            self.__appsCountWaitForSync = False
            return

    def getClanInfo(self):
        self.resync()
        return self.__vitalInfo['clanInfo'] or items.ClanExtInfoData()

    def canAcceptsJoinRequests(self):
        return self.getClanInfo().isOpened()

    def getInvitesCount(self):
        self.resync()
        return self.__vitalInfo['invitesCount']

    def getAppsCount(self):
        self.resync()
        return self.__vitalInfo['appsCount']

    @async
    def requestClanInfo(self, callback):
        self.__doRequest(contexts.ClanInfoCtx(self.__clanDbID), callback)

    @async
    @process
    def requestClanRatings(self, callback):
        result = yield self.__requestClanRatings()
        if len(result) > 0:
            callback(result[0])
        else:
            callback(items.ClanRatingsData())

    @async
    def requestGlobalMapStats(self, callback):
        self.__doRequest(contexts.ClanGlobalMapStatsCtx(self.__clanDbID), callback)

    @async
    def requestStrongholdInfo(self, callback):
        self.__doRequest(contexts.StrongholdInfoCtx(self.__clanDbID), callback)

    @async
    def requestStrongholdStatistics(self, callback):
        self.__doRequest(contexts.StrongholdStatisticsCtx(self.__clanDbID), callback)

    @async
    def requestInvitationsCount(self, callback):
        self.__doRequest(contexts.GetClanInvitesCount(self.__clanDbID, statuses=[CLAN_INVITE_STATES.ACTIVE]), callback)

    @async
    def requestApplicationsCount(self, callback, isForced):
        self.__doRequest(contexts.GetClanAppsCount(self.__clanDbID, not isForced, statuses=[CLAN_INVITE_STATES.ACTIVE]), callback)

    @async
    def requestMembers(self, callback):
        self.__doRequest(contexts.ClanMembersCtx(self.__clanDbID), callback)

    @async
    def requestProvinces(self, callback):
        self.__doRequest(contexts.GetProvincesCtx(self.__clanDbID), callback)

    @async
    def requestFavouriteAttributes(self, callback):
        self.__doRequest(contexts.ClanFavouriteAttributesCtx(self.__clanDbID), callback)

    @async
    def __requestClanRatings(self, callback):
        self.__doRequest(contexts.ClanRatingsCtx([self.__clanDbID]), callback)

    @process
    def __doRequest(self, ctx, callback):
        requestType = ctx.getRequestType()
        if requestType not in self.__cache:
            if requestType not in self.__processingRequests:
                self.__processingRequests[requestType].append(callback)
                result = yield self._clansCtrl.sendRequest(ctx)
                if result.isSuccess():
                    formattedData = ctx.getDataObj(result.data)
                    if ctx.isCaching():
                        self.__cache[requestType] = formattedData
                else:
                    formattedData = ctx.getDefDataObj()
                for cb in self.__processingRequests[requestType]:
                    cb(formattedData)

                del self.__processingRequests[requestType]
            else:
                self.__processingRequests[requestType].append(callback)
        else:
            callback(self.__cache[requestType])

    def processRequestResponse(self, ctx, response):
        requestType = ctx.getRequestType()
        if response.isSuccess():
            if requestType == CLAN_REQUESTED_DATA_TYPE.DECLINE_APPLICATION or requestType == CLAN_REQUESTED_DATA_TYPE.ACCEPT_APPLICATION:
                appsCountName = 'appsCount'
                newVal = self.__vitalInfo[appsCountName] - 1
                if newVal >= 0:
                    self.__changeWebInfo(appsCountName, newVal, 'onClanAppsCountReceived')
                if requestType == CLAN_REQUESTED_DATA_TYPE.DECLINE_APPLICATION:
                    state = CLAN_APPLICATION_STATES.DECLINED
                else:
                    state = CLAN_APPLICATION_STATES.ACCEPTED
                self._clansCtrl.notify('onClanAppStateChanged', ctx.getApplicationDbID(), state)

    def __changeWebInfo(self, fieldName, value, eventName):
        self.__vitalInfo[fieldName] = value
        self._clansCtrl.notify(eventName, self.__clanDbID, value)
        self._clansCtrl.notify('onClanWebVitalInfoChanged', self.__clanDbID, fieldName, value)

    def __cantResync(self, force, waitForSync):
        return not self.isClanValid() or waitForSync or self.isSynced() and not force

    def __repr__(self):
        return 'ClanDossier(dbID = %d, my = %s, web = %s, cache = %s)' % (self.__clanDbID,
         self.__isMy,
         self.__vitalInfo,
         self.__cache.keys())


class _ClanController(ClansListeners):

    def __init__(self):
        super(_ClanController, self).__init__()
        self.__cache = {}
        self.__searchDataCache = {}
        self.__state = None
        self.__profile = None
        self.__userCache = UserCache(self)
        self.__simWGCGEnabled = True
        return

    def simEnableWGCG(self, enable):
        self.__simWGCGEnabled = enable
        if self.__profile:
            self.__profile.resync(force=True)

    def simEnableClan(self, enable):
        settings = g_lobbyContext.getServerSettings()
        clanSettings = {'clanProfile': {'isEnabled': enable,
                         'gateUrl': settings.clanProfile.getSettingsJSON()}}
        settings.update(clanSettings)
        g_clientUpdateManager.update({'serverSettings': clanSettings})

    def simWGCGEnabled(self):
        return self.__simWGCGEnabled

    def init(self):
        self.__state = ClanUndefinedState(self)
        self.__state.init()

    def fini(self):
        self.stop()
        self.__state.fini()
        self.__state = None
        self.__userCache = None
        self.__cleanDossiers()
        return

    def start(self):
        self.__profile = MyClanAccountProfile(self)
        g_clientUpdateManager.addCallbacks({'stats.clanInfo': self.__onClanInfoChanged,
         'serverSettings.clanProfile.isEnabled': self.__onServerSettingChanged})
        self.invalidate()

    def stop(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        if self.__profile is not None:
            self.__profile.fini()
            self.__profile = None
        self.__state.logout()
        return

    def invalidate(self):
        self.__state.update()

    def getClanDossier(self, clanDbID = None):
        if clanDbID not in self.__cache:
            dossier = self.__cache[clanDbID] = _ClanDossier(clanDbID, self, isMy=clanDbID == self.__profile.getClanDbID())
        else:
            dossier = self.__cache[clanDbID]
        return dossier

    def resyncLogin(self, forceLogin = False):
        perms = self.__profile.getMyClanPermissions()
        if forceLogin or perms.canHandleClanInvites() and perms.canTrade() and perms.canExchangeMoney():
            self.__state.login()

    @async
    @process
    def sendRequest(self, ctx, callback, allowDelay = None):
        result = yield self.__state.sendRequest(ctx, allowDelay=allowDelay)
        if self.__profile is not None:
            self.__profile.processRequestResponse(ctx, result)
        if not result.isSuccess():
            _showError(result, ctx)
        callback(result)
        return

    def getStateID(self):
        return self.__state.getStateID()

    def isEnabled(self):
        return g_lobbyContext.getServerSettings().clanProfile.isEnabled()

    def isAvailable(self):
        return self.__state.isAvailable()

    def getWebRequester(self):
        return self.__state.getWebRequester()

    def getAccountProfile(self):
        return self.__profile

    def getLimits(self):
        return self.__state.getLimits(self.__profile)

    def changeState(self, state):
        oldState = self.__state
        self.__state = state
        self.notify('onClanStateChanged', oldState.getStateID(), state.getStateID())

    def onStateUpdated(self):
        if self.__state.isLoggedOn():
            self.__profile.resync()

    def isLoggedOn(self):
        return self.__state.isLoggedOn()

    def updateClanCommonDataCache(self, cache):
        for item in cache or {}:
            self.__searchDataCache[item.getDbID()] = item

    def clearClanCommonDataCache(self):
        self.__searchDataCache = {}

    def getClanCommonData(self, clanDbID):
        return self.__searchDataCache.get(clanDbID, None)

    @async
    @process
    def requestUsers(self, dbIDs, callback):
        result = yield self.__userCache.requestUsers(dbIDs)
        callback(result)

    def __onClanInfoChanged(self, _):
        self.__profile.resyncBwInfo()
        self.resyncLogin()

    def __onServerSettingChanged(self, *args):
        self.invalidate()

    def __cleanDossiers(self):
        for k, v in self.__cache.iteritems():
            v.fini()

        self.__cache.clear()

    def __repr__(self):
        return 'ClanCtrl(state = %s, profile = %s)' % (str(self.__state), self.__profile)


g_clanCtrl = _ClanController()