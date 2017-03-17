# Embedded file name: scripts/client/gui/hud.py
import functools
import math
import BigWorld
from Event import Event, EventManager
import GUI
import GameEnvironment
from EntityHelpers import EntityStates, isCorrectBombingAngle, isAvatar, getReductionPointVector, EntitySupportedClasses, isClientReadyToPlay
from GameServiceBase import GameServiceBase
import Math
from consts import *
from HUDconsts import *
import GUIHelper
import db.DBLogic
from gui.MiniScreen import *
import Keys
from MapBase import MarkerType, NavigationWindowsManager
from TeamObject import TeamObject
import ClientLog
from Map import Map
from Radar import Radar
from Minimap import Minimap
from consts import PART_FLAGS, CONSUMABLES_FOR_HAND_USE
from CrewHelpers import isCrewPart
from debug_utils import *
from gui.WindowsManager import g_windowsManager
from gui.Scaleform.windows import CustomObject
from HudElements.IngameChat import *
from HudElements.BombTarget import BombTarget
from HudElements.LandingPlace import LandingPlace
from HudElements.CollisionWarningSystem import CollisionWarningSystem
from HudElements.ForestallingPoint import ForestallingPoint, FP_STATES
from HudElements.IngameCursor import IngameCursor
import Cursor
from gui.Scaleform.utils.MeasurementSystem import MeasurementSystem
from Helpers.i18n import localizeMessages, localizeAirplane, localizeLobby, localizeAchievements, localizeTutorial
from gui.Scaleform.UI import HudStateType
import ResMgr
from clientConsts import WARNING_ALTITUDE_LEVEL, MIN_TARGET_SIZE, PLAYER_DETH, LOCALIZE_PLAYER_DETH_TABLE, MESSAGE_TYPE_UI_COLOR_YELLOW, MESSAGE_TYPE_UI_COLOR_GREEN, TARGET_RENDER_DISTANCE, OBJECTS_INFO, CombatScreenNames, NEUTRAL_OBJECTS_COMMAND_TEAM_INDEX, GUI_COMPONENTS_DEPH, TIME_FOR_SHOW_INTRO_HINT, OPTIMAL_HEIGHT_FOR_HINTS, DELAY_SHOW_DESTROYED_PLANE, DELAY_SHOW_DESTROYED_GROUNDOBJECT, COSUMABLES_FOR_HAND_USE_REPAIRING_MODULES, SPECTATOR_MODE_SCENARIO, NOT_CONTROLLED_MOD, TIME_FOR_HIDE_INTRO_HINT_BEFORE_START_BATTLE, PLANE_TYPE_NAME_HINTS, LOCAL_HOLIDAYS_MATRIX
from gui.Scaleform.UIHelper import SQUAD_TYPES, getTargetHealth, getTargetHealthPrc, EQUIPMENT_STATES, getKeyLocalization, getCalculatedBalanceCharacteristic, getPlayerNameWithClan, getTeamObjectType, getProjectiles
import InputMapping
from HudElements.GUICursor import *
from consts import OBJ_STATES
from gui.Scaleform.BattleLoading import BattleLoading
from gui.Scaleform.Help import Help, HelpSettingsKeys
from EntityHelpers import EntitySupportedClasses
from HelperFunctions import findIf
from Helpers.namesHelper import replaceTagChars
from Markers import Markers
from _preparedBattleData_db import preparedBattleData
import BattleReplay
import random
from EntityHelpers import AvatarFlags
from clientConsts import MARKERS_GROUP_ICON_TYPES, MARKERS_GROUP_ICON_INDEXES, MARKERS_GROUP_ICON_LOC_ID, PLANE_TYPE_ICO_PATH, DAMAGED_PARTS_TEAM_OBJECTS_CALLBACK_TIME
from Spectator import SpectatorStateDynamic, SpectatorModeDynamicCameraManager, SPECTATOR_MODE_STATES, SpectatorModeManager
from clientConsts import TEAM_OBJECTS_PARTS_TYPES, TARGET_PARTS_TYPES, FP_VISIBILITY_DISTANCE, COLLISION_WARNING_ANGLE
from gui.Scaleform.HUD.AwardManager import AwardManager
from gui.Scaleform.HUD.LeaderManager import LeaderManager
from gui.Scaleform.HUD.HintManager import HintManager
from gui.Scaleform.HUD.Counter import IncCounter
from gui.Scaleform.HUD.VehicleSwitcher import VehicleSwitchManager, VEHICLE_SWITCHER_DIRECTIONS
from gui.Scaleform.HUD.EquipmentManager import EquipmentManager
from Helpers.PerformanceSpecsHelper import getPerformanceSpecsDescriptions
from HUDHelpers import BattleMessageReactionHelper
from config_consts import IS_DEVELOPMENT
import _awards_data
from _consumables_data import ModsTypeEnum
from CameraStates import CameraState
from Helpers import AvatarHelper
from _skills_data import SkillDB, SpecializationEnum, SKILL_GROUP
from audio import GameSound
VISUAL_ENTITYES_CLASSES = TEAM_OBJECT_CLASS_NAMES + AVATAR_CLASS_NAMES + ['MapEntry']
ENTITY_COMMAND_CUT_TEXTURE_VECTORS = {ChatMessagesStringID.ENEMY_HERE: [Math.Vector2(0.0, 0.0), Math.Vector2(0.25, 0.5)],
 ChatMessagesStringID.ENEMY_MY_AIM: [Math.Vector2(0.25, 0.0), Math.Vector2(0.5, 0.5)],
 ChatMessagesStringID.GOT_IT: [Math.Vector2(0.5, 0.0), Math.Vector2(0.75, 0.5)],
 ChatMessagesStringID.JOIN_ME: [Math.Vector2(0.75, 0.0), Math.Vector2(1.0, 0.5)],
 ChatMessagesStringID.MY_LOCATION: [Math.Vector2(0.0, 0.5), Math.Vector2(0.25, 1.0)],
 ChatMessagesStringID.NEED_SHELTER: [Math.Vector2(0.25, 0.5), Math.Vector2(0.5, 1.0)],
 ChatMessagesStringID.FAILURE: [Math.Vector2(0.5, 0.5), Math.Vector2(0.75, 1.0)],
 ChatMessagesStringID.SOS: [Math.Vector2(0.75, 0.5), Math.Vector2(1.0, 1.0)]}
ENTITY_ARROWS_CUT_TEXTURE_VECTORS = {0: [Math.Vector2(0.25, 0.0),
     Math.Vector2(0.5, 0.5),
     Math.Vector2(0.0, 0.0),
     Math.Vector2(0.25, 0.5),
     Math.Vector2(0.0, 0.5),
     Math.Vector2(0.25, 1.0),
     Math.Vector2(0.25, 0.5),
     Math.Vector2(0.5, 1.0)],
 1: [Math.Vector2(0.75, 0.0),
     Math.Vector2(1.0, 0.5),
     Math.Vector2(0.5, 0.0),
     Math.Vector2(0.75, 0.5),
     Math.Vector2(0.5, 0.5),
     Math.Vector2(0.75, 1.0),
     Math.Vector2(0.25, 0.5),
     Math.Vector2(0.5, 1.0)]}

def normPrc(val, vmax):
    v = val * 100 / vmax
    if v > 100:
        v = 100
    if v < 0:
        v = 0
    return v


class WarningType:
    LOW_ALTITUDE = 0
    BORDER_TOO_CLOSE = 1
    STALL = 2
    AUTOPILOT = 3
    HEIGHT_SPEED = 4
    COLLISION_WARNING = 5


ACTIVE_COLOR = Math.Vector4(255, 255, 255, 255)
INACTIVE_COLOR = Math.Vector4(128, 128, 128, 64)

class SUPERIORITY_MSG_TYPES:
    DAMAGED = 0
    DESTRUCTION = 1


class _PerformanceSpecsDescriptions:

    def __init__(self, desc, hasRockets, hasBombs):
        self.desc = desc
        self.hasRockets = hasRockets
        self.hasBombs = hasBombs


class _Hints:

    def __init__(self, locText, imgPath, id):
        """
        @param <list>locText:
        @param <list>imgPath:
        @param <str>id:
        """
        self.locText = locText
        self.imgPath = imgPath
        self.id = id


class CentralHUD(object):

    class __CentralElement(object):

        def __init__(self, angle, texture):
            self.__angle = angle
            self.__guiElement = GUIHelper.createImage(texture, vAnchor='CENTER', hAnchor='CENTER', color=(255, 255, 255, 255))
            self.__guiElement.filterType = 'LINEAR'
            self.intencity = 0.0
            GUI.addRoot(self.__guiElement)

        def updateRingSize(self, hSize, vSize, mainPosition):
            delta = mainPosition - Math.Vector2(0.5 * BigWorld.screenWidth(), 0.5 * BigWorld.screenHeight())
            self.__guiElement.position = (math.sin(self.__angle) * hSize * 0.5 + 2.0 * delta.x / BigWorld.screenWidth(), math.cos(self.__angle) * vSize * 0.5 - 2.0 * delta.y / BigWorld.screenHeight(), 0)

        @property
        def intencity(self):
            return self.__intencity

        @intencity.setter
        def intencity(self, value):
            self.__intencity = value
            self.__guiElement.colour = ACTIVE_COLOR * value + INACTIVE_COLOR * (1.0 - value)

        @property
        def visible(self):
            return self.__guiElement.visible

        @visible.setter
        def visible(self, value):
            self.__guiElement.visible = value

    def __init__(self, f_getPosition = None):
        self.__visible = True
        self.__ringElements = []
        self.__mainPosition = f_getPosition
        self.right = self.__addRingElement(90.0, 'navigationGreenArrowRight_Selected.dds')
        self.up = self.__addRingElement(0, 'navigationGreenArrowUp_Selected.dds')
        self.left = self.__addRingElement(-90.0, 'navigationGreenArrowLeft_Selected.dds')
        self.down = self.__addRingElement(180.0, 'navigationGreenArrowDown_Selected.dds')
        self.right.intencity = 0.1
        self.up.intencity = 0.1
        self.left.intencity = 0.1
        self.down.intencity = 0.1
        self.updateSize()

    def __addRingElement(self, angleDegrees, texture):
        element = CentralHUD.__CentralElement(math.radians(angleDegrees), 'gui/circleHUD/test_croped/' + texture)
        self.__ringElements.append(element)
        return element

    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, value):
        self.__visible = value
        for element in self.__ringElements:
            element.visible = value

    def __setRingSize(self, hSize, vSize):
        for element in self.__ringElements:
            mp = self.__mainPosition() if self.__mainPosition is not None else Math.Vector2(0.5 * BigWorld.screenWidth(), 0.5 * BigWorld.screenHeight())
            element.updateRingSize(hSize, vSize, mp)

        return

    def updateSize(self):
        fov = BigWorld.projection().fov
        curZoomFactor = BigWorld.projection().fov / math.radians(60.0)
        mouseSealingZoneSizeDegrees = 19.0 * curZoomFactor
        vSize = math.tan(math.radians(mouseSealingZoneSizeDegrees)) / math.tan(fov / 2.0)
        vSize *= 2.0
        hSize = vSize * BigWorld.screenHeight() / BigWorld.screenWidth()
        self.__setRingSize(hSize, vSize)

    def setMouseRingSize(self, size):
        if size > 0.0:
            vSize = size / BigWorld.screenHeight() * 2.0
            hSize = vSize * BigWorld.screenHeight() / BigWorld.screenWidth()
            self.__setRingSize(hSize, vSize)


class EntityTypes:
    """
    use for EntitiesHud
    """
    UNKNOWN = -1
    AIRCRAFT_ENTITY = 0
    TEAM_OBJECT_ENTITY = 1
    POSITIVE_TARGET_OBJECT = 2
    AIRCRAFT_SQUAD_ENTITY = 3


class CenterPoint:

    def __init__(self):
        self.__dataProvider = None
        self.__ui = None
        self.__movie = None
        self.__matrixProvider = None
        return

    def init(self, ui, movie):
        self.__ui = ui
        self.__movie = movie
        self.__createScaleformMatrix(self.__matrixProvider)
        self.__matrixProvider = None
        return

    def __createScaleformMatrix(self, matrix):
        if matrix is not None:
            worldToclipMtxProvider = GUI.WorldToClipMP()
            worldToclipMtxProvider.target = matrix
            self.__dataProvider = GUI.ScaleformDataProvider(worldToclipMtxProvider, self.__movie, 'hud.centerPointUpdate', 'x;y;z;yaw;pitch;roll', '')
            self.__dataProvider.updateInterval = 1
        return

    def setMatrixProvider(self, matrixProvider):
        if self.__movie is not None:
            self.__createScaleformMatrix(matrixProvider)
        else:
            self.__matrixProvider = matrixProvider
        return

    def removeMatrixProvider(self):
        if self.__ui:
            self.__ui.call_1('hud.centerPointUpdate', 0, 0, 1, 0, 0, 0)
        self.__dataProvider = None
        self.__matrixProvider = None
        return


class MovingTarget:
    REDUCTION_POINT_OFFSET = Math.Vector3(0, -5, 0)

    def __init__(self, offsetMtx):
        self.__targetMatrix = offsetMtx
        self.__targetMatrix.source = BigWorld.player().realMatrix
        self.__targetMatrix.defaultLength = BigWorld.player().weaponsSettings.reductionPoint * HUD_REDUCTION_POINT_SCALE
        BattleReplay.g_replay.setPlaneAimMatrix(self.__targetMatrix)
        self.__dataProvider = None
        self.__active = False
        self.__valuesQueue = [0] * 10
        self.__valuesQueueIndex = 0
        self.__targetValue = 0
        self.__prevValue = 0
        self.__prevFov = 0
        self.__prevActive = 0
        self.__smoothStep = 0
        self.__minTargetSize = math.radians(MIN_TARGET_SIZE)
        return

    def getTargetMatrix(self):
        return self.__targetMatrix

    def init(self, movie):
        worldToclipMtxProvider = GUI.WorldToClipMP()
        worldToclipMtxProvider.target = self.__targetMatrix
        self.__dataProvider = GUI.ScaleformDataProvider(worldToclipMtxProvider, movie, 'hud.crosshairUpdate', 'x;y;z;yaw;pitch;roll', '')
        self.__dataProvider.updateInterval = 1

    def setSize(self, fov, size):
        self.__valuesQueue[self.__valuesQueueIndex] = size
        self.__valuesQueueIndex = (self.__valuesQueueIndex + 1) % 10
        newValue = sum(self.__valuesQueue) / 10
        if newValue != 0:
            newValue += self.__minTargetSize
        if newValue != self.__targetValue:
            self.__targetValue = newValue
            self.__smoothStep = (newValue - self.__prevValue if self.__prevValue < newValue else newValue - self.__prevValue) / 10
        if self.__prevValue != newValue or self.__prevFov != fov or self.__prevActive != self.__active:
            if abs(self.__prevValue - newValue) > 0.0001:
                newValue = self.__prevValue + self.__smoothStep
            ui = g_windowsManager.getBattleUI()
            self.__prevValue = newValue
            self.__prevFov = fov
            self.__prevActive = self.__active
            if self.__active and ui:
                ui.movingTargetSize(fov, newValue)

    def setTargetVisible(self, flag):
        self.__active = flag
        ui = g_windowsManager.getBattleUI()
        if ui:
            ui.movingTargetVisibility(flag)

    def isVisible(self):
        return self.__active


class PositionBlinkingUpdate:

    def __init__(self):
        self.__targetMatrix = None
        self.__dataProvider = None
        return

    def getTargetMatrix(self):
        return self.__targetMatrix

    def init(self, movie, fpMatrixProvider):
        self.__targetMatrix = fpMatrixProvider
        worldToclipMtxProvider = GUI.WorldToClipMP()
        worldToclipMtxProvider.target = self.__targetMatrix
        self.__dataProvider = GUI.ScaleformDataProvider(worldToclipMtxProvider, movie, 'hud.positionBlinkingUpdate', 'x;y;z;yaw;pitch;roll', '')
        self.__dataProvider.updateInterval = 1


class EnemyTurretsChecker:
    UPDATE_INTERVAL = 2
    WARNING_DISTANCE = 1400 * WORLD_SCALING

    def __init__(self):
        self.__list = {}
        self.__updateCallBack = None
        self.__readyToSpeech = True
        return

    def add(self, entity):
        self.__list[entity.id] = entity
        if not self.__updateCallBack:
            self.__update()

    def remove(self, entity):
        if entity.id in self.__list:
            del self.__list[entity.id]

    def __update(self):
        minDistance = None
        player = BigWorld.player()
        for entity in self.__list.values():
            dist = (entity.position - player.position).length
            if minDistance is None or dist < minDistance:
                minDistance = dist

        if minDistance != None and minDistance < self.WARNING_DISTANCE and EntityStates.inState(player, EntityStates.GAME):
            if self.__readyToSpeech:
                GameSound().voice.play('voice_damage_start')
                self.__readyToSpeech = False
        else:
            self.__readyToSpeech = True
        if len(self.__list) > 0:
            self.__setUpdateCallback()
        else:
            self.__updateCallBack = None
        return

    def __setUpdateCallback(self):
        self.__updateCallBack = BigWorld.callback(self.UPDATE_INTERVAL, self.__update)

    def destroy(self):
        if self.__updateCallBack:
            BigWorld.cancelCallback(self.__updateCallBack)
            self.__updateCallBack = None
        self.__list = {}
        return


class BattleQuest:

    def __init__(self, qId, qName = '', qDesc = '', qIsMain = False, qIsComplete = None):
        self.id = qId
        self.name = qName
        self.desc = qDesc
        self.isMain = qIsMain
        self.isComplete = qIsComplete


class SelectedComplexQuest:

    def __init__(self, qId):
        self.mainQuestId = qId
        self.quests = {}

    def isDataFull(self):
        for qId, qData in self.quests.iteritems():
            if qData.desc == '' or qData.isComplete is None:
                return False

        return True


class HUD(GameServiceBase):

    def __init__(self):
        super(HUD, self).__init__()
        self.__bombGroups = list()
        self.__markers = Markers()
        self.__matrixForMarkersGroup = list()
        self.__createEvents()
        self.__vehicleSwitchManager = VehicleSwitchManager()
        self.__leaderManager = LeaderManager()
        self.__awardManager = AwardManager()
        self.__equipmentManager = EquipmentManager(self.isEquipmentEnabledForUse)
        self.__hintManager = HintManager()
        self.__skipIntroCounter = IncCounter(Settings.g_instance.preIntroCount, self.__skipIntroFireCallback, self.__skipIntroFinishCallback)
        self.__introHintCallback = None
        self.__needRefreshObserverInfo = False
        self.__arenaBounds = None
        self.__navigationWindowsManager = NavigationWindowsManager()
        self.map = None
        self.minimap = None
        self.radar = None
        self.__bombTarget = None
        self.__collisionWarningSystem = None
        self.__miniScreenTargetID = None
        self.__isAllVisibleEntitiesCollected = False
        self.__stallSpeed = 0.0
        self.__criticalSpeed = 1000.0
        self.__battleUI = None
        self.__visible = False
        self.__forceHideHud = False
        self.__spectatorMode = False
        self.__chat = Chat()
        self.__attackRange = 0.0
        self.__gunAttackRange = -1.0
        self.__locDistUnit = MeasurementSystem().localizeHUD('ui_meter')
        self.__lastPartStates = {}
        self.__lastPartStatesTarget = {}
        self.lastAmmoCounters = {}
        self.__miniScreen = None
        self.__updateCallBack = -1
        self.__update1secCallBack = -1
        self.__timerUpdateEnabled = True
        self.__targetEntity = None
        self.__airHorizonUpdater = None
        self.__warningIndicators = {}
        self.__updateMouseRingSize()
        self.__centralHUD = None
        self.__shellDescriptions = {LAUNCH_SHELL_RESULT_EMPTY: {UPDATABLE_TYPE.ROCKET: 'ui_no_rockets',
                                     UPDATABLE_TYPE.BOMB: 'ui_no_bombs'},
         LAUNCH_SHELL_RESULT_DISABLED: {UPDATABLE_TYPE.ROCKET: 'UI_DISABLED_ROCKETS',
                                        UPDATABLE_TYPE.BOMB: 'UI_DISABLED_BOMBS'},
         LAUNCH_SHELL_RESULT_INCORRECT_ANGLE: {UPDATABLE_TYPE.ROCKET: 'UI_LARGE_ROLL',
                                               UPDATABLE_TYPE.BOMB: 'UI_LARGE_ROLL'}}
        self.__shellDescriptionsSpeech = {LAUNCH_SHELL_RESULT_EMPTY: {UPDATABLE_TYPE.ROCKET: 'voice_no_rockets',
                                     UPDATABLE_TYPE.BOMB: 'voice_no_bombs'},
         LAUNCH_SHELL_RESULT_INCORRECT_ANGLE: {UPDATABLE_TYPE.ROCKET: '',
                                               UPDATABLE_TYPE.BOMB: 'voice_no_bombing'}}
        self.__chatVisible = False
        self.__helpVisible = False
        self.__teamsVisible = False
        self.__offsetMtx = GUI.OffsetMp()
        self.__forestallingPoint = ForestallingPoint(int(Settings.g_instance.getGameUI()['alternativeColorMode']), self.__offsetMtx)
        self.__forestallingPoint.eChangeDistState += self.__eFPChangeDistState
        self.__entitiesHudCounter = 1073741825
        self.__entityesHudVisible = True
        self.__forestallingPointVisible = False
        self.__minimapVisible = True
        self.__radarVisible = True
        self.__centralHudVisible = False
        self.__miniScreenVisibility = None
        self.TEAM_OBJECT_SUPERIORITY_DATA_CENTER = {SUPERIORITY_MSG_TYPES.DAMAGED: {TYPE_TEAM_OBJECT.SMALL: 'HUD_MESSAGE_WE_DESTROYED_ENEMY_BUILDING_SUP2',
                                         TYPE_TEAM_OBJECT.BIG: 'HUD_MESSAGE_WE_DESTROYED_ENEMY_BASE_SUP2',
                                         TYPE_TEAM_OBJECT.CANNON: 'ui_downed_cannon',
                                         TYPE_TEAM_OBJECT.TURRET: 'HUD_MESSAGE_WE_DESTROYED_ENEMY_TURRET_SUP2',
                                         TYPE_TEAM_OBJECT.VEHICLE: 'HUD_MESSAGE_WE_DESTROYED_ENEMY_VEHICLE_SUP2'},
         SUPERIORITY_MSG_TYPES.DESTRUCTION: {TYPE_TEAM_OBJECT.SMALL: 'UI_DOWNED_GROUND_OBJECT_SUP2',
                                             TYPE_TEAM_OBJECT.BIG: 'UI_DOWNED_BASE_OBJECT_SUP2',
                                             TYPE_TEAM_OBJECT.CANNON: 'ui_downed_cannon',
                                             TYPE_TEAM_OBJECT.TURRET: 'UI_DOWNED_GROUND_OBJECT_SUP2',
                                             TYPE_TEAM_OBJECT.VEHICLE: 'UI_DOWNED_GROUND_OBJECT_SUP2'}}
        self.TEAM_OBJECT_SUPERIORITY_DATA = {SUPERIORITY_MSG_TYPES.DAMAGED: {TYPE_TEAM_OBJECT.SMALL: 'HUD_MESSAGE_BUILDING_DAMAGED_SUP2_TOP',
                                         TYPE_TEAM_OBJECT.BIG: 'HUD_MESSAGE_BASE_DAMAGED_SUP2_TOP',
                                         TYPE_TEAM_OBJECT.CANNON: 'ui_downed_cannon',
                                         TYPE_TEAM_OBJECT.TURRET: 'HUD_MESSAGE_TURRET_DAMAGED_SUP2_TOP',
                                         TYPE_TEAM_OBJECT.VEHICLE: 'HUD_MESSAGE_VEHICLE_DAMAGED_SUP2_TOP'},
         SUPERIORITY_MSG_TYPES.DESTRUCTION: {TYPE_TEAM_OBJECT.SMALL: 'UI_DOWNED_GROUND_OBJECT_SUP2_TOP',
                                             TYPE_TEAM_OBJECT.BIG: 'UI_DOWNED_BASE_OBJECT_SUP2_TOP',
                                             TYPE_TEAM_OBJECT.CANNON: 'ui_downed_cannon',
                                             TYPE_TEAM_OBJECT.TURRET: 'UI_DOWNED_TURRET_SUP2_TOP',
                                             TYPE_TEAM_OBJECT.VEHICLE: 'UI_DOWNED_GROUND_OBJECT_SUP2_TOP'}}
        self.TEAM_OBJECT_BASE_UNDER_ATTACK_DATA = {TYPE_TEAM_OBJECT.BIG: ['HUD_ENEMY_BASE_ATACKED', 'HUD_OWN_BASE_ATACKED']}
        self.__isEngineOverheated = False
        self.__isMapCreated = False
        self.CHAT_COMMANDS_MESSAGES = {InputMapping.CMD_F2_CHAT_COMMAND: ChatMessagesStringID.GOT_IT,
         InputMapping.CMD_F3_CHAT_COMMAND: ChatMessagesStringID.FAILURE,
         InputMapping.CMD_F4_CHAT_COMMAND: ChatMessagesStringID.NEED_SHELTER,
         InputMapping.CMD_F5_CHAT_COMMAND: ChatMessagesStringID.SOS,
         InputMapping.CMD_F6_CHAT_COMMAND: ChatMessagesStringID.MY_LOCATION,
         InputMapping.CMD_F7_CHAT_COMMAND: ChatMessagesStringID.ENEMY_HERE,
         InputMapping.CMD_F8_CHAT_COMMAND: ChatMessagesStringID.JOIN_ME,
         InputMapping.CMD_F9_CHAT_COMMAND: ChatMessagesStringID.ENEMY_MY_AIM}
        self.CHAT_COMMANDS_MESSAGES_REVERTED = dict(([v, k] for k, v in self.CHAT_COMMANDS_MESSAGES.items()))
        self.MARKER_MESSAGES_LOC_IDS = {GUICursorStates.NORMAL_OFF: 'HUD_MINIMAP_ATTENTION_STR',
         GUICursorStates.NORMAL_ON: 'HUD_MINIMAP_ATTENTION_STR',
         GUICursorStates.FRIENDLY: 'HUD_MINIMAP_ATTENTION_MY_LOCATION_STR',
         GUICursorStates.ENEMY: 'HUD_MINIMAP_ATTENTION_ENEMY_HERE_STR'}
        self.__guiCursor = GUICursor(GUICursorStates.NORMAL_OFF)
        self.__flapsState = 0
        self.__isCorrectBombingAngle = None
        self.__entityCommands = dict()
        self.__entityCommandCallBacks = {}
        self.__chatCommandLastExecuteTime = 0
        self.__isFire = False
        self.__crewParts = []
        self.__playerFragsSpeeches = ('voice_frag_first', 'voice_frag_second', 'voice_frag_third', 'voice_frag_fourth', 'voice_frag_fifth', 'voice_frag_next')
        self.lastDamageType = TUTORIAL_AVATAR_DESTROYED_REASON.NONE
        self.__battleLoading = BattleLoading()
        self.__battleLoading.onDispossed += self.__battleLoadingDispossed
        self.__minimapSize = None
        self.__entityList = dict()
        self.__enemyTurretsChecker = EnemyTurretsChecker()
        self.__speechFirstEnemyContact = True
        self.__clearTargetCallback = 0
        self.__visibleBombing = True
        self.__arenaLoaded = False
        self.__entityesHud = None
        self.__seaLevel = None
        InputMapping.g_instance.onProfileLoaded += self.__inputProfileChanged
        self.__installedParts = None
        self.__installedPartsTarget = None
        self.__smm = SpectatorModeManager()
        self.__smDynamicCameraManager = SpectatorModeDynamicCameraManager()
        self.__smm.eSetState += self.__onSpectatorModeSetState
        self.__isBattleLoadingVisible = True
        self.__teamObjectsGroups = dict()
        self.__outroCallback = None
        self.__outroTime = OUTRO_TIME
        self.__damagedPartsTeamObjectsCallbacks = dict()
        self.__performanceSpecsDescriptions = dict()
        self.getActiveQuest()
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

    def __createEvents(self):
        self.__eventManager = EventManager()
        em = self.__eventManager
        self.eAddEntity = Event(em)
        self.eRemoveEntity = Event(em)
        self.eDestruction = Event(em)
        self.eUpdateEnemyPositions = Event(em)
        self.eSetTargetEntity = Event(em)
        self.eUpdate1sec = Event(em)
        self.eUpdateTimer = Event(em)
        self.ePartStateChanging = Event(em)

    def afterLinking(self):
        super(HUD, self).afterLinking()
        self.__movingTarget = MovingTarget(self.__offsetMtx)
        self.__centerPoint = CenterPoint()
        if self.isTutorial():
            self.__positionBlinkingUpdate = PositionBlinkingUpdate()
        targetMatrix = GUI.OffsetMp()
        targetMatrix.source = BigWorld.player().realMatrix
        targetMatrix.defaultLength = BigWorld.player().weaponsSettings.reductionPoint * HUD_REDUCTION_POINT_SCALE
        self.__cursor = IngameCursor(targetMatrix)
        self.__entityesHud = GUI.EntitiesHud()
        self.__loadEntityColorScheme()
        self.__entityesHud.materialFX = 'BLEND'
        self.__entityesHud.entityRectTexture = BigWorld.PyTextureProvider(db.DBLogic.g_instance.getGUITexture('TX_HIGHLIGHT_SQUARE_ROUND'))
        self.__entityesHud.entityArrowTexture = BigWorld.PyTextureProvider(db.DBLogic.g_instance.getGUITexture('TX_ARROW_MARKER'))
        self.__entityesHud.entityCommandTexture = BigWorld.PyTextureProvider(db.DBLogic.g_instance.getGUITexture('TX_ENTITY_COMMANDS'))
        self.__entityesHud.entityCommandPositionOffset = ENTITY_COMMAND_POSITION_OFFSET
        self.__entityesHud.entityCommandTextureScale = ENTITY_COMMAND_TEXTURE_SCALE
        self.__entityesHud.targetMatrix = self.__movingTarget.getTargetMatrix()
        self.__entityesHud.sourceMatrix = BigWorld.player().realMatrix
        self.__entityesHud.py_callback_entity_select = self.__selectEntity
        self.__entityesHud.py_callback_entity_locked = self.__updateTargetLock
        self.__entityesHud.targetRenderDistance = DIST_FOR_NEXT_TARGETS * WORLD_SCALING
        self.__entityesHud.setSelectEntityData(RATIO_POTENTIAL_TARGETS, R_OUTSIDE_PRC, R_INSIDE_PRC, DIST_FOR_SELECT_TARGETS * WORLD_SCALING, FP_VISIBILITY_DISTANCE.get(BigWorld.player().settings.airplane.level) * WORLD_SCALING, self.__movingTarget.getTargetMatrix().defaultLength)
        self.__inputProfileChanged()
        selectedEntityTlUV, selectedEntityBrUV, enemyEntityTlUV, enemyEntityBrUV, squadEntityTlUV, squadEntityBrUV, allyEntityWithCommandTlUV, allyEntityWithCommandBrUV = ENTITY_ARROWS_CUT_TEXTURE_VECTORS[int(Settings.g_instance.getGameUI()['alternativeColorMode'])]
        self.__entityesHud.setEntityArrowUV(selectedEntityTlUV, selectedEntityBrUV, enemyEntityTlUV, enemyEntityBrUV, squadEntityTlUV, squadEntityBrUV, allyEntityWithCommandTlUV, allyEntityWithCommandBrUV)
        self.__centralHUD = CentralHUD(self.__cursor.getCursorScreenPositionSource)
        self.__centralHUD.visible = False
        GUI.addRoot(self.__entityesHud)
        self.__initBombTarget()
        self.__createMaps()
        self.__isMapCreated = True

    def destroy(self):
        self.__eventManager.clear()
        self.stop()
        super(self.__class__, self).destroy()

    def onGameChatEnabled(self, isEnabled):
        LOG_TRACE('onGameChatEnabled', isEnabled)
        self.__getBattleUI().chatUpdateStatus()

    def onMeasurementSystemChanged(self, measurementSystemIndex):
        ms = MeasurementSystem()
        self.__locDistUnit = ms.localizeHUD('ui_meter')
        gunAttackRange = ms.getMeters(self.gunAttackRange / WORLD_SCALING)
        self.uiCall('hud.initEffectiveShootingDist', round(gunAttackRange, 2))

    @property
    def movingTarget(self):
        return self.__movingTarget

    def centerPoint(self):
        return self.__centerPoint

    @property
    def positionBlinkingUpdate(self):
        return self.__positionBlinkingUpdate

    @property
    def centralHUDVisible(self):
        return self.__centralHudVisible

    @centralHUDVisible.setter
    def centralHUDVisible(self, value):
        self.__centralHudVisible = value
        self.__centralHUD.visible = self.__centralHudVisible and self.__visible and self.isBattleLoadingDispossessed()

    @property
    def centralHUD(self):
        return self.__centralHUD

    def __loadEntityColorScheme(self):
        for schemeName, entityColorSchemes in db.DBLogic.g_instance.getEntityColorSchemes().iteritems():
            for entityColorScheme in entityColorSchemes:
                self.__entityesHud.addColorPoint(schemeName, entityColorScheme.distance, entityColorScheme.color, entityColorScheme.scale, entityColorScheme.arrowAlpha)

    def __updateMouseRingSize(self):
        pass

    def __initBombTarget(self):
        self.__bombTarget = BombTarget()
        shellsInitialInfo = BigWorld.player().controllers['shellController'].getShellGroupsInitialInfo()
        for groupID, weaponData in shellsInitialInfo.items():
            if weaponData['shellID'] == UPDATABLE_TYPE.BOMB and weaponData['description'] is not None:
                self.__bombGroups.append(groupID)

        return

    def __updateTargets(self):
        self.__entityesHud.maxAutogliderDistance = self.__attackRange
        self.__entityesHud.maxAutogliderAngle = math.radians(360.0)
        if self.__isMapCreated:
            dispersionAngle = BigWorld.player().controllers['weapons'].getMaxVibroDispersionAngle()
            self.__movingTarget.setSize(GameEnvironment.getCamera().getFOV(), dispersionAngle)

    def initBattleResult(self):
        ui = self.__getBattleUI()
        if ui:
            ui.initBattleResult()

    def setBombTargetVisible(self, visible):
        visible = visible and self.__isAmmoBomrs() and EntityStates.inState(BigWorld.player(), EntityStates.GAME)
        self.__bombTarget.setVisible(visible)
        if visible:
            dispersionAngle = BigWorld.player().controllers['shellController'].getBombDispersionAngle()
            self.__bombTarget.setBombDispersionParams(dispersionAngle)

    def getBombTargetVisible(self):
        return self.__bombTarget.getBombTargetEnable()

    def __createMaps(self):
        arenaType = db.DBLogic.g_instance.getArenaData(BigWorld.player().arenaType)
        spaceName = arenaType.geometry
        self.map = Map(spaceName, self.sendMarkerMessage)
        self.minimap = Minimap(spaceName, self.sendMarkerMessage)
        self.radar = Radar(spaceName)
        self.__navigationWindowsManager.addNavigationWindow(self.map)
        self.__navigationWindowsManager.addNavigationWindow(self.minimap)
        self.__navigationWindowsManager.addNavigationWindow(self.radar)
        self.__navigationWindowsManager.setBeamMatrix(BigWorld.player().mapMatrix)
        self.minimap.map.radar = self.radar.map
        self.minimap.eMinimapResized = self.onMinimapResized
        self.map.map.radar = self.radar.map
        self.setRadarViewpoint(BigWorld.player().mapMatrix)
        LOG_INFO('HUD::__createMaps')

    def setRadarViewpoint(self, vpMtx):
        self.radar.map.viewpoint = vpMtx

    @staticmethod
    def getPreloadedResources():
        resourceList = []
        resourceList += Minimap.getPreloadedResources()
        resourceList += Map.getPreloadedResources()
        resourceList += Radar.getPreloadedResources()
        resourceList += [BOMB_SIGN_VISUAL, BOMB_SIGN_DISABLED_VISUAL, LandingPlace.LANDING_POINT_VISUAL]
        resourceList += ForestallingPoint.getPreloadedResources()
        return resourceList

    def onRecreateDevice(self):
        if self.__miniScreen:
            self.__miniScreen.updatePosition()
        if self.__centralHUD:
            self.__centralHUD.updateSize()

    def onOpenChat(self):
        """
        from flash mouse click event
        """
        self.onVisibilityChat(False)

    def onVisibilityChat(self, isNeedSend = True):
        LOG_DEBUG('onVisibilityChat')
        if not self.map.isVisible() and not self.__helpVisible and not self.__teamsVisible and not BattleReplay.isPlaying():
            self.__chatVisible = not self.__chatVisible
            self.uiCall('hud.onVisibilityChat', self.__chatVisible, isNeedSend)

    def onVisibilityTeams(self, visibleFlag):
        ui = self.__getBattleUI()
        if not self.map.isVisible() and not self.__helpVisible and ui and not self.__chatVisible:
            if visibleFlag != self.__teamsVisible:
                self.__teamsVisible = visibleFlag
                ui.onVisibilityTeams(visibleFlag)
                self.setVisibility(not visibleFlag)

    def onPlayerListChangeState(self):
        ui = self.__getBattleUI()
        if ui:
            settingsUI = Settings.g_instance.getGameUI()
            curPlayerListState = settingsUI['curPlayerListState']
            if curPlayerListState == settingsUI['minPlayerListState']:
                curPlayerListState = settingsUI['maxPlayerListState']
            else:
                curPlayerListState -= 1
            self.onSavePlayerListChangeState(curPlayerListState)
            self.onSetPlayerListChangeState(curPlayerListState)

    def onSetPlayerListChangeState(self, playerListState):
        self.uiCall('hud.playerListChangeState', playerListState)

    def onSavePlayerListChangeState(self, playerListState):
        Settings.g_instance.setGameUIValue('curPlayerListState', playerListState)

    def __skipIntroFireCallback(self, diff):
        Settings.g_instance.preIntroCount = diff

    def __skipIntroFinishCallback(self, diff):
        if Settings.g_instance.preIntroEnabled and not BattleReplay.isPlaying():
            self.__skipIntroFireCallback(diff)
            if BigWorld.player().arenaStartTime > 0 and int(round(BigWorld.player().arenaStartTime - BigWorld.serverTime())) > TIME_FOR_HIDE_INTRO_HINT_BEFORE_START_BATTLE:
                self.uiCall('hud.setVisibilitySkipIntroHint', True)
                self.__introHintCallback = BigWorld.callback(TIME_FOR_SHOW_INTRO_HINT, self.stopIntroHintCallback)

    def __clearSkipIntroHintCallback(self):
        if self.__introHintCallback is not None:
            self.uiCall('hud.setVisibilitySkipIntroHint', False)
            BigWorld.cancelCallback(self.__introHintCallback)
            self.__introHintCallback = None
        return

    def stopIntroHintCallback(self):
        clientStatsCollector = GameEnvironment.g_instance.service('ClientStatsCollector')
        if clientStatsCollector.getSkipIntro() != 1:
            clientStatsCollector.setSkipIntro(0 if Settings.g_instance.preIntroEnabled else -1)
        self.__clearSkipIntroHintCallback()

    def __skipIntroCommandEvent(self):
        clientStatsCollector = GameEnvironment.g_instance.service('ClientStatsCollector')
        clientStatsCollector.setSkipIntro(1 if Settings.g_instance.preIntroEnabled else -1)
        if EntityStates.inState(BigWorld.player(), EntityStates.PRE_START_INTRO) and self.__introHintCallback is not None:
            Settings.g_instance.preIntroEnabled = False
            self.__clearSkipIntroHintCallback()
        return

    def onHelpClose(self):
        self.__helpVisible = False
        commandProcessor = GameEnvironment.getInput().commandProcessor
        commandProcessor.getCommand(InputMapping.CMD_HELP).isFired = False

    def onHelp(self, fired):
        if self.onHelpUI(fired):
            self.uiCall('hud.onShowHelp', fired)

    def onHelpUI(self, fired):
        if not self.map.isVisible() and not self.__teamsVisible and not self.__chatVisible:
            if fired != self.__helpVisible:
                self.__helpVisible = fired
                return True
        return False

    def onVisibilityCursor(self, visibleFlag):
        ui = self.__getBattleUI()
        if ui:
            ui.onVisibilityCursor(visibleFlag)

    def setMinimapVisible(self, isVisible):
        """
        Set hud minimap visibility. Use this to make minimap visible even if hud was disabled
        @param isVisible:
        """
        self.__minimapVisible = isVisible
        self.__updateMinimapVisibility()

    def setRadarVisible(self, isVisible):
        """
        Set hud radar visibility.
        @param isVisible:
        """
        self.__radarVisible = isVisible
        self.__updateRadarVisibility()

    def setTargetPointerVisible(self, visible):
        """
        Set hud target pointer visibility. Use this to make target pointer visible even if hud was disabled
        @param visible:
        """
        self.__entityesHudVisible = visible
        self.__entityesHud.visible = visible
        self.__entityesHud.showArrows = visible

    def setForestallingPointVisible(self, isVisible):
        """
        Set hud forestalling point visibility. Use this to make point visible even if hud was disabled
        @param isVisible:
        """
        self.__forestallingPointVisible = isVisible
        self.__forestallingPoint.setVisible(self.__forestallingPointVisible)

    def disableForestallingPointForCurrentTarget(self):
        """
        Set forestalling point as disabled for current locked target
        """
        self.__forestallingPoint.setTarget(None)
        return

    def addTargetObject(self, matrix, entityType, isEnemy, color, isAlwaysVisible, timeForPotentialTargets):
        """
        Adds hud target pointer
        @param matrix: target matrix
        @type matrix: MatrixProvider
        @param entityType: 0 - Aircraft, 1 - Static object, 2 - positive target object
        @param isEnemy:
        @param color:
        @param isAlwaysVisible:
        @return: unique target id
        """
        self.__entitiesHudCounter += 1
        self.__entityesHud.addEntity(self.__entitiesHudCounter, matrix, entityType, isEnemy, color, isAlwaysVisible, timeForPotentialTargets)
        return self.__entitiesHudCounter

    def removeTargetObject(self, id):
        """
        Removes target pointer
        @param id:
        """
        self.__entityesHud.removeEntity(id)

    def isArrowPointerShown(self, entityId):
        """
        Indicating if hud arrow pointer could be shown for specific entity that was added using addEntity()
        or addTargetObject() functions
        @param entityId:
        @rtype: bool
        """
        return bool(self.__entityesHud.isArrowShownForEntity(entityId))

    def setEnableArrowsForAllEntities(self, isEnabled):
        self.__entityesHud.enableArrowsForAllEntities = isEnabled

    def onTutorialEnterState(self):
        self.setBombTargetVisible(self.__visibleBombing)

    def clear(self):
        res = []
        for id, en in self.entityList.iteritems():
            if isAvatar(en) and id != BigWorld.player().id:
                res.append(en)

        for en in res:
            self.removeEntity(en, True)

        self.clearTarget()
        self.__getBattleUI().call_1('hud.battleMessageClear')

    def addEntity(self, entity):
        if self.__isVisualEntity(entity):
            self.__markers.activateEntity(entity)
            if self.__isMapCreated and self.__isAllVisibleEntitiesCollected:
                self.eAddEntity(entity)
                self.__entityList[entity.id] = entity
                self.__updateObjectOnTheMap(entity, True)
                if entity.id != BigWorld.player().id:
                    color = self.__getEntityColor(entity, False)
                    entityType = issubclass(entity.__class__, TeamObject) and EntityTypes.TEAM_OBJECT_ENTITY or EntityTypes.AIRCRAFT_ENTITY
                    isEnemy = BigWorld.player().teamIndex != entity.teamIndex
                    if entityType == EntityTypes.AIRCRAFT_ENTITY and not isEnemy and SQUAD_TYPES.getSquadType(SQUAD_TYPES.getSquadIDbyAvatarID(entity.id), entity.id) == SQUAD_TYPES.OWN:
                        entityType = EntityTypes.AIRCRAFT_SQUAD_ENTITY
                    timeForPotentialTargets = TIME_FOR_POTENTIAL_TARGETS_AVATARS if isAvatar(entity) else TIME_FOR_POTENTIAL_TARGETS_TEAM_OBJECTS
                    self.__entityesHud.addEntity(entity.id, entity.matrix, entityType, isEnemy, color, True, timeForPotentialTargets)
                    if isEnemy:
                        if entityType == EntityTypes.AIRCRAFT_ENTITY:
                            if self.__speechFirstEnemyContact:
                                self.__speechFirstEnemyContact = False
                                if EntityStates.inState(BigWorld.player(), EntityStates.GAME):
                                    GameSound().voice.play('voice_appear_enemy')
                        elif getTeamObjectType(GameEnvironment.getClientArena(), entity.id) == TYPE_TEAM_OBJECT.TURRET:
                            self.__enemyTurretsChecker.add(entity)

    def removeEntity(self, entity, isLeaveWorld):
        self.__markers.deactivateEntity(entity)
        if self.__isMapCreated:
            if entity.id in self.__entityList:
                del self.__entityList[entity.id]
            if self.__enemyTurretsChecker:
                self.__enemyTurretsChecker.remove(entity)
            if entity is self.__targetEntity:
                if EntityStates.inState(entity, EntityStates.DESTROYED):
                    self.__setClearTargetCallback(entity)
                elif EntityStates.inState(entity, EntityStates.DESTROYED_FALL) and not isLeaveWorld:
                    if self.isTargetLock():
                        self.setTargetLock(False)
                else:
                    self.clearTarget()
            self.__updateObjectOnTheMap(entity, False)
            self.__entityesHud.removeEntity(entity.id)
            if self.__targetEntity is entity:
                self.__forestallingPoint.setTarget(None)
                self.__entityesHud.forestallingMatrix = None
        return

    def __updateObjectOnTheMap(self, entity, entityVisibility):
        clientArena = GameEnvironment.getClientArena()
        mapEntry = clientArena.getMapEntry(entity.id) if clientArena else None
        if not entityVisibility and EntityStates.inState(entity, EntityStates.DEAD | EntityStates.OBSERVER):
            self.removeEntityFromPlate(entity)
            if mapEntry:
                mapEntry.addedToPlate = False
        else:
            if mapEntry:
                mapEntry.inClientWorld = entityVisibility
                if not entityVisibility and mapEntry.isAlive and not EntityStates.inState(entity, EntityStates.PRE_START_INTRO):
                    mapEntry.setPositionAndYaw(Math.Vector3(entity.position.x, entity.position.y, entity.position.z), entity.yaw)
                self.updateObjectVisibility(mapEntry)
            if entityVisibility:
                self.addEntityToPlate(entity)
                if mapEntry:
                    mapEntry.addedToPlate = True
        return

    def updateObjectVisibility(self, obj):
        """
        use only for MapEntry objects!
        @param obj: <MapEntry>
        """
        if NEUTRAL_OBJECTS_COMMAND_TEAM_INDEX != obj.teamIndex:
            if obj.isAlive and not obj.inClientWorld:
                if obj.addedToPlate:
                    self.__updateEntityOnPlateMatrix(obj, obj.mapMatrix)
                else:
                    self.addEntityToPlate(obj)
                    obj.addedToPlate = True
            visible = obj.isAlive or obj.inClientWorld
            self.__navigationWindowsManager.setVisibility(obj, visible)
        else:
            LOG_DEBUG('updateObjectVisibility - object[%s] is not updated ' % obj.id)

    def __updateMatrixForMarkersGroup(self, entity, isVisible):
        if not SUPERIORITY2_BASE_HEALTH:
            return
        else:
            if self.__markers.initialized:
                mapEntry = GameEnvironment.getClientArena().getMapEntry(entity.id)
                if mapEntry:
                    matrix = mapEntry.mapMatrix
                    isTeamObject = mapEntry.classID in [EntitySupportedClasses.TeamTurret, EntitySupportedClasses.TeamObject, EntitySupportedClasses.TeamCannon]
                else:
                    isTeamObject = not isAvatar(entity)
                    matrix = entity.matrix
                if isTeamObject:
                    for groupName, groupEntities in self.__teamObjectsGroups.iteritems():
                        if entity.id in groupEntities:
                            self.__markers.setMatrix(groupName, entity.id, matrix if isVisible else None)
                            break

            else:
                self.__matrixForMarkersGroup.append((entity, isVisible))
            return

    def addEntityToPlate(self, entity):
        if NEUTRAL_OBJECTS_COMMAND_TEAM_INDEX != entity.teamIndex:
            self.__navigationWindowsManager.add(entity)
            self.__updateMatrixForMarkersGroup(entity, True)
        else:
            LOG_DEBUG('addEntityToPlate - object[%s] is not added to the map' % entity.id)

    def removeEntityFromPlate(self, entity):
        if NEUTRAL_OBJECTS_COMMAND_TEAM_INDEX != entity.teamIndex:
            self.__navigationWindowsManager.remove(entity)
            self.__updateMatrixForMarkersGroup(entity, False)
        else:
            LOG_DEBUG('removeEntityFromPlate - object[%s] is not removed from the map' % entity.id)

    def __updateEntityOnPlateMatrix(self, entity, matrix):
        if NEUTRAL_OBJECTS_COMMAND_TEAM_INDEX != entity.teamIndex:
            self.__navigationWindowsManager.setMatrix(entity, matrix)
        else:
            LOG_DEBUG('__updateEntityOnPlateMatrix - object[%s] is not updated Matrix' % entity.id)

    def onEntytiChangeHealth(self, entity, lastHealth):
        player = BigWorld.player()
        if entity.lastDamagerID == player.id:
            self.__entityesHud.blinkEntity(entity.id, HUD_HIHGHLIGHT_BLINK_COLOR, 0.2)
            if player.teamIndex != entity.teamIndex and entity.teamIndex <= 1:
                if isAvatar(entity):
                    if entity.lastDamageReason in (DAMAGE_REASON.BULLET, DAMAGE_REASON.ROCKET_EXPLOSION) and player.reportedDamagedEntityID != entity.id:
                        GameSound().voice.play('voice_hit_enemy')
                        player.reportedDamagedEntityID = entity.id
                elif entity.lastDamageReason in (DAMAGE_REASON.ROCKET_EXPLOSION, DAMAGE_REASON.BOMB_EXPLOSION):
                    GameSound().voice.play('voice_ground_target_hit')
            elif player.teamIndex == entity.teamIndex and isAvatar(entity) and player.reportedDamagedEntityID != entity.id:
                if entity.lastDamageReason == DAMAGE_REASON.BULLET:
                    curTime = BigWorld.time()
                    if player.reportedDamagedAllyTime + 2 < curTime:
                        GameSound().voice.play('voice_hit_ally')
                    player.reportedDamagedAllyTime = curTime
                elif entity.lastDamageReason == DAMAGE_REASON.RAMMING:
                    GameSound().voice.play('voice_ally_ram')
        if self.isTutorial():
            player.controllers['tutorialManager'].onEntityChangeHealth(entity, lastHealth)
        if entity.id == player.curVehicleID:
            self.updateHealth(entity.health, 0, entity.health)
        player.controllers['hintsManager'].onEntityChangeHealth(entity, lastHealth)

    def onTargetEntity(self, entity, replayMode = False):
        BattleReplay.g_replay.notifyTargetEntity(entity.id if entity else 0)
        if BattleReplay.isPlaying() and not replayMode:
            return
        else:
            player = BigWorld.player()
            state_DESTROYED = EntityStates.inState(player, EntityStates.DESTROYED)
            state_DESTROYED_FALL = EntityStates.inState(player, EntityStates.DESTROYED_FALL)
            if entity is not None and (state_DESTROYED or state_DESTROYED_FALL):
                return
            if not self.__spectatorMode:
                if not self.__miniScreen:
                    return
                self.__miniScreen.setTarget(entity)
                self.__miniScreen.update()
                ui = self.__getBattleUI()
                if ui and entity and isAvatar(entity):
                    ui.initDamageScheme(self.__getDamageScheme(entity), True)
                    self.__initInstalledParts(entity, True)
                    self.__lastPartStatesTarget.clear()
                    self.setModuleStates(None, entity.id, True)
                if self.__targetEntity:
                    self.__navigationWindowsManager.setLocked(self.__targetEntity, False)
                    if self.targetEntity.id in self.entityList:
                        self.__entityesHud.setEntityData(self.__targetEntity.id, self.__getEntityColor(self.__targetEntity, False), False)
                self.targetEntity = entity
                if entity is not None and EntityStates.inState(BigWorld.player(), EntityStates.GAME):
                    self.__forestallingPoint.setTarget(entity)
                    self.__entityesHud.forestallingMatrix = self.__forestallingPoint.matrixProvider
                    self.__navigationWindowsManager.setLocked(entity, True)
                    color = self.__getEntityColor(entity, True)
                    self.__entityesHud.setEntityData(entity.id, color, True)
                else:
                    self.__forestallingPoint.setTarget(None)
                    self.__entityesHud.forestallingMatrix = None
                self.__markers.selectTarget(self.targetEntity)
            return

    def __updateSpectatorText(self):
        owner = BigWorld.player()
        if owner.curVehicleID:
            entity = BigWorld.entities.get(owner.curVehicleID, None)
            if entity:
                self.updateHealth(entity.health, 0, entity.health)
        return

    def __getEntityColor(self, entity, isLocked):
        if isLocked:
            return HUD_HIGHLIGHT_LOCKED_COLOUR
        isEnemy = BigWorld.player().teamIndex != entity.teamIndex
        if issubclass(entity.__class__, TeamObject):
            return isEnemy and HUD_HIGHLIGHT_ENEMY_OBJECT_COLOUR or HUD_HIGHLIGHT_FRIEND_OBJECT_COLOUR
        elif isEnemy:
            return HUD_HIGHLIGHT_ENEMY_AIRCRAFT_COLOUR
        squadType = SQUAD_TYPES.getSquadType(SQUAD_TYPES.getSquadIDbyAvatarID(entity.id), entity.id)
        if squadType == SQUAD_TYPES.OWN:
            return HUD_HIGHLIGHT_SQUAD_AIRCRAFT_COLOUR
        else:
            return HUD_HIGHLIGHT_FRIEND_AIRCRAFT_COLOUR

    def __collectAllVisibleEntities(self):
        for entity in BigWorld.entities.values():
            if EntityStates.inState(entity, EntityStates.GAME | EntityStates.WAIT_START | EntityStates.PRE_START_INTRO):
                self.addEntity(entity)

    def __isVisualEntity(self, entity):
        return entity.__class__.__name__ in VISUAL_ENTITYES_CLASSES and entity.teamIndex != TEAM_ID.DECORATOR

    def onUpdatePlayerStats(self, avatarInfo):
        if BigWorld.player().battleType == ARENA_TYPE.PVE:
            self.__leaderManager.check()

    def doBattleUILoaded(self):
        if BigWorld.player().battleType == ARENA_TYPE.PVE:
            self.__leaderManager.initialized(self.__getBattleUI(), self.__chat)
            self.__hintManager.initialized(self.__markers, self.__getBattleUI(), self.movingTarget.getTargetMatrix(), self.__forestallingPoint.matrixProvider)
        self.__awardManager.initialized(self.__getBattleUI(), self.__chat)
        self.__equipmentManager.init(self.__getBattleUI())
        if self.minimap:
            self.__minimapSize = self.minimap.getMapSize()
            self.minimap.setMapSize(Settings.g_instance.getGameUI()['minimapSizeInBattleLoadingScreen'])
        if not self.__bombTarget:
            self.__initBombTarget()
        self.__getBattleUI().init(BigWorld.player().battleDuration)
        reserveEntitiesNum = 100
        self.lastAmmoCounters = {}
        self.onUpdateHUDSettings()
        self.__getBattleUI().reInit(True)
        self.__markers.rebuild()
        self.update()
        self.update1sec()
        self.updateUIWeaponRange(True)
        self.updateUIWeaponDispersion()
        mtxPlayer = BigWorld.player().realMatrix
        movie = self.__getBattleUI().movie
        self.__airHorizonUpdater = GUI.ScaleformDataProvider(mtxPlayer, movie, 'hud.aviahorizonUpdate', 'x;y;z;yaw;pitch;roll', '')
        self.__movingTarget.init(movie)
        self.__centerPoint.init(self.__getBattleUI(), movie)
        if self.isTutorial():
            self.__positionBlinkingUpdate.init(movie, self.__forestallingPoint.matrixProvider)
        self.__miniScreenLockTargetVisibility(False)
        clientArena = GameEnvironment.getClientArena()
        self.updateAmmoGroupCounters(BigWorld.player().getAmmoCountByGroup())
        self.forceUpdate(BigWorld.player().health, clientArena.getSortedAvatarInfosList())
        self.onPlayerAvatarChangeState(EntityStates.CREATED, BigWorld.player().state)
        if self.__collisionWarningSystem is None:
            self.__collisionWarningSystem = CollisionWarningSystem(self.__isCollisionWarning)
            self.__collisionWarningSystem.enabled(Settings.g_instance.getGameUI()['collisionWarningSystem'])
        self.onAlternativeColorModeEnabled(Settings.g_instance.getGameUI()['alternativeColorMode'])
        self.__getBattleUI().onUpdateDominationPrc(clientArena.dominationPrc)
        self.__getBattleUI().onUpdateTeamSuperiorityPoints(clientArena.superiorityPoints, clientArena.superiorityPoints[0], clientArena.superiorityPoints[1])
        MC_SCALE_NAME_FP = 'mcState'
        MC_ROOT_PATH_FP = '_root.mcInfoEntities.anticipationPoint'
        self.__forestallingPoint.addScaleformComponent(self.__getBattleUI().movie, MC_ROOT_PATH_FP, MC_SCALE_NAME_FP)
        BattleReplay.g_replay.onClientReady()
        return

    def __initInstalledParts(self, avatar = None, isTarget = False):
        if avatar is None:
            avatar = BigWorld.player()
        from db.DBParts import buildPresentPartsMap
        if isTarget:
            self.__installedPartsTarget = buildPresentPartsMap(avatar.settings.airplane.partsSettings, avatar.partTypes)
        else:
            self.__installedParts = buildPresentPartsMap(avatar.settings.airplane.partsSettings, avatar.partTypes)
        return

    def __getDamageScheme(self, avatar = None):
        if avatar is None:
            avatar = BigWorld.player()
        d = db.DBLogic.g_instance
        import _airplanesConfigurations_db
        aircraftConfig = _airplanesConfigurations_db.getAirplaneConfiguration(avatar.globalID)
        for module in aircraftConfig.modules:
            upgrade = d.upgrades.get(module, None)
            if upgrade is not None and upgrade.type == UPGRADE_TYPE.ENGINE:
                for v in upgrade.variant:
                    if v.aircraftName == avatar.settings.airplane.name:
                        if hasattr(v, 'damageSchema'):
                            return v.damageSchema
                        LOG_WARNING('__getDamageScheme - damageSchema can"t initialized for this plane', v.aircraftName)

        LOG_DEBUG('__getDamageScheme - result damageSchema is default = 1')
        return 1

    def onEntityChangeLastDamagerID(self, entity):
        if BigWorld.player().battleType == ARENA_TYPE.PVE:
            self.__hintManager.onEntityChangeLastDamagerID(entity)

    def __eFPChangeDistState(self, lastState, state):
        if state == FP_STATES.AIM:
            self.uiCall('hud.setFPState', FP_STATES.BIG_CIRCLE)
            aims = Settings.g_instance.getAimsData()
            isActive = True and aims['dynamycAim']
            self.uiCall('hud.setAimActive', isActive)
        else:
            self.uiCall('hud.setFPState', state)
            if lastState == FP_STATES.AIM:
                self.uiCall('hud.setAimActive', False)
        if BigWorld.player().battleType == ARENA_TYPE.PVE:
            self.__hintManager.onChangeDistState(self.__forestallingPoint.state)

    def __battleLoadingDispossed(self):
        self.__updateTimer(self.__getBattleUI())
        self.__isBattleLoadingVisible = False
        self.__getBattleUI().stopTickerNews()
        self.__battleLoading.onDispossed -= self.__battleLoadingDispossed
        import BattleReplay
        BattleReplay.g_replay.initPanelCallbacks()
        if self.minimap is not None and self.__minimapSize is not None:
            self.minimap.setMapSize(self.__minimapSize)
            if self.isTutorial():
                self.minimap.setDepth(GUI_COMPONENTS_DEPH.MINIMAP_IN_BATTLE_LOADING, True)
        self.__updateMinimapAndRadarVisibility()
        self.setTargetVisible(GameEnvironment.getCamera().zoomPresent() and EntityStates.inState(BigWorld.player(), EntityStates.WAIT_START | EntityStates.GAME | EntityStates.OBSERVER))
        if EntityStates.inState(BigWorld.player(), EntityStates.PRE_START_INTRO):
            GameEnvironment.getInput().inputAxis.notControlledByUser(False, NOT_CONTROLLED_MOD.AUTOPILOT)
        return

    def setBattleLoadingDisposeCondition(self, func):
        self.__battleLoading.setDisposeCondition(func)

    def collisionWarningSystemEnabled(self, flag):
        if self.__collisionWarningSystem is not None:
            self.__collisionWarningSystem.enabled(flag)
        return

    def __isCollisionWarning(self, flag):
        ui = self.__getBattleUI()
        if ui:
            ui.updateWarningIndicator(WarningType.COLLISION_WARNING, flag)

    def onAlternativeColorModeEnabled(self, flag):
        ui = self.__getBattleUI()
        if ui:
            ui.uiCall('hud.alternativeColor', flag)
        self.__navigationWindowsManager.setState(int(flag))
        self.__responseBattleHints()
        if self.__entityesHud is not None:
            selectedEntityTlUV, selectedEntityBrUV, enemyEntityTlUV, enemyEntityBrUV, squadEntityTlUV, squadEntityBrUV, allyEntityWithCommandTlUV, allyEntityWithCommandBrUV = ENTITY_ARROWS_CUT_TEXTURE_VECTORS[int(flag)]
            self.__entityesHud.setEntityArrowUV(selectedEntityTlUV, selectedEntityBrUV, enemyEntityTlUV, enemyEntityBrUV, squadEntityTlUV, squadEntityBrUV, allyEntityWithCommandTlUV, allyEntityWithCommandBrUV)
        return

    def onCombatInterfaceType(self, val):
        self.uiCall('hud.battleUIType', val)

    def initialData(self, data):
        self.__stallSpeed = data['stallSpeed']
        self.__criticalSpeed = data['criticalSpeed']
        if BigWorld.player().battleType == ARENA_TYPE.PVE:
            self.__hintManager.initialData(dict(stallSpeed=self.__stallSpeed))

    def stop(self):
        LOG_INFO('HUD::stop')
        Settings.g_instance.saveGameUI()
        InputMapping.g_instance.onProfileLoaded -= self.__inputProfileChanged
        self.__forestallingPoint.eChangeDistState -= self.__eFPChangeDistState
        self.__forestallingPoint.destroy()
        self.__forestallingPoint = None
        self.__vehicleSwitchManager.destroy()
        self.__leaderManager.destroy()
        self.__awardManager.destroy()
        self.__equipmentManager.destroy()
        self.__hintManager.destroy()
        self.__skipIntroCounter.destroy()
        self.__clearSkipIntroHintCallback()
        self.__markers.destroy()
        self.__markers = None
        self.__clearOutroCallback()
        if not self.__battleLoading.isDispossessed():
            self.__battleLoading.dispossess()
        if self.__entityesHud:
            self.__entityesHud.forestallingMatrix = None
            self.__entityesHud.py_callback_entity_select = None
            self.__entityesHud.py_callback_entity_locked = None
            self.__entityesHud = None
        self.__smm.destroy()
        self.__smm = None
        if self.__clearTargetCallback:
            BigWorld.cancelCallback(self.__clearTargetCallback)
        for senderID, callBack in self.__entityCommandCallBacks.items():
            BigWorld.cancelCallback(callBack)

        if self.__updateCallBack != -1:
            BigWorld.cancelCallback(self.__updateCallBack)
            self.__updateCallBack = -1
        if self.__update1secCallBack != -1:
            BigWorld.cancelCallback(self.__update1secCallBack)
            self.__update1secCallBack = -1
        self.__warningIndicators.clear()
        if self.__collisionWarningSystem is not None:
            self.__collisionWarningSystem.destroy()
        if self.__bombTarget:
            self.__bombTarget.destroy()
            self.__bombTarget = None
        if self.__miniScreen:
            self.__miniScreen.destroy()
            self.__miniScreen = None
        self.__navigationWindowsManager.destroy()
        if self.map:
            self.map.removeAllMarkers()
        self.map = None
        self.minimap = None
        self.radar = None
        self.__battleUI = None
        self.__airHorizonUpdater = None
        self.__movingTarget = None
        self.__centerPoint = None
        if self.isTutorial():
            self.__positionBlinkingUpdate = None
        return

    def battleStarted(self):
        self.setTargetVisible(GameEnvironment.getCamera().zoomPresent() and EntityStates.inState(BigWorld.player(), EntityStates.WAIT_START | EntityStates.GAME | EntityStates.OBSERVER))
        self.__awardManager.setEnabled(True)

    def changeWarningIndicator(self, id, v):
        if id not in self.__warningIndicators or self.__warningIndicators[id] != v:
            self.__warningIndicators[id] = v
            return True
        return False

    def testWarningIndicator(self, id):
        if id in self.__warningIndicators:
            v = self.__warningIndicators[id]
            if type(v) == bool:
                return v
            else:
                return v != 0
        return False

    def restart(self):
        self.__warningIndicators.clear()
        self.__markers.rebuild()
        self.updateHudElements()
        self.__smm.setState(SPECTATOR_MODE_STATES.OFF)
        ui = self.__getBattleUI()
        if ui:
            ui.restart()

    def forceUpdate(self, health, teamStats):
        ui = self.__getBattleUI()
        if ui:
            ui.forceUpdate(localizeHUD('HUD_WAITING4START_STR'), health, teamStats)

    def isFlashVisible(self):
        return not self.__forceHideHud

    def setFlashVisibility(self, flag):
        ui = self.__getBattleUI()
        if flag != self.__forceHideHud and ui:
            self.__forceHideHud = flag
            ui.setVisibility(not flag)

    def setCameraRingVisible(self, visible):
        ui = self.__getBattleUI()
        if ui:
            ui.setCameraRingVisible(visible)

    def setVisibility(self, flag):
        self.__visible = flag
        self.updateHudElements()
        self.setVisibleIngameCursor(flag)
        if not flag:
            self.map.setVisible(False)
            self.__miniScreenTargetID = None
        LOG_INFO('HUD visible %i' % self.__visible)
        return

    def isVisible(self):
        return self.__visible

    def reportBaseIsUnderAttack(self, objPos, objTeamIndex, objType):
        owner = BigWorld.player()
        isOwnObj = owner.teamIndex == objTeamIndex
        if isOwnObj:
            self.__navigationWindowsManager.setMarker(objPos.x, objPos.z, MarkerType.BASE_UNDER_ATTACK, MAP_BLINK_NUM)
        ui = self.__getBattleUI()
        if ui and objType in self.TEAM_OBJECT_BASE_UNDER_ATTACK_DATA:
            ui.updateAlert(localizeHUD(self.TEAM_OBJECT_BASE_UNDER_ATTACK_DATA[objType][int(isOwnObj)]), int(isOwnObj))

    def onPlayerAvatarChangeState(self, oldState, newState):
        LOG_INFO('HUD::onPlayerAvatarChangeState', EntityStates.getStateName(oldState), '->', EntityStates.getStateName(newState))
        self.setTargetVisible(GameEnvironment.getCamera().zoomPresent() and newState & (EntityStates.PRE_START_INTRO | EntityStates.WAIT_START | EntityStates.GAME | EntityStates.OBSERVER))
        if newState & EntityStates.DEAD and oldState & EntityStates.GAME:
            self.__onDestruction()
        if newState & EntityStates.OBSERVER and oldState & EntityStates.CREATED:
            self.__onDestruction()
            self.__setSpectatorMode(True)
            self.autoAlightFromDestroyedTransport()
        if oldState == EntityStates.PRE_START_INTRO:
            self.__markers.activateAll()
            if BigWorld.player().battleType == ARENA_TYPE.PVE and newState == EntityStates.GAME:
                self.__hintManager.start()
        self.__spawnedStatusChanged(newState & (EntityStates.GAME | EntityStates.WAIT_START | EntityStates.PRE_START_INTRO))
        if BigWorld.player().battleType == ARENA_TYPE.TRAINING and newState == EntityStates.END_GAME:
            self.__getBattleUI().updateHUDSettings()
            self.__getBattleUI().uiClearTextLabel('spectatorModeInfoAboutTypeDeath')
            self.__flapsChangeState(False, '')
            self.__smm.setState(SPECTATOR_MODE_STATES.INITIALIZED)
        elif newState == EntityStates.OUTRO:
            self.__initOutro()
        elif self.__smm.state != SPECTATOR_MODE_STATES.OUTRO and not newState & (EntityStates.END_GAME | EntityStates.OBSERVER):
            self.__setSpectatorMode(newState & EntityStates.DEAD)

    def isLivePlayers(self):
        skipBots = BigWorld.player().battleType == ARENA_TYPE.TRAINING and not IS_DEVELOPMENT
        _, livePlayersInAllyTeam = self.getCountPlayersInTeam(BigWorld.player().teamIndex, skipBots, True)
        if livePlayersInAllyTeam == 0:
            _, livePlayersInEnemyTeam = self.getCountPlayersInTeam(1 - BigWorld.player().teamIndex, skipBots, True)
            if livePlayersInEnemyTeam == 0:
                return False
            _, liveBotsInAllyTeam = self.getCountPlayersInTeam(BigWorld.player().teamIndex, False, True)
            if liveBotsInAllyTeam == 0:
                return False
        _, liveAnyInEnemyTeam = self.getCountPlayersInTeam(1 - BigWorld.player().teamIndex, False, True)
        return bool(liveAnyInEnemyTeam)

    def __initOutro(self):
        LOG_TRACE('OUTRO started')
        self.__updateMinimapAndRadarVisibility()
        ui = self.__getBattleUI()
        if ui is None or ui.gameResult is None:
            return
        else:
            self.__smm.setState(SPECTATOR_MODE_STATES.OUTRO)
            vo = CustomObject()
            vo.winIndex, _, vo.winState, vo.winResult = ui.gameResult
            ui.uiCall('hud.initOutro', vo)
            GameSound().onBattleEnd()
            self.__outroCallback = BigWorld.callback(0.0, self.__outroTimerUpdate)
            import BWPersonality
            BWPersonality.g_fromOutro = True
            GameSound().voice.skipDynSeqItems(['voice_battle_superiority_enemy', 'voice_battle_superiority'])
            return

    def getSpectatorMode(self):
        if self.__smm:
            return self.__smm.state
        return SPECTATOR_MODE_STATES.OFF

    def __clearOutroCallback(self):
        if self.__outroCallback is not None:
            BigWorld.cancelCallback(self.__outroCallback)
        self.__outroCallback = None
        return

    def __outroTimerUpdate(self):
        ui = self.__getBattleUI()
        if self.__outroTime >= 0:
            ui.uiCall('hud.bigTimerUpdateTime', self.__outroTime)
            self.__outroTime -= 1
            self.__outroCallback = BigWorld.callback(1.0, self.__outroTimerUpdate)
        else:
            ui.uiCall('hud.bigTimerHide')

    def __onDestruction(self):
        ui = self.__getBattleUI()
        if ui:
            ui.onDestruction()
            self.__isFire = False
            ui.reportFire('', 0)
        self.map.setVisible(False)
        self.updateArrowsVisibility()
        self.clearTarget()

    def __spawnedStatusChanged(self, v):
        if v:
            ui = self.__getBattleUI()
            if ui:
                ui.setIsSpectator(False)
        self.updateArrowsVisibility()

    def __setSpectatorMode(self, spectatorMode):
        if self.__spectatorMode != spectatorMode:
            self.__spectatorMode = spectatorMode
            self.__smm.setState(SPECTATOR_MODE_STATES.INITIALIZED if spectatorMode else SPECTATOR_MODE_STATES.OFF)
            ui = self.__getBattleUI()
            if ui:
                ui.reInit(True)
                ui.setSpectatorMode(spectatorMode)
            self.__updateMiniScreenVisibility()
            self.__navigationWindowsManager.setSpectatorMode(spectatorMode)

    def getCountPlayersInTeam(self, teamIndex, skipBots = False, skipPlayerAvatar = False):
        if not GameEnvironment.getClientArena().isAllServerDataReceived():
            return (0, 0)
        livePlayersInTeams = [0, 0]
        countPlayersInTeams = [0, 0]
        for id, avatarInfo in GameEnvironment.getClientArena().avatarInfos.iteritems():
            isBot = avatarInfo['classID'] == EntitySupportedClasses.AvatarBot
            countPlayersInTeams[avatarInfo['teamIndex']] += 1
            isDead = avatarInfo['stats']['flags'] & AvatarFlags.DEAD != 0
            if skipPlayerAvatar and id == BigWorld.player().id:
                continue
            if id == BigWorld.player().id and EntityStates.inState(BigWorld.player(), EntityStates.DEAD | EntityStates.OBSERVER):
                continue
            if not isDead:
                if not (skipBots and isBot):
                    livePlayersInTeams[avatarInfo['teamIndex']] += 1

        return (countPlayersInTeams[teamIndex], livePlayersInTeams[teamIndex])

    def setCursorState(self, cursorState):
        self.__cursor.setState(cursorState)

    def setCursorPosition(self, vector3Position):
        self.__cursor.setCursorPosition(Math.Vector4(vector3Position.x, vector3Position.y, 0.0, vector3Position.z))

    def getCursorPosition(self):
        return self.__cursor.getCursorScreenPosition()

    def setVisibleIngameCursor(self, visible):
        self.__cursor.visible = visible and not self.__forceHideHud and self.isBattleLoadingDispossessed()

    def setEnableIngameCursor(self, enable):
        self.__cursor.enable = enable

    def getVisibleIngameCursor(self):
        return self.__cursor.getVisible()

    def setCursorDefaultLength(self, value):
        self.__cursor.setCursorDefaultLength(value)

    def setMiniScreenVisible(self, isVisible):
        """
        Set hud mini screen visibility. Use this to make mini screen visible even if hud was disabled
        @param isVisible:
        """
        self.__miniScreenVisibility = isVisible
        self.__updateMiniScreenVisibility()

    def __updateMiniScreenVisibility(self):
        if self.__miniScreen:
            settingsUI = Settings.g_instance.getGameUI()
            flagShow = self.__miniScreenVisibility and not self.__teamsVisible if self.__miniScreenVisibility is not None else settingsUI['targetWindow'] and self.__visible
            self.__miniScreen.setVisible(flagShow and not self.__spectatorMode)
        return

    def sendMarkerMessage(self, posX, posZ):
        BigWorld.player().cell.sendMarkerMessage(posX, posZ, self.__guiCursor.state)

    def onReceiveMarkerMessage(self, senderID, posX, posZ, messageStringID, fromQueue):
        self.__navigationWindowsManager.setMarker(posX, posZ, MarkerType.DEFAULT, MAP_BLINK_NUM)
        if self.minimap.isVisible() or self.map.isVisible():
            posGridX, posGridZ = self.minimap.getGridPosition(posX, posZ)
            message = localizeHUD(self.MARKER_MESSAGES_LOC_IDS[messageStringID]).format(grid_square=str(posGridZ) + str(posGridX))
            messageType = MESSAGE_TYPE.BATTLE_ALLY
            if senderID != BigWorld.player().id:
                squadType = SQUAD_TYPES().getSquadType(SQUAD_TYPES().getSquadIDbyAvatarID(senderID), senderID)
                if squadType == SQUAD_TYPES.OWN:
                    messageType = MESSAGE_TYPE.BATTLE_SQUAD
            self.__chat.showTextMessage(senderID, messageType, 0, 0, message, fromQueue)
            if messageStringID == GUICursorStates.ENEMY:
                self.sendEntityCommands(senderID, ChatMessagesStringID.ENEMY_HERE)
            elif messageStringID == GUICursorStates.FRIENDLY:
                self.sendEntityCommands(senderID, ChatMessagesStringID.MY_LOCATION)

    def applyArenaData(self, arenaData):
        self.__arenaBounds = arenaData['bounds']
        self.__navigationWindowsManager.setBounds(self.__arenaBounds)

    def onPlayersInfo(self, isFired):
        self.uiCall('hud.additionalPlayersInfo', isFired)
        if self.__entityesHud:
            self.__entityesHud.setAdditionalInfoState(isFired)
        self.__navigationWindowsManager.setAltState(isFired)

    def showChatMessage(self, command, isFired):
        if command in self.CHAT_COMMANDS_MESSAGES:
            messageStringID = self.CHAT_COMMANDS_MESSAGES[command]
            if messageStringID in [ChatMessagesStringID.ENEMY_HERE, ChatMessagesStringID.MY_LOCATION]:
                if self.__guiCursor.state == GUICursorStates.NORMAL_ON or messageStringID == ChatMessagesStringID.ENEMY_HERE and self.__guiCursor.state == GUICursorStates.FRIENDLY or messageStringID == ChatMessagesStringID.MY_LOCATION and self.__guiCursor.state == GUICursorStates.ENEMY:
                    return
                if isFired:
                    if messageStringID == ChatMessagesStringID.ENEMY_HERE:
                        self.__guiCursor.state = GUICursorStates.ENEMY
                    elif messageStringID == ChatMessagesStringID.MY_LOCATION:
                        self.__guiCursor.state = GUICursorStates.FRIENDLY
                else:
                    self.__guiCursor.state = GUICursorStates.NORMAL_OFF
                self.__updateVisibilityMouseCursor(isFired)
            elif isFired:
                if BigWorld.time() - self.__chatCommandLastExecuteTime <= HUD_ENTITY_COMMAND_WAITING_TIME:
                    return
                targetID = 0
                if messageStringID in [ChatMessagesStringID.JOIN_ME, ChatMessagesStringID.ENEMY_MY_AIM]:
                    if self.targetEntity is not None and not EntityStates.inState(self.targetEntity, EntityStates.DESTROYED | EntityStates.DESTROYED_FALL):
                        targetID = self.targetEntity.id
                    else:
                        return
                self.__chatCommandLastExecuteTime = BigWorld.time()
                self.__chat.broadcastMessage('', MESSAGE_TYPE.BATTLE_PROMPT_COMMAND, messageStringID, targetID)
        return

    def visibilityMouseCursor(self, fired):
        if self.__guiCursor.state not in [GUICursorStates.ENEMY, GUICursorStates.FRIENDLY]:
            self.__guiCursor.state = GUICursorStates.NORMAL_ON if fired else GUICursorStates.NORMAL_OFF
            self.__updateVisibilityMouseCursor(fired)

    def __updateVisibilityMouseCursor(self, fired):
        player = BigWorld.player()
        if fired:
            player.onFireChange(0)
        self.onVisibilityCursor(fired)
        self.__updateVisibilityHudElems(fired)

    def __updateVisibilityHudElems(self, fired):
        """
        show or hide hud elements depending on the cursor visibility state
        @param fired: bool
        """
        if self.isVisible() and not self.map.isVisible():
            if fired:
                if not self.minimap.isVisible() and not self.radar.isVisible():
                    self.minimap.setVisible(True)
            else:
                self.__updateMinimapAndRadarVisibility()

    def showMap(self, fired, ignoreCommandIDsList, forceShowCursor):
        if (self.__visible or not self.__isBattleLoadingVisible and EntityStates.inState(BigWorld.player(), EntityStates.PRE_START_INTRO)) and not self.__teamsVisible and fired != self.map.isVisible():
            self.map.setVisible(fired)
            if self.map.isVisible():
                BigWorld.player().onFireChange(0)
            if forceShowCursor:
                Cursor.forceShowCursor(self.map.isVisible())
                BigWorld.player().setFlyMouseInputAllowed(not self.map.isVisible())

    def zoomInRadar(self):
        if self.__visible:
            self.radar.zoomIn()

    def zoomOutRadar(self):
        if self.__visible:
            self.radar.zoomOut()

    def onEscButtonPressed(self):
        if EntityStates.inState(BigWorld.player(), EntityStates.OUTRO):
            self.uiCall('hud.escButtonPressed')
            return
        if self.__chatVisible:
            self.onVisibilityChat(False)
            return
        if self.__visible and self.map.isVisible():
            self.showMap(False, [], True)
        else:
            self.__helpVisible = False
            self.uiCall('hud.escButtonPressed')

    def setVisibilityBattleloading(self, isVisible):
        if isVisible:
            self.map.setVisible(False)
        self.__isBattleLoadingVisible = isVisible
        self.setVisibility(isVisible)

    def isBattleLoadingVisible(self):
        return self.__isBattleLoadingVisible

    def setTargetVisible(self, value):
        LOG_DEBUG('setTargetVisible', value)
        backSideLook = not value
        if InputMapping.g_instance.currentProfileType in (INPUT_SYSTEM_STATE.MOUSE, INPUT_SYSTEM_STATE.GAMEPAD_DIRECT_CONTROL):
            cam = GameEnvironment.getCamera().getDefualtStrategies['CameraStrategyMouse']
            backSideLook = cam.backSideLook or cam.isOwerLook
        elif InputMapping.g_instance.currentProfileType == INPUT_SYSTEM_STATE.JOYSTICK:
            backSideLook = GameEnvironment.getCamera().getDefualtStrategies['CameraStrategyNormal'].action
        self.__movingTarget.setTargetVisible(value and self.isBattleLoadingDispossessed() and not backSideLook)

    def isTargetVisible(self):
        return self.__movingTarget.isVisible()

    def __getBattleUI(self):
        if not self.__battleUI:
            self.__battleUI = g_windowsManager.getBattleUI()
        return self.__battleUI

    def update1sec(self):
        battleUI = self.__getBattleUI()
        if battleUI:
            fps = BigWorld.getFPS()[1]
            ping = BigWorld.LatencyInfo().value[3] * 1000 - SERVER_TICK_LENGTH * 0.5 * 1000
            ping = max(1, ping)
            dataLost = 0
            owner = BigWorld.player()
            if owner is not None and owner.inWorld and owner.movementFilter():
                dataLost = owner.filter.dataLost
            battleUI.updateEngineStates(round(ping, 1), round(fps, 1), dataLost)
            if self.__timerUpdateEnabled:
                self.__updateTimer(battleUI)
        self.__update1secCallBack = BigWorld.callbackRealTime(1.0, self.update1sec)
        self.eUpdate1sec()
        return

    def __isAmmoBomrs(self):
        isAmmo = False
        for bombGroup in self.__bombGroups:
            if bombGroup in self.lastAmmoCounters:
                isAmmo = isAmmo or self.lastAmmoCounters[bombGroup] > 0

        return isAmmo

    def __updateBombTarget(self):
        self.__bombTarget.setVisible(self.__isAmmoBomrs() and self.__visibleBombing and self.__visible and EntityStates.inState(BigWorld.player(), EntityStates.GAME))
        if self.__bombTarget.isVisible():
            correctBombingAngle = isCorrectBombingAngle(BigWorld.player(), BigWorld.player().getRotation())
            if correctBombingAngle != self.__isCorrectBombingAngle:
                self.__isCorrectBombingAngle = correctBombingAngle
                self.uiCall('hud.isCorrectBombingAngle', self.__isCorrectBombingAngle)
            self.__bombTarget.setBombTargetEnable(correctBombingAngle)

    def update(self):
        self.__markers.update()
        ui = self.__getBattleUI()
        owner = BigWorld.player()
        if owner is not None and owner.inWorld:
            self.__miniScreen.update()
            self.__updateBombTarget()
            if not self.__spectatorMode:
                self.__updateTargets()
            if self.__smm.state < SPECTATOR_MODE_STATES.OBSERVER:
                self.__updateAltitude(owner)
        if self.__smm.state >= SPECTATOR_MODE_STATES.OBSERVER:
            en = BigWorld.entities.get(owner.curVehicleID, None)
            if en is not None:
                self.__updateAltitude(en)
                if ui:
                    ui.updateSpeed(en.getSpeed() * METERS_PER_SEC_TO_KMH_FACTOR)
        self.__updateCallBack = BigWorld.callback(0.1, self.update)
        if ui and ui.state == HudStateType.BATTLE_STARTED:
            if EntityStates.inState(owner, EntityStates.GAME):
                isStallWarningVisible = self.__stallSpeed > owner.getSpeed() > 0.0
                GameSound().onStallingDanger(isStallWarningVisible)
                if self.changeWarningIndicator(WarningType.STALL, isStallWarningVisible):
                    ui.updateWarningIndicator(WarningType.STALL, isStallWarningVisible)
                self.__updateBorderWarningIndicator(owner, ui)
            else:
                self.__updateSpectatorText()
        return

    def updateAmmoGroupCounters(self, gunsStatus):
        ui = self.__getBattleUI()
        if ui:
            ui.updateAmmoGroupCounters(gunsStatus)
            needUpdateDispersion = False
            if len(self.lastAmmoCounters) == 0:
                needUpdateDispersion = True
                self.lastAmmoCounters = gunsStatus.copy()
            else:
                for groupID, ammoCount in gunsStatus.items():
                    if self.lastAmmoCounters.get(groupID, 0) != ammoCount:
                        needUpdateDispersion = True
                        self.lastAmmoCounters[groupID] = ammoCount

            if needUpdateDispersion:
                self.updateUIWeaponDispersion()

    def autopilotVisibility(self, v):
        if EntityStates.inState(BigWorld.player(), EntityStates.GAME):
            ui = self.__getBattleUI()
            if ui and self.changeWarningIndicator(WarningType.AUTOPILOT, v):
                ui.updateWarningIndicator(WarningType.AUTOPILOT, bool(v))

    def __updateTimer(self, battleUI):
        battleUI.updateTime(BigWorld.serverTime(), BigWorld.player().arenaStartTime)
        self.eUpdateTimer()

    def updateAmmo(self, prc):
        ui = self.__getBattleUI()
        if ui:
            ui.updateAmmo(prc)

    def updatePlayerAmmo(self):
        player = BigWorld.player()
        self.updateAmmoGroupCounters(player.getAmmoCountByGroup())

    def updateForce(self, value):
        ui = self.__getBattleUI()
        if ui:
            prc = 1.0
            if 0 > value >= -1:
                prc = 1.0 + value
            ui.updateForce(prc)

    def updateEngineTemperature(self, engineTemperature, wepWorkTime, isForceEngine):
        ui = self.__getBattleUI()
        if ui:
            ui.updateEngineTemperature((engineTemperature - WEP_ENABLE_TEMPERATURE) / ENGINE_WORK_INTERVAL, isForceEngine)
            if EntityStates.inState(BigWorld.player(), EntityStates.GAME):
                k = (WEP_DISABLE_TEMPERATURE - WEP_ENABLE_TEMPERATURE) / wepWorkTime
                self.updateAfterBurningTime(max(0.0, wepWorkTime - (engineTemperature - WEP_ENABLE_TEMPERATURE) / k))
            owner = BigWorld.player()
            if owner.engineTemperature < WEP_MAX_TEMPERATURE and self.__isEngineOverheated:
                self.__isEngineOverheated = False
                ui.uiClearTextLabel('engineOverheat')

    def isEngineOverheated(self):
        return self.__isEngineOverheated

    def updateSpeed(self):
        ui = self.__getBattleUI()
        if ui:
            if EntityStates.inState(BigWorld.player(), EntityStates.PRE_START_INTRO):
                ui.updateSpeed(BigWorld.player().introFakeSpeed * METERS_PER_SEC_TO_KMH_FACTOR)
            elif self.__smm.state == SPECTATOR_MODE_STATES.OFF:
                ui.updateSpeed(BigWorld.player().speed * METERS_PER_SEC_TO_KMH_FACTOR)

    def updateSpeedTutorial(self):
        ui = self.__getBattleUI()
        if not ui:
            return
        tutManager = BigWorld.player().controllers.get('tutorialManager')
        if tutManager.isPaused():
            return
        if BigWorld.player().speed > 0 and BigWorld.player().speed < 1000:
            ui.updateSpeed(BigWorld.player().speed * METERS_PER_SEC_TO_KMH_FACTOR)

    def onChangeLanguage(self):
        for record in self.__entityList.values():
            record.updateLocalizedName()

        ui = self.__getBattleUI()
        if ui:
            ui.onChangeLanguage()

    def onChangeSpeedometerState(self, val):
        ui = self.__getBattleUI()
        if ui:
            ui.changeSpeedometerState(val)
            ui.changeVariometerState(val)

    def onChangeAviahorizonMode(self, val):
        ui = self.__getBattleUI()
        if ui:
            ui.onChangeAviahorizonMode(val)

    def __initMiniScreen(self):
        settingsUI = Settings.g_instance.getGameUI()
        miniScreenClass = MiniScreenTarget
        if settingsUI['targetWindowList']:
            miniScreenClass = MiniScreenRearView
        if self.__miniScreen:
            if self.__miniScreen.__class__ == miniScreenClass:
                return
            self.__miniScreen.destroy()
        self.__miniScreen = miniScreenClass()
        if self.__miniScreen.__class__ == MiniScreenTarget:
            self.__miniScreen.onMiniScreenTargetInfoUpdate += self.__miniScreenTargetInfoUpdate
            self.__miniScreen.onMiniScreenTargetInfoVisibility += self.__miniScreenTargetInfoVisibility
            self.__miniScreen.onMiniScreenLockTargetVisibility += self.__miniScreenLockTargetVisibility
        self.__miniScreen.setEntitiesHUD(self.__entityesHud)

    def __miniScreenLockTargetVisibility(self, visibility):
        ui = self.__getBattleUI()
        if ui:
            ui.uiCall('hud.updateInfoCapturedTargetMessage', visibility, localizeHUD('HUD_LOCK_TARGET_TEXT_2') if visibility else localizeHUD('HUD_UNLOCK_TARGET_TEXT_2'))

    def __miniScreenTargetInfoVisibility(self, visibility):
        if not visibility:
            self.__miniScreenTargetID = None
        ui = self.__getBattleUI()
        if ui:
            ui.uiCall('hud.visibleInfoCapturedTarget', visibility)
        return

    def __miniScreenTargetInfoUpdate(self, target):
        ui = self.__getBattleUI()
        if ui:
            targetDist = round((target.position - BigWorld.player().position).length / WORLD_SCALING, 1)
            vo = CustomObject()
            vo.distance = str(int(MeasurementSystem().getMeters(targetDist)))
            vo.health = getTargetHealthPrc(target)
            if target.id != self.__miniScreenTargetID:
                self.__miniScreenTargetID = target.id
                if isAvatar(target):
                    settings = db.DBLogic.g_instance.getAircraftData(target.planeID)
                    level = settings.airplane.level
                    icon = settings.airplane.planeType
                    diff, state, _ = getCalculatedBalanceCharacteristic(target.id)
                    vo.firepowerState = state['dps']
                    vo.maneuverabilityState = state['maneuverability']
                    vo.speedState = state['speedFactor']
                    vo.heightState = state['optimalHeight']
                    vo.strengthState = state['hp']
                    targetInfo = GameEnvironment.getClientArena().getAvatarInfo(self.__miniScreenTargetID)
                    isBot = targetInfo['classID'] == EntitySupportedClasses.AvatarBot
                    if isBot and self.isTutorial():
                        name = localizeAirplane(settings.airplane.name)
                        clanAbbrev = ''
                    else:
                        name = GameEnvironment.getClientArena().getObjectName(target.id)
                        clanAbbrev = targetInfo.get('clanAbbrev', '')
                else:
                    name = ''
                    clanAbbrev = ''
                    level = 0
                    icon = self.getTeamObjectTypeByParts(target.id)
                vo.metric = self.__locDistUnit
                vo.name = name
                vo.clanAbbrev = clanAbbrev
                vo.type = target.localizedName
                vo.level = level
                vo.icon = icon
                vo.isAvatar = isAvatar(target)
                ui.uiCall('hud.initInfoCapturedTarget', vo)
            else:
                if not isAvatar(target):
                    objectPartsType = self.getTeamObjectTypeByParts(target.id)
                    if objectPartsType != TEAM_OBJECTS_PARTS_TYPES.ERROR:
                        vo.icon = objectPartsType
                ui.uiCall('hud.updateInfoCapturedTarget', vo)

    def onNavWindowListChanged(self, val):
        self.__updateMinimapAndRadarVisibility()

    def __updateMinimapVisibility(self):
        self.minimap.setVisible(Settings.g_instance.getGameUI()['navigationWindowMinimap'] and self.__minimapVisible and self.__checkNavWindowsVisibility())

    def __updateRadarVisibility(self):
        self.radar.setVisible(Settings.g_instance.getGameUI()['navigationWindowRadar'] and self.__radarVisible and self.__checkNavWindowsVisibility())

    def __checkNavWindowsVisibility(self):
        return self.__visible and not EntityStates.inState(BigWorld.player(), EntityStates.OUTRO) and self.__smm.state not in (SPECTATOR_MODE_STATES.DYNAMIC_CAMERA, SPECTATOR_MODE_STATES.INITIALIZED)

    def __updateMinimapAndRadarVisibility(self):
        if self.__isAllVisibleEntitiesCollected:
            self.__updateMinimapVisibility()
            self.__updateRadarVisibility()

    def onArenaLoaded(self):
        BigWorld.player().initTutorialUI()
        self.__arenaLoaded = True
        if GameEnvironment.getClientArena().isAllServerDataReceived():
            self.initMarkers()
        self.sendSituationalPilotSkills()

    def isArenaLoaded(self):
        return self.__arenaLoaded

    def getSeaLevel(self):
        if self.__seaLevel is None:
            arData = db.DBLogic.g_instance.getArenaData(BigWorld.player().arenaType)
            self.__seaLevel = arData.altitudeMap - arData.seaLevelForFlightMdel / WORLD_SCALING
        return self.__seaLevel

    def __initTeamObjectsGroups(self):
        if not SUPERIORITY2_BASE_HEALTH:
            return
        for objID, objData in GameEnvironment.getClientArena().allObjectsData.iteritems():
            groupName = objData['groupName']
            if groupName:
                if groupName not in self.__teamObjectsGroups:
                    self.__teamObjectsGroups[groupName] = list()
                self.__teamObjectsGroups[groupName].append(objID)

        for groupName, groupEntities in self.__teamObjectsGroups.iteritems():
            self.__navigationWindowsManager.addGroup(groupName, groupEntities[:])

    def initMarkers(self):
        self.__battleLoading.sendHintsData(self.__getPerformanceSpecsDescriptions(BigWorld.player(), False).desc)
        self.__responseBattleHints()
        if self.__markers is not None and not self.__markers.initialized:
            self.__markers.load(self.__getBattleUI())
        for entityData in self.__matrixForMarkersGroup:
            self.__updateMatrixForMarkersGroup(entityData[0], entityData[1])

        self.__matrixForMarkersGroup = list()
        player = BigWorld.player()
        if player is not None and 'tutorialManager' in player.controllers:
            player.controllers['tutorialManager'].markersInited()
        return

    def updateHudElements(self):
        self.__updateMiniScreenVisibility()
        if self.__targetEntity:
            if self.__targetEntity.id in self.entityList:
                self.onTargetEntity(self.__targetEntity)
            else:
                LOG_DEBUG('___updateHudElements - self.__targetEntity.id(%s) not in entityList' % self.__targetEntity.id)
        self.__updateMinimapAndRadarVisibility()
        self.uiCall('hud.setFPColor', Settings.g_instance.colorPointIndexFP)
        self.__forestallingPoint.setVisible(self.__visible and Settings.g_instance.showAdvancePoint or self.__forestallingPointVisible)
        self.setBombTargetVisible(self.__visible and self.__visibleBombing)
        self.__centralHUD.visible = self.__centralHudVisible and self.__visible and self.isBattleLoadingDispossessed()
        self.__entityesHud.visible = self.__entityesHudVisible and self.__visible
        self.updateArrowsVisibility()

    def onUpdateUIComponents(self):
        ui = self.__getBattleUI()
        if ui:
            ui.updateHUDSettings()

    def onAimsSettingsUpdate(self):
        ui = self.__getBattleUI()
        if ui:
            ui.updateAim()

    def onMarkersSettingsUpdate(self):
        self.__markers.rebuild()

    def onUpdateHUDSettings(self):
        self.__initMiniScreen()
        self.updateHudElements()

    def updateMiniScreenPosition(self):
        if self.__miniScreen:
            self.__miniScreen.updatePosition()

    def updateRadarPosition(self):
        if self.radar:
            self.radar.updatePosition()

    def getRadarSize(self):
        if self.radar:
            return self.radar.background.size
        else:
            return None

    def updateArrowsVisibility(self):
        self.__entityesHud.showArrows = self.__entityesHudVisible and self.__visible and not EntityStates.inState(BigWorld.player(), EntityStates.PRE_START_INTRO | EntityStates.DEAD | EntityStates.OBSERVER | EntityStates.END_GAME)

    def __getHealthStr(self, health):
        return localizeHUD('HUD_HEALTH_STR').format(health=int(health + 0.99))

    def updateHealth(self, health, lastDamagerID, oldValue):
        ui = self.__getBattleUI()
        if ui:

            def calculate(_health):
                if _health <= 0:
                    return 0
                h = math.ceil(_health)
                if 1 >= h:
                    return 1
                return h

            ui.updateHealth(calculate(health))
            if lastDamagerID != 0 and lastDamagerID != BigWorld.player().id and self.__visible:
                self.uiCall('hud.showDamageDirection', math.degrees(self.getDamageAngle(lastDamagerID)), CIRCLE_HUD_DAMAGE_DIRECTION_HIDE_TIME * 1000.0)

    @staticmethod
    def getDamageAngle(authorID):
        author = BigWorld.entities.get(authorID)
        if author:
            screenPos = BigWorld.worldToScreen(author.position)
            screenCenterPos = Math.Vector3(BigWorld.screenWidth() / 2, BigWorld.screenHeight() / 2, 0)
            deltaPos = screenPos - screenCenterPos
            side = deltaPos.z
            deltaPos.z = 0
            deltaPos.normalise()
            pos = deltaPos * CIRCLE_HUD_DAMAGE_DIRECTION_R
            if side < 0:
                pos *= -1
            angle = math.atan2(pos.x, pos.y) - CIRCLE_HUD_DAMAGE_DIRECTION_PICTURE_ROTATION + math.pi
            angle = 2 * math.pi - angle
            return angle
        return 0

    def broadcastChatMessage(self, message, messageType):
        self.__chat.broadcastMessage(message, messageType)

    def sendEntityCommands(self, senderID, messageStringID, targetID = None):
        """
        Send entity command
        @param int senderID:
        @param int messageStringID: (see in class ChatMessagesStringID)
        """
        messageStringID = int(messageStringID)
        if messageStringID in self.CHAT_COMMANDS_MESSAGES_REVERTED:
            entity = None
            player = BigWorld.player()
            if senderID in self.entityList:
                entity = self.entityList[senderID]
                if player.id != senderID:
                    if (entity.position - player.position).length / WORLD_SCALING < CUR_TARGET_VISIBILITY_DISTANCE:
                        self.uiCall('hud.entityCommands', senderID, messageStringID)
                en = self.entityList.get(senderID, None)
                if en is not None:
                    if (en.position - player.position).length / WORLD_SCALING < CUR_TARGET_VISIBILITY_DISTANCE:
                        if messageStringID == ChatMessagesStringID.JOIN_ME:
                            self.uiCall('hud.entityCommands', targetID, ChatMessagesStringID.JOIN_ME_ENEMY)
                            self.__entityCommands[senderID] = (targetID, ChatMessagesStringID.JOIN_ME_ENEMY)
                        elif messageStringID == ChatMessagesStringID.ENEMY_MY_AIM:
                            self.uiCall('hud.entityCommands', targetID, ChatMessagesStringID.ENEMY_MY_AIM_ENEMY)
                            self.__entityCommands[senderID] = (targetID, ChatMessagesStringID.ENEMY_MY_AIM_ENEMY)
                    if senderID in self.__entityCommandCallBacks:
                        BigWorld.cancelCallback(self.__entityCommandCallBacks[senderID])
                    self.__entityCommandCallBacks[senderID] = BigWorld.callback(MAP_ENTITY_COMMAND_WAITING_TIME, functools.partial(self.__removeEntityCommand, senderID))
                    self.__entityesHud.setEntityCommand(senderID, messageStringID, ENTITY_COMMAND_CUT_TEXTURE_VECTORS[messageStringID][0], ENTITY_COMMAND_CUT_TEXTURE_VECTORS[messageStringID][1])
                else:
                    LOG_WARNING('sendEntityCommands - entity(%s) not in enemyList,mapEntry command=(%s)' % (senderID, messageStringID))
            entity = self.__getEntityFromMapEntry(entity, senderID)
            if entity is not None:
                self.__navigationWindowsManager.setEntityCommand(senderID, entity.mapMatrix, messageStringID)
            else:
                LOG_WARNING('sendEntityCommands - entity(%s) not in enemyList,mapEntry command=(%s)' % (senderID, messageStringID))
            entity = self.__getEntityFromMapEntry(self.entityList[targetID] if targetID is not None and targetID in self.entityList else None, targetID)
            if entity is not None:
                if messageStringID == ChatMessagesStringID.JOIN_ME:
                    self.__navigationWindowsManager.setEntityCommand(targetID, entity.mapMatrix, 9)
                elif messageStringID == ChatMessagesStringID.ENEMY_MY_AIM:
                    self.__navigationWindowsManager.setEntityCommand(targetID, entity.mapMatrix, 10)
            else:
                LOG_WARNING('sendEntityCommands - enemy(%s) not in enemyList,mapEntry command=(%s)' % (senderID, messageStringID))
        return

    def __getEntityFromMapEntry(self, entity, ID):
        if entity is None:
            mapEntry = GameEnvironment.getClientArena().getMapEntry(ID)
            if mapEntry and mapEntry.isAlive:
                entity = mapEntry
        return entity

    def __removeEntityCommand(self, entityID):
        self.__entityesHud.setEntityCommand(entityID, 0, Math.Vector2(0.0, 0.0), Math.Vector2(0.0, 0.0))

    def setUsersChatStatus(self, usersList):
        playersList = []
        clientArena = GameEnvironment.getClientArena()
        for userStatus in usersList:
            playerID = clientArena.getAvatarIdByDBId(int(userStatus[0]))
            if playerID is not None:
                playersList.append((playerID, userStatus[1]))
            else:
                LOG_ERROR('setUsersChatStatus: can not get playerID by dbid(%s)' % userStatus[0])

        self.__chat.setPlayersChatStatus(playersList)
        ui = self.__getBattleUI()
        if ui:
            ui.setPlayersChatStatus(playersList)
        return

    def showTextMessage(self, senderID, messageType, messageStringID, targetID, message, fromQueue):
        if messageType == MESSAGE_TYPE.BATTLE_PROMPT_COMMAND:
            messageType = MESSAGE_TYPE.BATTLE_ALLY
            if senderID != BigWorld.player().id:
                squadType = SQUAD_TYPES().getSquadType(SQUAD_TYPES().getSquadIDbyAvatarID(senderID), senderID)
                if squadType == SQUAD_TYPES.OWN:
                    messageType = MESSAGE_TYPE.BATTLE_SQUAD
        self.sendEntityCommands(senderID, messageStringID, targetID)
        if not Settings.g_instance.getGameUI()['isChatEnabled'] and int(messageStringID) not in self.CHAT_COMMANDS_MESSAGES_REVERTED:
            return
        if not self.__chat.isPlayerIgnored(senderID):
            fMessage = self.__chat.filterMessage(message, senderID)
            self.__chat.showTextMessage(senderID, messageType, messageStringID, targetID, fMessage, fromQueue)

    def showBattleMessageReactionResult(self, battleMessageType, isPositive, senderID, callerID, targetID):
        ownerID = BigWorld.player().id
        doShowChatMessage = ownerID == callerID
        reactionType = BattleMessageReactionHelper.BATTLE_MESSAGE_TYPE_RESULT_MAP_POSITIVE.get(battleMessageType, None) if isPositive else BATTLE_MESSAGE_TYPE.FAILURE
        if reactionType is not None:
            self.sendEntityCommands(senderID, reactionType, targetID)
        if not doShowChatMessage:
            return
        else:
            arena = GameEnvironment.getClientArena()
            senderName, callerName, targetName = arena.getObjectName(senderID), arena.getObjectName(callerID), arena.getObjectName(targetID)
            textMessage = MessagesID().getLocalizedMessage(reactionType, targetID) if BattleMessageReactionHelper.USE_STANDARD_MESSAGE_TEXT else BattleMessageReactionHelper.LocalizeBattleMessageReaction(battleMessageType, isPositive, senderName, callerName, targetName)
            if BattleMessageReactionHelper.USE_COLORS:
                htmlText = textMessage.replace('>', '&gt;')
                htmlText = htmlText.replace('<', '&lt;')
                isColorBlind = Settings.g_instance.getGameUI()['alternativeColorMode']
                if isColorBlind:
                    colorCode = BattleMessageReactionHelper.POSITIVE_REACTION_COLOR_ALT if isPositive else BattleMessageReactionHelper.NEGATIVE_REACTION_COLOR_ALT
                else:
                    colorCode = BattleMessageReactionHelper.POSITIVE_REACTION_COLOR if isPositive else BattleMessageReactionHelper.NEGATIVE_REACTION_COLOR
                htmlText = '<font color="{}">{}</font>'.format(colorCode, htmlText)
                self.__chat.showTextMessage(senderID, MESSAGE_TYPE.BATTLE_ALLY, 0, callerID, htmlText, False, isHTML=True)
                return
            self.__chat.showTextMessage(senderID, MESSAGE_TYPE.BATTLE_ALLY, 0, callerID, textMessage, False)
            return

    def showTextMessageFromLobby(self, senderID, messageType, message):
        if not Settings.g_instance.getGameUI()['isChatEnabled']:
            return
        playerID = GameEnvironment.getClientArena().getAvatarIdByDBId(senderID)
        if BigWorld.player().id != playerID:
            self.__chat.showTextMessage(playerID, messageType, 0, 0, message, False)

    def __generateObjectIco(self, objectType):
        return ''.join(['$', objectType])

    def __getLocalizePlayerDethInfo(self, killerName, killerData, lastDamageType, lastDamageReason):
        isKillerBot = killerData['classID'] == EntitySupportedClasses.AvatarBot
        playerDeadIndex = int(isKillerBot and BigWorld.player().battleType == ARENA_TYPE.PVE)
        if playerDeadIndex:
            killerName = killerName.replace('>', '&gt;')
            killerName = killerName.replace('<', '&lt;')
        killerAircraft = localizeAirplane(killerData['settings'].airplane.name)
        if lastDamageType == ACTION_DEALER.RAMMING:
            loc = localizeHUD(LOCALIZE_PLAYER_DETH_TABLE[PLAYER_DETH.FROM_HIT][playerDeadIndex]).format(name=killerName, aircraft=killerAircraft)
        elif lastDamageType == ACTION_DEALER.GUNNER:
            loc = localizeHUD(LOCALIZE_PLAYER_DETH_TABLE[PLAYER_DETH.FROM_GUNNER][playerDeadIndex]).format(name=killerName, aircraft=killerAircraft)
        elif lastDamageReason == DAMAGE_REASON.BOMB_EXPLOSION:
            loc = localizeHUD(LOCALIZE_PLAYER_DETH_TABLE[PLAYER_DETH.FROM_BOMB][playerDeadIndex]).format(name=killerName, aircraft=killerAircraft)
        elif lastDamageReason == DAMAGE_REASON.ROCKET_EXPLOSION:
            loc = localizeHUD(LOCALIZE_PLAYER_DETH_TABLE[PLAYER_DETH.FROM_ROCKET][playerDeadIndex]).format(name=killerName, aircraft=killerAircraft)
        elif lastDamageReason == DAMAGE_REASON.FIRING:
            loc = localizeHUD(LOCALIZE_PLAYER_DETH_TABLE[PLAYER_DETH.PLAYER_BURNED_YOU][playerDeadIndex]).format(name=killerName, aircraft=killerAircraft)
        else:
            loc = localizeHUD(LOCALIZE_PLAYER_DETH_TABLE[PLAYER_DETH.COMMON_REASON][playerDeadIndex]).format(name=killerName, aircraft=killerAircraft)
        return loc

    def reportDestruction(self, killingInfo, lastDamageType):
        LOG_DEBUG('reportDestruction', killingInfo, lastDamageType)

        def getPlayerName(playerData, withClan):
            if not (self.isTutorial() and playerData['classID'] == EntitySupportedClasses.AvatarBot):
                if withClan:
                    return getPlayerNameWithClan(playerData['playerName'], playerData['clanAbbrev'])
                return playerData['playerName']
            return localizeAirplane(playerData['settings'].airplane.name)

        ui = self.__getBattleUI()
        if ui:
            player = BigWorld.player()
            clientArena = GameEnvironment.getClientArena()
            killerData = clientArena.getAvatarInfo(killingInfo['killerID'])
            victimData = clientArena.getAvatarInfo(killingInfo['victimID'])
            playerAssist = reduce(lambda acc, x: (1 if x == player.id else acc), killingInfo['assists'], 0)
            if victimData:
                lastDamageReason = killingInfo['damageReason']
                victimName = getPlayerName(victimData, False)
                victimNameWithClan = getPlayerName(victimData, True)
                victimPlayerType = str(victimData['settings'].airplane.planeType)
                victimPlayerTeamIndex = victimData['teamIndex']
                isRammingOfTheLandObject = False
                victimSquadType = SQUAD_TYPES.getSquadType(victimData['squadID'], killingInfo['victimID'])
                if killerData:
                    killerName = getPlayerName(killerData, False)
                    killerNameWithChat = getPlayerName(killerData, True)
                    killerPlayerType = str(killerData['settings'].airplane.planeType)
                    killerPlayerTeamIndex = killerData['teamIndex']
                    killerSquadType = SQUAD_TYPES.getSquadType(killerData['squadID'], killingInfo['killerID'])
                else:
                    killerSquadType = SQUAD_TYPES.WITHOUT_SQUAD
                    objectTypeWithTurrets = getTeamObjectType(clientArena, killingInfo['killerID'])
                    objectType = clientArena.getTeamObjectType(killingInfo['killerID'])
                    if objectTypeWithTurrets == TYPE_TEAM_OBJECT.TURRET and lastDamageType == ACTION_DEALER.TURRET:
                        killerName = killerNameWithChat = localizeHUD(OBJECTS_INFO[objectType]['LOC_ID'])
                        killerPlayerType = ''.join([str(objectTypeWithTurrets), '0'])
                        killerPlayerTeamIndex = 1 - victimPlayerTeamIndex
                        if player.id == killingInfo['victimID']:
                            ui.uiCallTextLabel('spectatorModeInfoAboutTypeDeath', localizeHUD('UI_MESSAGE_YOU_DEAD_FROM_AA'))
                    else:
                        isRammingOfTheLandObject = True
                points = killingInfo.get('superiorityPoints', None)
                if killingInfo['killerID'] != killingInfo['victimID'] and not isRammingOfTheLandObject:
                    if player.id == killingInfo['victimID']:
                        ClientLog.g_instance.gameplay('You were detroyed by %s' % killerNameWithChat)
                        ui.updateAlert(self.getAlert(1, True, 1, SUPERIORITY_MSG_TYPES.DESTRUCTION, points), 1, 1)
                        self.lastDamageType = TUTORIAL_AVATAR_DESTROYED_REASON.OTHER
                        if killerData:
                            if lastDamageType == ACTION_DEALER.RAMMING:
                                self.lastDamageType = TUTORIAL_AVATAR_DESTROYED_REASON.RAMMING_AVATAR
                            ui.uiCallTextLabel('spectatorModeInfoAboutTypeDeath', self.__getLocalizePlayerDethInfo(killerNameWithChat, killerData, lastDamageType, lastDamageReason))
                        elif lastDamageReason == DAMAGE_REASON.FIRING:
                            ui.uiCallTextLabel('spectatorModeInfoAboutTypeDeath', localizeHUD(LOCALIZE_PLAYER_DETH_TABLE[PLAYER_DETH.YOU_BURNED][0]))
                    elif player.id == killingInfo['killerID']:
                        if player.teamIndex != victimPlayerTeamIndex:
                            if SUPERIORITY2_BASE_HEALTH:
                                ui.uiCallTextLabel('enemyKilled', localizeHUD('UI_MESSAGE_ENEMY_DOWN'))
                            GameSound().voice.skipDynSeqItems(['voice_hit_enemy',
                             'voice_crit_enemy',
                             'voice_fire_enemy',
                             'voice_hit_ally'])
                            if EntityStates.inState(player, EntityStates.GAME):
                                frags = killerData['stats']['frags'] + killerData['stats'].get('fragsAlly', 0) - 1
                                if frags < 0 or frags > len(self.__playerFragsSpeeches) - 1:
                                    frags = len(self.__playerFragsSpeeches) - 1
                                GameSound().voice.play(self.__playerFragsSpeeches[frags] if lastDamageType != ACTION_DEALER.RAMMING else 'voice_frag_ram')
                            ui.updateAlert(self.getAlert(0, True, 0, SUPERIORITY_MSG_TYPES.DESTRUCTION, points), 0, 0)
                            if not SUPERIORITY2_BASE_HEALTH and points:
                                planeType = PLANE_TYPE_ICO_PATH.PLANE_TYPE_DICT.get(victimData['settings'].airplane.planeType)
                                text = localizeHUD('HUD_SUPERIORITY_AIRPLANE_DOWNED').format(type=localizeHUD('HUD_PLANE_TYPE_%s_SMALL' % planeType.upper()))
                                ui.call_1('hud.showSuperiorityMessage', localizeHUD('HUD_SUPERIORITY_DECREASE'), ''.join(['-', str(int(points * SUPERIORITY_SCORE_PENALTY_COEF)), '%']))
                                ui.call_1('hud.showDamageMessage', text, ''.join(['+', str(points)]))
                        else:
                            ui.updateAlert(self.getAlert(1, True, 1, SUPERIORITY_MSG_TYPES.DESTRUCTION, points), 1, 1)
                            if EntityStates.inState(player, EntityStates.GAME):
                                GameSound().voice.play('voice_ally_destroy')
                        if player.battleType == ARENA_TYPE.PVE:
                            self.__leaderManager.checkDead(killingInfo['victimID'])
                        ClientLog.g_instance.gameplay('You destroyed %s' % victimNameWithClan)
                    else:
                        if killerPlayerTeamIndex == player.teamIndex:
                            if victimPlayerTeamIndex == killerPlayerTeamIndex:
                                ui.updateAlert(self.getAlert(1, True, 1, SUPERIORITY_MSG_TYPES.DESTRUCTION, points), 1, 1)
                            else:
                                if playerAssist:
                                    victimNameAssist = victimNameWithClan
                                    if victimData['classID'] == EntitySupportedClasses.AvatarBot and BigWorld.player().battleType == ARENA_TYPE.PVE:
                                        victimNameAssist = victimNameAssist.replace('>', '&gt;')
                                        victimNameAssist = victimNameAssist.replace('<', '&lt;')
                                    ui.uiCallTextLabel('playerAssist', localizeHUD('UI_ASSIST_MESSAGE').format(name=victimNameAssist, aircraft=localizeAirplane(victimData['settings'].airplane.name)))
                                ui.updateAlert(self.getAlert(0, True, 0, SUPERIORITY_MSG_TYPES.DESTRUCTION, points), 0, 0)
                        else:
                            isOwn = int(victimPlayerTeamIndex != killerPlayerTeamIndex)
                            ui.updateAlert(self.getAlert(isOwn, True, isOwn, SUPERIORITY_MSG_TYPES.DESTRUCTION, points), isOwn, isOwn)
                        ClientLog.g_instance.gameplay('%s destroyes %s' % (killerNameWithChat, victimNameWithClan))
                else:
                    text = localizeHUD('UI_SUICIDE_ALLY_AIRCRAFT')
                    isOwn = int(player.teamIndex == victimPlayerTeamIndex)
                    if player.id != killingInfo['victimID']:
                        ClientLog.g_instance.gameplay('Suicide of %s' % victimNameWithClan)
                        ui.updateAlert(self.getAlert(isOwn, True, isOwn, SUPERIORITY_MSG_TYPES.DESTRUCTION, points, None, text), isOwn, isOwn)
                    else:
                        ClientLog.g_instance.gameplay('You killed yourself')
                        self.lastDamageType = TUTORIAL_AVATAR_DESTROYED_REASON.OTHER
                        if lastDamageReason == DAMAGE_REASON.TERRAIN:
                            ui.uiCallTextLabel('spectatorModeInfoAboutTypeDeath', localizeHUD('HUD_PLAYER_DEAD_FROM_GROUND'))
                            self.lastDamageType = TUTORIAL_AVATAR_DESTROYED_REASON.GROUND
                        elif lastDamageReason == DAMAGE_REASON.TREES:
                            ui.uiCallTextLabel('spectatorModeInfoAboutTypeDeath', localizeHUD('HUD_PLAYER_DEAD_FROM_TREE'))
                        elif lastDamageReason == DAMAGE_REASON.OBSTACLE:
                            ui.uiCallTextLabel('spectatorModeInfoAboutTypeDeath', localizeHUD('UI_MESSAGE_YOU_FALL_ON_GROUND_TARGET'))
                        elif lastDamageReason == DAMAGE_REASON.WATER:
                            ui.uiCallTextLabel('spectatorModeInfoAboutTypeDeath', localizeHUD('HUD_PLAYER_DEAD_FROM_WATER'))
                            self.lastDamageType = TUTORIAL_AVATAR_DESTROYED_REASON.GROUND
                        elif lastDamageType == ACTION_DEALER.RAMMING or lastDamageReason == DAMAGE_REASON.RAMMING:
                            ui.uiCallTextLabel('spectatorModeInfoAboutTypeDeath', localizeHUD('UI_MESSAGE_YOU_FALL_ON_GROUND_TARGET'))
                        ui.updateAlert(self.getAlert(isOwn, True, isOwn, SUPERIORITY_MSG_TYPES.DESTRUCTION, points, None, text), isOwn, isOwn)
                msgVO = CustomObject()
                msgVO.playerID = player.id
                msgVO.killerID = killingInfo['victimID'] if isRammingOfTheLandObject else killingInfo['killerID']
                msgVO.victimID = killingInfo['victimID']
                msgVO.killerIsAvatar = killerData is not None
                msgVO.playerTeamIndex = player.teamIndex
                msgVO.killerTeamIndex = killerPlayerTeamIndex if msgVO.killerIsAvatar else -1
                msgVO.victimTeamIndex = victimPlayerTeamIndex
                msgVO.killerSquadType = killerSquadType
                msgVO.victimSquadType = victimSquadType
                msgVO.killerType = killerPlayerType if msgVO.killerIsAvatar else ''
                msgVO.victimType = victimPlayerType
                msgVO.killerName = replaceTagChars(killerName) if msgVO.killerIsAvatar else ''
                msgVO.killerClanAbbrev = msgVO.killerIsAvatar and killerData['clanAbbrev'] or ''
                msgVO.victimName = replaceTagChars(victimName)
                msgVO.victimClanAbbrev = victimData['clanAbbrev']
                msgVO.lastDamageType = lastDamageType
                msgVO.killerPlaneName = localizeAirplane(killerData['settings'].airplane.name) if msgVO.killerIsAvatar else ''
                msgVO.victimPlaneName = localizeAirplane(victimData['settings'].airplane.name)
                msgVO.playerPlaneName = player.localizedName
                playerData = clientArena.getAvatarInfo(player.id)
                msgVO.playerType = playerData['settings'].airplane.planeType
                msgVO.playerName = player.objectName
                msgVO.playerClanAbbrev = playerData['clanAbbrev']
                msgVO.assists = [player.id] if playerAssist else []
                self.uiCall('hud.battleMessage', msgVO)
        return

    def reportGainAward(self, awardInfo):
        avatarID, isRibbon, award_id, MaxProgress = awardInfo
        awardData = _awards_data.AwardsDB[award_id]
        quest_type = awardData.options.quest
        if quest_type in (_awards_data.QUEST_TYPE.MAIN_QUEST, _awards_data.QUEST_TYPE.CHILD_QUEST):
            if BigWorld.player().id == avatarID:
                import BWPersonality
                isMainQuest = quest_type == _awards_data.QUEST_TYPE.MAIN_QUEST
                questSelected = BWPersonality.g_questSelected
                if questSelected:
                    for qId, qData in questSelected.quests.iteritems():
                        if isMainQuest == qData.isMain:
                            qData.isComplete = True

            else:
                return
        self.__awardManager.add(awardInfo)

    def setFireState(self, avatarID, state):
        owner = BigWorld.player()
        if self.__smm.state >= SPECTATOR_MODE_STATES.OBSERVER and owner.curVehicleID == avatarID or self.__smm.state < SPECTATOR_MODE_STATES.OBSERVER and avatarID == owner.id:
            ui = self.__getBattleUI()
            if ui:
                ui.setFireState(state and 1 or 0)

    def reportTeamObjectDestruction(self, killerID, victimID, objectType, objectTeamIndex, points, pointsMax):
        ui = self.__getBattleUI()
        if ui:
            player = BigWorld.player()
            messageType = player.teamIndex == objectTeamIndex and 1 or 0
            if points:
                if victimID in self.__damagedPartsTeamObjectsCallbacks:
                    self.__clearDamagedPartsTeamObjectsCallback(victimID)
                if player.id == killerID:
                    text = localizeHUD('HUD_SUPERIORITY_DECREASE')
                    self.uiCall('hud.showSuperiorityMessage', text, ''.join([' -', str(int(pointsMax * SUPERIORITY_SCORE_PENALTY_COEF)), '%']))
                    self.uiCall('hud.showDamageMessage', localizeHUD(self.TEAM_OBJECT_SUPERIORITY_DATA_CENTER[SUPERIORITY_MSG_TYPES.DESTRUCTION][objectType]), ''.join(['+', str(points)]))
                text = self.getAlert(messageType, False, messageType, SUPERIORITY_MSG_TYPES.DESTRUCTION, points, objectType)
                self.__getBattleUI().updateAlert(text, messageType, messageType)
            if SUPERIORITY2_BASE_HEALTH:
                if objectType in self.TEAM_OBJECT_DESTRUCTION_DATA:
                    ui.updateAlert(localizeHUD(self.TEAM_OBJECT_DESTRUCTION_DATA[objectType][messageType]), messageType)
                    if not messageType and player.id == killerID and not self.isTutorial():
                        ui.uiCallTextLabel('enemyKilled', localizeHUD(self.TEAM_OBJECT_DESTRUCTION_DATA[objectType][messageType]))
                    killer = 'You' if killerID == player.id else ('Enemy(%s)' % killerID if messageType else 'Our(%s)' % killerID)
                    ClientLog.g_instance.gameplay('%s destroyed %s %s' % (killer, 'Our' if messageType else 'Enemy', TYPE_TEAM_OBJECT_STR_MAP_REVERTED[objectType]))
            if player.id == killerID:
                if player.teamIndex != objectTeamIndex:
                    GameSound().voice.clearDynSeq()
                    GameSound().voice.play('voice_ground_target_destroyed')

    def changeTOPartState(self, id, partID):
        if self.__markers.initialized:
            self.__markers.changeTOPartState(id, partID)

    def getAlert(self, side, isAvatar, colorType, msgType, points, objType = None, text = None, size = MSG_SUPERIORITY_SIZE):
        """
        @param side: <int> 0 - ALLY(left), 1 - ENEMY(right)
        @param colorType: <int> 0 - GREEN, 1 - RED
        @param msgType: <SUPERIORITY_MSG_TYPES>
        @param points: <str> or <int>
        @param objType: <TYPE_TEAM_OBJECT>
        @param size: <str> see: HTML TAG <SIZE>
        @return: <str> or None if error
        """
        if not points:
            return ''
        else:
            OBJECT_STR = text if text is not None else (localizeHUD('UI_DOWNED_AIRCRAFT_SUP2_TOP') if isAvatar else localizeHUD(self.TEAM_OBJECT_SUPERIORITY_DATA[msgType][objType]))
            if colorType:
                color1 = MSG_SUPERIORITY_RED_BLIND_COLOR if Settings.g_instance.getGameUI()['alternativeColorMode'] else MSG_SUPERIORITY_RED_COLOR
                color2 = MSG_SUPERIORITY_POINTS_RED_BLIND_COLOR if Settings.g_instance.getGameUI()['alternativeColorMode'] else MSG_SUPERIORITY_POINTS_RED_COLOR
            else:
                color1 = MSG_SUPERIORITY_GREEN_COLOR
                color2 = MSG_SUPERIORITY_POINTS_GREEN_COLOR
            return localizeHUD('HUD_MESSAGE_SUPERIORITY2' if side else 'HUD_MESSAGE_SUPERIORITY').format(msg_color1=str('%x' % color1), msg_color2=str('%x' % color2), size=str(size), points=str(points), type=OBJECT_STR)

    def reportTeamObjectPartGroupChanged(self, killerID, teamObjectID, points = None):
        LOG_DEBUG('reportTeamObjectPartGroupChanged', killerID, teamObjectID, points)
        if SUPERIORITY2_BASE_HEALTH:
            return
        else:
            owner = BigWorld.player()
            if self.__arenaLoaded:
                if points:
                    arena = GameEnvironment.getClientArena()
                    type = arena.getTeamObjectType(teamObjectID)
                    if owner.id == killerID:
                        if teamObjectID in self.__damagedPartsTeamObjectsCallbacks:
                            self.__damagedPartsTeamObjectsCallbacks[teamObjectID][1] += points
                        else:
                            self.__damagedPartsTeamObjectsCallbacks[teamObjectID] = [BigWorld.callback(DAMAGED_PARTS_TEAM_OBJECTS_CALLBACK_TIME, functools.partial(self.__clearDamagedPartsTeamObjectsCallback, teamObjectID)), points]
                        self.uiCall('hud.showDamageMessage', localizeHUD(self.TEAM_OBJECT_SUPERIORITY_DATA_CENTER[SUPERIORITY_MSG_TYPES.DAMAGED][type]), ''.join(['+', str(self.__damagedPartsTeamObjectsCallbacks[teamObjectID][1])]))
                    isOwn = int(BigWorld.player().teamIndex == arena.allObjectsData[teamObjectID]['teamIndex'])
                    text = self.getAlert(isOwn, False, isOwn, SUPERIORITY_MSG_TYPES.DAMAGED, points, type)
                    self.__getBattleUI().updateAlert(text, isOwn, isOwn)
                    en = self.entityList.get(teamObjectID, None)
                    if en is not None:
                        if self.__markers.initialized:
                            self.__markers.changeTeamObjectPartGroup(en)
            else:
                LOG_DEBUG('reportTeamObjectPartGroupChanged - __arenaLoaded not inited')
            return

    def __clearDamagedPartsTeamObjectsCallback(self, teamObjectID):
        BigWorld.cancelCallback(self.__damagedPartsTeamObjectsCallbacks[teamObjectID][0])
        del self.__damagedPartsTeamObjectsCallbacks[teamObjectID]

    def onScenarioSetIcon(self, groupName, iconIndex, textID, temaIndex):
        if iconIndex > 0:
            iconTeamIndex = int(temaIndex != BigWorld.player().teamIndex)
            try:
                textID = MARKERS_GROUP_ICON_LOC_ID.get(iconIndex)[iconTeamIndex]
                iconIndex = MARKERS_GROUP_ICON_INDEXES.get(iconIndex)[iconTeamIndex]
            except:
                LOG_ERROR('onScenarioSetIcon', iconTeamIndex, iconIndex, temaIndex)
                LOG_CURRENT_EXCEPTION()

        if self.__markers is not None and self.__markers.initialized:
            self.__markers.activateGroup(groupName, iconIndex, localizeHUD(textID))
        self.__navigationWindowsManager.initGroup(groupName, iconIndex)
        return

    def getTeamObjectTypeByParts(self, id, partsData = None):
        partsData = self.__getTeamObjectPartsData(id, partsData)
        if partsData is None:
            LOG_DEBUG('getTeamObjectTypeByParts - partsData is None', id)
            return TEAM_OBJECTS_PARTS_TYPES.SIMPLE
        elif not partsData:
            LOG_DEBUG('getTeamObjectTypeByParts - object has no live parts', id)
            return TEAM_OBJECTS_PARTS_TYPES.ERROR
        else:
            hasArmored, hasFiring, hasSimple = False, False, False
            for part in partsData:
                if part['isArmored']:
                    hasArmored = True
                else:
                    hasSimple = True
                if part['isFiring']:
                    hasFiring = True

            if not hasSimple:
                if hasFiring:
                    return TEAM_OBJECTS_PARTS_TYPES.FIRING_ARMORED
                return TEAM_OBJECTS_PARTS_TYPES.ARMORED
            elif hasFiring:
                if hasArmored:
                    return TEAM_OBJECTS_PARTS_TYPES.SIMPLE_FIRING_ARMORED
                return TEAM_OBJECTS_PARTS_TYPES.SIMPLE_FIRING
            elif hasArmored:
                return TEAM_OBJECTS_PARTS_TYPES.SIMPLE_ARMORED
            return TEAM_OBJECTS_PARTS_TYPES.SIMPLE
            return

    def __getTeamObjectPartsData(self, id, partsData = None, isConsiderDead = False):
        if partsData is None:
            en = BigWorld.entities.get(id, None)
            if en is None:
                LOG_WARNING('getTeamObjectTypesByParts - team object live the world', id)
                return
            partsData = en.getPartsTypeData(None, isConsiderDead)
        return partsData

    def getTeamObjectPartsTypes(self, id, partsData = None, isConsiderDead = False):
        """
        :param id: <int>
        :param partsData: <list>
        :return: <dict>
        """
        partsData = self.__getTeamObjectPartsData(id, partsData, isConsiderDead)
        partsInfo = dict()
        for part in partsData:
            partsInfo[part['partId']] = dict()
            partsInfo[part['partId']]['isDead'] = part['isDead']
            if part['isFiring']:
                if part['isArmored']:
                    partsInfo[part['partId']]['type'] = TARGET_PARTS_TYPES.ARMORED_FIRING
                else:
                    partsInfo[part['partId']]['type'] = TARGET_PARTS_TYPES.NOT_ARMORED_FIRING
            elif part['isArmored']:
                partsInfo[part['partId']]['type'] = TARGET_PARTS_TYPES.ARMORED_STATIC
            else:
                partsInfo[part['partId']]['type'] = TARGET_PARTS_TYPES.NOT_ARMORED_STATIC

        return partsInfo

    def onScenarioSetText(self, textID, colorID):
        self.__hintManager.showCustomHint(5, localizeHUD(textID), colorID)

    def onPartFlagSwitchedNotification(self, partID, flagID, flagValue):
        if self.__smm.state > SPECTATOR_MODE_STATES.OFF or EntityStates.inState(BigWorld.player(), EntityStates.OBSERVER | EntityStates.DEAD):
            return
        ui = self.__getBattleUI()
        if ui:
            if flagID == PART_FLAGS.FIRE:
                self.__isFire = flagValue
                if flagValue:
                    ui.reportFire(localizeHUD(self.getHolidayLocal('HUD_START_FIRE')), 1)
                else:
                    ui.reportFire(localizeHUD('hud_stop_fire'), 0)

    def reportEngineOverheat(self):
        self.__isEngineOverheated = True
        ui = self.__getBattleUI()
        if ui:
            ui.reportEngineOverheat(localizeHUD(self.getHolidayLocal('HUD_MESSAGE_ENGINE_OVERHEAT')))

    def onUpdateEngineState(self, newStates):
        """
        @param <list>newStates:
        """
        ui = self.__getBattleUI()
        if ui:
            if HUD_MODULE_DAMAGED not in newStates and HUD_MODULE_DESTROYED not in newStates:
                ui.uiClearTextLabel('engineOverheat')
            elif HUD_MODULE_NORMAL in newStates:
                ui.uiCallTextLabel('engineOverheat', localizeHUD('HUD_MESSAGE_ENGINE_DAMAGED_LESS_AFTERBURN'))
            elif HUD_MODULE_DAMAGED in newStates:
                ui.uiCallTextLabel('engineOverheat', localizeHUD('HUD_MESSAGE_ENGINE_DAMAGED_LESS_AFTERBURN'))
            else:
                ui.uiCallTextLabel('engineOverheat', localizeHUD('HUD_MESSAGE_CANNOT_BOOST_ENGINE_DEAD'))

    def reportOverheatedGun(self):
        ui = self.__getBattleUI()
        if ui:
            ui.reportStatusGun(localizeHUD('HUD_MESSAGE_GUN_OVERHEAT'))

    def reportNoShell(self, shellID, result):
        ui = self.__getBattleUI()
        if ui and result in self.__shellDescriptions:
            if result in self.__shellDescriptionsSpeech:
                GameSound().voice.play(self.__shellDescriptionsSpeech[result][shellID])
                GameSound().ui.postEvent('Play_hud_no_equipment')
            msg = localizeHUD(self.__shellDescriptions[result][shellID])
            if UPDATABLE_TYPE.BOMB == shellID:
                ui.reportOutOfBombs(msg)
            elif UPDATABLE_TYPE.ROCKET == shellID:
                ui.reportOutOfAmmo(msg)

    def __updateAltitude(self, owner):
        ui = self.__getBattleUI()
        if ui:
            alt = owner.getAltitudeAboveObstacle()
            arData = db.DBLogic.g_instance.getArenaData(BigWorld.player().arenaType)
            altWater = owner.position.y / WORLD_SCALING + self.getSeaLevel()
            ui.updateAltitude(alt, altWater)
            if EntityStates.inState(BigWorld.player(), EntityStates.GAME):
                isLowAltitudeWarningVisible = alt < WARNING_ALTITUDE_LEVEL
                if self.changeWarningIndicator(WarningType.LOW_ALTITUDE, isLowAltitudeWarningVisible):
                    ui.updateWarningIndicator(WarningType.LOW_ALTITUDE, isLowAltitudeWarningVisible)

    def __updateBorderWarningIndicator(self, owner, ui):
        if self.__arenaBounds:
            left = 10000000000.0
            right = -10000000000.0
            top = 10000000000.0
            bottom = -10000000000.0
            for point in self.__arenaBounds:
                left = min(left, point.x)
                right = max(right, point.x)
                top = min(top, point.z)
                bottom = max(bottom, point.z)

            yaw = owner.yaw * 180.0 / math.pi
            distanceWarningVisible = right - owner.position.x < WARNING_DISTANCE_TO_MAP_BORDER and yaw > 0 and yaw < 180 or owner.position.x - left < WARNING_DISTANCE_TO_MAP_BORDER and yaw < 0 and yaw > -180 or bottom - owner.position.z < WARNING_DISTANCE_TO_MAP_BORDER and yaw > -90 and yaw < 90 or owner.position.z - top < WARNING_DISTANCE_TO_MAP_BORDER and (yaw < -90 or yaw > 90)
            if self.testWarningIndicator(WarningType.AUTOPILOT):
                distanceWarningVisible = False
            if self.changeWarningIndicator(WarningType.BORDER_TOO_CLOSE, distanceWarningVisible):
                ui.updateWarningIndicator(WarningType.BORDER_TOO_CLOSE, distanceWarningVisible)

    def stopTimerUpdate(self):
        self.__timerUpdateEnabled = False

    def updateUIWeaponDispersion(self):
        self.updateUIWeaponRange()
        self.__updateTargets()

    def updateUIWeaponRange(self, frontend = False):
        owner = BigWorld.player()
        avatarInfo = GameEnvironment.getClientArena().getAvatarInfo(owner.id)
        shellsRange = owner.controllers['shellController'].getMaxRocketFlightRange()
        self.__forestallingPoint.setBulletSpeed(owner.controllers['weapons'].bulletSpeedForMostLargeCaliberGroup)
        self.__attackRange = max(self.gunAttackRange, shellsRange)
        self.__forestallingPoint.setBulletRange(self.gunAttackRange, self.__getFPAttackRangeFromDPS(), avatarInfo['settings'].airplane.level, self.__movingTarget.getTargetMatrix().defaultLength, self.__movingTarget.getTargetMatrix())
        self.__movingTarget.getTargetMatrix().bulletRange = self.gunAttackRange

    def __getFPAttackRangeFromDPS(self):
        gunsGroups = BigWorld.player().controllers['weapons'].getGunGroups()
        groupIndex = 0
        groupDps = 0.0
        for i, group in enumerate(gunsGroups):
            if group.dps > groupDps:
                groupDps = group.dps
                groupIndex = i

        attackRange = gunsGroups[groupIndex].gunDescription.bulletFlyDist
        return attackRange

    @property
    def gunAttackRange(self):
        if self.__gunAttackRange < 0.0:
            self.__gunAttackRange = BigWorld.player().controllers['weapons'].getWeaponGroupsMaxAttackRange()
        return self.__gunAttackRange

    def getForestallingPointScreenPos(self):
        if not self.__forestallingPoint.isVisible():
            return None
        matrix = Math.Matrix(self.__forestallingPoint.matrixProvider)
        pos = BigWorld.worldToScreen(matrix.translation)
        if pos.x < 0 or pos.x > BigWorld.screenWidth() or pos.y < 0 or pos.y > BigWorld.screenHeight() or pos.z < 0:
            return None
        dist = self.__forestallingPoint.getFadeDistance()
        if BigWorld.player().position.distTo(matrix.translation) > dist:
            return None
        else:
            return pos

    def getForestallingPointWorldPos(self):
        matrix = Math.Matrix(self.__forestallingPoint.matrixProvider)
        return matrix.translation

    def disableForestallingPointUpdate(self, value):
        self.__forestallingPoint.disableUpdate(value)

    def disableBombTargetUpdate(self, value):
        self.__bombTarget.disableUpdate(value)

    def getBombingPointWorldPos(self):
        if self.__bombTarget is None or self.__bombTarget.matrixProvider is None:
            return
        else:
            matrix = Math.Matrix(self.__bombTarget.matrixProvider)
            return matrix

    def setBombingVisibility(self, value):
        self.__visibleBombing = value

    def onPartStateChanging(self, partData):
        if partData.partTypeData.componentType not in PART_TYPES_TO_ID:
            return
        else:
            damageReason = partData.damageReason
            ui = self.__getBattleUI()
            if ui:
                if not EntityStates.inState(BigWorld.player(), EntityStates.OBSERVER):
                    self.setModuleStates(partData.partTypeData.componentType)
                partTypeStr = self.__getPartTypeStr(partData.partID)
                if partTypeStr:
                    authorData = GameEnvironment.getClientArena().getAvatarInfo(partData.authorID)
                    partName = localizeHUD('hud_aircraft_module_' + partTypeStr)
                    messageType = MESSAGE_TYPE_UI_COLOR_YELLOW
                    msg = None
                    stateID = partData.stateID
                    if isCrewPart(partTypeStr):
                        if damageReason not in [DAMAGE_REASON.FIRING, DAMAGE_REASON.DESTRUCTION]:
                            if stateID == HUD_MODULE_DESTROYED:
                                msg = localizeHUD('UI_CREW_DESTROYED').format(crew=partName)
                            elif damageReason == DAMAGE_REASON.REPAIRING and stateID == HUD_MODULE_DAMAGED:
                                messageType = MESSAGE_TYPE_UI_COLOR_GREEN
                                msg = localizeHUD('UI_CREW_REPAIRED').format(crew=partName)
                    elif authorData:
                        if 'Engine' != partTypeStr:
                            return
                        playerName = authorData.get('playerName', None)
                        if playerName is not None and authorData['classID'] == EntitySupportedClasses.AvatarBot:
                            playerName = playerName.replace('>', '&gt;')
                            playerName = playerName.replace('<', '&lt;')
                        if damageReason == DAMAGE_REASON.OBSTACLE or damageReason == DAMAGE_REASON.TERRAIN:
                            msg = localizeHUD('ui_ramming_module_damaged').format(module=partName)
                        elif damageReason == DAMAGE_REASON.RAMMING:
                            if playerName is not None:
                                ico = self.__generateObjectIco(str(authorData['settings'].airplane.planeType))
                                msg = localizeHUD('ui_ramming_module_damaged_by_plane').format(module=partName, ico=ico, player=playerName)
                        elif damageReason == DAMAGE_REASON.BULLET:
                            if playerName is not None:
                                ico = self.__generateObjectIco(str(authorData['settings'].airplane.planeType))
                                if stateID == HUD_MODULE_DAMAGED:
                                    msg = localizeHUD('ui_module_damaged_by_player').format(player=playerName, ico=ico, module=partName)
                                elif stateID == HUD_MODULE_DESTROYED:
                                    msg = localizeHUD('ui_module_destroyed_by_player').format(player=playerName, ico=ico, module=partName)
                            elif stateID == HUD_MODULE_DAMAGED:
                                msg = localizeHUD('ui_module_damaged_by_turret').format(module=partName)
                            elif stateID == HUD_MODULE_DESTROYED:
                                msg = localizeHUD('ui_module_destroyed_by_turret').format(module=partName)
                        elif damageReason == DAMAGE_REASON.REPAIRING and stateID == HUD_MODULE_NORMAL:
                            messageType = MESSAGE_TYPE_UI_COLOR_GREEN
                            msg = localizeHUD('UI_MODULE_REPAIRED').format(module=partName)
                    if msg:
                        ClientLog.g_instance.gameplay('Damage: %s' % msg.encode('utf-8'))
                        ui.onPartFlagSwitchedNotification(msg, messageType)
            return

    def onPartFlagSwitchedOn(self, partId, flagID, authorID):
        pass

    def __getPartTypeStr(self, partID):
        partSettings = BigWorld.player().settings.airplane.getPartByID(partID)
        if partSettings:
            partTypeData = partSettings.getFirstPartType()
            partTypeStr = partTypeData.componentType
            return partTypeStr
        else:
            return None
            return None

    def setBattleDuration(self, battleDuration):
        ui = self.__getBattleUI()
        if ui:
            ui.setBattleDuration(battleDuration)

    def uiCall(self, func, *methodArgs):
        ui = self.__getBattleUI()
        if ui:
            if ui.isInited:
                ui.uiCall(func, *methodArgs)
            else:
                LOG_WARNING("uiCall - UI can't initialized!", func)

    def sendMessageToFlash(self, path):
        ui = self.__getBattleUI()
        if ui:
            ui.onPartFlagSwitchedNotification(localizeMessages('LOBBY_MSG_SCREENSHOT').format(adress=path), MESSAGE_TYPE_UI_COLOR_GREEN)

    def initSpeedIndicator(self, minSpeed, maxSpeed, optSpeed):
        pass

    def updateSpeedIndicator(self, speed, diffSpeed):
        pass

    def updateAfterBurningTime(self, forsageTime):
        """
        send to flash forsage time
        @param <float>: forsageTime
        """
        self.uiCall('hud.updateAfterBurningTime', forsageTime)

    def autoAlightFromDestroyedTransport(self):
        self.switchVehicle(True)

    def onSwitchedVehicle(self, ownerVehicleID, curVehicleID, lastVehicleID):
        LOG_TRACE('HUD: onSwitchedVehicle', ownerVehicleID, curVehicleID, lastVehicleID)
        if not EntityStates.inState(BigWorld.player(), EntityStates.GAME | EntityStates.WAIT_START | EntityStates.PRE_START_INTRO):
            if not self.isLivePlayers():
                ca = GameEnvironment.getClientArena()
                if ca.isAllServerDataReceived():
                    for id, avatarInfo in ca.avatarInfos.iteritems():
                        LOG_TRACE('HUD: onSwitchedVehicle', id, avatarInfo['stats']['flags'] if 'stats' in avatarInfo else None, avatarInfo['playerName'])

                return
        ui = self.__getBattleUI()
        if ui:
            ui.uiClearTextLabel('spectatorModeInfoAboutTypeDeath')
        self.__flapsChangeState(False, '')
        if self.__smm.state == SPECTATOR_MODE_STATES.INITIALIZED:
            self.__smm.setState(SPECTATOR_MODE_STATES.OBSERVER)
        curVehicle = self.entityList.get(curVehicleID, None)
        if curVehicle:
            self.__markers.deactivateEntity(curVehicle)
            self.__needRefreshObserverInfo = False
            self.__refreshObserverInfo(curVehicle)
        else:
            self.__needRefreshObserverInfo = True
            LOG_DEBUG('onSwitchedVehicle - need reinit data for observer')
        if lastVehicleID != ownerVehicleID:
            lastVehicle = self.entityList.get(lastVehicleID, None)
            if lastVehicle is not None:
                self.__markers.activateEntity(lastVehicle)
        return

    def updateSpectator(self, vehicleID):
        if self.__needRefreshObserverInfo:
            self.__needRefreshObserverInfo = False
            self.__refreshObserverInfo(BigWorld.entities[vehicleID])

    def __refreshObserverInfo(self, curVehicle):
        self.__navigationWindowsManager.setBeamMatrix(curVehicle.matrix)
        ui = self.__getBattleUI()
        if ui:
            self.uiCall('hud.onSwitchedVehicle', curVehicle.id)
            ui.initHealthmeter(curVehicle)
            ui.initVarioAndSpeed(curVehicle)
            self.uiCall('hud.damagePanelInit')
            ui.initDamageScheme(self.__getDamageScheme(curVehicle))
        self.__lastPartStates.clear()
        self.__initInstalledParts(curVehicle)
        self.setModuleStates(None, curVehicle.id)
        self.__entityesHud.updateSpectator(curVehicle.id)
        return

    def tryUseMissingFlaps(self, isUp):
        """
        show info about missing flaps
        @param <bool>: isUp
        """
        self.__flapsChangeState(isUp, 'HUD_MESSAGE_NO_FLAPS')

    def updateFlaps(self, isUp):
        """
        show info about used flaps
        @param <bool>: isUp
        """
        self.__flapsChangeState(isUp, 'HUD_MESSAGE_FLAPS_DRAWN')

    def __flapsChangeState(self, isUp, locID):
        if isUp != self.__flapsState:
            self.__flapsState = isUp
            ui = self.__getBattleUI()
            if ui:
                if isUp:
                    ui.uiCallTextLabel('flaps', localizeHUD(locID))
                else:
                    ui.uiClearTextLabel('flaps')

    def setHudCrosshairType(self, mouseMode):
        pass

    def onHideModalScreen(self, movieName = None):
        self.setVisibility(True)
        player = BigWorld.player()
        if player is not None and 'tutorialManager' in player.controllers:
            player.controllers['tutorialManager'].onHideModalScreen(movieName)
        return

    def onReportBattleResult(self, clientBattleResult):
        self.stopTimerUpdate()

    def onReportDestruction(self, killingInfo):
        avatarID = killingInfo.get('victimID', None)
        if avatarID is not None and avatarID in self.__entityCommands:
            commandID = self.__entityCommands[avatarID][1]
            self.uiCall('hud.entityCommands', avatarID if commandID not in [ChatMessagesStringID.JOIN_ME_ENEMY, ChatMessagesStringID.ENEMY_MY_AIM_ENEMY] else self.__entityCommands[avatarID][0], commandID, False)
            del self.__entityCommands[avatarID]
        damageType = killingInfo.get('lastDamageType', None)
        LOG_DEBUG('reportDestruction', killingInfo, damageType)
        self.reportDestruction(killingInfo, damageType)
        return

    def onReportGainAward(self, awardInfo):
        self.reportGainAward(awardInfo)

    def onHideBackendGraphics(self):
        self.setVisibility(False)
        GUI.mcursor().position = (0, 0)
        GameEnvironment.getInput().setIntermissionMenuMode(True, self.isFlashVisible() and EntityStates.inState(BigWorld.player(), EntityStates.GAME))

    def onNewAvatarsInfo(self, newAvatarsList = None):
        if not self.__isAllVisibleEntitiesCollected:
            self.__isAllVisibleEntitiesCollected = True
            self.__navigationWindowsManager.add(BigWorld.player())
            self.__collectAllVisibleEntities()
            if self.__getBattleUI() and not self.isTutorial():
                self.__updateMinimapAndRadarVisibility()
            performanceSpecsDescriptions = self.__getPerformanceSpecsDescriptions(BigWorld.player(), True)
            if self.__getBattleUI() and self.__getBattleUI().isInited and not self.isBattleLoadingDispossessed():
                self.__battleLoading.sendHintsData(performanceSpecsDescriptions.desc)

    def onAllServerDataReceived(self):
        if self.__arenaLoaded:
            self.initMarkers()

    def onLaunch(self, avatarID):
        if self.__spectatorMode or self.__miniScreen is None:
            return
        else:
            if self.targetEntity is not None and self.targetEntity.id == avatarID and self.targetEntity.inWorld:
                self.__miniScreenTargetID = None
                self.__miniScreenTargetInfoUpdate(self.targetEntity)
            return

    def updateAvatarPartStates(self, id, partId, stateID, componentType):
        player = BigWorld.player()
        if id in (player.curVehicleID, player.id) and (componentType is None or componentType in PART_TYPES_TO_ID):
            self.setModuleStates(None, id)
        if self.targetEntity and self.targetEntity.id == id and (componentType is None or componentType in PART_TYPES_TO_ID):
            self.setModuleStates(componentType, id, True)
        return

    def onReceiveAllTeamObjectsData(self):
        self.__initTeamObjectsGroups()

    def setModuleStates(self, changedModuleType = None, entityID = None, isTarget = False):
        LOG_DEBUG('hud.setModuleStates', changedModuleType, entityID, isTarget)
        avatar = BigWorld.player()
        if entityID is not None:
            avatar = BigWorld.entities.get(entityID, None)
            if avatar is None:
                LOG_DEBUG('setModuleStates - avatar out of world', entityID)
                return
        if EntityStates.inState(avatar, EntityStates.DESTROYED | EntityStates.DESTROYED_FALL):
            LOG_DEBUG('hud.setModuleStates: avatar already destroyed!')
            return
        else:
            if self.__installedParts is None and not isTarget or self.__installedPartsTarget is None and isTarget:
                self.__initInstalledParts(avatar, isTarget)
            installedParts = self.__installedParts
            if isTarget:
                installedParts = self.__installedPartsTarget
            worthStates = dict()
            for partID, partState in avatar.partStates:
                partSettings = avatar.settings.airplane.getPartByID(partID)
                if partSettings:
                    partUpgrade = installedParts.get(partID)
                    if partUpgrade is None or not partUpgrade.componentType:
                        LOG_DEBUG('setModuleStates - part not installed', partID)
                        continue
                    partTypeData = None
                    for upgradeData in partSettings.upgrades.itervalues():
                        if upgradeData.componentType:
                            partTypeData = upgradeData
                            break

                    if partTypeData is None:
                        LOG_ERROR('setModuleStates - empty part data', partID)
                        continue
                    partTypeStr = partTypeData.componentType
                    componentPosition = partTypeData.componentPosition
                    if changedModuleType is None or partTypeStr == changedModuleType:
                        hudPartID = PART_TYPES_TO_ID.get(partTypeStr)
                        if hudPartID is not None:
                            existWorthState = None
                            existWorthPart = worthStates.get(partTypeStr)
                            if existWorthPart is None:
                                worthStates[partTypeStr] = dict()
                            else:
                                existWorthState = existWorthPart.get(componentPosition)
                            if existWorthState is None or existWorthState < partState:
                                worthStates[partTypeStr][componentPosition] = partState

            self.__setModuleStates(worthStates, isTarget, entityID)
            return

    def __setModuleStates(self, worthStates, isTarget, entityID):
        LOG_DEBUG('hud.__setModuleStates', worthStates, isTarget)
        ui = self.__getBattleUI()
        if ui:
            playSoundCritStart = None
            playSoundCritFixed = None
            lastPartStates = self.__lastPartStates
            if isTarget:
                lastPartStates = self.__lastPartStatesTarget
            changedStates = list()
            for partTypeStr, partsData in worthStates.iteritems():
                hudPartID = PART_TYPES_TO_ID.get(partTypeStr)
                if hudPartID is not None:
                    for position, state in partsData.iteritems():
                        if partTypeStr not in lastPartStates:
                            lastPartStates[partTypeStr] = dict()
                        lastState = lastPartStates[partTypeStr].get(position)
                        if not lastState or lastState != state:
                            if lastState and not isTarget:
                                if state == HUD_MODULE_DESTROYED:
                                    if partTypeStr == 'Pilot':
                                        playSoundCritStart = 'Play_crit_pilot'
                                    else:
                                        playSoundCritStart = 'Play_crit_red_start'
                                elif state == HUD_MODULE_DAMAGED:
                                    playSoundCritFixed = 'Play_crit_red_fixed'
                            changedStates.append([hudPartID, state, position])
                            lastPartStates[partTypeStr][position] = state
                            self.ePartStateChanging(partTypeStr, state, position, entityID)

            if playSoundCritStart:
                GameSound().ui.postEvent(playSoundCritStart)
            if playSoundCritFixed:
                GameSound().ui.postEvent(playSoundCritFixed)
            if changedStates:
                ui.setModuleStates(changedStates, isTarget)
        return

    def onVictimInformAboutCrit(self, partID, victimID, partState):
        LOG_DEBUG('hud.onVictimInformAboutCrit', partID, victimID, partState)
        if victimID == BigWorld.player().id:
            LOG_DEBUG('onVictimInformAboutCrit: victim is avatar', victimID)
            return
        else:
            avatar = BigWorld.entities.get(victimID, None)
            if avatar is None:
                LOG_DEBUG('onVictimInformAboutCrit: avatar out of world', victimID)
                return
            if partState == HUD_MODULE_DESTROYED:
                GameSound().ui.postEvent('Play_crit_red_NPC')
            partSettings = avatar.settings.airplane.getPartByID(partID)
            if partSettings:
                partTypeData = None
                for upgradeData in partSettings.upgrades.itervalues():
                    if upgradeData.componentType:
                        partTypeData = upgradeData
                        break

                if partTypeData is None:
                    LOG_WARNING('onVictimInformAboutCrit - empty part data', partID)
                    return
                hudPartID = PART_TYPES_TO_ID.get(partTypeData.componentType)
                self.__markers.setModuleState(victimID, hudPartID, partState)
            return

    def __responseBattleHints(self):
        performanceSpecsDescriptions = self.__getPerformanceSpecsDescriptions(BigWorld.player(), False)
        if performanceSpecsDescriptions is None:
            return
        else:
            ownerInfo = GameEnvironment.getClientArena().getAvatarInfo(BigWorld.player().id)
            if ownerInfo is not None:
                settings = ownerInfo['settings']
                hintData = []
                for hintObj in db.DBLogic.g_instance.getHelpHints().allHints:
                    hintPlaneTypeArray = hintObj.type.split(',')
                    if PLANE_TYPE_NAME_HINTS[settings.airplane.planeType] in hintPlaneTypeArray or 'ALL' in hintPlaneTypeArray:
                        if hintObj.hasBombs and not performanceSpecsDescriptions.hasBombs or hintObj.hasRockets and not performanceSpecsDescriptions.hasRockets or hintObj.hasGunner and not BigWorld.player().hasGunner() or hintObj.hasRocketsOrBombs and not performanceSpecsDescriptions.hasBombs and not performanceSpecsDescriptions.hasRockets or hintObj.highRise and performanceSpecsDescriptions.desc[AIRCRAFT_CHARACTERISTIC.OPTIMAL_HEIGHT].value < OPTIMAL_HEIGHT_FOR_HINTS:
                            LOG_DEBUG('__sendHintsData - failure to conditions')
                        else:
                            hintData.append(_Hints([ localizeTutorial(text) for text in hintObj.locText ], hintObj.imgPathBlind[:] if Settings.g_instance.getGameUI()['alternativeColorMode'] else hintObj.imgPath[:], hintObj.id))

                if hintData:
                    self.uiCall('responseBattleHints', hintData)
            return

    def __getPerformanceSpecsDescriptions(self, owner, isRefresh = False):
        if not isRefresh:
            performanceSpecsDescriptionsCached = self.__performanceSpecsDescriptions.get(owner.id, None)
            if performanceSpecsDescriptionsCached is not None:
                return performanceSpecsDescriptionsCached
        avatarsInfo = GameEnvironment.getClientArena().avatarInfos
        ownerInfo = avatarsInfo.get(owner.id, None)
        if ownerInfo is None:
            return
        else:
            hasBombs, hasRockets = False, False
            shellsInitialInfo = owner.controllers['shellController'].getShellGroupsInitialInfo()
            for groupID, weaponData in shellsInitialInfo.items():
                if weaponData['shellID'] == UPDATABLE_TYPE.BOMB and weaponData['description'] is not None:
                    hasBombs = True
                elif weaponData['shellID'] == UPDATABLE_TYPE.ROCKET and weaponData['description'] is not None:
                    hasRockets = True

            if (hasBombs or hasRockets) and ownerInfo.get('shellsCount', None) is None:
                return
            projectiles = getProjectiles(owner.globalID, ownerInfo.get('shellsCount', None))
            performanceSpecsDescriptions = getPerformanceSpecsDescriptions(owner.globalID, True, projectiles, ownerInfo.get('equipment', None), maxHealth=ownerInfo.get('maxHealth', None))
            self.__performanceSpecsDescriptions[owner.id] = _PerformanceSpecsDescriptions(performanceSpecsDescriptions, hasRockets, hasBombs)
            return self.__performanceSpecsDescriptions[owner.id]

    def UIinitialized(self):
        performanceSpecs = self.__getPerformanceSpecsDescriptions(BigWorld.player(), False)
        self.__battleLoading.initialized(self.__getBattleUI(), None if performanceSpecs is None else performanceSpecs.desc)
        self.__responseBattleHints()
        self.updateConsumables(BigWorld.player().consumables)
        gunAttackRange = MeasurementSystem().getMeters(BigWorld.player().controllers['weapons'].getWeaponGroupsMaxAttackRange() / WORLD_SCALING)
        self.uiCall('hud.initEffectiveShootingDist', round(gunAttackRange, 2))
        ui = self.__getBattleUI()
        if ui:
            ui.initDamageScheme(self.__getDamageScheme())
        self.__initInstalledParts()
        self.setModuleStates()
        self.uiCall('hud.setFPColor', Settings.g_instance.colorPointIndexFP)
        self.uiCall('hud.helpEnabled', True)
        if BattleReplay.isPlaying():
            self.uiCall('hud.setEnableReplays')
        return

    def onMovieLoaded(self, movieName, movieInstance):
        from gui.Scaleform import main_interfaces
        if movieName == main_interfaces.GUI_SCREEN_UI:
            self.doBattleUILoaded()
            self.setVisibility(True)
        BigWorld.player().onFireChange(0)
        if movieInstance.isModalMovie:
            self.setVisibility(False)

    def addInputListeners(self, processor):
        uiInited = lambda ui: (False if ui is None else ui.isInited)
        predicateCommands = [InputMapping.CMD_REPLAY_SHOW_CURSOR,
         InputMapping.CMD_INTERMISSION_MENU,
         InputMapping.CMD_SHOW_PLAYERS_INFO,
         InputMapping.CMD_SHOW_CURSOR,
         InputMapping.CMD_VISIBILITY_HUD,
         InputMapping.CMD_CHAT_ON_OFF]
        predicateCommands.extend(InputMapping.CHAT_COMMANDS)
        predicateCommands.extend(InputMapping.EQUIPMENT_COMMANDS)
        spectatorModeCommands = self.__smm.getSpectatorModeCommands()
        predicateCommands += spectatorModeCommands
        dynamicCameraSwitchStatesCommands = self.__smDynamicCameraManager.getSwitchStatesCommands()
        predicateCommands += dynamicCameraSwitchStatesCommands.iterkeys()
        for command in dynamicCameraSwitchStatesCommands.iterkeys():
            processor.addPredicate(command, lambda : not BattleReplay.isPlaying() and self.__smm.state == SPECTATOR_MODE_STATES.DYNAMIC_CAMERA)

        processor.addListeners(InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE0, lambda : self.spectatorModeDynamicCameraSwitch(dynamicCameraSwitchStatesCommands.get(InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE0)))
        processor.addListeners(InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE1, lambda : self.spectatorModeDynamicCameraSwitch(dynamicCameraSwitchStatesCommands.get(InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE1)))
        processor.addListeners(InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE2, lambda : self.spectatorModeDynamicCameraSwitch(dynamicCameraSwitchStatesCommands.get(InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE2)))
        processor.addListeners(InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE3, lambda : self.spectatorModeDynamicCameraSwitch(dynamicCameraSwitchStatesCommands.get(InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE3)))
        processor.addListeners(InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE4, lambda : self.spectatorModeDynamicCameraSwitch(dynamicCameraSwitchStatesCommands.get(InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE4)))
        processor.addListeners(InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE5, lambda : self.spectatorModeDynamicCameraSwitch(dynamicCameraSwitchStatesCommands.get(InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE5)))
        for command in spectatorModeCommands:
            processor.addPredicate(command, lambda : not BattleReplay.isPlaying() and self.__smm.state not in [SPECTATOR_MODE_STATES.INITIALIZED, SPECTATOR_MODE_STATES.OFF, SPECTATOR_MODE_STATES.OUTRO])

        processor.addListeners(InputMapping.CMD_SPECTATOR_MODE_OBSERVER, lambda : self.__smm.setState(SPECTATOR_MODE_STATES.OBSERVER))
        processor.addListeners(InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA, lambda : self.__smm.setState(SPECTATOR_MODE_STATES.DYNAMIC_CAMERA))
        for command in predicateCommands:
            processor.addPredicate(command, lambda : uiInited(self.__battleUI))

        import BattleReplay
        processor.addPredicate(InputMapping.CMD_HELP, lambda : uiInited(self.__battleUI))
        cmdMap = InputMapping.g_instance
        processor.addListeners(InputMapping.CMD_INTERMISSION_MENU, self.onEscButtonPressed)
        processor.addListeners(InputMapping.CMD_MINIMAP_ZOOM_IN, self.zoomInRadar)
        processor.addListeners(InputMapping.CMD_MINIMAP_ZOOM_OUT, self.zoomOutRadar)
        processor.addListeners(InputMapping.CMD_SHOW_MAP, None, None, lambda fired: self.showMap(fired, [InputMapping.CMD_SHOW_MAP, InputMapping.CMD_SHOW_CURSOR], not GameEnvironment.getInput().isFired(InputMapping.CMD_SHOW_CURSOR)))
        for command in InputMapping.CHAT_COMMANDS:
            processor.addListeners(command, None, None, functools.partial(self.showChatMessage, command))

        processor.addListeners(InputMapping.CMD_HELP, None, None, lambda fired: self.onHelp(fired))
        processor.addListeners(InputMapping.CMD_SHOW_PLAYERS_INFO, None, None, lambda fired: self.onPlayersInfo(fired))
        processor.addListeners(InputMapping.CMD_SHOW_CURSOR, None, None, lambda fired: self.visibilityMouseCursor(fired))
        processor.addListeners(InputMapping.CMD_REPLAY_SHOW_CURSOR, None, None, lambda fired: self.visibilityMouseCursor(fired))
        processor.addListeners(InputMapping.CMD_VISIBILITY_HUD, None, None, lambda fired: self.setFlashVisibility(fired))
        processor.addListeners(InputMapping.CMD_MINIMAP_SIZE_INC, None, None, lambda fired: (self.minimap.incMapSize() if fired else ()))
        processor.addListeners(InputMapping.CMD_MINIMAP_SIZE_DEC, None, None, lambda fired: (self.minimap.decMapSize() if fired else ()))
        processor.addListeners(InputMapping.CMD_NEXT_VEHICLE_WHEN_DEAD, lambda : self.switchVehicle(True))
        processor.addPredicate(InputMapping.CMD_NEXT_VEHICLE_WHEN_DEAD, lambda : self.__smm.state not in [SPECTATOR_MODE_STATES.FILM])
        processor.addListeners(InputMapping.CMD_PREV_VEHICLE_WHEN_DEAD, lambda : self.switchVehicle(False))
        processor.addPredicate(InputMapping.CMD_PREV_VEHICLE_WHEN_DEAD, lambda : self.__smm.state not in [SPECTATOR_MODE_STATES.FILM])
        for command in InputMapping.EQUIPMENT_COMMANDS:
            processor.addListeners(command, functools.partial(self.__equipmentManager.useEquipment, command))

        isEntityesHudInited = lambda : self.__entityesHud is not None
        processor.addPredicate(InputMapping.CMD_LOCK_TARGET, isEntityesHudInited)
        processor.addPredicate(InputMapping.CMD_LOCK_TARGET, self.isEntityesLockEnabled)
        processor.addPredicate(InputMapping.CMD_NEXT_TARGET, isEntityesHudInited)
        processor.addPredicate(InputMapping.CMD_NEXT_TARGET_TEAM_OBJECT, isEntityesHudInited)
        processor.addPredicate(InputMapping.CMD_LOCK_TARGET_IN_SCREEN_CENTER, isEntityesHudInited)
        processor.addListeners(InputMapping.CMD_LOCK_TARGET_IN_SCREEN_CENTER, self.__entityesHud.tryToSelectAndLockEntity)
        processor.addListeners(InputMapping.CMD_LOCK_TARGET, lambda : self.setTargetLock(self.__entityesHud.captureTargetsEnabled))
        processor.addListeners(InputMapping.CMD_NEXT_TARGET, lambda : self.selectNextEntity(EntityTypes.AIRCRAFT_ENTITY))
        processor.addListeners(InputMapping.CMD_NEXT_TARGET_TEAM_OBJECT, lambda : self.selectNextEntity(EntityTypes.TEAM_OBJECT_ENTITY))
        processor.addListeners(InputMapping.CMD_FLAPS_UP, None, None, self.flapsMessage)
        processor.addListeners(InputMapping.CMD_CHAT_ON_OFF, None, None, lambda fired: Settings.g_instance.setGameUIValue('isChatEnabled', not Settings.g_instance.getGameUI()['isChatEnabled']))
        processor.addListeners(InputMapping.CMD_SKIP_INTRO, self.__skipIntroCommandEvent)
        return

    def flapsMessage(self, value):
        if not BattleReplay.isPlaying():
            BattleReplay.g_replay.onFlapsMessage(value)
        if value and BigWorld.player().autopilot:
            return None
        elif preparedBattleData[BigWorld.player().globalID].flaps:
            return self.updateFlaps(value)
        else:
            return self.tryUseMissingFlaps(value)

    def isEntityesLockEnabled(self):
        if self.targetEntity is None or self.targetEntity.id not in self.entityList:
            return False
        else:
            return True

    def switchVehicle(self, isNext):
        LOG_TRACE('HUD::switchVehicle', isNext)
        if not self.isLivePlayers():
            return
        ui = self.__getBattleUI()
        if ui:
            ui.uiClearTextLabel('spectatorModeInfoAboutTypeDeath')
            self.__flapsChangeState(False, '')
        id = self.__vehicleSwitchManager.fire(VEHICLE_SWITCHER_DIRECTIONS.INC if isNext else VEHICLE_SWITCHER_DIRECTIONS.DEC)
        if id != -1:
            BigWorld.player().switchToVehicle(id)

    def isCrewDamaged(self):
        res = list()
        for partTypeStr, partsData in self.__lastPartStates.iteritems():
            hudPartID = PART_TYPES_TO_ID.get(partTypeStr)
            if hudPartID is not None:
                for position, state in partsData.iteritems():
                    if state == HUD_MODULE_DESTROYED:
                        if isCrewPart(partTypeStr):
                            return True

        return False

    def getPartsInCritState(self):
        res = list()
        for partTypeStr, partsData in self.__lastPartStates.iteritems():
            hudPartID = PART_TYPES_TO_ID.get(partTypeStr)
            if hudPartID is not None:
                for position, state in partsData.iteritems():
                    if state == HUD_MODULE_DESTROYED:
                        if not isCrewPart(partTypeStr):
                            res.append(hudPartID)
                            break

        return res

    def isEngineDamaged(self):
        return PART_TYPES_TO_ID['Engine'] in self.getPartsInCritState()

    def isFire(self):
        return self.__isFire

    def isTailOrWingsCrit(self):
        critParts = self.getPartsInCritState()
        partsToTest = [PART_TYPES_TO_ID['Tail'], PART_TYPES_TO_ID['LeftWing'], PART_TYPES_TO_ID['RightWing']]
        for part in partsToTest:
            if part in critParts:
                return True

        return False

    def isEquipmentEnabledForUse(self, equipmentType, mod):
        owner = BigWorld.player()
        if equipmentType == ModsTypeEnum.HP_RESTORE:
            return self.isCrewDamaged()
        if equipmentType in [ModsTypeEnum.FIX_TAIL_AND_WINGS]:
            return self.isTailOrWingsCrit()
        if equipmentType in [ModsTypeEnum.FIRE_EXTINGUISH_MANUAL, ModsTypeEnum.FIRE_EXTINGUISH_AUTO, ModsTypeEnum.FIRE_CHANCE]:
            return self.isFire()
        if equipmentType in (ModsTypeEnum.ENGINE_RESTORE, ModsTypeEnum.AUTO_ENGINE_RESTORE):
            return self.isEngineDamaged()
        if equipmentType == ModsTypeEnum.CLEAR_GUNS_OVERHEAT:
            return owner.controllers['weapons'].isGunsOverHeated(getattr(mod, 'activationValue', 0))
        if equipmentType == ModsTypeEnum.FIRE_WORK:
            return True
        if equipmentType == ModsTypeEnum.CLEAR_ENGINE_OVERHEAT:
            return owner.engineTemperature > getattr(mod, 'activationValue', 0)
        if equipmentType in [ModsTypeEnum.ROLL_MAX_SPEED_CFG,
         ModsTypeEnum.YAW_MAX_SPEED_CFG,
         ModsTypeEnum.PITCH_MAX_SPEED_CFG,
         ModsTypeEnum.LOCK_ENGINE_POWER]:
            return True
        return False

    def updateConsumables(self, consumables):
        """
        @param consumables: <list>
        """
        LOG_DEBUG('updateConsumables', consumables)
        self.__equipmentManager.updateConsumables(consumables)

    def onUseEquipment(self, slotID):
        self.__equipmentManager.onUseEquipment(slotID)

    def updateEquipmentControls(self, consumables):
        self.__equipmentManager.updateEquipmentInputMapping(consumables)

    def isTutorial(self):
        return 'tutorialManager' in BigWorld.player().controllers

    def switchVisibleNickPlayers(self):
        self.uiCall('hud.switchVisibleNickPlayers')

    def restartHUD_QA(self):
        self.doLeaveWorld()
        self.destroy()
        self.__init__()
        self.afterLinking()

    def updateMinimapSize(self):
        self.minimap.notifySizeChange()

    def onMinimapResized(self, newSize):
        self.uiCall('hud.setMapHeight', newSize)
        LOG_TRACE('HUD::onMinimapResized(%f)' % newSize)

    def battleLoadingClose(self):
        LOG_DEBUG('battleLoadingClose')
        self.__battleLoading.dispossess()
        self.__skipIntroCounter.fire()

    def isBattleLoadingDispossessed(self):
        return self.__battleLoading.isDispossessed()

    def doLeaveWorld(self):
        self.__entityList = dict()
        self.__enemyTurretsChecker.destroy()
        self.__enemyTurretsChecker = None
        self.clearTarget()
        GameServiceBase.doLeaveWorld(self)
        return

    def __selectEntity(self, entityId):
        """
        callback from C++ select entity
        @param entityId:
        """
        if self.__clearTargetCallback is not None:
            BigWorld.cancelCallback(self.__clearTargetCallback)
        if entityId in self.entityList:
            self.onTargetEntity(self.entityList[entityId])
        else:
            LOG_WARNING('__selectEntity - entity(%s) not found in entityList!' % entityId)
        return

    def onForceTargetEntity(self, entity):
        """
        callback to C++ - set entity as target
        @param entity:
        """
        if self.__entityesHud:
            self.__entityesHud.selectEntity(entity.id if entity is not None else 0)
        return

    def selectNextEntity(self, entityType):
        if self.__entityesHud:
            if self.targetEntity is not None and self.targetEntity.id in self.entityList and not self.isTargetLock():
                if entityType == EntityTypes.AIRCRAFT_ENTITY and isAvatar(self.targetEntity) or entityType == EntityTypes.TEAM_OBJECT_ENTITY and not isAvatar(self.targetEntity):
                    self.setTargetLock(True)
                    return
            self.__entityesHud.selectNextEntity(entityType)
        return

    def isTargetLock(self):
        """
        return lock or not current selected target
        @return: bool
        """
        if self.__entityesHud:
            return not self.__entityesHud.captureTargetsEnabled
        return False

    def clearTarget(self):
        LOG_DEBUG('___clearTarget - id=(%s)' % self.targetEntity.id if self.targetEntity else None)
        if self.__entityesHud:
            self.setTargetLock(False)
            self.__entityesHud.selectEntity(0)
        if self.targetEntity is not None:
            self.onTargetEntity(None)
        return

    def __setClearTargetCallback(self, entity):
        if entity is self.__targetEntity:
            if self.__clearTargetCallback is not None:
                BigWorld.cancelCallback(self.__clearTargetCallback)
            self.__clearTargetCallback = BigWorld.callback(DELAY_SHOW_DESTROYED_PLANE if isAvatar(entity) else DELAY_SHOW_DESTROYED_GROUNDOBJECT, self.clearTarget)
        return

    def __updateTargetLock(self, isLocked):
        """
        point for all updates lock target
        @param isLocked: <bool>
        """
        BattleReplay.g_replay.notifyTargetLock(isLocked)

    def setTargetLock(self, isLocked):
        if self.__entityesHud:
            self.__entityesHud.captureTargetsEnabled = not isLocked
            self.__updateTargetLock(self.isTargetLock())

    def removeEntityesHudCursorMatrixProvider(self):
        if self.__entityesHud:
            self.__entityesHud.cursorMatrixProvider = None
        return

    def restoreEntityesHudCursorMatrixProvider(self):
        self.__inputProfileChanged()

    def __inputProfileChanged(self):
        if self.__entityesHud:
            if InputMapping.g_instance.currentProfileType in (INPUT_SYSTEM_STATE.MOUSE, INPUT_SYSTEM_STATE.GAMEPAD_DIRECT_CONTROL):
                self.__entityesHud.cursorMatrixProvider = GameEnvironment.getCamera().getDefualtStrategies['CameraStrategyMouse'].cursorMatrixProvider
            else:
                self.__entityesHud.cursorMatrixProvider = None
        return

    @property
    def targetEntity(self):
        return self.__targetEntity

    @targetEntity.setter
    def targetEntity(self, entity):
        self.__targetEntity = entity
        self.eSetTargetEntity(self.__targetEntity)
        if BigWorld.player().battleType == ARENA_TYPE.PVE:
            self.__hintManager.onSetTargetEntity(entity)

    @property
    def entityList(self):
        return self.__entityList

    def setMinimapLimitPosition(self, posX, posY):
        if self.minimap is not None:
            self.minimap.setLimitPosition(posX, posY)
        return

    def __updateSpectatorCamera(self, state):
        params = {}
        if state == SPECTATOR_MODE_STATES.DYNAMIC_CAMERA or state == SPECTATOR_MODE_STATES.FILM:
            self.uiCall('hud.spectatorDynamicCameraState', self.__smDynamicCameraManager.index)
            params['timelineID'] = self.__smDynamicCameraManager.index
        camera = GameEnvironment.getCamera()
        if camera:
            spectatorController = camera.spectator
            if spectatorController:
                if camera.getState() in (CameraState.Spectator, CameraState.SpectatorSide):
                    GameSound().ui.postEvent('Play_hud_switching_camera')
                spectatorController.setState(state, params)
        else:
            LOG_ERROR('Unable to get a camera')

    def __onSpectatorModeSetState(self, state):
        self.uiCall('hud.spectatorMode', state)
        if state in (SPECTATOR_MODE_STATES.OBSERVER, SPECTATOR_MODE_STATES.DYNAMIC_CAMERA, SPECTATOR_MODE_STATES.FILM):
            self.__getBattleUI().setSpectatorHintEnabled(True)
        if state != SPECTATOR_MODE_STATES.OBSERVER:
            self.uiCall('hud.labelClearText', 'spectatorMode')
        self.__updateSpectatorCamera(state)

    def spectatorModeDynamicCameraSwitch(self, newState = -1):
        if newState == -1:
            self.__smDynamicCameraManager.incStateIndex()
        else:
            if newState == self.__smDynamicCameraManager.index:
                return
            self.__smDynamicCameraManager.index = newState
        self.__updateSpectatorCamera(SPECTATOR_MODE_STATES.DYNAMIC_CAMERA)

    def getActiveQuest(self):
        LOG_DEBUG('getActiveQuest')
        BigWorld.player().base.getQuestSelectConsist()

    def sendSituationalPilotSkills(self):
        skills_id = AvatarHelper.getAvatarSkillsList(BigWorld.player())
        skills = []
        for id_ in skills_id:
            skill = SkillDB[id_]
            if skill.crewMemberTypes[0] == SpecializationEnum.PILOT and skill.group == SKILL_GROUP.UNIQUE:
                skills.append({'id': id_,
                 'pathActive': getattr(skill, 'icoHudActivePath', ''),
                 'pathInactive': getattr(skill, 'icoHudPath', ''),
                 'name': getattr(skill, 'name', ''),
                 'description': getattr(skill, 'fullDescription', '')})

        self.uiCall('hud.situationalPilotSkills', skills)

    def onUniqueSkillStateChanged(self, skill_id, is_active):
        self.uiCall('hud.uniqueSkillStateChanged', skill_id, is_active)