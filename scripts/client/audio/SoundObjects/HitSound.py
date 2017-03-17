# Embedded file name: scripts/client/audio/SoundObjects/HitSound.py
from WwiseGameObject import WwiseGameObject, GS
import BigWorld
import math
from consts import DAMAGE_REASON
import GameEnvironment
import Settings
from audio.AKTunes import RTPC_Zoomstate_MAX, FREECAM_DIST_STEP, RTPC_Aircraft_Camera_Zoomstate_VDT

class HitSound(WwiseGameObject):
    AVATAR_LOGIC_HIT = 'Play_hit_LOGIC_Avatar'
    NPC_LOGIC_HIT = 'Play_hit_LOGIC_NPC'
    AVATAR_EFFECT_HIT = 'Play_hit_EFFECT_damage_Avatar'
    NPC_EFFECT_HIT = 'Play_hit_EFFECT_damage_Spectator'
    OTHER_DAMAGE = 'Play_hit_IMPACT_'

    def __init__(self, entityID, position, ev, dmgType = None):
        dmgRamming = [DAMAGE_REASON.RAMMING]
        self.__isPlayer = ev in ('Play_hit_LOGIC_Avatar', 'Play_hit_EFFECT_damage_Avatar')
        if dmgType == DAMAGE_REASON.TREES:
            ev = self.OTHER_DAMAGE + 'Threes'
        elif dmgType in dmgRamming:
            ev = self.OTHER_DAMAGE + 'Ram'
        ctx = node = 0
        if not position:
            engineSound = GS().enumSoundObjects(entityID, 'engine')
            if engineSound and len(engineSound) > 0:
                so = engineSound[0]
                ctx = so.context.cidProxy.handle
                node = so.node.id
        WwiseGameObject.__init__(self, 'HitSound-{0}'.format(ev), ctx, node, position)
        cam = GameEnvironment.getCamera()
        if self.__isPlayer and cam:
            cam.eZoomStateChanged += self.__onZoomStateChanged
            cam.eDistanceChanged += self.__onDistanceChanged
            self.__onZoomStateChanged(RTPC_Zoomstate_MAX if cam.isSniperMode else Settings.g_instance.camZoomIndex)
        if hasattr(BigWorld.player(), 'eLeaveWorldEvent'):
            BigWorld.player().eLeaveWorldEvent += self.__onLeaveWorld
        self.postEvent(ev, self.__onLeaveWorld)

    def __onZoomStateChanged(self, val):
        self.__RTPC_Zoomstate(RTPC_Zoomstate_MAX - val)

    def __onDistanceChanged(self, d):
        self.__RTPC_Zoomstate(math.floor(d / FREECAM_DIST_STEP))

    def __RTPC_Zoomstate(self, val):
        if self.destroyed:
            return
        else:
            value = min(max(0, val), RTPC_Zoomstate_MAX)
            state = 'Zoomstate_0{0}'.format(value) if value > 0 else None
            self.setRTPC('RTPC_Aircraft_Camera_Zoomstate', value, RTPC_Aircraft_Camera_Zoomstate_VDT)
            if state:
                self.setSwitch('SWITCH_Camera_Zoomstate', state)
            return

    @staticmethod
    def canPlayHit(entityID, health, oldHealth, damagerID, dmgType):
        isPlayer = entityID == BigWorld.player().id
        dmgRamming = [DAMAGE_REASON.RAMMING,
         DAMAGE_REASON.OBSTACLE,
         DAMAGE_REASON.TERRAIN,
         DAMAGE_REASON.WATER]
        dmgExplosion = [DAMAGE_REASON.FIRING, DAMAGE_REASON.ROCKET_EXPLOSION, DAMAGE_REASON.BOMB_EXPLOSION]
        if GS().isReplayMute:
            return False
        if not isPlayer and (damagerID != BigWorld.player().id or dmgType == DAMAGE_REASON.AA_EXPLOSION):
            return False

        def calculate(_health):
            if _health <= 0:
                return 0
            h = math.ceil(_health)
            if 1 >= h:
                return 1
            return h

        if health and calculate(health) >= oldHealth:
            return False
        if dmgType in dmgExplosion:
            return False
        if not isPlayer and (dmgType == DAMAGE_REASON.TREES or dmgType in dmgRamming):
            return False
        return True

    @staticmethod
    def canPlayEffect(name):
        entityID = None
        player = BigWorld.player()
        if name == HitSound.AVATAR_EFFECT_HIT:
            entityID = BigWorld.player().id
        else:
            entityID = player.curVehicleID
        return entityID and not GS().isBurning(entityID, 5.0)

    def __onLeaveWorld(self):
        cam = GameEnvironment.getCamera()
        if self.__isPlayer and cam:
            cam.eZoomStateChanged -= self.__onZoomStateChanged
            cam.eDistanceChanged -= self.__onDistanceChanged
        self.stopAll(500, True)