# Embedded file name: scripts/client/gui/Scaleform/Battle.py
import weakref
import BigWorld
import GUI
import Math
import SoundGroups
import VOIP
import constants
import BattleReplay
import CommandMapping
from ConnectionManager import connectionManager
from account_helpers.settings_core.SettingsCore import g_settingsCore
from gui.Scaleform.daapi.view.battle import indicators
from gui.Scaleform.daapi.view.battle.damage_info_panel import VehicleDamageInfoPanel
from gui.Scaleform.daapi.view.battle.football_over_time_bar import FootballOverTimeBar
from gui.Scaleform.daapi.view.battle.gas_attack import GasAttackPlugin
from gui.Scaleform.daapi.view.battle.repair_timer import RepairTimerPlugin
from gui.Scaleform.daapi.view.battle.resource_points import ResourcePointsPlugin
from gui.Scaleform.daapi.view.battle.respawn_view import RespawnViewPlugin
from gui.Scaleform.daapi.view.battle.PlayersPanelsSwitcher import PlayersPanelsSwitcher
from gui.Scaleform.daapi.view.battle.RadialMenu import RadialMenu
from gui.Scaleform.daapi.view.battle.flag_notification import FlagNotificationPlugin
from gui.Scaleform.daapi.view.battle.players_panel import playersPanelFactory
from gui.Scaleform.daapi.view.battle.score_panel import scorePanelFactory
from gui.Scaleform.daapi.view.battle.ConsumablesPanel import ConsumablesPanel
from gui.Scaleform.daapi.view.battle.BattleRibbonsPanel import BattleRibbonsPanel
from gui.Scaleform.daapi.view.battle.TimersBar import timersBarFactory
from gui.Scaleform.daapi.view.battle.battle_end_warning_panel import BattleEndWarningPanel, BattleEndWarningEmptyObject
from gui.Scaleform.daapi.view.battle.damage_panel import DamagePanel
from gui.Scaleform.daapi.view.battle.messages import PlayerMessages, VehicleErrorMessages, VehicleMessages
from gui.Scaleform.daapi.view.battle.stats_form import statsFormFactory
from gui.Scaleform.daapi.view.battle.teams_bases_panel import TeamBasesPanel
from gui.Scaleform.daapi.view.battle.markers import MarkersManager
from gui.Scaleform.daapi.view.common.report_bug import makeHyperLink, reportBugOpenConfirm
from gui.Scaleform.locale.MENU import MENU
import gui
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.battle_control import g_sessionProvider
from gui.battle_control.DynSquadViewListener import DynSquadViewListener
from gui.battle_control.DynSquadViewListener import RecordDynSquadViewListener, ReplayDynSquadViewListener
from gui.battle_control.battle_arena_ctrl import battleArenaControllerFactory
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE, BATTLE_CTRL, VIEW_COMPONENT_RULE
from gui.battle_control.debug_ctrl import IDebugPanel
from gui.shared import g_eventBus, events, EVENT_BUS_SCOPE
from gui.shared.utils.plugins import PluginsCollection
from messenger import MessengerEntry
from vehicle_systems.camouflages import getFootballEventCamouflageKind
from windows import BattleWindow
from SettingsInterface import SettingsInterface
from debug_utils import LOG_DEBUG, LOG_ERROR
from helpers import i18n, isPlayerAvatar
from gui import DEPTH_OF_Battle, GUI_SETTINGS, g_tankActiveCamouflage, g_guiResetters, g_repeatKeyHandlers, game_control
from gui.LobbyContext import g_lobbyContext
from gui.Scaleform import VoiceChatInterface, ColorSchemeManager
from gui.Scaleform.SoundManager import SoundManager
from gui.shared.denunciator import BattleDenunciator
from gui.shared.utils.functions import makeTooltip
from gui.Scaleform.windows import UIInterface
from gui.Scaleform.MovingText import MovingText
from gui.Scaleform.Minimap import Minimap
from gui.Scaleform.CursorDelegator import g_cursorDelegator
from gui.Scaleform.ingame_help import IngameHelp
from gui.Scaleform import SCALEFORM_SWF_PATH
from gui.battle_control.arena_info import hasFlags, hasRespawns, hasResourcePoints, isFalloutMultiTeam, hasRepairPoints, isFalloutBattle, hasGasAttack, isRandomBattle, getArenaType, battleEndWarningEnabled, isEventBattle
from gui.battle_control import avatar_getter
_SCOPE = EVENT_BUS_SCOPE.BATTLE
_BATTLE_END_WARNING_COMPONENT = 'legacy/battleEndWarning'
_COMPONENTS_TO_CTRLS = ((BATTLE_CTRL.HIT_DIRECTION, ('legacy/hitDirection',)),
 (BATTLE_CTRL.TEAM_BASES, ('legacy/teamBasesPanel',)),
 (BATTLE_CTRL.DEBUG, ('legacy/debugPanel',)),
 (BATTLE_CTRL.PERIOD, ('legacy/battleTimer',
   'legacy/prebattleTimer',
   'legacy/ppSwitcher',
   _BATTLE_END_WARNING_COMPONENT)))

class Battle(BattleWindow):
    teamBasesPanel = property(lambda self: self.__teamBasesPanel)
    timersBar = property(lambda self: self.__timersBar)
    footballOverTimeBar = property(lambda self: self.__footballOverTimeBar)
    consumablesPanel = property(lambda self: self.__consumablesPanel)
    damagePanel = property(lambda self: self.__damagePanel)
    markersManager = property(lambda self: self.__markersManager)
    vErrorsPanel = property(lambda self: self.__vErrorsPanel)
    vMsgsPanel = property(lambda self: self.__vMsgsPanel)
    pMsgsPanel = property(lambda self: self.__pMsgsPanel)
    minimap = property(lambda self: self.__minimap)
    radialMenu = property(lambda self: self.__radialMenu)
    damageInfoPanel = property(lambda self: self.__damageInfoPanel)
    fragCorrelation = property(lambda self: self.__fragCorrelation)
    statsForm = property(lambda self: self.__statsForm)
    leftPlayersPanel = property(lambda self: self.__leftPlayersPanel)
    rightPlayersPanel = property(lambda self: self.__rightPlayersPanel)
    ribbonsPanel = property(lambda self: self.__ribbonsPanel)
    ppSwitcher = property(lambda self: self.__ppSwitcher)
    VEHICLE_DESTROY_TIMER = {'ALL': 'all',
     constants.VEHICLE_MISC_STATUS.VEHICLE_DROWN_WARNING: 'drown',
     constants.VEHICLE_MISC_STATUS.VEHICLE_IS_OVERTURNED: 'overturn'}
    VEHICLE_DEATHZONE_TIMER = {'ALL': 'all',
     constants.DEATH_ZONES.STATIC: 'death_zone',
     constants.DEATH_ZONES.GAS_ATTACK: 'gas_attack'}
    VEHICLE_DEATHZONE_TIMER_SOUND = {constants.DEATH_ZONES.GAS_ATTACK: {'warning': 'fallout_gaz_sphere_warning',
                                        'critical': 'fallout_gaz_sphere_timer'}}
    __cameraVehicleID = -1
    __stateHandlers = {VEHICLE_VIEW_STATE.FIRE: '_setFireInVehicle',
     VEHICLE_VIEW_STATE.SHOW_DESTROY_TIMER: '_showVehicleTimer',
     VEHICLE_VIEW_STATE.HIDE_DESTROY_TIMER: '_hideVehicleTimer',
     VEHICLE_VIEW_STATE.SHOW_DEATHZONE_TIMER: 'showDeathzoneTimer',
     VEHICLE_VIEW_STATE.HIDE_DEATHZONE_TIMER: 'hideDeathzoneTimer',
     VEHICLE_VIEW_STATE.OBSERVED_BY_ENEMY: '_showSixthSenseIndicator'}

    def __init__(self, appNS):
        g_sessionProvider.registerViewComponents(*_COMPONENTS_TO_CTRLS)
        self.__ns = appNS
        self.__soundManager = None
        self.__arena = BigWorld.player().arena
        self.__plugins = PluginsCollection(self)
        plugins = {}
        if hasFlags():
            plugins['flagNotification'] = FlagNotificationPlugin
        if hasRepairPoints():
            plugins['repairTimer'] = RepairTimerPlugin
        if hasRespawns() and (constants.IS_DEVELOPMENT or not BattleReplay.g_replayCtrl.isPlaying):
            plugins['respawnView'] = RespawnViewPlugin
        if hasResourcePoints():
            plugins['resources'] = ResourcePointsPlugin
        if hasGasAttack():
            plugins['gasAttack'] = GasAttackPlugin
        self.__plugins.addPlugins(plugins)
        self.__denunciator = BattleDenunciator()
        self.__timerSounds = {}
        for timer, sounds in self.VEHICLE_DEATHZONE_TIMER_SOUND.iteritems():
            self.__timerSounds[timer] = {}
            for level, sound in sounds.iteritems():
                self.__timerSounds[timer][level] = SoundGroups.g_instance.getSound2D(sound)

        self.__timerSound = None
        BattleWindow.__init__(self, 'battle.swf')
        self.__isHelpWindowShown = False
        self.__cameraMode = None
        self.component.wg_inputKeyMode = 1
        self.component.position.z = DEPTH_OF_Battle
        self.movie.backgroundAlpha = 0
        self.addFsCallbacks({'battle.leave': self.onExitBattle})
        self.addExternalCallbacks({'battle.showCursor': self.cursorVisibility,
         'battle.tryLeaveRequest': self.tryLeaveRequest,
         'battle.populateFragCorrelationBar': self.populateFragCorrelationBar,
         'battle.populateTimersBar': self.populateTimersBar,
         'battle.populateFootballOverTimeBar': self.populateFootballOverTimeBar,
         'Battle.UsersRoster.Appeal': self.onDenunciationReceived,
         'Battle.selectPlayer': self.selectPlayer,
         'battle.helpDialogOpenStatus': self.helpDialogOpenStatus,
         'battle.initLobbyDialog': self._initLobbyDialog,
         'battle.reportBug': self.reportBug})
        self.__dynSquadListener = None
        BigWorld.wg_setRedefineKeysMode(False)
        self.onPostmortemVehicleChanged(BigWorld.player().playerVehicleID)
        return

    @property
    def appNS(self):
        return self.__ns

    @property
    def soundManager(self):
        return self.__soundManager

    def attachCursor(self, flags = 0):
        return g_cursorDelegator.activateCursor()

    def detachCursor(self):
        return g_cursorDelegator.detachCursor()

    def syncCursor(self, flags = 0):
        pass

    def getRoot(self):
        return self.__battle_flashObject

    def getCameraVehicleID(self):
        return self.__cameraVehicleID

    def populateTimersBar(self, _):
        if self.__timersBar is not None:
            self.__timersBar.populate()
        return

    def populateFootballOverTimeBar(self, _):
        if self.__footballOverTimeBar is not None:
            self.__footballOverTimeBar.populate()
        return

    def populateFragCorrelationBar(self, _):
        if self.__fragCorrelation is not None:
            self.__fragCorrelation.populate()
        return

    def showAll(self, event):
        self.call('battle.showAll', [event.ctx['visible']])
        self.damagePanel.showAll(self.__cameraMode != 'video')

    def showCursor(self, isShow):
        self.cursorVisibility(-1, isShow)

    def selectPlayer(self, _, vehId):
        player = BigWorld.player()
        if isPlayerAvatar():
            player.selectPlayer(int(vehId))

    def onDenunciationReceived(self, _, uid, userName, topic):
        self.__denunciator.makeAppeal(uid, userName, topic)
        self.__arenaCtrl.invalidateGUI()

    def onPostmortemVehicleChanged(self, vehicleID):
        if self.__cameraVehicleID == vehicleID:
            return
        self.__cameraVehicleID = vehicleID
        self.__arenaCtrl.invalidateGUI(not g_sessionProvider.getCtx().isPlayerObserver())
        self._hideVehicleTimer('ALL')
        self.hideDeathzoneTimer('ALL')
        self.__vErrorsPanel.clear()
        self.__vMsgsPanel.clear()

    def onCameraChanged(self, cameraMode, curVehID = None):
        LOG_DEBUG('onCameraChanged', cameraMode, curVehID)
        if self.__cameraMode == 'mapcase':
            self.setAimingMode(False)
        elif cameraMode == 'mapcase':
            self.setAimingMode(True)
        self.__cameraMode = cameraMode

        def setVisible(cname):
            m = self.getMember(cname)
            if m is not None:
                m.visible = cameraMode != 'video'
            return

        if self.__isGuiShown():
            self.damagePanel.showAll(cameraMode != 'video')
            setVisible('vehicleErrorsPanel')
        if cameraMode == 'video':
            self.__cameraVehicleID = -1
            self.__vErrorsPanel.clear()
            self.__vMsgsPanel.clear()
            self._hideVehicleTimer('ALL')
            self.hideDeathzoneTimer('ALL')

    def __isGuiShown(self):
        m = self.getMember('_root')
        if m is not None and callable(m.isGuiVisible):
            return m.isGuiVisible()
        else:
            return False

    def _showVehicleTimer(self, value):
        code, time, warnLvl = value
        LOG_DEBUG('show vehicles destroy timer', code, time, warnLvl)
        self.call('destroyTimer.show', [self.VEHICLE_DESTROY_TIMER[code], time, warnLvl])

    def _hideVehicleTimer(self, code = None):
        LOG_DEBUG('hide vehicles destroy timer', code)
        if code is None:
            code = 'ALL'
        self.call('destroyTimer.hide', [self.VEHICLE_DESTROY_TIMER[code]])
        return

    def showDeathzoneTimer(self, value):
        zoneID, time, warnLvl = value
        if self.__timerSound is not None:
            self.__timerSound.stop()
            self.__timerSound = None
        sound = self.__timerSounds.get(zoneID, {}).get(warnLvl)
        if sound is not None:
            self.__timerSound = sound
            self.__timerSound.play()
        LOG_DEBUG('show vehicles deathzone timer', zoneID, time, warnLvl)
        self.call('destroyTimer.show', [self.VEHICLE_DEATHZONE_TIMER[zoneID], time, warnLvl])
        return

    def hideDeathzoneTimer(self, zoneID = None):
        if self.__timerSound is not None:
            self.__timerSound.stop()
            self.__timerSound = None
        if zoneID is None:
            zoneID = 'ALL'
        LOG_DEBUG('hide vehicles deathzone timer', zoneID)
        self.call('destroyTimer.hide', [self.VEHICLE_DEATHZONE_TIMER[zoneID]])
        return

    def _showSixthSenseIndicator(self, isShow):
        self.call('sixthSenseIndicator.show', [isShow])

    def setVisible(self, bool):
        LOG_DEBUG('[Battle] visible', bool)
        self.component.visible = bool

    def afterCreate(self):
        event = events.AppLifeCycleEvent
        g_eventBus.handleEvent(event(self.__ns, event.INITIALIZING))
        player = BigWorld.player()
        voice = VoiceChatInterface.g_instance
        LOG_DEBUG('[Battle] afterCreate')
        setattr(self.movie, '_global.wg_isShowLanguageBar', GUI_SETTINGS.isShowLanguageBar)
        setattr(self.movie, '_global.wg_isShowServerStats', constants.IS_SHOW_SERVER_STATS)
        setattr(self.movie, '_global.wg_isShowVoiceChat', GUI_SETTINGS.voiceChat)
        setattr(self.movie, '_global.wg_voiceChatProvider', voice.voiceChatProvider)
        setattr(self.movie, '_global.wg_isChina', constants.IS_CHINA)
        setattr(self.movie, '_global.wg_isKorea', constants.IS_KOREA)
        setattr(self.movie, '_global.wg_isReplayPlaying', BattleReplay.g_replayCtrl.isPlaying)
        BattleWindow.afterCreate(self)
        addListener = g_eventBus.addListener
        addListener(events.GameEvent.HELP, self.toggleHelpWindow, scope=_SCOPE)
        addListener(events.GameEvent.GUI_VISIBILITY, self.showAll, scope=_SCOPE)
        player.inputHandler.onPostmortemVehicleChanged += self.onPostmortemVehicleChanged
        player.inputHandler.onCameraChanged += self.onCameraChanged
        g_settingsCore.onSettingsChanged += self.__accs_onSettingsChanged
        g_settingsCore.interfaceScale.onScaleChanged += self.__onRecreateDevice
        isMutlipleTeams = isFalloutMultiTeam()
        isFallout = isFalloutBattle()
        isEvent = isEventBattle()
        self.proxy = weakref.proxy(self)
        self.__battle_flashObject = self.proxy.getMember('_level0')
        if self.__battle_flashObject:
            self.__battle_flashObject.resync()
        voice.populateUI(self.proxy)
        voice.onPlayerSpeaking += self.setPlayerSpeaking
        voice.onVoiceChatInitFailed += self.onVoiceChatInitFailed
        self.colorManager = ColorSchemeManager._ColorSchemeManager()
        self.colorManager.populateUI(self.proxy)
        self.movingText = MovingText()
        self.movingText.populateUI(self.proxy)
        self.__settingsInterface = SettingsInterface()
        self.__settingsInterface.populateUI(self.proxy)
        self.__soundManager = SoundManager()
        self.__soundManager.populateUI(self.proxy)
        self.__debugPanel = DebugPanel()
        self.__timersBar = timersBarFactory(self.proxy, isEvent)
        if battleEndWarningEnabled():
            self.__battleEndWarningPanel = BattleEndWarningPanel(self.proxy, getArenaType())
        else:
            self.__battleEndWarningPanel = BattleEndWarningEmptyObject(self.proxy, getArenaType())
        self.__teamBasesPanel = TeamBasesPanel(self.proxy)
        self.__consumablesPanel = ConsumablesPanel(self.proxy)
        self.__damagePanel = DamagePanel(self.proxy)
        self.__markersManager = MarkersManager(self.proxy)
        self.__ingameHelp = IngameHelp(self.proxy)
        self.__minimap = Minimap(self.proxy)
        self.__radialMenu = RadialMenu(self.proxy)
        self.__ribbonsPanel = BattleRibbonsPanel(self.proxy)
        self.__ppSwitcher = PlayersPanelsSwitcher(self.proxy)
        self.__footballOverTimeBar = None
        if isEvent:
            self.__footballOverTimeBar = FootballOverTimeBar(self.__arena, self.proxy)
        isColorBlind = g_settingsCore.getSetting('isColorBlind')
        self.__leftPlayersPanel = playersPanelFactory(self.proxy, True, isColorBlind, isFallout, isMutlipleTeams)
        self.__rightPlayersPanel = playersPanelFactory(self.proxy, False, isColorBlind, isFallout, isMutlipleTeams)
        self.__damageInfoPanel = VehicleDamageInfoPanel(self.proxy)
        self.__damageInfoPanel.start()
        self.__fragCorrelation = scorePanelFactory(self.proxy, isFallout, isMutlipleTeams, isEvent)
        self.__statsForm = statsFormFactory(self.proxy, isFallout, isMutlipleTeams, isEvent)
        self.__plugins.init()
        self.isVehicleCountersVisible = g_settingsCore.getSetting('showVehiclesCounter')
        self.__fragCorrelation.showVehiclesCounter(self.isVehicleCountersVisible)
        self.__vErrorsPanel = VehicleErrorMessages(self.proxy)
        self.__vMsgsPanel = VehicleMessages(self.proxy)
        self.__pMsgsPanel = PlayerMessages(self.proxy)
        self.__plugins.start()
        self.__consumablesPanel.start()
        self.__damagePanel.start()
        self.__ingameHelp.start()
        self.__vErrorsPanel.start()
        self.__vMsgsPanel.start()
        self.__pMsgsPanel.start()
        self.__markersManager.start()
        self.__markersManager.setMarkerDuration(GUI_SETTINGS.markerHitSplashDuration)
        markers = {'enemy': g_settingsCore.getSetting('enemy'),
         'dead': g_settingsCore.getSetting('dead'),
         'ally': g_settingsCore.getSetting('ally')}
        self.__updateEventMarkerSettings(markers)
        self.__markersManager.setMarkerSettings(markers)
        MessengerEntry.g_instance.gui.invoke('populateUI', self.proxy)
        g_guiResetters.add(self.__onRecreateDevice)
        g_repeatKeyHandlers.add(self.component.handleKeyEvent)
        self.__onRecreateDevice()
        self.__statsForm.populate()
        self.__leftPlayersPanel.populateUI(self.proxy)
        self.__rightPlayersPanel.populateUI(self.proxy)
        self.__debugPanel.populateUI(self.proxy)
        if BattleReplay.g_replayCtrl.isPlaying:
            BattleReplay.g_replayCtrl.onBattleSwfLoaded()
        self.__populateData()
        self.__minimap.start()
        self.__radialMenu.setSettings(self.__settingsInterface)
        self.__radialMenu.populateUI(self.proxy)
        self.__ribbonsPanel.start()
        add = g_sessionProvider.addViewComponent
        add('legacy/hitDirection', indicators.createDamageIndicator(), rule=VIEW_COMPONENT_RULE.NONE)
        add('legacy/teamBasesPanel', self.__teamBasesPanel)
        add('legacy/debugPanel', self.__debugPanel)
        add('legacy/battleTimer', self.__timersBar)
        add('legacy/prebattleTimer', self.__timersBar)
        add('legacy/ppSwitcher', self.__ppSwitcher)
        add(_BATTLE_END_WARNING_COMPONENT, self.__battleEndWarningPanel)
        self.__arenaCtrl = battleArenaControllerFactory(self, isFallout, isMutlipleTeams, isEvent)
        g_sessionProvider.addArenaCtrl(self.__arenaCtrl)
        self.updateFlagsColor()
        self.movie.setFocussed(SCALEFORM_SWF_PATH)
        self.call('battle.initDynamicSquad', self.__getDynamicSquadsInitParams(enableButton=not BattleReplay.g_replayCtrl.isPlaying))
        self.call('sixthSenseIndicator.setDuration', [GUI_SETTINGS.sixthSenseDuration])
        if isEvent:
            storingCamoKind = getFootballEventCamouflageKind(g_sessionProvider.getArenaDP().getNumberOfTeam())
        else:
            storingCamoKind = self.__arena.arenaType.vehicleCamouflageKind
        g_tankActiveCamouflage[player.vehicleTypeDescriptor.type.compactDescr] = storingCamoKind
        keyCode = CommandMapping.g_instance.get('CMD_VOICECHAT_MUTE')
        if not BigWorld.isKeyDown(keyCode):
            VOIP.getVOIPManager().setMicMute(True)
        ctrl = g_sessionProvider.getVehicleStateCtrl()
        ctrl.onVehicleStateUpdated += self.__onVehicleStateUpdated
        ctrl.onPostMortemSwitched += self.__onPostMortemSwitched
        if BattleReplay.g_replayCtrl.isPlaying:
            self.__dynSquadListener = ReplayDynSquadViewListener(self.proxy)
        elif BattleReplay.g_replayCtrl.isRecording:
            self.__dynSquadListener = RecordDynSquadViewListener(self.proxy)
        else:
            self.__dynSquadListener = DynSquadViewListener(self.proxy)
        g_eventBus.handleEvent(event(self.__ns, event.INITIALIZED))
        return

    def beforeDelete(self):
        LOG_DEBUG('[Battle] beforeDelete')
        removeListener = g_eventBus.removeListener
        removeListener(events.GameEvent.HELP, self.toggleHelpWindow, scope=_SCOPE)
        removeListener(events.GameEvent.GUI_VISIBILITY, self.showAll, scope=_SCOPE)
        ctrl = g_sessionProvider.getVehicleStateCtrl()
        if ctrl is not None:
            ctrl.onVehicleStateUpdated -= self.__onVehicleStateUpdated
            ctrl.onPostMortemSwitched -= self.__onPostMortemSwitched
        player = BigWorld.player()
        if player and player.inputHandler:
            player.inputHandler.onPostmortemVehicleChanged -= self.onPostmortemVehicleChanged
            player.inputHandler.onCameraChanged -= self.onCameraChanged
        if self.colorManager:
            self.colorManager.dispossessUI()
        voice = VoiceChatInterface.g_instance
        if voice:
            voice.dispossessUI(self.proxy)
            voice.onPlayerSpeaking -= self.setPlayerSpeaking
            voice.onVoiceChatInitFailed -= self.onVoiceChatInitFailed
        if self.__plugins is not None:
            self.__plugins.stop()
            self.__plugins.fini()
            self.__plugins = None
        if self.movingText is not None:
            self.movingText.dispossessUI()
            self.movingText = None
        if self.__timerSound is not None:
            self.__timerSound.stop()
            self.__timerSound = None
        if self.__soundManager is not None:
            self.__soundManager.dispossessUI()
            self.__soundManager = None
        if self.colorManager is not None:
            self.colorManager.dispossessUI()
            self.colorManager = None
        if self.component:
            g_repeatKeyHandlers.discard(self.component.handleKeyEvent)
        g_settingsCore.onSettingsChanged -= self.__accs_onSettingsChanged
        g_settingsCore.interfaceScale.onScaleChanged -= self.__onRecreateDevice
        self.__timersBar.destroy()
        if self.__footballOverTimeBar:
            self.__footballOverTimeBar.destroy()
        self.__battleEndWarningPanel.destroy()
        self.__teamBasesPanel.destroy()
        self.__consumablesPanel.destroy()
        self.__damagePanel.destroy()
        self.__markersManager.destroy()
        self.__ingameHelp.destroy()
        self.__vErrorsPanel.destroy()
        self.__vMsgsPanel.destroy()
        self.__pMsgsPanel.destroy()
        self.__radialMenu.destroy()
        self.__minimap.destroy()
        self.__ribbonsPanel.destroy()
        self.__fragCorrelation.destroy()
        self.__statsForm.destroy()
        self.__damageInfoPanel.destroy()
        remove = g_sessionProvider.removeViewComponent
        remove('legacy/hitDirection')
        remove('legacy/teamBasesPanel')
        remove('legacy/debugPanel')
        remove('legacy/battleTimer')
        remove('legacy/prebattleTimer')
        remove('legacy/ppSwitcher')
        if self.__arenaCtrl is not None:
            g_sessionProvider.removeArenaCtrl(self.__arenaCtrl)
            self.__arenaCtrl.clear()
            self.__arenaCtrl = None
        self.__ppSwitcher.destroy()
        self.__debugPanel.dispossessUI()
        self.__leftPlayersPanel.dispossessUI()
        self.__rightPlayersPanel.dispossessUI()
        MessengerEntry.g_instance.gui.invoke('dispossessUI')
        self.__arena = None
        self.__denunciator = None
        g_guiResetters.discard(self.__onRecreateDevice)
        self.__settingsInterface.dispossessUI()
        self.__settingsInterface = None
        if self.__dynSquadListener:
            self.__dynSquadListener.destroy()
            self.__dynSquadListener = None
        BattleWindow.beforeDelete(self)
        event = events.AppLifeCycleEvent
        g_eventBus.handleEvent(event(self.__ns, event.DESTROYED))
        return

    def __onVehicleStateUpdated(self, state, value):
        if state not in self.__stateHandlers:
            return
        else:
            handler = getattr(self, self.__stateHandlers[state], None)
            if handler and callable(handler):
                if value is not None:
                    handler(value)
                else:
                    handler()
            return

    def _setFireInVehicle(self, bool):
        self.call('destroyTimer.onFireInVehicle', [bool])

    def onVoiceChatInitFailed(self):
        if GUI_SETTINGS.voiceChat:
            self.call('VoiceChat.initFailed', [])

    def clearCommands(self):
        pass

    def bindCommands(self):
        self.__consumablesPanel.bindCommands()
        self.__ingameHelp.buildCmdMapping()

    def updateFlagsColor(self):
        isColorBlind = g_settingsCore.getSetting('isColorBlind')
        colorGreen = self.colorManager.getSubScheme('flag_team_green', isColorBlind=isColorBlind)['rgba']
        colorRed = self.colorManager.getSubScheme('flag_team_red', isColorBlind=isColorBlind)['rgba']
        arenaDP = g_sessionProvider.getArenaDP()
        teamsOnArena = arenaDP.getTeamsOnArena()
        for teamIdx in teamsOnArena:
            color = colorGreen if arenaDP.isAllyTeam(teamIdx) else colorRed
            BigWorld.wg_setFlagColor(teamIdx, color / 255)

        for teamIdx in [0] + teamsOnArena:
            BigWorld.wg_setFlagEmblem(teamIdx, 'system/maps/wg_emblem.dds', Math.Vector4(0.0, 0.1, 0.5, 0.9))

    def setPlayerSpeaking(self, accountDBID, flag):
        self.__callEx('setPlayerSpeaking', [accountDBID, flag])
        vID = g_sessionProvider.getCtx().getVehIDByAccDBID(accountDBID)
        if vID > 0:
            self.__markersManager.showDynamic(vID, flag)

    def isPlayerSpeaking(self, accountDBID):
        return VoiceChatInterface.g_instance.isPlayerSpeaking(accountDBID)

    def __onPostMortemSwitched(self):
        if self.radialMenu is not None:
            self.radialMenu.forcedHide()
        if not g_sessionProvider.getCtx().isPlayerObserver():
            self.__callEx('showPostmortemTips', [1.0, 5.0, 1.0])
        return

    def cursorVisibility(self, _, visible, x = None, y = None, customCall = False, enableAiming = True):
        if visible:
            g_cursorDelegator.syncMousePosition(self, x, y, customCall)
        else:
            g_cursorDelegator.restoreMousePosition()
        avatar_getter.setForcedGuiControlMode(visible, stopVehicle=False, enableAiming=enableAiming)

    def tryLeaveRequest(self, _):
        resStr = 'quitBattle'
        icon = RES_ICONS.MAPS_ICONS_BATTLE_DESERTERLEAVEBATTLE
        if isEventBattle():
            resStr = 'quitBattleFootball'
            icon = RES_ICONS.MAPS_ICONS_BATTLE_FOOTBALLLEAVEBATTLE
        replayCtrl = BattleReplay.g_replayCtrl
        canRespawn = False
        player = BigWorld.player()
        if hasRespawns():
            isVehicleAlive = not g_sessionProvider.getArenaDP().getVehicleInteractiveStats().stopRespawn
            canRespawn = isVehicleAlive
        else:
            isVehicleAlive = getattr(player, 'isVehicleAlive', False)
        isVehicleOverturned = getattr(player, 'isVehicleOverturned', False)
        isNotTraining = self.__arena.guiType != constants.ARENA_GUI_TYPE.TRAINING
        if not replayCtrl.isPlaying:
            if constants.IS_KOREA and gui.GUI_SETTINGS.igrEnabled and self.__arena is not None and isNotTraining:
                vehicleID = getattr(player, 'playerVehicleID', -1)
                if vehicleID in self.__arena.vehicles:
                    vehicle = self.__arena.vehicles[vehicleID]
                    if isVehicleAlive and vehicle.get('igrType') != constants.IGR_TYPE.NONE:
                        resStr = 'quitBattleIGR'
                else:
                    LOG_ERROR("Player's vehicle not found", vehicleID)
            if canRespawn:
                isDeserter = isVehicleAlive and isNotTraining
            else:
                isDeserter = isVehicleAlive and isNotTraining and not isVehicleOverturned
            if isDeserter:
                resStr += '/deserter'
        else:
            isDeserter = False
        self.__callEx('tryLeaveResponse', [resStr, isDeserter, icon])
        return

    def onExitBattle(self, _):
        arena = getattr(BigWorld.player(), 'arena', None)
        LOG_DEBUG('onExitBattle', arena)
        if arena:
            BigWorld.player().leaveArena()
        return

    def toggleHelpWindow(self, _):
        self.__callEx('showHideHelp', [not self.__isHelpWindowShown])

    def setAimingMode(self, isAiming):
        self.__callEx('setAimingMode', [isAiming])

    def helpDialogOpenStatus(self, cid, isOpened):
        self.__isHelpWindowShown = isOpened

    def _initLobbyDialog(self, cid):
        if connectionManager.serverUserName:
            tooltipBody = i18n.makeString('#tooltips:header/info/players_online_full/body')
            tooltipFullData = makeTooltip('#tooltips:header/info/players_online_full/header', tooltipBody % {'servername': connectionManager.serverUserName})
            self.__callEx('setServerStatsInfo', [tooltipFullData])
            self.__callEx('setServerName', [connectionManager.serverUserName])
            if constants.IS_SHOW_SERVER_STATS:
                stats = game_control.g_instance.serverStats.getStats()
                if 'clusterCCU' in stats and 'regionCCU' in stats:
                    self.__callEx('setServerStats', [stats['clusterCCU'], stats['regionCCU']])
                else:
                    self.__callEx('setServerStats', [None, None])
        else:
            self.__callEx('setServerName', ['-'])
        links = GUI_SETTINGS.reportBugLinks
        if len(links):
            reportBugButton = makeHyperLink('ingameMenu', MENU.INGAME_MENU_LINKS_REPORT_BUG)
            self.__callEx('setReportBugLink', [reportBugButton])
        return

    def reportBug(self, _):
        reportBugOpenConfirm(g_sessionProvider.getArenaDP().getVehicleInfo().player.accountDBID)

    def __getDynamicSquadsInitParams(self, enableAlly = True, enableEnemy = False, enableButton = True):
        isAvailableBattleType = isRandomBattle() or isEventBattle()
        return [isAvailableBattleType and enableAlly, enableEnemy, isAvailableBattleType and enableButton]

    def __populateData(self):
        ctx = g_sessionProvider.getCtx()
        data = [ctx.getArenaTypeName(),
         ctx.getArenaFrameLabel(isLegacy=True),
         ctx.getArenaDescriptionString(),
         ctx.getTeamName(enemy=False),
         ctx.getTeamName(enemy=True),
         ctx.getArenaWinString(),
         ctx.getGuiEventType()]
        settings = g_lobbyContext.getServerSettings()
        quest = [None] * 3
        if settings is not None and settings.isPotapovQuestEnabled():
            info = ctx.getQuestInfo()
            if info is not None:
                quest[0] = info.name
                if info.condition:
                    quest[1] = info.condition
                if info.condition:
                    quest[2] = info.additional
        data.extend(quest)
        data.append(ctx.getArenaSmallIcon())
        self.__callEx('arenaData', data)
        return

    def __onRecreateDevice(self, scale = None):
        params = list(GUI.screenResolution())
        params.append(g_settingsCore.interfaceScale.get())
        self.call('Stage.Update', params)
        self.__markersManager.updateMarkersScale()

    def invalidateGUI(self):
        arenaCtrl = getattr(self, '_Battle__arenaCtrl', None)
        if arenaCtrl is not None:
            arenaCtrl.invalidateGUI()
        return

    def __callEx(self, funcName, args = None):
        self.call('battle.' + funcName, args)

    def __accs_onSettingsChanged(self, diff):
        self.colorManager.update()
        if 'isColorBlind' in diff:
            isColorBlind = diff['isColorBlind']
            self.__leftPlayersPanel.defineColorFlags(isColorBlind=isColorBlind)
            self.__rightPlayersPanel.defineColorFlags(isColorBlind=isColorBlind)
            self.updateFlagsColor()
            self.__markersManager.updateMarkers()
            self.__minimap.updateEntries()
        if 'enemy' in diff or 'dead' in diff or 'ally' in diff:
            markers = {'enemy': g_settingsCore.getSetting('enemy'),
             'dead': g_settingsCore.getSetting('dead'),
             'ally': g_settingsCore.getSetting('ally')}
            self.__updateEventMarkerSettings(markers)
            self.__markersManager.setMarkerSettings(markers)
            self.__markersManager.updateMarkerSettings()
        if 'showVehiclesCounter' in diff:
            self.isVehicleCountersVisible = diff['showVehiclesCounter']
            self.__fragCorrelation.showVehiclesCounter(self.isVehicleCountersVisible)
        if 'interfaceScale' in diff:
            self.__onRecreateDevice()
        self.__arenaCtrl.invalidateGUI()
        self.__arenaCtrl.invalidateArenaInfo()

    def __updateEventMarkerSettings(self, markers):
        """
        Football Event functionality. Method have to be removed after event!!!
        :param markers:
        """
        if isEventBattle():

            def __forbidSettings(settings):
                for key in settings.iterkeys():
                    if key == 'markerBaseHp' or key == 'markerAltHp':
                        settings[key] = 3
                    elif key != 'markerBasePlayerName' and key != 'markerAltPlayerName':
                        typeOfSetting = type(settings[key])
                        if typeOfSetting is bool:
                            settings[key] = False
                        elif typeOfSetting is int or typeOfSetting is long:
                            settings[key] = 0

            __forbidSettings(markers['enemy'])
            __forbidSettings(markers['ally'])
            __forbidSettings(markers['dead'])

    def setTeamValuesData(self, data):
        if self.__battle_flashObject is not None:
            self.__battle_flashObject.setTeamValues(data)
        return

    def setFootballGoalsData(self, data):
        if self.__battle_flashObject is not None:
            self.__battle_flashObject.setFootballGoalsData(data)
        return

    def setFootballBallPossessionData(self, data):
        if self.__battle_flashObject is not None:
            self.__battle_flashObject.setFootballBallPossessionData(data)
        return

    def setMultiteamValues(self, data):
        if self.__battle_flashObject is not None:
            self.__battle_flashObject.setMultiteamValues(data)
        return

    def getPlayerNameLength(self, isEnemy):
        panel = self.rightPlayersPanel if isEnemy else self.leftPlayersPanel
        return panel.getPlayerNameLength()

    def getVehicleNameLength(self, isEnemy):
        panel = self.rightPlayersPanel if isEnemy else self.leftPlayersPanel
        return panel.getVehicleNameLength()

    def getTeamBasesPanel(self):
        return self.__teamBasesPanel

    def getBattleTimer(self):
        return self.__timersBar

    def getFootballOverTimeBar(self):
        return self.__footballOverTimeBar

    def getPreBattleTimer(self):
        return self.__timersBar

    def getConsumablesPanel(self):
        return self.__consumablesPanel

    def getDamagePanel(self):
        return self.__damagePanel

    def getMarkersManager(self):
        return self.__markersManager

    def getVErrorsPanel(self):
        return self.__vErrorsPanel

    def getVMsgsPanel(self):
        return self.__vMsgsPanel

    def getPMsgsPanel(self):
        return self.__pMsgsPanel

    def getMinimap(self):
        return self.__minimap

    def getRadialMenu(self):
        return self.__radialMenu

    def getDamageInfoPanel(self):
        return self.__damageInfoPanel

    def getFragCorrelation(self):
        return self.__fragCorrelation

    def getStatsForm(self):
        return self.__statsForm

    def getLeftPlayersPanel(self):
        return self.__leftPlayersPanel

    def getRightPlayersPanel(self):
        return self.__rightPlayersPanel

    def getRibbonsPanel(self):
        return self.__ribbonsPanel

    def getPlayersPanelsSwitcher(self):
        return self.__ppSwitcher

    def getDebugPanel(self):
        return self.__debugPanel


class DebugPanel(UIInterface, IDebugPanel):

    def __init__(self):
        super(DebugPanel, self).__init__()
        self.flashObject = None
        return

    def populateUI(self, proxy):
        super(DebugPanel, self).populateUI(proxy)
        self.flashObject = self.uiHolder.getMember('_level0.debugPanel')
        self.flashObject.script = self

    def updateDebugInfo(self, ping, fps, lag, fpsReplay = -1):
        if fpsReplay != 0 and fpsReplay != -1:
            fps = '{0}({1})'.format(fpsReplay, fps)
        else:
            fps = str(fps)
        ping = str(ping)
        self.flashObject.as_updateDebugInfo(fps, ping, lag)

    def dispossessUI(self):
        self.flashObject.script = None
        self.flashObject = None
        super(DebugPanel, self).dispossessUI()
        return