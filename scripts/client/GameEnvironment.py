# Embedded file name: scripts/client/GameEnvironment.py
from Camera import Camera
from ClientArena import ClientArena
from ClientStatsCollector import ClientStatsCollector
from CrewSkills.debug import ENABLED as SkillsDebugEnabled
from Event import Event, EventManager
import gui.hud
import GlobalEvents
from input.InputController import *
import consts
g_instance = None
import BattleReplay
from functools import partial

class GameEnvironment():

    def __init__(self):
        self.__playerAvatar = None
        self.__isStarted = False
        self.__services = {}
        self.__preWorldEvents = []
        self.__events = []
        self.__em = EventManager()
        self.eHideBackendGraphics = Event(self.__em)
        self.eShowBackendGraphics = Event(self.__em)
        self.eChangeLanguage = Event(self.__em)
        self.eUpdateHUDSettings = Event(self.__em)
        self.eMarkersSettingsUpdate = Event(self.__em)
        self.eAimsSettingsUpdate = Event(self.__em)
        self.eUpdateUIComponents = Event(self.__em)
        return

    def __del__(self):
        self.__em.clear()

    def start(self, playerAvatar):
        self.__playerAvatar = playerAvatar
        self.__isStarted = True
        self.__createServices()
        self.__initServices()
        self.__linkPreWorldEvents()

    def end(self):
        self.__destroyServices()
        self.__playerAvatar = None
        self.__isStarted = False
        return

    def __linkPreWorldEvent(self, event, func):
        event += func
        self.__preWorldEvents.append((event, func))

    def __linkPreWorldEvents(self):
        clientArena = self.__services['ClientArena']
        hud = self.__services['HUD']
        input = self.__services['Input']
        cam = self.__services['Camera']
        replay = BattleReplay.g_replay
        self.__linkPreWorldEvent(GlobalEvents.onMovieLoaded, hud.onMovieLoaded)
        self.__linkPreWorldEvent(clientArena.onReceiveTextMessage, hud.showTextMessage)
        self.__linkPreWorldEvent(clientArena.onBattleMessageReactionResult, hud.showBattleMessageReactionResult)
        self.__linkPreWorldEvent(clientArena.onReceiveMarkerMessage, self.__playerAvatar.onReceiveMarkerMessage)
        self.__linkPreWorldEvent(clientArena.onVehicleKilled, self.__playerAvatar.reportDestruction)
        self.__linkPreWorldEvent(clientArena.onGainAward, hud.onReportGainAward)
        self.__linkPreWorldEvent(clientArena.onTeamObjectDestruction, self.__playerAvatar.reportTeamObjectDestruction)
        self.__linkPreWorldEvent(clientArena.onBaseIsUnderAttack, hud.reportBaseIsUnderAttack)
        self.__linkPreWorldEvent(clientArena.onApplyArenaData, hud.applyArenaData)
        self.__linkPreWorldEvent(clientArena.onNewAvatarsInfo, hud.onNewAvatarsInfo)
        self.__linkPreWorldEvent(clientArena.onAllServerDataReceived, hud.onAllServerDataReceived)
        self.__linkPreWorldEvent(clientArena.onReceiveAllTeamObjectsData, hud.onReceiveAllTeamObjectsData)
        self.__linkPreWorldEvent(clientArena.onUpdateTeamSuperiorityPoints, self.__playerAvatar.onUpdateTeamSuperiorityPoints)
        self.__linkPreWorldEvent(clientArena.onReportBattleResult, self.__playerAvatar.onReportBattleResult)
        self.__linkPreWorldEvent(clientArena.onReceiveVOIPChannelCredentials, self.__playerAvatar.onReceiveVOIPChannelCredentials)
        self.__linkPreWorldEvent(clientArena.onRecreateAvatar, hud.restartHUD_QA)
        self.__linkPreWorldEvent(self.eChangeLanguage, hud.onChangeLanguage)
        self.__linkPreWorldEvent(self.eUpdateHUDSettings, hud.onUpdateHUDSettings)
        self.__linkPreWorldEvent(self.eMarkersSettingsUpdate, hud.onMarkersSettingsUpdate)
        self.__linkPreWorldEvent(self.eAimsSettingsUpdate, hud.onAimsSettingsUpdate)
        self.__linkPreWorldEvent(self.eUpdateUIComponents, hud.onUpdateUIComponents)
        self.__linkPreWorldEvent(self.__playerAvatar.eEnterWorldEvent, self.__onEnterWorld)
        self.__linkPreWorldEvent(self.__playerAvatar.eEnterWorldEvent, clientArena.initArenaData)
        self.__linkPreWorldEvent(self.__playerAvatar.eLeaveWorldEvent, self.__onLeaveWorld)
        self.__linkPreWorldEvent(self.__playerAvatar.eLeaveWorldEvent, replay.doLeaveWorld)
        self.__linkPreWorldEvent(self.__playerAvatar.onStateChanged, cam.onPlayerAvatarStateChanged)
        self.__linkPreWorldEvent(input.eAddProcessorListeners, hud.addInputListeners)
        self.__linkPreWorldEvent(input.eAddProcessorListeners, cam.addInputListeners)
        self.__linkPreWorldEvent(input.eAddProcessorListeners, replay.addInputListeners)
        self.__linkPreWorldEvent(cam.eSetCameraRingVisible, hud.setCameraRingVisible)
        self.__linkPreWorldEvent(cam.eSetViewpoint, hud.setRadarViewpoint)
        self.__linkPreWorldEvent(hud.eSetTargetEntity, cam.setTargetEntity)
        self.__linkPreWorldEvent(hud.eSetTargetEntity, self.__playerAvatar.setTargetEntity)

    def __unlinkPreWorldEvents(self):
        self.__preWorldEvents.reverse()
        for ev, fn in self.__preWorldEvents:
            ev -= fn

        self.__preWorldEvents = []

    def __linkEvent(self, event, func):
        event += func
        self.__events.append((event, func))

    def __linkEvents(self):
        clientArena = self.__services['ClientArena']
        hud = self.__services['HUD']
        input = self.__services['Input']
        cam = self.__services['Camera']
        stats = self.__services['ClientStatsCollector']
        replay = BattleReplay.g_replay
        DebugHUD = self.__services.get('DebugHUD')
        self.__linkEvent(GlobalEvents.onHideModalScreen, hud.onHideModalScreen)
        self.__linkEvent(GlobalEvents.onHideModalScreen, input.onHideModalScreen)
        self.__linkEvent(self.eShowBackendGraphics, hud.onHideModalScreen)
        self.__linkEvent(self.eShowBackendGraphics, input.onHideModalScreen)
        self.__linkEvent(self.eShowBackendGraphics, partial(input.setIntermissionMenuMode, False))
        self.__linkEvent(self.eHideBackendGraphics, hud.onHideBackendGraphics)
        self.__linkEvent(self.__playerAvatar.onUpdateArena, clientArena.doUpdateArena)
        self.__linkEvent(self.__playerAvatar.onGunOverheatedEvent, hud.reportOverheatedGun)
        self.__linkEvent(self.__playerAvatar.eArenaLoaded, hud.onArenaLoaded)
        self.__linkEvent(self.__playerAvatar.eArenaLoaded, replay.onArenaLoaded)
        self.__linkEvent(clientArena.onUpdatePlayerStats, hud.onUpdatePlayerStats)
        self.__linkEvent(clientArena.onReceiveMarkerMessage, hud.onReceiveMarkerMessage)
        self.__linkEvent(self.__playerAvatar.eUpdateEngineTemperature, hud.updateEngineTemperature)
        self.__linkEvent(clientArena.onReportBattleResult, hud.onReportBattleResult)
        self.__linkEvent(self.__playerAvatar.ePartFlagSwitchedNotification, hud.onPartFlagSwitchedNotification)
        self.__linkEvent(self.__playerAvatar.ePartFlagSwitchedOn, hud.onPartFlagSwitchedOn)
        self.__linkEvent(self.__playerAvatar.ePartCrit, hud.onPartStateChanging)
        self.__linkEvent(self.__playerAvatar.eSetBombTargetVisible, hud.setBombTargetVisible)
        self.__linkEvent(self.__playerAvatar.onStateChanged, hud.onPlayerAvatarChangeState)
        self.__linkEvent(self.__playerAvatar.eEngineOverheat, hud.reportEngineOverheat)
        self.__linkEvent(self.__playerAvatar.eUpdateEngineState, hud.onUpdateEngineState)
        self.__linkEvent(self.__playerAvatar.eUpdateForce, hud.updateForce)
        self.__linkEvent(clientArena.onTeamObjectDestruction, hud.reportTeamObjectDestruction)
        self.__linkEvent(clientArena.onTeamObjectPartGroupChanged, hud.reportTeamObjectPartGroupChanged)
        self.__linkEvent(clientArena.onScenarioSetIcon, hud.onScenarioSetIcon)
        self.__linkEvent(clientArena.onScenarioSetText, hud.onScenarioSetText)
        self.__linkEvent(self.__playerAvatar.eReportDestruction, hud.onReportDestruction)
        self.__linkEvent(self.__playerAvatar.eRespawn, hud.restart)
        self.__linkEvent(self.__playerAvatar.eReportNoShell, hud.reportNoShell)
        self.__linkEvent(self.__playerAvatar.eUpdateHUDAmmo, hud.updatePlayerAmmo)
        self.__linkEvent(self.__playerAvatar.eVictimInformAboutCrit, hud.onVictimInformAboutCrit)
        self.__linkEvent(self.__playerAvatar.eSendInitialData, hud.initialData)
        self.__linkEvent(self.__playerAvatar.eUpdateHealth, hud.updateHealth)
        self.__linkEvent(self.__playerAvatar.eUpdateConsumables, hud.updateConsumables)
        self.__linkEvent(self.__playerAvatar.onAutopilotEvent, hud.autopilotVisibility)
        self.__linkEvent(self.__playerAvatar.eFlyKeyBoardInputAllowed, input.onFlyKeyBoardInputAllowed)
        self.__linkEvent(self.__playerAvatar.eRespawn, cam.reset)
        self.__linkEvent(self.__playerAvatar.onReceiveServerData, cam.update)
        if hud.isTutorial():
            self.__linkEvent(self.__playerAvatar.onReceiveServerData, hud.updateSpeedTutorial)
        else:
            self.__linkEvent(self.__playerAvatar.onReceiveServerData, hud.updateSpeed)
        self.__linkEvent(self.__playerAvatar.onAvatarLeaveWorldEvent, cam.doAvatarLeaveWorld)
        self.__linkEvent(self.__playerAvatar.eUpdateSpectator, cam.updateSpectator)
        self.__linkEvent(self.__playerAvatar.eUpdateSpectator, hud.updateSpectator)
        self.__linkEvent(self.__playerAvatar.eFlyKeyBoardInputAllowed, cam.onFlyKeyBoardInputAllowed)
        self.__linkEvent(self.__playerAvatar.eFlyKeyBoardInputAllowed, replay.onFlyKeyBoardInputAllowed)
        self.__linkEvent(self.__playerAvatar.eStartCollectClientStats, stats.startCollectClientStats)
        self.__linkEvent(self.__playerAvatar.eStopCollectClientStats, stats.stopCollectClientStats)
        self.__linkEvent(self.__playerAvatar.onStateChanged, input.onPlayerAvatarStateChanged)
        self.__linkEvent(GlobalEvents.onKeyEvent, input.handleKeyEvent)
        if not BattleReplay.isPlaying():
            self.__linkEvent(GlobalEvents.onMouseEvent, cam.processMouseEvent)
        self.__linkEvent(GlobalEvents.onMouseEvent, input.processMouseEvent)
        self.__linkEvent(GlobalEvents.onAxisEvent, input.processJoystickEvent)
        self.__linkEvent(GlobalEvents.onSetFocus, input.onSetFocus)
        self.__linkEvent(GlobalEvents.onRecreateDevice, hud.onRecreateDevice)
        self.__linkEvent(GlobalEvents.onScreenshot, hud.sendMessageToFlash)
        self.__linkEvent(Settings.g_instance.eChangeMiniScreenPosition, hud.updateMiniScreenPosition)
        self.__linkEvent(Settings.g_instance.eChangeRadarPosition, hud.updateRadarPosition)
        self.__linkEvent(Settings.g_instance.eCollisionWarningSystemEnabled, hud.collisionWarningSystemEnabled)
        self.__linkEvent(Settings.g_instance.eAlternativeColorModeEnabled, hud.onAlternativeColorModeEnabled)
        self.__linkEvent(Settings.g_instance.onNavWindowListChanged, hud.onNavWindowListChanged)
        self.__linkEvent(Settings.g_instance.eCombatInterfaceType, hud.onCombatInterfaceType)
        self.__linkEvent(Settings.g_instance.eMainDevicesVisibility, hud.onChangeSpeedometerState)
        self.__linkEvent(Settings.g_instance.eAviaHorizonType, hud.onChangeAviahorizonMode)
        self.__linkEvent(Settings.g_instance.ePlayerListType, hud.onSetPlayerListChangeState)
        self.__linkEvent(Settings.g_instance.onMeasurementSystemChanged, hud.onMeasurementSystemChanged)
        self.__linkEvent(Settings.g_instance.eGameChatEnabled, hud.onGameChatEnabled)
        if not BattleReplay.isPlaying():
            self.__linkEvent(Settings.g_instance.eSetSniperMode, replay.notifySniperModeType)
            self.__linkEvent(Settings.g_instance.eSetSniperMode, cam.setSniperModeType)
        self.__linkEvent(Settings.g_instance.eCameraEffectsSetEnabled, cam.setEffectsEnabled)
        self.__linkEvent(Settings.g_instance.eMaxMouseCombatFovChanged, cam.setMaxMouseCombatFov)
        self.__linkEvent(input.eSideViewPressed, cam.onEnterSideView)
        self.__linkEvent(input.eSideViewReleased, cam.onLeaveSideView)
        self.__linkEvent(input.ePlayerListChangeState, hud.onPlayerListChangeState)
        self.__linkEvent(input.eVisibilityTeams, hud.onVisibilityTeams)
        self.__linkEvent(input.eVisibilityChat, hud.onVisibilityChat)
        self.__linkEvent(self.__playerAvatar.eSwitchedVehicle, hud.onSwitchedVehicle)
        self.__linkEvent(self.__playerAvatar.eAutoAlightFromDestroyedTransport, hud.autoAlightFromDestroyedTransport)
        self.__linkEvent(input.eInputProfileChange, cam.onInputProfileChange)
        self.__linkEvent(input.eBattleModeChange, cam.onBattleModeChange)
        self.__linkEvent(clientArena.onReportBattleResult, replay.onBattleResultsReceived)
        self.__linkEvent(hud.eUpdate1sec, replay.updateHUDProgress)
        self.__linkEvent(clientArena.onLaunch, hud.onLaunch)
        self.__linkEvent(self.__playerAvatar.eUniqueSkillStateChanged, hud.onUniqueSkillStateChanged)
        if DebugHUD and SkillsDebugEnabled:
            self.__linkEvent(self.__playerAvatar.eUniqueSkillStateChanged, DebugHUD.updateAvaibleSkills)
            self.__linkEvent(self.__playerAvatar.eRestartInput, DebugHUD.clearSkills)

    def __unlinkEvents(self):
        self.__events.reverse()
        for ev, fn in self.__events:
            ev -= fn

        self.__events = []

    def service(self, serviceName):
        if self.__isStarted:
            return self.__services[serviceName]
        else:
            return None
            return None

    def __createServices(self):
        self.__services['ClientArena'] = ClientArena()
        self.__services['HUD'] = gui.hud.HUD()
        self.__services['Input'] = InputController()
        self.__services['Camera'] = Camera()
        self.__services['ClientStatsCollector'] = ClientStatsCollector()
        if consts.IS_DEBUG_IMPORTED:
            from debug.AvatarDebug import AvatarDebugService
            self.__services['DebugHUD'] = AvatarDebugService()

    def __initServices(self):
        for s in self.__services.values():
            s.init(self)

    def __onEnterWorld(self):
        self.__linkEvents()
        for s in self.__services.values():
            s.afterLinking()

        BattleReplay.g_replay.afterLinking()

    def __onLeaveWorld(self):
        self.__unlinkEvents()
        for s in self.__services.values():
            s.doLeaveWorld()

    def __destroyServices(self):
        self.__unlinkPreWorldEvents()
        for s in self.__services.values():
            s.destroy()
            del s

        self.__services.clear()

    def getGlobalID(self):
        clientArena = getClientArena()
        if clientArena is None:
            return 0
        else:
            avatarInfo = clientArena.avatarInfos.get(self.__playerAvatar.id, None)
            if avatarInfo:
                airplaneInfo = avatarInfo.get('airplaneInfo', None)
                if airplaneInfo:
                    return airplaneInfo['globalID']
            return 0

    def isPlayerStarted(self):
        return self.__isStarted


def getGlobalID():
    global g_instance
    return g_instance.getGlobalID()


def getCamera():
    return g_instance.service('Camera')


def getInput():
    return g_instance.service('Input')


def getHUD():
    return g_instance.service('HUD')


def getDebugHUD():
    return g_instance.service('DebugHUD')


def getClientArena():
    return g_instance.service('ClientArena')


def CreateGameEnvironment():
    global g_instance
    if g_instance is None:
        g_instance = GameEnvironment()
    return


CreateGameEnvironment()