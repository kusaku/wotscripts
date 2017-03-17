# Embedded file name: scripts/client/audio/SoundModes.py
import BigWorld
from audio.AKConsts import SOUND_MODES
from EntityHelpers import EntityStates

class SoundModeHandler:

    def __init__(self, avatarID, soundObject, soundStrategies, soundModeID):
        soundObject.soundModeHandlerCreated = True
        self._avatarID = avatarID
        self._soundObject = soundObject
        self._soundStrategies = soundStrategies
        self._soundModeID = soundModeID
        self._isPlayer = BigWorld.player().id == self._avatarID
        self.__strategy = None
        self.__setStrategy(self._soundModeID)
        self.__registerEvents()
        return

    def __registerEvents(self):
        player = BigWorld.player()
        player.eRespawn += self.__onRespawn
        player.eUpdateSpectator += self.__onSpectator
        player.eLeaveWorldEvent += self.__onPlayerLeaveWorld
        player.onAvatarEnterWorldEvent += self.__onAvatarEnterWorldEvent
        player.onStateChanged += self.__playerStateChanged

    def _createSoundStrategy(self, soundModeID):
        return self._soundStrategies[soundModeID](self._avatarID, self._soundObject)

    def __onRespawn(self):
        if BigWorld.player().state != EntityStates.WAIT_START:
            return
        if self._isPlayer:
            self.__setStrategy(self._soundModeID)

    def __onSpectator(self, avatarID):
        if not self.__strategy:
            return
        else:
            if self._isPlayer:
                self.__setStrategy(None)
            elif self.__strategy.soundModeID == SOUND_MODES.SPECTATOR and not self._isPlayer:
                self.__setStrategy(SOUND_MODES.AVATAR)
            elif self.__strategy.soundModeID == SOUND_MODES.AVATAR and self._avatarID == avatarID:
                self.__setStrategy(SOUND_MODES.SPECTATOR)
            return

    def __onAvatarEnterWorldEvent(self, avatarID):
        if self._avatarID == avatarID:
            BigWorld.entities.get(self._avatarID).eOnAvatarStateChanged += self.__onAvatarStateChangedBase

    def __onAvatarStateChangedBase(self, avatarID, oldState, newState):
        if oldState != newState and newState == EntityStates.DESTROYED:
            self.__onAvatarDestroy()

    def __playerStateChanged(self, oldState, newState):
        if self._isPlayer and oldState != newState and newState == EntityStates.DESTROYED:
            self.__onAvatarDestroy()

    def __setStrategy(self, soundModeID):
        if self.__strategy:
            self.__strategy.finish()
        if soundModeID is not None:
            self.__strategy = self._createSoundStrategy(soundModeID)
        else:
            self.__strategy = None
        return

    def __onAvatarDestroy(self):
        self.__setStrategy(None)
        return

    def __onPlayerLeaveWorld(self):
        self._soundObject = None
        self._soundStrategies = None
        self.__strategy = None
        return


class SoundModeStrategyBase:

    def __init__(self, avatarID, soundObject):
        self._avatarID = avatarID
        self._soundObject = soundObject
        self._cid = soundObject.context.cidProxy.handle
        self._node = soundObject.node.id
        self._isPlayerLeaveWorld = False
        self._createSoundObject()
        self._registerEventsBase()
        BigWorld.player().eLeaveWorldEvent += self.__onPlayerLeaveWorld

    def _destroySoundObject(self):
        if self._soundObject.wwiseGameObject:
            self._soundObject.wwiseGameObject.stopAll(0, True)
            self._onDestroySoundObject()
            self._soundObject.wwiseGameObject = None
        return

    def _onDestroySoundObject(self):
        pass

    def __clear(self):
        self._soundObject = None
        self._cid = None
        self._node = None
        return

    def finish(self):
        if self._soundObject:
            self._clearEventsBase()
            self._clearCBBase()
            self._destroySoundObject()
            self._finishBase()
            self.__clear()

    def _finishBase(self):
        pass

    def _registerEventsBase(self):
        pass

    def _clearEventsBase(self):
        pass

    def _createSoundObject(self):
        pass

    def _clearCBBase(self):
        pass

    def __onPlayerLeaveWorld(self):
        self._isPlayerLeaveWorld = True
        self.finish()

    @property
    def soundModeID(self):
        return None