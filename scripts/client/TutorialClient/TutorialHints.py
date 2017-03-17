# Embedded file name: scripts/client/TutorialClient/TutorialHints.py
import GameEnvironment
import Keys
import BigWorld
from Helpers.i18n import localizeTutorial
import InputMapping
import Math
from TeamObject import TeamObject
from TutorialClient.TutorialUIWrapper import TutorialUIWrapper
from config_consts import IS_DEVELOPMENT
from consts import AXIS_NAME_TO_INT_MAP, INPUT_SYSTEM_STATE, TutorialHintsInputEnum, INPUT_SYSTEM_PROFILES_LIST_REVERT, WORLD_SCALING, WEP_DISABLE_TEMPERATURE, GUN_OVERHEATING_TEMPERATURE, TUTORIAL_MARKER_ARROW_DELAY, TUTORIAL_HINT_FORCE_SHOW_TIME, TUTORIAL_RELOAD_SHELLS_DELAY, DAMAGE_REASON, SHELL_INDEX
from clientConsts import INPUT_SYSTEM_PROFILES
from debug_utils import LOG_ERROR, LOG_DEBUG
from gui.Scaleform.UI import TutorialCaptionParams
from _performanceCharacteristics_db import airplanes
import math
import copy
import gui.hud
from EntityHelpers import EntityStates
import GlobalEvents
from traceback import print_stack
import updatable.UpdatableManager
ONE_DAY_DELAY = 86400
CONDITION_AFTER_TIMEOUT = 10
DISABLED_KEYS = ['KEY_ESCAPE',
 'KEY_LWIN',
 'KEY_RWIN',
 'KEY_APPS',
 'KEY_DEBUG',
 'KEY_NUMLOCK',
 'KEY_SCROLL',
 'KEY_CAPSLOCK',
 'KEY_SYSRQ',
 'KEY_NONE',
 'KEY_RALT',
 'KEY_LALT',
 'KEY_RCONTROL',
 'KEY_LCONTROL',
 'KEY_TAB']

class GAME_MODES:
    PVP = 'pvp'
    PVE = 'pve'
    ALL = 'all'


class HIDE_MARKER:
    NONE = 0
    HINT_END = 1
    HIDE = 2
    SHOW = 3

    @staticmethod
    def convertStrToID(strVal):
        strToID = {'None': HIDE_MARKER.NONE,
         'HideHint': HIDE_MARKER.HINT_END,
         'Hide': HIDE_MARKER.HIDE,
         'Show': HIDE_MARKER.SHOW}
        return strToID[strVal]

    @staticmethod
    def getNextValue(valueSrc, valueTgt):
        if valueTgt == HIDE_MARKER.SHOW:
            return HIDE_MARKER.NONE
        if valueSrc == HIDE_MARKER.NONE or valueSrc == HIDE_MARKER.HINT_END:
            return valueTgt
        if valueSrc == HIDE_MARKER.HIDE:
            return HIDE_MARKER.HIDE


class VOHint:

    def __init__(self, data, inputIndex, pressAnyKeyHintTimeout):
        self.header = data.header
        self.actionIcon = data.actionIcon
        self.actionBtn = ''
        self.picture = ''
        self.hintText = data.hintText
        self.sizeText = data.sizeText
        if pressAnyKeyHintTimeout > 0:
            self.timeOut = pressAnyKeyHintTimeout * 1000
        if data.commandID != '':
            keysMapping = {'up': InputMapping.getKeyLocalization(InputMapping.getKeyNameByCode(Keys.KEY_UPARROW)),
             'down': InputMapping.getKeyLocalization(InputMapping.getKeyNameByCode(Keys.KEY_DOWNARROW)),
             'left': InputMapping.getKeyLocalization(InputMapping.getKeyNameByCode(Keys.KEY_LEFTARROW)),
             'right': InputMapping.getKeyLocalization(InputMapping.getKeyNameByCode(Keys.KEY_RIGHTARROW))}
            if inputIndex == TutorialHintsInputEnum['mouse']:
                mSet = InputMapping.g_instance.primarySettings
                if data.commandID == 'CMD_PITCH_UP':
                    if mSet.MOUSE_INVERT_VERT:
                        self.picture = 'down_anim'
                    else:
                        self.picture = 'up_anim'
                elif data.commandID == 'CMD_PITCH_DOWN':
                    if mSet.MOUSE_INVERT_VERT:
                        self.picture = 'up_anim'
                    else:
                        self.picture = 'down_anim'
                elif data.commandID == 'CMD_TURN_LEFT':
                    self.picture = 'left_anim'
                elif data.commandID == 'CMD_TURN_RIGHT':
                    self.picture = 'right_anim'
                else:
                    localizedKeys = InputMapping.g_instance.getLocalizedCommandKeysAndAxes(data.commandID)
                    if len(localizedKeys) > 0:
                        self.actionBtn = localizedKeys[len(localizedKeys) - 1]
                        for ind, val in keysMapping.items():
                            if keysMapping[ind] == self.actionBtn:
                                self.picture = ind
                                self.actionBtn = ''
                                break

            elif inputIndex == TutorialHintsInputEnum['keyboard']:
                localizedKeys = InputMapping.g_instance.getLocalizedCommandKeysAndAxes(data.commandID)
                if len(localizedKeys) > 0:
                    self.actionBtn = localizedKeys[len(localizedKeys) - 1]
                    for ind, val in keysMapping.items():
                        if keysMapping[ind] == self.actionBtn:
                            self.picture = ind
                            self.actionBtn = ''
                            break

            elif inputIndex == TutorialHintsInputEnum['joystick'] or inputIndex == TutorialHintsInputEnum['gamepad']:
                joyMapping = {0: {1: 'roll_left_anim',
                     -1: 'roll_right_anim'},
                 1: {1: 'up_anim',
                     -1: 'down_anim'},
                 2: {1: 'fire',
                     -1: 'fire'},
                 3: {1: 'left_anim',
                     -1: 'right_anim'},
                 4: {1: 'forsage',
                     -1: 'forsage'},
                 5: {1: 'left_anim',
                     -1: 'right_anim'}}
                jSet = InputMapping.g_instance.primarySettings
                curAxis = -1
                curAxisDir = 1
                if data.commandID == 'CMD_PITCH_UP':
                    curAxis = jSet.VERTICAL_AXIS
                    curAxisDir = -1 if jSet.INVERT_VERTICAL else 1
                elif data.commandID == 'CMD_PITCH_DOWN':
                    curAxis = jSet.VERTICAL_AXIS
                    curAxisDir = 1 if jSet.INVERT_VERTICAL else -1
                elif data.commandID == 'CMD_TURN_LEFT':
                    curAxis = jSet.HORIZONTAL_AXIS
                    curAxisDir = -1 if jSet.INVERT_HORIZONTAL else 1
                elif data.commandID == 'CMD_TURN_RIGHT':
                    curAxis = jSet.HORIZONTAL_AXIS
                    curAxisDir = 1 if jSet.INVERT_HORIZONTAL else -1
                elif data.commandID == 'CMD_ROLL_LEFT':
                    curAxis = jSet.ROLL_AXIS
                    curAxisDir = -1 if jSet.INVERT_ROLL else 1
                elif data.commandID == 'CMD_ROLL_RIGHT':
                    curAxis = jSet.ROLL_AXIS
                    curAxisDir = 1 if jSet.INVERT_ROLL else -1
                elif data.commandID == 'CMD_PRIMARY_FIRE':
                    curAxis = 2
                    curAxisDir = 1
                elif data.commandID == 'CMD_INCREASE_FORCE':
                    curAxis = 4
                    curAxisDir = 1
                elif data.commandID == 'CMD_DECREASE_FORCE':
                    curAxis = 4
                    curAxisDir = -1
                else:
                    localizedKeys = InputMapping.g_instance.getLocalizedCommandKeysAndAxes(data.commandID)
                    if len(localizedKeys) > 0:
                        self.actionBtn = localizedKeys[len(localizedKeys) - 1]
                        for ind, val in keysMapping.items():
                            if keysMapping[ind] == self.actionBtn:
                                self.picture = ind
                                self.actionBtn = ''
                                break

                if curAxis >= 0:
                    self.picture = joyMapping[curAxis][curAxisDir]


class VOHintCompleted:

    def __init__(self, data):
        self.picture = data.actionIcon
        self.hintText = data.hintText


class VOHighlightedElems:

    def __init__(self, data):
        self.weaponPanel = False
        self.navWindow = False
        self.forsage = False
        self.healthMeter = False
        self.speedometer = False
        self.variometer = False
        self.progressbar = False
        self.targetWindow = False
        self.targetPoint = False
        self.arrowPointer = False
        self.markerPointer = False
        self.weaponRocket = False
        self.weaponBomb = False
        self.weaponGun = False
        self.weaponCannon = False
        if data is not None:
            if data.hudElement1 != '':
                setattr(self, data.hudElement1, True)
            if data.hudElement2 != '':
                setattr(self, data.hudElement2, True)
            if data.hudElement3 != '':
                setattr(self, data.hudElement3, True)
        return


class VOShadowElems:

    def __init__(self, data):
        self.progressbar = False
        self.healthMeter = False
        self.speedometer = False
        self.variometer = False
        self.forsage = False
        self.navWindow = False
        self.targetWindow = False
        self.targetWindowPower = False
        self.targetWindowSpeed = False
        self.targetWindowMobility = False
        self.weaponPanel = False
        self.weaponBomb = False
        self.weaponRocket = False
        self.weaponGun = False
        self.targetPoint = False
        self.markerPointer = False
        self.arrowPointer = False
        if data is not None:
            if data.shadowElement1 != '':
                setattr(self, data.shadowElement1, True)
            if data.shadowElement2 != '':
                setattr(self, data.shadowElement2, True)
            if data.shadowElement3 != '':
                setattr(self, data.shadowElement3, True)
        return


class Dummy:
    pass


def getShadowKillInfo(data, killedAvatarsFunc = None):
    self = Dummy()
    self.avatarKiller = ''
    self.allyAvatarID = -1
    self.enemyAvatarID = -1
    if killedAvatarsFunc is None or data is None:
        return self
    else:
        if data.shadowElement1 == 'enemyKilled' or data.shadowElement2 == 'enemyKilled' or data.shadowElement3 == 'enemyKilled':
            avatar = killedAvatarsFunc(False)
            if avatar is not None:
                self.allyAvatarID = avatar.lastDamagerID
                self.enemyAvatarID = avatar.id
                self.avatarKiller = 'left'
        if data.shadowElement1 == 'allyKilled' or data.shadowElement2 == 'allyKilled' or data.shadowElement3 == 'allyKilled':
            avatar = killedAvatarsFunc(True)
            if avatar is not None:
                self.allyAvatarID = avatar.id
                self.enemyAvatarID = avatar.lastDamagerID
                self.avatarKiller = 'right'
        return self


class VOHighlightedElemTP:

    def __init__(self):
        self.targetPoint = True


class ConditionEntity:

    def __init__(self, position):
        self.position = position


def getTargetImpl(targetPos, targetName):
    if targetName != '':
        ids = GameEnvironment.getClientArena().findIDsByPlayerName(targetName)
        if len(ids) > 0:
            entity = BigWorld.entities.get(ids[0], None)
            if entity is not None:
                return entity.position + targetPos
            else:
                return
        else:
            return
    return targetPos


def getTargetSpeedImpl(targetName):
    if targetName != '':
        ids = GameEnvironment.getClientArena().findIDsByPlayerName(targetName)
        if len(ids) > 0:
            entity = BigWorld.entities.get(ids[0], None)
            if entity is not None:
                return entity.getSpeed()
    return 0


def getTargetEntityImpl(targetName):
    if targetName != '':
        ids = GameEnvironment.getClientArena().findIDsByPlayerName(targetName)
        if len(ids) > 0:
            entity = BigWorld.entities.get(ids[0], None)
            return entity
    return


def parseTargetAsPosImpl(targetName):
    res = None
    valuesList = targetName.split(' ')
    if len(valuesList) != 3:
        return res
    else:
        return ConditionEntity(Math.Vector3(float(valuesList[0]), float(valuesList[1]), float(valuesList[2])))


class MarkerData:

    def __init__(self, targetPos, targetName, showMarker, showDistance, showFPBlink, conditionNext, conditionGen, conditionHide, lockTarget):
        self.targetPos = targetPos
        self.targetName = targetName
        self.showMarker = showMarker
        self.showDistance = showDistance
        self.showFPBlink = showFPBlink
        self.conditionNext = conditionNext
        self.conditionGen = conditionGen
        self.conditionHide = conditionHide
        self.lockTarget = lockTarget
        self._hidden = False

    def getTarget(self):
        return getTargetImpl(self.targetPos, self.targetName)

    def getShowFlags(self):
        return (self.showMarker, self.showDistance, self.showFPBlink)

    def valid(self):
        return self.targetPos is not None

    def updateHideStatus(self, conditions):
        self._hidden = False
        if self.conditionHide != '' and self.conditionHide in conditions and conditions[self.conditionHide].valid():
            self._hidden = True

    def switchToNext(self, conditions):
        if len(self.conditionNext) == 0:
            return False
        for cond in self.conditionNext:
            if cond not in conditions or not conditions[cond].valid():
                return False

        return True

    def getHideStatus(self):
        return self._hidden


class BaseAction:

    def __init__(self, data):
        self._name = data.name
        self._targetPos = None
        self._targetName = ''
        self._condition = data.condition
        self._manager = None
        self._activated = False
        return

    def addData(self, data):
        pass

    def setManager(self, manager):
        self._manager = manager

    def reset(self):
        self._activated = False

    def setTarget(self, dest, destName):
        self._targetPos = dest
        self._targetName = destName

    def getTarget(self):
        return getTargetImpl(self._targetPos, self._targetName)

    def update(self, conditionsSet):
        if not self.conditionsTrue(conditionsSet):
            self._activated = False
            return False
        return True

    def onDestroy(self):
        self._manager = None
        return

    def conditionsTrue(self, conditionsSet):
        for cond in self._condition:
            if cond not in conditionsSet or not conditionsSet[cond].valid():
                return False

        return True

    def getGenConditions(self):
        return []


class SetWPEvasionAction(BaseAction):

    def __init__(self, data):
        BaseAction.__init__(self, data)
        self._botName = data.botName
        self._value = data.enable

    def update(self, conditionsSet):
        if not BaseAction.update(self, conditionsSet):
            return False
        if self._activated:
            return False
        self._activated = True
        player = BigWorld.player()
        player.tutorialSetWPStrategyEvasion(self._botName, self._value)
        return True


class SetBSSimpleModeAction(BaseAction):

    def __init__(self, data):
        BaseAction.__init__(self, data)
        self._botName = data.botName
        self._value = data.enable
        self._distance = data.distance
        self._snapAltitude = data.snapAltitude

    def update(self, conditionsSet):
        if not BaseAction.update(self, conditionsSet):
            return False
        if self._activated:
            return False
        self._activated = True
        player = BigWorld.player()
        player.tutorialSetBotStrategySimpleMode(self._botName, self._value, self._distance, self._snapAltitude)
        return True


class SetWPSplineAction(BaseAction):

    class SplineData:

        def __init__(self, splineName, condition):
            self.splineName = splineName
            self.condition = condition

    def __init__(self, data):
        BaseAction.__init__(self, data)
        self._botName = data.botName
        self._splines = [SetWPSplineAction.SplineData(data.splineName, data.condition)]
        self._splineCurr = ''

    def addData(self, data):
        self._splines.append(SetWPSplineAction.SplineData(data.splineName, data.condition))

    def update(self, conditionsSet):
        validSpline = None
        for spline in self._splines:
            failed = False
            for cond in spline.condition:
                if cond not in conditionsSet or not conditionsSet[cond].valid():
                    failed = True
                    break

            if not failed:
                validSpline = spline
                break

        if validSpline is None or validSpline.splineName == self._splineCurr:
            return False
        elif self._activated:
            return False
        else:
            self._activated = True
            self._splineCurr = validSpline.splineName
            player = BigWorld.player()
            player.tutorialSetWPStrategySpline(self._botName, validSpline.splineName)
            return True

    def onDestroy(self):
        BaseAction.onDestroy(self)
        self._splines = []


class SetRestartPartAction(BaseAction):

    def __init__(self, data):
        BaseAction.__init__(self, data)

    def update(self, conditionsSet):
        if not BaseAction.update(self, conditionsSet):
            return False
        elif self._activated:
            return False
        else:
            self._activated = True
            if self._manager is not None:
                self._manager.resetSheduled()
            return True


class SetOvershadowAction(BaseAction):

    def __init__(self, data):
        BaseAction.__init__(self, data)
        self._show = data.show

    def update(self, conditionsSet):
        if not BaseAction.update(self, conditionsSet):
            return False
        elif self._activated:
            return False
        else:
            self._activated = True
            if self._manager is not None:
                self._manager.showOvershadow(self._show)
            return True


class SetShowBombingAction(BaseAction):

    def __init__(self, data):
        BaseAction.__init__(self, data)
        self._show = data.show
        self._showCur = not self._show

    def update(self, conditionsSet):
        if not BaseAction.update(self, conditionsSet):
            if self._showCur == self._show:
                self._showCur = not self._show
                GameEnvironment.getHUD().setBombingVisibility(self._showCur)
            return False
        if self._showCur != self._show:
            self._showCur = self._show
            GameEnvironment.getHUD().setBombingVisibility(self._showCur)
        return True


class SetReloadAction(BaseAction):
    CONST_COUNT = 10000
    COND_TIME = 1

    def __init__(self, data):
        BaseAction.__init__(self, data)
        self._onRCondition = data.onRocketsCondition
        self._onBCondition = data.onBombsCondition
        self._genConditions = []
        self._reloadRocketsTime = -1
        self._reloadBombsTime = -1

    def update(self, conditionsSet):
        if not BaseAction.update(self, conditionsSet):
            return False
        self._lastRocketsCount = BigWorld.player().controllers['shellController'].getShellCount(SHELL_INDEX.TYPE1)
        self._lastBombsCount = BigWorld.player().controllers['shellController'].getShellCount(SHELL_INDEX.TYPE2)
        if self._lastRocketsCount <= 0 and self._reloadRocketsTime < 0:
            self._reloadRocketsTime = BigWorld.time() + TUTORIAL_RELOAD_SHELLS_DELAY
        if self._lastBombsCount <= 0 and self._reloadBombsTime < 0:
            self._reloadBombsTime = BigWorld.time() + TUTORIAL_RELOAD_SHELLS_DELAY
        self._genConditions = []
        reloadRockets = False
        reloadBombs = False
        if self._reloadRocketsTime > 0 and BigWorld.time() > self._reloadRocketsTime:
            reloadRockets = True
            self._reloadRocketsTime = -1
            self._genConditions.append((self._onRCondition, self.COND_TIME))
            self._lastRocketsCount = self.CONST_COUNT
        if self._reloadBombsTime > 0 and BigWorld.time() > self._reloadBombsTime:
            reloadBombs = True
            self._reloadBombsTime = -1
            self._genConditions.append((self._onBCondition, self.COND_TIME))
            self._lastBombsCount = self.CONST_COUNT
        if reloadRockets or reloadBombs:
            BigWorld.player().tutorialReloadShells(reloadRockets, reloadBombs)
            return True
        return False

    def getGenConditions(self):
        return self._genConditions


class BaseHint(object):

    def __init__(self, data):
        self.__datas = [None,
         None,
         None,
         None]
        self.action = data.actionName
        self.addData(data)
        self._validInputIndex = -1
        self.completed = -1
        self.activateTime = BigWorld.time()
        self.showTimeout = -1
        self._blockTimeout = 0
        self._activateTimeout = 10000
        self._priority = 0
        self.actionParent = ''
        self.childrenPresent = False
        self.baseUpdatePassed = False
        self.hudElement1 = ''
        self.hudElement2 = ''
        self.hudElement3 = ''
        self.shadowElement1 = ''
        self.shadowElement2 = ''
        self.shadowElement3 = ''
        self.hudElementsColor = 'green'
        self.ui = None
        self.hideMarkerIcon = HIDE_MARKER.NONE
        self.hideMarkerArrow = HIDE_MARKER.NONE
        self._targetPos = None
        self._targetName = ''
        self.conditionGenerated = ''
        self.conditionGeneratedDelay = 0
        self.conditionGeneratedAfter = ''
        self.conditionGeneratedAfterDelay = 0
        self.pause = False
        self.groupID = 0
        if hasattr(data, 'priority'):
            self._priority = data.priority
        if hasattr(data, 'activateTimeout'):
            self._activateTimeout = data.activateTimeout
        if hasattr(data, 'blockTimeout'):
            self._blockTimeout = data.blockTimeout
        if hasattr(data, 'showTimeout'):
            self.showTimeout = data.showTimeout
        if hasattr(data, 'actionParent'):
            self.actionParent = data.actionParent
        if hasattr(data, 'hideMarkerIcon'):
            self.hideMarkerIcon = HIDE_MARKER.convertStrToID(data.hideMarkerIcon)
        if hasattr(data, 'hideMarkerArrow'):
            self.hideMarkerArrow = HIDE_MARKER.convertStrToID(data.hideMarkerArrow)
        if hasattr(data, 'hudElement1'):
            self.hudElement1 = data.hudElement1
        if hasattr(data, 'hudElement2'):
            self.hudElement2 = data.hudElement2
        if hasattr(data, 'hudElement3'):
            self.hudElement3 = data.hudElement3
        if hasattr(data, 'hudElementsColor'):
            self.hudElementsColor = data.hudElementsColor
        if hasattr(data, 'shadowElement1'):
            self.shadowElement1 = data.shadowElement1
        if hasattr(data, 'shadowElement2'):
            self.shadowElement2 = data.shadowElement2
        if hasattr(data, 'shadowElement3'):
            self.shadowElement3 = data.shadowElement3
        if hasattr(data, 'conditionGenerated'):
            self.conditionGenerated = data.conditionGenerated
        if hasattr(data, 'conditionGeneratedDelay'):
            self.conditionGeneratedDelay = data.conditionGeneratedDelay
        if hasattr(data, 'conditionGeneratedAfter'):
            self.conditionGeneratedAfter = data.conditionGeneratedAfter
        if hasattr(data, 'conditionGeneratedAfterDelay'):
            self.conditionGeneratedAfterDelay = data.conditionGeneratedAfterDelay
        if hasattr(data, 'pause'):
            self.pause = data.pause
        if hasattr(data, 'groupID'):
            self.groupID = data.groupID
        return

    def setTarget(self, dest, destName):
        self._targetPos = dest
        self._targetName = destName

    def getTarget(self):
        return getTargetImpl(self._targetPos, self._targetName)

    def blockTimeout(self):
        return self._blockTimeout

    def addData(self, data):
        type = 'mouse'
        if hasattr(data, 'type'):
            type = data.type
        inputId = TutorialHintsInputEnum[type]
        self.__datas[inputId] = copy.copy(data)
        self.__datas[inputId].type = type
        if hasattr(self.__datas[inputId], 'header'):
            self.__datas[inputId].header = localizeTutorial(self.__datas[inputId].header)
        if hasattr(self.__datas[inputId], 'hintText'):
            self.__datas[inputId].hintText = localizeTutorial(self.__datas[inputId].hintText)
        if not hasattr(self.__datas[inputId], 'actionIcon'):
            self.__datas[inputId].actionIcon = ''
        if not hasattr(self.__datas[inputId], 'commandID'):
            self.__datas[inputId].commandID = ''
        if not hasattr(self.__datas[inputId], 'voiceId'):
            self.__datas[inputId].voiceId = ''
        if not hasattr(self.__datas[inputId], 'sizeText'):
            self.__datas[inputId].sizeText = 'small'
        if not hasattr(self.__datas[inputId], 'condition'):
            self.__datas[inputId].condition = []
        self.actionRequired = ''
        if hasattr(data, 'actionRequired'):
            self.actionRequired = data.actionRequired

    def updateShow(self):
        if self.hudElement1 == 'targetPoint' or self.hudElement2 == 'targetPoint' or self.hudElement3 == 'targetPoint':
            screenPoint = GameEnvironment.getHUD().getForestallingPointScreenPos()
            if self.ui is not None and screenPoint is not None:
                self.ui.showTutorialHighlightTargetPoint(VOHighlightedElemTP(), screenPoint.x, screenPoint.y)
        return

    def updateFull(self, hintsStatus, conditionsSet):
        res = self.update(hintsStatus, conditionsSet)
        if self.actionParent != '' and self.completed >= 0 and self.baseUpdatePassed and res < 0:
            self.completed = -1
            self.notifyParent(hintsStatus)
        return res

    def update(self, hintsStatus, conditionsSet):
        self.baseUpdatePassed = False
        if self.completed + self.showTimeout > BigWorld.time():
            self.updateShow()
        if self.actionParent != '' and self.actionParent in hintsStatus and (hintsStatus[self.actionParent].activateTime < BigWorld.time() or hintsStatus[self.actionParent].completed >= 0 and hintsStatus[self.actionParent].completed + hintsStatus[self.actionParent].showTimeout > BigWorld.time()):
            return -1
        if self.actionRequired != '' and (self.actionRequired not in hintsStatus or hintsStatus[self.actionRequired].completed + hintsStatus[self.actionRequired].showTimeout > BigWorld.time() or hintsStatus[self.actionRequired].completed < 0):
            return -1
        if not self.conditionsTrue(conditionsSet):
            return -1
        curTime = BigWorld.time()
        if curTime < self.activateTime:
            return -1
        self.baseUpdatePassed = True
        return 1

    def isActive(self):
        return self._validInputIndex >= 0

    def updateActivity(self, inputIndex):
        self._validInputIndex = -1
        if self.__datas[inputIndex] is not None:
            self._validInputIndex = inputIndex
            return
        elif self.__datas[TutorialHintsInputEnum['mouse']] is not None:
            self._validInputIndex = TutorialHintsInputEnum['mouse']
            return
        else:
            return

    def priority(self):
        return self._priority

    def onDestroy(self):
        self.ui = None
        self.__datas = []
        return

    def onShow(self):
        self.completed = BigWorld.time()
        self.activateTime = BigWorld.time() + self._activateTimeout
        if self.childrenPresent:
            self.activateTime += ONE_DAY_DELAY

    def conditionsTrue(self, conditionsSet):
        conditions = []
        if self._validInputIndex >= 0:
            conditions = self.__datas[self._validInputIndex].condition
        for cond in conditions:
            if cond not in conditionsSet or not conditionsSet[cond].valid():
                return False

        return True

    def _getData(self):
        if self._validInputIndex >= 0:
            return self.__datas[self._validInputIndex]
        else:
            return None

    def getCommandID(self):
        data = self._getData()
        if data is None:
            return -1
        elif data.commandID == '':
            return -1
        else:
            return InputMapping.g_descriptions.getCommandIntID(data.commandID)

    def continuous(self):
        return False

    def onDynamicCollision(self):
        pass

    def notifyParent(self, hintsStatus):
        hintsStatus[self.actionParent].activateTime -= ONE_DAY_DELAY
        if hintsStatus[self.actionParent].actionParent != '':
            hintsStatus[hintsStatus[self.actionParent].actionParent].notifyParent(hintsStatus)

    def setMarkerData(self, markerVisible):
        pass

    def getShowParams(self, inputIndex, inputProfileType, pressAnyKeyHintTimeout = -1):
        data = self._getData()
        if data is None:
            LOG_ERROR('TutorialHints: hint {0} has no valid data for [{1}] input', data.action, INPUT_SYSTEM_PROFILES_LIST_REVERT[inputProfileType])
            return ('', None, '')
        else:
            params = VOHint(data, inputIndex, pressAnyKeyHintTimeout)
            params.curProfileName = INPUT_SYSTEM_PROFILES[inputProfileType]
            return ('hud.showHintControlTutorial', params, data.voiceId)

    def reset(self):
        self.completed = -1
        self.activateTime = BigWorld.time()

    def modifyActivateTime(self, delta):
        self.activateTime += delta


class InfoHint(BaseHint):

    def __init__(self, data):
        BaseHint.__init__(self, data)

    def update(self, hintsStatus, conditionsSet):
        if BaseHint.update(self, hintsStatus, conditionsSet) < 0:
            return -1
        return self.priority()


class CompleteHint(BaseHint):

    def __init__(self, data):
        BaseHint.__init__(self, data)

    def update(self, hintsStatus, conditionsSet):
        if BaseHint.update(self, hintsStatus, conditionsSet) < 0:
            return -1
        return self.priority()

    def getShowParams(self, inputIndex, inputProfileType, pressAnyKeyHintTimeout = -1):
        data = self._getData()
        if data is None:
            LOG_ERROR('TutorialHints: hint {0} has no valid data for [{1}] input', data.action, INPUT_SYSTEM_PROFILES_LIST_REVERT[inputProfileType])
            return ('', None, '')
        else:
            return ('hud.showHintResultTutorial', VOHintCompleted(data), data.voiceId)


class GoDirectionsHint(BaseHint):

    def __init__(self, data):
        BaseHint.__init__(self, data)
        self.activateTime = BigWorld.time() + 5
        self._angles = Math.Vector2(0, 0)
        self._angle = 0
        if hasattr(data, 'angle'):
            self._angle = math.radians(data.angle)

    def goCondition(self):
        return False

    def update(self, hintsStatus, conditionsSet):
        if BaseHint.update(self, hintsStatus, conditionsSet) < 0:
            return -1
        else:
            target = self.getTarget()
            if target is None:
                return -1
            invMatrix = Math.Matrix(BigWorld.camera().matrix)
            localPos = invMatrix.applyPoint(target)
            self._angles.set(localPos.pitch, localPos.yaw)
            if self.goCondition():
                return self.priority()
            return -1
            return

    def continuous(self):
        return True


class GoUpHint(GoDirectionsHint):

    def __init__(self, data):
        GoDirectionsHint.__init__(self, data)

    def goCondition(self):
        if self._angles.x < -self._angle:
            return True
        else:
            return False


class GoDownHint(GoDirectionsHint):

    def __init__(self, data):
        GoDirectionsHint.__init__(self, data)

    def goCondition(self):
        if self._angles.x > self._angle:
            return True
        else:
            return False


class GoLeftHint(GoDirectionsHint):

    def __init__(self, data):
        GoDirectionsHint.__init__(self, data)

    def goCondition(self):
        if self._angles.y < -self._angle:
            return True
        else:
            return False


class GoRightHint(GoDirectionsHint):

    def __init__(self, data):
        GoDirectionsHint.__init__(self, data)

    def goCondition(self):
        if self._angles.y > self._angle:
            return True
        else:
            return False


class ForsageHint(BaseHint):

    def __init__(self, data):
        BaseHint.__init__(self, data)
        self._temperatureK = 0
        if hasattr(data, 'temperatureK'):
            self._temperatureK = data.temperatureK

    def update(self, hintsStatus, conditionsSet):
        if BaseHint.update(self, hintsStatus, conditionsSet) < 0:
            return -1
        player = BigWorld.player()
        temperature = player.engineTemperature
        if temperature < self._temperatureK * WEP_DISABLE_TEMPERATURE or not player.isWarEmergencyPower:
            return -1
        return self.priority()


class EngineOverheatHint(BaseHint):

    def __init__(self, data):
        BaseHint.__init__(self, data)
        self._initTime = 0
        self._timeActive = 10

    def update(self, hintsStatus, conditionsSet):
        if BaseHint.update(self, hintsStatus, conditionsSet) < 0:
            self._initTime = -1
            return -1
        player = BigWorld.player()
        isEngineOverheated = GameEnvironment.getHUD().isEngineOverheated()
        if isEngineOverheated and player.isWarEmergencyPower:
            self._initTime = BigWorld.time()
        if BigWorld.time() - self._initTime > self._timeActive:
            return -1
        return self.priority()


class MenuHint(BaseHint):

    def __init__(self, data):
        BaseHint.__init__(self, data)

    def update(self, hintsStatus, conditionsSet):
        if BaseHint.update(self, hintsStatus, conditionsSet) < 0:
            return -1
        return self.priority()


class AltitudeHint(BaseHint):

    def __init__(self, data):
        BaseHint.__init__(self, data)
        self._altitude = 0
        self._entity = BigWorld.player()
        if hasattr(data, 'altitude'):
            self._altitude = math.radians(data.altitude)

    def setParams(self, entity, alt):
        pass

    def update(self, hintsStatus, conditionsSet):
        if BaseHint.update(self, hintsStatus, conditionsSet) < 0:
            return -1
        if not self._entity:
            return -1
        curAlt = self._entity.altitudeAboveObstacle
        if curAlt < self._altitude:
            return self.priority()
        return -1

    def onDestroy(self):
        self._entity = None
        BaseHint.onDestroy(self)
        return


class RangeAimHint(BaseHint):

    def __init__(self, data):
        BaseHint.__init__(self, data)
        self._angle = 0
        self._distance = 0
        self._invert = False
        self._approaching = True
        if hasattr(data, 'angle'):
            self._angle = math.radians(data.angle)
        if hasattr(data, 'distance'):
            self._distance = data.distance * WORLD_SCALING
        if hasattr(data, 'invert'):
            self._invert = data.invert

    def update(self, hintsStatus, conditionsSet):
        player = BigWorld.player()
        target = self.getTarget()
        if target is None:
            return -1
        dist = (player.position - target).length
        approaching = True
        if dist < self._distance:
            approaching = False
        if approaching == self._approaching:
            return -1
        self._approaching = approaching
        if BaseHint.update(self, hintsStatus, conditionsSet) < 0:
            return -1
        invMatrix = Math.Matrix(BigWorld.camera().matrix)
        localPos = invMatrix.applyPoint(target)
        cond = dist < self._distance and abs(localPos.yaw) < self._angle and abs(localPos.pitch) < self._angle
        if not self._invert and cond:
            return self.priority()
        elif self._invert and not cond:
            return self.priority()
        else:
            return -1


class RangeFireHint(BaseHint):

    def __init__(self, data):
        BaseHint.__init__(self, data)
        self._angle = 0
        self._distance = 0
        self._inAngle = False
        self._inDistance = False
        self._timeRocketFired = -1
        if hasattr(data, 'angle'):
            self._angle = math.radians(data.angle)
        if hasattr(data, 'distance'):
            self._distance = data.distance * WORLD_SCALING
        if hasattr(data, 'inAngle'):
            self._inAngle = data.inAngle
        if hasattr(data, 'inDistance'):
            self._inDistance = data.inDistance
        BigWorld.player().eLaunchShell += self.__onPlayerLaunchShell

    def __onPlayerLaunchShell(self, shellTypeID):
        if shellTypeID == SHELL_INDEX.TYPE1:
            self._timeRocketFired = BigWorld.time()

    def update(self, hintsStatus, conditionsSet):
        if BaseHint.update(self, hintsStatus, conditionsSet) < 0:
            return -1
        target = self.getTarget()
        if target is None:
            return -1
        player = BigWorld.player()
        isFiring = player.armamentStates != 0 or BigWorld.time() - self._timeRocketFired < 1
        if not isFiring:
            return -1
        dist = (player.position - target).length
        invMatrix = Math.Matrix(BigWorld.camera().matrix)
        localPos = invMatrix.applyPoint(target)
        cond = False
        if self._inDistance:
            cond = dist < self._distance
        else:
            cond = dist > self._distance
        if self._inAngle:
            cond = cond and abs(localPos.yaw) < self._angle and abs(localPos.pitch) < self._angle
        else:
            cond = cond and abs(localPos.yaw) > self._angle and abs(localPos.pitch) > self._angle
        if not cond:
            return -1
        else:
            return self.priority()

    def onDestroy(self):
        BigWorld.player().eLaunchShell -= self.__onPlayerLaunchShell
        BaseHint.onDestroy(self)


class GunsOverheatHint(BaseHint):

    def __init__(self, data):
        BaseHint.__init__(self, data)
        self._temperatureK = 1.0
        if hasattr(data, 'temperatureK'):
            self._temperatureK = data.temperatureK

    def update(self, hintsStatus, conditionsSet):
        if BaseHint.update(self, hintsStatus, conditionsSet) < 0:
            return -1
        else:
            player = BigWorld.player()
            weapons = player.controllers.get('weapons', None)
            if weapons:
                for group in weapons.getGunGroups():
                    if group.temperature > self._temperatureK * GUN_OVERHEATING_TEMPERATURE:
                        self._overheatedTime = BigWorld.time()
                        return self.priority()

            return -1


class TargetingHint(BaseHint):

    def __init__(self, data):
        BaseHint.__init__(self, data)
        self._distance = 0
        self._inDistance = True
        self._angleCos = 0
        self._inAngle = True
        self._marker = 'None'
        self._markerVisible = False
        if hasattr(data, 'distance'):
            self._distance = data.distance * WORLD_SCALING
        if hasattr(data, 'inDistance'):
            self._inDistance = data.inDistance
        if hasattr(data, 'angle'):
            self._angleCos = math.cos(math.radians(data.angle))
        if hasattr(data, 'inAngle'):
            self._inAngle = data.inAngle
        if hasattr(data, 'marker'):
            self._marker = data.marker

    def update(self, hintsStatus, conditionsSet):
        if BaseHint.update(self, hintsStatus, conditionsSet) < 0:
            return -1
        else:
            target = self.getTarget()
            if target is None:
                return -1
            if self._marker == 'ScreenIn' and not self._markerVisible:
                return -1
            if self._marker == 'ScreenOut' and self._markerVisible:
                return -1
            player = BigWorld.player()
            dist = (player.position - target).length
            if self._inDistance:
                if dist > self._distance:
                    return -1
            elif dist < self._distance:
                return -1
            matr = Math.Matrix()
            matr.setRotateYPR(Math.Vector3(player.yaw, player.pitch, 0))
            dirPlayer = matr.applyToAxis(2)
            dirOnTgt = target - player.position
            dirOnTgt.normalise()
            cosA = dirPlayer.dot(dirOnTgt)
            if self._inAngle:
                if cosA < self._angleCos:
                    return -1
            elif cosA > self._angleCos:
                return -1
            return self.priority()

    def setMarkerData(self, markerVisible):
        self._markerVisible = markerVisible


class DistDirNoForsageHint(BaseHint):

    def __init__(self, data):
        BaseHint.__init__(self, data)
        self._initTime = -1
        self._minDistance = 0
        self._noForsageTime = 0
        self._maxAngle = 0
        self._temperatureK = -1
        if hasattr(data, 'minDistance'):
            self._minDistance = data.minDistance * WORLD_SCALING
        if hasattr(data, 'noForsageTime'):
            self._noForsageTime = data.noForsageTime
        if hasattr(data, 'maxAngle'):
            self._maxAngle = math.radians(data.maxAngle)
        if hasattr(data, 'temperatureK'):
            self._temperatureK = data.temperatureK

    def update(self, hintsStatus, conditionsSet):
        if BaseHint.update(self, hintsStatus, conditionsSet) < 0:
            self._initTime = -1
            return -1
        target = self.getTarget()
        if target is None:
            return -1
        player = BigWorld.player()
        if player.isWarEmergencyPower:
            self._initTime = BigWorld.time()
        temperature = player.engineTemperature
        if temperature > self._temperatureK * WEP_DISABLE_TEMPERATURE:
            return -1
        dist = (player.position - target).length
        if dist < self._minDistance:
            return -1
        elif BigWorld.time() - self._initTime < self._noForsageTime:
            return -1
        invMatrix = Math.Matrix(BigWorld.camera().matrix)
        localPos = invMatrix.applyPoint(target)
        cond = abs(localPos.yaw) < self._maxAngle and abs(localPos.pitch) < self._maxAngle
        if not cond:
            return -1
        else:
            return self.priority()


class CollisionHint(BaseHint):

    def __init__(self, data):
        super(CollisionHint, self).__init__(data)
        self._collisionTime = -1
        self._activeDelay = 10

    def update(self, hintsStatus, conditionsSet):
        if BaseHint.update(self, hintsStatus, conditionsSet) < 0:
            return -1
        if BigWorld.time() - self._collisionTime > self._activeDelay:
            return -1
        return self.priority()

    def onDynamicCollision(self):
        self._collisionTime = BigWorld.time()

    def reset(self):
        super(CollisionHint, self).reset()
        self._collisionTime = -1


class DescentHint(BaseHint):

    def __init__(self, data):
        BaseHint.__init__(self, data)
        self.altitude = data.altitude
        self.descentTime = data.descentTime
        self.descentBeginTime = -1

    def update(self, hintsStatus, conditionsSet):
        player = BigWorld.player()
        if player.pitch > 0:
            if self.descentBeginTime < 0:
                self.descentBeginTime = BigWorld.time()
        else:
            self.descentBeginTime = -1
        if BaseHint.update(self, hintsStatus, conditionsSet) < 0:
            return -1
        curAlt = player.altitudeAboveObstacle
        if curAlt > self.altitude:
            return -1
        if self.descentBeginTime < 0 or BigWorld.time() - self.descentBeginTime < self.descentTime:
            return -1
        return self.priority()


class NoseUpHint(BaseHint):

    def __init__(self, data):
        BaseHint.__init__(self, data)
        self.pitch = math.radians(data.angle)
        self.pitchTime = data.time
        self.pitchBeginTime = -1
        self.invert = data.invert

    def update(self, hintsStatus, conditionsSet):
        player = BigWorld.player()
        if player.pitch < -self.pitch and not self.invert or player.pitch > self.pitch and self.invert:
            if self.pitchBeginTime < 0:
                self.pitchBeginTime = BigWorld.time()
        else:
            self.pitchBeginTime = -1
        if BaseHint.update(self, hintsStatus, conditionsSet) < 0:
            return -1
        if self.pitchBeginTime < 0 or BigWorld.time() - self.pitchBeginTime < self.pitchTime:
            return -1
        return self.priority()


class UnderAttackHint(BaseHint):

    def __init__(self):
        BaseHint.__init__(self, data)
        self.angleCosFwd = math.cos(math.radians(data.angleBotFwd))
        self.angleCosBwd = math.cos(math.radians(data.anglePlayerBack))
        self.distance = data.distance
        self.botNames = data.botNames

    def update(self, hintsStatus, conditionsSet):
        if BaseHint.update(self, hintsStatus, conditionsSet) < 0:
            return -1
        player = BigWorld.player()
        found = False
        matr = Math.Matrix()
        for name in self.botNames:
            ids = GameEnvironment.getClientArena().findIDsByPlayerName(name)
            if len(ids) > 0:
                entity = BigWorld.entities.get(ids[0], None)
                if entity is not None:
                    matr.setRotateYPR(Math.Vector3(ent.yaw, ent.pitch, 0))
                    dirBot = matr.applyToAxis(2)
                    dirBotToAvatar = player.position - ent.position
                    len = dirBotToAvatar.length
                    if len > self.distance:
                        continue
                    dirBotToAvatar.normalise()
                    angleCosBotToAvatar = dirAvatarToBot.dot(dirBot)
                    if angleCosBotToAvatar < self.angleCosFwd:
                        continue
                    matr.setRotateYPR(Math.Vector3(player.yaw, player.pitch, 0))
                    dirAvatar = matr.applyToAxis(2)
                    angleCosAvatarToBot = dirBotToAvatar.dot(dirAvatar)
                    if angleCosAvatarToBot < self.angleCosBwd:
                        continue
                    found = True
                    break

        if not found:
            return -1
        else:
            return self.priority()


class Condition:
    targetPos = None
    targetName = ''
    paused = False
    pausedTime = -1
    pausedUnTime = -1

    @staticmethod
    def setTarget(pos, name):
        Condition.targetPos = pos
        Condition.targetName = name

    @staticmethod
    def setPause(value):
        Condition.paused = value
        if value:
            Condition.pausedTime = BigWorld.time()
        else:
            Condition.pausedUnTime = BigWorld.time()

    def modifyActivateTime(self):
        timeDelta = BigWorld.time() - Condition.pausedTime
        self.time += timeDelta

    def getTarget(self):
        return getTargetImpl(self.targetPos, self.targetName)

    def getTargetEntity(self):
        return getTargetEntityImpl(self.targetName)

    def getTargetSpeed(self):
        return getTargetSpeedImpl(self.targetName)

    def parseTargetAsPos(self, targetName):
        return parseTargetAsPosImpl(targetName)

    def getEntity(self, name):
        if name == 'player':
            return BigWorld.player()
        elif name == 'target':
            return self.getTargetEntity()
        elif name == 'forestallingPoint':
            return ConditionEntity(GameEnvironment.getHUD().getForestallingPointWorldPos())
        ids = GameEnvironment.getClientArena().findIDsByPlayerName(name)
        if len(ids) > 0:
            return BigWorld.entities.get(ids[0], None)
        else:
            return self.parseTargetAsPos(name)

    def getEntityHeight(self, nameSrc, nameTgt):
        if nameTgt == 'ground':
            entity = self.getEntity(nameSrc)
            if entity:
                return entity.altitudeAboveObstacle
            else:
                return
        elif nameTgt == 'water':
            entity = self.getEntity(nameSrc)
            if entity:
                return entity.getAltitudeAboveWaterLevel() * WORLD_SCALING
            else:
                return
        entitySrc = self.getEntity(nameSrc)
        entityTgt = self.getEntity(nameTgt)
        if entitySrc is None or entityTgt is None:
            return
        else:
            return entitySrc.position.y - entityTgt.position.y

    def getEntitySpeed(self, name):
        if name == 'player':
            return BigWorld.player().getSpeed()
        elif name == 'target':
            return self.getTargetSpeed()
        elif name == 'ground':
            return 0
        else:
            return None

    def __init__(self, name, duration = -1, delay = 0):
        self.name = name
        self.time = BigWorld.time() + delay
        self.duration = duration if duration > 0 else ONE_DAY_DELAY
        self._valid = False

    def update(self):
        """
        if (Condition.paused):
            self._valid = False;
            return;
        """
        time = BigWorld.time()
        self._valid = time > self.time and time < self.time + self.duration

    def valid(self):
        return self._valid

    def onDestroy(self):
        pass

    def prolong(self, time):
        self.time = BigWorld.time()
        if self.duration < time:
            self.duration = time

    def onEntityChangeHealth(self, entity, lastHealth):
        pass


class ConditionFlaps(Condition):

    def __init__(self, name, invert, duration = -1, delay = 0):
        Condition.__init__(self, name, duration, delay)
        self._invert = invert

    def update(self):
        Condition.update(self)
        if not self._valid:
            return
        flapsFired = GameEnvironment.getInput().isFired(InputMapping.CMD_FLAPS_UP)
        if self._invert:
            self._valid = not flapsFired
        else:
            self._valid = flapsFired


class ConditionSpeedDelta(Condition):

    def __init__(self, name, nameSrc, nameTarget, speedDelta, invert, duration = -1, delay = 0):
        Condition.__init__(self, name, duration, delay)
        self._nameSrc = nameSrc
        self._nameTarget = nameTarget
        self._speedDelta = speedDelta / 3.6
        self._invert = invert

    def update(self):
        Condition.update(self)
        if not self._valid:
            return
        else:
            self._valid = False
            entitySrcSpeed = self.getEntitySpeed(self._nameSrc)
            if entitySrcSpeed is None:
                return
            entityTgtSpeed = self.getEntitySpeed(self._nameTarget)
            if entityTgtSpeed is None:
                return
            speedDelta = entitySrcSpeed - entityTgtSpeed
            if self._invert:
                self._valid = speedDelta > self._speedDelta
            else:
                self._valid = speedDelta < self._speedDelta
            return


class ConditionHeightDelta(Condition):

    def __init__(self, name, nameSrc, nameTarget, deltaMin, deltaMax, invert, duration = -1, delay = 0):
        Condition.__init__(self, name, duration, delay)
        self._deltaMin = deltaMin * WORLD_SCALING
        self._deltaMax = deltaMax * WORLD_SCALING
        self._nameSrc = nameSrc
        self._nameTarget = nameTarget
        self._invert = invert

    def update(self):
        Condition.update(self)
        if not self._valid:
            return
        else:
            self._valid = False
            hDelta = self.getEntityHeight(self._nameSrc, self._nameTarget)
            if hDelta is None:
                self._valid = False
                return
            cond = hDelta > self._deltaMin and hDelta < self._deltaMax
            if self._invert:
                self._valid = not cond
            else:
                self._valid = cond
            return


class ConditionArea(Condition):

    def __init__(self, name, duration, delay, center, radius, inside):
        Condition.__init__(self, name, duration, delay)
        self.center = center
        self.radius = radius * WORLD_SCALING
        self.inside = inside

    def update(self):
        Condition.update(self)
        if not self._valid:
            return
        player = BigWorld.player()
        dist = player.position.distTo(self.center)
        self._valid = False
        if self.inside and dist < self.radius:
            self._valid = True
        if not self.inside and dist > self.radius:
            self._valid = True


class ConditionAreaTarget(Condition):

    def __init__(self, name, duration, delay, radius, inside):
        Condition.__init__(self, name, duration, delay)
        self.radius = radius * WORLD_SCALING
        self.inside = inside

    def update(self):
        Condition.update(self)
        if not self._valid:
            return
        else:
            self._valid = False
            player = BigWorld.player()
            target = self.getTarget()
            if target is None:
                return
            dist = player.position.distTo(target)
            if self.inside and dist < self.radius:
                self._valid = True
            if not self.inside and dist > self.radius:
                self._valid = True
            return


class ConditionTurnTowards(Condition):

    def __init__(self, name, nameSrc, nameTarget, turnDuration, duration = -1, delay = 0):
        Condition.__init__(self, name, duration, delay)
        self._nameSrc = nameSrc
        self._nameTarget = nameTarget
        self._turnDuration = turnDuration
        self._prevDirSrc = Math.Vector(0, 0, 1)
        self._prevUpSrc = Math.Vector(0, 0, 1)
        self._prevDirTgt = Math.Vector(0, 0, 1)
        self._timeBegin = -1

    def update(self):
        Condition.update(self)
        if not self._valid:
            return
        else:
            self._valid = False
            entitySrc = self.getEntity(self._nameSrc)
            if entitySrc is None:
                return
            entityTgt = self.getEntity(self._nameTarget)
            if entityTgt is None:
                return
            matr = Math.Matrix()
            matr.setRotateYPR(Math.Vector3(entitySrc.yaw, entitySrc.pitch, entitySrc.roll))
            dirSrc = matr.applyToAxis(2)
            dirSrcToTgt = entityTgt.position - entitySrc.position
            dirSrcToTgt.normalise()
            len = dirBotToAvatar.length
            upSrc = self._prevSrcDir * dirSrc
            upSrc.normalise()
            if upSrc.dot(self._prevUp) > 0.5 and (dirSrc * dirSrcToTgt).dot(upSrc) > 0.5:
                if self._timeBegin < 0:
                    self._timeBegin = BigWorld.time()
            else:
                self._timeBegin = -1
            self._prevSrcDir = dirSrc
            self._prevTgtDir = dirTgt
            self._prevUp = upScr
            if BigWorld.time() - self._timeBegin > self._turnDuration:
                self._valid = True
            return


class ConditionAngle(Condition):

    def __init__(self, name, nameSrc, nameTarget, angleMin, angleMax, inAngles, duration = -1, delay = 0):
        Condition.__init__(self, name, duration, delay)
        self._nameSrc = nameSrc
        self._nameTarget = nameTarget
        self._angleMinCos = math.cos(math.radians(max(min(angleMin, 90), 0)))
        self._angleMaxCos = math.cos(math.radians(max(min(angleMax, 90), 0)))
        self._invert = not inAngles

    def update(self):
        Condition.update(self)
        if not self._valid:
            return
        else:
            self._valid = False
            entitySrc = self.getEntity(self._nameSrc)
            if entitySrc is None:
                return
            entityTgt = self.getEntity(self._nameTarget)
            if entityTgt is None:
                return
            matr = Math.Matrix()
            matr.setRotateYPR(Math.Vector3(entitySrc.yaw, entitySrc.pitch, entitySrc.roll))
            dirSrc = matr.applyToAxis(2)
            dirSrcToTgt = entityTgt.position - entitySrc.position
            dirSrcToTgt.normalise()
            angleCos = dirSrc.dot(dirSrcToTgt)
            cond = angleCos < self._angleMinCos and angleCos > self._angleMaxCos
            if not self._invert and cond:
                self._valid = True
            elif self._invert and not cond:
                self._valid = True
            return


class ConditionFiring(Condition):

    def __init__(self, name, nameSrc, invert, duration = -1, delay = 0):
        Condition.__init__(self, name, duration, delay)
        self._nameSrc = nameSrc
        self._invert = invert

    def update(self):
        Condition.update(self)
        if not self._valid:
            return
        else:
            self._valid = False
            entitySrc = self.getEntity(self._nameSrc)
            if entitySrc is None:
                return -1
            isFiring = entitySrc.armamentStates != 0
            if not self._invert and isFiring:
                self._valid = True
            elif self._invert and not isFiring:
                self._valid = True
            return


class ConditionDamgedParts(Condition):

    def __init__(self, name, nameParts, invert, duration = -1, delay = 0):
        Condition.__init__(self, name, duration, delay)
        self._nameParts = nameParts
        self._invert = invert

    def update(self):
        Condition.update(self)
        if not self._valid:
            return
        self._valid = False
        player = BigWorld.player()
        for partID, partServerState in player.partStates:
            partSettings = player.settings.airplane.getPartByID(partID)
            if partSettings:
                partTypeData = partSettings.getFirstPartType()
                partTypeStr = partTypeData.componentType
                if partTypeStr in self._nameParts and partServerState > 0:
                    self._valid = True
                    return


class ConditionConus(Condition):

    def __init__(self, name, nameSrc, nameTarget, heightDeltaUp, heightDelta, widthDelta, invert, duration = -1, delay = 0):
        Condition.__init__(self, name, duration, delay)
        self._nameSrc = nameSrc
        self._nameTarget = nameTarget
        self._invert = invert
        self._heightDelta = heightDelta
        self._widthDelta = widthDelta
        self._heightDeltaUp = heightDeltaUp

    def update(self):
        Condition.update(self)
        if not self._valid:
            return
        else:
            self._valid = False
            entitySrc = self.getEntity(self._nameSrc)
            if entitySrc is None:
                return
            entityTgt = self.getEntity(self._nameTarget)
            if entityTgt is None:
                return
            targetCur = entityTgt.position
            pos = entitySrc.position
            deltaY = abs(pos.y - targetCur.y)
            deltaXZ = math.sqrt((pos.x - targetCur.x) * (pos.x - targetCur.x) + (pos.z - targetCur.z) * (pos.z - targetCur.z))
            directCond = deltaY > self._heightDelta and deltaXZ < deltaY * self._widthDelta / self._heightDelta
            if self._heightDeltaUp > 0.0:
                directCond = directCond and deltaY <= self._heightDeltaUp
            if self._invert and not directCond:
                self._valid = True
            elif not self._invert and directCond:
                self._valid = True
            return


class ConditionBombing(Condition):

    def __init__(self, name, position, radius, invert, duration = -1, delay = 0):
        Condition.__init__(self, name, duration, delay)
        self._position = position
        self._radius = radius
        self._invert = invert

    def update(self):
        Condition.update(self)
        if not self._valid:
            return
        else:
            self._valid = False
            matrix = GameEnvironment.getHUD().getBombingPointWorldPos()
            if matrix is None:
                return
            dist = (matrix.translation - self._position).length
            flag = dist < self._radius
            if not self._invert and flag:
                self._valid = True
            elif self._invert and not flag:
                self._valid = True
            return


class ConditionBombingAngle(Condition):

    def __init__(self, name, invert, duration = -1, delay = 0):
        Condition.__init__(self, name, duration, delay)
        self._invert = invert

    def update(self):
        Condition.update(self)
        if not self._valid:
            return
        self._valid = GameEnvironment.getHUD().getBombTargetVisible()
        if self._invert:
            self._valid = not self._valid


class ConditionCommand(Condition):

    def __init__(self, name, commandID, blocked, duration = -1, delay = 0):
        Condition.__init__(self, name, duration, delay)
        self._commandID = InputMapping.g_descriptions.getCommandIntID(commandID)
        self._blocked = blocked
        self._validCond = False
        input = GameEnvironment.getInput()
        if self._blocked:
            input.commandProcessor.filteredCommandEvent += self.commandFilteredCB
        else:
            input.commandProcessor.addListeners(self._commandID, self.commandListenerBeginCB, self.commandListenerEndCB)

    def commandFilteredCB(self, commandID, isFired):
        if Condition.paused and isFired:
            return
        input = GameEnvironment.getInput()
        if commandID == self._commandID:
            if isFired:
                self._validCond = True
            else:
                self._validCond = False

    def commandListenerBeginCB(self, event = None):
        if Condition.paused:
            return
        self._validCond = True

    def commandListenerEndCB(self, event = None):
        self._validCond = False

    def update(self):
        Condition.update(self)
        if not self._valid:
            return
        self._valid = self._validCond

    def onDestroy(self):
        commandProcessor = GameEnvironment.getInput().commandProcessor
        if commandProcessor is not None:
            if self._blocked:
                commandProcessor.filteredCommandEvent -= self.commandFilteredCB
            else:
                commandProcessor.removeListeners(self._commandID, self.commandListenerBeginCB, self.commandListenerEndCB)
        Condition.onDestroy(self)
        return


class ConditionDestruction(Condition):

    def __init__(self, name, entityName, damage, duration = -1, delay = 0):
        Condition.__init__(self, name, duration, delay)
        player = BigWorld.player()
        self.__timeDestruction = -1
        self.__entityName = entityName
        self.__damage = damage
        if player is None:
            LOG_DEBUG('ConditionDestruction : Player is missing')
            return
        else:
            player.eReportDestruction += self.onDestruction
            return

    def onDestroy(self):
        player = BigWorld.player()
        if player is None and IS_DEVELOPMENT:
            GENARATE_TRACEBACK
        player.eReportDestruction -= self.onDestruction
        Condition.onDestroy(self)
        return

    def update(self):
        Condition.update(self)
        if not self._valid:
            return
        self._valid = False
        if self.__timeDestruction < 0:
            return
        self._valid = BigWorld.time() - self.__timeDestruction < 10

    def onDestruction(self, killingInfo):
        clientArena = GameEnvironment.getClientArena()
        killerData = clientArena.getAvatarInfo(killingInfo['killerID'])
        victimData = clientArena.getAvatarInfo(killingInfo['victimID'])
        player = BigWorld.player()
        victimEntity = BigWorld.entities.get(killingInfo['victimID'], None)
        if victimEntity is None:
            LOG_DEBUG('ConditionDestruction : victimEntity not found ', killingInfo['victimID'])
            return
        elif self.__damage == 'ram' and victimEntity.lastDamageReason != DAMAGE_REASON.RAMMING:
            return
        elif self.__damage == 'bullet' and victimEntity.lastDamageReason != DAMAGE_REASON.BULLET:
            return
        else:
            if self.__entityName == 'team0':
                if victimData['teamIndex'] != 0 or killingInfo['victimID'] == BigWorld.player().id or killingInfo['killerID'] == player.id and victimData['teamIndex'] == player.teamIndex:
                    return
            elif self.__entityName == 'team1':
                if victimData['teamIndex'] != 1 or killingInfo['victimID'] == BigWorld.player().id or killingInfo['killerID'] == player.id and victimData['teamIndex'] == player.teamIndex:
                    return
            elif self.__entityName == 'player':
                if player.id != victimData['teamIndex']:
                    return
            elif self.__entityName != victimData['playerName']:
                return
            self.__timeDestruction = BigWorld.time()
            return


class ConditionHit(Condition):

    def __init__(self, name, source, target, duration = -1, delay = 0):
        Condition.__init__(self, name, duration, delay)
        self.__timeHit = -1
        self.__source = source
        self.__target = target

    def update(self):
        Condition.update(self)
        if not self._valid:
            return
        self._valid = False
        if self.__timeHit < 0:
            return
        self._valid = BigWorld.time() - self.__timeHit < 10

    def onEntityChangeHealth(self, entity, lastHealth):
        clientArena = GameEnvironment.getClientArena()
        hitter = BigWorld.entities.get(entity.lastDamagerID, None)
        if hitter is None:
            return
        else:
            if self.__target == 'team0':
                if entity.teamIndex != 0:
                    return
            elif self.__target == 'team1':
                if entity.teamIndex != 1:
                    return
            elif self.__target != '':
                if self.__target == 'player':
                    player = BigWorld.player()
                    if player.id != entity.id:
                        return
                elif entity.objectName != self.__target:
                    return
            if self.__source == 'team0':
                if hitter.teamIndex != 0:
                    return
            elif self.__source == 'team1':
                if hitter.teamIndex != 1:
                    return
            elif self.__source != '':
                if self.__source == 'player':
                    player = BigWorld.player()
                    if player.id != entity.lastDamagerID:
                        return
                elif hitter.objectName != self.__source:
                    return
            self.__timeHit = BigWorld.time()
            return


class ConditionBRPresent(Condition):

    def __init__(self, name, invert, duration = -1, delay = 0):
        Condition.__init__(self, name, duration, delay)
        self.__invert = invert

    def update(self):
        Condition.update(self)
        if not self._valid:
            return
        self._valid = False
        pr = updatable.UpdatableManager.g_instance.updatablesPresent()
        if self.__invert:
            self._valid = not pr
        else:
            self._valid = pr


class PauseData:

    def __init__(self):
        self.paused = False
        self.scheduled = None
        self.commandID = None
        self.filterAllowBackup = None
        self.inputAllowed = None
        self.inputFilterData = None
        self.inputFilterCB = None
        self.eventAdded = False
        return

    def schedulePause(self, value, commandID):
        self.scheduled = value
        if self.scheduled and commandID is not None:
            self.commandID = commandID
        return

    def setInputFilterData(self, data, funcCB):
        self.inputFilterData = data
        self.inputFilterCB = funcCB

    def onDestroy(self):
        self.commandID = None
        self.inputFilterData = None
        self.inputFilterCB = None
        return


class HintsManager:

    def __init__(self, tutorialManager):
        self.__tutorialManager = tutorialManager
        self.__hints = {}
        self.__inputProfileType = -1
        self.__inputIndex = -1
        self.__loaded = False
        self.__conditions = {}
        self.__timeHideHint = -1
        self.__priority = -1
        self.__enabled = True
        self.__target = None
        self.__actionName = ''
        self.__timeBlocked = -1
        self.__partIndex = -1
        self.__markerVisible = False
        self.__arrowVisible = False
        self.__arrowVisibleTime = 0
        self.__hideMarkerIcon = HIDE_MARKER.NONE
        self.__hideMarkerArrow = HIDE_MARKER.NONE
        self.__lastCollisionTime = -1
        self.__markers = {}
        self.__markerActive = -1
        self.__markerCBClearTarget = None
        self.__markerCBSetTarget = None
        self.__markerPosPrev = None
        self.__actions = {}
        self.__resetSheduled = False
        self.__timeShown = 0
        self.__pauseData = PauseData()
        GameEnvironment.g_instance.eHideBackendGraphics += self.hideBackendGraphics
        GameEnvironment.g_instance.eShowBackendGraphics += self.showBackendGraphics
        self.__isEscapeMenu = False
        self.__continuousNeedHide = False
        self.__groupID = -1
        return

    def hideBackendGraphics(self):
        self.__isEscapeMenu = True

    def showBackendGraphics(self):
        self.__isEscapeMenu = False

    def setLockTargetCallbacks(self, clearCall, setCall):
        self.__markerCBClearTarget = clearCall
        self.__markerCBSetTarget = setCall

    def setHint(self, hint, ui):
        lessonData = self.__tutorialManager._tutorialData.lesson[self.__tutorialManager._currentLessonIndex]
        if hint.showTimeout < 0:
            hint.showTimeout = lessonData.hintsDelay
        hint.ui = ui

    def loadData(self, partIndex, type, data):
        if type.find('Hint') >= 0:
            return self.loadHint(partIndex, type, data)
        if type.find('Action') >= 0:
            return self.loadAction(partIndex, type, data)

    def loadAction(self, partIndex, type, data):
        if partIndex not in self.__actions:
            self.__actions[partIndex] = {}
        if data.name in self.__actions[partIndex]:
            self.__actions[partIndex][data.name].addData(data)
        else:
            self.__actions[partIndex][data.name] = self.createElement(data, type)
            self.__actions[partIndex][data.name].setManager(self)
        return ''

    def loadHint(self, partIndex, type, data):
        if partIndex not in self.__hints:
            self.__hints[partIndex] = {}
        if data.actionName in self.__hints[partIndex]:
            self.__hints[partIndex][data.actionName].addData(data)
        else:
            self.__hints[partIndex][data.actionName] = self.createElement(data, type)
            self.setHint(self.__hints[partIndex][data.actionName], self.__tutorialManager.tutorialUI.ui)
        return self.__hints[partIndex][data.actionName].actionParent

    def createElement(self, data, type):
        return globals()[type](data)

    def markerAdd(self, index, target, targetName, showDistance, showMarker, showFPBlink, conditionNext, conditionGen, conditionHide, lockTarget):
        self.__markers[index] = MarkerData(target, targetName, showMarker, showDistance, showFPBlink, conditionNext, conditionGen, conditionHide, lockTarget)

    def markerSetActive(self, index):
        if index >= len(self.__markers) and len(self.__markers) > 0:
            index = 0
        if self.__markerActive >= 0:
            self.removeCondition(self.__markers[self.__markerActive].conditionGen)
        self.__markerActive = index
        self.setCondition(self.__markers[self.__markerActive].conditionGen)
        self.setTarget(self.__markers[self.__markerActive].targetPos, self.__markers[self.__markerActive].targetName)
        if self.__markers[self.__markerActive].lockTarget == 'clear' and self.__markerCBClearTarget is not None:
            self.__markerCBClearTarget()
        if self.__markers[self.__markerActive].lockTarget == 'lock' and self.__markerCBSetTarget is not None:
            self.__markerCBSetTarget()
        return

    def markersUpdate(self):
        if self.__markerActive < 0:
            return
        if self.__markers[self.__markerActive].switchToNext(self.__conditions):
            self.markerSetActive(self.__markerActive + 1)
        self.__markers[self.__markerActive].updateHideStatus(self.__conditions)

    def markerClearAll(self):
        for markerInd in self.__markers:
            self.removeCondition(self.__markers[markerInd].conditionGen)

        self.__markers = {}
        self.__markerActive = -1
        self.__markerPosPrev = None
        return

    def markerActiveGetShowData(self):
        if self.__markerActive < 0:
            return (None, (False, False, False), False)
        else:
            pos = self.__markers[self.__markerActive].getTarget()
            if pos is None:
                if self.__markerPosPrev is not None:
                    return (self.__markerPosPrev, (True, True, False), False)
                else:
                    return (None, (False, False, False), False)
            self.__markerPosPrev = Math.Vector3(pos)
            showFlags = self.__markers[self.__markerActive].getShowFlags()
            hideMarker = self.__markers[self.__markerActive].getHideStatus()
            return (pos, showFlags, hideMarker)

    def onInputProfileChanged(self, inputProfileType):
        if inputProfileType == INPUT_SYSTEM_STATE.KEYBOARD:
            self.__inputIndex = TutorialHintsInputEnum['keyboard']
        elif inputProfileType == INPUT_SYSTEM_STATE.GAMEPAD_DIRECT_CONTROL:
            self.__inputIndex = TutorialHintsInputEnum['gamepad']
        elif inputProfileType == INPUT_SYSTEM_STATE.JOYSTICK:
            self.__inputIndex = TutorialHintsInputEnum['joystick']
        elif inputProfileType == INPUT_SYSTEM_STATE.MOUSE:
            self.__inputIndex = TutorialHintsInputEnum['mouse']
        self.__inputProfileType = inputProfileType
        for partIndex in self.__hints:
            for key in self.__hints[partIndex]:
                self.__hints[partIndex][key].updateActivity(self.__inputIndex)

    def onPartChanged(self, partIndex):
        self.__timeBlocked = -1
        if self.__actionName != '':
            hint = None
            try:
                hint = self.__hints[self.__partIndex][self.__actionName]
            except:
                LOG_ERROR('HintsManager::onPartChanged: Unable to get hint: partIndex: {0}, actionName: {1}'.format(self.__partIndex, self.__actionName))

            if hint is not None:
                if hint.continuous():
                    self.hideTutorialHintControl()
                else:
                    self.removeCondition(self.__hints[self.__partIndex][self.__actionName].conditionGenerated)
        self.__partIndex = partIndex
        return

    def conditionsUpdate(self, partIndex):
        condToRem = []
        for key in self.__conditions:
            cond = self.__conditions[key]
            if BigWorld.time() - cond.time > cond.duration:
                condToRem.append(key)

        for key in condToRem:
            self.__conditions[key].onDestroy()
            del self.__conditions[key]

        for key in self.__conditions:
            self.__conditions[key].update()

    def isPlayerDead(self):
        player = BigWorld.player()
        if player is None or not EntityStates.inState(player, EntityStates.GAME):
            return True
        else:
            return False
            return

    def hintsUpdate(self, partIndex):
        if partIndex not in self.__hints:
            return
        else:
            priority = -1
            obj = None
            for key in self.__hints[partIndex]:
                object = self.__hints[partIndex][key]
                if object.isActive():
                    res = object.updateFull(self.__hints[partIndex], self.__conditions)
                    if res > priority and (self.__groupID < 0 or object.groupID == self.__groupID):
                        priority = res
                        obj = object

            if self.__pauseData.paused:
                return
            if BigWorld.time() > self.__timeHideHint and self.__timeHideHint > 0:
                self.hideTutorialHintControl()
            continuousNeedHide = self.__actionName != '' and self.__actionName in self.__hints[partIndex] and self.__hints[partIndex][self.__actionName].continuous() and (obj is None or self.__actionName != obj.action)
            if BigWorld.time() - self.__timeShown < TUTORIAL_HINT_FORCE_SHOW_TIME:
                if continuousNeedHide:
                    self.__continuousNeedHide = True
                return
            if self.__continuousNeedHide or continuousNeedHide:
                if self.__continuousNeedHide and (self.__actionName == '' or not self.__hints[partIndex][self.__actionName].continuous()):
                    LOG_ERROR('Continuous action error {0}', self.__actionName)
                    if IS_DEVELOPMENT:
                        GENERATE_TRACEBACK
                self.hideTutorialHintControl()
            if BigWorld.time() < self.__timeBlocked and priority < 1000:
                return
            if self.isPlayerDead():
                return
            if obj is not None and priority >= self.__priority and self.__actionName != obj.action:
                self.hideTutorialHintControl()
                funcString, params, voiceId = obj.getShowParams(self.__inputIndex, self.__inputProfileType, obj.showTimeout if obj.pause else -1)
                self.__tutorialManager.showTutorialHintControl(funcString, params, True)
                paramsHighlighted = VOHighlightedElems(obj)
                self.__tutorialManager.tutorialUI.ui.showTutorialHighlightControls(paramsHighlighted, obj.hudElementsColor)
                shadowParams = VOShadowElems(obj)
                self.__tutorialManager.tutorialUI.ui.showTutorialShadowHintControls(shadowParams)
                shadowKillParams = getShadowKillInfo(obj, self.__tutorialManager.getLastDestroyedAvatar)
                self.__tutorialManager.tutorialUI.ui.showTutorialShadowKillInfo(shadowKillParams)
                lessonData = self.__tutorialManager._tutorialData.lesson[self.__tutorialManager._currentLessonIndex]
                if voiceId != '':
                    self.__tutorialManager.playVoice(voiceId, True)
                showTimeout = obj.showTimeout
                self.__timeHideHint = BigWorld.time() + showTimeout if not obj.continuous() else ONE_DAY_DELAY
                self.__priority = priority
                self.__actionName = obj.action
                LOG_DEBUG('start action', self.__actionName, voiceId)
                self.__hideMarkerIcon = HIDE_MARKER.getNextValue(self.__hideMarkerIcon, obj.hideMarkerIcon)
                self.__hideMarkerArrow = HIDE_MARKER.getNextValue(self.__hideMarkerArrow, obj.hideMarkerArrow)
                self.__timeShown = BigWorld.time()
                self.__pauseData.schedulePause(True if obj.pause else None, obj.getCommandID())
                if not obj.continuous():
                    obj.onShow()
                self.setCondition(obj.conditionGenerated, -1, obj.conditionGeneratedDelay)
                self.__timeBlocked = BigWorld.time() + ONE_DAY_DELAY
            return

    def actionsUpdate(self, partIndex):
        if partIndex not in self.__actions:
            return
        else:
            genConditions = None
            for key in self.__actions[partIndex]:
                if self.__actions[partIndex][key].update(self.__conditions):
                    genConditions = self.__actions[partIndex][key].getGenConditions()
                    for data in genConditions:
                        self.setCondition(data[0], data[1])

            return

    def resetClear(self):
        self.hideTutorialHintControl()
        self.__timeBlocked = -1
        self.__hideMarkerIcon = HIDE_MARKER.NONE
        self.__hideMarkerArrow = HIDE_MARKER.NONE
        partIndex = self.__partIndex
        for cond in self.__conditions:
            self.__conditions[cond].onDestroy()

        self.__conditions.clear()
        for key in self.__hints[partIndex]:
            self.__hints[partIndex][key].reset()

        for key in self.__actions[partIndex]:
            self.__actions[partIndex][key].reset()

        if self.__pauseData.paused:
            self.__pauseData.paused = False
            BigWorld.player().tutorialPause(False)
        self.__timeHideHint = -1
        self.__priority = -1
        self.__target = None
        self.__actionName = ''
        self.__timeBlocked = -1
        self.__isEscapeMenu = False
        self.__continuousNeedHide = False
        self.__timeShown = 0
        self.__groupID = -1
        return

    def resetUpdate(self, partIndex):
        if not self.__resetSheduled:
            return
        else:
            BigWorld.player().tutorialRestartPart()
            self.__resetSheduled = None
            return

    def commandListenersCB(self, event = None):
        if event is not None and event.isRepeatedEvent():
            return False
        else:
            if event is not None:
                keyName = InputMapping.getKeyNameByCode(event.key)
                if keyName is not None and keyName in DISABLED_KEYS:
                    return
            if self.__isEscapeMenu:
                return False
            self.__pauseData.schedulePause(False, None)
            return

    def commandFilteredCB(self, commandID, isFired):
        input = GameEnvironment.getInput()
        if commandID == self.__pauseData.commandID:
            if isFired:
                self.__pauseData.schedulePause(False, None)
        return

    def pauseSetInputFilterData(self, data, callback):
        self.__pauseData.setInputFilterData(data, callback)

    def pauseUpdate(self, partIndex):
        input = GameEnvironment.getInput()
        if self.__pauseData.paused:
            if BigWorld.time() > self.__timeHideHint:
                if not self.__pauseData.inputAllowed:
                    self.__pauseData.inputAllowed = True
                    if self.__pauseData.commandID != -1:
                        input.commandProcessor.setFilter([self.__pauseData.commandID])
                        input.commandProcessor.addListeners(self.__pauseData.commandID, self.commandListenersCB)
                    else:
                        GlobalEvents.onKeyEvent += self.commandListenersCB
                    self.__pauseData.eventAdded = True
        elif self.__pauseData.inputFilterData is not None:
            self.__pauseData.inputFilterCB(self.__pauseData.inputFilterData)
            self.__pauseData.inputFilterData = None
            self.__pauseData.inputFilterCB = None
        if self.__pauseData.scheduled is None:
            return
        elif self.__pauseData.scheduled and self.__pauseData.paused:
            self.__pauseData.scheduled = None
            return
        else:
            self.__pauseData.paused = self.__pauseData.scheduled
            BigWorld.player().tutorialPause(self.__pauseData.paused)
            if self.__pauseData.paused:
                Condition.setPause(True)
                GameEnvironment.getHUD().disableForestallingPointUpdate(True)
                GameEnvironment.getHUD().disableBombTargetUpdate(True)
                self.__pauseData.inputAllowed = False
                self.__pauseData.filterAllowBackup = input.commandProcessor.getFilter()
                input.commandProcessor.setFilter([InputMapping.CMD_VISIBILITY_HUD] if self.__isEscapeMenu else list())
            else:
                Condition.setPause(False)
                GameEnvironment.getHUD().disableForestallingPointUpdate(False)
                GameEnvironment.getHUD().disableBombTargetUpdate(False)
                input.commandProcessor.setFilter(self.__pauseData.filterAllowBackup)
                if self.__pauseData.commandID != -1:
                    input.commandProcessor.removeListeners(self.__pauseData.commandID, self.commandListenersCB)
                else:
                    GlobalEvents.onKeyEvent -= self.commandListenersCB
                self.__pauseData.eventAdded = False
                self.__pauseData.commandID = None
                self.hideTutorialHintControl()
                timeDelta = BigWorld.time() - self.__timeShown
                for act in self.__hints[partIndex]:
                    self.__hints[partIndex][act].modifyActivateTime(timeDelta)

                for cond in self.__conditions:
                    self.__conditions[cond].modifyActivateTime()

            self.__pauseData.scheduled = None
            return

    def update(self):
        inputProfileType = InputMapping.g_instance.currentProfileType
        if self.__inputProfileType != inputProfileType:
            self.onInputProfileChanged(inputProfileType)
        partIndex = self.__tutorialManager._currentLessonPartIndex
        if self.__partIndex != partIndex:
            self.onPartChanged(partIndex)
        if not self.enabled():
            return
        else:
            self.resetUpdate(partIndex)
            if self.__resetSheduled is None:
                return
            self.conditionsUpdate(partIndex)
            self.markersUpdate()
            self.actionsUpdate(partIndex)
            self.hintsUpdate(partIndex)
            self.pauseUpdate(partIndex)
            return

    def loadLessonHints(self):
        self.clear()
        parents = []
        tutData = self.__tutorialManager._tutorialData
        lessonData = tutData.lesson[self.__tutorialManager._currentLessonIndex]
        for partInd in range(0, len(lessonData.lessonPart)):
            part = lessonData.lessonPart[partInd]
            if hasattr(part, 'hints'):
                data = part.hints
                for index in range(0, len(data.element)):
                    concreteType, dt = data.element[index].__dict__.items()[0]
                    hintParent = self.loadData(partInd, concreteType, dt)
                    if hintParent != '':
                        parents.append([partInd, hintParent])
                    self.__loaded = True

        for param in parents:
            self.__hints[param[0]][param[1]].childrenPresent = True

        self.enable(True)

    @property
    def loaded(self):
        return self.__loaded

    def clear(self):
        self.__loaded = False
        for partIndex in self.__hints:
            for action in self.__hints[partIndex]:
                self.__hints[partIndex][action].onDestroy()

        self.__hints = {}
        for partIndex in self.__actions:
            for action in self.__actions[partIndex]:
                self.__actions[partIndex][action].onDestroy()

        self.__actions = {}
        for cond in self.__conditions:
            self.__conditions[cond].onDestroy()

        self.__conditions.clear()
        self.__markerCBClearTarget = None
        self.__markerCBSetTarget = None
        return

    def onDestroy(self):
        if self.__pauseData.commandID is not None and self.__pauseData.eventAdded:
            if self.__pauseData.commandID != -1:
                commandProcessor = GameEnvironment.getInput().commandProcessor
                if commandProcessor is not None:
                    commandProcessor.removeListeners(self.__pauseData.commandID, self.commandListenersCB)
            else:
                GlobalEvents.onKeyEvent -= self.commandListenersCB
        self.__pauseData.onDestroy()
        GameEnvironment.g_instance.eHideBackendGraphics -= self.hideBackendGraphics
        GameEnvironment.g_instance.eShowBackendGraphics -= self.showBackendGraphics
        self.__tutorialManager = None
        self.clear()
        return

    def conditionPresent(self, name):
        if name in self.__conditions:
            return True
        return False

    def setCondition(self, name, duration = -1, delay = 0):
        if name == '':
            return
        if name in self.__conditions and IS_DEVELOPMENT:
            print '!!!!!!!!!!!!!!!!!!!!!!!! condition: [', name, '] already present'
            CONDITION_ALREADY_PRESENT
        self.__conditions[name] = Condition(name, duration, delay)

    def setConditionEx(self, condition):
        if condition.name == '':
            return
        if condition.name in self.__conditions and IS_DEVELOPMENT:
            print '!!!!!!!!!!!!!!!!!!!!!!!! condition: [', condition.name, '] already present'
            CONDITION_ALREADY_PRESENT
        self.__conditions[condition.name] = condition

    def removeCondition(self, name):
        if name in self.__conditions:
            self.__conditions[name].onDestroy()
            del self.__conditions[name]

    def prolongCondition(self, name, time):
        if name in self.__conditions:
            self.__conditions[name].prolong(time)
        else:
            self.setCondition(name, time)

    def hideTutorialHintControl(self):
        self.__tutorialManager.showTutorialHintControl('', None, False)
        self.__tutorialManager.tutorialUI.ui.showTutorialShadowHintControls(VOShadowElems(None))
        self.__tutorialManager.tutorialUI.ui.showTutorialShadowKillInfo(getShadowKillInfo(None))
        self.__tutorialManager.playVoice(-1, False)
        self.__continuousNeedHide = False
        if self.__actionName != '' and self.__actionName in self.__hints[self.__partIndex]:
            if self.__hints[self.__partIndex][self.__actionName].continuous():
                self.__hints[self.__partIndex][self.__actionName].onShow()
            self.removeCondition(self.__hints[self.__partIndex][self.__actionName].conditionGenerated)
            self.setCondition(self.__hints[self.__partIndex][self.__actionName].conditionGeneratedAfter, CONDITION_AFTER_TIMEOUT, self.__hints[self.__partIndex][self.__actionName].conditionGeneratedAfterDelay)
            self.__timeBlocked = BigWorld.time() + self.__hints[self.__partIndex][self.__actionName].blockTimeout()
        self.__tutorialManager.tutorialUI.ui.showTutorialHighlightControls(VOHighlightedElems(None), '')
        self.__timeHideHint = -1
        self.__priority = -1
        self.__actionName = ''
        if self.__hideMarkerIcon == HIDE_MARKER.HINT_END:
            self.__hideMarkerIcon = HIDE_MARKER.NONE
        if self.__hideMarkerArrow == HIDE_MARKER.HINT_END:
            self.__hideMarkerArrow = HIDE_MARKER.NONE
        return

    @property
    def hideMarkerIcon(self):
        if self.__hideMarkerIcon == HIDE_MARKER.NONE:
            return False
        return True

    @property
    def hideMarkerArrow(self):
        if self.__hideMarkerArrow == HIDE_MARKER.NONE:
            return False
        return True

    def enable(self, enable):
        self.__enabled = enable
        if not enable:
            self.hideTutorialHintControl()

    def enabled(self):
        return self.__enabled and self.__loaded

    def setTarget(self, vec, destName):
        self.__target = vec
        self.__destName = destName
        partIndex = self.__tutorialManager._currentLessonPartIndex
        Condition.setTarget(self.__target, self.__destName)
        for act in self.__hints[partIndex]:
            self.__hints[partIndex][act].setTarget(self.__target, self.__destName)

    def onWarningChanged(self, warning, active):
        warningStr = ''
        if warning == gui.hud.WarningType.COLLISION_WARNING:
            warningStr = 'warning_collision'
        elif warning == gui.hud.WarningType.STALL:
            warningStr = 'warning_stall'
        elif warning == gui.hud.WarningType.LOW_ALTITUDE:
            warningStr = 'warning_altitude'
        elif warning == gui.hud.WarningType.BORDER_TOO_CLOSE:
            warningStr = 'warning_border'
        if warningStr != '':
            if active:
                if not self.isPaused() and not self.conditionPresent(warningStr):
                    self.setCondition(warningStr)
            else:
                self.removeCondition(warningStr)

    def onDynamicCollision(self):
        partIndex = self.__tutorialManager._currentLessonPartIndex
        needSet = False
        if self.__lastCollisionTime < 0:
            self.__lastCollisionTime = BigWorld.time()
            needSet = True
        elif BigWorld.time() - self.__lastCollisionTime < 1.0:
            self.__lastCollisionTime = BigWorld.time()
        else:
            self.__lastCollisionTime = -1
            needSet = True
        if needSet:
            for act in self.__hints[partIndex]:
                self.__hints[partIndex][act].onDynamicCollision()

    def setMarkerData(self, markerVisible, arrowVisible):
        if not self.enabled():
            return
        if self.__markerVisible != markerVisible:
            for partIndex in self.__hints:
                for act in self.__hints[partIndex]:
                    self.__hints[partIndex][act].setMarkerData(markerVisible)

            self.__markerVisible = markerVisible
        if self.__arrowVisible and not arrowVisible:
            self.__arrowVisibleTime = BigWorld.time()
        self.__arrowVisible = arrowVisible

    def getMarkerData(self):
        markerPos, showFlags, hideMarker = self.markerActiveGetShowData()
        return (markerPos,
         not hideMarker and showFlags[0] and not self.hideMarkerIcon,
         not hideMarker and not self.hideMarkerArrow and BigWorld.time() - self.__arrowVisibleTime > TUTORIAL_MARKER_ARROW_DELAY,
         not hideMarker and showFlags[1],
         showFlags[2])

    def resetSheduled(self):
        self.__resetSheduled = True

    def showOvershadow(self, show):
        self.__tutorialManager.showOvershadow(show)

    def onEntityChangeHealth(self, entity, lastHealth):
        for key in self.__conditions:
            cond = self.__conditions[key]
            cond.onEntityChangeHealth(entity, lastHealth)

    def isPaused(self):
        if self.__pauseData.paused:
            return True
        if BigWorld.time() - Condition.pausedUnTime < 1:
            return True
        return False

    def onRequestPartRestart(self):
        self.resetClear()
        self.__resetSheduled = False

    def onRespawn(self):
        self.hideTutorialHintControl()

    def setGroupID(self, groupID):
        self.groupID = groupID
        if groupID < 0:
            return
        if self.__actionName != '' and self.__actionName in self.__hints[self.__partIndex] and self.__hints[self.__partIndex][self.__actionName].groupID != groupID:
            self.hideTutorialHintControl()