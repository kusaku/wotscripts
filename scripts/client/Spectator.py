# Embedded file name: scripts/client/Spectator.py
import BigWorld
from MathExt import *
from consts import *
from StateMachine import *
from debug_utils import *
from Event import Event, EventManager
from clientConsts import SPECTATOR_MODE_SCENARIO
from EntityHelpers import EntityStates, isAvatar
import random
import InputMapping
from CameraStates import *

class SPECTATOR_MODE_STATES:
    OFF = -1
    INITIALIZED = 0
    OBSERVER = 1
    DYNAMIC_CAMERA = 2
    FILM = 3
    OUTRO = 4


class SpectatorModeDynamicCameraManager(object):

    def __init__(self):
        self.__index = 1

    def incStateIndex(self):
        self.__index += 1
        if self.__index == len(SPECTATOR_MODE_SCENARIO):
            self.__index = 0

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, newIndex):
        self.__index = newIndex

    def getSwitchStatesCommands(self):
        return {InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE0: 0,
         InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE1: 1,
         InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE2: 2,
         InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE3: 3,
         InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE4: 4,
         InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA_STATE5: 5}


class SpectatorModeManager(object):

    def __init__(self):
        self.__state = SPECTATOR_MODE_STATES.OFF
        self.eSetState = Event()

    def destroy(self):
        self.eSetState.clear()

    @property
    def state(self):
        return self.__state

    def setState(self, newState):
        if self.__state != newState:
            self.__state = newState
            self.eSetState(newState)

    def getSpectatorModeCommands(self):
        return [InputMapping.CMD_SPECTATOR_MODE_OBSERVER, InputMapping.CMD_SPECTATOR_MODE_DYNAMIC_CAMERA]


class SpectatorStateMachine(object):

    def __init__(self, camera):
        self.__states = {}
        self.__curState = None
        self.__defaultStateID = SpectatorState.OBSERVER
        self.addState(SpectatorStateObserver(camera))
        self.addState(SpectatorStateDynamic(camera))
        self.addState(SpectatorStateFilm(camera))
        return

    def updateTarget(self):
        if self.__curState:
            self.__curState.updateTarget()
        else:
            self.setState(self.__defaultStateID)

    def addState(self, stateObject):
        self.__states[stateObject.id] = stateObject

    def setState(self, stateID, params = {}):
        if stateID is not None:
            if stateID in self.__states:
                if self.__curState and stateID != self.__curState.id:
                    self.__curState.stop()
                self.__curState = self.__states[stateID]
                self.__curState.start(params)
                return True
            LOG_ERROR('Unknown state: ', stateID)
        return False

    def destroy(self):
        if self.__curState:
            self.__curState.stop()
            self.__curState = None
        for state in self.__states.itervalues():
            state.destroy()

        self.__states.clear()
        return


class SpectatorState(object):
    OBSERVER = 1
    DYNAMIC = 2
    FILM = 3

    def __init__(self, cameraManager):
        self._cameraManager = cameraManager
        self._id = None
        return

    def start(self, params):
        pass

    def stop(self):
        curState = self._cameraManager.getState()
        self._cameraManager.leaveState(curState)

    def destroy(self):
        pass

    def updateTarget(self):
        pass

    @property
    def id(self):
        return self._id


class ShuffleControllerBase(object):

    def __init__(self, shuffleIntervalMin, shuffleIntervalMax):
        self.__cbTimer = None
        self.__shuffleInterval = (shuffleIntervalMin, shuffleIntervalMax)
        return

    def shuffle(self):
        pass

    def update(self):
        interval = random.randint(self.__shuffleInterval[0], self.__shuffleInterval[1]) if self.__shuffleInterval[0] != self.__shuffleInterval[0] else self.__shuffleInterval[0]
        self.__cbTimer = BigWorld.callback(interval, self.update)

    def setShuffleInterval(self, minVal, maxVal):
        self.__shuffleInterval = (minVal, maxVal)

    def start(self):
        if not self.__cbTimer:
            interval = random.randint(self.__shuffleInterval[0], self.__shuffleInterval[1]) if self.__shuffleInterval[0] != self.__shuffleInterval[0] else self.__shuffleInterval[0]
            self.__cbTimer = BigWorld.callback(interval, self.update)
            return True
        else:
            LOG_ERROR('The timer is in progress!')
            return False

    def stop(self):
        if self.__cbTimer:
            BigWorld.cancelCallback(self.__cbTimer)
            self.__cbTimer = None
        return


class SpectatorStateDynamic(SpectatorState):
    SHUFFLE_INTERVAL = 5.0

    class ShuffleControllerDynamic(ShuffleControllerBase):

        def __init__(self, shuffleInterval):
            ShuffleControllerBase.__init__(self, shuffleInterval, shuffleInterval)
            self.__timelineSequence = [1,
             2,
             3,
             4,
             5]
            self.__curTimelineIdx = 0
            self.state = None
            return

        def __shuffle(self):
            import random
            random.shuffle(self.__timelineSequence)
            self.__curTimelineIdx = 0

        def __incTimeline(self):
            self.__curTimelineIdx += 1
            if self.__curTimelineIdx >= len(self.__timelineSequence):
                self.__shuffle()
            self.__updateStateTimeline()

        def __updateStateTimeline(self):
            if self.state:
                self.state.startTimeline(self.__timelineSequence[self.__curTimelineIdx])
            else:
                LOG_ERROR('No state attached!')

        def update(self):
            ShuffleControllerBase.update(self)
            self.__incTimeline()

        def start(self):
            if ShuffleControllerBase.start(self):
                self.__updateStateTimeline()
                return True
            else:
                return False

    def __init__(self, stateMachine):
        SpectatorState.__init__(self, stateMachine)
        self._id = SpectatorState.DYNAMIC
        self.__shuffleController = SpectatorStateDynamic.ShuffleControllerDynamic(self.__class__.SHUFFLE_INTERVAL)
        self.__shuffleController.state = self

    def start(self, params):
        timelineID = params['timelineID']
        if timelineID == 0:
            self.__shuffleController.start()
        else:
            self.__shuffleController.stop()
            self.startTimeline(timelineID)

    def startTimeline(self, timelineID):
        if timelineID < len(SPECTATOR_MODE_SCENARIO):
            cinematicStartTime = None
            if self._cameraManager.getState() == CameraState.SpectatorSide:
                cinematicStartTime = self._cameraManager.getStateObject().strategy.curTime
            player = BigWorld.player()
            player.controllers['scenarioCameraController'].onEvent(SPECTATOR_MODE_SCENARIO[timelineID], BigWorld.serverTime())
            if cinematicStartTime:
                curCamState = self._cameraManager.getStateObject()
                curCamStrategy = curCamState.strategy
                curCamState.setCinematicTime(cinematicStartTime % curCamStrategy.duration)
        else:
            LOG_ERROR('Invalid timeline ID: ', timelineID)
        return

    def stop(self):
        SpectatorState.stop(self)
        self.__shuffleController.stop()

    def destroy(self):
        self.__shuffleController = None
        return

    def updateTarget(self):
        self._cameraManager.getStateObject().updateTarget()


class SpectatorStateObserver(SpectatorState):

    def __init__(self, stateMachine):
        SpectatorState.__init__(self, stateMachine)
        self._id = SpectatorState.OBSERVER

    def start(self, params):
        currentTarget = self._cameraManager.context.entity
        newState = CameraState.Spectator
        if EntityStates.inState(currentTarget, EntityStates.DESTROYED_FALL):
            newState = CameraState.DestroyedFall
        elif EntityStates.inState(currentTarget, EntityStates.DESTROYED):
            newState = CameraState.DestroyedLanded
        self._cameraManager.setState(newState)

    def updateTarget(self):
        if self._cameraManager.getState() == CameraState.Spectator:
            self._cameraManager.getStateObject().updateTarget()
        else:
            self._cameraManager.setState(CameraState.Spectator)


class SpectatorStateFilm(SpectatorState):
    SHUFFLE_MAX_INTERVAL = 3.0
    SHUFFLE_MIN_INTERVAL = 7.0
    NEXT_TARGET_INTERVAL = 10.0

    class ShuffleControllerFilm(ShuffleControllerBase):

        def __init__(self, shuffleIntervalMin, shuffleIntervalMax):
            ShuffleControllerBase.__init__(self, shuffleIntervalMin, shuffleIntervalMax)
            self.__timelineSequence = [1,
             2,
             3,
             4,
             5]
            self.__curTimelineIdx = 0
            self.state = None
            self.entity = None
            return

        def __shuffle(self):
            import random
            random.shuffle(self.__timelineSequence)
            self.__curTimelineIdx = 0

        def __incTimeline(self):
            self.__curTimelineIdx += 1
            if self.__curTimelineIdx >= len(self.__timelineSequence):
                self.__shuffle()
            self.__updateStateTimeline()

        def __updateStateTimeline(self):
            if self.state:
                self.state.startTimeline(self.__timelineSequence[self.__curTimelineIdx])
            else:
                LOG_ERROR('No state attached!')

        def update(self):
            ShuffleControllerBase.update(self)
            self.__incTimeline()

        def start(self):
            if ShuffleControllerBase.start(self):
                self.__updateStateTimeline()
                return True
            else:
                return False

    def __init__(self, stateMachine):
        SpectatorState.__init__(self, stateMachine)
        self._id = SpectatorState.FILM
        self.__shuffleController = SpectatorStateFilm.ShuffleControllerFilm(self.__class__.SHUFFLE_MIN_INTERVAL, self.__class__.SHUFFLE_MAX_INTERVAL)
        self.__shuffleController.state = self
        self.__cbSelectTarget = None
        return

    def __selectNextTarget(self):
        friendlyVehicles = []
        for entity in BigWorld.entities.values():
            if isAvatar(entity) and entity.teamIndex == BigWorld.player().teamIndex and EntityStates.inState(entity, EntityStates.GAME):
                if 'modelManipulator' in entity.controllers:
                    if entity.controllers['modelManipulator'].isLoaded:
                        friendlyVehicles.append(entity.id)

        if len(friendlyVehicles) > 0:
            import random
            random.shuffle(friendlyVehicles)
            self.__shuffleController.stop()
            entity = BigWorld.entities.get(friendlyVehicles[0], None)
            if entity and not entity.isDestroyed:
                self.__shuffleController.entity = entity
                self.__shuffleController.start()
                BigWorld.player().switchToVehicle(friendlyVehicles[0])
                self.__cbSelectTarget = BigWorld.callback(self.__class__.NEXT_TARGET_INTERVAL, self.__selectNextTarget)
        return

    def start(self, params):
        timelineID = params['timelineID']
        if timelineID == 0:
            self.__shuffleController.start()
        else:
            self.__shuffleController.stop()
            self.startTimeline(timelineID)
        if not self.__cbSelectTarget:
            self.__selectNextTarget()
        else:
            LOG_ERROR('Target selection timer already started!!!')

    def startTimeline(self, timelineID):
        if timelineID < len(SPECTATOR_MODE_SCENARIO):
            cinematicStartTime = None
            if self._cameraManager.getState() == CameraState.SpectatorSide:
                cinematicStartTime = self._cameraManager.getStateObject().strategy.curTime
            player = BigWorld.player()
            player.controllers['scenarioCameraController'].onEvent(SPECTATOR_MODE_SCENARIO[timelineID], BigWorld.serverTime())
            if cinematicStartTime:
                curCamState = self._cameraManager.getStateObject()
                curCamStrategy = curCamState.strategy
                curCamState.setCinematicTime(cinematicStartTime % curCamStrategy.duration)
        else:
            LOG_ERROR('Invalid timeline ID: ', timelineID)
        return

    def stop(self):
        SpectatorState.stop(self)
        self.__shuffleController.stop()
        if self.__cbSelectTarget:
            BigWorld.cancelCallback(self.__cbSelectTarget)
        self.__cbSelectTarget = None
        return

    def destroy(self):
        self.__shuffleController = None
        return

    def updateTarget(self):
        self._cameraManager.getStateObject().updateTarget()