# Embedded file name: scripts/client/gui/Scaleform/UI.py
import BattleReplay
import BigWorld
import Settings
from Event import Event
from debug_utils import LOG_DEBUG, LOG_WARNING, LOG_ERROR, LOG_TRACE
from Helpers.i18n import localizeHUD, localizeAirplane, localizeTutorial, localizeComponents, localizeLobby
from consts import MESSAGE_TYPE, FIRST_SWITCH_TO_THE_NEXT_VEHICLE_DELAY, SUPERIORITY2_BASE_HEALTH, SUPERIORITY2_LIVES_COUNT
from consts import MESSAGE_MAX_SIZE, METERS_PER_SEC_TO_KMH_FACTOR, UPDATABLE_TYPE, GAME_RESULT, WORLD_SCALING, ARENA_TYPE
import Math
import db.DBLogic
from EntityHelpers import *
import gui.hud
from gui.Scaleform.windows import GUIWindow
from gui.Scaleform.windows import CustomObject
from gui import Cursor
from gui.WebPageHolder import WebPageHolder
import InputMapping
from gui.Scaleform.utils.MeasurementSystem import MeasurementSystem
from gui.HUDconsts import PERCENT_BEFORE_DOMINATION_WIN, TIME_AFTER_ARENA_STARTED_FOR_HIDE_BEGIN_MESSAGES, HUD_MINIMAP_ENTITY_TYPE_TUTORIAL_MARKER_POINTER, HUD_MINIMAP_ENTITY_GATE_MARKER_TUTORIAL, TIME_AFTER_ARENA_STARTED_FOR_HIDE_LOADING_SCREEN
from UIHelper import BattleInfo, SQUAD_TYPES, getKeyLocalization, getCalculatedBalanceCharacteristic, getPlayerNameWithClan
import GameEnvironment
from clientConsts import FLASH_HUD_STATES, VOIP_ICON_TYPES, VOIP_ICON_TYPES_ARENA, WEAPON_TYPES, MESSAGE_TYPE_UI_COLOR_GREEN, CLASTERS, TIME_FOR_HIDE_INTRO_HINT_BEFORE_START_BATTLE, PLANE_TYPE_ICO_PATH, getHudPlaneIcon, SNOW_BALLS_ICON_PATH, SNOW_BALLS_ICON_EMPTY_PATH, LOCAL_HOLIDAYS_MATRIX, QUEST_CONDITION_ERROR, COMPLEX_QUEST_MIN_PLANE_LEVEL, HUD_AMMO_BELTS_TYPE_ICO
from Help import Help
from _preparedBattleData_db import preparedBattleData
import messenger
import VOIP
import GUI
from HelperFunctions import wowpRound
from UIHelper import onDenunciation
import GlobalEvents
from Spectator import SPECTATOR_MODE_STATES
from audio import GameSound

class HudStateType():
    INITIALIZED = 0
    WAIT_PLAYERS = 1
    WAIT_BATTLE = 2
    BATTLE_STARTED = 3


class _HelpKeyVO():

    def __init__(self, id, label):
        self.id = id
        self.label = label


class TextLabel():

    def __init__(self, labelName = '', text = ''):
        self.id = labelName
        self.text = text


class _SpectatorHintParams():

    def __init__(self, btn = '', btn_description = ''):
        self.btn = btn
        self.btn_description = btn_description


class TutorialHintParams():

    def __init__(self, message = '', fadeoutTime = None, pictures = None):
        self.message = message
        self.names = pictures
        self.time = fadeoutTime
        self.isAction = False
        self.nameAction1 = ''
        self.nameAction2 = ''
        self.action1ButtonID = -1
        self.action2ButtonID = -1
        self.message1 = None
        self.buttons = None
        return


class TutorialHeaderParams():

    def __init__(self, title = '', message = '', message2 = '', buttons = None, image = ''):
        self.title = title
        self.message = message
        self.message2 = message2
        self.buttons = buttons
        self.image = image


class TutorialCaptionParams():

    def __init__(self):
        self.title = ''
        self.message = ''
        self.isAction1 = False
        self.nameAction1 = ''
        self.action1ButtonID = -1
        self.isAction2 = False
        self.nameAction2 = ''
        self.action2ButtonID = -1
        self.isAction3 = False
        self.nameAction3 = ''
        self.action3ButtonID = -1
        self.isBonus = False
        self.nameReward = ''
        self.countCredits = None
        self.nameCredits = ''
        self.countExperience = None
        self.nameExperience = ''
        self.countGolds = None
        self.nameGolds = ''
        return


class TutorialResultParams():

    def __init__(self):
        self.lessonIndex = -1
        self.header = ''
        self.type = 0
        self.title = ''
        self.description1 = ''
        self.description2 = ''
        self.time = 0
        self.isBonus = False
        self.nameReward = ''
        self.countCredits = None
        self.nameCredits = ''
        self.countExperience = None
        self.nameExperience = ''
        self.countGolds = None
        self.nameGolds = ''
        self.textCompleted = ''
        self.isLastLesson = False
        return


class ElementsVisibleParams():

    def __init__(self):
        self.weapon = True


class PlayerChatStatus():

    def __init__(self, playerId = 0, status = 0):
        self.id = playerId
        self.status = status


class UI(GUIWindow):
    CONVERT_CHAT_MSG_TYPE_FROM_FLASH = {0: MESSAGE_TYPE.BATTLE_ALL,
     1: MESSAGE_TYPE.BATTLE_ALLY,
     2: MESSAGE_TYPE.BATTLE_SQUAD}
    CONVERT_CHAT_MSG_TYPE_TO_FLASH = {MESSAGE_TYPE.BATTLE_ALL: 0,
     MESSAGE_TYPE.BATTLE_ALLY: 1,
     MESSAGE_TYPE.BATTLE_ALL_FROM_OPPONENT: 2,
     MESSAGE_TYPE.BATTLE_SQUAD: 3,
     MESSAGE_TYPE.BATTLE_NEUTRAL: 4,
     MESSAGE_TYPE.BATTLE_NEUTRAL_UNIVERSAL: 5}
    CONVERT_WEAPON_TYPES_TO_FLASH = {UPDATABLE_TYPE.BOMB: WEAPON_TYPES.BOMB,
     UPDATABLE_TYPE.ROCKET: WEAPON_TYPES.ROCKET}
    GAME_RESULT_LOC_IDS = {GAME_RESULT.DRAW_TIME_IS_RUNNING_OUT: ['HUD_DRAW_TIME', 'HUD_DRAW_TIME', 'HUD_DRAW_TIME'],
     GAME_RESULT.SUPERIORITY_SUCCESS: ['HUD_WIN_SUPERIORITY_STR', 'HUD_LOOSE_SUPERIORITY_STR', ''],
     GAME_RESULT.ELIMINATION: ['HUD_ENEMIES_ELIMINATION_STR', 'HUD_OWN_ELIMINATION_STR', ''],
     GAME_RESULT.DRAW_ELIMINATION: ['HUD_DRAW_PLAYERS', 'HUD_DRAW_PLAYERS', 'HUD_DRAW_PLAYERS'],
     GAME_RESULT.DRAW_ELIMINATION_NO_PLAYERS: ['HUD_PVE_NO_PLAYERS', 'HUD_PVE_NO_PLAYERS', 'HUD_PVE_NO_PLAYERS'],
     GAME_RESULT.DRAW_SUPERIORITY: ['HUD_DRAW_SUPERIORITY_STR', 'HUD_DRAW_SUPERIORITY_STR', 'HUD_DRAW_SUPERIORITY_STR']}
    GAME_RESULT_SIDE_COLOR = {GAME_RESULT.DRAW_TIME_IS_RUNNING_OUT: ['completionFightSuperiorityEnemy', 'completionFightSuperiorityEnemy', 'completionFightSuperiorityEnemy'],
     GAME_RESULT.SUPERIORITY_SUCCESS: ['completionFightSuperiority', 'completionFightSuperiorityEnemy', 'completionFightSuperiority'],
     GAME_RESULT.ELIMINATION: ['completionFightSuperiority', 'completionFightSuperiorityEnemy', 'completionFightSuperiority'],
     GAME_RESULT.DRAW_ELIMINATION: ['completionFightSuperiorityEnemy', 'completionFightSuperiorityEnemy', 'completionFightSuperiorityEnemy'],
     GAME_RESULT.DRAW_ELIMINATION_NO_PLAYERS: ['completionFightSuperiorityEnemy', 'completionFightSuperiorityEnemy', 'completionFightSuperiorityEnemy'],
     GAME_RESULT.DRAW_SUPERIORITY: ['completionFightSuperiorityEnemy', 'completionFightSuperiorityEnemy', 'completionFightSuperiorityEnemy']}
    GAME_RESULT = ['HUD_WINNERS_STR', 'HUD_LOOSERS_STR', 'HUD_DRAW_STR']
    SPEC_TYPE_FIREPOWER = 0
    SPEC_TYPE_MANEV = 1
    SPEC_TYPE_SPEED = 2
    SPEC_TYPE_ALT = 3
    SPEC_TYPE_HP = 4
    SPEC_HINT_TYPE_FULL = 2
    SPEC_HINT_TYPE_TOOLTIP = 1
    SPEC_HINTS_COMPARISON_MAP = [[['LOBBY_AIRCRAFT_COMPARISON_FIREPOWER_EQUAL_ALLY_', 'LOBBY_AIRCRAFT_COMPARISON_YOUR_FIREPOWER_BETTER_ALLY_', 'LOBBY_AIRCRAFT_COMPARISON_FIREPOWER_BETTER_ALLY_'],
      ['LOBBY_AIRCRAFT_COMPARISON_NAMEUVERABILITY_EQUAL_ALLY_', 'LOBBY_AIRCRAFT_COMPARISON_YOUR_MANEUVERABILITY_BETTER_ALLY_', 'LOBBY_AIRCRAFT_COMPARISON_MANEUVERABILITY_BETTER_ALLY_'],
      ['LOBBY_AIRCRAFT_COMPARISON_SPEED_EQUAL_ALLY_', 'LOBBY_AIRCRAFT_COMPARISON_YOUR_SPEED_BETTER_ALLY_', 'LOBBY_AIRCRAFT_COMPARISON_SPEED_BETTER_ALLY_'],
      ['LOBBY_AIRCRAFT_COMPARISON_ALTITUDE_EQUAL_ALLY_', 'LOBBY_AIRCRAFT_COMPARISON_YOUR_ALTITUDE_BETTER_ALLY_', 'LOBBY_AIRCRAFT_COMPARISON_ALTITUDE_BETTER_ALLY_'],
      ['LOBBY_AIRCRAFT_COMPARISON_HITPOINTS_EQUAL_ALLY_', 'LOBBY_AIRCRAFT_COMPARISON_YOUR_HITPOINTS_BETTER_ALLY_', 'LOBBY_AIRCRAFT_COMPARISON_HITPOINTS_BETTER_ALLY_']], [['LOBBY_AIRCRAFT_COMPARISON_ENEMY_FIREPOWER_EQUAL_', 'LOBBY_AIRCRAFT_COMPARISON_YOUR_FIREPOWER_BETTER_', 'LOBBY_AIRCRAFT_COMPARISON_ENEMY_FIREPOWER_BETTER_'],
      ['LOBBY_AIRCRAFT_COMPARISON_ENEMY_NAMEUVERABILITY_EQUAL_', 'LOBBY_AIRCRAFT_COMPARISON_YOUR_MANEUVERABILITY_BETTER_', 'LOBBY_AIRCRAFT_COMPARISON_ENEMY_MANEUVERABILITY_BETTER_'],
      ['LOBBY_AIRCRAFT_COMPARISON_ENEMY_SPEED_EQUAL_', 'LOBBY_AIRCRAFT_COMPARISON_YOUR_SPEED_BETTER_', 'LOBBY_AIRCRAFT_COMPARISON_ENEMY_SPEED_BETTER_'],
      ['LOBBY_AIRCRAFT_COMPARISON_ENEMY_ALTITUDE_EQUAL_', 'LOBBY_AIRCRAFT_COMPARISON_YOUR_ALTITUDE_BETTER_', 'LOBBY_AIRCRAFT_COMPARISON_ENEMY_ALTITUDE_BETTER_'],
      ['LOBBY_AIRCRAFT_COMPARISON_ENEMY_HITPOINTS_EQUAL_', 'LOBBY_AIRCRAFT_COMPARISON_YOUR_HITPOINTS_BETTER_', 'LOBBY_AIRCRAFT_COMPARISON_ENEMY_HITPOINTS_BETTER_']]]
    SPEC_HINTS_ALL_SAME = [['LOBBY_AIRCRAFT_COMPARISON_ALLY', 'LOBBY_AIRCRAFT_COMPARISON_ALLY', 'LOBBY_AIRCRAFT_COMPARISON_ALLY'], ['LOBBY_AIRCRAFT_COMPARISON_ENEMY_ALL_EQUAL_2', 'LOBBY_AIRCRAFT_COMPARISON_YOUR_ALL_BETTER_2', 'LOBBY_AIRCRAFT_COMPARISON_ENEMY_ALL_BETTER_2']]

    def __init__(self):
        GUIWindow.__init__(self, 'hud.swf')
        self._ms = MeasurementSystem()
        self.isModalMovie = False
        self.__isSpectator = False
        self.__hudState = HudStateType.INITIALIZED
        self.__isOptionVisible = False
        self.__isInited = False
        self.__isRadarAltimetr = True
        self.__isTeamStatsVisible = False
        self.__isInputStayActive = False
        self.__headerMsgCallbackId = None
        self.__taskbarIconFlashed = False
        self.__respawnTextCallbackID = None
        self.__isResultScreenTutorial = False
        self.onTutorialUIBtnClick = Event()
        self.onTutorialInitialized = Event()
        self.onTutorialPaused = Event()
        self.onGetTimer = Event()
        self.onTutorialMouseClick = Event()
        self.onHitLimitAreaCircleEvent = Event()
        self.onTutorialResultInitialized = Event()
        self.onTutorialResultClose = Event()
        self.onTutorialResultContinue = Event()
        self.onTutorialResultReject = Event()
        self.onTutorialResultRestart = Event()
        self.onWarningChanged = Event()
        self.__curBasesPrc = [0, 0]
        self.__messagesStackForSingleDisplay = []
        self.__playerFlags = {}
        self.__teamSpeechLastPlayer = {}
        self.__warningMessages = {gui.hud.WarningType.LOW_ALTITUDE: [['hud.variometerMessage', 'HUD_TOO_LOW_ALTITUDE_STR']],
         gui.hud.WarningType.BORDER_TOO_CLOSE: [['borderTooClose', 'HUD_MAP_BORDER_TOO_CLOSE']],
         gui.hud.WarningType.STALL: [['hud.speedometerMessage', 'HUD_STALL_STR']],
         gui.hud.WarningType.HEIGHT_SPEED: [['hud.speedometerMessage', 'HUD_CRYTICAL_SPEED_STR']],
         gui.hud.WarningType.AUTOPILOT: [['autopilot', 'ui_autopilot_mode'], ['autopilot1', 'HUD_MESSAGE_AUTOPILOT']],
         gui.hud.WarningType.COLLISION_WARNING: [['hud.variometerMessage', 'HUD_TOO_LOW_ALTITUDE_STR']]}
        self.__resetWarningIndicatorsFlags()
        self.__speedNorm = 0.0
        self.__altitudeNorm = 0.0
        self.gameResult = None
        self.WEAPON_GROUPS_COMMANDS = {1: InputMapping.CMD_FIRE_GROUP_1,
         2: InputMapping.CMD_FIRE_GROUP_2,
         3: InputMapping.CMD_FIRE_GROUP_3}
        self.__currentLives = None
        self.__maxLives = None
        self.__respawnCount = 0
        self.__spectatorHintEnabled = False
        self.__spectatorHintVisibilityCallback = None
        self.__uiInitialized = False
        self.__deferredCompareVehicle = None
        return

    def getHolidayLocal(self, idLocal):
        import BWPersonality
        listEvents = BWPersonality.g_initPlayerInfo.activeEvents
        if listEvents is None:
            return idLocal
        else:
            for holiday in listEvents:
                matrix = LOCAL_HOLIDAYS_MATRIX.get(holiday, None)
                if matrix is not None:
                    return matrix.get(idLocal, idLocal)

            return idLocal

    def getSpecHint(self, teamIndex, specType, state, specHintType):
        return '{0}{1}'.format(self.SPEC_HINTS_COMPARISON_MAP[teamIndex][specType][state], specHintType)

    def initialized(self):
        self.movie.backgroundAlpha = 0.0
        self.addExternalCallbacks({'setBattleLoadingTabIndex': self.setBattleLoadingTabIndex,
         'hud.requestChatSend': self.onSendChatMessage,
         'ui.ChangeMiniScreenPosition': self.onMiniScreenPositionChange,
         'ui.ChangeRadarPosition': self.onRadarPositionChange,
         'hud.setMinimapLimitPosition': self.__onSetMinimapLimitPosition,
         'ui.requestRadarSize': self.getRadarSize,
         'hud.requestShowCursor': self.showCursor,
         'hud.requestHideCursor': self.hideCursor,
         'hud.requestSetCursorPosition': self.__setCursorPosition,
         'hud.requestStartDispatchKeyInput': self.startDispatchKeyInput,
         'hud.requestStopDispatchKeyInput': self.stopDispatchKeyInput,
         'settings.GetSettings': self.onEnterOptions,
         'settings.Close': self.onCloseOptions,
         'hud.requestBackToHangar': self.onRequestBackToHangar,
         'hud.requestExit': self.onRequestExit,
         'hud.requestForum': self.onRequestForum,
         'hud.requestError': self.onRequestError,
         'hud.requestHideBackendGraphics': self.requestHideBackendGraphics,
         'hud.requestShowBackendGraphics': self.requestShowBackendGraphics,
         'hud.hide': lambda : GameEnvironment.getHUD().setVisibilityBattleloading(False),
         'hud.show': lambda : GameEnvironment.getHUD().setVisibilityBattleloading(True),
         'system.loadingClosed': BigWorld.player().onHUDBattleLoadingClosed,
         'help.initialized': self.onHelp,
         'help.deInitialized': self.__onHelpClose,
         'hud.onButtonClick': self.onTutorialUIBtnClick,
         'hud.tutorialInitialized': self.onTutorialInitialized,
         'hud.tutorialPaused': self.onTutorialPaused,
         'hangar.tutorialInitialized': self.onTutorialResultInitialized,
         'hangar.closeTutorial': self.onTutorialResultClose,
         'hangar.continueTutorial': self.onTutorialResultContinue,
         'hangar.rejectionTutorial': self.onTutorialResultReject,
         'hangar.startTutorial': self.onTutorialResultRestart,
         'hud.countTickTimer': self.onGetTimer,
         'hud.onTutorialMouseClick': self.onTutorialMouseClick,
         'hud.hitLimitAreaCircle': self.onHitLimitAreaCircleEvent,
         'debugMenuEvent': self.onDevMenuEvent,
         'onSavePlayerListChangeState': self.__onSavePlayerListChangeState,
         'tutorial.onEnterState': GameEnvironment.getHUD().onTutorialEnterState,
         'hud.requestMutePlayer': self.__requestMutePlayer,
         'hud.getActiveQuest': self.__onGetActiveQuest,
         'hud.onUseEquipment': self.__onUseEquipment,
         'hud.onDenunciation': self.__onDenunciation,
         'hud.editFriendStatus': self.__editFriendStatus,
         'hud.editIgnoreStatus': self.__editIgnoreStatus,
         'hud.onOpenChat': GameEnvironment.getHUD().onOpenChat,
         'requestComparingVehicle': self.__onRequestComparingVehicle,
         'battleLoadingClose': self.__battleLoadingClose,
         'hud.pressButtonReplays': BattleReplay.g_replay.action,
         'hud.setPositionReplays': BattleReplay.g_replay.rewindToTime,
         'hud.switchToVehicle': self.__switchToVehicle,
         'hud.outroFadein': BigWorld.player().exitGame,
         'hud.spectatorModeDynamicCameraSwitch': GameEnvironment.getHUD().spectatorModeDynamicCameraSwitch})
        self.hideCursor()
        self.__linkEvents()
        GUIWindow.initialized(self)
        self.call_1('hud.playerListChangeState', Settings.g_instance.getGameUI()['curPlayerListState'])
        self.call_1('hud.battleUIType', Settings.g_instance.getGameUI()['combatInterfaceType'])
        self.call_1('battleLoadingTabIndex', Settings.g_instance.gameUI['battleLoadingTabIndex'])
        self.call_1('hud.preIntroEnabled', Settings.g_instance.preIntroEnabled and not BattleReplay.isPlaying())
        self.__setMapInfo()
        self.__isInited = True
        self.updateHUDSettings()
        self.__updateKeys()
        self.updateAim()
        self.chatUpdateStatus()
        self.__help = Help()
        self.uiCall('hud.chatIsSquad', bool(SQUAD_TYPES.playerSquadID()))
        self.__onDenunciationsLeft()
        self.uiCall('hud.isSuperiority2', SUPERIORITY2_BASE_HEALTH)
        self.__onNewAvatarsInfo()
        if Settings.g_instance.clusterID == CLASTERS.CN:
            self._startTickerNews()

    def __linkEvents(self):
        clientArena = GameEnvironment.getClientArena()
        clientArena.onUpdateTurretBoosterInfo += self.__updateTurretBoosterInfo
        clientArena.onGameResultChanged += self.__onGameResultChanged
        clientArena.onNewAvatarsInfo += self.__onNewAvatarsInfo
        clientArena.onUpdatePlayerStats += self.onUpdatePlayerStats
        clientArena.onUpdateTeamSuperiorityPoints += self.onUpdateTeamSuperiorityPoints
        clientArena.onUpdateDominationPrc += self.onUpdateDominationPrc
        InputMapping.g_instance.onSaveControls += self.__updateControls
        BattleReplay.g_replay.eInitHUD += self.__replayInitHUD
        BattleReplay.g_replay.eUpdateHUDProgress += self.__replayUpdateHUDProgress
        BattleReplay.g_replay.eUpdateHUDButtons += self.__replayUpdateHUDButtons
        BattleReplay.g_replay.eShowMessageHUD += self.__replayShowMessage
        BattleReplay.g_replay.eShowPanel += self.__replayShowPanel
        BattleReplay.g_replay.eHidePanel += self.__replayHidePanel
        BattleReplay.g_replay.eShowFinish += self.__replayShowFinish
        GlobalEvents.onQuestSelectUpdated += self.__onQuestSelectUpdate

    def __unlinkEvents(self):
        InputMapping.g_instance.onSaveControls -= self.__updateControls
        clientArena = GameEnvironment.getClientArena()
        if clientArena is not None:
            clientArena.onUpdateTurretBoosterInfo -= self.__updateTurretBoosterInfo
            clientArena.onNewAvatarsInfo -= self.__onNewAvatarsInfo
            clientArena.onUpdatePlayerStats -= self.onUpdatePlayerStats
            clientArena.onUpdateTeamSuperiorityPoints -= self.onUpdateTeamSuperiorityPoints
            clientArena.onUpdateDominationPrc -= self.onUpdateDominationPrc
            clientArena.onGameResultChanged -= self.__onGameResultChanged
        BattleReplay.g_replay.eShowFinish -= self.__replayShowFinish
        BattleReplay.g_replay.eHidePanel -= self.__replayHidePanel
        BattleReplay.g_replay.eShowPanel -= self.__replayShowPanel
        BattleReplay.g_replay.eShowMessageHUD -= self.__replayShowMessage
        BattleReplay.g_replay.eUpdateHUDButtons -= self.__replayUpdateHUDButtons
        BattleReplay.g_replay.eUpdateHUDProgress -= self.__replayUpdateHUDProgress
        BattleReplay.g_replay.eInitHUD -= self.__replayInitHUD
        GlobalEvents.onQuestSelectUpdated -= self.__onQuestSelectUpdate
        return

    def __onGameResultChanged(self, gameResult, winState):
        LOG_DEBUG('__onGameResultChanged', gameResult, winState)
        player = BigWorld.player()
        if gameResult in UI.GAME_RESULT_SIDE_COLOR and gameResult in UI.GAME_RESULT_LOC_IDS:
            resIndex = 2 if winState == 2 else int(player.teamIndex != winState)
            if gameResult == GAME_RESULT.ELIMINATION:
                self.uiClearTextLabel(self.getHolidayLocal('HUD_MESSAGE_ALLIES_DEAD'))
                self.uiClearTextLabel(self.getHolidayLocal('HUD_MESSAGE_ENEMIES_DEAD'))
            self.gameResult = (resIndex,
             gameResult,
             localizeHUD(self.getHolidayLocal(UI.GAME_RESULT[resIndex])),
             localizeHUD(UI.GAME_RESULT_LOC_IDS[gameResult][resIndex]))

    def __onNewAvatarsInfo(self, newAvatarsList = None):
        player = BigWorld.player()
        LOG_DEBUG('UI::__onNewAvatarsInfo(), stateName=%s' % EntityStates.getStateName(player.state))
        if self.__isInited:
            if 'clanAbbrev' in GameEnvironment.getClientArena().getAvatarInfo(player.id):
                self.initHealthmeter()
            self.setIsSpectator(EntityStates.inState(player, EntityStates.DEAD | EntityStates.OBSERVER | EntityStates.END_GAME))
            self.updateTeamsLists(GameEnvironment.getClientArena().getSortedAvatarInfosList())
            self.__getUsersChatStatus(newAvatarsList)
            self.uiCall('hud.chatIsSquad', bool(SQUAD_TYPES.playerSquadID()))
        if self.__uiInitialized or not GameEnvironment.getClientArena().isAllServerDataReceived():
            return
        else:
            GameEnvironment.getHUD().UIinitialized()
            LOG_DEBUG('UI initialized')
            VOIP.api().onEnterArenaScreen()
            self.__uiInitialized = True
            if self.__deferredCompareVehicle is not None:
                self.__onRequestComparingVehicle(self.__deferredCompareVehicle)
                self.__deferredCompareVehicle = None
            return

    def dispossessUI(self):
        self.__unlinkEvents()
        self.removeAllCallbacks()
        if self.__headerMsgCallbackId is not None:
            BigWorld.cancelCallback(self.__headerMsgCallbackId)
            self.__headerMsgCallbackId = None
        self.__clearSpectatorHintVisibilityCallback()
        import BWPersonality
        BWPersonality.g_waitingInfoHelper.startWaiting(WAITING_INFO_TYPE.ACCOUNT_INIT)
        return

    @property
    def state(self):
        return self.__hudState

    def stopTickerNews(self):
        if Settings.g_instance.clusterID == CLASTERS.CN:
            self._stopTickerNews()

    def __battleLoadingClose(self):
        if BigWorld.player().arenaStartTime <= 0.0:
            LOG_DEBUG('__battleLoadingClose - wait players')
            return
        GameEnvironment.getHUD().battleLoadingClose()
        self.updateHUDSettings()

    def __onRequestComparingVehicle(self, ID):
        if not self.__uiInitialized:
            self.__deferredCompareVehicle = ID
            return
        teamIndex = 0 if BigWorld.player().teamIndex == GameEnvironment.getClientArena().getAvatarInfo(ID)['teamIndex'] else 1
        vo = CustomObject()
        diff, state, percentDiff = getCalculatedBalanceCharacteristic(ID)
        vo.firepowerState = state['dps']
        vo.maneuverabilityState = state['maneuverability']
        vo.speedState = state['speedFactor']
        vo.heightState = state['optimalHeight']
        vo.hpState = state['hp']
        vo.firepower = diff['dps']
        vo.maneuverability = diff['maneuverability']
        vo.speed = diff['speedFactor']
        vo.height = diff['optimalHeight']
        vo.hp = diff['hp']
        vo.firepowerText = localizeLobby(self.getSpecHint(teamIndex, self.SPEC_TYPE_FIREPOWER, vo.firepowerState, self.SPEC_HINT_TYPE_TOOLTIP))
        vo.maneuverabilityText = localizeLobby(self.getSpecHint(teamIndex, self.SPEC_TYPE_MANEV, vo.maneuverabilityState, self.SPEC_HINT_TYPE_TOOLTIP))
        vo.speedText = localizeLobby(self.getSpecHint(teamIndex, self.SPEC_TYPE_SPEED, vo.speedState, self.SPEC_HINT_TYPE_TOOLTIP))
        vo.heightText = localizeLobby(self.getSpecHint(teamIndex, self.SPEC_TYPE_ALT, vo.heightState, self.SPEC_HINT_TYPE_TOOLTIP))
        vo.hpText = localizeLobby(self.getSpecHint(teamIndex, self.SPEC_TYPE_HP, vo.hpState, self.SPEC_HINT_TYPE_TOOLTIP))
        stateList = (state['dps'], state['maneuverability'], state['speedFactor'])
        vo.description = []
        if stateList.count(stateList[0]) == len(stateList):
            vo.description.append(localizeLobby(self.SPEC_HINTS_ALL_SAME[teamIndex][stateList[0]]))
        else:
            vo.description.append(localizeLobby(self.getSpecHint(teamIndex, self.SPEC_TYPE_FIREPOWER, vo.firepowerState, self.SPEC_HINT_TYPE_FULL)))
            vo.description.append(localizeLobby(self.getSpecHint(teamIndex, self.SPEC_TYPE_MANEV, vo.maneuverabilityState, self.SPEC_HINT_TYPE_FULL)))
            vo.description.append(localizeLobby(self.getSpecHint(teamIndex, self.SPEC_TYPE_SPEED, vo.speedState, self.SPEC_HINT_TYPE_FULL)))
        vo.description.append(localizeLobby(self.getSpecHint(teamIndex, self.SPEC_TYPE_ALT, vo.heightState, self.SPEC_HINT_TYPE_FULL)))
        self.call_1('responseComparingVehicle', vo)

    def __switchToVehicle(self, playerID):
        self.uiClearTextLabel('spectatorModeInfoAboutTypeDeath')
        BigWorld.player().switchToVehicle(playerID)

    def __onDenunciation(self, playerID, denunciationID, violatorKind):
        """
        @param <int> playerID:
        @param denunciationID:  see class consts.DENUNCIATION
        @param <int> violatorKind:    1 - enemy, 2 - ally
        """
        DBId = GameEnvironment.getClientArena().getDBId(playerID)
        if DBId is not None:
            onDenunciation(DBId, denunciationID, violatorKind)
            self.__onDenunciationsLeft()
        else:
            LOG_ERROR('__onDenunciation - playerID(%s) not in voipMap, or voipMap not defined' % playerID)
        return

    def __onDenunciationsLeft(self):
        import BWPersonality
        self.call_1('hud.denunciations', BWPersonality.g_initPlayerInfo.denunciationsLeft)

    def __onUseEquipment(self, slotID):
        GameEnvironment.getHUD().onUseEquipment(slotID)

    def __editFriendStatus(self, playerID, operation):
        """
        @param <int> playerID:
        @param <bool> operation:  true - add to friends, false - remove from friends
        """
        DBId = GameEnvironment.getClientArena().getDBId(playerID)
        if DBId is not None:
            LOG_DEBUG('__editFriendStatus', DBId, operation)
            if messenger.g_xmppChatHandler:
                playerName = GameEnvironment.getClientArena().getObjectName(playerID)
                messenger.g_xmppChatHandler.editFriendList(DBId, playerName, operation)
        else:
            LOG_ERROR('__editFriendStatus: can not get dbid by playerID(%s)' % playerID)
        return

    def __editIgnoreStatus(self, playerID, operation):
        """
        @param <int> playerID:
        @param <bool> operation:  true - add to ignore list, false - remove from ignore list
        """
        DBId = GameEnvironment.getClientArena().getDBId(playerID)
        if DBId is not None:
            LOG_DEBUG('__editIgnoreStatus', DBId, operation)
            if messenger.g_xmppChatHandler:
                playerName = GameEnvironment.getClientArena().getObjectName(playerID)
                messenger.g_xmppChatHandler.editIgnoreList(DBId, playerName, operation)
        else:
            LOG_ERROR('__editIgnoreStatus: can not get dbid by playerID(%s)' % playerID)
        return

    def __getUsersChatStatus(self, avatarsList):
        if messenger.g_xmppChatHandler:
            if avatarsList:
                infoList = avatarsList
            else:
                infoList = GameEnvironment.getClientArena().avatarInfos.values()
            dbidList = []
            for avatar in infoList:
                dbid = avatar.get('databaseID')
                if dbid is not None:
                    dbidList.append(dbid)
                elif avatarsList:
                    LOG_ERROR('__getUsersChatStatus: can not get databaseID by in avatars info')

            messenger.g_xmppChatHandler.getUsersChatStatus(dbidList)
        return

    def setPlayersChatStatus(self, playersList):
        playersChatStatusList = []
        for playerStatus in playersList:
            itemVO = PlayerChatStatus(playerStatus[0], playerStatus[1])
            playersChatStatusList.append(itemVO)

        self.call_1('hud.playerListSetChatList', playersChatStatusList)

    @property
    def isInited(self):
        return self.__isInited

    def setBattleLoadingTabIndex(self, val):
        Settings.g_instance.setGameUIValue('battleLoadingTabIndex', val)

    def chatUpdateStatus(self):
        owner = BigWorld.player()
        vo = CustomObject()
        vo.isBanned = getattr(owner, 'isChatBan', False)
        vo.isEnabled = Settings.g_instance.gameUI['isChatEnabled'] and not GameEnvironment.getHUD().isTutorial()
        self.call_1('hud.chatUpdateStatus', vo)

    def setCameraRingVisible(self, visible):
        if self.__isInited:
            self.call_1('hud.visibleCenterPoint', visible)
        else:
            self.__cameraRingVisible = visible

    def onChangeLanguage(self):
        self.__resetWarningIndicatorsFlags()
        self.updateHUDSettings(True)
        self.__updateLocalizedPlanesName()
        self.initHealthmeter()
        self.__setMapInfo()

    def __setMapInfo(self):
        battleType, battleName, mapName, teamTask, playerTask = BattleInfo().getBattleInfo()
        self.call_1('hud.setMapInfo', battleType, battleName, mapName, teamTask, playerTask, not BigWorld.player().isPvPUnlocked)

    def onRequestForum(self):
        WebPageHolder().openWebBrowser(WebPageHolder.URL_FORUM)

    def onRequestError(self):
        WebPageHolder().openWebBrowser(WebPageHolder.URL_SEND_ERROR)

    def onRequestExit(self):
        LOG_TRACE('UI Quit')
        BigWorld.quit()

    def onRequestBackToHangar(self):
        player = BigWorld.player()
        player.exitGame()

    def __onSavePlayerListChangeState(self, playerListState):
        GameEnvironment.getHUD().onSavePlayerListChangeState(int(playerListState))

    def onVisibilityTeams(self, visibleFlag):
        self.__isTeamStatsVisible = visibleFlag
        self.call_1('hud.onVisibilityTeams', visibleFlag)

    def onVisibilityCursor(self, visibleFlag):
        self.call_1('hud.onVisibilityCursor', visibleFlag)

    def requestHideBackendGraphics(self, state):
        """
        @param state: <FLASH_HUD_STATES>
        """
        self.__isInputStayActive = self.__isTeamStatsVisible
        if FLASH_HUD_STATES.TAB == state and not self.__isTeamStatsVisible:
            return
        if not self.__isInputStayActive:
            GameEnvironment.g_instance.eHideBackendGraphics()

    def requestShowBackendGraphics(self):
        if not self.__isInputStayActive:
            GameEnvironment.g_instance.eShowBackendGraphics()
            if self.__isOptionVisible:
                self.onCloseOptions()

    def initBattleResult(self):
        LOG_TRACE('initBattleResult')
        self.call_1('hud.battleResultShow')

    def initHealthmeter(self, owner = None):
        owner = owner or BigWorld.player()
        ownerData = GameEnvironment.getClientArena().getAvatarInfo(owner.id)
        self.call_1('hud.healthmeterInit', owner.objectName, ownerData['clanAbbrev'], localizeAirplane(owner.settings.airplane.name), owner.maxHealth, owner.health)

    def init(self, battleDuration, owner = None):
        self.hideCursor()
        if owner is None:
            owner = BigWorld.player()
        self.call_1('hud.playerTaskSetup', owner.settings.airplane.planeType)
        self.__battleDuration = battleDuration
        self.__initGuns(owner, False)
        gameUI = Settings.g_instance.getGameUI()
        self.onChangeAviahorizonMode(gameUI['horizonList'])
        speedometerInfo = CustomObject()
        speedometerInfo.state = gameUI['mainDevices']
        speedometerInfo.message = ''
        speedometerInfo.metric = self._ms.localizeHUD('ui_speed')
        speedometerInfo.force = 1.0
        speedometerInfo.speed = 0.0
        speedometerInfo.temperature = 0.0
        speedometerInfo.xs, speedometerInfo.x1, speedometerInfo.x2, speedometerInfo.x3, speedometerInfo.x4, speedometerInfo.xf, speedometerInfo.speedNorm = preparedBattleData[owner.globalID].speedometer
        self.__speedNorm = speedometerInfo.speedNorm * METERS_PER_SEC_TO_KMH_FACTOR
        speedometerInfo.speedNorm = self._ms.getKmh(self.__speedNorm)
        speedometerInfo.maxTemperature = (WEP_MAX_TEMPERATURE - WEP_ENABLE_TEMPERATURE) / ENGINE_WORK_INTERVAL
        self.call_1('hud.speedometerInit', speedometerInfo)
        variometerInfo = CustomObject()
        variometerInfo.state = gameUI['mainDevices']
        variometerInfo.message = ''
        variometerInfo.metric = self._ms.localizeHUD('ui_vario')
        variometerInfo.altitude = 0.0
        variometerInfo.xs, variometerInfo.x1, variometerInfo.x2, variometerInfo.x3, variometerInfo.x4, variometerInfo.xf, variometerInfo.altitudeNorm = preparedBattleData[owner.globalID].altimeter
        self.__altitudeNorm = variometerInfo.altitudeNorm
        variometerInfo.altitudeNorm = self._ms.getMeters(self.__altitudeNorm)
        self.call_1('hud.variometerInit', variometerInfo)
        return

    def initVarioAndSpeed(self, owner):
        speedometerInfo = CustomObject()
        speedometerInfo.xs, speedometerInfo.x1, speedometerInfo.x2, speedometerInfo.x3, speedometerInfo.x4, speedometerInfo.xf, speedometerInfo.speedNorm = preparedBattleData[owner.globalID].speedometer
        self.__speedNorm = speedometerInfo.speedNorm * METERS_PER_SEC_TO_KMH_FACTOR
        speedometerInfo.speedNorm = self._ms.getKmh(self.__speedNorm)
        self.call_1('hud.speedometerInit', speedometerInfo)
        variometerInfo = CustomObject()
        variometerInfo.xs, variometerInfo.x1, variometerInfo.x2, variometerInfo.x3, variometerInfo.x4, variometerInfo.xf, variometerInfo.altitudeNorm = preparedBattleData[owner.globalID].altimeter
        self.__altitudeNorm = variometerInfo.altitudeNorm
        variometerInfo.altitudeNorm = self._ms.getMeters(self.__altitudeNorm)
        self.call_1('hud.variometerInit', variometerInfo)

    def ___updateSpeedometerAndVariometerInfo(self):
        speedometerInfo = CustomObject()
        speedometerInfo.speedNorm = self._ms.getKmh(self.__speedNorm)
        self.call_1('hud.speedometerInit', speedometerInfo)
        variometerInfo = CustomObject()
        variometerInfo.altitudeNorm = self._ms.getMeters(self.__altitudeNorm)
        self.call_1('hud.variometerInit', variometerInfo)

    def reInit(self, fullReinit):
        if fullReinit:
            self.__resetWarningIndicatorsFlags()
        self.updateHUDSettings()

    def onChangeAviahorizonMode(self, val):
        LOG_DEBUG('onChangeAviahorizonMode', val)
        self.call_1('hud.aviahorizonSetMode', val)

    def changeSpeedometerState(self, val):
        self.call_1('hud.speedometerState', val)

    def changeVariometerState(self, val):
        self.call_1('hud.variometerState', val)

    def startDispatchKeyInput(self):
        self.__isInputStayActive = True
        owner = BigWorld.player()
        owner.setFlyKeyBoardInputAllowed(False)

    def stopDispatchKeyInput(self):
        self.__isInputStayActive = False
        owner = BigWorld.player()
        owner.setFlyKeyBoardInputAllowed(True)

    def showCursor(self):
        if not GameEnvironment.getHUD().map.isVisible():
            Cursor.forceShowCursor(True)
            entity = BigWorld.player()
            entity.setFlyMouseInputAllowed(False)
        GameEnvironment.getHUD().updateMinimapSize()

    def hideCursor(self):
        if not GameEnvironment.getHUD().map.isVisible() and not self.__isResultScreenTutorial:
            Cursor.forceShowCursor(False)
            entity = BigWorld.player()
            entity.setFlyMouseInputAllowed(True)
        GameEnvironment.getHUD().updateMinimapSize()

    def __setCursorPosition(self, x, y):
        """
        callback from flash
        @param x: float
        @param y: float
        """
        GUI.mcursor().position = Math.Vector2(x, y)

    def onMiniScreenPositionChange(self, posX, posY):
        Settings.g_instance.changeMiniScreenPosition(posX, posY)

    def onRadarPositionChange(self, posX, posY):
        Settings.g_instance.changeRadarPosition(posX, posY)

    def __onSetMinimapLimitPosition(self, posX, posY):
        """
        set limit position for minimap in pixels
        @param posX:<float>
        @param posY:<float>
        """
        GameEnvironment.getHUD().setMinimapLimitPosition(posX, posY)

    def getRadarSize(self):
        size = GameEnvironment.getHUD().getRadarSize()
        if size is not None:
            self.call_1('hud.radarSize', size[0], size[1])
        else:
            LOG_WARNING('getRadarSize - radar size is None')
        return

    def updateHUDSettings(self, updateLanguage = False):
        if not self.__isInited:
            return
        self.call_1('hud.speedometerMetric', self._ms.localizeHUD('ui_speed'))
        self.call_1('hud.variometerMetric', self._ms.localizeHUD('ui_vario'))
        self.___updateSpeedometerAndVariometerInfo()
        gameUI = Settings.g_instance.getGameUI()
        self.__isRadarAltimetr = gameUI['heightMode'] != 0
        for indicatorIndex in range(0, len(self.warningIndicatorsFlags)):
            self.updateWarningIndicator(indicatorIndex, self.warningIndicatorsFlags[indicatorIndex], True)

        if not updateLanguage:
            self.call_1('hud.updateState', self.__getObjVisualSettings())
            self.call_1('hud.variometerHeightMode', gameUI['heightMode'])

    def __updateControls(self):
        if GameEnvironment.g_instance.isPlayerStarted():
            self.__updateKeys()
            self.__initGuns(BigWorld.player(), True)
            GameEnvironment.getHUD().updateEquipmentControls(BigWorld.player().consumables)

    def __updateKeys(self):
        vo = CustomObject()
        vo.force = getKeyLocalization(InputMapping.CMD_INCREASE_FORCE)
        vo.showTeams = getKeyLocalization(InputMapping.CMD_SHOW_TEAMS)
        vo.showMap = getKeyLocalization(InputMapping.CMD_SHOW_MAP)
        self.call_1('hud.updateKeys', vo)

    def updateAim(self):
        vo = CustomObject()
        for key, value in Settings.g_instance.getAimsData().items():
            setattr(vo, key, value)

        self.call_1('hud.updateCameraType', getattr(InputMapping.g_instance.primarySettings, 'CAMERA_TYPE', -1))
        self.call_1('hud.updateAim', vo)

    def __getObjVisualSettings(self):
        gameUI = Settings.g_instance.getGameUI()
        visualSettings = CustomObject()
        isLivePlayers = self.__spectatorHintEnabled and GameEnvironment.getHUD().isLivePlayers() if not EntityStates.inState(BigWorld.player(), EntityStates.GAME | EntityStates.WAIT_START | EntityStates.PRE_START_INTRO) else True
        visualSettings.spectatorHint = 0 if not isLivePlayers else 1
        visualSettings.damagePanel = 0 if not isLivePlayers else (1 + gameUI['damageSchemaLocationList'] if gameUI['damageSchema'] else 0)
        visualSettings.weaponPanel = 0 if self.__isSpectator else 1
        visualSettings.speedometer = 0 if not isLivePlayers else (1 + gameUI['mainDevicesLocationList'] if gameUI['mainDevices'] else 0)
        visualSettings.variometer = visualSettings.speedometer
        if not GameEnvironment.getHUD().isTutorial():
            visualSettings.playerList = 1 + gameUI['players'] if gameUI['players'] and (not self.__isSpectator or GameEnvironment.getHUD().getSpectatorMode() == SPECTATOR_MODE_STATES.OBSERVER) else 0
        visualSettings.healthMeter = visualSettings.damagePanel
        visualSettings.aviahorizont = 0 if not GameEnvironment.getCamera().zoomPresent() else gameUI['horizon']
        visualSettings.captureBase = True
        visualSettings.crosshair = 0 if not GameEnvironment.getCamera().zoomPresent() else 1
        visualSettings.crosshair = visualSettings.crosshair and self.__hudState == HudStateType.BATTLE_STARTED
        visualSettings.targetWindow = 0 if self.__isSpectator else gameUI['targetWindow']
        visualSettings.navWindow = gameUI['navigationWindowMinimap']
        visualSettings.speedometerAndVariometer = gameUI['speedometerAndVariometer']
        visualSettings.bombRocketPanel = 0 if self.__isSpectator else self.__checkHasBombOrRockets()
        visualSettings.forsage = 0 if self.__isSpectator else 1
        visualSettings.equipmentPanel = 0 if self.__isSpectator else 1
        return visualSettings

    def __checkHasBombOrRockets(self):
        owner = BigWorld.player()
        weaponGroups = owner.getAmmoGroupsInitialInfo()
        for groupID, weaponData in weaponGroups.items():
            if weaponData['shellID'] != -1 and weaponData['description'] is not None:
                return 1

        return 0

    def __resetWarningIndicatorsFlags(self):
        self.warningIndicatorsFlags = len(self.__warningMessages) * [False]

    def updateWarningIndicator(self, indicatorIndex, flag, override = False):
        LOG_DEBUG('updateWarningIndicator', indicatorIndex, flag, override)
        if self.warningIndicatorsFlags[indicatorIndex] != flag or override:
            self.warningIndicatorsFlags[indicatorIndex] = flag
            for labelTextData in self.__warningMessages[indicatorIndex]:
                label = labelTextData[0]
                text = localizeHUD(self.getHolidayLocal(labelTextData[1]))
                if indicatorIndex == gui.hud.WarningType.BORDER_TOO_CLOSE or indicatorIndex == gui.hud.WarningType.AUTOPILOT:
                    text = text if indicatorIndex == gui.hud.WarningType.AUTOPILOT else ''.join([text, '\n'])
                    if flag:
                        self.call_1('hud.labelSetText', TextLabel(label, text))
                    else:
                        self.call_1('hud.labelClearText', label)
                elif Settings.g_instance.gameUI['mainDevices'] == 1:
                    self.call_1(label, text if flag else '')
                self.onWarningChanged(indicatorIndex, flag)

    def forceUpdate(self, spawnedStatusLocalization, health, teamStats):
        self.setIsSpectator(False)
        self.updateHealth(health)
        self.movingTargetVisibility(True)
        self.updateTeamsLists(teamStats)

    def setVisibility(self, flag):
        self.call_1('hud.setVisibility', flag)

    def updateTime(self, serverTime, arenaStartTime):
        if not self.__isInited:
            return
        if arenaStartTime <= 0:
            if self.__hudState != HudStateType.WAIT_PLAYERS and GameEnvironment.getHUD().isBattleLoadingDispossessed():
                self.__hudState = HudStateType.WAIT_PLAYERS
                if self.__respawnCount == 0:
                    self.call_1('hud.labelSetText', TextLabel('prebattle', localizeHUD('wait_players')))
                self.call_1('hud.updateTime', 0)
                LOG_INFO('HUD - set state WAIT_PLAYERS', serverTime, arenaStartTime)
            self.call_1('hud.updateTime', 0)
        else:
            curTime = int(round(arenaStartTime - serverTime))
            if curTime > 0:
                if self.__hudState != HudStateType.WAIT_BATTLE and GameEnvironment.getHUD().isBattleLoadingDispossessed():
                    self.__hudState = HudStateType.WAIT_BATTLE
                    if self.__respawnCount == 0:
                        self.call_1('hud.labelSetText', TextLabel('prebattle', localizeHUD('wait_battle')))
                    LOG_INFO('HUD - set state WAIT_BATTLE', serverTime, arenaStartTime)
                self.call_1('hud.updateTime', -curTime)
                self.call_1('hud.bigTimerUpdateTime', curTime)
                player = BigWorld.player()
                if GameEnvironment.getHUD().isArenaLoaded():
                    GameSound().ui.play('UISoundTimerClock')
                taskbarIconFlashed = self.__taskbarIconFlashed
                if curTime <= 5:
                    windowVisible = BigWorld.isWindowVisible()
                    windowFocused = BigWorld.isWindowFocused()
                    windowStateOK = not windowVisible or not windowFocused
                    if not taskbarIconFlashed and windowStateOK:
                        BigWorld.startFlashTaskbarIconRed()
                    self.__taskbarIconFlashed = True
                else:
                    self.__taskbarIconFlashed = False
                if curTime <= TIME_FOR_HIDE_INTRO_HINT_BEFORE_START_BATTLE:
                    GameEnvironment.getHUD().stopIntroHintCallback()
            else:
                if self.__hudState != HudStateType.BATTLE_STARTED:
                    self.__hudState = HudStateType.BATTLE_STARTED
                    self.call_1('hud.labelClearText', 'prebattle')
                    self.call_1('hud.bigTimerHide')
                    if abs(curTime) < TIME_AFTER_ARENA_STARTED_FOR_HIDE_BEGIN_MESSAGES:
                        if self.__respawnCount == 0:
                            self.call_1('hud.labelSetText', TextLabel('battleBegin', localizeHUD(self.getHolidayLocal('WAIT_BATTLE_FINISH'))))
                    GameEnvironment.getInput().refreshButtons([InputMapping.CMD_SHOW_CURSOR, InputMapping.CMD_SHOW_MAP])
                    player = BigWorld.player()
                    GameEnvironment.getHUD().battleStarted()
                    player.battleStarted()
                    LOG_INFO('HUD - set state BATTLE_STARTED', serverTime, arenaStartTime)
                curTime += int(self.__battleDuration)
                if curTime < 0:
                    curTime = 0
                self.call_1('hud.updateTime', curTime)

    def updateAlert(self, msg, team, msgType = 0):
        LOG_DEBUG('updateAlert', msg, team, msgType)
        if msg:
            self.call_1('hud.messageEnemy' if team else 'hud.messageAlly', msg, msgType)

    def restart(self):
        if not SUPERIORITY2_BASE_HEALTH:
            return
        else:
            self.__respawnCount += 1
            if self.__currentLives == 1 and self.__maxLives > 1:
                self.call_1('hud.labelSetText', TextLabel('prebattle', localizeHUD('HUD_SPAWNS_COUNT_LAST')))
                if self.__respawnTextCallbackID is None:
                    self.__respawnTextCallbackID = BigWorld.callback(TIME_AFTER_ARENA_STARTED_FOR_HIDE_BEGIN_MESSAGES, self.__hidePrebattleText)
            elif self.__currentLives > 1:
                self.call_1('hud.labelSetText', TextLabel('prebattle', localizeHUD('HUD_SPAWNS_COUNT_BIG').format(curPlane=str(self.__currentLives - 1))))
                if self.__respawnTextCallbackID is None:
                    self.__respawnTextCallbackID = BigWorld.callback(TIME_AFTER_ARENA_STARTED_FOR_HIDE_BEGIN_MESSAGES, self.__hidePrebattleText)
            return

    def __hidePrebattleText(self):
        self.__respawnTextCallbackID = None
        self.call_1('hud.labelClearText', 'prebattle')
        return

    def onDestruction(self):
        LOG_DEBUG('onDestruction')
        if self.__currentLives > 1:
            self.__currentLives -= 1
        self.uiClearTextLabel('completionFightSuperiorityEnemy')
        self.uiClearTextLabel('completionFightSuperiority')
        self.uiClearTextLabel('completionFightLastPlaneEnemy')
        self.uiClearTextLabel('completionFightLastPlane')
        self.__resetWarningIndicatorsFlags()
        self.setIsSpectator(True)
        if EntityStates.inState(BigWorld.player(), EntityStates.DESTROYED_FALL):
            self.__spectatorHintVisibilityCallback = BigWorld.callback(FIRST_SWITCH_TO_THE_NEXT_VEHICLE_DELAY + 0.1, self.__spectatorHintVisibility)

    def __clearSpectatorHintVisibilityCallback(self):
        if self.__spectatorHintVisibilityCallback is not None:
            BigWorld.cancelCallback(self.__spectatorHintVisibilityCallback)
            self.__spectatorHintVisibilityCallback = None
        return

    def __spectatorHintVisibility(self):
        self.__clearSpectatorHintVisibilityCallback()
        self.setSpectatorHintEnabled(True)

    def setSpectatorHintEnabled(self, isEnabled):
        self.__spectatorHintEnabled = isEnabled
        self.updateHUDSettings()

    def setSpectatorMode(self, spectatorMode):
        if spectatorMode:
            self.call_1('hud.labelSetText', TextLabel('spectatorMode', localizeHUD('ui_spectator_mode')))
        else:
            self.call_1('hud.labelClearText', 'spectatorModeInfoAboutTypeDeath')
            self.call_1('hud.labelClearText', 'spectatorMode')

    def __initGuns(self, owner, isReinit):
        weaponSlotClass = WeaponSlotRecord
        uiFunction = 'hud.weaponInit'
        if isReinit:
            weaponSlotClass = WeaponSlotRecordBase
            uiFunction = 'hud.weaponReInit'
        weaponGroups = owner.getAmmoGroupsInitialInfo()
        groupsInfo = []
        from consts import MAX_WEAPON_GROUP
        groups = [0] + [1] * MAX_WEAPON_GROUP
        for groupID in weaponGroups.iterkeys():
            groups[groupID] = 0

        for groupID, weaponData in weaponGroups.items():
            if weaponData.get('description', None) is not None:
                groupsInfo.append(weaponSlotClass(groupID, weaponData, weaponData['objCount'], sum(groups[0:groupID]), self.WEAPON_GROUPS_COMMANDS))

        groupsInfo.sort(key=lambda g: g.id)
        self.call_1(uiFunction, groupsInfo)
        return

    def updateAmmoGroupCounters(self, gunsStatus):
        for groupID, countBullets in gunsStatus.items():
            self.call_1('hud.weaponUpdate', groupID, countBullets)

    def updateHealth(self, health):
        self.call_1('hud.healthmeterUpdate', health)

    def updateAmmo(self, prc):
        pass

    def reportEngineOverheat(self, msg):
        self.call_1('hud.labelSetText', TextLabel('engineOverheat', msg))

    def reportStatusGun(self, statusMessage):
        self.call_1('hud.labelSetText', TextLabel('statusGun', statusMessage))

    def reportOutOfBombs(self, msg):
        self.call_1('hud.labelSetText', TextLabel('outOfBombs', msg))

    def reportOutOfAmmo(self, msg):
        self.call_1('hud.labelSetText', TextLabel('outOfAmmo', msg))

    def updateForce(self, prc):
        self.call_1('hud.speedometerForce', prc)

    def updateEngineTemperature(self, prc, isForceEngine):
        self.call_1('hud.speedometerTemperature', prc, isForceEngine)

    def updateSpeed(self, v):
        self.call_1('hud.speedometerSpeed', self._ms.getKmh(v))

    def updateAltitude(self, aboveObstacle, aboveSea):
        if self.__isRadarAltimetr:
            self.call_1('hud.variometerAltitude', self._ms.getMeters(aboveObstacle), self._ms.getMeters(aboveSea))
        else:
            self.call_1('hud.variometerAltitude', self._ms.getMeters(aboveSea), self._ms.getMeters(aboveSea))

    def updateEngineStates(self, ping, fps, dataLost):
        self.call_1('hud.updateEngineStates', fps, ping, dataLost)

    def onSendChatMessage(self, message, messageType):
        message = message[:MESSAGE_MAX_SIZE]
        GameEnvironment.getHUD().broadcastChatMessage(message.encode('utf-8'), UI.CONVERT_CHAT_MSG_TYPE_FROM_FLASH.get(messageType, -1))

    def addChatMessage(self, chatMessage):
        chatMessage.msgType = UI.CONVERT_CHAT_MSG_TYPE_TO_FLASH.get(chatMessage.msgType, -1)
        self.call_1('hud.chatMessage', chatMessage)

    def movingTargetSize(self, curFOV, value):
        self.call_1('hud.crosshairTargetSize', value / curFOV * 2.0 * BigWorld.screenHeight())

    def movingTargetVisibility(self, flag):
        flag = flag and GameEnvironment.getCamera().zoomPresent()
        vo = CustomObject()
        vo.crosshair = flag and self.__hudState == HudStateType.BATTLE_STARTED
        self.setVisibilityAviahorizont(flag)
        self.call_1('hud.updateState', vo)

    def setVisibilityAviahorizont(self, isVisible):
        vo = CustomObject()
        vo.aviahorizont = isVisible and (0 if self.__isSpectator else Settings.g_instance.getGameUI()['horizon'])
        self.call_1('hud.updateState', vo)

    def setIsSpectator(self, isSpectator):
        LOG_DEBUG('setIsSpectator', isSpectator)
        self.__isSpectator = isSpectator
        self.updateHUDSettings()

    def updateTeamsLists(self, data):
        if not GameEnvironment.getClientArena().isAllServerDataReceived() or not self.isInited:
            return
        else:
            owner = BigWorld.player()
            playersList = []
            for avatarInfo in data:
                playerStatRecord = PlayerStatRecord(avatarInfo, owner)
                if playerStatRecord.ID == owner.id:
                    if self.__currentLives is None:
                        self.__currentLives = SUPERIORITY2_LIVES_COUNT
                        self.__maxLives = SUPERIORITY2_LIVES_COUNT
                if SUPERIORITY2_BASE_HEALTH and playerStatRecord.isBot:
                    continue
                playersList.append(playerStatRecord)

            LOG_DEBUG('updateTeamsLists', data)
            self.call_1('hud.playerListUpdate', playersList)
            return

    def onUpdatePlayerStats(self, avatarInfo):
        LOG_DEBUG('hud.playerListUpdateStats', avatarInfo)
        stats = avatarInfo['stats']
        avatarID = avatarInfo['avatarID']
        self.call_1('hud.playerListUpdateStats', PlayerStatRecordBase(avatarInfo, BigWorld.player()))
        if avatarID not in self.__playerFlags or self.__playerFlags[avatarID] != stats['flags']:
            self.__reportLastPlayer(BigWorld.player())
            self.__playerFlags[avatarID] = stats['flags']

    def __reportLastPlayer(self, player):
        livePlayersInTeams = [0, 0]
        countPlayersInTeams = [0, 0]
        playerInfo = GameEnvironment.getClientArena().avatarInfos.get(player.id)
        playerIsAlive = not bool(playerInfo and playerInfo['stats']['flags'] & AvatarFlags.DEAD != 0)
        for avatarInfo in GameEnvironment.getClientArena().avatarInfos.values():
            countPlayersInTeams[avatarInfo['teamIndex']] += 1
            isDead = avatarInfo['stats']['flags'] & AvatarFlags.DEAD != 0
            if not isDead:
                livePlayersInTeams[avatarInfo['teamIndex']] += 1

        if not all(livePlayersInTeams):
            return
        else:
            for teamIndex, livePlayersCount in enumerate(livePlayersInTeams):
                strId = None
                if livePlayersCount == 1 and countPlayersInTeams[teamIndex] > 1:
                    if teamIndex == player.teamIndex:
                        if playerIsAlive and EntityStates.inState(player, EntityStates.GAME):
                            strId = 'completionFightLastPlane'
                            text = localizeHUD(self.getHolidayLocal('HUD_MESSAGE_ALLIES_DEAD'))
                            if teamIndex not in self.__teamSpeechLastPlayer:
                                GameSound().voice.play('voice_battle_last_plane')
                                self.__teamSpeechLastPlayer[teamIndex] = True
                    else:
                        strId = 'completionFightLastPlaneEnemy'
                        text = localizeHUD(self.getHolidayLocal('HUD_MESSAGE_ENEMIES_DEAD'))
                        if teamIndex not in self.__teamSpeechLastPlayer:
                            GameSound().voice.play('voice_battle_last_plane_enemy')
                            self.__teamSpeechLastPlayer[teamIndex] = True
                if strId is not None and strId not in self.__messagesStackForSingleDisplay:
                    self.__messagesStackForSingleDisplay.append(strId)
                    self.uiCallTextLabel(strId, text)

            return

    def onUpdateDominationPrc(self, basesPrc):
        self.call_1('hud.captureBaseDomination', round(min(basesPrc[0], 1.0), 3), round(min(basesPrc[1], 1.0), 3))
        owner = BigWorld.player()
        if extractGameMode(owner.gameMode) == GAME_MODE.SUPERIORITY_2:
            return
        ownScore = int(basesPrc[0] * 100)
        enemyScore = int(basesPrc[1] * 100)
        if basesPrc[0] > basesPrc[1]:
            if ownScore >= PERCENT_BEFORE_DOMINATION_WIN > self.__curBasesPrc[0]:
                self.uiCallTextLabel('completionFightSuperiority', localizeHUD(self.getHolidayLocal('HUD_MESSAGE_ALLMOST_WIN')))
                GameSound().voice.play('voice_battle_superiority')
            elif self.__curBasesPrc[0] >= PERCENT_BEFORE_DOMINATION_WIN > ownScore:
                self.uiClearTextLabel('completionFightSuperiority')
        elif basesPrc[0] < basesPrc[1]:
            if enemyScore >= PERCENT_BEFORE_DOMINATION_WIN > self.__curBasesPrc[1]:
                self.uiCallTextLabel('completionFightSuperiorityEnemy', localizeHUD(self.getHolidayLocal('HUD_MESSAGE_ALLMOST_LOSE')))
                GameSound().voice.play('voice_battle_superiority_enemy')
            elif self.__curBasesPrc[1] >= PERCENT_BEFORE_DOMINATION_WIN > enemyScore:
                self.uiClearTextLabel('completionFightSuperiorityEnemy')
        self.__curBasesPrc[0] = ownScore
        self.__curBasesPrc[1] = enemyScore

    def onUpdateTeamSuperiorityPoints(self, prevScore, ownScore, enemyScore):
        if ownScore > enemyScore:
            if prevScore[0] <= prevScore[1]:
                self.updateAlert(localizeHUD('ui_we_have_the_advantage'), 0)
        elif ownScore < enemyScore:
            if prevScore[0] >= prevScore[1]:
                self.updateAlert(localizeHUD('ui_enemy_has_the_advantage'), 1)
        self.call_1('hud.captureBaseScore', ownScore, enemyScore)

    def __updateTurretBoosterInfo(self, sameTeam):
        player = BigWorld.player()
        if sameTeam:
            self.uiCallTextLabel('turretBoostEnemy', localizeHUD('HUD_MESSAGE_BOOSTER_LOST'))
            if EntityStates.inState(player, EntityStates.GAME):
                GameSound().voice.clearDynSeq()
                GameSound().voice.play('voice_ground_hq_destroyed')
        else:
            player.reportedDestroyedObjectHQTime = BigWorld.time()
            self.uiCallTextLabel('turretBoost', localizeHUD('HUD_MESSAGE_BOOSTER_GAIN'))
            GameSound().voice.skipDynSeqItems(['voice_ground_target_hit',
             'voice_ground_target_crit',
             'voice_ground_target_destroyed',
             'voice_ground_targets_destroyed',
             'voice_ground_target_fire'])
            if EntityStates.inState(player, EntityStates.GAME):
                GameSound().voice.play('voice_ground_enemy_hq_destroyed')

    def newBomberAvailable(self, teamIndex):
        self.call_1('ui.newBomberAvailable', [teamIndex])

    def incomingBomberNotification(self, startTime, teamIndex):
        self.call_1('ui.incomingBomberNotification', [startTime, teamIndex])

    def bomberDestruction(self, teamIndex):
        self.call_1('ui.bomberDestruction', [teamIndex])

    def onReportTargetInfo(self, message):
        pass

    def setModuleStates(self, states, isTarget = False):
        LOG_DEBUG('ui.setModuleStates', states, isTarget)
        if isTarget:
            self.call_1('hud.damagePanelUpdateTarget', states)
        else:
            self.call_1('hud.damagePanelUpdate', states)

    def initDamageScheme(self, scheme, isTarget = False):
        LOG_DEBUG('ui.initDamageScheme', scheme, isTarget)
        if isTarget:
            self.call_1('hud.initDamageSchemeTarget', scheme)
        else:
            self.call_1('hud.initDamageScheme', scheme)

    def setFireState(self, state):
        LOG_DEBUG('setFireState: hud.damagePanelFire', state)
        self.call_1('hud.damagePanelFire', state)

    def reportFire(self, msg, state):
        LOG_DEBUG('ui.reportFire', state)
        isEnabled = not EntityStates.inState(BigWorld.player(), EntityStates.DEAD)
        if state:
            self.call_1('hud.labelClearText', 'extinguishFire')
            if isEnabled:
                self.call_1('hud.labelSetText', TextLabel('fire', msg))
        else:
            self.call_1('hud.labelClearText', 'fire')
            if isEnabled:
                self.call_1('hud.labelSetText', TextLabel('extinguishFire', msg))

    def onPartFlagSwitchedNotification(self, msg, messageType):
        self.call_1('hud.messageDamage', msg, int(messageType))

    def onPlayerChangeSpeakIconState(self, avatarId, iconID, muted):
        iconID, animate = {VOIP_ICON_TYPES.NONE: (VOIP_ICON_TYPES_ARENA.NONE, False),
         VOIP_ICON_TYPES.DISCONNECTED: (VOIP_ICON_TYPES_ARENA.DISCONNECTED, False),
         VOIP_ICON_TYPES.LISTENING: (VOIP_ICON_TYPES_ARENA.NONE, False),
         VOIP_ICON_TYPES.ARENA_CHANNEL_TALKING: (VOIP_ICON_TYPES_ARENA.ARENA_CHANNEL, True),
         VOIP_ICON_TYPES.SQUAD_CHANNEL_TALKING: (VOIP_ICON_TYPES_ARENA.SQUAD_CHANNEL, True),
         VOIP_ICON_TYPES.SQUAD_CHANNEL: (VOIP_ICON_TYPES_ARENA.SQUAD_CHANNEL, False),
         VOIP_ICON_TYPES.ARENA_CHANNEL: (VOIP_ICON_TYPES_ARENA.ARENA_CHANNEL, False),
         VOIP_ICON_TYPES.MUTED: (VOIP_ICON_TYPES_ARENA.MUTED, False),
         VOIP_ICON_TYPES.UNAVAILABLE: (VOIP_ICON_TYPES_ARENA.UNAVAILABLE, False)}.get(iconID, (None, False))
        if iconID is not None:
            LOG_TRACE('calling hud.playerListUpdateSpeaker with args: ', avatarId, iconID, animate)
            self.call_1('hud.playerListUpdateSpeaker', avatarId, iconID, animate)
        else:
            LOG_ERROR('onPlayerChangeSpeakIconState: invalid icon ID', iconID)
        self.call_1('hud.playerListSetMuted', avatarId, bool(muted))
        return

    def __requestMutePlayer(self, avatarId, mute):
        VOIP.api().setAvatarMuted(avatarId, mute)

    def __onGetActiveQuest(self):
        LOG_DEBUG('UI hud, __onGetActiveQuest')
        import BWPersonality
        questSelected = BWPersonality.g_questSelected
        if questSelected and questSelected.isDataFull():
            self.__onQuestSelectUpdate()
        else:
            GameEnvironment.getHUD().getActiveQuest()

    def __onQuestSelectUpdate(self):
        questCondErr = QUEST_CONDITION_ERROR.ALLOWED
        import BWPersonality
        if BWPersonality.g_questSelected.quests:
            if BigWorld.player().battleType == ARENA_TYPE.JAPANESE_THREAT:
                questCondErr = QUEST_CONDITION_ERROR.JAPANESE
            elif BigWorld.player().battleType != ARENA_TYPE.NORMAL:
                questCondErr = QUEST_CONDITION_ERROR.WRONG_BATTLE_TYPE
            elif BigWorld.player().settings.airplane.level < COMPLEX_QUEST_MIN_PLANE_LEVEL:
                questCondErr = QUEST_CONDITION_ERROR.WRONG_PLANE_LEVEL
        LOG_DEBUG('UI hud, __onQuestSelectUpdate', BWPersonality.g_questSelected.quests, questCondErr)
        self.call_1('hud.setActiveQuest', BWPersonality.g_questSelected.quests.values(), questCondErr)

    def __updateLocalizedPlanesName(self):
        owner = BigWorld.player()
        data = GameEnvironment.getClientArena().avatarInfos
        playersList = []
        for avatarInfo in data.values():
            playerStatRecord = PlayerStatRecord(avatarInfo, owner, True)
            if SUPERIORITY2_BASE_HEALTH and playerStatRecord.isBot:
                continue
            playersList.append(playerStatRecord)

        LOG_DEBUG('hud.playerListUpdateStatsBatch', playersList)
        self.call_1('hud.playerListUpdateStatsBatch', playersList)

    def onEnterOptions(self):
        self.__isOptionVisible = True
        from gui.WindowsManager import g_windowsManager
        g_windowsManager.showOptions()

    def onCloseOptions(self):
        self._ms = MeasurementSystem()
        if self._modalScreen:
            self._modalScreen.closeFlash()
        if GameEnvironment.getInput() is not None:
            GameEnvironment.getInput().forceRefreshButtons([InputMapping.CMD_HELP])
        self.__isOptionVisible = False
        from gui.WindowsManager import g_windowsManager
        g_windowsManager.hideOptions()
        return

    def __onHelpClose(self):
        GameEnvironment.getHUD().onHelpClose()

    def onHelp(self):
        vo, keys = self.__help.getData()
        GameEnvironment.getHUD().onHelpUI(True)
        self.call_1('help.setButtonsText', vo, keys)

    def showMessageCameraLocked(self, show, keyName):
        if show:
            messageStr = localizeHUD('ui_camera_locked').format(key=keyName)
            self.call_1('hud.labelSetText', TextLabel('cameraLocked', messageStr))
        else:
            self.call_1('hud.labelClearText', 'cameraLocked')

    def hideTutorial(self):
        """
        Hide tutorial screen
        """
        self.call_1('hud.hideTutorial')

    def showTutorial(self):
        """
        Init tutorial screen
        """
        self.call_1('hud.showTutorial')

    def clearTutorial(self):
        """
        Clears tutorial screen
        """
        self.call_1('hud.clearTutorial')

    def showTutorialResult(self):
        """
        Init tutorial result screen
        """
        self.__isResultScreenTutorial = True
        self.call_1('hangar.showTutorial')

    def setTutorialResult(self, params):
        """
        fill tutorial result screen
        """
        self.call_1('hangar.tutorialSetProperties', params)

    def showHintTutorial(self, tutorialHintParams):
        """
        Show localized tutorial hint
        @param tutorialHintParams: hint init params
        @type tutorialHintParams: TutorialHintParams
        """
        self.call_1('hud.showHintTutorial', tutorialHintParams)

    def showCaptionTutorial(self, tutorialCaptionParams):
        """
        Show localized tutorial caption(lesson brief)
        @param tutorialCaptionParams: tutorial caption init params
        @type tutorialCaptionParams: TutorialCaptionParams
        """
        self.call_1('hud.showCaptionTutorial', tutorialCaptionParams)

    def showHeaderTutorial(self, tutorialHeaderParams):
        """
        Show localized tutorial header(common text)
        @type tutorialHeaderParams: TutorialHeaderParams
        """
        self.call_1('hud.showHeaderTutorial', tutorialHeaderParams)

    def showTutorialOptions(self):
        self.call_1('settings.showNecessarySettings')

    def setTimerVisible(self, isVisible):
        """
        Hides/shows timer
        @param isVisible: hide or show
        @type isVisible: bool
        """
        self.call_1('hud.showTimer', isVisible)

    def resetTimer(self):
        """
        Reset timer
        """
        self.call_1('hud.resetTimer')

    def startTimer(self):
        """
        Start timer
        """
        self.call_1('hud.startTimer')

    def stopTimer(self):
        """
        Stop timer
        """
        self.call_1('hud.stopTimer')

    def getTimer(self):
        self.call_1('hud.getTimer')

    def updateBigTime(self, curTime):
        self.call_1('hud.bigTimerUpdateTime', curTime)
        GameSound().ui.play('UISoundTimerClock')

    def hideBigTime(self):
        self.call_1('hud.bigTimerHide')

    def showLimitArea(self, visible, width, height):
        """
        Shows limit area on screen
        @type visible: bool
        @param width: width of the area as a % of the screen width (from 0.0 to 1.0)
        @param height: height of the area as a % of the screen height (from 0.0 to 1.0)
        """
        self.call_1('hud.showLimitArea', visible, width, height)

    def showLimitAreaEx(self, visible, width, height, emptyWidth):
        """
        Shows limit area on screen
        @type visible: bool
        @param width: width of the area as a % of the screen width (from 0.0 to 1.0)
        @param height: height of the area as a % of the screen height (from 0.0 to 1.0)
        @param emptyWidth: with of the empty area as a % of the screen height (from 0.0 to 1.0)
        """
        self.call_1('hud.showLimitAreaEx', visible, width, height, emptyWidth)

    def rotateLimitAreaEx(self, angle):
        """
        @param angle: rotation angle (degrees)
        """
        self.call_1('hud.rotLimitAreaEx', angle)

    def rotateLimitArea(self, angle):
        """
        @param angle: rotation angle (degrees)
        """
        self.call_1('hud.rotLimitArea', angle)

    def showShadow(self, isVisible, isFadeIn = False):
        """
        Shadow screen
        @param isVisible:
        @param isFadeIn:
        """
        self.call_1('hud.showShadow', isVisible, isFadeIn)

    def showLowSpeedWarning(self, enable):
        if enable:
            vo = CustomObject()
            vo.id = 'speedlimit'
            vo.text = localizeTutorial('TUTORIAL_LESSON_1_WARNING_DONT_IDLE_ENGINE_ON_LOW_SPEED')
            self.call_1('hud.labelSetText', vo)
        else:
            self.call_1('hud.labelClearText', 'speedlimit')

    def showTutorialArrowPointer(self, enable):
        vo = CustomObject()
        vo.arrowPointer = enable
        self.call_1('hud.setElementsVisible', vo)

    def setTutorialArrowPointer(self, angle, distance):
        self.call_1('hud.showArrowPointerTutorial', angle, distance)

    def showTutorialMarkerPointer(self, enable):
        vo = CustomObject()
        vo.markerPointer = enable
        self.call_1('hud.setElementsVisible', vo)

    def showTutorialMarkerPointerMinimap(self, posX, posZ):
        hud = GameEnvironment.getHUD()
        if hud.minimap is not None and hud.minimap.isVisible():
            hud.minimap.removeAllMarkers()
            pMatrix = Math.Matrix()
            pMatrix.setTranslate((posX, 1.0, posZ))
            hud.minimap.addAnyObjectWithBlink(pMatrix, HUD_MINIMAP_ENTITY_TYPE_TUTORIAL_MARKER_POINTER, HUD_MINIMAP_ENTITY_GATE_MARKER_TUTORIAL, 2, 100000, True, True)
        return

    def setTutorialMarkerPointer(self, x, y, distance):
        self.call_1('hud.showMarkerPointerTutorial', x, y, distance)

    def showLimitAreaCircle(self, visible, x, y, width, height, angle = 0):
        """
        
        @param visible:
        @param x:
        @param y:
        @param width:
        @param height:
        @param angle:
        """
        self.call_1('hud.showLimitAreaCircle', visible, x, y, width, height, angle)

    def rotLimitAreaCircle(self, angle):
        """
        @param angle:
        """
        self.call_1('hud.rotLimitAreaCircle', angle)

    def isHitLimitAreaCircle(self, x, y):
        """
        Request to check that x, y position is in limit area
        @param x: in pixels
        @param y: in pixels
        """
        self.call_1('hud.isHitLimitAreaCircle', x, y)

    def setElementsVisible(self, params):
        """
        Set visible for hud elements
        @type params: ElementsVisibleParams
        """
        self.call_1('hud.setElementsVisible', params)
        vo = CustomObject()
        callStateUpdate = False
        if hasattr(params, 'weapon'):
            vo.weaponPanel = params.weapon
            callStateUpdate = True
        if hasattr(params, 'destroyInfo'):
            vo.battleMessagesMode = params.destroyInfo
            callStateUpdate = True
        if hasattr(params, 'healthMeter'):
            vo.healthMeter = params.healthMeter
            callStateUpdate = True
        if hasattr(params, 'forsage'):
            vo.forsage = params.forsage
            callStateUpdate = True
        if hasattr(params, 'playerList') and params.playerList:
            vo.playerList = 2
            callStateUpdate = True
        if hasattr(params, 'damagePanel'):
            vo.damagePanel = params.damagePanel
            callStateUpdate = True
        if hasattr(params, 'speedometer'):
            vo.speedometer = params.speedometer
            callStateUpdate = True
        if hasattr(params, 'variometer'):
            vo.variometer = params.variometer
            callStateUpdate = True
        if hasattr(params, 'aviahorizont') and Settings.g_instance.getGameUI()['horizon']:
            vo.aviahorizont = params.aviahorizont
            callStateUpdate = True
        if callStateUpdate:
            self.call_1('hud.updateState', vo)

    def showTutorialHintControl(self, funcString, params, enable):
        if enable:
            self.call_1(funcString, params)
        else:
            vo = CustomObject()
            vo.hintControl = False
            vo.hintResult = False
            self.call_1('hud.setElementsVisible', vo)

    def showTutorialShadowHintControls(self, params):
        self.call_1('hud.showShadowHintTutorial', params)

    def showTutorialShadowKillInfo(self, params):
        self.call_1('hud.showShadowPlayerList', params.avatarKiller != '', params.allyAvatarID, params.enemyAvatarID, params.avatarKiller)

    def showTutorialHighlightControls(self, params, color):
        self.call_1('hud.showBlinkingHighlight', params, 0, 0, color)

    def showTutorialHighlightTargetPoint(self, params, x, y):
        self.call_1('hud.showBlinkingHighlight', params, x, y)

    def setProgressBarValue(self, value, caption, segmentsNum):
        self.call_1('hud.updateProgressBar', value, caption, segmentsNum)

    def setTutorialAmmoLock(self, lockRockets, lockBombs, lockGuns):
        self.call_1('hud.setLockAmmo', lockRockets, lockBombs, lockGuns)

    def showHeaderMessage(self, title, message, duration = 0):
        vo = CustomObject()
        vo.headerMessages = 1
        self.call_1('hud.updateState', vo)
        self.call_1('hud.setHeaderMessages', title, message)
        if duration > 0:

            def hide():
                self.__headerMsgCallbackId = None
                self.hideHeaderMessage()
                return

            self.__headerMsgCallbackId = BigWorld.callback(duration, hide)

    def hideHeaderMessage(self):
        vo = CustomObject()
        vo.headerMessages = 0
        self.call_1('hud.updateState', vo)

    def uiCall(self, func, *methodArgs):
        self.call_1(func, *methodArgs)

    def uiCallTextLabel(self, labelId, text):
        self.call_1('hud.labelSetText', TextLabel(labelId, text))

    def uiClearTextLabel(self, labelId):
        self.call_1('hud.labelClearText', labelId)

    def onDevMenuEvent(self, VO):
        from debug.common import CustomMenu
        CustomMenu.debugMenuEvent(VO)

    def __replayInitHUD(self, maxTime, tips):
        self.call_1('hud.setEnableReplays')
        self.call_1('hud.setTimeMaxReplays', maxTime)
        self.call_1('hud.setToolTipsReplays', tips)

    def __replayShowPanel(self):
        self.call_1('hud.showPanelReplays')

    def __replayHidePanel(self):
        self.call_1('hud.hidePanelReplays')

    def __replayUpdateHUDProgress(self, curTime, rate):
        self.call_1('hud.setTimeCurrentReplays', curTime)
        self.call_1('hud.setProgressReplays', rate)

    def __replayUpdateHUDButtons(self, isPaused, playSpeed, btns):
        self.call_1('hud.setPauseReplays', not isPaused)
        self.call_1('hud.setSpeedReplays', playSpeed)
        self.call_1('hud.setButtonsEnableReplays', btns)

    def __replayShowMessage(self, message):
        self.call_1('hud.messageDamage', message, MESSAGE_TYPE_UI_COLOR_GREEN)

    def __replayShowFinish(self):
        self.call_1('hud.showCompletionMessage')
        self.__replayShowMessage(localizeHUD('REPLAY_MESSAGE_REPLAY_ENDED'))


def determinePlayerState(avatarInfo, ownerID):
    if avatarInfo['avatarID'] == ownerID:
        return 2
    stats = avatarInfo['stats']
    if stats['flags'] & AvatarFlags.LOST != 0:
        return 4
    elif stats['flags'] & AvatarFlags.LOADED != 0:
        return 1
    else:
        return 0


class PlayerStatRecordBase():

    def __init__(self, avatarInfo, owner):
        stats = avatarInfo['stats']
        self.ID = avatarInfo['avatarID']
        self.lives = stats['lifes']
        self.frags = stats['frags']
        self.fragsTeamObject = stats['fragsTeamObjects']
        self.isDead = stats['flags'] & AvatarFlags.DEAD != 0
        self.state = determinePlayerState(avatarInfo, owner.id)
        self.assists = stats['assists']
        self.assistsGround = stats['assistsGround']
        self.isTeamKiller = stats['flags'] & AvatarFlags.TEAM_KILLER != 0
        self.superiorityPoints = stats['score']


class PlayerStatRecord(PlayerStatRecordBase):

    def __init__(self, avatarInfo, owner, updateLanguage = False):
        PlayerStatRecordBase.__init__(self, avatarInfo, owner)
        settings = avatarInfo['settings']
        self.planeName = localizeAirplane(settings.airplane.name)
        if updateLanguage == False:
            serverTeamID = avatarInfo['teamIndex']
            self.isIgr = bool(avatarInfo['attrs'] & (ACCOUNT_ATTR.IGR_BASE | ACCOUNT_ATTR.IGR_PREMIUM))
            self.teamID = 0 if serverTeamID == owner.teamIndex else 1
            self.planeLevel = settings.airplane.level
            self.squadNumber = avatarInfo['squadID']
            self.squadType = SQUAD_TYPES.getSquadType(self.squadNumber, self.ID)
            self.planeType = settings.airplane.planeType
            self.planeNumber = avatarInfo['airplaneInfo']['decals'][4]
            self.isBot = avatarInfo['classID'] == EntitySupportedClasses.AvatarBot
            self.playerName = avatarInfo['playerName'] if not (self.isBot and GameEnvironment.getHUD().isTutorial()) else self.planeName
            self.playerClanAbbrev = avatarInfo['clanAbbrev'] if not (self.isBot and GameEnvironment.getHUD().isTutorial()) else ''
            self.planeIconPath = settings.airplane.hudIcoPath
            self.planeTypeIconPath = getHudPlaneIcon(settings.airplane.planeType)


class WeaponSlotRecordBase():

    def __init__(self, groupID, weaponData, gunsCount, correction, weaponGroupsCommands):
        self.id = groupID
        self.key = getKeyLocalization(weaponGroupsCommands.get(groupID - correction, InputMapping.CMD_PRIMARY_FIRE))
        if not self.key:
            self.key = getKeyLocalization(InputMapping.CMD_PRIMARY_FIRE)
        if weaponData['shellID'] != -1:
            self.key = getKeyLocalization(InputMapping.CMD_LAUNCH_ROCKET) if weaponData['shellIndex'] == SHELL_INDEX.TYPE1 else getKeyLocalization(InputMapping.CMD_LAUNCH_BOMB)


class WeaponSlotRecord(WeaponSlotRecordBase):

    def __init__(self, groupID, weaponData, gunsCount, correction, weaponGroupsCommands):
        WeaponSlotRecordBase.__init__(self, groupID, weaponData, gunsCount, correction, weaponGroupsCommands)
        description = weaponData['description']
        self.iconPath = description.hudIcoPath if weaponData['shellID'] != -1 else HUD_AMMO_BELTS_TYPE_ICO.get(weaponData['ammoBeltType'], description.hudIcoPath)
        self.iconEmptyPath = description.iconEmptyPath
        self.quantity = weaponData['initialCount']
        self.warningQuantity = weaponData.get('warningCount', -1)
        self.ammoBeltType = weaponData['ammoBeltType']
        if weaponData['shellID'] != -1:
            self.weaponType = UI.CONVERT_WEAPON_TYPES_TO_FLASH[weaponData['shellID']]
            self.caliber = localizeComponents('WEAPON_NAME_' + description.caliber)
        else:
            caliber = description.caliber
            self.weaponType = WEAPON_TYPES.GUN if caliber < 20 else WEAPON_TYPES.CANNON
            if caliber == int(caliber):
                caliber = int(caliber)
            self.caliber = str(gunsCount) + 'x' + str(caliber)