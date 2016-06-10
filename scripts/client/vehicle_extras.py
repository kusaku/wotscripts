# Embedded file name: scripts/client/vehicle_extras.py
import BigWorld
import Math
import random
from functools import partial
import weakref
from helpers.EffectsList import EffectsListPlayer
from AvatarInputHandler import ShakeReason
from debug_utils import LOG_CODEPOINT_WARNING, LOG_CURRENT_EXCEPTION
from helpers import i18n
from helpers.EntityExtra import EntityExtra
from items import vehicles
from operator import xor

def reload():
    modNames = (reload.__module__,)
    from sys import modules
    import __builtin__
    for m in modNames:
        __builtin__.reload(modules[m])

    print 'vehicle_extras reloaded'


class NoneExtra(EntityExtra):

    def _start(self, data, args):
        LOG_CODEPOINT_WARNING()
        self.stop(data)


class ShowShooting(EntityExtra):

    def _start(self, data, burstCount):
        vehicle = data['entity']
        gunDescr = vehicle.typeDescriptor.gun
        stages, effects, _ = gunDescr['effects']
        data['entity_id'] = vehicle.id
        data['_effectsListPlayer'] = EffectsListPlayer(effects, stages, **data)
        data['_burst'] = (burstCount, gunDescr['burst'][1])
        data['_gunModel'] = vehicle.appearance.compoundModel
        self.__doShot(data)

    def _cleanup(self, data):
        if data.get('_effectsListPlayer') is not None:
            data['_effectsListPlayer'].stop()
        timerID = data.get('_timerID')
        if timerID is not None:
            BigWorld.cancelCallback(timerID)
            data['_timerID'] = None
        return

    def __doShot(self, data):
        data['_timerID'] = None
        try:
            vehicle = data['entity']
            if not vehicle.isAlive():
                self.stop(data)
                return
            burstCount, burstInterval = data['_burst']
            gunModel = data['_gunModel']
            effPlayer = data['_effectsListPlayer']
            effPlayer.stop()
            withShot = 0
            if burstCount == 1:
                effPlayer.play(gunModel, None, partial(self.stop, data))
                withShot = 1
            else:
                data['_burst'] = (burstCount - 1, burstInterval)
                data['_timerID'] = BigWorld.callback(burstInterval, partial(self.__doShot, data))
                effPlayer.play(gunModel)
                withShot = 2
            if data['entity'].isPlayerVehicle:
                avatar = BigWorld.player()
                avatar.getOwnVehicleShotDispersionAngle(avatar.gunRotator.turretRotationSpeed, withShot)
            if not vehicle.appearance.isInWater:
                groundWaveEff = effPlayer.effectsList.relatedEffects.get('groundWave')
                if groundWaveEff is not None:
                    self.__doGroundWaveEffect(data['entity'], groundWaveEff, gunModel)
            self.__doRecoil(vehicle, gunModel)
            if vehicle.isPlayerVehicle:
                appearance = vehicle.appearance
                appearance.executeShootingVibrations(vehicle.typeDescriptor.shot['shell']['caliber'])
        except Exception:
            LOG_CURRENT_EXCEPTION()
            self.stop(data)

        return

    def __doRecoil(self, vehicle, gunModel):
        appearance = vehicle.appearance
        appearance.recoil()

    def __doGroundWaveEffect(self, vehicle, groundWaveEff, gunModel):
        node = gunModel.node('HP_gunFire')
        gunMatr = Math.Matrix(node)
        gunPos = gunMatr.translation
        gunDir = gunMatr.applyVector((0, 0, 1))
        upVec = Math.Matrix(vehicle.matrix).applyVector(Math.Vector3(0, 1, 0))
        if upVec.y != 0:
            centerToGun = gunPos - vehicle.position
            centerToGunDist = centerToGun.length
            centerToGun.normalise()
            gunHeight = centerToGunDist * centerToGun.dot(upVec) / upVec.y
            gunPos.y -= gunHeight
        testRes = BigWorld.wg_collideSegment(BigWorld.player().spaceID, gunPos + Math.Vector3(0, 0.5, 0), gunPos - Math.Vector3(0, 1.5, 0), 128)
        if testRes is None:
            return
        else:
            position = testRes[0]
            BigWorld.player().terrainEffects.addNew(position, groundWaveEff.effectsList, groundWaveEff.keyPoints, None, dir=gunDir, surfaceMatKind=testRes[2], start=position + Math.Vector3(0, 0.5, 0), end=position - Math.Vector3(0, 0.5, 0), entity_id=vehicle.id)
            return


class DamageMarker(EntityExtra):

    def _readConfig(self, dataSection, containerName):
        self.deviceUserString = dataSection.readString('deviceUserString')
        if not self.deviceUserString:
            self._raiseWrongConfig('deviceUserString', containerName)
        self.deviceUserString = i18n.makeString(self.deviceUserString)
        soundSection = dataSection['sounds']
        self.sounds = {}
        for state in ('critical', 'destroyed', 'functional', 'fixed'):
            sound = soundSection.readString(state)
            if sound:
                self.sounds[state] = sound


class TrackHealth(DamageMarker):

    def _readConfig(self, dataSection, containerName):
        DamageMarker._readConfig(self, dataSection, containerName)
        self.__isLeft = dataSection.readBool('isLeft')
        functionalCanMoveState = 'functionalCanMove'
        self.sounds[functionalCanMoveState] = dataSection.readString('sounds/' + functionalCanMoveState)

    def _start(self, data, args):
        data['entity'].appearance.addCrashedTrack(self.__isLeft)

    def _cleanup(self, data):
        data['entity'].appearance.delCrashedTrack(self.__isLeft)


class Fire(EntityExtra):

    def _readConfig(self, dataSection, containerName):
        self.sounds = {}
        startSound = dataSection.readString('sounds/fireStarted')
        if startSound:
            self.sounds['critical'] = startSound
            self.sounds['destroyed'] = startSound
        else:
            self._raiseWrongConfig('sounds/fireStarted', containerName)
        stopSound = dataSection.readString('sounds/fireStopped')
        if stopSound:
            self.sounds['fixed'] = stopSound
        else:
            self._raiseWrongConfig('sounds/fireStopped', containerName)

    def _start(self, data, args):
        data['_isStarted'] = False
        vehicle = data['entity']
        isUnderwater = vehicle.appearance.isUnderwater
        data['wasUnderwater'] = isUnderwater
        if not isUnderwater:
            self.__playEffect(data)
        data['_isStarted'] = True
        vehicle.appearance.switchFireVibrations(True)

    def _cleanup(self, data):
        if not data['_isStarted']:
            return
        else:
            vehicle = data['entity']
            vehicle.appearance.switchFireVibrations(False)
            effectsListPlayer = self.__getEffectsListPlayer(data)
            if effectsListPlayer is not None:
                if vehicle.health <= 0:
                    effectsListPlayer.stop(forceCallback=True)
                    return
                effectsListPlayer.keyOff()
            return

    def __getEffectsListPlayer(self, data):
        effectsListPlayerRef = data.get('_effectsPlayer', None)
        if effectsListPlayerRef is not None:
            return effectsListPlayerRef()
        else:
            return

    def __playEffect(self, data):
        vehicle = data['entity']
        stages, effects, _ = random.choice(vehicle.typeDescriptor.type.effects['flaming'])
        data['entity_id'] = vehicle.id
        waitForKeyOff = True
        effectListPlayer = vehicle.appearance.boundEffects.addNew(None, effects, stages, waitForKeyOff, **data)
        data['_effectsPlayer'] = weakref.ref(effectListPlayer)
        return

    def checkUnderwater(self, vehicle, isVehicleUnderwater):
        data = vehicle.extras[self.index]
        wasUnderwater = data.get('wasUnderwater', False)
        if isVehicleUnderwater and not wasUnderwater:
            effectsListPlayer = self.__getEffectsListPlayer(data)
            if effectsListPlayer is not None:
                effectsListPlayer.stop(forceCallback=True)
                del data['_effectsPlayer']
        if not isVehicleUnderwater and wasUnderwater:
            self.__playEffect(data)
        data['wasUnderwater'] = isVehicleUnderwater
        return


class Afterburning(EntityExtra):
    _EFFECT_NAME = 'effect'

    def _readConfig(self, dataSection, containerName):
        effectsName = dataSection.readString(Afterburning._EFFECT_NAME)
        if not effectsName:
            self._raiseWrongConfig(Afterburning._EFFECT_NAME, containerName)
        self.afterburningEffectsList = vehicles.g_cache._vehicleEffects.get(effectsName, None)
        if self.afterburningEffectsList is None:
            self._raiseWrongConfig(Afterburning._EFFECT_NAME, containerName)
        return

    def _start(self, data, args):
        vehicle = data['entity']
        data['entity_id'] = vehicle.id
        getRunning = vehicle.getRunningExtra
        hasTrackCrash = getRunning('leftTrackHealth') is not None or getRunning('rightTrackHealth') is not None
        if not hasTrackCrash:
            self.startEmission(vehicle, data)
        return

    def _cleanup(self, data):
        effectsList = data['_effectsListPlayer']()
        if effectsList is not None:
            effectsList.keyOff()
        return

    def startEmission(self, vehicle, data = None):
        if data is None:
            data = vehicle.extras[self.index]
        effects = random.choice(self.afterburningEffectsList)
        effectsPlayer = data.get('_effectsListPlayer', None)
        if effectsPlayer is not None:
            effectsPlayer = effectsPlayer()
        if effectsPlayer is None:
            effectsPlayer = vehicle.appearance.boundEffects.addNew(None, effects.effectsList, effects.keyPoints, True, **data)
            data['_effectsListPlayer'] = weakref.ref(effectsPlayer)
        effectsPlayer.stop()
        effectsPlayer.play(vehicle.appearance.compoundModel, None, None, True)
        return

    def ceaseEmission(self, vehicle, data = None):
        hasOnlyOnceCrash = xor(vehicle.getRunningExtra('leftTrackHealth') is not None, vehicle.getRunningExtra('rightTrackHealth') is not None)
        if not hasOnlyOnceCrash:
            return
        else:
            if data is None:
                data = vehicle.extras[self.index]
            effectsListPlayer = data['_effectsListPlayer']()
            if effectsListPlayer is not None:
                effectsListPlayer.keyOff()
            return