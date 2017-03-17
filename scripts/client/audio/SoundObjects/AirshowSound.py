# Embedded file name: scripts/client/audio/SoundObjects/AirshowSound.py
from WwiseGameObject import WwiseGameObject, WwiseGameObjectFactory
import db.DBLogic
import BigWorld
from audio.AKTunes import RTPC_Airshow_Update_Interval
from EntityHelpers import EntityStates
from SoundUtils import AirshowSoundCore
from audio.SoundObjectSettings import SoundObjectSettings
from audio.SoundModes import SoundModeStrategyBase, SoundModeHandler
from audio.AKConsts import SOUND_MODES, CURRENT_PLAYER_MODE
import audio.debug
g_airshowSoundCore = None

class AirshowSound(WwiseGameObject):
    PLAY_EVENT = 'Play_flyby_NPC'
    SWITCH_TIME = 'SWITCH_Aishow_Flyby_Time_Interval'
    SWITCH_TYPE = 'SWITCH_Aishow_Flyby_Type'

    def __init__(self, name, cid, node):
        WwiseGameObject.__init__(self, name, cid, node)


class AirshowSoundStrategy(SoundModeStrategyBase):

    def __init__(self, avatarID, soundObject):
        SoundModeStrategyBase.__init__(self, avatarID, soundObject)

    def _registerEventsBase(self):
        self._registerEvents()

    def _registerEvents(self):
        pass

    def _clearEventsBase(self):
        self._clearEvents()

    def _clearEvents(self):
        pass

    def _createSoundObject(self):
        pass

    def _clearCBBase(self):
        self._clearCB()

    def _clearCB(self):
        pass

    def _finishBase(self):
        self._finish()

    def _finish(self):
        pass

    def _onDestroySoundObject(self):
        audio.debug.LOG_AUDIO('%s %d' % ('AirshowSound; Destroyed; avatar.id', self._avatarID))


class AirshowSoundStrategyPlayer(AirshowSoundStrategy):
    pass


class AirshowSoundStrategyAvatar(AirshowSoundStrategy):

    def __init__(self, avatarID, soundObject):
        global g_airshowSoundCore
        self.__player = BigWorld.player()
        self.__avatarID = avatarID
        self.__airshowDB = db.DBLogic.g_instance.getAirshowParameters()
        self.__bottomOfExternalSphere = self.__airshowDB.externalSphereRadius * self.__airshowDB.externalSphereRange
        self.__topOfExternalSphere = self.__airshowDB.externalSphereRadius * (2 - self.__airshowDB.externalSphereRange)
        if not g_airshowSoundCore:
            g_airshowSoundCore = AirshowSoundCore(self.__airshowDB.minSpeed, self.__airshowDB.internalShpereRadius, self.__bottomOfExternalSphere, self.__topOfExternalSphere)
        self.__airshowSoundCore = g_airshowSoundCore
        AirshowSoundStrategy.__init__(self, avatarID, soundObject)
        self.__reset(BigWorld.entities.get(self._avatarID))
        self.__start()

    def _createSoundObject(self):
        if not self._soundObject.wwiseGameObject:
            self._soundObject.wwiseGameObject = AirshowSound('AirshowSound-{0}'.format(self._avatarID), self._cid, self._node)
            audio.debug.LOG_AUDIO('%s %d' % ('AirshowSound; Created; avatar.id', self._avatarID))

    def _registerEvents(self):
        self.__player.eLeaveWorldEvent += self.__onLeaveWorld
        self.__player.onAvatarEnterWorldEvent += self.__onAvatarEnterWorldEvent
        self.__player.onAvatarLeaveWorldEvent += self.__onAvatarLeaveWorldEvent
        self.__player.onStateChanged += self.__onPlayerStateChanged

    def _clearEvents(self):
        self.__player.eLeaveWorldEvent -= self.__onLeaveWorld
        self.__player.onAvatarEnterWorldEvent -= self.__onAvatarEnterWorldEvent
        self.__player.onAvatarLeaveWorldEvent -= self.__onAvatarLeaveWorldEvent
        self.__player.onStateChanged -= self.__onPlayerStateChanged

    def __reset(self, avatar):
        self.__avatar = avatar
        self.__cooldown = False
        self.__cooldownCB = None
        self.__updateCB = None
        self.__activated = False
        aircraftSound = db.DBLogic.g_instance.getAircraftSound(avatar.settings.airplane.name)
        self.__flybyType = db.DBLogic.g_instance.getAircraftEngineSet(aircraftSound.engineSet)['FlybyType']
        BigWorld.entities.get(self._avatarID).eOnAvatarStateChanged += self._onStateChanged
        return

    def __start(self):
        if not self.__activated and self.__avatar:
            self.__activated = True
            self.__updateCB = BigWorld.callback(RTPC_Airshow_Update_Interval, self.__update)

    def _clearCB(self):
        if self.__cooldownCB:
            BigWorld.cancelCallback(self.__cooldownCB)
            self.__cooldownCB = None
        if self.__updateCB:
            BigWorld.cancelCallback(self.__updateCB)
            self.__updateCB = None
        return

    def _finish(self):
        if self.__activated:
            self._clearCB()
            self.__activated = False

    def __update(self):
        self.__updateCB = BigWorld.callback(RTPC_Airshow_Update_Interval, self.__update)
        if self.__cooldown:
            return
        flyTime = self.__airshowSoundCore.getFlyTime(self.__player.position, self.__player.getWorldVector(), self.__avatar.position, self.__avatar.getWorldVector())
        if flyTime > 0:
            self.__airshowAction(self.__getClosestTimeInterval(flyTime))
            self.__cooldown = True
            self.__cooldownCB = BigWorld.callback(self.__airshowDB.cooldownTime, self.__onFinishAirshowAction)

    def __getClosestTimeInterval(self, time):
        intervals = self.__airshowDB.timeIntervals.keys()
        matches = [ abs(time - value) for value in intervals ]
        return self.__airshowDB.timeIntervals[intervals[matches.index(min(matches))]]

    def __onPlayerStateChanged(self, oldState, state):
        if state == EntityStates.DESTROYED_FALL or state == EntityStates.DESTROYED:
            self._finish()

    def _onStateChanged(self, avatar, oldState, state):
        if state == EntityStates.DESTROYED_FALL:
            self.__flybyType = 'Dead'

    def __onLeaveWorld(self):
        self._finish()
        self._clearEvents()

    def __onAvatarEnterWorldEvent(self, avatarID):
        if self.__avatarID == avatarID:
            self._finish()
            self.__reset(BigWorld.entities.get(avatarID))
            self.__start()

    def __onAvatarLeaveWorldEvent(self, playerAvatar, avatarID):
        if self.__avatarID == avatarID:
            self._finish()
            self.__avatar = None
        return

    def __airshowAction(self, time):
        self._soundObject.wwiseGameObject.setSwitch(AirshowSound.SWITCH_TYPE, self.__flybyType)
        self._soundObject.wwiseGameObject.setSwitch(AirshowSound.SWITCH_TIME, time)
        self.__play(AirshowSound.PLAY_EVENT)

    def __onFinishAirshowAction(self):
        self.__cooldown = False
        self.__cooldownCB = None
        return

    def __play(self, event):
        self._soundObject.wwiseGameObject.postEvent(event)


class AirshowSoundStrategySpectator(AirshowSoundStrategy):
    pass


g_factory = None

class AirshowSoundFactory(WwiseGameObjectFactory):

    def __init__(self):
        self.__soundStrategies = {SOUND_MODES.PLAYER: AirshowSoundStrategyPlayer,
         SOUND_MODES.AVATAR: AirshowSoundStrategyAvatar,
         SOUND_MODES.SPECTATOR: AirshowSoundStrategySpectator}

    def createAvatar(self, avatar, so):
        if not so.soundModeHandlerCreated and CURRENT_PLAYER_MODE == SOUND_MODES.PLAYER:
            SoundModeHandler(avatar.id, so, self.__soundStrategies, SOUND_MODES.AVATAR)

    @staticmethod
    def instance():
        global g_factory
        if not g_factory:
            g_factory = AirshowSoundFactory()
        return g_factory

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
        so.factory = AirshowSoundFactory.instance()
        so.context = context
        soundObjects.append(so)