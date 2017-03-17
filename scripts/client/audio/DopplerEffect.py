# Embedded file name: scripts/client/audio/DopplerEffect.py
import BigWorld
from AKConsts import SPEED_OF_SOUND
from consts import WORLD_SCALING
from AKTunes import RTPC_DopplerEffect_Update_Interval
from EntityHelpers import EntityStates
from debug_utils import LOG_INFO
from audio.AKConsts import DEBUG_AUDIO_TAG
g_instance = None

class DopplerEffect:
    RTPC = 'RTPC_NPC_Doppler_Delta'
    DOPPLER_RANGE = 500 * WORLD_SCALING

    def __init__(self):
        self.__soundSpeed = SPEED_OF_SOUND * WORLD_SCALING * WORLD_SCALING
        self.__entities = {}
        self.__listener = None
        self.__listenerID = None
        self.__updateCB = None
        player = BigWorld.player()
        player.eLeaveWorldEvent += self.__onPlayerLeaveWorld
        player.onStateChanged += self.__onPlayerStateChanged
        return

    def __onPlayerLeaveWorld(self):
        self.deactivate()
        self.__entities.clear()

    def __onPlayerStateChanged(self, oldState, state):
        if state == EntityStates.OUTRO:
            self.deactivate()

    def activate(self):
        self.__updateCB = BigWorld.callback(RTPC_DopplerEffect_Update_Interval, self.__update)
        LOG_INFO('%s %s' % (DEBUG_AUDIO_TAG, 'DopplerEffect; Activated'))

    def deactivate(self):
        if self.__updateCB:
            BigWorld.cancelCallback(self.__updateCB)
            self.__updateCB = None
            LOG_INFO('%s %s' % (DEBUG_AUDIO_TAG, 'DopplerEffect; Deactivated'))
        return

    def __getDopplerEffect(self, source):
        distance = self.__listener.position - source.position
        if not distance:
            return 0
        sourceSpeed = source.getWorldVector()
        speed = sourceSpeed - self.__listener.getWorldVector()
        relativeSpeed = distance.dot(speed) / distance.length
        return relativeSpeed / self.__soundSpeed

    def __isInRange(self, source):
        return self.__listener.position.distTo(source.position) < DopplerEffect.DOPPLER_RANGE

    def add(self, entity, wwiseSoundObject):
        if entity not in self.__entities:
            self.__entities[entity] = set()
        self.__entities[entity].add(wwiseSoundObject)
        LOG_INFO('%s %s %d' % (DEBUG_AUDIO_TAG, 'DopplerEffect; Add Entity ', entity))

    def discard(self, entityID, wwiseSoundObject):
        if entityID in self.__entities and self.__entities[entityID]:
            self.__entities[entityID].discard(wwiseSoundObject)
            LOG_INFO('%s %s %d' % (DEBUG_AUDIO_TAG, 'DopplerEffect; Discard Entity ', entityID))

    def removeEntity(self, entityID):
        del self.__entities[entityID]

    def __update(self):
        self.__updateCB = BigWorld.callback(RTPC_DopplerEffect_Update_Interval, self.__update)
        self.__listener = BigWorld.entities.get(self.__listenerID, None)
        if not self.__listener or not self.__listener.inWorld:
            return
        else:
            for entityID in self.__entities:
                entity = BigWorld.entities.get(entityID)
                if not entity or not entity.inWorld or entityID == self.__listener.id or not self.__isInRange(entity):
                    continue
                dopplerEffect = self.__getDopplerEffect(entity)
                for soundObject in self.__entities[entityID]:
                    soundObject.setRTPC(DopplerEffect.RTPC, dopplerEffect)

            return

    def setListener(self, avatar):
        self.__listener = avatar
        self.__listenerID = avatar.id
        LOG_INFO('%s %s %d' % (DEBUG_AUDIO_TAG, 'DopplerEffect; Listener: ', avatar.id))

    @property
    def listener(self):
        return self.__listener

    @staticmethod
    def instance():
        global g_instance
        if not g_instance:
            g_instance = DopplerEffect()
        return g_instance