# Embedded file name: scripts/client/TutorialClient/TutorialUIWrapper.py
import math
from Helpers.i18n import localizeTutorial
import InputMapping
import Math
from debug_utils import LOG_DEBUG
from gui.Scaleform.UI import TutorialHintParams, TutorialHeaderParams
import BigWorld

class TutorialUIWrapper(object):
    """
    Provides a more convenient way to work with tutorial UI
    """

    class __ScreenCache:

        def __init__(self):
            self.clear()

        def clear(self):
            self.headerParams = None
            self.hintParams = None
            self.isTimerVisible = False
            return

    def __init__(self, ui):
        """
        Constructor
        @param ui: UI manager
        @type ui: UI
        """
        self.ui = ui
        self.ui.onTutorialUIBtnClick += self.__onBtnPressed
        self.ui.onTutorialInitialized += self.__onTutorialInitialized
        self.ui.onGetTimer += self.__onGetTimer
        self.ui.onTutorialPaused += self.__onTutorialPaused
        self.ui.onTutorialResultInitialized += self.onTRInitialized
        self.ui.onTutorialResultClose += self.onTRClose
        self.ui.onTutorialResultContinue += self.onTRContinue
        self.ui.onTutorialResultReject += self.onTRReject
        self.ui.onTutorialResultRestart += self.onTRRestart
        self.ui.onWarningChanged += self.onWarningChanged
        self.__callbacks = dict()
        self.__callbacksCounter = 0
        self.__initializing = False
        self.__initialized = False
        self.__onInitializedCallback = None
        self.__onGetTimerCallback = None
        self.__cbTRInitialized = None
        self.__cbTRClose = None
        self.__cbTRContinue = None
        self.__cbTRReject = None
        self.__cbTRRestart = None
        self.__cbWarningChanged = None
        self.__actionsQueue = list()
        self.__isLimitAreaVisible = False
        self.__isLimitAreaVisibleEx = False
        self.__isTutorialPaused = False
        self.__lastHeaderParams = None
        self.__lastHintParams = None
        self.__isTimerVisible = False
        self.__screenCache = TutorialUIWrapper.__ScreenCache()
        InputMapping.g_instance.onSaveControls += self.__onInputControlsSave
        return

    def isTutorialPaused(self):
        """
        Indicating tutorial paused by other movie
        @return:
        """
        return self.__isTutorialPaused

    def showTutorial(self, onInitializedCallback = None):
        """
        Enables UI tutorial mode
        @param onInitializedCallback: callback on initialized
        """
        if self.__initialized:
            return
        self.ui.showTutorial()
        self.__initializing = True
        self.__onInitializedCallback = onInitializedCallback

    def hideTutorial(self):
        """
        Disables UI tutorial mode
        """
        self.ui.hideTutorial()
        self.__initializing = False
        self.__initialized = False
        del self.__actionsQueue[:]

    def showTutorialResult(self, onInitializedCallback = None):
        """
        Shows Tutorial Result window
        @param onInitializedCallback: callback on initialized
        """
        self.ui.showTutorialResult()
        self.__cbTRInitialized = onInitializedCallback

    def restoreScreenState(self):
        """
        Restores cached hud components states
        """
        self.clearScreen()
        if self.__screenCache.headerParams is not None:
            self.__lastHeaderParams = self.__screenCache.headerParams
            self.ui.showHeaderTutorial(self.__screenCache.headerParams)
        if self.__screenCache.hintParams is not None:
            self.__lastHintParams = self.__screenCache.hintParams
            self.ui.showHintTutorial(self.__screenCache.hintParams)
        if self.__screenCache.isTimerVisible:
            self.setTimerVisible(self.__screenCache.isTimerVisible)
        return

    def cacheScreenState(self):
        """
        Saves current hud components states
        """
        self.__screenCache.headerParams = self.__lastHeaderParams
        self.__screenCache.hintParams = self.__lastHintParams
        self.__screenCache.isTimerVisible = self.__isTimerVisible

    def clearScreen(self, clearScreenCache = False):
        """
        Hide all tutorial UI elements
        @param clearScreenCache:
        """
        if clearScreenCache:
            self.__screenCache.clear()
        self.__lastHeaderParams = None
        self.__lastHintParams = None
        self.__isTimerVisible = False
        self.ui.clearTutorial()
        self.__callbacks.clear()
        return

    def showHint(self, text, fadeoutTime = None, pictures = None, commandId = None, additionalText = None):
        """
        @param text:
        @param fadeoutTime:
        @param pictures:
        @param commandId:
        @param additionalText: additional hint text, that will be shown under main text
        """
        if self.__initializing:
            self.__actionsQueue.append(lambda : self.showHint(text, fadeoutTime, pictures, commandId, additionalText))
            return
        else:
            tutorialHintParams = TutorialHintParams(localizeTutorial(text), fadeoutTime, pictures)
            if additionalText:
                tutorialHintParams.message1 = localizeTutorial(additionalText)
            tutorialHintParams.buttons = InputMapping.g_instance.getLocalizedCommandKeysAndAxes(commandId) if commandId is not None else None
            tutorialHintParams.commandId = commandId
            self.__lastHintParams = tutorialHintParams
            self.ui.showHintTutorial(self.__lastHintParams)
            return

    def showHeader(self, title, message, message2 = '', commandId = None, image = None):
        """
        Show caption
        @param title: title
        @param message: text
        @param message2:
        @param commandId:
        @param image:
        """
        if self.__initializing:
            self.__actionsQueue.append(lambda : self.showHeader(title, message, message2, commandId, image))
            return
        else:
            self.__lastHeaderParams = TutorialHeaderParams(localizeTutorial(title), localizeTutorial(message), localizeTutorial(message2) if message2 else '', InputMapping.g_instance.getLocalizedCommandKeysAndAxes(commandId) if commandId is not None else None, image)
            self.ui.showHeaderTutorial(self.__lastHeaderParams)
            return

    def showCaption(self, tutorialCaptionParams, action1BtnCallback = None, action2BtnCallback = None, action3BtnCallback = None, localize = True):
        """
        Show caption UI element.
        @param tutorialCaptionParams: caption init params. Btn ids will be assigned by this method.
        @type tutorialCaptionParams: TutorialCaptionParams
        @param action1BtnCallback: delegate on action btn pressed
        @type action1BtnCallback: delegate()
        @param action2BtnCallback: delegate on action btn pressed
        @type action2BtnCallback: delegate()
        @param action3BtnCallback: delegate on action btn pressed
        @type action3BtnCallback: delegate()
        @param localize:
        """
        if self.__initializing:
            self.__actionsQueue.append(lambda : self.showCaption(tutorialCaptionParams, action1BtnCallback, action2BtnCallback, action3BtnCallback, localize))
            return
        else:
            if action1BtnCallback and tutorialCaptionParams.isAction1:
                self.__callbacks[self.__callbacksCounter] = action1BtnCallback
                tutorialCaptionParams.action1ButtonID = self.__callbacksCounter
                self.__callbacksCounter += 1
            if action2BtnCallback and tutorialCaptionParams.isAction2:
                self.__callbacks[self.__callbacksCounter] = action2BtnCallback
                tutorialCaptionParams.action2ButtonID = self.__callbacksCounter
                self.__callbacksCounter += 1
            if action3BtnCallback and tutorialCaptionParams.isAction3:
                self.__callbacks[self.__callbacksCounter] = action3BtnCallback
                tutorialCaptionParams.action3ButtonID = self.__callbacksCounter
                self.__callbacksCounter += 1
            if localize:
                tutorialCaptionParams.message = localizeTutorial(tutorialCaptionParams.message)
                tutorialCaptionParams.title = localizeTutorial(tutorialCaptionParams.title)
                if tutorialCaptionParams.nameAction1:
                    tutorialCaptionParams.nameAction1 = localizeTutorial(tutorialCaptionParams.nameAction1)
                if tutorialCaptionParams.nameAction2:
                    tutorialCaptionParams.nameAction2 = localizeTutorial(tutorialCaptionParams.nameAction2)
                if tutorialCaptionParams.nameAction3:
                    tutorialCaptionParams.nameAction3 = localizeTutorial(tutorialCaptionParams.nameAction3)
                if tutorialCaptionParams.nameCredits:
                    tutorialCaptionParams.nameCredits = localizeTutorial(tutorialCaptionParams.nameCredits)
                if tutorialCaptionParams.nameExperience:
                    tutorialCaptionParams.nameExperience = localizeTutorial(tutorialCaptionParams.nameExperience)
                if tutorialCaptionParams.nameReward:
                    tutorialCaptionParams.nameReward = localizeTutorial(tutorialCaptionParams.nameReward)
                if tutorialCaptionParams.nameGolds:
                    tutorialCaptionParams.nameGolds = localizeTutorial(tutorialCaptionParams.nameGolds)
            if tutorialCaptionParams.countCredits is None or tutorialCaptionParams.countCredits <= 0:
                tutorialCaptionParams.countCredits = ''
                tutorialCaptionParams.nameCredits = ''
            if tutorialCaptionParams.countExperience is None or tutorialCaptionParams.countExperience <= 0:
                tutorialCaptionParams.countExperience = ''
                tutorialCaptionParams.nameExperience = ''
            if tutorialCaptionParams.countGolds is None or tutorialCaptionParams.countGolds <= 0:
                tutorialCaptionParams.countGolds = ''
                tutorialCaptionParams.nameGolds = ''
            self.ui.showCaptionTutorial(tutorialCaptionParams)
            return

    def setTimerVisible(self, isVisible):
        """
        @param isVisible:
        """
        self.__isTimerVisible = isVisible
        self.ui.setTimerVisible(isVisible)

    def setTimerRunning(self, isRunning):
        """
        @param isRunning:
        """
        if isRunning:
            self.ui.startTimer()
        else:
            self.ui.stopTimer()

    def resetTimer(self):
        """
        Resets timer
        """
        self.ui.resetTimer()

    def getTimer(self, callback = None):
        """
        Returns time lapse since timer was started
        @param callback: result callback
        @type callback: delegate(timeLapsSeconds)
        """
        self.__onGetTimerCallback = callback
        self.ui.getTimer()

    def showLimitArea(self, visible, width, height, emptyAreaWidth = None):
        """
        Show limit area
        @param visible:
        @param width:
        @param height:
        @param emptyAreaWidth:
        """
        if emptyAreaWidth:
            self.__isLimitAreaVisibleEx = visible
            self.ui.showLimitAreaEx(visible, width, height, emptyAreaWidth)
        else:
            self.__isLimitAreaVisible = visible
            self.ui.showLimitArea(visible, width, height)

    def updateLimitAreaRotation(self, rotationAngle):
        """
        Update limit area rotation on screen
        @param rotationAngle: rotation
        """
        if self.__isLimitAreaVisibleEx:
            self.ui.rotateLimitAreaEx(rotationAngle)
        if self.__isLimitAreaVisible:
            self.ui.rotateLimitArea(rotationAngle)

    def destroy(self):
        """
        Destructor
        """
        self.__callbacks.clear()
        self.__callbacks = None
        self.ui.onGetTimer -= self.__onGetTimer
        self.ui.onTutorialPaused -= self.__onTutorialPaused
        self.ui.onTutorialResultInitialized -= self.onTRInitialized
        self.ui.onTutorialResultClose -= self.onTRClose
        self.ui.onTutorialResultContinue -= self.onTRContinue
        self.ui.onTutorialResultReject -= self.onTRReject
        self.ui.onTutorialResultRestart -= self.onTRRestart
        self.ui.onWarningChanged -= self.onWarningChanged
        self.setTRCallbacks(None, None, None, None)
        self.__cbWarningChanged = None
        self.ui = None
        self.__screenCache = None
        InputMapping.g_instance.onSaveControls -= self.__onInputControlsSave
        return

    def __onBtnPressed(self, btnId):
        callback = self.__callbacks.get(btnId, None)
        if callback:
            callback()
        return

    @property
    def initialized(self):
        return self.__initialized

    def __onTutorialInitialized(self):
        self.__initializing = False
        self.__initialized = True
        for delegate in self.__actionsQueue:
            delegate()

        del self.__actionsQueue[:]
        if self.__onInitializedCallback is not None:
            self.__onInitializedCallback()
            self.__onInitializedCallback = None
        return

    def __onTutorialPaused(self, paused):
        self.__isTutorialPaused = paused

    def __onGetTimer(self, timeLapse):
        if self.__onGetTimerCallback is not None:
            self.__onGetTimerCallback(timeLapse)
            self.__onGetTimerCallback = None
        return

    def __onInputControlsSave(self):
        if self.__lastHintParams is not None and self.__lastHintParams.commandId is not None:
            self.__lastHintParams.buttons = InputMapping.g_instance.getLocalizedCommandKeysAndAxes(self.__lastHintParams.commandId)
            self.ui.showHintTutorial(self.__lastHintParams)
        if self.__screenCache.hintParams is not None and self.__screenCache.hintParams.commandId is not None:
            self.__screenCache.hintParams.buttons = InputMapping.g_instance.getLocalizedCommandKeysAndAxes(self.__screenCache.hintParams.commandId)
        return

    def onTRInitialized(self):
        if self.__cbTRInitialized is not None:
            self.__cbTRInitialized()
            self.__cbTRInitialized = None
        return

    def onTRClose(self, lessonIndex):
        if self.__cbTRClose is not None:
            self.__cbTRClose()
        return

    def onTRContinue(self, lessonIndex):
        if self.__cbTRContinue is not None:
            self.__cbTRContinue()
        return

    def onTRReject(self):
        if self.__cbTRReject is not None:
            self.__cbTRReject()
        return

    def onTRRestart(self, lessonIndex):
        if self.__cbTRRestart is not None:
            self.__cbTRRestart()
        return

    def setTRCallbacks(self, cbClose, cbContinue, cbReject, cbRestart):
        self.__cbTRClose = cbClose
        self.__cbTRContinue = cbContinue
        self.__cbTRReject = cbReject
        self.__cbTRRestart = cbRestart

    def onWarningChanged(self, warning, active):
        if self.__cbWarningChanged is not None:
            self.__cbWarningChanged(warning, active)
        return

    def setWarningCallback(self, callback):
        self.__cbWarningChanged = callback


class MouseLimitArea(object):

    def __init__(self, ui, avatar, width, height, offsetX, offsetY, lockOnHorizon):
        """
        @type ui: gui.Scaleform.UI.UI
        @param avatar:
        @param width:
        @param height:
        @param offsetX:
        @param: offsetY:
        """
        self.__ui = ui
        self.__avatar = avatar
        self.__width = width
        self.__height = height
        self.__offsetX = offsetX
        self.__offsetY = offsetY
        self.__angle = 0
        self.update = lockOnHorizon and self.__updateRotation or self.__updateMovement
        self.setVisible(True)

    def __updateRotation(self):
        self.__angle = math.degrees(self.__avatar.roll)
        self.__ui.rotLimitAreaCircle(self.__angle)

    def __updateMovement(self):
        pass

    def setVisible(self, isVisible):
        """
        Hide/show limit area
        @param isVisible:
        """
        self.__ui.showLimitAreaCircle(isVisible, self.__offsetX, self.__offsetY, self.__width, self.__height, self.__angle)

    def destroy(self):
        self.__ui.showLimitAreaCircle(False, 0, 0, 0, 0, 0)
        self.__avatar = None
        self.__ui = None
        return