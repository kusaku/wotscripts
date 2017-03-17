# Embedded file name: scripts/client/Account.py
from functools import partial
import time
import cPickle
import zlib
import weakref
import collections
import BigWorld
import Settings
import Keys
from Event import Event, EventManager
from Helpers.AccountOperationsMgr import AccountOperationsMgr, ifaceDataCallback
from Helpers.i18n import localizeLobby, localizeMessages
from OperationCodes import OPERATION_CODE
from clientConsts import GUI_TYPES, HANGAR_MODE, GUI_TYPES_DICT
import config_consts
from consts import RESPONSE_TYPE, ECONOMICS_PROMO_PARAMS, EMPTY_IDTYPELIST, PLANE_MARKET_STATUS, TUTORIAL_QUEUE_SHOW_WAITING_AVG_TIME, PKG_SEND_INTERVAL, PREBATLE_DATA, WAITING_INFO_TYPE, MAX_SEND_DATA_SIZE, ALLOW_CREDIT_BUYS, MESSAGE_TYPE
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_ERROR, LOG_DEBUG, LOG_TRACE, LOG_INFO, LOG_NOTE, LOG_WARNING, LOG_MX, LOG_INFO_FORMAT
from exchangeapi.ErrorCodes import SUCCESS
from gui.Scaleform.Waiting import Waiting
from gui.Scaleform.utils.HangarSpace import g_hangarSpace
from gui.WindowsManager import g_windowsManager
from ConnectionManager import connectionManager
import ClientLog
import GameServerMessenger
import GlobalEvents
import VOIP
import messenger
from consts import DB_MODULE_NAMES
import wgPickle
import consts
import db.DBLogic
import BWPersonality
from gui.Scaleform.LobbyCarouselHelper import LobbyCarouselHelper
from gui.Scaleform.PartSender import PartSender
from Operations.OperationReceiver import OperationReceiver
from exchangeapi.CommonUtils import splitIDTypeList, joinIDTypeList, listFromId, METHODTOINDEX, convertIfaceDataFromUI
from exchangeapi.AdapterUtils import getAdapter
from Helpers.InterfaceSenderQueue import InterfaceSenderQueue
from exchangeapi.UICallbackUtils import UI_CALLBACKS
from Helpers.cache import deleteFromCache, getFromCache, setToCache
from gui.Scaleform.windows import GUIWindowAccount
import _economics
from Helpers.reliableDelivery import clearMappedCallbacks
from eventhandlers.responseEvents import disposePackageChain, startPackageChain
from Helpers.TokenManager import TokenManager
from adapters.IHangarSpacesAdapter import getDefaultSpaceID, getHangarSpaceByID
from HelperFunctions import createIMessage
from CrewHelpers import DEFAULT_BOT_AVATAR_BODY_TYPE
import operator
import _warAction
DATA_STORAGE = {'ifaces': {}}
PLANE_BLOCK_TYPE = {}
WAIT_ARENA_CREATON_TIME = 30.0

class PlayerAccount(BigWorld.Entity):

    def debugViewer_addNewKey(self, dvKey, str_data):
        from debug.layer0.DebugViewer.Debug_View_Manager import DebugViewManager
        DebugViewManager().addNewKey(dvKey, str_data)

    def debugViewer_removeKey(self, dvKey):
        from debug.layer0.DebugViewer.Debug_View_Manager import DebugViewManager
        DebugViewManager().removeKey(dvKey)

    def debugViewer_pushToView(self, str_data):
        from debug.layer0.DebugViewer.Debug_View_Manager import DebugViewManager
        DebugViewManager().pushToView(str_data)

    def __init__(self):
        self.isInTutorialQueue = False
        self.__lastProcessedPkgCallback = None
        self.__spaceUnloadCallback = None
        self.__lastProcessedPkgIndex = -1
        self.__waitVoipClientStatus = False
        self.tokenManager = TokenManager()
        self.__wasLogin = False
        self.__dynamicHangarUpdateCallback = None
        self.__queueVSECallback = None
        self.__queueVSEData = collections.deque()
        return

    def version_177(self):
        pass

    def isPendingResponses(self):
        pass

    @property
    def _lobbyInstance(self):
        return g_windowsManager.getLobbyUI()

    @property
    def __prebattleInstance(self):
        return g_windowsManager.getPrebatleUI()

    def onStreamComplete(self, id, data):
        try:
            streamID, response = cPickle.loads(zlib.decompress(data))
            if streamID == consts.STREAM_CLIENT.STREAM_ID_RESPONSE:
                responseType, sequenceId, invocationId, returnCode, responseData = response
                self.clientReceiveResponse(responseType, sequenceId, invocationId, returnCode, responseData)
            elif streamID == consts.STREAM_CLIENT.STREAM_ID_TRAINING_ROOM_LIST:
                self.refreshRoomListResponse(response)
            elif streamID == consts.STREAM_CLIENT.STREAM_ID_TRAINING_ROOM_DATA:
                dataType, sequenceID, sessionID, pickledData = response
                self.updateTrainingRoom(dataType, sequenceID, sessionID, pickledData)
        except:
            LOG_ERROR('onStreamComplete id', id)
            LOG_CURRENT_EXCEPTION()
            connectionManager.disconnect()

    def receivePlayerInfo(self, initPlayerInfoMap):
        databaseID = getattr(initPlayerInfoMap, 'databaseID', BWPersonality.g_initPlayerInfo.databaseID)
        if databaseID != BWPersonality.g_initPlayerInfo.databaseID:
            BWPersonality.g_commandsFiredCounter.reset()
        info = BWPersonality.g_initPlayerInfo
        info.update(initPlayerInfoMap)
        Settings.g_instance.contactInfo.updateAccountName(info.accountName)
        Settings.g_instance.save()
        LOG_INFO_FORMAT(self, 'receivePlayerInfo: serverRunTime={0}; updatePlayerInfoResponse={1}; initPlayerInfoMap: {2}', BigWorld.stime(), time.ctime(info.serverLocalTime), initPlayerInfoMap)
        BWPersonality.g_settings.hangarSpaceSettings = BWPersonality.g_settings.getHangarSpaceSettings(info.databaseID)
        SKIP_CLIENT_DIFFTIME = 30
        deltaTimeClientServer = int(time.time()) - info.serverLocalTime
        if abs(deltaTimeClientServer) < SKIP_CLIENT_DIFFTIME:
            deltaTimeClientServer = 0
        self.deltaTimeClientServer = deltaTimeClientServer
        info.isDeveloper = info.isDeveloper and consts.IS_DEBUG_IMPORTED
        from Helpers import cache
        cache.init()
        self.checkLocalizationLanguage()
        BigWorld.Screener.setUserId(info.databaseID)
        info.premiumExpiryTime = -1 if info.premiumExpiryTime < info.serverLocalTime else info.premiumExpiryTime + self.deltaTimeClientServer
        self._updatePremiumCost(info.premiumCost)
        if BWPersonality.g_lobbyInterview[0] and info.useGUIType != GUI_TYPES.EMPTY and BWPersonality.g_lastMapID != -1 and BWPersonality.g_lastBattleType != consts.ARENA_TYPE.TUTORIAL:
            g_windowsManager.showInterview()
        else:
            self.receivePlayerInfoPostProcess()
        BWPersonality.gameParams = BWPersonality.g_initPlayerInfo.gameParams.copy()

    def receivePlayerInfoPostProcess(self):
        if self.__wasLogin:
            self.__wasLogin = False
        else:
            startPackageChain()
        self.__updateLastProcessedPkg()
        connectionManager.onDisconnected += self.__stopPackageChain
        info = BWPersonality.g_initPlayerInfo
        if info.useGUIType == GUI_TYPES.NORMAL or info.useGUIType == GUI_TYPES.PREMIUM:
            if info.premiumExpiryTime > info.serverLocalTime:
                self.premiumExpiryTime = info.premiumExpiryTime
            LOG_DEBUG('g_windowsManager.showLobby')
            g_windowsManager.showLobby()
            self.__isLobbyLoading = True
            BWPersonality.g_lobbyCarouselHelper.syncServData()
        elif info.useGUIType == GUI_TYPES.EMPTY:
            g_windowsManager.closeCurMovie()
        self.__currentSequence = info.responseSequence
        self.__checkClientReceiveResponse()
        self.__initGlobalGamesPlayed()
        VOIP.initialize(info.databaseID)
        BWPersonality.g_waitingInfoHelper.updateWaitingStats()

    def _updatePremiumCost(self, newCost):
        premDayTag = {1: 'BUY_PREMIUM_1_DAY',
         3: 'BUY_PREMIUM_3_DAY',
         7: 'BUY_PREMIUM_1_WEEK',
         30: 'BUY_PREMIUM_1_MONTH',
         180: 'BUY_PREMIUM_6_MONTH',
         360: 'BUY_PREMIUM_12_MONTH'}
        BWPersonality.g_premiumData = [ dict(days=prem['days'], cost=prem['cost'], currency=consts.PAYMENT_TYPE_STR[prem['currency']], isEnabled=True, localizedDays=localizeLobby(premDayTag[prem['days']])) for prem in newCost ]
        lobby = self._lobbyInstance
        if lobby is not None:
            self.resendIfaces(['IPremiumCost'])
            lobby.updatePremiumInfo()
        return

    def resendIfaces(self, interfaceList, oblocationTypes = None, callback = None):
        request = []
        for ids, idsValue in UI_CALLBACKS.iteritems():
            for types, typesValue in idsValue.iteritems():
                for iface in typesValue.iterkeys():
                    if interfaceList is None or iface in interfaceList:
                        idTypeList = joinIDTypeList(listFromId(ids), listFromId(types))
                        from exchangeapi.AdapterUtils import getOblocation
                        if oblocationTypes is None or getOblocation(iface, listFromId(types)) in oblocationTypes:
                            deleteFromCache(idTypeList, iface)
                            request.append([{iface: {}}, idTypeList])

        if request:

            def _onResponse(respdata):
                GUIWindowAccount.obdataResponse(None, None, weakref.ref(self._lobbyInstance), [[int(consts.IS_CLIENT), METHODTOINDEX['view']], respdata, SUCCESS])
                if callback:
                    callback()
                return

            accountUI = g_windowsManager.getAccountUI()
            if accountUI:
                accountUI.viewIFace(convertIfaceDataFromUI(request), dbgCallback=_onResponse)
        return

    def responseSender(self, idTypeList, ifacename, ob, code = SUCCESS, method = 'edit'):
        from exchangeapi.CommonUtils import METHODTOINDEX
        if code == SUCCESS:
            idList, typeList = splitIDTypeList(idTypeList)
            ob = getAdapter(ifacename, typeList)(self, ob, idTypeList=idTypeList)
        self.processIfaceData(None, None, [[int(consts.IS_CLIENT), METHODTOINDEX[method]], [[{ifacename: ob}, idTypeList]], code])
        return

    def __onReceiveOperation(self, operation):
        self.operationCmdHandlers[operation.operationCode](operation)

    def __handleSetIfaceData(self, operation, args = None):
        if operation is None:
            ifaceDataCallback(self.processIfaceData, None, None, args[0])
        else:
            ifaceDataCallback(self.processIfaceData, None, None, operation.args[0])
            operation.destroy()
        return

    def processIfaceData(self, op, code, respob):
        global DATA_STORAGE
        headers, respdata, code = respob
        if code == 0:
            if self.ifaceHandler and not DATA_STORAGE['ifaces']:
                self.ifaceHandler(headers, respdata)
            else:
                from exchangeapi.CommonUtils import idFromList
                for ifaces, idTypeList in respdata:
                    idList, typeList = splitIDTypeList(idTypeList)
                    ids = idFromList(idList)
                    types = idFromList(typeList)
                    queryData = dict(((ifacename, data) for ifacename, data in ifaces.iteritems()))
                    DATA_STORAGE['ifaces'].setdefault(BWPersonality.g_initPlayerInfo.databaseID, {}).setdefault(ids, {}).setdefault(types, []).append((queryData, headers))

    def __handleLastSessionKey(self, operation):
        key, changeKey = operation.args
        changeKey = changeKey or getattr(self, 'forceChangeSessionKey', False)
        self.forceChangeSessionKey = False
        from Helpers.cache import isSessionKeyValid, deleteCache, getSessionKey
        if not isSessionKeyValid(key):
            LOG_DEBUG('invalidate cache...')
            clientSessionKey = getSessionKey()
            deleteCache()
            if not clientSessionKey:
                LOG_DEBUG('get new session key...')
                self.accountCmd.getNewSessionKey(self.__newSessionKeyResponse)
            else:
                LOG_DEBUG('save session key...')
                from Helpers.cache import saveSessionKey
                self.accountCmd.saveSessionKey(clientSessionKey)
                saveSessionKey(clientSessionKey)
        elif changeKey:
            LOG_DEBUG('get new session key...')
            deleteCache()
            self.accountCmd.getNewSessionKey(self.__newSessionKeyResponse)
        else:
            self.accountCmd.sessionKeySynced()
            startPackageChain()
        operation.destroy()

    def __newSessionKeyResponse(self, operation, resultID, *args):
        sessionKey = args[0]
        from Helpers.cache import saveSessionKey
        saveSessionKey(sessionKey)
        self.accountCmd.saveSessionKey(sessionKey)

    def __handleActionListChanged(self, operation):
        self.syncActionList()
        promoActions = operation.args[0]
        economics = promoActions.get(DB_MODULE_NAMES.ECONOMICS, None)
        if economics and BWPersonality.g_lobbyCarouselHelper.inventory.inventoryDataInitialized:
            for planeID in BWPersonality.g_lobbyCarouselHelper.inventory.getBoughtAircraftsList():
                BWPersonality.g_lobbyCarouselHelper.inventory.setDailyFirstWinRemains(planeID, economics[ECONOMICS_PROMO_PARAMS.FIRST_DAILY_WIN_BONUS_REMAINS][planeID])
                BWPersonality.g_lobbyCarouselHelper.inventory.setDailyFirstWinXPCoeff(planeID, economics[ECONOMICS_PROMO_PARAMS.FIRST_DAILY_WIN_BONUS_XP_COEFF])
                BWPersonality.g_lobbyCarouselHelper.refreshAircraftData(planeID, True)

        operation.destroy()
        return

    def syncActionList(self):
        if self.__isSyncingActions:
            LOG_TRACE('syncActionList() already syncing')
            self.__resyncActions = True
            return
        else:
            LOG_TRACE('syncActionList() start syncing')
            self.__isSyncingActions = True
            self.__resyncActions = False
            inv = BWPersonality.g_lobbyCarouselHelper.inventory
            patchTypes = ['goldPrice',
             'plane',
             'consumable',
             'equipment',
             'ammobelt']
            replaceIfaces = ['ICrewSkillsDropCost',
             'ICrewSpecializationRetrainCost',
             'ICrewSpecializationResearchCost',
             'IBarrackPrice',
             'IPriceSchemes',
             'IPlaneBirthdayEnabled',
             'ITicketPlanes']

            def currentPatchResp(oldPatchID, respdata):
                patchID = respdata[0][0]['ICurrentPatch']['patchID']
                setToCache([[None, 'patch']], 'ICurrentPatch', {'patchID': oldPatchID})

                def queryModulePrices(newPrices, moduleType):
                    sellPrices = {}

                    def genRequest():
                        for moduleId, (cr, gd, tk) in newPrices.iteritems():
                            idTypeList = [[moduleId, moduleType]]
                            currentPrice = getFromCache(idTypeList, 'IPrice')
                            if moduleType in ALLOW_CREDIT_BUYS:
                                data = {'price': [gd * _economics.Economics.goldRateForCreditBuys if gd else cr, gd]}
                            else:
                                data = {'price': [0 if gd else cr, gd]}
                            if data == currentPrice:
                                continue
                            LOG_TRACE('syncActionList() genRequest() updating price: {0}, {1}'.format(idTypeList, data))
                            setToCache(idTypeList, 'IPrice', data)
                            yield [{'IPrice': {}}, idTypeList]
                            if moduleType == 'plane':
                                deleteFromCache(idTypeList, 'ITicketPrice')
                                setToCache(idTypeList, 'ITicketPrice', {'ticketPrice': tk})
                                yield [{'ITicketPrice': {}}, idTypeList]
                                status = getFromCache(idTypeList, 'IStatus')
                                if status is not None and status['status'] == PLANE_MARKET_STATUS.BOUGHT:
                                    setSellPrice = True
                                else:
                                    setSellPrice = False
                            else:
                                setSellPrice = True
                            if setSellPrice:
                                currentSellPrices = sellPrices.setdefault(moduleType, {})
                                deleteFromCache(idTypeList, 'ISellPrice')
                                sellPrice = (tk * _economics.Economics.creditsTicketSellPrice + gd * _economics.Economics.goldRateForCreditBuys if gd or tk else cr) * _economics.Economics.sellCoeff
                                data = {'credits': sellPrice}
                                currentSellPrices[moduleId] = sellPrice
                                setToCache(idTypeList, 'ISellPrice', data)
                                yield [{'ISellPrice': {}}, idTypeList]

                        return

                    if moduleType != 'goldPrice':
                        self._lobbyInstance.viewIFace(list(genRequest()), cacheResponse=False)
                    if moduleType == 'goldPrice':
                        _economics.Economics.goldPrice = newPrices['goldPrice']
                        self._lobbyInstance.updateGoldRate()
                    elif moduleType == 'plane':
                        inv.setAircrafsPrices(newPrices, sellPrices.get('plane', {}))
                        updatePlanePrices()

                def updatePlanePrices():
                    if self._lobbyInstance:
                        if self._lobbyInstance.mode == HANGAR_MODE.RESEARCH:
                            self._lobbyInstance.researchTreeHelper.reloadCurrentBranch()
                        if self._lobbyInstance.lobbyModulesTreeHelper.initialized:
                            self._lobbyInstance.lobbyModulesTreeHelper.updateAircraftInfo()
                            self._lobbyInstance.lobbyModulesTreeHelper.updateAircraftNodePrices()
                        for planeID in inv.getBoughtAircraftsList():
                            BWPersonality.g_lobbyCarouselHelper.refreshAircraftData(planeID, True)

                def patchResp(respdata):
                    if not self._lobbyInstance:
                        LOG_TRACE('syncActionList() patchResp() no lobby instance')
                        self.__doneSyncActionList()
                        return
                    else:
                        for patch in respdata:
                            if patch[1][0][1] != 'patch':
                                for ifaceName in patch[0].iterkeys():
                                    LOG_TRACE('syncActionList() patchResp() view iface: {0}, {1}'.format(ifaceName, patch[1]))
                                    self._lobbyInstance.viewIFace([[{ifaceName: {}}, patch[1]]], cacheResponse=False)

                                continue
                            if len(patch[1]) == 1:
                                self._updatePremiumCost(patch[0]['IPatch']['patchData']['premiumCost'])
                            else:
                                LOG_TRACE('syncActionList() patchResp() querying module prices: {0}, {1}'.format(patch[0]['IPatch']['patchData'], patch[1][1][1]))
                                queryModulePrices(patch[0]['IPatch']['patchData'], patch[1][1][1])

                        setToCache([[None, 'patch']], 'ICurrentPatch', {'patchID': patchID})
                        self.__doneSyncActionList()
                        return

                def processComponentsData(accountUI, data):
                    for component in data or []:
                        ids, types, ifacename = component
                        if ifacename == 'IRentConf':
                            for planeID in component[0]:
                                deleteFromCache([[planeID, component[1][0]]], ifacename)
                                accountUI.viewIFace([[{ifacename: {}}, [[planeID, component[1][0]]]]])

                        elif ifacename == 'IExchangeXPRate':
                            deleteFromCache(EMPTY_IDTYPELIST, ifacename)
                            accountUI.viewIFace([[{ifacename: {}}, EMPTY_IDTYPELIST]])

                queried = False
                if patchID != oldPatchID:
                    accountUI = g_windowsManager.getAccountUI()
                    if accountUI:
                        LOG_TRACE('syncActionList() new patchID: {0}, old: {1}'.format(patchID, oldPatchID))
                        query = [[{'IPatch': {}}, [[patchID, 'patch']]]] + [ [{'IPatch': {}}, [[patchID, 'patch'], [None, x]]] for x in patchTypes ]
                        deleteFromCache([[0, 'slot']], 'IPrice')
                        query += [[{'IPrice': {}}, [[0, 'slot']]]]
                        deleteFromCache([[None, 'slot']], 'IPrice')
                        query += [[{'IPrice': {}}, [[None, 'slot']]]]
                        for ifaceName in replaceIfaces:
                            deleteFromCache(EMPTY_IDTYPELIST, ifaceName)
                            query += [[{ifaceName: {}}, EMPTY_IDTYPELIST]]

                        idTypeList = [[None, 'patch']]
                        processComponentsData(accountUI, getFromCache(idTypeList, 'IComponents'))
                        deleteFromCache(idTypeList, 'IComponents')
                        if patchID is not None:
                            processComponentsData(accountUI, respdata[0][0]['ICurrentPatch']['components'])
                            setToCache(idTypeList, 'IComponents', respdata[0][0]['ICurrentPatch']['components'])
                        LOG_TRACE('syncActionList() querying patches: {0}'.format(query))
                        accountUI.viewIFace(query, dbgCallback=patchResp)
                        queried = True
                    else:
                        LOG_ERROR('syncActionList() FAILED. accountUI not found')
                else:
                    if self._lobbyInstance:
                        goldPrice = getFromCache([[patchID, 'patch'], [None, 'goldPrice']], 'IPatch')
                        if goldPrice is not None:
                            _economics.Economics.goldPrice = goldPrice['patchData']['goldPrice']
                            self._lobbyInstance.updateGoldRate()
                    LOG_TRACE('syncActionList() patchID is equal to an old one: {0}'.format(patchID))
                if not queried:
                    self.__doneSyncActionList()
                return

            idTypeList = [[None, 'patch']]
            oldPatch = getFromCache(idTypeList, 'ICurrentPatch')
            deleteFromCache(idTypeList, 'ICurrentPatch')
            oldPatchID = oldPatch['patchID'] if oldPatch is not None else oldPatch
            accountUI = g_windowsManager.getAccountUI()
            if accountUI:
                accountUI.viewIFace([[{'ICurrentPatch': {}}, idTypeList]], dbgCallback=partial(currentPatchResp, oldPatchID))
            return

    def __doneSyncActionList(self):
        LOG_TRACE('__doneSyncActionList()')
        self.__isSyncingActions = False
        if self.__resyncActions:
            self.syncActionList()

    def checkLocalizationLanguage(self):
        data = getFromCache(EMPTY_IDTYPELIST, 'ILocalizationLanguage')
        if data is None or data['lang'] != localizeLobby('LOCALIZATION_LANGUAGE'):
            from Helpers.cache import deleteCache
            self.base.setClientLocalization(localizeLobby('LOCALIZATION_LANGUAGE').encode('ascii'))
            deleteCache()
        return

    def updateAccountResources(self, credits, gold, exp, tickets, questChips):
        """
        Update money panel
        @param exp:
        @param gold:
        @param credits:
        @param tickets:
        """
        if self._lobbyInstance != None:
            self._lobbyInstance.call_1('hangar.updateMoneyPanel', credits, gold, exp, tickets, questChips)
        return

    def updateCarouselResponse(self, carouselMap):
        if self._lobbyInstance != None:
            self._lobbyInstance.updateCarouselResponse(carouselMap)
        return

    def getShopAirplanesResponse(self, resultID, airplanesListArgs):
        airplanesList = wgPickle.loads(wgPickle.FromServerToClient, airplanesListArgs)
        if self._lobbyInstance != None:
            self._lobbyInstance.lobbyShopHelper.getShopAirplanesResponse(resultID, airplanesList)
        return

    def refreshRoomListResponse(self, roomList):
        LOG_DEBUG('Account(client)::refreshRoomListResponse', roomList)
        if self._lobbyInstance != None:
            self._lobbyInstance.trainingRoomHelper.refreshRoomListResponse(roomList)
        return

    def updateTrainingRoom(self, dataType, sequenceID, sessionID, trainingRoomDataPickled):
        LOG_DEBUG('Account(client)::updateTrainingRoom add to pool', sessionID, sequenceID, dataType)
        if dataType == PREBATLE_DATA.SET_SESSION:
            self.resetTrainingRoomData()
            self.__updateTrainingSession = sessionID
            return
        self.__updateTrainingRoomData[sequenceID] = (sessionID, dataType, trainingRoomDataPickled)
        self.__checkUpdateTrainingRoom()

    def __checkUpdateTrainingRoom(self):
        while self.__updateTrainingRoomData.has_key(self.__updateTrainingSequence):
            sessionID, dataType, trainingRoomDataPickled = self.__updateTrainingRoomData.pop(self.__updateTrainingSequence)
            if sessionID != self.__updateTrainingSession:
                LOG_DEBUG('Account(client)::updateTrainingRoom:Wrong session', sessionID, self.__updateTrainingSession, dataType)
                break
            LOG_DEBUG('Account(client)::updateTrainingRoom process:', dataType, self.__updateTrainingSequence)
            if self._lobbyInstance != None:
                trainingRoomData = accountDataList = wgPickle.loads(wgPickle.FromServerToClient, trainingRoomDataPickled)
                LOG_DEBUG('Account(client)::updateTrainingRoom data=', trainingRoomData)
                if dataType == PREBATLE_DATA.ROOM_INFO:
                    self._lobbyInstance.trainingRoomHelper.updateTrainingRoom(trainingRoomData)
                elif dataType == PREBATLE_DATA.TEAM_LIST:
                    for accountData in trainingRoomData:
                        self._lobbyInstance.trainingRoomHelper.updateRoomTeamAccount(accountData)

                elif dataType == PREBATLE_DATA.REMOVE_MEMBER:
                    self._lobbyInstance.trainingRoomHelper.removeRoomTeamAccount(trainingRoomData)
                else:
                    LOG_ERROR('updateTrainingRoom: unknown dataType', dataType, sequence, trainingRoomData)
            self.__updateTrainingSequence += 1

        return

    def resetTrainingRoomData(self):
        LOG_DEBUG('Account(client)::resetTrainingRoomData')
        self.__updateTrainingRoomData = {}
        self.__updateTrainingSequence = 0
        self.__updateTrainingSession = 0

    def updatePrebattleCreateRoomAvailableFilters(self):
        if self._lobbyInstance:
            self._lobbyInstance.updatePrebattleCreateRoomAvailableFilters()

    def onJoinedToPrebattle(self):
        self.startWaitingForArena()

    def forceLeaveRoom(self):
        LOG_DEBUG('Account(client)::forceLeaveRoom')
        if self._lobbyInstance != None:
            self._lobbyInstance.trainingRoomHelper.forceLeaveRoom()
        return

    def leaveRoomWithReason(self, reasonID):
        LOG_DEBUG('Account(client)::leaveRoomWithReason: errorId = {0}'.format(reasonID))
        if self._lobbyInstance != None:
            self._lobbyInstance.trainingRoomHelper.leaveRoomWithReason(reasonID)
        return

    def showTrainingRoom(self):
        LOG_DEBUG('Account(client)::showTrainingRoom')
        if self._lobbyInstance != None:
            self._lobbyInstance.showTrainingRoom()
        return

    def updateCarouselAirplane(self, aircraftID):
        LOG_DEBUG('Account(client)::updateCarouselSlotResponse decals', aircraftID)
        if not self.isWaitingBattle():
            BWPersonality.g_lobbyCarouselHelper.updateCarouselAirplane(aircraftID)

    def __onHangarLoaded(self):
        LOG_TRACE('Account::onHangarLoaded')
        self.base.onHangarLoaded()
        self.__checkClanInfo()
        BWPersonality.g_lobbyCrewBodyType = DEFAULT_BOT_AVATAR_BODY_TYPE
        BWPersonality.g_lobbyCrewLastNationID = None
        BWPersonality.g_lobbyCarouselHelper.checkLobbyCrewAnimation()
        if consts.QA_START_GUI_AUTOTESTS:
            from debug.layer0.qa.GUI.framework.RemoteAPI.ClientSideRouter import client_router
            client_router()
            print 'Client router for UI tests started...'
        if config_consts.IS_DEVELOPMENT != BWPersonality.g_initPlayerInfo.isDevelopment:
            LOG_ERROR('IS_DEVELOPMENT mismatch: server is development = %s, client is development = %s' % (BWPersonality.g_initPlayerInfo.isDevelopment, config_consts.IS_DEVELOPMENT))
            BigWorld.quit()
            return
        else:
            return

    def __linkEvents(self):
        GlobalEvents.onMovieLoaded += self.__onMovieLoaded
        GlobalEvents.onHideModalScreen += self.__onHideModalScreen
        self.__operationReceiver.onReceiveOperation += self.__onReceiveOperation
        GlobalEvents.onHangarLoaded += self.__onHangarLoaded

    def __unlinkEvents(self):
        GlobalEvents.onMovieLoaded -= self.__onMovieLoaded
        GlobalEvents.onHideModalScreen -= self.__onHideModalScreen
        self.__operationReceiver.onReceiveOperation -= self.__onReceiveOperation
        GlobalEvents.onHangarLoaded -= self.__onHangarLoaded

    def onBecomePlayer(self):
        """
        This analog of __init__ here
        """
        LOG_INFO('onBecomePlayer')
        self.__clientFailureVerify()
        self.onWaitQeueueDequeued(False)
        from SyncOperationKeeper import SyncOperationKeeper
        SyncOperationKeeper.clearAllFlags()
        self.operationCmdHandlers = {OPERATION_CODE.CMD_SET_IFACE_DATA: self.__handleSetIfaceData,
         OPERATION_CODE.CMD_SEND_LAST_SESSION: self.__handleLastSessionKey,
         OPERATION_CODE.CMD_ACTION_LIST_CHANGED: self.__handleActionListChanged}
        self.__operationReceiver = OperationReceiver(self.base, wgPickle.FromServerToClient, wgPickle.FromClientToServer)
        self.__linkEvents()
        self._premWaiting = False
        self._premWaitingExpiryTime = 0
        self.premiumExpiryTime = 0
        self.deltaTimeClientServer = 0
        if db.DBLogic.g_instance == None:
            return
        else:
            if BWPersonality.g_connectedAccountID == None or BWPersonality.g_connectedAccountID != self.id:
                self.__onConnected()
                BWPersonality.g_waitingInfoHelper.stopWaiting(WAITING_INFO_TYPE.LOGIN)
                BWPersonality.g_connectedAccountID = self.id
                BWPersonality.g_lobbyInterview = [None, None]
                BWPersonality.g_lastMapID = -1
            self.__isSyncingActions = False
            self.__resyncActions = False
            self.__isLobbyLoading = False
            self.__waitingForArenaCallback = None
            self.__waitingForArenaID = None
            self.playersCount = 0
            self.queueCount = 0
            self.__queueStatisticPacked = None
            self.__premiumCallback = None
            em = EventManager()
            self.__em = em
            self.onUpdatePremiumTime = Event(em)
            self.onInitPremium = Event(em)
            self.ifaceHandler = None
            self.requestsAvailable = False
            self.onAddArena = Event(em)
            self.__requestID = 0
            BigWorld.resetEntityManager(True, False)
            BigWorld.clearAllSpaces(True)
            self.__currentSequence = 1
            self.__responseQueue = {}
            self.resetTrainingRoomData()
            self.accountCmd = None
            if consts.IS_DEBUG_IMPORTED:
                if consts.QA_ACCOUNT_ENABLED and consts.QA_TESTING_ENABLED:
                    from debug.layer0.qa.AccountAPI import AccountAPI
                    self.accountCmd = AccountAPI(self, self.base)
            if self.accountCmd is None:
                self.accountCmd = AccountOperationsMgr(self.base)
            if consts.QA_CLIENT_ACCOUNT_TESTING:
                from debug.layer0.qa.Functional_testing.ClientAccountTestController import ClientAccountTestController
                ClientAccountTestController(consts.QA_CLIENT_ACCOUNT_TESTING)
            self.interfaceSender = InterfaceSenderQueue(self.accountCmd)
            if BWPersonality.g_lobbyCarouselHelper.inventory:
                BWPersonality.g_lobbyCarouselHelper.inventory.setOpSender(self.accountCmd)
            if messenger.g_xmppChatHandler:
                messenger.g_xmppChatHandler.onEnterLobbyEvent()
            from gui.Scaleform.WebBrowser import WebBrowser
            WebBrowser.ReportBecomePlayer()
            BWPersonality.g_waitingInfoHelper.init(self)
            BWPersonality.g_waitingInfoHelper.stopWaiting(WAITING_INFO_TYPE.ACCOUNT_INIT)
            return

    def __onConnected(self):
        global DATA_STORAGE
        LOG_DEBUG('Account::connected ')
        from Helpers import cache
        if cache.INITIALIZED:
            cache.destroy()
        BWPersonality.g_lobbyCarouselHelper = LobbyCarouselHelper()
        from exchangeapi.UICallbackUtils import clearUICallbacks
        clearUICallbacks()
        DATA_STORAGE = {'ifaces': {}}
        self.__wasLogin = True

    def checkAccessibility(self, hangarSpace, accType, activeEvents):

        def __validateStartTime(hangarSpace):
            if 'startTime' not in hangarSpace:
                return True
            return hangarSpace['startTime'] <= time.time() - self.deltaTimeClientServer

        def __validateEndTime(hangarSpace):
            if 'endTime' not in hangarSpace:
                return True
            return hangarSpace['endTime'] >= time.time() - self.deltaTimeClientServer

        if hangarSpace and accType in hangarSpace['accountTypes'] and __validateStartTime(hangarSpace) and __validateEndTime(hangarSpace):
            if not hangarSpace['events'] and (not activeEvents or not hangarSpace['exceptEvents']):
                return True
            if activeEvents:
                return all((event in activeEvents for event in hangarSpace['events'])) and not any((event in activeEvents for event in hangarSpace['exceptEvents']))
        return False

    def updateHangarSpace(self, override = None):
        from BWPersonality import g_lobbyCarouselHelper
        currSpaceID = BWPersonality.g_settings.hangarSpaceSettings['spaceID']
        if g_lobbyCarouselHelper is not None:
            if override:
                space = getHangarSpaceByID(override)
                spaceData = (space['hangarType'], space['spaceID'])
            else:
                spaceData = self.__getHungarSpaceData(False)
            if spaceData[1] == currSpaceID:
                return
            g_hangarSpace.refreshSpace(*spaceData)
            vehicleInfo = g_lobbyCarouselHelper.getCarouselAirplaneSelected()
            g_lobbyCarouselHelper.queryRefresh3DModel(vehicleInfo, False, True)
        return

    def findSuitableHangarSpace(self, spaces):
        currentAccountType = GUI_TYPES_DICT[BWPersonality.g_initPlayerInfo.useGUIType]
        activeEvents = [ e.upper() for e in BWPersonality.g_initPlayerInfo.activeEvents ]
        for hangarSpace in sorted(spaces, key=operator.itemgetter('index')):
            if self.checkAccessibility(hangarSpace, currentAccountType, activeEvents):
                return hangarSpace

        return None

    def _getWarActionHangar(self, currSpaceID):
        import BWPersonality
        uiConfig = _warAction.WarAction.uiConfig
        warState = BWPersonality.gameParams.get('warAction', {}).get('state', None)
        hangar = None
        if warState == consts.WAR_STATE.WAR:
            hangar = uiConfig.hangarWar
        elif warState not in [consts.WAR_STATE.END, consts.WAR_STATE.OFF, consts.WAR_STATE.UNDEFINED]:
            hangar = uiConfig.hangarPeace
        else:
            return
        curHangarSpace = getHangarSpaceByID(hangar)
        return (curHangarSpace['hangarType'], curHangarSpace['spaceID'])

    def __getHungarSpaceData(self, showWindow = False, switchOnPremBought = False):
        currSpaceID = BWPersonality.g_settings.hangarSpaceSettings['spaceID']
        curHangarSpace = getHangarSpaceByID(currSpaceID)
        currentAccountType = GUI_TYPES_DICT[BWPersonality.g_initPlayerInfo.useGUIType]
        warActionHangar = self._getWarActionHangar(currSpaceID)
        if warActionHangar:
            warHangar = warActionHangar
            BWPersonality.g_settings.hangarSpaceSettings['spaceID'] = warActionHangar[1]
            return warHangar
        else:
            from zlib import crc32
            from db.DBLogic import g_instance as dbInstance

            def __getDuration(hangarSpace):
                if 'endTime' not in hangarSpace:
                    return 0
                return hangarSpace['endTime'] - (time.time() - self.deltaTimeClientServer)

            def __setDynamicHangarUpdateCallback(hangarSpace):

                def __reinitHangarSpace():
                    self.onInitPremium(True, self.__getHungarSpaceData())

                duration = __getDuration(hangarSpace)
                if duration > 0:
                    if self.__dynamicHangarUpdateCallback is not None:
                        BigWorld.cancelCallback(self.__dynamicHangarUpdateCallback)
                    self.__dynamicHangarUpdateCallback = BigWorld.callback(duration + 1, partial(__reinitHangarSpace))
                return

            currentAccountType = GUI_TYPES_DICT[BWPersonality.g_initPlayerInfo.useGUIType]
            activeEvents = [ e.upper() for e in BWPersonality.g_initPlayerInfo.activeEvents ]

            def applySpace(space):
                BWPersonality.g_settings.hangarSpaceSettings['spaceID'] = space['spaceID']
                g_windowsManager.getAccountUI().editIFace([[{'ICurrentHangarSpace': {'spaceID': space['spaceID']}}, EMPTY_IDTYPELIST]])
                __setDynamicHangarUpdateCallback(space)

            if curHangarSpace is None:
                LOG_DEBUG('__getHungarSpaceData {0} {1}'.format(BWPersonality.g_settings.hangarSpaceSettings['spaceID'], curHangarSpace))
            if curHangarSpace and curHangarSpace.get('isModal', False) and self.checkAccessibility(curHangarSpace, currentAccountType, activeEvents):
                __setDynamicHangarUpdateCallback(curHangarSpace)
                return (curHangarSpace['hangarType'], curHangarSpace['spaceID'])
            activeEventsCRC32 = BWPersonality.g_settings.hangarSpaceSettings['eventsHash']
            curEventsCRC32 = str(crc32(''.join(activeEvents))) if activeEvents else ''
            oldSpaces = (getFromCache(EMPTY_IDTYPELIST, 'IHangarSpaces') or {}).get('spaces', [])
            if curEventsCRC32 != activeEventsCRC32:
                BWPersonality.g_settings.hangarSpaceSettings['eventsHash'] = curEventsCRC32
                g_windowsManager.getAccountUI().editIFace([[{'IHangarSpacesHash': {'hash': curEventsCRC32}}, EMPTY_IDTYPELIST]])
                g_windowsManager.getAccountUI().editIFace([[{'IHangarSpaces': {'showWindow': False}}, EMPTY_IDTYPELIST]])
            modalSpaces = (hangarSpace for spaceID, hangarSpace in dbInstance.userHangarSpaces.iteritems() if hangarSpace.get('isModal', False))
            hangarSpace = self.findSuitableHangarSpace(modalSpaces)
            if hangarSpace:
                applySpace(hangarSpace)
                return (hangarSpace['hangarType'], hangarSpace['spaceID'])

            def _showSwitchMessage():
                if switchOnPremBought:
                    msgText = 'SYSTEM_MESSAGE_HANGAR_HOLIDAY_1'
                else:
                    msgText = 'SYSTEM_MESSAGE_HANGAR_HOLIDAY'
                msgid, messageMap = createIMessage(MESSAGE_TYPE.TOOLTIP_HOLIDAY_HANGAR, localizeMessages(msgText))
                self.responseSender([[msgid, 'message']], 'IMessage', messageMap)

            switchSpaces = (hangarSpace for spaceID, hangarSpace in dbInstance.userHangarSpaces.iteritems() if hangarSpace.get('switchOnActivation', False))
            hangarSpace = self.findSuitableHangarSpace(switchSpaces)
            if hangarSpace:
                if not BWPersonality.g_settings.hangarSpaceSettings['ignoreEventHangar']:
                    if not BWPersonality.g_settings.hangarSpaceSettings['spaceID'] or hangarSpace['spaceID'] not in oldSpaces:
                        applySpace(hangarSpace)
                        g_windowsManager.getAccountUI().editIFace([[{'IHangarSpaces': {'showWindow': False}}, EMPTY_IDTYPELIST]])
                        _showSwitchMessage()
                        return (hangarSpace['hangarType'], hangarSpace['spaceID'])
                    if switchOnPremBought:
                        _showSwitchMessage()
            else:
                BWPersonality.g_settings.hangarSpaceSettings['ignoreEventHangar'] = False
            currentSpaceIsValid = self.checkAccessibility(curHangarSpace, currentAccountType, activeEvents)
            if activeEvents and (curEventsCRC32 != activeEventsCRC32 or not currentSpaceIsValid):
                regularSpaces = (hangarSpace for spaceID, hangarSpace in dbInstance.userHangarSpaces.iteritems() if not hangarSpace.get('switchOnActivation', False))
                hangarSpace = self.findSuitableHangarSpace(regularSpaces)
                if hangarSpace and (not curHangarSpace or hangarSpace['spaceID'] != curHangarSpace['spaceID']) and (hangarSpace['spaceID'] not in oldSpaces or not currentSpaceIsValid):
                    applySpace(hangarSpace)
                    showWindow = curHangarSpace is not None and curHangarSpace.get('chooseHangarAfter', False)
                    if showWindow or not BWPersonality.g_settings.hangarSpaceSettings['spaceID'] or hangarSpace['spaceID'] not in oldSpaces:
                        g_windowsManager.getAccountUI().editIFace([[{'IHangarSpaces': {'showWindow': True}}, EMPTY_IDTYPELIST]])
                    return (hangarSpace['hangarType'], hangarSpace['spaceID'])
            if not currentSpaceIsValid:
                spaceID = getDefaultSpaceID(currentAccountType)
                hangarSpace = getHangarSpaceByID(spaceID)
                if curHangarSpace and curHangarSpace.get('isModal', False) and curHangarSpace.get('chooseHangarAfter', False):
                    showWindow = True
                elif not hangarSpace.get('isModal', False):
                    showWindow = showWindow or curEventsCRC32 != activeEventsCRC32 and BWPersonality.g_initPlayerInfo.useGUIType == GUI_TYPES.PREMIUM
                else:
                    showWindow = False
                applySpace(hangarSpace)
                g_windowsManager.getAccountUI().editIFace([[{'IHangarSpaces': {'showWindow': showWindow}}, EMPTY_IDTYPELIST]])
                return (hangarSpace['hangarType'], spaceID)
            g_windowsManager.getAccountUI().editIFace([[{'IHangarSpaces': {'showWindow': False}}, EMPTY_IDTYPELIST]])
            __setDynamicHangarUpdateCallback(curHangarSpace)
            return (curHangarSpace['hangarType'], curHangarSpace['spaceID'])

    def __clearSpaceUnloadCallback(self):
        if self.__spaceUnloadCallback is not None:
            BigWorld.cancelCallback(self.__spaceUnloadCallback)
            self.__spaceUnloadCallback = None
        return

    def __waitSpaceUnloading(self):
        LOG_INFO('Waiting for previous space to unload...')
        if BigWorld.spacePresent() and not BigWorld.isClientSpace():
            self.__spaceUnloadCallback = BigWorld.callback(0.1, self.__waitSpaceUnloading)
        else:
            LOG_INFO('Creating hangar space...')
            self.__clearSpaceUnloadCallback()
            g_hangarSpace.init(*self.__getHungarSpaceData())

    def __turnOnHangarSpace(self):
        LOG_INFO('Turn on hangar space')
        self.__clearSpaceUnloadCallback()
        if BigWorld.spacePresent() and not BigWorld.isClientSpace():
            self.__spaceUnloadCallback = BigWorld.callback(0.1, self.__waitSpaceUnloading)
        else:
            g_hangarSpace.init(*self.__getHungarSpaceData())

    def __turnOffHangarSpace(self):
        self.__clearSpaceUnloadCallback()
        g_hangarSpace.destroy()
        LOG_INFO('Hangar destroyed')

    def onBecomeNonPlayer(self):
        LOG_INFO('PlayerAccount::onBecomeNonPlayer')
        BWPersonality.g_waitingInfoHelper.deinit()
        self.__unlinkEvents()
        self.__operationReceiver.destroy()
        self.__operationReceiver = None
        disposePackageChain()
        clearMappedCallbacks()
        self.__stopPackageChain()
        connectionManager.onDisconnected -= self.__stopPackageChain
        if self.__dynamicHangarUpdateCallback is not None:
            BigWorld.cancelCallback(self.__dynamicHangarUpdateCallback)
            self.__dynamicHangarUpdateCallback = None
        if self.__queueVSECallback is not None:
            BigWorld.cancelCallback(self.__queueVSECallback)
            self.__queueVSECallback = None
        if BWPersonality.g_lobbyCarouselHelper:
            BWPersonality.g_lobbyCarouselHelper.clearQueue()
        self.__clearStartingArenaCallback()
        self.__turnOffHangarSpace()
        self.__clearPremiumCallback()
        self.premiumExpiryTime = 0
        self.__em.clear()
        PartSender().clearCallbacks()
        PartSender().clearAllPools()
        from eventhandlers.onRentEvent import clearRentCallbacks
        clearRentCallbacks()
        from gui.WindowsManager import g_windowsManager
        self.interfaceSender.destroy()
        self.accountCmd.destroy()
        self.requestsAvailable = False
        g_windowsManager.hideAll()
        Waiting.hideAll()
        BigWorld.worldDrawEnabled(False)
        BWPersonality.g_settings.hangarSpaceSettings = None
        return

    def isGUIBlocked(self, event):
        return False

    def handleKeyEvent(self, event):
        if event.key == Keys.KEY_C:
            return True
        if event.key == Keys.KEY_L:
            return True
        return False

    def isWaitingBattle(self):
        return self.__waitingForArenaCallback != None

    def startWaitingForArena(self):
        if self.__waitingForArenaCallback == None:
            self.__waitingForArenaID = Waiting.show('Lobby_start_arena')
            g_hangarSpace.setFreeze(True)
            self.__waitingForArenaCallback = BigWorld.callback(WAIT_ARENA_CREATON_TIME, self.stopWaitingForArena)
        return

    def stopWaitingForArena(self):
        g_hangarSpace.setFreeze(False)
        self.__clearStartingArenaCallback()
        if self.__waitingForArenaID is not None:
            Waiting.hide(self.__waitingForArenaID)
        return

    def __clearStartingArenaCallback(self):
        if self.__waitingForArenaCallback:
            BigWorld.cancelCallback(self.__waitingForArenaCallback)
            self.__waitingForArenaCallback = None
        return

    def startTutorial(self, lessonIndex):
        LOG_DEBUG('Account::startTutorial', lessonIndex)
        BWPersonality.g_tutorialIndex = lessonIndex
        self.base.startTutorial(lessonIndex)
        ClientLog.g_instance.general('Start tutorial')

    def enterSpace(self, arenaIndex, joinAsSpectator):
        LOG_INFO('PlayerAccount: Enter space', arenaIndex)
        self.__clearStartingArenaCallback()
        self.__turnOffHangarSpace()
        self.base.connect2Arena(arenaIndex, joinAsSpectator)

    def updateArenaData(self, arenaData):
        self.onAddArena(arenaData)

    def onPremUserAction(self):
        if not self._premWaiting:
            return
        self._premWaiting = False
        self.premBought(self._premWaitingExpiryTime, False)

    def premBought(self, expiryTime, waitForUserAction):
        if waitForUserAction:
            self._premWaiting = True
            self._premWaitingExpiryTime = expiryTime
            return
        self.premiumExpiryTime = expiryTime + self.deltaTimeClientServer
        if self.premiumExpiryTime > 0:
            self.__updatePremiumTime()
            BWPersonality.g_initPlayerInfo.useGUIType = GUI_TYPES.PREMIUM
            self.onInitPremium(True, self.__getHungarSpaceData(showWindow=True, switchOnPremBought=True))
        else:
            self.premiumExpiryTime = 0
        return self.premiumExpiryTime

    def premExtended(self, expiryTime, deltaTime):
        if self._premWaiting:
            self._premWaitingExpiryTime = expiryTime
            return
        premiumExpiryTime = expiryTime + self.deltaTimeClientServer
        if deltaTime > 0:
            self.premiumExpiryTime = max(premiumExpiryTime, self.premiumExpiryTime)
        else:
            self.premiumExpiryTime = min(premiumExpiryTime, self.premiumExpiryTime)
        self.__updatePremiumTime()
        return self.premiumExpiryTime

    def premExpired(self):
        self.__clearPremiumCallback()
        self.premiumExpiryTime = 0
        BWPersonality.g_initPlayerInfo.useGUIType = GUI_TYPES.NORMAL
        self.onInitPremium(False, self.__getHungarSpaceData())

    def __onMovieLoaded(self, movieID, movieInstance):
        if movieID == 'ui':
            from gui.WindowsManager import g_windowsManager
            g_windowsManager.closeBattleUI()
        elif movieID == 'prebattle':
            if self.__prebattleInstance != None and self.__queueStatisticPacked != None:
                self.__prebattleInstance.setPrebattleStatistic(self.__queueStatisticPacked)
            if BWPersonality.g_initPlayerInfo.isDeveloper == True and config_consts.IS_DEVELOPMENT:
                self.__prebattleInstance.hideForceStartButton(False)
            else:
                self.__prebattleInstance.hideForceStartButton(True)
        elif movieID == 'lobby':
            self.__updatePremiumTime()
            self.__isLobbyLoading = False
            self.__turnOnHangarSpace()
        return

    def __onHideModalScreen(self, movieID = ''):
        if movieID == 'Options':
            from gui.WindowsManager import g_windowsManager
            g_windowsManager.showLobby()

    def receivePlayersCount(self, playersCount, queueCount):
        self.playersCount = playersCount
        self.queueCount = queueCount

    def setPrebattleStatistic(self, battleType, queueStatisticPacked):
        self.__queueStatisticPacked = queueStatisticPacked if self.battleType == battleType else None
        if self.__prebattleInstance and self.__queueStatisticPacked:
            self.__prebattleInstance.setPrebattleStatistic(queueStatisticPacked)
        return

    def receiveBuyPlane(self, resultID, airplaneID):
        if self._lobbyInstance != None:
            self._lobbyInstance.lobbyShopHelper.onBuyPlaneResponse(resultID, airplaneID)
            self._lobbyInstance.onBuyPlaneResponse(airplaneID)
        return

    def receiveSellPlane(self, resultID, planeID):
        if self._lobbyInstance != None:
            self._lobbyInstance.lobbyShopHelper.onSellPlaneResponse(resultID, planeID)
        return

    def receiveRepairPlane(self, resultID, aircraftID):
        BWPersonality.g_lobbyCarouselHelper.onRepairPlaneResponse(resultID, aircraftID)

    def voipReceiveSquadChannel(self, channel, clients_list):
        LOG_TRACE('voipReceiveSquadChannel:', channel, clients_list)
        if channel != '':
            VOIP.api().onEnterSquadChannel(channel, clients_list)
        else:
            VOIP.api().onLeaveSquadChannel()

    def onLeftQueue(self):
        from gui.WindowsManager import g_windowsManager
        ClientLog.g_instance.general('Left queue')
        g_windowsManager.showLobby()

    def onEnterToQueue(self, arenaType):
        self.battleType = arenaType
        self._queueStatisticPacked = None
        self.__turnOffHangarSpace()
        from gui.WindowsManager import g_windowsManager
        Waiting.hideAll()
        gameParams = getFromCache(EMPTY_IDTYPELIST, 'IGameModesParams')
        if gameParams:
            gameParams['curMode'] = arenaType
            setToCache(EMPTY_IDTYPELIST, 'IGameModesParams', gameParams)
        g_windowsManager.showPrebattle()
        return

    def onEnterArena(self, planeID, arenaType):
        self.battleType = arenaType
        PLANE_BLOCK_TYPE[planeID] = (PLANE_BLOCK_TYPE.get(planeID, consts.BLOCK_TYPE.UNLOCKED) | consts.BLOCK_TYPE.LOADING_BATTLE) ^ consts.BLOCK_TYPE.LOADING_BATTLE | consts.BLOCK_TYPE.IN_BATTLE
        LOG_TRACE('Account {0} join to arena type {1} on plane {2}:'.format(BWPersonality.g_initPlayerInfo.databaseID, arenaType, planeID))
        ClientLog.g_instance.general('Account {0} join to arena type {1} on plane {2}:'.format(BWPersonality.g_initPlayerInfo.databaseID, arenaType, planeID))

    def onWaitQeueueEnqueued(self, queueType, number, queueLen, avgWaitingTime):
        LOG_DEBUG('onWaitQeueueEnqueued', queueType, number, queueLen, avgWaitingTime)
        if self.isInTutorialQueue:
            if self._lobbyInstance != None:
                self._lobbyInstance.call_1('hangar.tutorialQueueUpdate', queueType, number, queueLen, max(1, avgWaitingTime / 60000.0) if avgWaitingTime > 0 else 0)
        else:
            Waiting.hideAll()
            if avgWaitingTime < TUTORIAL_QUEUE_SHOW_WAITING_AVG_TIME:
                if self._lobbyInstance != None:
                    self._lobbyInstance.showTutorialWaiting(True)
            else:
                self.isInTutorialQueue = True
                if self._lobbyInstance != None:
                    self._lobbyInstance.call_1('hangar.tutorialEnqueued', queueType)
                    self._lobbyInstance.call_1('hangar.tutorialQueueUpdate', queueType, number, queueLen, max(1, avgWaitingTime / 60000.0) if avgWaitingTime > 0 else 0)
        return

    def onTutorialEnqueueFailure(self, errorCode, errorStr):
        LOG_DEBUG('onTutorialEnqueueFailure', errorCode, errorStr)
        self.isInTutorialQueue = False
        if self._lobbyInstance != None:
            self._lobbyInstance.showTutorialWaiting(False)
            self._lobbyInstance.call_1('hangar.tutorialDequeueCompleted')
        return

    def onWaitQeueueDequeued(self, isKicked):
        LOG_DEBUG('onWaitQeueueDequeued', isKicked)
        self.isInTutorialQueue = False
        if self._lobbyInstance != None:
            self._lobbyInstance.showTutorialWaiting(False)
            self._lobbyInstance.call_1('hangar.tutorialDequeueCompleted')
        return

    def hideForceStartButton(self, needToHideButton):
        LOG_DEBUG('Account(client)::hideForceStartButton', needToHideButton)
        if self.__prebattleInstance != None:
            self.__prebattleInstance.hideForceStartButton(needToHideButton)
        return

    def messenger_onActionByServer(self, actionID, reqID, args):
        GameServerMessenger.g_instance.onActionByServer(messenger.XmppChat.MessengerActionProcessor(), actionID, reqID, args)

    def onTokenReceived(self, requestID, tokenType, data):
        dataMap = cPickle.loads(data)
        if dataMap.has_key('error'):
            LOG_ERROR('onTokenReceived', str(dataMap))
            self.tokenManager.receiveChatToken(-1, -1, requestID)
        else:
            self.tokenManager.receiveChatToken(dataMap['databaseID'], dataMap['token'], requestID)

    def receiveChatTokenForLobby(self, spaID, token):
        if self._lobbyInstance is not None and self._lobbyInstance.isOpenShopLink():
            self._lobbyInstance.receiveChatToken(spaID, token)
        return

    def updatePlayerResources(self, credits, exp, gold, tickets, questChips):
        if self._lobbyInstance != None:
            LOG_NOTE('hangar.updateMoneyPanel', credits, gold, exp, tickets, questChips)
            self._lobbyInstance.call_1('hangar.updateMoneyPanel', credits, gold, exp, tickets, questChips)
        return

    def clientReceiveResponse(self, responseType, sequenceId, invocationId, operationCode, argStr):
        """
        receive operation
        @param responseType
        @param sequenceId:
        @param operationCode:
        @param invocationId:
        @param argStr:
        """
        self.__responseQueue[sequenceId] = (responseType,
         invocationId,
         operationCode,
         argStr)
        self.__checkClientReceiveResponse()

    def __checkClientReceiveResponse(self):
        while self.__responseQueue.has_key(self.__currentSequence) or self.__responseQueue.has_key(0):
            if self.__responseQueue.has_key(0):
                responseType, invocationId, operationCode, argStr = self.__responseQueue[0]
                del self.__responseQueue[0]
            else:
                responseType, invocationId, operationCode, argStr = self.__responseQueue[self.__currentSequence]
                del self.__responseQueue[self.__currentSequence]
                self.__currentSequence += 1
            if responseType == RESPONSE_TYPE.RESPONSE_TYPE_CMD:
                if self.accountCmd.getOperationByInvocationId(invocationId) is None:
                    try:
                        args = self.accountCmd.unpackAgrumentString(argStr)
                    except Exception:
                        return

                    self.__handleSetIfaceData(None, args)
                else:
                    self.accountCmd.receiveOperationResponse(invocationId, operationCode, argStr)
            elif responseType == RESPONSE_TYPE.RESPONSE_TYPE_OPERATION:
                self.__operationReceiver.receiveOperation(invocationId, operationCode, argStr)

        return

    def receiveOperationTimeout(self, invocationId):
        """
        REceive operation timeout
        @param invocationId:
        """
        self.__operationReceiver.receiveOperationTimeout(invocationId)

    def onKickedFromServer(self, reason, isBan, expiryTime):
        LOG_MX('onKickedFromServer', reason, isBan, expiryTime)
        BigWorld.callback(2.13, partial(self.__kickSelf, reason, isBan, expiryTime))

    def __kickSelf(self, reason, isBan, expiryTime):
        LOG_MX('__kickSelf', reason, isBan, expiryTime)
        from gui.Scaleform.Disconnect import Disconnect
        Disconnect.show(reason, isBan, expiryTime)

    def receviveBanInfo(self, restrictionType, isBan, reason, expireTime):
        LOG_INFO('receviveBanInfo: ', restrictionType, isBan, expireTime, reason)

    def __clearPremiumCallback(self):
        if self.__premiumCallback is not None:
            BigWorld.cancelCallback(self.__premiumCallback)
            self.__premiumCallback = None
        return

    def __updatePremiumTime(self):
        self.__clearPremiumCallback()
        if self.premiumExpiryTime > 0:
            diffTime = int(self.premiumExpiryTime) - int(time.time())
            if diffTime > 0:
                self.onUpdatePremiumTime(int(diffTime))
                self.__premiumCallback = BigWorld.callback(5.0, self.__updatePremiumTime)
            else:
                self.premiumExpiryTime = 0
                lch = BWPersonality.g_lobbyCarouselHelper
                lch.queryRefresh3DModel(lch.getCarouselAirplaneSelected(), False, True)

    def receiveServerConsts(self, constsDataStr):
        constsData = wgPickle.loads(wgPickle.FromServerToClient, constsDataStr)
        LOG_INFO('Resived server consts: ')
        for constData in constsData:
            LOG_INFO('const', constData)
            setattr(globals()[constData[0]], constData[1], constData[2])

        if config_consts.SEND_CONSTS_TO_CLIENT:
            db.DBLogic.initDB()
            self.onBecomePlayer()

    def getAccountPortalStatsLink(self, accountName):
        if BWPersonality.g_initPlayerInfo.databaseID is None:
            LOG_DEBUG('PlayerAccount::getAccountPortalStatsLink - databaseID = None accountName=%s' % accountName)
            return
        else:
            return '-'.join([str(BWPersonality.g_initPlayerInfo.databaseID), accountName])

    def __initGlobalGamesPlayed(self):

        def _onResponse(responseob):
            if isinstance(responseob, basestring):
                LOG_ERROR('_onResponse error: {0}'.format(responseob))
                return
            BWPersonality.g_gamesPlayed = responseob[0][0]['ISummaryStats'].get('gamesPlayed', 0)

        accountUI = g_windowsManager.getAccountUI()
        if accountUI:
            accountUI.viewIFace([[{'ISummaryStats': {}}, [[BWPersonality.g_initPlayerInfo.databaseID, 'account']]]], dbgCallback=_onResponse)
        else:
            LOG_ERROR('accountUI is not initialized yet')

    def sendCrashReport(self, timeDelta, crashType, crashCode, crashDescr, crashDump):
        """
        sendCrashReport - Send Crash Report to Server
        @param timeDelta: Delta Time  (s, now() - 'crash date')
        @param crashType: Crash Type 0 - system assert, 1 - game assertion
        @param crashCode: Crash code or subtype
        @param crashDesc: crash description
        @param crashDump: zlib compressed dump or callstack
        """
        header = wgPickle.dumps(wgPickle.FromClientToServer, (timeDelta,
         crashType,
         crashCode,
         crashDescr,
         len(crashDump)))
        LOG_TRACE('send crash Report to server')
        self.base.crashReport(0, header)
        if config_consts.SEND_DUMPS_TO_SERVER and len(crashDump) > 0:
            LOG_TRACE('sending crash dump to server %d bytes' % len(crashDump))
            self._crashDump = buffer(crashDump)
            self._crashSendIndex = 0
            self.__sendCrashDump()

    def __sendCrashDump(self):
        """
            __sendCrashDump - callbacke-d loop, send CrashDump to server
        """
        sendSize = MAX_SEND_DATA_SIZE
        toSendLeft = len(self._crashDump) - self._crashSendIndex * sendSize
        sendBuffer = buffer(self._crashDump, self._crashSendIndex * sendSize, min(toSendLeft, sendSize))
        self._crashSendIndex += 1
        self.base.crashReport(self._crashSendIndex, str(sendBuffer))
        if toSendLeft > sendSize:
            BigWorld.callback(0.1, self.__sendCrashDump)
        else:
            LOG_TRACE('Crash dump to server has been sent')
            self._crashDump = None
        return

    def __clientFailureVerify(self):
        import datetime, re, os
        fname = os.path.join(BigWorld.getUserDataDirectory(), 'logs/', 'crash.tmp')
        try:
            if os.path.isfile(fname):
                with open(fname, 'r') as f:
                    dumpFileName = f.readline().rstrip('\n')
                    datetimeStr = f.readline().rstrip('\n')
                    exceptionClass = f.readline().rstrip('\n')
                    exceptionDesc = f.read()
                    LOG_TRACE('Crash is detected in a previous run %s' % dumpFileName)
                    t = [ int(s) for s in re.findall('\\d\\d', datetimeStr) ]
                    if len(t) > 0:
                        t[0] += 2000
                        timeDelta = datetime.datetime.now() - datetime.datetime(*t)
                    else:
                        timeDelta = datetime.datetime.now() - datetime.datetime.now()
                    data = ''
                    try:
                        with open(os.path.abspath(dumpFileName), 'rb') as fileDump:
                            data = zlib.compress(fileDump.read())
                    except:
                        LOG_WARNING('Error opening file: %s' % dumpFileName)

                    crashType = 1 if exceptionClass == 'EXCEPTION_CPP' else 0
                    self.forceChangeSessionKey = True
                    self.sendCrashReport(timeDelta.seconds, crashType, exceptionClass, exceptionDesc, data)
                os.remove(fname)
        except:
            LOG_CURRENT_EXCEPTION()

    def sendOperation(self, opCode, callback):
        """
        Needed for VOIP.
        @param opCode: operation code
        @param callback: operation response callback(operation)
        """
        if self.accountCmd is not None:
            op = self.accountCmd.sendOperation(opCode, None, False)
            if callback is not None:
                op.onResponse += callback
            return op
        else:
            LOG_ERROR('sendOperation failed - no operation sender')
            return
            return

    def __stopPackageChain(self):
        if self.__lastProcessedPkgCallback is not None:
            BigWorld.cancelCallback(self.__lastProcessedPkgCallback)
            self.__lastProcessedPkgCallback = None
        return

    def __updateLastProcessedPkg(self):
        self.__stopPackageChain()
        lastProcessed = getAdapter('ILastProcessedResponse', ['account'])(None, None)
        if self.__lastProcessedPkgIndex != lastProcessed['rid']:
            LOG_TRACE('Sending last package index: {0}'.format(lastProcessed['rid']))
            self.base.lastProcessedPkg(lastProcessed['rid'])
            self.__lastProcessedPkgIndex = lastProcessed['rid']
        self.__lastProcessedPkgCallback = BigWorld.callback(PKG_SEND_INTERVAL, self.__updateLastProcessedPkg)
        return

    def voipClientStatus(self, channelType, channelName, status):
        if hasattr(self.base, 'voipClientStatus'):
            if not self.__waitVoipClientStatus:
                self.__waitVoipClientStatus = True
                self.base.voipClientStatus(channelType, channelName, status)
        else:
            LOG_ERROR('PlayerAvatar.voipClientStatus: base not ready (?), will retry later')
            BigWorld.callback(3, lambda : self.voipClientStatus(channelType, channelName, status))

    def voipSquadStatus(self, squadID, status):
        self.base.voipSquadStatus(squadID, status)

    def voipMuteClient(self, dbid, mute):
        self.base.voipMuteClient(dbid, mute)

    def voipServerStatus(self, status, args):
        args = dict([ (pair['key'], pair['value']) for pair in args ])
        LOG_TRACE('voipServerStatus %d, args: %r' % (status, args))
        VOIP.api().onServerMessage(status, args)
        self.__waitVoipClientStatus = False

    def clanMembersListDiff(self, clanDBID, membersData):
        membersDiff = cPickle.loads(membersData)
        LOG_INFO('clanMembersListDiff', membersDiff)

    def updateClanInfo(self, clanInfoData):
        clanDBID, clanAbbrev, clanName, clanMotto = wgPickle.loads(wgPickle.FromServerToClient, clanInfoData)
        LOG_INFO('updateClanInfo', clanDBID, clanAbbrev, clanName, clanMotto)

    def __checkClanInfo(self):
        pInfo = BWPersonality.g_initPlayerInfo
        cInfo = BWPersonality.g_clanExtendedInfo
        LOG_DEBUG('check clan info clanId, clanName, members number:', pInfo.clanDBID, cInfo.clanName, len(cInfo.members))
        accountUI = g_windowsManager.getAccountUI()
        if pInfo.clanDBID > 0 and accountUI:
            if cInfo.clanName == '':
                LOG_INFO('clan name is empty, request IClanInfoShort!')
                accountUI.viewIFace([[{'IClanInfoShort': {}}, EMPTY_IDTYPELIST]])
            if len(cInfo.members) == 0:
                LOG_INFO('clan members is empty, request IClanMembers!')
                accountUI.viewIFace([[{'IClanMembers': {}}, EMPTY_IDTYPELIST]])

    def __isVSEReady(self):
        return BigWorld.isVisualScriptRunning() and g_hangarSpace.isVSEPlansStarted

    def callVSE(self, event, param):
        if self.__isVSEReady():
            if self.__queueVSEData:
                self.__queueVSEData.append((event, param))
                for event, param in self.__queueVSEData:
                    LOG_DEBUG('VSEcall: Call from QUEUE', event, param)
                    BigWorld.callback(0, partial(BigWorld.sendVisualScriptEvent, event, param))

                self.__queueVSEData.clear()
            else:
                LOG_DEBUG('VSEcall: Call direct', event, param)
                BigWorld.callback(0, partial(BigWorld.sendVisualScriptEvent, event, param))
        else:
            LOG_DEBUG('VSEcall: Add to queue ', event, param)
            self.__queueVSEData.append((event, param))
            if self.__queueVSECallback is None:
                self.__queueVSECallback = BigWorld.callback(0.1, self.__checkVSEStatusCallback)
        return

    def __checkVSEStatusCallback(self):
        if self.__isVSEReady():
            self.__queueVSECallback = None
            for event, param in self.__queueVSEData:
                LOG_DEBUG('VSEcall: Call from Callback', event, param)
                BigWorld.callback(0, partial(BigWorld.sendVisualScriptEvent, event, param))

            self.__queueVSEData.clear()
            self.__queueVSECallback = None
        else:
            self.__queueVSECallback = BigWorld.callback(0.1, self.__checkVSEStatusCallback)
        return


class _AccountRepository(object):

    def __init__(self, name):
        pass


def _delAccountRepository():
    global _g_accountRepository
    LOG_MX('_delAccountRepository')
    _g_accountRepository = None
    return


Account = PlayerAccount