# Embedded file name: scripts/client/audio/SoundObjects/WindSound.py
from WwiseGameObject import WwiseGameObject, GS, WwiseGameObjectFactory
import db.DBLogic
import BigWorld
import GameEnvironment
from audio.AKTunes import RTPC_Wind_Update_Interval
from audio.AKConsts import SOUND_MODES, CURRENT_PLAYER_MODE
from audio.SoundModes import SoundModeStrategyBase, SoundModeHandler
from MathExt import clamp
import math
from CameraStates import CameraState
from audio.SoundObjectSettings import SoundObjectSettings
from EntityHelpers import EntityStates
import audio.debug

class WindSound(WwiseGameObject):
    EVENT_LOADING = {'START': 'Play_wind_loading_screen',
     'STOP': 'Stop_wind_loading_screen'}
    EVENT_PLAYER = {'START': 'Play_wind_gameplay_main',
     'STOP': 'Stop_wind_gameplay_main'}
    EVENT_SPECTATOR = {'START': 'Play_wind_spectator',
     'STOP': 'Stop_wind_spectator'}
    RTCP_CRITICAL_LANDSCAPE = 'RTPC_Wind_Critical_Landscape'
    RTCP_CRITICAL_MANEUVERS = 'RTPC_Wind_Critical_Maneuvers'
    RTCP_CRITICAL_CAMERA_SPEED = 'RTPC_Wind_Camera_Speed'

    def __init__(self, name, cid, node):
        WwiseGameObject.__init__(self, name, cid, node)


class WindSoundStrategy(SoundModeStrategyBase):
    __LOADING = True

    def __init__(self, avatarID, soundObject):
        self._windDB = db.DBLogic.g_instance.getWindParameters()
        self.__avatar = BigWorld.entities.get(avatarID)
        self.__avatarID = avatarID
        self.__avatarDiveSpeed = self.__avatar.settings.airplane.flightModel.hull[0].diveSpeed
        self.__avatarStallSpeed = self.__avatar.settings.airplane.flightModel.hull[0].stallSpeed
        self.__updateCB = None
        self.__spectatorMode = False
        self.__currentStopEvent = None
        self._isPlayer = self.__avatar.id == BigWorld.player().id
        self.__finished = None
        self._criticalEffectsList = [self.__updateCriticalLandscape, self.__updateCriticalManeuvers]
        SoundModeStrategyBase.__init__(self, avatarID, soundObject)
        if WindSoundStrategy.__LOADING:
            self._startLogic(WindSound.EVENT_LOADING, False)
            WindSoundStrategy.__LOADING = False
        else:
            self._generateStartEvent()
        return

    def _startLogic(self, event, inProcess = True):
        if self.__currentStopEvent:
            self._soundObject.wwiseGameObject.postEvent(self.__currentStopEvent)
        self._soundObject.wwiseGameObject.postEvent(event['START'])
        self.__currentStopEvent = event['STOP']
        self.__inProcess = inProcess
        self.__updateCB = BigWorld.callback(RTPC_Wind_Update_Interval, self.__updateAvatarParameters)

    def _destroySoundObject(self):
        if self.__currentStopEvent:
            self._soundObject.wwiseGameObject.postEvent(self.__currentStopEvent)
            self.__currentStopEvent = None
        elif self._soundObject.wwiseGameObject:
            self._soundObject.wwiseGameObject.stopAll(self._windDB.onDestroyFadeTime, True)
        self.__inProcess = False
        self._soundObject.wwiseGameObject = None
        self._onDestroySoundObject()
        return

    def __updateAvatarParameters(self):
        self.__avatar = BigWorld.entities.get(self.__avatarID, None)
        if not self.__inProcess or not self.__avatar or EntityStates.inState(self.__avatar, EntityStates.DESTROYED):
            return
        else:
            self.__updateWindAircraftSpeed()
            self.__updateListenerAngle()
            self.__updateCriticalEffects()
            self.__updateCB = BigWorld.callback(RTPC_Wind_Update_Interval, self.__updateAvatarParameters)
            return

    def __updateWindAircraftSpeed(self):
        self.__avatarSpeed = self.__avatar.getSpeed()
        param = (self.__avatarSpeed - self.__avatarStallSpeed) / (self.__avatarDiveSpeed - self.__avatarStallSpeed) * 100
        RTPC_Wind_Aircraft_Speed = clamp(0, param, 100)
        self._soundObject.wwiseGameObject.setRTPC('RTPC_Wind_Aircraft_Speed', RTPC_Wind_Aircraft_Speed)
        if audio.debug.IS_AUDIO_DEBUG:
            audio.debug.SHOW_DEBUG_OBJ('Wind_Aircraft_Speed', RTPC_Wind_Aircraft_Speed, group='WindSound')

    def __updateListenerAngle(self):
        avatar = self.__avatar.getWorldVector().getNormalized()
        camera = BigWorld.camera().direction.getNormalized()
        angle = 90 * (1 - camera.dot(avatar))
        self._soundObject.wwiseGameObject.setRTPC('RTPC_Aircraft_Listener_Angle', angle)
        if audio.debug.IS_AUDIO_DEBUG:
            audio.debug.SHOW_DEBUG_OBJ('Aircraft_Listener_Angle', angle, group='WindSound')

    def __updateCriticalEffects(self):
        criticalEffectsValues = {}
        for func in self._criticalEffectsList:
            func(criticalEffectsValues)

        for RTPC, value in criticalEffectsValues.iteritems():
            self._soundObject.wwiseGameObject.setRtpcWithGlobal(RTPC, value)
            if audio.debug.IS_AUDIO_DEBUG:
                audio.debug.SHOW_DEBUG_OBJ(str(RTPC).replace('RTPC_', ''), value, group='WindSound')

    def __updateCriticalLandscape(self, criticalEffectsValues):
        height = self.__avatar.getAltitudeAboveObstacle()
        top = self._windDB.altitudeTop
        bottom = self._windDB.altitudeBottom
        value = (1 - (height - bottom) / (top - bottom)) * 100
        criticalEffectsValues[WindSound.RTCP_CRITICAL_LANDSCAPE] = clamp(0, value, 100)

    def __updateCriticalManeuvers(self, criticalEffectsValues):
        avatarWorldVector = self.__avatar.getWorldVector()
        avatarAxisZ = self.__avatar.getRotation().getAxisZ()
        angle = math.degrees(avatarWorldVector.angle(avatarAxisZ))
        top = self._windDB.maneuversAngleTop
        bottom = self._windDB.maneuversAngleBottom
        value = (angle - bottom) / (top - bottom) * 100
        criticalEffectsValues[WindSound.RTCP_CRITICAL_MANEUVERS] = 0 if math.isnan(value) else clamp(0, value, 100)

    def _registerEventsBase(self):
        player = BigWorld.player()
        if WindSoundStrategy.__LOADING:
            GS().eOnBattleStart += self._generateStartEvent
        player.eLeaveWorldEvent += self.__onLeaveWorld

    def _clearEventsBase(self):
        player = BigWorld.player()
        GS().eOnBattleStart -= self._generateStartEvent
        player.eLeaveWorldEvent -= self.__onLeaveWorld

    def _generateStartEvent(self):
        pass

    def _finishBase(self):
        if not self.__finished:
            self.__finished = True
            self._clearEventsBase()
            self._clearCBBase()

    def __onLeaveWorld(self):
        WindSoundStrategy.__LOADING = True
        self._finishBase()

    def _clearCBBase(self):
        self._criticalEffectsList = None
        if self.__updateCB:
            BigWorld.cancelCallback(self.__updateCB)
            self.__updateCB = None
        return


class WindSoundStrategyPlayer(WindSoundStrategy):

    def __init__(self, avatarID, soundObject):
        self.__cameraInfo = {}
        self.__cameraInfo['camera'] = BigWorld.camera()
        self.__cameraInfo['cameraGE'] = GameEnvironment.getCamera()
        self.__cameraInfo['direction'] = self.__cameraInfo['camera'].direction
        self.__cameraInfo['ticksDelay'] = 2
        self.__cameraInfo['ticksCounter'] = 0
        WindSoundStrategy.__init__(self, avatarID, soundObject)
        self._criticalEffectsList.append(self.__updateCameraSpeed)

    def _onDestroySoundObject(self):
        self.__cameraInfo.clear()
        audio.debug.LOG_AUDIO('%s %s' % ('WindSound; Destroyed;', 'Player'))

    def _generateStartEvent(self):
        self._startLogic(WindSound.EVENT_PLAYER)

    def __updateCameraSpeed(self, criticalEffectsValues):
        criticalEffectsValues[WindSound.RTCP_CRITICAL_CAMERA_SPEED] = 0
        if GameEnvironment.getCamera().getState() != CameraState.Free:
            self.__cameraInfo['ticksCounter'] = 0
            return
        speed = math.degrees(self.__cameraInfo['direction'].angle(self.__cameraInfo['camera'].direction)) / RTPC_Wind_Update_Interval
        top = self._windDB.cameraSpeedTop
        bottom = self._windDB.cameraSpeedBottom
        if bottom < speed:
            self.__cameraInfo['ticksCounter'] += 1
        else:
            self.__cameraInfo['ticksCounter'] = 0
        if self.__cameraInfo['ticksDelay'] <= self.__cameraInfo['ticksCounter']:
            value = (speed - bottom) / (top - bottom) * 100
            criticalEffectsValues[WindSound.RTCP_CRITICAL_CAMERA_SPEED] = clamp(0, value, 100)
        self.__cameraInfo['direction'] = self.__cameraInfo['camera'].direction

    def _createSoundObject(self):
        if not self._soundObject.wwiseGameObject:
            self._soundObject.wwiseGameObject = WindSound('WindSoundPlayer', self._cid, self._node)
            audio.debug.LOG_AUDIO('%s %s' % ('WindSound; Created;', 'Player'))

    @property
    def soundModeID(self):
        return SOUND_MODES.PLAYER


class WindSoundStrategySpectator(WindSoundStrategy):

    def __init__(self, avatarID, soundObject):
        WindSoundStrategy.__init__(self, avatarID, soundObject)

    def _generateStartEvent(self):
        self._startLogic(WindSound.EVENT_SPECTATOR)

    def _createSoundObject(self):
        if not self._soundObject.wwiseGameObject:
            self._soundObject.wwiseGameObject = WindSound('WindSoundSpectator-{0}'.format(self._avatarID), self._cid, self._node)
            audio.debug.LOG_AUDIO('%s %d' % ('WindSound; Created; avatar.id', self._avatarID))

    def _onDestroySoundObject(self):
        audio.debug.LOG_AUDIO('%s %d' % ('WindSound; Destroyed; avatar.id', self._avatarID))

    @property
    def soundModeID(self):
        return SOUND_MODES.SPECTATOR


class WindSoundStrategyAvatar(SoundModeStrategyBase):

    @property
    def soundModeID(self):
        return SOUND_MODES.AVATAR


g_factory = None

class WindSoundFactory(WwiseGameObjectFactory):

    def __init__(self):
        self.__soundStrategies = {SOUND_MODES.PLAYER: WindSoundStrategyPlayer,
         SOUND_MODES.AVATAR: WindSoundStrategyAvatar,
         SOUND_MODES.SPECTATOR: WindSoundStrategySpectator}

    def createPlayer(self, so):
        if not so.soundModeHandlerCreated:
            SoundModeHandler(BigWorld.player().id, so, self.__soundStrategies, CURRENT_PLAYER_MODE)

    def createAvatar(self, avatar, so):
        if not so.soundModeHandlerCreated:
            arena = GameEnvironment.getClientArena()
            avatarInfo = arena.avatarInfos.get(avatar.id, {})
            isPlayerTeamate = arena.avatarInfos.get(BigWorld.player().id)['teamIndex'] == avatarInfo['teamIndex']
            if isPlayerTeamate:
                SoundModeHandler(avatar.id, so, self.__soundStrategies, SOUND_MODES.AVATAR)

    @staticmethod
    def getSoundObjectSettings(data):
        modelManipulator = data['modelManipulator']
        info = data['info']
        partByNames = data['partByNames']
        objectBuilder = data['objectBuilder']
        soundObjects = data['soundObjects']
        context = data['context']
        so = SoundObjectSettings()
        pathList = modelManipulator.ModelManipulator3.ObjectDataReader._resolvePath(info.mointPoint, '', partByNames)
        so.node = objectBuilder.rootNode.resolvePath(modelManipulator.CompoundBuilder.convertPath(pathList))
        so.factory = WindSoundFactory.instance()
        so.context = context
        soundObjects.append(so)

    @staticmethod
    def instance():
        global g_factory
        if not g_factory:
            g_factory = WindSoundFactory()
        return g_factory