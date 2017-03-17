# Embedded file name: scripts/client/ScenarioClient/HangarVehicleCinematicHelper.py
__author__ = 'm_antipov'
import Math
import random
import BigWorld
from HangarScenarioController import HangarScenarioController
from debug_utils import LOG_ERROR, LOG_DEBUG
from functools import partial
from consts import CAMERAEFFECTS_PATH
HANGAR_CINEMATIC_OSCILLATION = 'HANGAR_CINEMATIC_OSCILLATION'

class HangarVehicleCinematicHelper:
    CAMERA_RETURN_TIME = 2.0

    def __init__(self, clientHangarSpace, scenarioData, excludeEvents):
        self.__scenarioController = HangarScenarioController(scenarioData)
        self.__space = clientHangarSpace
        self.__savedInterpolationDuration = 0.0
        self.__startTimeLineName = None
        self.__startTimeLineDuration = 0.0
        self.__stopTimeLineName = None
        self.__stopTimeLineDuration = 0.0
        self.__intermediateTimeLinesDuration = 0.0
        self.__excludeEvents = excludeEvents
        self.__intermediateTimeLines = []
        self.__intermediateTimeLineIndex = 0
        self.__nextActionCB = None
        self.__nextTimeLineCB = None
        self.__returnToNormalTime = 0.0
        self.__cinematicInProgress = False
        self.__defaultViewYaw = 0.0
        self.__defaultViewPitch = 0.0
        self.__parseScenarioData(scenarioData)
        return

    def setDefaultView(self, pitch, yaw):
        self.__defaultViewYaw = yaw
        self.__defaultViewPitch = pitch

    def startCinematic(self):
        if self.__startTimeLineDuration > 0.0:
            if self.__cinematicInProgress:
                self.__onCinematicFinished()
            self.__savedInterpolationDuration = self.__space.hangarCamera.getInterpolationDuration()
            self.__space.hangarCamera.setInterpolationDuration(0.0)
            self.__shuffleTimelines()
            self.__intermediateTimeLineIndex = 0
            self.__space.hangarCamera.getAircraftCam().effectController.init(CAMERAEFFECTS_PATH, '', Math.Matrix(), {})
            self.__space.hangarCamera.getAircraftCam().effectController.startEffect(HANGAR_CINEMATIC_OSCILLATION, 1.0)
            self.__scenarioController.onEvent(self.__startTimeLineName, BigWorld.serverTime())
            self.__nextTimeLineCB = BigWorld.callback(self.__startTimeLineDuration, self.__playNexTimeLine)
            self.__cinematicInProgress = True
        else:
            LOG_ERROR('No hangar cinematic found!')

    def cancelCinematic(self):
        if self.__stopTimeLineDuration > 0.0:
            if self.__nextTimeLineCB:
                BigWorld.cancelCallback(self.__nextTimeLineCB)
                self.__nextTimeLineCB = None
            if self.__cinematicInProgress:
                from CameraStates import CameraState
                self.__space.hangarCamera.leaveState(CameraState.SpectatorSide)
                self.__scenarioController.onEvent(self.__stopTimeLineName, BigWorld.serverTime())
                self.__nextTimeLineCB = BigWorld.callback(self.__stopTimeLineDuration, self.__onCinematicFinished)
        else:
            self.stopCinematic()
        return

    def stopCinematic(self):
        self.__space.hangarCamera.getAircraftCam().effectController.stopEffect(HANGAR_CINEMATIC_OSCILLATION)
        self.__scenarioController.forceStop()
        if self.__cinematicInProgress:
            self.__onCinematicFinished()

    def __parseScenarioData(self, data):
        numTimelines = len(data.timeline)
        timeline = []
        for tl in data.timeline:
            if tl.startEvent not in self.__excludeEvents:
                timeline.append(tl)

        if numTimelines > 0:
            self.__startTimeLineName = timeline[0].startEvent
            if hasattr(timeline[0], 'duration'):
                self.__startTimeLineDuration = timeline[0].duration
            else:
                LOG_ERROR('Wrong scenario data!')
            if numTimelines > 1:
                self.__stopTimeLineName = timeline[-1].startEvent
                if hasattr(timeline[-1], 'duration'):
                    self.__stopTimeLineDuration = timeline[-1].duration
                else:
                    LOG_ERROR('Wrong scenario data!')
        for i in range(1, numTimelines - 1):
            tl = timeline[i]
            if hasattr(tl, 'duration'):
                self.__intermediateTimeLinesDuration += tl.duration
            else:
                LOG_ERROR('Wrong scenario data!')
            duration = 0.0
            if hasattr(tl, 'duration'):
                duration = tl.duration
            else:
                LOG_ERROR('Wrong scenario data!')
            self.__intermediateTimeLines.append((str(tl.startEvent), duration))

    def __shuffleTimelines(self):
        random.shuffle(self.__intermediateTimeLines)

    def __playNexTimeLine(self):
        numTimelines = len(self.__intermediateTimeLines)
        if self.__intermediateTimeLineIndex < numTimelines:
            eventName, duration = self.__intermediateTimeLines[self.__intermediateTimeLineIndex]
            self.__scenarioController.onEvent(eventName, BigWorld.serverTime())
            self.__intermediateTimeLineIndex += 1
            self.__nextTimeLineCB = BigWorld.callback(duration, self.__playNexTimeLine)
        elif self.__stopTimeLineDuration > 0.0:
            self.__scenarioController.onEvent(self.__stopTimeLineName, BigWorld.serverTime())
            self.__nextTimeLineCB = BigWorld.callback(self.__stopTimeLineDuration, self.__onCinematicFinished)
        else:
            self.__onCinematicFinished()

    def __interpolationFinishedCallback(self, strategy, interpolationDuration):
        strategy.interpolationEndCallback = None
        self.__space.hangarCamera.setInterpolationDuration(interpolationDuration)
        return

    def __onCinematicFinished(self):
        from CameraStates import CameraState
        self.__space.hangarCamera.setInterpolationDuration(self.__class__.CAMERA_RETURN_TIME)
        self.__space.hangarCamera.leaveState(CameraState.SpectatorSide)
        BigWorld.dcursor().pitch = self.__defaultViewPitch
        BigWorld.dcursor().yaw = self.__defaultViewYaw
        BigWorld.dcursor().roll = 0.0
        if self.__space.hangarCamera.getStateObject():
            strategy = self.__space.hangarCamera.getStateObject().strategy
            strategy.interpolationEndCallback = partial(self.__interpolationFinishedCallback, strategy, self.__savedInterpolationDuration)
        if self.__nextTimeLineCB:
            BigWorld.cancelCallback(self.__nextTimeLineCB)
            self.__nextTimeLineCB = None
        self.__space.hangarCamera.getAircraftCam().effectController.clear()
        self.__cinematicInProgress = False
        return

    def destroy(self):
        self.stopCinematic()
        self.__space = None
        self.__intermediateTimeLines = None
        self.__scenarioController.destroy()
        self.__scenarioController = None
        return