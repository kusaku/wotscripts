# Embedded file name: scripts/client/TutorialClient/TutorialManager.py
import GameEnvironment
import Keys
import BigWorld
from Helpers.i18n import localizeTutorial
import InputMapping
import Math
from OperationCodes import OPERATION_RETURN_CODE
from TeamObject import TeamObject
from TutorialClient.GunsOverheatedTrigger import GunsOverheatedTrigger
from TutorialClient.KeyInputTrigger import KeyInputTrigger
from TutorialClient.MouseLimitsTrigger import MouseLimitsTrigger
from TutorialClient.TutorialUIWrapper import TutorialUIWrapper, MouseLimitArea
from TutorialClient.UICaptionInputTrigger import UICaptionInputTrigger
from TutorialClient.HealthTrigger import HealthTrigger
from TutorialCommon.TutorialManagerBase import TutorialManagerBase
from TutorialObjects import TutorialObjects
from consts import AXIS_NAME_TO_INT_MAP, INPUT_SYSTEM_STATE, TutorialHintsInputEnum, TUTORIAL_AVATAR_DESTROYED_REASON
import consts
from debug_utils import LOG_ERROR, LOG_DEBUG
from gui.HUDconsts import HUD_HIGHLIGHT_TUTORIAL_OBJECT_COLOUR, TIME_FOR_POTENTIAL_TARGETS_AVATARS
from gui.MapBase import MarkerType
from gui.Scaleform.UI import TutorialCaptionParams, TutorialResultParams
from gui.Scaleform.Waiting import Waiting
from wgPickle import FromClientToServer, FromServerToClient
import GlobalEvents
from _performanceCharacteristics_db import airplanes
import math
import copy
from clientConsts import INPUT_SYSTEM_PROFILES, TUTORIAL_DATA_WAITING_SCREEN_MESSAGE
from TutorialHints import *
from TutorialActionHandlers import *
import Settings
from gui.WindowsManager import g_windowsManager
from EntityHelpers import EntityStates
from traceback import print_stack
from gui.hud import EntityTypes
from audio import GameSound

class TutorialManager(TutorialManagerBase):
    """
    tutorial manager
    """

    class __UITargetVisibleChecker(object):

        def __init__(self, onVisibleChangedDelegate):
            """
            """
            self.position = None
            self.__onVisibleDelegate = onVisibleChangedDelegate
            self.__objectData = None
            self.__objectId = None
            self.__isVisible = False
            self.__started = True
            return

        @property
        def objectData(self):
            return self.__objectData

        def clear(self):
            if self.__objectData is not None:
                self.__onVisibleDelegate(False, self.__objectData)
            self.__objectData = None
            self.__objectId = None
            return

        def setObjectData(self, objectData, objectId):
            self.__objectData = objectData
            self.__objectId = objectId

        def stop(self):
            self.__started = False
            self.__isVisible = False

        def start(self):
            self.__started = True

        def update(self):
            """
            update
            """
            if self.__objectData is not None and self.__started:
                visible = GameEnvironment.getHUD().isArrowPointerShown(self.__objectId)
                if self.__isVisible != visible:
                    self.__isVisible = visible
                    self.__onVisibleDelegate(self.__isVisible, self.__objectData)
            return

        def destroy(self):
            self.__objectData = None
            self.__objectId = None
            self.__onVisibleDelegate = None
            return

    __UPDATE_TIME = 0.02

    def safeUICallDecorator(func):
        """
        Decorator
        @param func:
        @return:
        """

        def wrapped_func(*args):
            if args[0].__tutorialUI is not None:
                func(*args)
            else:
                args[0].__actionsCache.append(lambda : func(*args))
            return

        return wrapped_func

    def __init__(self, owner, opReceiver):
        """
        
        @param owner: avatar
        @param opReceiver: avatar
        @return:
        """
        TutorialManagerBase.__init__(self, owner, consts.EXECUTOR_TYPE.CLIENT, opReceiver)
        self.__mouseLimits = None
        self.__tutorialUI = None
        self.__objectsManager = TutorialObjects()
        self.__updateCallbackId = -1
        self.__actionsCache = list()
        self.__startLessonOperation = None
        self._owner.onAutopilotEvent += self.__onAutopilot
        self.__hintParamsCached = None
        self.__uiTargets = dict()
        self.__uiTargetVisibleChecker = TutorialManager.__UITargetVisibleChecker(self.__onUITargetVisibleChanged)
        self.__lockNextNewTarget = False
        self.__isCurrentLessonDone = False
        self.__isAutopilotMsgBlocked = False
        self.__isAutopilotOn = False
        self.__loadingModelsCount = 0
        self.__autopilotVoiceId = None
        self.__autoPilotActivated = -1
        self.__raceHandler = None
        self.__markerHandler = None
        self.__speedController = None
        self.__countdownHandler = None
        self.__fpHighlightHandler = None
        self.__hintsManager = None
        self.__lessonFinishOperation = None
        self.__lessonStarted = False
        self.__endLessonCallbackId = -1
        self.__realStartLessonOperation = None
        self.__onInitUIStartLesson = False
        self.__mouseLocked = False
        self.__loadCompleted = False
        self.__markersInited = False
        self.__onInitMarkersStartLesson = False
        self.__destroyedAvatars = []
        self.__startUpdate()
        return

    @property
    def objectsManager(self):
        """
        @return: tutorial objects manager
        @rtype: TutorialObjects.TutorialObjects
        """
        return self.__objectsManager

    @property
    def tutorialUI(self):
        """
        tutorial UI
        @rtype: Tutorial.TutorialUIWrapper
        """
        return self.__tutorialUI

    def onEnterWorld(self):
        """
        onEnterWorld callback
        """
        GameEnvironment.getInput().commandProcessor.setFilter([])
        GameEnvironment.getCamera().setZoomEnable(False)
        GameEnvironment.getCamera().setSniperModeEnabled(False)
        GameEnvironment.getHUD().setMinimapVisible(False)
        GameEnvironment.getCamera().getDefualtStrategies['CameraStrategyMouse'].lockCursor()
        self.__mouseLocked = True
        GameEnvironment.getHUD().setBattleLoadingDisposeCondition(self.loadCompleted)

    def initTutorialUI(self):
        """
        Initializes tutorial UI
        """
        GameEnvironment.getHUD().setMinimapVisible(False)
        GameEnvironment.getHUD().setRadarVisible(False)
        from gui.WindowsManager import g_windowsManager
        self.__tutorialUI = TutorialUIWrapper(g_windowsManager.getBattleUI())
        self.__tutorialUI.setWarningCallback(self.onWarningChanged)
        BigWorld.worldDrawEnabled(False)

        def onInit():
            hud = GameEnvironment.getHUD()
            hud.setTargetPointerVisible(False)
            hud.setForestallingPointVisible(True)
            hud.setEnableArrowsForAllEntities(True)
            self.__tutorialUI.clearScreen()
            self.showOvershadow(False, True)
            BigWorld.worldDrawEnabled(True)
            if self.__onInitUIStartLesson:
                self.startLessonRequest()
                self.__onInitUIStartLesson = False

        self.__tutorialUI.showTutorial(onInit)
        GameEnvironment.getHUD().eAddEntity += self.__onAddEnemy
        for action in self.__actionsCache:
            action()

        del self.__actionsCache[:]

    def clearOnRestart(self):
        if self.__raceHandler is not None:
            self.__raceHandler.onDestroy()
        self.__raceHandler = None
        if self.__markerHandler is not None:
            self.__markerHandler.onDestroy()
        self.__markerHandler = None
        if self.__countdownHandler is not None:
            self.__countdownHandler.onDestroy()
        self.__countdownHandler = None
        if self.__fpHighlightHandler is not None:
            self.__fpHighlightHandler.onDestroy()
        self.__fpHighlightHandler = None
        if self.__speedController is not None:
            self.__speedController.onDestroy()
        self.__speedController = None
        if self.__hintsManager is not None:
            self.__hintsManager.onDestroy()
        self.__hintsManager = None
        self.__destroyedAvatars = []
        self.__lessonStarted = False
        self.__loadCompleted = False
        return

    def destroy(self):
        """
        Destructor
        """
        self.__stopUpdate()
        if self.__mouseLimits is not None:
            self.__mouseLimits.destroy()
            self.__mouseLimits = None
        input = GameEnvironment.getInput()
        if input is not None and input.commandProcessor is not None:
            input.commandProcessor.setFilter(None)
        self._owner.onAutopilotEvent -= self.__onAutopilot
        TutorialManagerBase.destroy(self)
        if self.__tutorialUI:
            self.__tutorialUI.destroy()
            self.__tutorialUI = None
        self.__objectsManager.removeAll()
        self.__objectsManager = None
        self.__uiTargetVisibleChecker.destroy()
        self.__uiTargetVisibleChecker = None
        if self.__mouseLocked:
            GameEnvironment.getCamera().getDefualtStrategies['CameraStrategyMouse'].unlockCursor()
            self.__mouseLocked = False
        GameEnvironment.getHUD().setBattleLoadingDisposeCondition(None)
        self.clearOnRestart()
        return

    def _createTrigger(self, type, data, operation):
        if type == 'UICaptionInputTrigger':
            if self.__tutorialUI is None:
                self.__actionsCache.append(lambda : self._addNewTrigger(type, data, operation))
                return
            else:
                return UICaptionInputTrigger(self, data, operation)
        else:
            if type == 'keyInputTrigger':
                return KeyInputTrigger(self, self._owner, data, operation)
            if type == 'mouseLimitsTrigger':
                if self.__mouseLimits is None:
                    LOG_ERROR('Mouse limits are not shown on screen')
                return MouseLimitsTrigger(data, operation, self.__tutorialUI.ui)
            if type == 'gunsOverheatedTrigger':
                return GunsOverheatedTrigger(self._owner, data, operation)
            if type == 'healthTrigger':
                return HealthTrigger(data, operation)
        return

    def unassignedCommands(self, keys):
        curMapping = InputMapping.g_instance.getCurMapping()
        res = []
        for key in keys:
            arr = None
            attr = getattr(InputMapping, key, -1)
            if attr != -1:
                found = False
                arr = curMapping[attr]['keyNames']
                for data in arr:
                    if data['name'] != 'KEY_NONE':
                        found = True
                        break

                if not found:
                    res.append(key)

        return res

    def checkUnassignedCommands(self):
        lessonData = self._tutorialData.lesson[self._currentLessonIndex]
        res = self.unassignedCommands(lessonData.forceKeys)
        if res:
            Settings.g_instance.cmdFilter = res
            self.tutorialUI.ui.showTutorialOptions()

    @safeUICallDecorator
    def _onStartLessonRequest(self, operation):
        self.__startLessonOperation = operation
        lessonData = self._tutorialData.lesson[self._currentLessonIndex]
        self.__loadingModelsCount = len(lessonData.cache.object) if hasattr(lessonData.cache, 'object') else 0
        if self.__loadingModelsCount > 0:

            def onModelsLoaded():
                self.__loadingModelsCount -= 1
                if self.__loadingModelsCount == 0:
                    self.__loadCompleted = True

            for objectCache in lessonData.cache.object:
                self.__objectsManager.add(objectCache.objectName, Math.Vector3(), Math.Vector3(), objectCache.modelPath, objectCache.texturePath, None, False, onModelsLoaded)

        else:
            self.__loadCompleted = True
        if not self.__tutorialUI.initialized:
            self.__onInitUIStartLesson = True
        else:
            self.startLessonRequest()
        return

    def loadCompleted(self):
        return self.__loadCompleted

    def markersInited(self):
        self.__markersInited = True
        if self.__onInitMarkersStartLesson:
            self.startLessonRequest()

    def checkBotLoaded(self):
        lessonData = self._tutorialData.lesson[self._currentLessonIndex]
        for botData in lessonData.cache.bot:
            if not GameEnvironment.getClientArena().getAvatarInfoByName(botData.name):
                return False

        return True

    @safeUICallDecorator
    def startLessonRequest(self):
        """
        @type operation: ReceivedOperation
        """
        if not self.__markersInited:
            self.__onInitMarkersStartLesson = True
            return
        self.__isAutopilotMsgBlocked = False
        lessonData = self._tutorialData.lesson[self._currentLessonIndex]
        self.clearOnRestart()
        self.checkUnassignedCommands()

        def showStartHUD():
            """
            captionParams = TutorialCaptionParams();
            captionParams.title = lessonData.captionTitle;
            captionParams.message = lessonData.captionMessage;
            
            callback = None;
            self.__isCurrentLessonDone = operation.args[1];
            if(self.__isCurrentLessonDone):
                captionParams.isAction1 = True;
                captionParams.nameAction1 = lessonData.examBtnText;
                callback = lambda : self.__startLesson(OPERATION_RETURN_CODE.START_EXAM);
            else:
                #show lesson reward description
                captionParams.isBonus = True;
                captionParams.nameReward = lessonData.nameReward;
                captionParams.countCredits = lessonData.countCredits;
                captionParams.nameCredits = lessonData.nameCredits;
                captionParams.nameExperience = lessonData.nameExperience;
                captionParams.countExperience = lessonData.countExperience;
                captionParams.nameGolds = lessonData.nameGold;
                captionParams.countGolds = lessonData.countGold;
            
            self.__tutorialUI.showCaption(tutorialCaptionParams = captionParams, action1BtnCallback= callback);
            
            self.__tutorialUI.showHint(text = lessonData.hintMessage, pictures = lessonData.hintImages, additionalText=lessonData.hintAdditionalText);
            
            self.__tutorialUI.ui.onTutorialMouseClick += self.__onMouseClick;
            GlobalEvents.onKeyEvent += self.__onStartLessonKeyEvent;
            """
            self.__isCurrentLessonDone = self.__startLessonOperation.args[1]
            self.__hintsManager = HintsManager(self)
            self.__hintsManager.loadLessonHints()
            self.__hintsManager.setLockTargetCallbacks(self.__clearTarget, self.__lockNextTarget)
            self.__startLesson(OPERATION_RETURN_CODE.SUCCESS)

        showStartHUD()

    def onTRClose(self):
        self.__lessonFinishOperation.sendResponse(OPERATION_RETURN_CODE.SUCCESS)
        self.__onTRClear()

    def onTRContinue(self):
        self.__lessonFinishOperation.sendResponse(OPERATION_RETURN_CODE.NEXT_LESSON)
        self.__onTRClear()

    def onTRRestart(self):
        self.__lessonFinishOperation.sendResponse(OPERATION_RETURN_CODE.RESTART_LESSON)
        self.__onTRClear()

    def onTRInitialized(self):
        import BWPersonality
        lessonData = self._tutorialData.lesson[self._currentLessonIndex]
        trParams = TutorialResultParams()
        trParams.header = localizeTutorial(lessonData.endCaptionTitle)
        trParams.title = localizeTutorial(lessonData.endCaptionTitle)
        isTutorialComplete = self.__lessonFinishOperation.args[0]
        lessonDuration = self.__lessonFinishOperation.args[1]
        BWPersonality.g_tutorialForbidLessons = self.__lessonFinishOperation.args[2]
        trParams.lessonIndex = self._currentLessonIndex
        trParams.type = 2
        hours, remainder = divmod(lessonDuration, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            timeStr = '%d:%02d:%02d' % (hours, minutes, seconds)
        else:
            timeStr = '%d:%02d' % (minutes, seconds)
        trParams.description1 = localizeTutorial(lessonData.endCaptionMessageShort)
        trParams.time = timeStr
        trParams.description2 = localizeTutorial(lessonData.endCaptionMessage)
        trParams.textCompleted = ''
        trParams.isLastLesson = (trParams.lessonIndex >= len(self._tutorialData.lesson) - 1 or trParams.lessonIndex + 1 in BWPersonality.g_tutorialForbidLessons) and self._tutorialData.lesson[self._currentLessonIndex + 1 if self._currentLessonIndex + 1 < len(self._tutorialData.lesson) else 0].requiredLessonId != trParams.lessonIndex
        self.__tutorialUI.setTRCallbacks(self.onTRClose, self.onTRContinue, None, self.onTRRestart)
        if not self.__isCurrentLessonDone:
            trParams.isBonus = True
            trParams.nameReward = localizeTutorial(lessonData.nameReward)
            trParams.nameCredits = localizeTutorial(lessonData.nameCredits)
            trParams.countCredits = lessonData.countCredits
            trParams.nameExperience = localizeTutorial(lessonData.nameExperience)
            trParams.countExperience = lessonData.countExperience
            trParams.nameGolds = localizeTutorial(lessonData.nameGold)
            trParams.countGolds = lessonData.countGold
        else:
            trParams.textCompleted = localizeTutorial(lessonData.lobbyTitleCompleted)
        self.__tutorialUI.ui.setTutorialResult(trParams)
        self.__endLessonCallbackId = BigWorld.callback(self._tutorialData.showResultScreenTimeout, self.onTRClose)
        return

    def __onTRClear(self):
        if self.__tutorialUI is not None:
            self.__tutorialUI.setTRCallbacks(None, None, None, None)
        self.__lessonFinishOperation = None
        if self.__endLessonCallbackId != -1:
            BigWorld.cancelCallback(self.__endLessonCallbackId)
            self.__endLessonCallbackId = -1
        return

    def _onRequestFinishLesson(self, operation):
        self.__isAutopilotMsgBlocked = True
        self.__tutorialUI.showTutorialResult(self.onTRInitialized)
        self.__uiTargetVisibleChecker.clear()
        self.__objectsManager.removeAll()
        self.__hintsManager.enable(False)
        self.__lessonFinishOperation = operation

    def _onFinishLesson(self):
        self.__tutorialUI.ui.showShadow(True, True)

    def __onStartLessonKeyEvent(self, event):
        if event.key != Keys.KEY_LEFTMOUSE and event.key != Keys.KEY_ESCAPE and event.isKeyUp() and self._owner.isFlyKeyBoardInputAllowed():
            self.__startLesson(OPERATION_RETURN_CODE.SUCCESS)

    def __onMouseClick(self):
        self.__startLesson(OPERATION_RETURN_CODE.SUCCESS)

    def __startLesson(self, operationReturnCode):
        self.__startLessonOperation.sendResponse(operationReturnCode)
        self.__startLessonOperation = None
        self.__lessonStarted = True
        GameEnvironment.getCamera().getDefualtStrategies['CameraStrategyMouse'].unlockCursor()
        self.__mouseLocked = False
        return

    def __onAutopilot(self, isOn):
        if isOn == self.__isAutopilotOn:
            return
        else:
            self.__isAutopilotOn = isOn
            if isOn:
                if self.__hintsManager is not None:
                    self.__hintsManager.setCondition('autopilot')
                self.showOvershadow(True)
            else:
                if self.__hintsManager is not None:
                    self.__hintsManager.removeCondition('autopilot')
                self.showOvershadow(False)
            return

    def __onAddEnemy(self, entity):
        if self.__lockNextNewTarget:
            self.__lockNextTarget()

    def __lockNextTarget(self):
        hud = GameEnvironment.getHUD()
        hud.selectNextEntity(EntityTypes.UNKNOWN)
        if hud.targetEntity is not None and isinstance(hud.targetEntity, TeamObject):
            hud.disableForestallingPointForCurrentTarget()
        return

    def __clearTarget(self):
        GameEnvironment.getHUD().clearTarget()

    def __onUITargetVisibleChanged(self, isVisible, targetData):
        if not targetData.uiTargetHintMessage:
            return
        else:
            if isVisible:
                self.__tutorialUI.showHint(targetData.uiTargetHintMessage)
            elif self.__hintParamsCached is not None:
                self.__tutorialUI.showHint(*self.__hintParamsCached)
            return

    def __startUpdate(self):
        if self.__updateCallbackId == -1:
            self.__updateCallbackId = BigWorld.callback(TutorialManager.__UPDATE_TIME, self.__update)

    def __update(self):
        TutorialManagerBase.update(self, TutorialManager.__UPDATE_TIME)
        if self.__mouseLimits is not None:
            self.__mouseLimits.update()
        self.__uiTargetVisibleChecker.update()
        if self.__updateCallbackId != -1:
            self.__updateCallbackId = BigWorld.callback(TutorialManager.__UPDATE_TIME, self.__update)
        if self.__raceHandler is not None:
            self.__raceHandler.update()
        if self.__speedController is not None:
            self.__speedController.update()
        hintsManager = None
        if self.__hintsManager is not None and self.__hintsManager.enabled() and not Waiting.isVisible():
            hintsManager = self.__hintsManager
        allowFPBlink = True
        if hintsManager is not None:
            hintsManager.update()
            if self.__markerHandler is not None:
                markerPos, markerVisible, arrowVisible, distanceVisible, allowFPBlink = hintsManager.getMarkerData()
                resMarkerVisible, resArrowVisible = self.__markerHandler.update(markerPos, markerVisible, arrowVisible, distanceVisible)
                hintsManager.setMarkerData(resMarkerVisible, resArrowVisible)
        if self.__fpHighlightHandler is not None:
            self.__fpHighlightHandler.update(allowFPBlink)
        return

    def __stopUpdate(self):
        if self.__updateCallbackId != -1:
            BigWorld.cancelCallback(self.__updateCallbackId)
            self.__updateCallbackId = -1

    @safeUICallDecorator
    def __headerActionHandler(self, type, data):
        if data.resetInputAxis:
            GameEnvironment.getInput().inputAxis.restart(True)
        self.__tutorialUI.showHeader(data.title, data.message, getattr(data, 'message2', ''), getattr(data, 'commandId', None), getattr(data, 'image', None))
        return

    def __resetInputAxesHandler(self, type, data):
        GameEnvironment.getInput().inputAxis.restart(True)

    @safeUICallDecorator
    def __hintActionHandler(self, type, data):
        fadeoutTime = data.__dict__.get('fadeoutTime', None)
        additionalText = data.__dict__.get('additionalText', None)
        self.__hintParamsCached = (data.text,
         fadeoutTime,
         getattr(data, 'images', None),
         getattr(data, 'commandId', None),
         additionalText)
        self.__tutorialUI.showHint(*self.__hintParamsCached)
        return

    def __hideObjectActionHandler(self, type, data):
        object = self.__objectsManager.getObjectById(data.objectName)
        if object is None:
            return
        else:
            if self.__uiTargets.has_key(data.objectName):
                GameEnvironment.getHUD().removeTargetObject(self.__uiTargets.pop(data.objectName))
                if self.__uiTargetVisibleChecker.objectData.objectName == data.objectName:
                    self.__uiTargetVisibleChecker.clear()
            object.visible = False
            return

    def __updateObjectActionHandler(self, type, data):
        object = self.__objectsManager.getObjectById(data.objectName)
        if hasattr(data, 'texturePath'):
            object.setTexture(data.texturePath)
        if hasattr(data, 'position'):
            object.setPosition(data.position)
        if hasattr(data, 'lookAt'):
            object.lookAt(data.lookAt.position, data.lookAt.roll)
        elif hasattr(data, 'rotation'):
            object.setRotation((data.rotation.yaw, data.rotation.pitch, data.rotation.roll))
        if data.uiTarget:
            if not self.__uiTargets.has_key(data.objectName):
                matrix = Math.Matrix()
                matrix.translation = data.position
                uiTargetId = GameEnvironment.getHUD().addTargetObject(matrix, EntityTypes.POSITIVE_TARGET_OBJECT, True, HUD_HIGHLIGHT_TUTORIAL_OBJECT_COLOUR, True, TIME_FOR_POTENTIAL_TARGETS_AVATARS)
                self.__uiTargetVisibleChecker.setObjectData(data, uiTargetId)
                self.__uiTargets[data.objectName] = uiTargetId
        elif self.__uiTargets.has_key(data.objectName):
            GameEnvironment.getHUD().removeTargetObject(self.__uiTargets.pop(data.objectName))
            if self.__uiTargetVisibleChecker.objectData.objectName == data.objectName:
                self.__uiTargetVisibleChecker.clear()

    def __showObjectActionHandler(self, type, data):
        object = self.__objectsManager.getObjectById(data.objectName)
        if object is None:
            return
        else:
            object.visible = True
            object.setScale(data.scale)
            object.setPosition(self._owner.position + self._owner.getRotation().rotateVec(data.position) if data.playerPositionRelative else data.position)
            if hasattr(data, 'lookAt'):
                object.lookAt(self._owner.position + data.lookAt.position if data.playerPositionRelative else data.lookAt.position, data.lookAt.roll)
            elif hasattr(data, 'rotation'):
                object.setRotation((data.rotation.yaw, data.rotation.pitch, data.rotation.roll))
            if data.uiTarget:
                matrix = Math.Matrix()
                matrix.translation = data.position
                uiTargetId = GameEnvironment.getHUD().addTargetObject(matrix, EntityTypes.POSITIVE_TARGET_OBJECT, True, HUD_HIGHLIGHT_TUTORIAL_OBJECT_COLOUR, True, TIME_FOR_POTENTIAL_TARGETS_AVATARS)
                self.__uiTargets[data.objectName] = uiTargetId
                self.__uiTargetVisibleChecker.setObjectData(data, uiTargetId)
            return

    def setInputFilter(self, data):
        if data.allowKeyCommands:
            GameEnvironment.getInput().commandProcessor.setFilter(None)
        else:
            GameEnvironment.getInput().commandProcessor.setFilter([ InputMapping.g_descriptions.getCommandIntID(commandName) for commandName in data.keyCommand ])
        return

    def __setInputFilterActionHandler(self, type, data):
        if self.__hintsManager is None:
            return
        else:
            self.__hintsManager.pauseSetInputFilterData(data, self.setInputFilter)
            if data.allowKeyCommands:
                self.tutorialUI.ui.setTutorialAmmoLock(False, False, False)
            else:
                self.tutorialUI.ui.setTutorialAmmoLock('CMD_LAUNCH_ROCKET' not in data.keyCommand, 'CMD_LAUNCH_BOMB' not in data.keyCommand, 'CMD_PRIMARY_FIRE' not in data.keyCommand)
            GameEnvironment.getCamera().setZoomEnable(data.allowCameraZoom)
            GameEnvironment.getCamera().setSniperModeEnabled(data.allowSniperMode)
            return

    @safeUICallDecorator
    def __showMouseLimitsActionHandler(self, type, data):
        self.__mouseLimits = MouseLimitArea(self.__tutorialUI.ui, self._owner, data.width, data.height, data.offsetX, data.offsetY, data.lockOnHorizon)

    @safeUICallDecorator
    def __hideMouseLimitsActionHandler(self, type, data):
        if self.__mouseLimits is not None:
            self.__mouseLimits.destroy()
            self.__mouseLimits = None
        return

    @safeUICallDecorator
    def __uiTimerActionHandler(self, type, data):
        if hasattr(data, 'visible'):
            self.__tutorialUI.setTimerVisible(data.visible)
        if hasattr(data, 'isRunning'):
            self.__tutorialUI.setTimerRunning(data.isRunning)
        if getattr(data, 'resetTimer', False):
            self.__tutorialUI.resetTimer()

    @safeUICallDecorator
    def __uiClearScreenActionHandler(self, type, data):
        self.__tutorialUI.clearScreen(True)
        self.__hintParamsCached = None
        return

    @safeUICallDecorator
    def __uiOvershadowScreenActionHandler(self, type, data):
        self.showOvershadow(data.visible)

    def __lockNextNewTargetActionHandler(self, type, data):
        self.__lockNextNewTarget = data.isActive
        self.__lockNextTarget()

    @safeUICallDecorator
    def __setHUDElementsVisibleActionHandler(self, type, data):
        self.__tutorialUI.ui.setElementsVisible(data)
        if hasattr(data, 'minimap'):
            GameEnvironment.getHUD().setMinimapVisible(data.minimap)
        if hasattr(data, 'radar'):
            GameEnvironment.getHUD().setRadarVisible(data.radar)
        if hasattr(data, 'targetWindow'):
            GameEnvironment.getHUD().setMiniScreenVisible(data.targetWindow)
        if hasattr(data, 'battleArrows'):
            GameEnvironment.getHUD().setTargetPointerVisible(data.battleArrows)

    def __blockAutopilotMsgActionHandler(self, type, data):
        self.__isAutopilotMsgBlocked = data.isBlocked
        self.__onAutopilot(self.__isAutopilotOn)

    def playVoice(self, voiceId, enable):
        if enable:
            GameSound().voice.playTutorial(voiceId)
        else:
            GameSound().voice.stopTutorial()

    def __playVoiceActionHandler(self, type, data):
        self.playVoice(data.voiceId, True)

    def __stopVoiceActionHandler(self, type, data):
        self.playVoice(-1, False)

    def __minimapMarkersActionHandler(self, type, data):
        if data.isVisible:
            for pos in data.worldPosition:
                GameEnvironment.getHUD().minimap.setMarker(pos.x, pos.z, MarkerType.DEFAULT, 0)

        else:
            GameEnvironment.getHUD().minimap.removeAllMarkers()

    def __raceActionHandler(self, type, data):
        if data.enabled:
            if self.__raceHandler is not None:
                self.__raceHandler.onDestroy()
            self.__raceHandler = RaceHandler(data.splineName, data.caption, self._tutorialData.splinePointRadius, self.tutorialUI.ui)
        else:
            self.__raceHandler.onDestroy()
            self.__raceHandler = None
        return

    def __setProgressBarActionHandler(self, type, data):
        self.tutorialUI.ui.setProgressBarValue(data.segmentIndex, localizeTutorial(data.caption), data.segmentNum)

    def __speedControllerActionHandler(self, type, data):
        if data.enabled:
            if self.__speedController is not None:
                self.__speedController.onDestroy()
            self.__speedController = SpeedController(self._owner)
        else:
            self.__speedController.onDestroy()
            self.__speedController = None
        return

    def __setConditionActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            self.__hintsManager.setCondition(data.name, data.duration, data.delay)
            return

    def __setConditionAreaActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            condition = ConditionArea(data.name, data.duration, data.delay, data.center, data.radius, data.inside)
            self.__hintsManager.setConditionEx(condition)
            return

    def __setConditionAreaTargetActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            condition = ConditionAreaTarget(data.name, data.duration, data.delay, data.radius, data.inside)
            self.__hintsManager.setConditionEx(condition)
            return

    def __setConditionConusActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            condition = ConditionConus(data.name, data.nameSrc, data.nameTarget, data.heightDeltaUp, data.heightDelta, data.widthDelta, data.invert, data.duration, data.delay)
            self.__hintsManager.setConditionEx(condition)
            return

    def __setConditionFlapsActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            generator = ConditionFlaps(data.name, data.invert, data.duration, data.delay)
            self.__hintsManager.setConditionEx(generator)
            return

    def __setConditionSpeedDeltaActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            generator = ConditionSpeedDelta(data.name, data.nameSrc, data.nameTarget, data.speedDelta, data.invert, data.duration, data.delay)
            self.__hintsManager.setConditionEx(generator)
            return

    def __setConditionHeightDeltaActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            generator = ConditionHeightDelta(data.name, data.nameSrc, data.nameTarget, data.deltaMin, data.deltaMax, data.invert, data.duration, data.delay)
            self.__hintsManager.setConditionEx(generator)
            return

    def __setConditionTurnTowardsActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            generator = ConditionTurnTowards(data.name, data.nameSrc, data.nameTarget, data.turnDuration, data.duration, data.delay)
            self.__hintsManager.setConditionEx(generator)
            return

    def __setConditionAngleActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            generator = ConditionAngle(data.name, data.nameSrc, data.nameTarget, data.angleMin, data.angleMax, data.inAngles, data.duration, data.delay)
            self.__hintsManager.setConditionEx(generator)
            return

    def __setConditionFiringActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            generator = ConditionFiring(data.name, data.nameSrc, data.invert, data.duration, data.delay)
            self.__hintsManager.setConditionEx(generator)
            return

    def __setConditionDamPartsActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            generator = ConditionDamgedParts(data.name, data.nameParts, data.invert, data.duration, data.delay)
            self.__hintsManager.setConditionEx(generator)
            return

    def __setConditionBombingActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            generator = ConditionBombing(data.name, data.position, data.radius, data.invert, data.duration, data.delay)
            self.__hintsManager.setConditionEx(generator)
            return

    def __setConditionBombingAngleActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            generator = ConditionBombingAngle(data.name, data.invert, data.duration, data.delay)
            self.__hintsManager.setConditionEx(generator)
            return

    def __setConditionCommandActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            generator = ConditionCommand(data.name, data.commandID, data.blocked, data.duration, data.delay)
            self.__hintsManager.setConditionEx(generator)
            return

    def __setConditionDestructionActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            damageType = 'any'
            if hasattr(data, 'damage'):
                damageType = data.damage
            generator = ConditionDestruction(data.name, data.entityName, damageType, data.duration, data.delay)
            self.__hintsManager.setConditionEx(generator)
            return

    def __setConditionHitActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            generator = ConditionHit(data.name, data.source, data.target, data.duration, data.delay)
            self.__hintsManager.setConditionEx(generator)
            return

    def __setConditionBRPresentActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            generator = ConditionBRPresent(data.name, data.invert, data.duration, data.delay)
            self.__hintsManager.setConditionEx(generator)
            return

    def __removeConditionActionHandler(self, type, data):
        if self.__hintsManager is None or data.name == '':
            return
        else:
            self.__hintsManager.removeCondition(data.name)
            return

    def __setHintsGroupActionHandler(self, type, data):
        if self.__hintsManager is None:
            return
        else:
            self.__hintsManager.setGroupID(data.groupID)
            return

    def showOvershadow(self, value, slowFade = True):
        if self.tutorialUI is None:
            return
        else:
            self.tutorialUI.ui.showShadow(value, slowFade)
            return

    def onAvatarDestroyed(self):
        self.showOvershadow(True)

    def onRespawn(self):
        player = BigWorld.player()
        if player is not None:
            player.eUpdateEngineTemperature(player.engineTemperature, player.wepWorkTime, False)
        if self.__hintsManager is None:
            return
        else:
            if GameEnvironment.getHUD().lastDamageType == TUTORIAL_AVATAR_DESTROYED_REASON.GROUND:
                self.__hintsManager.setCondition('death_ground', 1)
            elif GameEnvironment.getHUD().lastDamageType == TUTORIAL_AVATAR_DESTROYED_REASON.RAMMING_AVATAR:
                self.__hintsManager.setCondition('death_avatar', 1)
            if GameEnvironment.getHUD().lastDamageType != TUTORIAL_AVATAR_DESTROYED_REASON.NONE:
                self.__hintsManager.setCondition('death_any', 1)
            self.__hintsManager.onRespawn()
            return

    def onGameStateChanged(self, avatar, state):
        if not self.__lessonStarted:
            return
        if avatar.id == BigWorld.player().id:
            if state & EntityStates.DESTROYED:
                self.onAvatarDestroyed()
            elif state & EntityStates.GAME_CONTROLLED:
                self.onRespawn()
        elif (state & EntityStates.DESTROYED or state & EntityStates.DESTROYED_FALL) and avatar.id not in self.__destroyedAvatars:
            self.__destroyedAvatars.append(avatar.id)

    def getLastDestroyedAvatar(self, ally = True):
        size = len(self.__destroyedAvatars)
        if size == 0:
            return
        else:
            clientArena = GameEnvironment.getClientArena()
            player = BigWorld.player()
            for ind in range(size):
                avatar = BigWorld.entities.get(self.__destroyedAvatars[size - ind - 1], None)
                if avatar is None:
                    continue
                if ally:
                    if avatar.teamIndex == player.teamIndex:
                        return avatar
                elif avatar.teamIndex != player.teamIndex:
                    return avatar

            return

    def showTutorialHintControl(self, funcString, params, enable):
        self.__tutorialUI.ui.showTutorialHintControl(funcString, params, enable)

    def __setMarkerActionHandler(self, type, data):
        if self.__hintsManager is not None:
            conditionHide = ''
            if hasattr(data, 'conditionHide'):
                conditionHide = data.conditionHide
            self.__hintsManager.markerAdd(data.index, data.target, data.targetEntity, data.showDistance, data.showMarker, data.showFPBlink, data.conditionNext, data.conditionGen, conditionHide, data.lockTarget)
        return

    def __setMarkerActiveActionHandler(self, type, data):
        if self.__hintsManager is not None:
            self.__hintsManager.markerSetActive(data.index)
            if self.__markerHandler is None:
                self.__markerHandler = MarkerHandler(self.tutorialUI.ui)
        return

    def __removeMarkerActionHandler(self, type, data):
        if self.__hintsManager is not None:
            self.__hintsManager.markerClearAll()
        if self.__markerHandler is not None:
            self.__markerHandler.onDestroy()
            self.__markerHandler = None
        return

    def __countdownActionHandler(self, type, data):
        if self.__countdownHandler is not None:
            self.__countdownHandler.onDestroy()
        self.__countdownHandler = CountdownHandler(data.time, self.tutorialUI.ui)
        return

    def __forestallingPointHighlightActionHandler(self, type, data):
        if self.__fpHighlightHandler is not None:
            self.__fpHighlightHandler.onDestroy()
            self.__fpHighlightHandler = None
        if data.enable:
            self.__fpHighlightHandler = FPHighlightHandler(self.tutorialUI.ui)
        return

    def __resetCameraActionHandler(self, type, data):
        GameEnvironment.getInput().inputAxis.setAssaultMode(False)
        GameEnvironment.getCamera().resetToMinZoom()
        if data.enabled:
            GameEnvironment.getCamera().getDefualtStrategies['CameraStrategyMouse'].resetCursor()

    def __showEffectActionHandler(self, type, data):
        EffectManager.g_instance.createWorldEffect(Effects.getEffectId(data.effectID), data.position, {})

    def __showBotEffectActionHandler(self, type, data):
        ids = GameEnvironment.getClientArena().findIDsByPlayerName(data.botName)
        if len(ids) > 0:
            entity = BigWorld.entities.get(ids[0], None)
            if entity is not None:
                entity.controllers['modelManipulator'].setEffectVisible(data.effectID, data.enable)
        return

    def __setSpeechLevelActionHandler(self, type, data):
        if data.level == 'tutorial':
            GameSound().voice.enableGameMsgs(False)
        elif data.level == 'all':
            GameSound().voice.enableGameMsgs(True)

    def onHideModalScreen(self, movieName = None):
        if movieName is not None and movieName == 'Options':
            self.checkUnassignedCommands()
        return

    def onWarningChanged(self, warning, active):
        if self.__hintsManager is not None and self.__hintsManager.enabled():
            self.__hintsManager.onWarningChanged(warning, active)
        return

    def onDynamicCollision(self):
        if self.__hintsManager is not None:
            self.__hintsManager.onDynamicCollision()
        return

    def _onStartLessonRealRequest(self, operation):
        operation.sendResponse(OPERATION_RETURN_CODE.SUCCESS)

    def _onRequestPartRestart(self, operation):
        GameEnvironment.getHUD().clear()
        self.__destroyedAvatars = []
        if self.__hintsManager is not None:
            self.__hintsManager.onRequestPartRestart()
        return

    def onEntityChangeHealth(self, entity, lastHealth):
        if self.__hintsManager is not None:
            self.__hintsManager.onEntityChangeHealth(entity, lastHealth)
        return

    def isPaused(self):
        if self.__hintsManager is None:
            return False
        else:
            return self.__hintsManager.isPaused()