# Embedded file name: scripts/client/gui/Scaleform/Lobby.py
from OperationCodes import OPERATION_RETURN_CODE
import BigWorld, ResMgr, Settings
from HelperFunctions import findIf
import VOIP
import _economics
import _tutorial_data
import config_consts
from consts import GAME_MODE, INACTIVE_ACCOUNT_DISCONNECT_TIME, BLOCK_TYPE, TUTORIAL_LESSON_INVITE_DISABLE_PLANE_LEVEL, EMPTY_IDTYPELIST, CLIENT_STATS_TYPE, WAITING_INFO_TYPE, CLIENT_UPDATE_STATS_PERIOD, CLIENT_UPDATE_HANGAR_PERIOD
from config_consts import IS_CHINA
from clientConsts import LAYER_0_IMPORTED
import db.DBLogic
import ClientLog
import consts
from gui.Scaleform.LobbyModulesTreeHelper import LobbyModulesTreeHelper, AircraftCharacteristicsDataVO
import messenger
from Helpers.i18n import localizeOptions, getFormattedTime, localizeTutorial, localizeMessages, localizeLobby, localizeAchievements
from gui.WebPageHolder import WebPageHolder
from gui.Scaleform.utils.HangarSpace import g_hangarSpace
from gui.Scaleform.windows import GUIWindowAccount
from gui.Scaleform.Waiting import Waiting, WaitingFlags
from gui.Scaleform.PartSender import PartSender
from gui.Scaleform.TrainingRoomsHelper import TrainingRoomHelper
from gui.Scaleform.LobbyShopHelper import LobbyShopHelper
from gui.Scaleform.ResearchTreeHelper import ResearchTreeHelper
from gui.Scaleform.LobbyAirplaneHelper import ExchangeExpItemVO, getUpgradeSpecs
from gui.Scaleform.WebBrowser import WebBrowser
from debug_utils import LOG_DEBUG, LOG_ERROR, LOG_INFO, LOG_WARNING, LOG_NOTE, LOG_CURRENT_EXCEPTION, LOG_TRACE
import time
from functools import partial
import re
from LobbyCustomization import LobbyCustomization
from consts import CAMOUFLAGE_GROUPS, calculateGunDPS
from consts import UPGRADE_TYPE, PREMIUM_TIME_LIMIT, REQUEST_STAT_TYPE_FLAGS
import Helpers
from gui.Scaleform.utils.MeasurementSystem import MeasurementSystem
from gui.Scaleform.LobbyAirplaneHelper import getLobbyAirplane
from clientConsts import BATTLE_NAME_BY_TYPE_HUD_LOC_ID, BATTLE_LOBBY_DESC_BY_TYPE_HUD_LOC_ID, BATTLE_LOBBY_ICON_BY_TYPE_HUD_LOC_ID, KEY_RESEARCH_TREE_NATION, KEY_RESEARCH_TREE_NATION_LIST, KEY_RESEARCH_TREE_DEV_NATION_LIST, HANGAR_MODE, HANGAR_BUTTONS, DISABLE_TUTORIAL_PROMPT_WINDOW, TUTORIAL_DATA_WAITING_SCREEN_MESSAGE, PVE_DATA_WAITING_SCREEN_MESSAGE, CLASTERS, SWITCH_STYLES_BUTTONS, HANGAR_LOBBY_WAITING_SCREEN_MESSAGE
import InputMapping
from SyncOperationKeeper import SyncOperationKeeper, FLAGS_CODE
from Help import Help, HelpSettingsKeys
from exchangeapi.ErrorCodes import SUCCESS
from gui.Scaleform.EULA import OBTIntroInterface, ReleaseIntroInterface, SingleExpIntroInterface, GeneralTestIntroInterface
from UIHelper import onDenunciation
from TutorialClient.TutorialHints import GAME_MODES
from CameraStates import CameraState
from Helpers.cache import getFromCache, deleteFromCache
from account_helpers import ClanEmblemsCache
from gui.Scaleform.WaitingInfoHelper import WaitingInfoHelper
import wgPickle
from audio import GameSound

class MsgBoxBtnVO:

    def __init__(self, id, name):
        self.id = id
        self.name = name


class UpdatePlayerResourcesTypes:
    NORMAL = 0
    EXCHANGE_EXP_CONVERT = 1
    EXCHANGE_GOLD_EXCHANGE = 2


class battleTypeItemVO:

    def __init__(self, mapID = -1, mapName = '', mapDescr = '', mapIcon = ''):
        self.id = mapID
        self.name = mapName
        self.description = mapDescr
        self.icon = mapIcon


class battleTitleItemVO:

    def __init__(self):
        self.name = ''
        self.container = []


class AUTODETECT_WINDOWS:
    WAITING = 1
    REQUEST_QUESTION = 2
    RESULT_BAD = 3
    RESULT_OK = 4
    RESULT_SD_HD = 5


class AUTODETECT_STATES:
    RUN = 0
    WAIT = 1
    SD_HD = 2


class TutorialPromptParams:

    def __init__(self, isBonus, nameReward, countCredits, nameCredits, countExperience, nameExperience, countGolds, nameGolds, title, titleCompleted, description1, description2, type, lessonIndex, isLastLesson):
        self.isBonus = isBonus
        self.nameReward = nameReward
        self.countCredits = countCredits
        self.nameCredits = nameCredits
        self.countExperience = countExperience
        self.nameExperience = nameExperience
        self.countGolds = countGolds
        self.nameGolds = nameGolds
        self.title = title
        self.textCompleted = titleCompleted
        self.description1 = description1
        self.description2 = description2
        self.type = type
        self.lessonIndex = lessonIndex
        self.isLastLesson = isLastLesson


class TutorialLessonVO:

    class LessonStatusEnum:
        CLOSED = 0
        OPENED = 1
        PASSED = 2

    def __init__(self):
        self.id = 0
        self.lessonNumber = 0
        self.lessonName = None
        self.status = 0
        self.disabledTitle = None
        self.time = 0
        self.rewardExp = 0
        self.rewardCreds = 0
        self.rewardGold = 0
        return


class ChatUserItemVO:

    def __init__(self):
        self.jid = ''
        self.name = ''
        self.online = False


class UserChatStatus:

    def __init__(self, dbid = 0, status = 0):
        self.id = dbid
        self.status = status


class Lobby(GUIWindowAccount):
    POPUP_PREMIUM = 0
    POPUP_GOLD_EXCHANGE = 1
    POPUP_EXP_EXCHANGE = 2
    ACTIVATE_PREM_CB_NAME = 'premium.activate'
    PRIZES_WINDOW_SHOW_CB_NAME = 'prizesWindow.show'
    FLASH_ERROR_CB_NAME = 'flash.error'
    FLASH_TRACE_CB_NAME = 'flash.trace'
    FLASH_WAITING_START_CB_NAME = 'flash.waitingStart'
    FLASH_WAITING_STOP_CB_NAME = 'flash.waitingStop'
    WAIT_PLANE_LOADED_CB_NAME = 'lobby.waitPlaneLoaded'

    def __init__(self):
        import BWPersonality
        BWPersonality.g_waitingInfoHelper.startWaiting(WAITING_INFO_TYPE.HANGAR_LOAD)
        BWPersonality.g_waitingInfoHelper.startWaiting(WAITING_INFO_TYPE.HANGAR_ALL_DATA_LOADED)
        Waiting.onHide += self.__initialWaitingHidden
        Waiting.onHide += self.__waitingVisibilityChanged
        Waiting.onShow += self.__waitingVisibilityChanged
        GUIWindowAccount.__init__(self, 'hangar.swf')
        self._planeLoadedSubsciptions = {}
        self._activePopups = []
        self.mode = HANGAR_MODE.HOME
        self.moneySilver = 0
        self.updateCallback = -1
        self.updateClientStatsCallback = -1
        self.innactiveAccountAutoDropperCalback = -1
        self.__modalWindowsQueue = list()
        self.__selectedSlot = -1
        self.__slotsTotal = 0
        self.__flashWaitingId = -1
        self.__flashWaitingList = []
        self.__lockBuyPrem = False
        self.__clanEmblemsReqs = []
        self.trainingRoomHelper = TrainingRoomHelper(self)
        self.researchTreeHelper = ResearchTreeHelper(self)
        self.lobbyShopHelper = LobbyShopHelper(self)
        self.captchaHelper = None
        if BWPersonality.g_initPlayerInfo.captchaEnabled:
            from gui.Scaleform.LobbyCaptchaHelper import LobbyCaptchaHelper
            self.captchaHelper = LobbyCaptchaHelper(self)
        self.AOGASNotifier = None
        if BWPersonality.g_initPlayerInfo.isAOGASEnabled:
            if BWPersonality.g_AOGASNotifier is None:
                from gui.Scaleform.LobbyAOGASNotifier import LobbyAOGASNotifier
                BWPersonality.g_AOGASNotifier = LobbyAOGASNotifier(BWPersonality.g_initPlayerInfo.AOGASParams)
            self.AOGASNotifier = BWPersonality.g_AOGASNotifier
        self.lobbyModulesTreeHelper = LobbyModulesTreeHelper(self)
        Lobby.BATTLE_TYPE_LIST = [consts.ARENA_TYPE.NORMAL, consts.ARENA_TYPE.TRAINING, consts.ARENA_TYPE.PVE]
        if config_consts.IS_DEVELOPMENT:
            Lobby.BATTLE_TYPE_LIST.append(consts.ARENA_TYPE.TUTORIAL)
        self.__messagesWindowReady = False
        self.dbgHideHangarPlane = False
        self.__lobbyCarouselHelper = BWPersonality.g_lobbyCarouselHelper
        self.__lobbyCarouselHelper.setHandler(self)
        self.__onTutorialInitializedCallback = None
        self.__notCompleteTutorialLessonIndex = 0
        player = self.getPlayer()
        if player is not None:
            player.onUpdatePremiumTime += self.__onUpdatePremiumTime
            player.onInitPremium += self.__onInitPremium
        self.__playerResources = {'credits': 0,
         'experience': 0,
         'gold': 0}
        self.__premiumExpiryTime = -1
        self.__inTrainingRoom = False
        self.__autodetectState = None
        Settings.g_instance.onMeasurementSystemChanged += self.__onMeasurementSystemChanged
        Settings.g_instance.eDetectBestSettingsAdvStart += self.__detectBestSettingsAdvCallbackStart
        Settings.g_instance.eDetectBestSettingsAdvEnd += self.__detectBestSettingsAdvCallbackEnd
        g_hangarSpace.eOnVehicleStart += self.__onVehicleStart
        g_hangarSpace.eOnVehicleLoaded += self.__onVehicleLoaded
        self.__tutorialLessonsListInitialized = False
        self.__msgBoxBtnDelegates = dict()
        self.__msgBoxShown = False
        self.__msgBoxBtnIdCounter = 0
        self.__msgBoxMessagesCache = list()
        self.__gunsDps = dict()
        self.__tutorialWaitingID = -1
        self.__tutorialInvitationCB = None
        self.__isOpenShopLink = False
        self.__camTargetShiftLobbyModes = set([HANGAR_MODE.AMMUNITION,
         HANGAR_MODE.MODULES,
         HANGAR_MODE.CUSTOMIZATION,
         HANGAR_MODE.CREW])
        self.__autodetectWaitingID = -1
        self.__pvpUnlocked = False
        self.__webBrowser = WebBrowser(self)
        return

    @property
    def inTrainingRoom(self):
        return self.__inTrainingRoom

    def _isPopupActive(self, popupType):
        """
        :param popupType: popup type constant, e.g. Lobby.POPUP_PREMIUM
        """
        return popupType in self._activePopups

    def _popupActivated(self, popupType, state):
        """
        :param popupType: popup type constant, e.g. Lobby.POPUP_PREMIUM
        :param state: popup state - true for shown, false for hidden
        """
        if popupType in self._activePopups:
            if not state:
                self._activePopups.remove(popupType)
            return
        if state:
            self._activePopups.append(popupType)

    def initialized(self):
        import BWPersonality
        self.mode = HANGAR_MODE.HOME
        self.movie.backgroundAlpha = 0.0
        self.addExternalCallbacks({'hangar.GetAirplanesList': self.__lobbyCarouselHelper.getAirplanesListRequest,
         'hangar.SelectedPlaneID': self.__onSelectedPlaneID,
         'hangar.RepairPlane': self.__lobbyCarouselHelper.onRequestRepairPlane,
         'hangar.SetPrimary': self.__lobbyCarouselHelper.onSetAirplanePrimary,
         'hangar.PlaneInfoRequest': self.__lobbyCarouselHelper.onGetAirplaneDescription,
         'hangar.JoinBattle': self.onJoinBattle,
         'hangar.SpaceMove': self.onSpaceMove,
         'hangar.BattleTypeSelected': self.onBattleTypeSelected,
         'hangar.SetMode': self.onSetMode,
         'hangar.UIready': self.onUIReady,
         'hangar.onLobbyButtonClick': self.onLobbyButtonClick,
         'hangar.getNextAircraftsPart': self.__lobbyCarouselHelper.getNextAircraftsPart,
         'hangar.getCustomizationList': self.__getCustomizationList,
         'hangar.previewCustomization': self.__setCamouflagesForPreview,
         'hangar.showPreview': self.__switchPreviewCustomizationVisibility,
         'hangar.getUpgradeCharacteristics': self.__getUpgradeCharacteristics,
         'hangar.getClanEmblem': self.__getClanEmblem,
         'shop.GetShopPlanes': self.lobbyShopHelper.onGetShopAirlanesRequest,
         'shop.GetPlaneDescription': self.lobbyShopHelper.onUpdateShopAirplaneDescription,
         'messages.GetMessagesList': self.onGetMessagesList,
         'settings.GetSettings': self.onEnterOptions,
         'settings.Close': self.onCloseOptions,
         'hangarMenu.ServerDisconnecting': self.onServerDisconnecting,
         'hangarMenu.QuitGame': self.onQuitGame,
         'hangarMenu.LoginForum': self.onLoginForum,
         'hangarMenu.SendError': self.onSendError,
         'hangarMenu.OpenAchievements': self.onAchievements,
         'hangarMenu.BuyGold': self.onBuyGold,
         'hangarMenu.BuyQuestChips': self.onBuyQuestChips,
         'trainingRoomsList.initialized': self.trainingRoomHelper.onInitialized,
         'trainingRoomsList.RefreshRoomList': self.trainingRoomHelper.onRefreshRoomList,
         'trainingRoomsList.Close': self.trainingRoomHelper.onCloseTrainingRoomList,
         'trainingRoomsList.onEnterToRoom': self.trainingRoomHelper.onEnterTrainingRoom,
         'trainingsRoomCreating.initialized': self.trainingRoomHelper.onRoomCreateInitialized,
         'trainingsRoomCreating.Continue': self.trainingRoomHelper.onRoomCreateContinue,
         'trainingsRoomCreating.Close': self.trainingRoomHelper.onRoomCreateClose,
         'trainingsRoomTeams.initialized': self.trainingRoomHelper.onRoomTeamsInitialized,
         'trainingsRoomTeams.updateAccountTeamID': self.trainingRoomHelper.onRoomTeamUpdateAccountTeamID,
         'trainingsRoomTeams.AddBots': self.trainingRoomHelper.onRoomTeamAddBots,
         'trainingsRoomTeams.DeleteBot': self.trainingRoomHelper.onRoomTeamDeleteBot,
         'trainingsRoomTeams.fillBots': self.trainingRoomHelper.onRoomTeamBotsAutoFill,
         'trainingsRoomTeams.editBot': self.trainingRoomHelper.editBot,
         'trainingsRoomTeams.swapTeams': self.trainingRoomHelper.swapTeams,
         'trainingsRoomTeams.moveTeam': self.trainingRoomHelper.moveTeam,
         'trainingsRoomTeams.removeBots': self.trainingRoomHelper.onRoomTeamBotsRemove,
         'trainingsRoomTeams.Close': self.trainingRoomHelper.onCloseTrainingTeams,
         'trainingsRoomTeams.changeMap': self.trainingRoomHelper.onChangeMap,
         'trainingsRoomTeams.changeDescription': self.trainingRoomHelper.onChangeDescription,
         'trainingsRoomPreview.initialized': self.trainingRoomHelper.onRoomPreviewInitialized,
         'trainingsRoomPreview.closed': self.trainingRoomHelper.onRoomPreviewClosed,
         'trainingRooms.Leave': self.trainingRoomHelper.onTrainingRoomLeave,
         'research.Initialized': self.researchTreeHelper.onInitialized,
         'research.NationTreeId': self.researchTreeHelper.onGetAircraftsDataByNationID,
         'research.ResearchPlane': self.researchTreeHelper.onAircraftResearch,
         'research.GetAircraftUpgrades': self.researchTreeHelper.onGetAircraftUpgrades,
         'research.GetUpgradesList': self.__lobbyCarouselHelper.sendUpgradesListToAS,
         'research.showModulesTree': self.researchTreeHelper.onEnteredAircrafID,
         'research.BackToResearchTree': self.researchTreeHelper.onBackToResearchTree,
         'buyPremium.initialized': self.__onBuyPremiumInitialization,
         'buyPremium.Buy': self.__onBuyPremiumAccept,
         'buyPremium.disposed': self.__onBuyPremiumDisposed,
         'exchangeExp.initialized': self.__onExchangeExpInitialization,
         'exchangeExp.disposed': self.__onExchangeExpDispose,
         'exchangeExp.Convert': self.__onExchangeExpConvert,
         'exchangeGold.initialized': self.__onExchangeGoldInitialization,
         'exchangeGold.disposed': self.__onExchangeGoldDispose,
         'exchangeGold.Exchange': self.__onExchangeGoldExchange,
         'hangar.startTutorial': self.onStartTutorial,
         'hangar.lessonListClose': self.__onTutorialLessonListClosed,
         'hangar.rejectionTutorial': self.__onTutorialInviteReject,
         'hangar.tutorialDequeued': self.__onTutorialDequeued,
         'hangar.tutorialInitialized': self.__onTutorialInitialized,
         'maintenance.SetAutoRepair': self.__setAirplaneAutoRepairFlag,
         'maintenance.SetShellsAutoRefillingFlag': self.onSetShellsAutoRefillingFlag,
         'hangar.onMessageButtonClick': self.__onMsgBoxBtnClick,
         'chat.searchUsersByName': self.__onSearchUsersByName,
         'chat.createChannel': self.__onCreateChannel,
         'chat.deleteChannel': self.__onDeleteChannel,
         'chat.joinChannel': self.__onJoinChannel,
         'chat.leaveChannel': self.__onLeaveChannel,
         'chat.kickFromChannel': self.__onKickFromChannel,
         'chat.editFriendStatus': self.__editFriendStatus,
         'chat.editIgnoreStatus': self.__editIgnoreStatus,
         'chat.getUsersChatStatus': self.__getUsersChatStatus,
         'chat.joinPrivateChannel': self.__onJoinPrivateChannel,
         'voip.subscribeSquadMemberObserver': self.__voipSubscribeSquadMemberObserver,
         'voip.unsubscribeSquadMemberObserver': self.__voipUnsubscribeSquadMemberObserver,
         'obtIntro.closed': self.__obtIntroClose,
         'obtIntro.initialized': self.__obtIntroInitialized,
         'obtIntro.OpenLink': self.__obtIntroOpenLink,
         'introRelease.closed': self.__ReleaseIntroClose,
         'introRelease.initialized': self.__ReleaseIntroInitialized,
         'introRelease.OpenLink': self.__ReleaseIntroOpenLink,
         'introExp.closed': self.__SingleExpIntroClose,
         'introExp.initialized': self.__SingleExpIntroInitialized,
         'introExp.OpenLink': self.__SingleExpIntroOpenLink,
         'introGeneralTest.closed': self.__GeneralTestIntroClose,
         'introGeneralTest.initialized': self.__GeneralTestIntroInitialized,
         'introGeneralTest.OpenLink': self.__GeneralTestIntroOpenLink,
         'lobby.TokensHelp': lambda args: WebPageHolder().openWebBrowser(WebPageHolder.URL_TOKENS_HELP),
         'hangar.hideGiftPlaneWindow': self.__popWindowsQueue,
         'hangar.waitingShow': self.__showFlashWaitingScreen,
         'hangar.waitingHide': self.__hideFlashWaitingScreen,
         'hangar.startForWaitingArena': BigWorld.player().startWaitingForArena,
         'hangar.stopForWaitingArena': BigWorld.player().stopWaitingForArena,
         'hangar.onDenunciation': self.__onDenunciation,
         'autodetect.initialized': self.__settingsAutodetectInitialized,
         'autodetect.apply': self.__settingsAutodetectApply,
         'autodetect.start': self.__settingsAutodetectStart,
         'browser.initialized': self.__onWebBrowserInitialized,
         'browser.refresh': self.__onWebBrowserRefresh,
         'browser.close': self.__onWebBrowserClose,
         'browser.mouse': self.__onWebBrowserMouseMove,
         self.FLASH_ERROR_CB_NAME: self.__logFlashError,
         self.FLASH_TRACE_CB_NAME: self.__logFlashTrace,
         self.FLASH_WAITING_START_CB_NAME: BWPersonality.g_waitingInfoHelper.startWaiting,
         self.FLASH_WAITING_STOP_CB_NAME: BWPersonality.g_waitingInfoHelper.stopWaiting,
         self.PRIZES_WINDOW_SHOW_CB_NAME: self._prizesWindowShow,
         self.ACTIVATE_PREM_CB_NAME: self._activatePremium,
         self.WAIT_PLANE_LOADED_CB_NAME: self._waitPlaneLoaded})
        if self.captchaHelper is not None:
            self.captchaHelper.registerCallbacks()
        self.lobbyModulesTreeHelper.registerCallbacks()
        GUIWindowAccount.initialized(self)
        self.call_1('hangar.fromOutro', BWPersonality.g_fromOutro)
        BWPersonality.g_fromOutro = False
        if self.__lobbyCarouselHelper.isInventoryReady:
            LOG_DEBUG('Lobby initialized. Syncing actions.')
            BigWorld.player().syncActionList()
        self.__onDenunciationsLeft()
        self.__setNationList()
        self.updatePlayerInfo()
        self.updateMoneyPanelRequest()
        if self.captchaHelper is not None:

            def onCaptchaData(isSuccess):
                if isSuccess and self.captchaHelper.isCaptchaRequired():
                    self.captchaHelper.showCaptcha()

            self.captchaHelper.updateDataRequest(onCaptchaData)
        if self.AOGASNotifier is not None:
            self.AOGASNotifier.enableNotifyAccount(self)
        self.updateCallback = BigWorld.callback(1.73, self.__updatePlayersCount)
        self.updateClientStatsCallback = BigWorld.callback(CLIENT_UPDATE_STATS_PERIOD, self.__updateClientStats)
        self.__initInnactiveAccountAutoDropTimer()
        player = self.getPlayer()
        if player is not None:
            player.accountCmd.showTrainingRoomResponse()
        if Settings.g_instance.clusterID == CLASTERS.CN:
            self._startTickerNews()
        if Settings.g_instance.clusterID == CLASTERS.CN:
            self.__webBrowser.showIfNecessary()
        Waiting.addErrorCB(self.__waitingError)
        return

    def _prizesWindowShow(self, value):
        self.__lobbyCarouselHelper.prizesWindowShown(value)

    def _activatePremium(self):
        player = self.getPlayer()
        if player is not None:
            player.onPremUserAction()
        self.__lobbyCarouselHelper.addPendingPlanes()
        return

    def _onRssUrlOpen(self, link):
        if self.__webBrowser is not None and self.__webBrowser.shadow is not None:
            self.__webBrowser.shadow.awesomium.loadURL(link)
        else:
            WebPageHolder().openUrl(link)
        return

    def __onWebBrowserInitialized(self):
        self.__webBrowser.onOpen()

    def __onWebBrowserRefresh(self):
        self.__webBrowser.onRefresh()

    def __onWebBrowserClose(self):
        self.__webBrowser.onClose()

    def __onWebBrowserMouseMove(self, xpos, ypos):
        self.__webBrowser.handleMouseMoveEvent(xpos, ypos)

    def __onDenunciation(self, DBId, denunciationID, violatorKind):
        onDenunciation(DBId, denunciationID, violatorKind)
        self.__onDenunciationsLeft()

    def __onDenunciationsLeft(self):
        import BWPersonality
        self.call_1('hangar.denunciations', BWPersonality.g_initPlayerInfo.denunciationsLeft)

    def __processWindowsQueueHead(self):
        Waiting.onHide -= self.__processWindowsQueueHead
        if self.__modalWindowsQueue:
            if Waiting.isVisible():
                Waiting.onHide += self.__processWindowsQueueHead
            else:
                self.__modalWindowsQueue.sort(lambda x, y: cmp(y[3], x[3]))
                self.__modalWindowsQueue[-1][0]()
                if self.__modalWindowsQueue[-1][2]:
                    self.__popWindowsQueue()

    def __pushWindowQueue(self, onShowCallbak, onHideCallback, autoPop = False, order = 0, id = None):
        self.__modalWindowsQueue.insert(0, (onShowCallbak,
         onHideCallback,
         autoPop,
         order,
         id))
        if len(self.__modalWindowsQueue) == 1:
            self.__processWindowsQueueHead()

    def __popWindowsQueue(self):
        if self.__modalWindowsQueue:
            if self.__modalWindowsQueue[-1][1]:
                self.__modalWindowsQueue[-1][1]()
            self.__modalWindowsQueue.pop()
            self.__processWindowsQueueHead()

    def __clearWindowsQueue(self):
        self.__modalWindowsQueue = list()

    def __removeWindowsQueueByID(self, idList, isProcessWindows = False):
        toRemove = [ i for i, window in enumerate(self.__modalWindowsQueue) if window[4] in idList ]
        for i in toRemove:
            self.__modalWindowsQueue.pop(i)

        if isProcessWindows:
            self.__processWindowsQueueHead()

    def __onSelectedPlaneID(self, planeID):
        """
        Call by clicking in carusel on plane, from flash call
        @param planeID: selected plane
        """
        LOG_DEBUG('onSelectedPlaneID {0}'.format(planeID))
        if planeID != -1:
            if not self.__lobbyCarouselHelper.inventory.getAircraftPData(planeID):
                LOG_ERROR('Attempt to select plane (id={0}) that is not present in carousel'.format(planeID))
                return
            if self.trainingRoomHelper:
                d = db.DBLogic.g_instance
                self.trainingRoomHelper.refreshRoomListForChangePlane(planeID, d.getAircraftData(planeID).airplane.level)
        self.__lobbyCarouselHelper.onSelectedPlaneID(planeID)

    def getCarouselSelectedAircraft(self):
        """
        @rtype: LobbyAirplane
        """
        return self.__lobbyCarouselHelper.getCarouselAirplaneSelected()

    def __onExchangeExpInitialization(self):
        self._popupActivated(Lobby.POPUP_EXP_EXCHANGE, True)
        self.updateExpExchangeRate()

    def updateExpExchangeRate(self):
        if not self._isPopupActive(Lobby.POPUP_EXP_EXCHANGE):
            return
        self.getPlayer().accountCmd.getAircraftsExp(self.__onExchangeResourcesResponse)

    def __onExchangeExpDispose(self):
        self._popupActivated(Lobby.POPUP_EXP_EXCHANGE, False)

    def __onExchangeResourcesResponse(self, operation, resultID, planeExp):
        freeExpVO = [ ExchangeExpItemVO(aircraftID, freeExp, isPremium, isElite) for aircraftID, freeExp, isPremium, isElite in planeExp if isElite ]
        self.call_1('exchangeExp.setPlanesFreeExp', freeExpVO)

    def __onExchangeExpConvert(self, aircraftIDs, gold):
        gold = int(gold)
        rateData = getFromCache(EMPTY_IDTYPELIST, 'IExchangeXPRate')
        if rateData is not None:
            freeExp = int(round(gold * rateData['rate']))
            self.getPlayer().accountCmd.buyFreeExp(freeExp, aircraftIDs, gold, partial(self.__onExchangeRespond, UpdatePlayerResourcesTypes.EXCHANGE_EXP_CONVERT))
        return

    def __onExchangeGoldInitialization(self):
        self._popupActivated(Lobby.POPUP_GOLD_EXCHANGE, True)
        self.updateGoldRate()

    def updateGoldRate(self):
        if not self._isPopupActive(Lobby.POPUP_GOLD_EXCHANGE):
            return
        LOG_TRACE('updateGoldRate', _economics.Economics.goldPrice)
        self.call_1('exchangeGold.setRate', _economics.Economics.goldPrice)

    def __onExchangeGoldDispose(self):
        self._popupActivated(Lobby.POPUP_GOLD_EXCHANGE, False)

    def __onExchangeGoldExchange(self, gold):
        credits = gold * _economics.Economics.goldPrice
        LOG_TRACE('__onExchangeGoldExchange', gold, _economics.Economics.goldPrice)
        self.getPlayer().accountCmd.buyCredits(credits, gold, partial(self.__onExchangeRespond, UpdatePlayerResourcesTypes.EXCHANGE_GOLD_EXCHANGE))

    def __onExchangeRespond(self, typeExchange, operation, resultID, aircraftIDs = None):
        LOG_TRACE('__onExchangeRespond', resultID)
        if resultID == OPERATION_RETURN_CODE.SUCCESS:
            GameSound().ui.play('UISoundExchange')
            self.getPlayer().accountCmd.updatePlayerResources(partial(self.updatePlayerResourcesResponse, [partial(self.__exchange, typeExchange, aircraftIDs)]))

    def __exchange(self, typeUpdatePlayerResources, aircraftIDs, operation, resultID, *args):
        LOG_DEBUG('Lobby::__exchange', typeUpdatePlayerResources, aircraftIDs, operation, resultID, args)
        from eventhandlers import onChangeExperience
        if typeUpdatePlayerResources == UpdatePlayerResourcesTypes.EXCHANGE_EXP_CONVERT:
            if aircraftIDs is not None:
                self.__lobbyCarouselHelper.inventory.syncAircraftsData([ planeID for planeID in aircraftIDs if self.__lobbyCarouselHelper.getCarouselAirplane(planeID) is not None ], onChangeExperience.onSynced)
        return

    def onSetShellsAutoRefillingFlag(self, autoRefill, aircraftID):
        plane = self.__lobbyCarouselHelper.getCarouselAirplane(aircraftID)
        if plane is not None:
            plane.autoRefill = autoRefill
            self.call_1('hangar.updateCarouselSlot', aircraftID, plane.getCarouselAirplaneObject())
            self.getPlayer().accountCmd.setShellsAutoRefillingFlag(aircraftID, autoRefill)
        return

    def __setAirplaneAutoRepairFlag(self, autoRepairFlag, planeID):
        player = self.getPlayer()
        if player:
            plane = self.__lobbyCarouselHelper.getCarouselAirplane(planeID)
            if plane is not None:
                plane.autoRepair = autoRepairFlag
                self.call_1('hangar.updateCarouselSlot', planeID, plane.getCarouselAirplaneObject())
            player.accountCmd.setAirplaneAutoRepairFlag(planeID, autoRepairFlag)
        return

    def dispossessUI(self):
        Waiting.removeErrorCB(self.__waitingError)
        GUIWindowAccount.dispossessUI(self)
        self.__clearWindowsQueue()
        player = self.getPlayer()
        if player is not None:
            player.onUpdatePremiumTime -= self.__onUpdatePremiumTime
            player.onInitPremium -= self.__onInitPremium
            player.requestsQueue = []
        Waiting.onHide -= self.__processWindowsQueueHead
        Waiting.onHide -= self.__initialWaitingHidden
        Waiting.onHide -= self.__waitingVisibilityChanged
        Waiting.onShow -= self.__waitingVisibilityChanged
        self.__cancelCallback()
        self.removeAllCallbacks()
        self.trainingRoomHelper.destroy()
        self.trainingRoomHelper = None
        self.lobbyShopHelper.destroy()
        self.lobbyShopHelper = None
        self.researchTreeHelper.destroy()
        self.researchTreeHelper = None
        self.lobbyModulesTreeHelper.destroy()
        self.lobbyModulesTreeHelper = None
        if self.captchaHelper is not None:
            self.captchaHelper.destroy()
            self.captchaHelper = None
        if self.AOGASNotifier is not None:
            self.AOGASNotifier.disableNotifyAccount()
            self.AOGASNotifier = None
        planeInfo = self.__lobbyCarouselHelper.getCarouselAirplaneSelected()
        if planeInfo and planeInfo.customization:
            planeInfo.customization.destroy()
            planeInfo.customization = None
        self.__lobbyCarouselHelper.setHandler(None)
        self.__lobbyCarouselHelper = None
        Settings.g_instance.onMeasurementSystemChanged -= self.__onMeasurementSystemChanged
        Settings.g_instance.eDetectBestSettingsAdvStart -= self.__detectBestSettingsAdvCallbackStart
        Settings.g_instance.eDetectBestSettingsAdvEnd -= self.__detectBestSettingsAdvCallbackEnd
        g_hangarSpace.eOnVehicleLoaded -= self.__onVehicleLoaded
        g_hangarSpace.eOnVehicleStart -= self.__onVehicleStart
        self.__msgBoxBtnDelegates.clear()
        self.__msgBoxBtnDelegates = None
        del self.__msgBoxMessagesCache[:]
        self.__msgBoxMessagesCache = None
        self.__tutorialInvitationCB = None
        self.__webBrowser.release()
        self.__webBrowser = None
        self.__onTutorialInitializedCallback = None
        deleteFromCache(EMPTY_IDTYPELIST, 'ITimeDelta')
        return

    def __initInnactiveAccountAutoDropTimer(self):
        if self.innactiveAccountAutoDropperCalback != -1:
            BigWorld.cancelCallback(self.innactiveAccountAutoDropperCalback)
        if INACTIVE_ACCOUNT_DISCONNECT_TIME:
            self.innactiveAccountAutoDropperCalback = BigWorld.callback(INACTIVE_ACCOUNT_DISCONNECT_TIME, self.__innactiveAccountAutoDrop)

    def __innactiveAccountAutoDrop(self):
        self.onServerDisconnecting()

    def updatePlayerInfo(self):
        """ updatePlayerInfo """
        import BWPersonality
        self.__premiumExpiryTime = BWPersonality.g_initPlayerInfo.premiumExpiryTime
        contactInfo = Settings.g_instance.contactInfo
        serverName = contactInfo.serverName
        isDisableLinks = Settings.g_instance.clusterID == CLASTERS.CN
        LOG_DEBUG('hangar.updatePlayerInfo - accName:%s, clan:%s, isDev:%s, serverName:%s, isDisableLinks:%s' % (BWPersonality.g_initPlayerInfo.accountName,
         BWPersonality.g_initPlayerInfo.clanAbbrev,
         str(bool(BWPersonality.g_initPlayerInfo.isDeveloper)),
         serverName,
         isDisableLinks))
        uiDevFlag = BWPersonality.g_initPlayerInfo.isDeveloper or consts.IS_DEBUG_IMPORTED and (config_consts.IS_DEVELOPMENT or LAYER_0_IMPORTED)
        self.call_1('hangar.updatePlayerInfo', BWPersonality.g_initPlayerInfo.accountName, BWPersonality.g_initPlayerInfo.clanAbbrev, uiDevFlag, serverName, isDisableLinks, BWPersonality.g_initPlayerInfo.databaseID)
        if g_hangarSpace is not None:
            g_hangarSpace.refreshDecals()
        self.__fillBattleTypeList()
        return

    def updateMoneyPanelRequest(self):
        """ Request initial player info needed when lobby started
        These information can be obtained in 'updatePlayerResourcesResponse' callback """
        LOG_DEBUG('Lobby::updateMoneyPanelRequest')
        self.getPlayer().accountCmd.updatePlayerResources(partial(self.updatePlayerResourcesResponse, None))
        return

    def __checkShowHelpOnStart(self):
        if Help.checkShowHelpOnStart(HelpSettingsKeys.HANGAR):
            self.call_1('hangar.showHelp')

    def onStartTutorial(self, lessonIndex):
        self.getPlayer().startTutorial(lessonIndex)
        import BWPersonality
        BWPersonality.g_lastBattleType = consts.ARENA_TYPE.TUTORIAL

    def __showTutorial(self, onInitializedCallback):
        self.__onTutorialInitializedCallback = onInitializedCallback
        self.__pushWindowQueue(lambda : self.call_1('hangar.showTutorial'), None, True, 100)
        return

    def __checkTutorialCompleteForGameMode(self, gameMode, completeLessons):
        """
        @param gameMode: class <GAME_MODES>
        @param completeLessons: <list>
        @return: <bool>
        """
        for lessonID, lessonData in enumerate(_tutorial_data.TutorialData.lesson):
            if lessonData.gameModes == gameMode and lessonID not in completeLessons:
                return False

        return True

    def onEnterHangarAfterBuyPlane(self):
        pass

    def onBuyPlaneResponse(self, airplaneID):
        if db.DBLogic.g_instance.getAircraftData(airplaneID).airplane.level >= TUTORIAL_LESSON_INVITE_DISABLE_PLANE_LEVEL:
            self.call_1('hangar.tutorialInvitationPanel', False, '', 0)
        self.__tutorialInvitationCB = self.onEnterHangarAfterBuyPlane
        GameSound().ui.postEvent('Play_ui_buy_plane')
        self.__lobbyCarouselHelper.inventory.openAircraft(airplaneID)

    def showTutorialWaiting(self, show):
        if self.__tutorialWaitingID >= 0:
            return
        if show:
            self.__tutorialWaitingID = Waiting.show(TUTORIAL_DATA_WAITING_SCREEN_MESSAGE)
        elif self.__tutorialWaitingID >= 0:
            Waiting.hide(self.__tutorialWaitingID)
            self.__tutorialWaitingID = -1

    def __onTutorialInviteReject(self):
        if self.__notCompleteTutorialLessonIndex != -1:
            self.getPlayer().accountCmd.setTutorialInvite(self.__notCompleteTutorialLessonIndex)

    def __onTutorialDequeued(self, queueType):
        player = self.getPlayer()
        if player is not None:
            player.base.leaveWaitingQueue(queueType)
        return

    def __onTutorialInitialized(self):
        pass

    def __onTutorialLessonListClosed(self):
        self.__tutorialLessonsListInitialized = False

    def updatePlayerResourcesResponse(self, callbacks, operation, resultID, *args):
        LOG_DEBUG('Lobby::updatePlayerResourcesResponse', args[0])
        playerResourcesMap = args[0]
        self.moneySilver = playerResourcesMap['credits']
        LOG_NOTE('hangar.updateMoneyPanel', playerResourcesMap['credits'], playerResourcesMap['gold'], playerResourcesMap['experience'], playerResourcesMap['tickets'], playerResourcesMap['questChips'])
        self.call_1('hangar.updateMoneyPanel', playerResourcesMap['credits'], playerResourcesMap['gold'], playerResourcesMap['experience'], playerResourcesMap['tickets'], playerResourcesMap['questChips'])
        if callbacks is not None:
            for callback in callbacks:
                callback(operation, resultID, *args)

        for key, value in playerResourcesMap.items():
            self.__playerResources[key] = value

        return

    def __updatePlayersCount(self):
        """ BigWorld callback that returns total count players on server and players in queue"""
        player = self.getPlayer()
        playersTotal = getattr(player, 'playersCount', 1)
        playersInQueue = getattr(player, 'queueCount', 1)
        self.call_1('hangar.updatePlayersCount', playersTotal, playersInQueue)
        if player is not None:
            player.base.getPlayersCount()
            self.updateCallback = BigWorld.callback(1.73, self.__updatePlayersCount)
        else:
            LOG_ERROR('Lobby::__updatePlayersCount. Player =', player)
            self.updateCallback = -1
        return

    def __updateClientStats(self):
        player = self.getPlayer()
        if player is not None:
            import BWPersonality
            BWPersonality.g_waitingInfoHelper.updateWaitingStats()
            self.updateClientStatsCallback = BigWorld.callback(CLIENT_UPDATE_STATS_PERIOD, self.__updateClientStats)
        else:
            self.updateClientStatsCallback = -1
        return

    class BuyPremiumVO:

        def __init__(self, commercial):
            self.txtCommercial = commercial

    def updatePremiumInfo(self):
        if not self._isPopupActive(Lobby.POPUP_PREMIUM):
            return
        titles = Lobby.BuyPremiumVO(localizeLobby('BUY_PREMIUM_COMMERCIAL_TEXT')) if self.__premiumExpiryTime < 0 else Lobby.BuyPremiumVO(localizeLobby('BUY_PREMIUM_COMMERCIAL_TEXT'))
        self.call_1('buyPremium.setTitleData', titles)
        import BWPersonality
        self.call_1('buyPremium.setData', BWPersonality.g_premiumData)

    def __onBuyPremiumInitialization(self):
        self._popupActivated(Lobby.POPUP_PREMIUM, True)
        self.updatePremiumInfo()

    def __onBuyPremiumDisposed(self):
        self._popupActivated(Lobby.POPUP_PREMIUM, False)

    def __onBuyPremiumAccept(self, timeIndex):
        self.__lockBuyPrem = True
        self.call_1('hangar.canBuyPremiumAccount', False)
        self.getPlayer().accountCmd.buyPremium(timeIndex, partial(self.__onBuyPremiumRespond, self.getPlayer().premiumExpiryTime == 0))

    def __onBuyPremiumRespond(self, refreshPlane, operation, resultID, serverTime, premiumExpiryTime):
        self.__lockBuyPrem = False
        if resultID == OPERATION_RETURN_CODE.SUCCESS:
            self.__premiumExpiryTime = -1 if premiumExpiryTime < serverTime else int(time.time()) + premiumExpiryTime - serverTime
            self.getPlayer().accountCmd.updatePlayerResources(partial(self.updatePlayerResourcesResponse, None))
            selectedPlane = self.__lobbyCarouselHelper.getCarouselAirplaneSelected()
            LOG_TRACE('__onBuyPremiumRespond()', self.__premiumExpiryTime, selectedPlane.planeID if selectedPlane is not None else selectedPlane)
            GameSound().ui.play('UISoundBuyPremium')
            if refreshPlane:
                self.__lobbyCarouselHelper.queryRefresh3DModel(selectedPlane, False, True)
        else:
            import BWPersonality
            self.call_1('hangar.canBuyPremiumAccount', not BWPersonality.g_initPlayerInfo.disableBuyPremium)
        return

    def __onUpdatePremiumTime(self, diffTime):
        oneDay = 86399
        import BWPersonality
        for prem in BWPersonality.g_premiumData:
            prem['isEnabled'] = not self.__lockBuyPrem and prem['days'] * 24 * 3600 + diffTime <= PREMIUM_TIME_LIMIT

        self.call_1('hangar.canBuyPremiumAccount', not self.__lockBuyPrem and diffTime + oneDay <= PREMIUM_TIME_LIMIT and not BWPersonality.g_initPlayerInfo.disableBuyPremium)
        self.call_1('hangar.premiumAccountTimeLeft', diffTime)

    def __onInitPremium(self, isPremium, spaceData):
        import BWPersonality
        currSpaceID = BWPersonality.g_settings.hangarSpaceSettings['spaceID']
        warActionHangar = self.getPlayer()._getWarActionHangar(currSpaceID)
        if not warActionHangar:
            g_hangarSpace.refreshSpace(*spaceData)
        if not isPremium:
            self.__onUpdatePremiumTime(-1)
            self.__premiumExpiryTime = -1
        selectedPlane = self.__lobbyCarouselHelper.getCarouselAirplaneSelected()
        LOG_TRACE('__onInitPremium()', self.dbgHideHangarPlane, self.__premiumExpiryTime, selectedPlane.planeID if selectedPlane is not None else selectedPlane)
        if self.dbgHideHangarPlane:
            g_hangarSpace.refreshVehicle(None)
        elif not warActionHangar:
            vehicleInfo = self.__lobbyCarouselHelper.getCarouselAirplaneSelected()
            self.__lobbyCarouselHelper.queryRefresh3DModel(vehicleInfo, False, True)
        return

    def onGetMessagesList(self):
        """deprecated. should be removed"""
        pass

    def onCarouselLoaded(self):
        self.dbgHideHangarPlane = False
        self.__lobbyCarouselHelper.processDefferdUpdatingPlaneIDs()

    def onSpaceMove(self, dx, dy, dz):
        if g_hangarSpace.space:
            g_hangarSpace.space.handleMouseEvent(int(dx), int(dy), int(dz))

    def onJoinBattle(self, battleType):
        if SyncOperationKeeper.getFlagStatus(FLAGS_CODE.IN_BATTLE):
            return
        else:
            LOG_DEBUG('onJoinBattle. battleType', battleType)
            player = self.getPlayer()
            if player is None:
                LOG_ERROR('Lobby::onJoinBattle. Player =', player)
                return
            if battleType == consts.ARENA_TYPE.TUTORIAL and config_consts.IS_DEVELOPMENT:
                player.startTutorial(self.__notCompleteTutorialLessonIndex)
            return

    def updatePrebattleCreateRoomAvailableFilters(self):
        self.trainingRoomHelper.updatePrebattleCreateRoomAvailableFilters()

    def __onVehicleStart(self):
        self.__showSmallWaiting()

    def __onVehicleLoaded(self):
        import BWPersonality
        self.__hideSmallWaiting()
        player = self.getPlayer()
        if not BWPersonality.g_initGame:
            BWPersonality.g_loadLobbyTime = time.time() - BWPersonality.g_loadLobbyTime
            if player:
                player.base.updateClientDetails(BWPersonality.g_loadLoginTime, BWPersonality.g_loadLobbyTime)
            BWPersonality.g_initGame = True
            self.__checkAutodetectSettings()
        if BWPersonality.g_initPlayerInfo.requestStats & REQUEST_STAT_TYPE_FLAGS.GAME_PLAYER_CONTROL:
            from gui.Scaleform.GameOptions.GameOptionsStats import SettingsStatsManager
            stats = SettingsStatsManager()
            stats.fill()
            if stats.data:
                stats.sendStatsData(player)
            BWPersonality.g_initPlayerInfo.requestStats &= ~REQUEST_STAT_TYPE_FLAGS.GAME_PLAYER_CONTROL
        BigWorld.memoryMark('hangarVehicleLoaded')

    def __showSmallWaiting(self):
        if not Waiting.isVisible():
            self.call_1('updateSmallWaiting', True)

    def __hideSmallWaiting(self):
        self.call_1('updateSmallWaiting', False)

    def __getCustomizationList(self):
        planeInfo = self.__lobbyCarouselHelper.getCarouselAirplaneSelected()
        if planeInfo and planeInfo.customization:
            planeInfo.customization.sendCustomizationList(self)

    def __updateCustomization(self, aircraftID):
        planeInfo = self.__lobbyCarouselHelper.getCarouselAirplane(aircraftID)
        planeInfo.customization.destroy()
        planeInfo.customization = LobbyCustomization(planeInfo.planeID, self.__lobbyCarouselHelper.inventory.getInstalledCamouflages(planeInfo.planeID))
        planeInfo.customization.sendChangedCustomizationList(self)

    def __customizationApplyingRespond(self, aircraftID, operation, resultID, *args):
        self.__lobbyCarouselHelper.inventory.syncAircraftsData([aircraftID], partial(self.__updateCustomization, aircraftID))

    def __setCamouflagesForPreview(self, camouflageHull, camouflageNose, camouflageWings):
        LOG_DEBUG('__setCamouflagesForPreview::from flash', camouflageHull, camouflageNose, camouflageWings)
        planeInfo = self.__lobbyCarouselHelper.getCarouselAirplaneSelected()
        if planeInfo is not None and planeInfo.customization is not None:
            if self.mode != HANGAR_MODE.CUSTOMIZATION:
                camouflageHull = planeInfo.customization.currentCamouflages[CAMOUFLAGE_GROUPS.HULL]
                camouflageNose = planeInfo.customization.currentCamouflages[CAMOUFLAGE_GROUPS.NOSE]
                camouflageWings = planeInfo.customization.currentCamouflages[CAMOUFLAGE_GROUPS.WINGS]
            LOG_DEBUG('__setCamouflagesForPreview::set', camouflageHull, camouflageNose, camouflageWings)
            planeInfo.customization.setCamouflagesForPreview(camouflageHull, camouflageNose, camouflageWings)
        else:
            LOG_ERROR('__setCamouflagesForPreview - planeInfo or customization is None', camouflageHull, camouflageNose, camouflageWings)
        return

    def __switchPreviewCustomizationVisibility(self, isVisible):
        planeInfo = self.__lobbyCarouselHelper.getCarouselAirplaneSelected()
        planeInfo.customization.switchPreviewCustomizationVisibility(isVisible)

    def handleKeyEvent(self, event):
        self.__initInnactiveAccountAutoDropTimer()
        return GUIWindowAccount.handleKeyEvent(self, event)

    def __obtIntroOpen(self):
        if Help.checkShowHelpOnStart(HelpSettingsKeys.HANGAR_OBT_INTRO):
            self.__pushWindowQueue(lambda : self.call_1('hangar.showOBTIntro'), lambda : self.call_1('hangar.hideOBTIntro'), False)

    def __obtIntroClose(self):
        self.__popWindowsQueue()

    def __obtIntroInitialized(self):
        for text in OBTIntroInterface().getText():
            LOG_DEBUG('__obtIntroInitialized', text)
            self.call_1('obtIntro.SetMsg', text)

    def __obtIntroOpenLink(self, link):
        WebPageHolder().openUrl(link)

    def __ReleaseIntroOpen(self):
        if Help.checkShowHelpOnStart(HelpSettingsKeys.HANGAR_RELEASE_INTRO):
            self.__pushWindowQueue(lambda : self.call_1('hangar.showReleaseIntro'), lambda : self.call_1('hangar.hideReleaseIntro'), False, 3)

    def __ReleaseIntroClose(self):
        self.__popWindowsQueue()

    def __ReleaseIntroInitialized(self):
        for text in ReleaseIntroInterface().getText():
            LOG_DEBUG('__ReleaseIntroInitialized', text)
            self.call_1('introRelease.SetMsg', text)

    def __ReleaseIntroOpenLink(self, link):
        WebPageHolder().openUrl(link)

    def SingleExpIntroOpen(self):
        self.__pushWindowQueue(lambda : self.call_1('hangar.showExpIntro'), lambda : self.call_1('hangar.hideExpIntro'), False, 7)

    def __SingleExpIntroClose(self):
        self.__popWindowsQueue()

    def __SingleExpIntroInitialized(self):
        for text in SingleExpIntroInterface().getText():
            LOG_DEBUG('__SingleExpIntroInitialized', text)
            self.call_1('introExp.SetMsg', text)

    def __SingleExpIntroOpenLink(self, link):
        WebPageHolder().openUrl(link)

    def __GeneralTestIntroOpen(self):
        if Help.checkShowHelpOnStart(HelpSettingsKeys.HANGAR_GENERAL_TEST_INTRO, False):
            self.__pushWindowQueue(lambda : self.call_1('hangar.showGeneralTestIntro'), lambda : self.call_1('hangar.hideGeneralTestIntro'), False, 5)

    def __GeneralTestIntroClose(self):
        self.__popWindowsQueue()

    def __GeneralTestIntroInitialized(self):
        for text in GeneralTestIntroInterface().getText():
            LOG_DEBUG('__GeneralTestIntroInitialized', text)
            self.call_1('introGeneralTest.SetMsg', text)

    def __GeneralTestIntroOpenLink(self, link):
        WebPageHolder().openUrl(link)

    def onGameModesParams(self, params):
        self.__pvpUnlocked = params['pvpUnlocked']

    def giftPlaneWindowShow(self):

        def onShowCallbak():
            self.call_1('hangar.showGiftPlaneWindow')

        self.__pushWindowQueue(onShowCallbak, None, False, 9)
        return

    def pveWindowShow(self, msgID, freeXP = 0, credits = 0, gold = 0):

        def onShowCallbak(nameWin):
            self.call_1(nameWin)

        def onShowCallbakParam(nameWin, freeXP, credits, gold):
            self.call_1(nameWin, freeXP, credits, gold)

        if msgID == consts.MESSAGE_TYPE.PVP_FIRST_RUN:
            self.__pushWindowQueue(partial(onShowCallbak, 'hangar.showPvpInfo'), None, True, 9)
        elif msgID == consts.MESSAGE_TYPE.PVE_OLDUSER_WELCOME:
            self.__pushWindowQueue(partial(onShowCallbak, 'hangar.showPveInfoSeniorPracticed'), None, True, 9)
        elif msgID == consts.MESSAGE_TYPE.PVE_COMPLETE_MAIN_QUEST:
            self.__pushWindowQueue(partial(onShowCallbakParam, 'hangar.showPveEndComplete', freeXP, credits, gold), None, True, 9)
        elif msgID == consts.MESSAGE_TYPE.PVE_VS_PVP_INFO:
            self.__pushWindowQueue(partial(onShowCallbak, 'hangar.showPveInviteStandartPracticed'), None, True, 9)
        elif msgID == consts.MESSAGE_TYPE.PVE_INVITE_WELCOME:
            self.__pushWindowQueue(partial(onShowCallbak, 'hangar.showPveInviteWelcome'), None, True, 9)
        return

    def onEnterOptions(self):
        from gui.WindowsManager import g_windowsManager
        g_windowsManager.showOptions()

    def onCloseOptions(self):
        if self._modalScreen:
            self._modalScreen.closeFlash()
        from gui.WindowsManager import g_windowsManager
        g_windowsManager.hideOptions()

    def __onMeasurementSystemChanged(self, measurementSystemIndex):
        self.__lobbyCarouselHelper.refreshSelectedPlane()
        player = self.getPlayer()
        if player is not None:
            player.resendIfaces(['IMeasurementSystem'], ['mixed', 'client'])
        return

    def onServerDisconnecting(self):

        def logoff():
            VOIP.api().onLeaveSquadChannel()
            BigWorld.disconnect()
            BigWorld.clearEntitiesAndSpaces()
            from Helpers import cache
            cache.destroy()
            from gui.WindowsManager import g_windowsManager
            g_windowsManager.showLogin()

        BigWorld.callback(0, logoff)

    def onQuitGame(self):
        BigWorld.quit()

    def onLoginForum(self):
        WebPageHolder().openWebBrowser(WebPageHolder.URL_FORUM)

    def onSendError(self):
        WebPageHolder().openWebBrowser(WebPageHolder.URL_SEND_ERROR)

    def onAchievements(self):
        player = self.getPlayer()
        import BWPersonality
        if BWPersonality.g_initPlayerInfo.accountName is not None and player is not None:
            accountPortalStatsLink = player.getAccountPortalStatsLink(BWPersonality.g_initPlayerInfo.accountName)
            if accountPortalStatsLink is not None:
                WebPageHolder().openWebBrowser(WebPageHolder.URL_ACHIEVEMENTS, accountPortalStatsLink)
        return

    def onBuyGold(self):
        if Settings.g_instance.clusterID == CLASTERS.CN:
            try:
                url = Settings.g_instance.scriptConfig.urls[WebPageHolder.URL_BUY_GOLD]
                import base64
                from ConnectionManager import connectionManager
                areaID = connectionManager.areaID
                loginName = connectionManager.loginName
                if areaID is None or loginName is None:
                    LOG_ERROR('onBuyGold - bad areaID or loginName in scriptConfig', areaID, loginName)
                    return
                userEncoded = base64.b64encode(loginName)
                url = url % {'userEncoded': userEncoded,
                 'areaID': areaID}
                WebPageHolder().openUrl(url)
            except:
                LOG_ERROR('onBuyGold - bad url in scriptConfig')

        elif not self.__isOpenShopLink:
            import BWPersonality
            player = BigWorld.player()
            url = Settings.g_instance.scriptConfig.urls[WebPageHolder.URL_BUY_GOLD]
            url = url % {'spa_id': str(BWPersonality.g_initPlayerInfo.databaseID)}
            WebPageHolder().openUrl(url)
        return

    def onBuyQuestChips(self):
        import BWPersonality
        url = Settings.g_instance.scriptConfig.urls[WebPageHolder.URL_BUY_QUEST_CHIPS]
        WebPageHolder().openUrl(url)

    def isOpenShopLink(self):
        return self.__isOpenShopLink

    def __cancelCallback(self):
        if self.updateCallback != -1:
            BigWorld.cancelCallback(self.updateCallback)
            self.updateCallback = -1
        if self.updateClientStatsCallback != -1:
            BigWorld.cancelCallback(self.updateClientStatsCallback)
            self.updateClientStatsCallback = -1
        if self.innactiveAccountAutoDropperCalback != -1:
            BigWorld.cancelCallback(self.innactiveAccountAutoDropperCalback)
            self.innactiveAccountAutoDropperCalback = -1
        for id, size in self.__clanEmblemsReqs:
            ClanEmblemsCache.g_clanEmblemsCache.cancellCallback(id, size)

        self.__clanEmblemsReqs = []

    def getActiveTreeNationID(self):
        return Settings.g_instance.getResearchTreeValue(KEY_RESEARCH_TREE_NATION)

    def setActiveTreeNationID(self, val):
        Settings.g_instance.setResearchTreeValue(KEY_RESEARCH_TREE_NATION, val)
        Settings.g_instance.save()

    def __setNationList(self):
        nationList = Settings.g_instance.getResearchTreeValue(KEY_RESEARCH_TREE_DEV_NATION_LIST)
        if nationList is not None:
            self.call_1('hangar.setNationSequence', nationList.split(','))
        return

    def showTrainingRoom(self):
        self.call_1('hangar.showTrainingRoom')
        self.__inTrainingRoom = True

    def onBattleTypeSelected(self, battleTypeID):
        LOG_DEBUG('onBattleTypeSelected', battleTypeID)
        import BWPersonality
        if battleTypeID == consts.ARENA_TYPE.TRAINING:
            if not self.__inTrainingRoom:
                if self.__lobbyCarouselHelper.getCarouselAirplaneSelected() is None:
                    return
                self.call_1('hangar.showTrainingRoomList')
                self.__inTrainingRoom = True
        else:
            if battleTypeID == consts.ARENA_TYPE.TUTORIAL:
                self.call_1('hangar.showTutorialLessons')
            self.__inTrainingRoom = False
        BWPersonality.g_lastBattleType = battleTypeID
        return

    def onSetMode(self, mode):
        LOG_DEBUG('onSetMode', mode)
        self.mode = mode
        self.__lobbyCarouselHelper.onLobbyModeChanged(mode)
        if mode == HANGAR_MODE.HOME and self.__tutorialInvitationCB is not None:
            self.__tutorialInvitationCB()
            self.__tutorialInvitationCB = None
        if mode == HANGAR_MODE.CREW:
            self.shiftHangarCamera()
        return

    def shiftHangarCamera(self):
        clientHangarSpace = g_hangarSpace.space
        if clientHangarSpace:
            hangarCamera = clientHangarSpace.hangarCamera
            if hangarCamera and hangarCamera.getState() == CameraState.Free:
                hangarCamera.getStateObject().setCameraTargetShift(self.mode in self.__camTargetShiftLobbyModes)

    def onUIReady(self):
        self.shiftHangarCamera()

    def onLobbyButtonClick(self, id):
        LOG_DEBUG('onLobbyButtonClick', id)

    def getPlayer(self):
        player = BigWorld.player()
        from Account import PlayerAccount
        if player is not None and player.__class__ == PlayerAccount:
            return player
        else:
            LOG_ERROR('Lobby::getPlayer. Player =', player)
            return
            return

    def __fillBattleTypeList(self):
        import BWPersonality
        battleTypeASList = []
        for battleType in Lobby.BATTLE_TYPE_LIST:
            itemVO = battleTypeItemVO(battleType, localizeLobby(BATTLE_NAME_BY_TYPE_HUD_LOC_ID[battleType]), localizeLobby(BATTLE_LOBBY_DESC_BY_TYPE_HUD_LOC_ID[battleType]), BATTLE_LOBBY_ICON_BY_TYPE_HUD_LOC_ID[battleType])
            if BWPersonality.g_initPlayerInfo.attrs & consts.ACCOUNT_ATTR.RANDOM_BATTLES:
                battleTypeASList.append(itemVO)

        battleTitleSingleVO = battleTitleItemVO()
        battleTitleSingleVO.name = localizeLobby('BATTLE_TITLE_SINGLE_MODE')
        battleTitleSingleVO.container = [consts.ARENA_TYPE.NORMAL, consts.ARENA_TYPE.TUTORIAL, consts.ARENA_TYPE.PVE]
        battleTitleWithFriendsVO = battleTitleItemVO()
        battleTitleWithFriendsVO.name = localizeLobby('BATTLE_TITLE_WITH_FRIENDS_MODE')
        battleTitleWithFriendsVO.container = [consts.ARENA_TYPE.TRAINING]

    def __getUpgradeCharacteristics(self, nameID):
        LOG_DEBUG('getUpgradeCharacteristics', nameID)

        class CharacteristsicsDataVO:

            def __init__(self, name, level, characteristics):
                self.name = name
                self.level = level
                self.characteristics = characteristics

        d = db.DBLogic.g_instance
        aircraftID = self.researchTreeHelper.enteredInAircraftID
        if aircraftID is None:
            aircraftID = self.lobbyModulesTreeHelper.getSelectedPlaneID()
        if aircraftID is None:
            aircraftID = self.__lobbyCarouselHelper.getCarouselAirplaneSelected().planeID
        if aircraftID is None:
            LOG_ERROR('Not found suitable aircraftID, mode=%s, part nameID=%s' % (str(self.mode), str(nameID)))
            return
        else:
            selectedPlaneName = d.getAircraftName(aircraftID)
            upgrade = d.upgrades.get(nameID, None)
            if upgrade is not None:
                localizedName, specs, _, _ = getUpgradeSpecs(upgrade, aircraftID)
                self.call_1('hangar.getUpgradeCharacteristicsData', CharacteristsicsDataVO(localizedName, upgrade.level, specs))
            return

    def __getClanEmblem(self, clanID, emblemSize):
        LOG_DEBUG('getClanEmblem', clanID, emblemSize)
        if clanID > 0:
            self.__clanEmblemsReqs.append((clanID, emblemSize))
            ClanEmblemsCache.g_clanEmblemsCache.get(clanID, self.__onReceiveClanEmblem, False, emblemSize)

    def __onReceiveClanEmblem(self, id, texture, size):
        if texture:
            LOG_DEBUG('lobby: received clan emblem:', id, texture, size)
            self.__clanEmblemsReqs.remove((id, size))
            self.call_1('hangar.setClanEmblem', id, texture, size)

    def showMessageBox(self, title, msg, btn1Name, btn1callback, btn2Name, btn2callback, cacheIfShown = True):
        """
        @param title:
        @param msg:
        @type btn1Name: string
        @param btn1callback:
        @type btn2Name: string
        @param btn2callback:
        @param cacheIfShown: cache message if msg box is already shown. Cached messages will be shown automatically
        @return: btn1Id, btn2Id
        """
        btn1VO = None
        if btn1Name is not None:
            btn1VO = MsgBoxBtnVO(self.__msgBoxBtnIdCounter, btn1Name)
            if btn1callback:
                self.__msgBoxBtnDelegates[self.__msgBoxBtnIdCounter] = btn1callback
            self.__msgBoxBtnIdCounter += 1
        btn2VO = None
        if btn2Name is not None:
            btn2VO = MsgBoxBtnVO(self.__msgBoxBtnIdCounter, btn2Name)
            if btn2callback:
                self.__msgBoxBtnDelegates[self.__msgBoxBtnIdCounter] = btn2callback
            self.__msgBoxBtnIdCounter += 1
        if self.__msgBoxShown:
            if cacheIfShown:
                self.__msgBoxMessagesCache.append((title,
                 msg,
                 btn1Name,
                 btn1callback,
                 btn2Name,
                 btn2callback,
                 cacheIfShown))
                return
            self.call_1('hangar.hideMessage')
        self.call_1('hangar.showMessage', title, msg, btn1VO, btn2VO)
        self.__msgBoxShown = True
        return

    def __onMsgBoxBtnClick(self, btnId):
        self.__msgBoxShown = False
        callback = self.__msgBoxBtnDelegates.get(int(btnId), None)
        if callback:
            callback()
        if len(self.__msgBoxMessagesCache) > 0:
            params = self.__msgBoxMessagesCache.pop(0)
            self.showMessageBox(*params)
        return

    def __onSearchUsersByName(self, strTemplate):
        if messenger.g_xmppChatHandler and strTemplate:
            messenger.g_xmppChatHandler.searchUsersByName(strTemplate, 0, self.__updateSearchResult)

    def __onCreateChannel(self, callbackStr):
        if messenger.g_xmppChatHandler:
            from messenger.XmppChat import ChannelType
            jid, password = messenger.g_xmppChatHandler.createChannel(ChannelType.SQUAD)
            self.call_1(callbackStr, jid, password)

    def __onDeleteChannel(self, jid):
        if messenger.g_xmppChatHandler and jid:
            messenger.g_xmppChatHandler.deleteChannel(jid)

    def __onJoinChannel(self, jid, password = ''):
        if messenger.g_xmppChatHandler and jid:
            messenger.g_xmppChatHandler.joinChannel(jid, password)

    def __onJoinPrivateChannel(self, userId, name):
        xmppHandler = messenger.g_xmppChatHandler
        if xmppHandler and userId and name:
            jid = '%s@%s' % (userId, xmppHandler.params['xmpp_host'])
            xmppHandler.joinChannel(jid, '', name)

    def __onLeaveChannel(self, jid):
        if messenger.g_xmppChatHandler and jid:
            messenger.g_xmppChatHandler.leaveChannel(jid)

    def __onKickFromChannel(self, jid, user):
        if messenger.g_xmppChatHandler and jid and user:
            messenger.g_xmppChatHandler.kickFromChannel(jid, user)

    def __editFriendStatus(self, dbid, userName, operation):
        LOG_DEBUG('__editFriendStatus', dbid, operation)
        if messenger.g_xmppChatHandler:
            messenger.g_xmppChatHandler.editFriendList(dbid, userName, operation)

    def __editIgnoreStatus(self, dbid, userName, operation):
        LOG_DEBUG('__editIgnoreStatus', dbid, operation)
        if messenger.g_xmppChatHandler:
            messenger.g_xmppChatHandler.editIgnoreList(dbid, userName, operation)

    def __getUsersChatStatus(self, dbidList):
        if messenger.g_xmppChatHandler:
            messenger.g_xmppChatHandler.getUsersChatStatus(dbidList)

    def setUsersChatStatus(self, usersList):
        chatStatusList = []
        for userStatus in usersList:
            itemVO = UserChatStatus(userStatus[0], userStatus[1])
            chatStatusList.append(itemVO)

        self.call_1('chat.usersSetChatStatus', chatStatusList)

    def __voipSubscribeSquadMemberObserver(self, funcName):
        VOIP.api().subscribeMemberStateObserver(consts.VOIP.MEMBER_STATUS_OBSERVER_TYPES.LOBBY_SQUAD_PANEL, funcName)

    def __voipUnsubscribeSquadMemberObserver(self, funcName):
        VOIP.api().unsubscribeMemberStateObserver(consts.VOIP.MEMBER_STATUS_OBSERVER_TYPES.LOBBY_SQUAD_PANEL, funcName)

    def addUserToSquad(self, dbid):
        self.call_1('chat.addUserToSquad', [str(dbid)])

    def showUserGameStatistics(self, dbid, nickname, clanTag):
        self.call_1('chat.showUserGameStatistics', str(dbid), nickname, clanTag)

    def __updateSearchResult(self, args, error):
        if error:
            return
        result = []
        xmppParams = messenger.g_xmppChatHandler.params
        for spaID, nickname, isOnline in args:
            if spaID != xmppParams.get('spaID'):
                vo = ChatUserItemVO()
                vo.jid = '%d@%s' % (spaID, xmppParams.get('xmpp_host'))
                vo.name = nickname
                vo.online = isOnline
                result.append(vo)

        self.call_1('chat.updateSearchResult', result)

    def __showFlashWaitingScreen(self, screenID, waitingFlag = WaitingFlags.NONE):
        if screenID in self.__flashWaitingList or screenID is None:
            raise Exception("Flash waiting screen '{0}' is already activated".format(screenID))
            return
        else:
            self.__flashWaitingList.append(screenID)
            LOG_DEBUG('Flash waiting show: {0}'.format(screenID))
            if self.__flashWaitingId >= 0:
                return
            self.__flashWaitingId = Waiting.show('LOBBY_LOAD_HANGAR_SPACE_VEHICLE', waitingFlag)
            return

    def __hideFlashWaitingScreen(self, screenID):
        if screenID not in self.__flashWaitingList or screenID is None:
            raise Exception("Flash waiting screen '{0}' is not activated".format(screenID))
            return
        else:
            self.__flashWaitingList.remove(screenID)
            LOG_DEBUG('Flash waiting hide: {0}'.format(screenID))
            if len(self.__flashWaitingList) > 0 or self.__flashWaitingId < 0:
                return
            GameSound().ui.playLobbyResults()
            Waiting.hide(self.__flashWaitingId)
            self.__flashWaitingId = -1
            return

    def __checkAutodetectSettings(self):
        from gui.GraphicsPresets import GraphicsPresets
        if Settings.g_instance.graphicsDetails == GraphicsPresets.CUSTOM_PRESET_KEY:
            Settings.g_instance.setMain(Settings.GS_AUTODETECT_INITED_KEY, True)
            return
        if Settings.g_instance.gsAutodetectEnabled:
            if not getattr(Settings.g_instance, Settings.GS_AUTODETECT_INITED_KEY) or Settings.g_instance.isHardwareChanged() or Settings.g_instance.isContentChanged():
                Settings.g_instance.detectBestSettingsAdv()

    def __detectBestSettingsAdvCallbackStart(self):
        if self.__autodetectState != AUTODETECT_STATES.RUN:
            self.__autodetectState = AUTODETECT_STATES.RUN
            self.__autodetectWaitingID = Waiting.show('SETTINGS_GRAPH_AUTODETECT_IN_PROGRESS_MESSAGE')
            self.__processWindowsQueueHead()

    def __detectBestSettingsAdvCallbackEnd(self):
        s = Settings.g_instance
        bestQuality = s.defaultMain.graphicsDetails
        if bestQuality in ('Very High', 'High') and not s.isHDContent():
            LOG_DEBUG('__detectBestSettingsAdvCallbackEnd - not HDContent', s.graphicsDetails, bestQuality)
            s.setGraphicsDetailsSD()
            if getattr(Settings.g_instance, Settings.GS_AUTODETECT_INITED_KEY):
                self.__autodetectState = AUTODETECT_STATES.SD_HD
                self.call_1('hangar.showAutoDetectionGraphics')
            else:
                self.__closeAutodetectWaiting()
            return
        if s.isHardwareChanged():
            if s.graphicsDetails != bestQuality:
                s.setMain(Settings.GS_AUTODETECT_INITED_KEY, True)
                self.call_1('hangar.showAutoDetectionGraphics')
            else:
                self.__closeAutodetectWaiting()
        elif not getattr(s, Settings.GS_AUTODETECT_INITED_KEY):
            self.__closeAutodetectWaiting()
        else:
            s.setMain(Settings.GS_AUTODETECT_INITED_KEY, True)
            self.call_1('hangar.showAutoDetectionGraphics')

    def __closeAutodetectWaiting(self):
        self.__autodetectState = None
        Settings.g_instance.setMain(Settings.GS_AUTODETECT_INITED_KEY, True)
        Waiting.hide(self.__autodetectWaitingID)
        self.__sendStats(0)
        return

    def __settingsAutodetectStart(self):
        Settings.g_instance.detectBestSettingsAdv()

    def __settingsAutodetectApply(self, result = 0):
        self.__removeWindowsQueueByID(['hangar.showAutoDetectionGraphics', 'autodetect.SetMsg'], True)
        self.__sendStats(result)

    def __sendStats(self, result):
        if result == 0:
            Settings.g_instance.applyAutodetect(Settings.SETTINGS_AUTODETECT_KEYS.GS)
            Settings.g_instance.applyAutodetect(Settings.SETTINGS_AUTODETECT_KEYS.GS_RESOLUTION)
        resDict = [dict(statID=consts.GAME_OPTIONS_STATS_AUTODETECT['GRAPHICS_DETAILS'], floatValue=0, stringValue=str(Settings.g_instance.graphicsDetails)),
         dict(statID=consts.GAME_OPTIONS_STATS_AUTODETECT['HARDWARES'], floatValue=0, stringValue=str(Settings.g_instance.hardwares)),
         dict(statID=consts.GAME_OPTIONS_STATS_AUTODETECT['USER_CHOICE'], floatValue=0, stringValue=str(result)),
         dict(statID=consts.GAME_OPTIONS_STATS_AUTODETECT['RAITING'], floatValue=0, stringValue=str(Settings.g_instance.hardwaresRating()))]
        player = self.getPlayer()
        if player is not None:
            player.base.updateGameOptionsStats(consts.GAME_OPTIONS_STATS_TYPE.GAME_OPTIONS_STATS_AUTODETECT, resDict)
        return

    def __settingsAutodetectInitialized(self):
        if self.__autodetectState == AUTODETECT_STATES.SD_HD:
            self.__autodetectState = None
            resQuality, currentresQualityLoc, bestresQualityLoc = Settings.g_instance.getAutodetect(Settings.SETTINGS_AUTODETECT_KEYS.GS)
            self.__pushWindowQueue(lambda : self.call_1('autodetect.SetMsg', localizeOptions('SETTINGS_MESSAGE_CAN_USE_HD_DOWNLOAD_BUTTON').format(settings=bestresQualityLoc), AUTODETECT_WINDOWS.RESULT_SD_HD), None, False, 0, 'autodetect.SetMsg')
            Waiting.hide(self.__autodetectWaitingID)
        elif self.__autodetectState == AUTODETECT_STATES.RUN:
            self.__autodetectState = None
            resQuality, currentresQualityLoc, bestresQualityLoc = Settings.g_instance.getAutodetect(Settings.SETTINGS_AUTODETECT_KEYS.GS)
            resolutionRes, resolutionCurrent, resolutionBest = Settings.g_instance.getAutodetect(Settings.SETTINGS_AUTODETECT_KEYS.GS_RESOLUTION)
            LOG_DEBUG('__settingsAutodetectInitialized', resQuality, currentresQualityLoc, bestresQualityLoc, resolutionRes, resolutionCurrent, resolutionBest)
            if resQuality == Settings.SETTINGS_AUTODETECT_RESULT.ERROR and resolutionRes == Settings.SETTINGS_AUTODETECT_RESULT.ERROR:
                return
            message = ''
            typeWindow = AUTODETECT_WINDOWS.RESULT_BAD
            if resolutionRes in (Settings.SETTINGS_AUTODETECT_RESULT.ERROR, Settings.SETTINGS_AUTODETECT_RESULT.OK):
                if resQuality == Settings.SETTINGS_AUTODETECT_RESULT.HIGHER:
                    message = localizeOptions('SETTINGS_GRAPH_AUTODETECT_TOO_HIGH_SETTINGS_ONLY_MESSAGE').format(settings_1=currentresQualityLoc, settings_2=bestresQualityLoc)
                elif resQuality == Settings.SETTINGS_AUTODETECT_RESULT.LOWER:
                    message = localizeOptions('SETTINGS_GRAPH_AUTODETECT_TOO_LOW_MESSAGE').format(settings_1=currentresQualityLoc, settings_2=bestresQualityLoc)
                elif resQuality == Settings.SETTINGS_AUTODETECT_RESULT.OK:
                    typeWindow = AUTODETECT_WINDOWS.RESULT_OK
                    message = localizeOptions('SETTINGS_GRAPH_AUTODETECT_OK_MESSAGE').format(settings_1=currentresQualityLoc)
            elif resolutionRes == Settings.SETTINGS_AUTODETECT_RESULT.HIGHER:
                if resQuality == Settings.SETTINGS_AUTODETECT_RESULT.OK:
                    message = localizeOptions('SETTINGS_GRAPH_AUTODETECT_TOO_HIGH_RESOLUTION_ONLY_MESSAGE').format(resolution_1=resolutionCurrent, resolution_2=resolutionBest)
                elif resQuality == Settings.SETTINGS_AUTODETECT_RESULT.HIGHER:
                    message = localizeOptions('SETTINGS_GRAPH_AUTODETECT_TOO_HIGH_MESSAGE').format(settings_1=currentresQualityLoc, resolution_1=resolutionCurrent, settings_2=bestresQualityLoc, resolution_2=resolutionBest)
            if not message:
                typeWindow = AUTODETECT_WINDOWS.RESULT_OK
                message = localizeOptions('SETTINGS_GRAPH_AUTODETECT_OK_MESSAGE').format(settings_1=currentresQualityLoc)
            self.__pushWindowQueue(lambda : self.call_1('autodetect.SetMsg', message, typeWindow), None, False, 0, 'autodetect.SetMsg')
            Waiting.hide(self.__autodetectWaitingID)
        return

    def __logFlashError(self, errorStrings):
        for entry in errorStrings:
            LOG_ERROR('Flash error: {0}'.format(entry))

    def __logFlashTrace(self, *args):
        LOG_TRACE('Flash trace: {0}'.format(', '.join(map(str, args))))

    def __waitingError(self):
        self.call_1('GetPendingIfaces', self.FLASH_ERROR_CB_NAME)

    def __initialWaitingHidden(self):
        if Waiting.isVisible():
            return
        import BWPersonality
        Waiting.onHide -= self.__initialWaitingHidden
        BWPersonality.g_waitingInfoHelper.stopWaiting(WAITING_INFO_TYPE.HANGAR_LOAD)
        BWPersonality.g_waitingInfoHelper.updateWaitingStats()

    def __waitingVisibilityChanged(self):
        self.viewIFace([[{'IWaitingScreen': {}}, EMPTY_IDTYPELIST]], cacheResponse=False)

    def _waitPlaneLoaded(self, planeID, cbName):
        if self.__lobbyCarouselHelper.getCarouselAirplane(planeID) is not None:
            self.call_1(cbName, planeID)
            return
        else:
            self._planeLoadedSubsciptions.setdefault(planeID, []).append(cbName)
            return

    def planeLoaded(self, planeID):
        self.__lobbyCarouselHelper.checkLobbyCrewAnimation()
        callbacks = self._planeLoadedSubsciptions.get(planeID, None)
        if callbacks is not None:
            for cb in callbacks:
                self.call_1(cb, planeID)

            del self._planeLoadedSubsciptions[planeID]
        return