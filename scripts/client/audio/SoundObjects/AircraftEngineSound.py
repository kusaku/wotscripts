# Embedded file name: scripts/client/audio/SoundObjects/AircraftEngineSound.py
from WwiseGameObject import WwiseGameObject, GS, WwiseGameObjectFactory
import BigWorld
import math
from consts import WEP_ENABLE_TEMPERATURE, ENGINE_WORK_INTERVAL, WEP_DISABLE_TEMPERATURE
import GameEnvironment
import Settings
from EntityHelpers import EntityStates
from CameraStates import CameraState
import db.DBLogic
from audio.AKTunes import RTPC_Altitude_Update_Interval, RTPC_ListenerAngle_Update_Interval, RTPC_Zoomstate_MAX, RTPC_Aircraft_Camera_Zoomstate_VDT, RTPC_Aircraft_Engine_RPM_VDT, RTPC_Aircraft_Engine_RPM_MAX, RTPC_Aircraft_Engine_Boost_VDT, RTPC_ListenerAngle_VDT, RTPC_AircraftPitch_VDT, RTPC_AircraftRoll_VDT, FREECAM_DIST_STEP
from audio.AKConsts import OVERHEAT_STARTED, OVERHEAT_MID, OVERHEAT_COOLDOWN, PartState, SOUND_MODES, CURRENT_PLAYER_MODE, SOUND_CASES
from audio.DopplerEffect import DopplerEffect
from audio.SoundModes import SoundModeStrategyBase, SoundModeHandler
from audio.SoundObjectSettings import SoundObjectSettings
from audio.SoundBanksManager import SoundBanksManager

class AircraftEngineSound(WwiseGameObject):
    NPC_DESTROYED_EVENT = 'Play_NPC_engine_destroyed'
    PLAYER_DESTROYED_EVENT = 'Play_engine_destroyed'
    AIRCRAFT_PLANE_TYPE_SWITCH = 'SWITCH_Aircraft_Plain_Type'

    def __init__(self, name, cid, node):
        WwiseGameObject.__init__(self, name, cid, node)

    def _onStateChanged(self, avatar, old, new):
        if old == new:
            return
        if new == EntityStates.DESTROYED:
            self.stopAll()
        if avatar.id == BigWorld.player().id:
            return
        if new == EntityStates.DESTROYED_FALL:
            self.postEvent(AircraftEngineSound.NPC_DESTROYED_EVENT)


class AircraftEngineStrategy(SoundModeStrategyBase):

    def __init__(self, avatarID, soundObject):
        self._soundSet = soundObject.soundSet
        self._isPlayer = BigWorld.player().id == avatarID
        self._alive = self._isPlayer
        self._altitudeCB = None
        self._anglesCB = None
        self._playingState = None
        self._avatarID = avatarID
        self._avatar = None
        SoundModeStrategyBase.__init__(self, avatarID, soundObject)
        self._altitudeCB = BigWorld.callback(RTPC_Altitude_Update_Interval, self.__RTPC_AltitudeCB)
        return

    def __RTPC_AltitudeCB(self):
        if not self._isPlayer and not self._alive:
            return
        entity = BigWorld.entities.get(self._avatarID)
        if not entity:
            return
        GS().updateSpeedAndAltitude(entity, self._isPlayer, self._soundObject.wwiseGameObject)
        if self._isPlayer:
            sfx = GS().fixedSoundObject(entity.id, 'sfx')
            if sfx:
                GS().updateSpeedAndAltitude(entity, True, sfx)
        self._altitudeCB = BigWorld.callback(RTPC_Altitude_Update_Interval, self.__RTPC_AltitudeCB)

    def _registerEventsBase(self):
        BigWorld.player().eLeaveWorldEvent += self.__onLeaveWorldBase
        BigWorld.player().onAvatarLeaveWorldEvent += self.__onAvatarLeaveWorldBase
        BigWorld.player().onAvatarEnterWorldEvent += self.onAvatarEnterWorld
        GS().eOnBattleEnd += self.stop
        self._registerEvents()

    def _registerEvents(self):
        pass

    def _clearEventsBase(self):
        BigWorld.player().eLeaveWorldEvent -= self.__onLeaveWorldBase
        BigWorld.player().onAvatarLeaveWorldEvent -= self.__onAvatarLeaveWorldBase
        GS().eOnBattleEnd -= self.stop
        self._clearEvents()

    def _clearEvents(self):
        pass

    def __onLeaveWorldBase(self):
        self._playingState = None
        self._clearCBBase()
        self._onLeaveWorld()
        return

    def _onLeaveWorld(self):
        pass

    def __onAvatarLeaveWorldBase(self, playerAvatar, avatarID):
        if avatarID == self._avatarID:
            if not self._alive:
                return
            self._alive = False
            self._onAvatarLeaveWorld()

    def _onAvatarLeaveWorld(self):
        pass

    def stop(self):
        self._soundObject.wwiseGameObject.stopAll(500)
        self._playingState = None
        self._clearCBBase()
        self._stop()
        return

    def _stop(self):
        pass

    def play(self, state = 'Main'):
        if not self._alive:
            return
        if self._playingState == state:
            return
        tag = self._getTag(state)
        if tag in self._soundSet:
            self._soundObject.wwiseGameObject.postEvent(self._soundSet[tag])
            self._playingState = state

    def _getTag(self, state):
        raise False or AssertionError('override getTag')

    def _clearCBBase(self):
        if self._altitudeCB:
            BigWorld.cancelCallback(self._altitudeCB)
            self._altitudeCB = None
        self._clearCB()
        return

    def _clearCB(self):
        pass

    def onAvatarEnterWorld(self, avatarID):
        if self._avatarID == avatarID:
            self._alive = True
            self.play()


class AircraftEngineStrategyPlayer(AircraftEngineStrategy):

    def __init__(self, avatarID, soundObject):
        AircraftEngineStrategy.__init__(self, avatarID, soundObject)
        self.__t0 = WEP_ENABLE_TEMPERATURE
        self.__boost = 0.0
        self.__damaged = False
        self.__ovhPlayingState = None
        self.__ovhMid = 0
        self.__sniperMode = False
        self.__RTPC_init()
        self._anglesCB = BigWorld.callback(RTPC_ListenerAngle_Update_Interval, self.__RTPC_AnglesCB)
        return

    def _createSoundObject(self):
        if not self._soundObject.wwiseGameObject:
            self._soundObject.wwiseGameObject = AircraftEngineSound('EngineSoundPlayer-{0}'.format(self._avatarID), self._cid, self._node)
            if BigWorld.player().clientIsReady:
                self.play()

    @property
    def soundModeID(self):
        return SOUND_MODES.PLAYER

    def _registerEvents(self):
        BigWorld.player().eUpdateForce += self.__onForce
        BigWorld.player().eUpdateEngineTemperature += self.__onEngine
        BigWorld.player().eEngineOverheat += self.__onEngineOverheat
        BigWorld.player().onStateChanged += self.__onPlayerStateChanged
        BigWorld.player().eUpdateSpectator += self.__onSpectator
        hud = GameEnvironment.getHUD()
        hud.ePartStateChanging += self.__onPartState
        cam = GameEnvironment.getCamera()
        cam.eZoomStateChanged += self.__onZoomStateChanged
        cam.eDistanceChanged += self.__onDistanceChanged
        cam.eSniperMode += self.__onSniperMode
        cam.eStateChanged += self.__onCamStateChanged
        GS().eLoadingScreenClosed += self.play

    def _clearEvents(self):
        BigWorld.player().eUpdateForce -= self.__onForce
        BigWorld.player().eUpdateEngineTemperature -= self.__onEngine
        BigWorld.player().eEngineOverheat -= self.__onEngineOverheat
        BigWorld.player().onStateChanged -= self.__onPlayerStateChanged
        BigWorld.player().eUpdateSpectator -= self.__onSpectator
        hud = GameEnvironment.getHUD()
        hud.ePartStateChanging -= self.__onPartState
        cam = GameEnvironment.getCamera()
        cam.eZoomStateChanged -= self.__onZoomStateChanged
        cam.eDistanceChanged -= self.__onDistanceChanged
        cam.eSniperMode -= self.__onSniperMode
        cam.eStateChanged -= self.__onCamStateChanged
        GS().eLoadingScreenClosed -= self.play

    def _onLeaveWorld(self):
        self.__ovhPlayingState = None
        self.__damaged = False
        return

    def _stop(self):
        self.__stopOverheat()
        self.__stopDamageFX()

    def _getTag(self, state):
        return '{0}{1}'.format('PlayerEngine', state)

    def __RTPC_AnglesCB(self):
        if not self._alive:
            return
        entity = BigWorld.player()
        if hasattr(entity.filter, 'vector') is False:
            self._anglesCB = BigWorld.callback(RTPC_ListenerAngle_Update_Interval, self.__RTPC_AnglesCB)
            return
        player = entity.filter.vector.getNormalized()
        camera = BigWorld.camera().direction.getNormalized()
        self._soundObject.wwiseGameObject.setRTPC('RTPC_Aircraft_Listener_Angle', 90 * (1 - camera.dot(player)), RTPC_ListenerAngle_VDT)
        self._soundObject.wwiseGameObject.setRtpcWithGlobal('RTPC_Aircraft_Nosedive_Angle', -math.degrees(entity.pitch), RTPC_AircraftPitch_VDT)
        self._soundObject.wwiseGameObject.setRtpcWithGlobal('RTPC_Aircraft_Body_Roll', math.fabs(math.degrees(entity.roll)), RTPC_AircraftRoll_VDT)
        self._anglesCB = BigWorld.callback(RTPC_ListenerAngle_Update_Interval, self.__RTPC_AnglesCB)

    def _clearCB(self):
        if self._isPlayer and self._anglesCB:
            BigWorld.cancelCallback(self._anglesCB)
            self._anglesCB = None
        return

    def __RTPC_init(self):
        self.__RTPC_Engine_RPM(0, 0)
        self.__RTPC_Engine_Boost_Fixed(False)
        cam = GameEnvironment.getCamera()
        self.__onZoomStateChanged(RTPC_Zoomstate_MAX if cam.isSniperMode else Settings.g_instance.camZoomIndex)

    def __RTPC_Engine_RPM(self, force, vdt = RTPC_Aircraft_Engine_RPM_VDT):
        if self.__damaged:
            return
        lowBoundF = 4.0 if force < 0 else 2.0
        rpm = (1.0 + force) * (RTPC_Aircraft_Engine_RPM_MAX / 4.0) + RTPC_Aircraft_Engine_RPM_MAX / lowBoundF
        self._soundObject.wwiseGameObject.setRTPC('RTPC_Aircraft_Engine_RPM', rpm, vdt)

    def __RTPC_Engine_Boost_Fixed(self, forsage):
        if self.__boost > 0.0 and forsage:
            return
        boost = 1.0 if forsage else 0.0
        tag = 'RtpcEngineBoost{0}'.format('Attack' if forsage else 'Release')
        fdt = float(self._soundSet.get(tag, -1.0))
        idt = int(1000.0 * fdt)
        self._soundObject.wwiseGameObject.setRtpcWithGlobal('RTPC_Aircraft_Engine_Boost', boost, idt if idt > 0 else RTPC_Aircraft_Engine_Boost_VDT)
        self.__boost = boost

    def __onZoomStateChanged(self, val):
        self.__RTPC_Zoomstate(RTPC_Zoomstate_MAX - val)

    def __RTPC_Zoomstate(self, val):
        self._soundObject.wwiseGameObject.setRtpcWithGlobal('RTPC_Aircraft_Camera_Zoomstate', min(max(0, val), RTPC_Zoomstate_MAX), RTPC_Aircraft_Camera_Zoomstate_VDT)

    def __onForce(self, F):
        if BigWorld.player().autopilot:
            return
        self.__RTPC_Engine_RPM(F)

    def __onEngineOverheat(self):
        self.__boost = 0
        self._soundObject.wwiseGameObject.setRtpcWithGlobal('RTPC_Aircraft_Engine_Boost', self.__boost, RTPC_Aircraft_Engine_Boost_VDT)
        if BigWorld.player().autopilot:
            return
        else:
            ev = self._soundSet.get('PlayerEngineOverheated', None)
            self._soundObject.wwiseGameObject.postEvent(str(ev).replace('_start', '_end'))
            self._soundObject.wwiseGameObject.postEvent(str(ev).replace('_start', '_oneshot'))
            self.__ovhPlayingState = OVERHEAT_COOLDOWN
            return

    def __onEngine(self, engineTemperature, wepWorkTime, isWarEmergencyPower):
        if BigWorld.player().autopilot:
            self.__stopOverheat()
        else:
            self.__overheatSound(engineTemperature, isWarEmergencyPower)
        self.__RTPC_Engine_Boost_Fixed(isWarEmergencyPower)

    def __stopOverheat(self):
        if not self._isPlayer or not self.__ovhPlayingState:
            return
        else:
            ev = self._soundSet.get('PlayerEngineOverheated', None)
            self._soundObject.wwiseGameObject.postEvent(str(ev).replace('_start', '_end'))
            self.__ovhPlayingState = None
            return

    def __overheatSound(self, engineTemperature, forsage):
        ev = self._soundSet.get('PlayerEngineOverheated', None)
        if not ev:
            return
        else:
            ovhStart = WEP_ENABLE_TEMPERATURE + ENGINE_WORK_INTERVAL * float(self._soundSet['OverheatRelativeStart'])
            if self.__ovhPlayingState:
                if engineTemperature < ovhStart:
                    self._soundObject.wwiseGameObject.postEvent(str(ev).replace('_start', '_end'))
                    self.__ovhPlayingState = None
                elif forsage:
                    self._soundObject.wwiseGameObject.postEvent(str(ev).replace('_start', '_oneshot'))
                return
            if not forsage:
                return
            if engineTemperature > ovhStart and not self.__ovhPlayingState:
                self._soundObject.wwiseGameObject.postEvent(ev)
                self.__ovhPlayingState = OVERHEAT_STARTED
                self.__ovhMid = ovhStart + (WEP_DISABLE_TEMPERATURE - engineTemperature) * 0.5
            elif self.__ovhPlayingState == OVERHEAT_STARTED and engineTemperature > self.__ovhMid:
                self._soundObject.wwiseGameObject.postEvent(str(ev).replace('_start', '_mid'))
                self.__ovhPlayingState = OVERHEAT_MID
            return

    def __onPlayerStateChanged(self, oldState, state):
        if state & EntityStates.DESTROYED_FALL:
            planeType = self._soundSet['PlainType']
            self._soundObject.wwiseGameObject.setSwitch(AircraftEngineSound.AIRCRAFT_PLANE_TYPE_SWITCH, planeType)
            self._soundObject.wwiseGameObject.postEvent(AircraftEngineSound.PLAYER_DESTROYED_EVENT)
            self.__stopDamageFX()
        elif state & EntityStates.DESTROYED:
            self._onDestroySoundObject()

    def _onDestroySoundObject(self):
        if self._soundObject and self._soundObject.wwiseGameObject:
            self._soundObject.wwiseGameObject.postEvent('Stop_avatar_destroy')
        self.__stopDamageFX()
        self._alive = False

    def __stopDamageFX(self):
        if not self.__damaged:
            return
        else:
            ev = self._soundSet['PlayerEngineDamaged']
            self._soundObject.wwiseGameObject.postEvent(str(ev).replace('Play_', 'Stop_'))
            if self._playingState == 'Damaged':
                self._playingState = None
            self.__damaged = False
            self.__RTPC_Engine_RPM(0.0)
            return

    def __onSpectator(self, target):
        if not self._alive:
            return
        self.__stopDamageFX()
        self._alive = False

    def __onPartState(self, name, stateID, position, entityID):
        if not self._alive:
            return
        if self._avatarID != entityID:
            return
        if name == 'Engine':
            if not self.__damaged and stateID in [PartState.Destructed]:
                self.play('Damaged')
                self.__damaged = True
                self._soundObject.wwiseGameObject.setRTPC('RTPC_Aircraft_Engine_RPM', 0.0, RTPC_Aircraft_Engine_RPM_VDT)
            elif self.__damaged and stateID in [PartState.Repaired,
             PartState.Normal,
             PartState.RepairedPartly,
             PartState.Damaged]:
                self.__stopDamageFX()

    def __onDistanceChanged(self, d):
        self.__RTPC_Zoomstate(math.floor(d / FREECAM_DIST_STEP))

    def __onSniperMode(self, sniper):
        if sniper:
            self.play('Cockpit')
        else:
            self.play()
        self.__sniperMode = sniper

    def __onCamStateChanged(self):
        cam = GameEnvironment.getCamera()
        if not cam:
            return
        state = cam.getState()
        combatStates = [CameraState.GamepadCombat, CameraState.JoystickCombat, CameraState.MouseCombat]
        if CameraState.Free == state:
            self.play()
        elif self.__sniperMode and state in combatStates:
            self.play('Cockpit')


class AircraftEngineStrategyAvatar(AircraftEngineStrategy):

    def __init__(self, avatarID, soundObject):
        AircraftEngineStrategy.__init__(self, avatarID, soundObject)
        self.onAvatarEnterWorld(avatarID)

    def _createSoundObject(self):
        if not self._soundObject.wwiseGameObject:
            self._soundObject.wwiseGameObject = AircraftEngineSound('EngineSoundNPC-{0}'.format(self._avatarID), self._cid, self._node)
            if not self._avatarID == BigWorld.player().id:
                DopplerEffect.instance().add(self._avatarID, self._soundObject.wwiseGameObject)

    @property
    def soundModeID(self):
        return SOUND_MODES.AVATAR

    def _getTag(self, state):
        return '{0}{1}'.format('NPCEngine', state)

    def _onDestroySoundObject(self):
        DopplerEffect.instance().discard(self._avatarID, self._soundObject.wwiseGameObject)


class AircraftEngineStrategySpectator(AircraftEngineStrategy):

    def __init__(self, avatarID, soundObject):
        AircraftEngineStrategy.__init__(self, avatarID, soundObject)
        self.onAvatarEnterWorld(avatarID)

    def _createSoundObject(self):
        if not self._soundObject.wwiseGameObject:
            self._soundObject.wwiseGameObject = AircraftEngineSound('EngineSoundSpectator-{0}'.format(self._avatarID), self._cid, self._node)
            self._soundObject.wwiseGameObject.setSwitch(SOUND_MODES.SWITCH, SOUND_MODES.WWISE[SOUND_MODES.SPECTATOR])

    @property
    def soundModeID(self):
        return SOUND_MODES.SPECTATOR

    def _getTag(self, state):
        return '{0}{1}'.format('NPCEngine', state)


g_factory = None

class AircraftEngineSoundFactory(WwiseGameObjectFactory):

    def __init__(self):
        self.__soundStrategies = {SOUND_MODES.PLAYER: AircraftEngineStrategyPlayer,
         SOUND_MODES.AVATAR: AircraftEngineStrategyAvatar,
         SOUND_MODES.SPECTATOR: AircraftEngineStrategySpectator}
        self.__soundBanksManager = SoundBanksManager.instance()

    def createPlayer(self, so):
        if not so.soundModeHandlerCreated:
            bank = so.soundSet['SoundBankPlayer']
            self.__soundBanksManager.loadBank(bank)
            self.__soundBanksManager.attachWwiseObjectToCase(bank, SOUND_CASES.ARENA)
            SoundModeHandler(BigWorld.player().id, so, self.__soundStrategies, CURRENT_PLAYER_MODE)

    def createAvatar(self, avatar, so):
        if not so.soundModeHandlerCreated:
            bank = so.soundSet['SoundBankNPC']
            self.__soundBanksManager.loadBank(bank)
            self.__soundBanksManager.attachWwiseObjectToCase(bank, SOUND_CASES.ARENA)
            SoundModeHandler(avatar.id, so, self.__soundStrategies, SOUND_MODES.AVATAR)

    @staticmethod
    def instance():
        global g_factory
        if not g_factory:
            g_factory = AircraftEngineSoundFactory()
        return g_factory

    @staticmethod
    def getSoundObjectSettings(data):
        modelManipulator = data['modelManipulator']
        partByNames = data['partByNames']
        objectBuilder = data['objectBuilder']
        isPlayer = data['isPlayer']
        soundObjects = data['soundObjects']
        context = data['context']
        info = data['info']
        so = SoundObjectSettings()
        pathList = modelManipulator.ModelManipulator3.ObjectDataReader._resolvePath(info.mointPoint, '', partByNames)
        so.node = objectBuilder.rootNode.resolvePath(modelManipulator.CompoundBuilder.convertPath(pathList))
        engineSet = db.DBLogic.g_instance.getAircraftEngineSet('Default')
        engineSet.update(db.DBLogic.g_instance.getAircraftEngineSet(info.engineSet))
        so.soundSet = GS().findLoadSet(engineSet, isPlayer, False, False, ['OverheatRelativeStart',
         'RtpcEngineBoostAttack',
         'RtpcEngineBoostRelease',
         'PlainType'])
        so.factory = AircraftEngineSoundFactory.instance()
        so.context = context
        soundObjects.append(so)