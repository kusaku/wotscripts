# Embedded file name: scripts/client/CameraEffect.py
import BigWorld
import Math
import math
from MathExt import clamp
from clientConsts import SPEED_IDLE_EFFECT_START, SPEED_IDLE_EFFECT_END
from consts import CAMERAEFFECTS_PATH, VELLOCITY_OF_SOUND, LOGICAL_PART, WORLD_SCALING, SPEED_SCALING
from debug_utils import LOG_DEBUG, LOG_ERROR, LOG_WARNING, LOG_TRACE
import GameEnvironment
from CameraStates import CameraState
import db.DBLogic
from EntityHelpers import EntityStates
from _preparedBattleData_db import preparedBattleData
import operator
g_instance = None
SPEEDOMETER_DATA_SIZE = 7
SPEEDOMETER_STALL_SPEED_IDX = 0
SPEEDOMETER_NORMAL_START_SPEED_IDX = 2
SPEEDOMETER_NORMAL_END_SPEED_IDX = 3
SPEEDOMETER_CRITICAL_SPEED_IDX = 5
SPEEDOMETER_MAX_SPEED_IDX = 6

class Param:
    TargetCamPreset = 0


def Init():
    global g_instance
    LOG_TRACE('Init()')
    if g_instance == None:
        g_instance = CameraEffectManager()
        g_instance.init()
    return g_instance


def Destroy():
    global g_instance
    LOG_TRACE('Destroy()')
    if g_instance != None:
        g_instance.destroy()
        g_instance = None
    return


def debugReload():
    global g_instance
    LOG_DEBUG('!!!!! CameraEffects reloaded')
    if g_instance != None:
        g_instance.destroy()
        g_instance = CameraEffectManager()
    return


class SpeedState:
    SLOW = 0
    NORMAL = 1
    FAST = 2

    def __init__(self, start, end, effectID, prevStateID, nextStateID, stateMachine):
        self.__startValue = start
        self.__endValue = end
        self.__effectID = effectID
        self.__prevStateID = prevStateID
        self.__nextStateID = nextStateID
        self.__stateMachine = stateMachine

    def __setEffectTime(self, effectID, time):
        effectController = GameEnvironment.getCamera().getAircraftCam().effectController
        return effectController.setEffectTime(effectID, time)

    def start(self):
        g_instance.onCameraEffect(self.__effectID, True)

    def stop(self):
        g_instance.onCameraEffect(self.__effectID, False)

    def update(self, speedValue):
        stateChanged = False
        if speedValue > self.__endValue:
            stateChanged = self.goNextState()
        elif speedValue < self.__startValue:
            stateChanged = self.goPrevState()
        if stateChanged:
            self.__stateMachine.update(speedValue)
        else:
            finalSpeedValue = clamp(self.__startValue, speedValue, self.__endValue)
            finalSpeedValue = (finalSpeedValue - self.__startValue) / (self.__endValue - self.__startValue)
            res = self.__setEffectTime(self.__effectID, finalSpeedValue)
            if not res:
                g_instance.onCameraEffect(self.__effectID, True)
                self.__setEffectTime(self.__effectID, finalSpeedValue)

    def goNextState(self):
        return self.__stateMachine.setState(self.__nextStateID)

    def goPrevState(self):
        return self.__stateMachine.setState(self.__prevStateID)


class SpeedStateMachine:

    def __init__(self):
        self.__states = {}
        self.__curState = None
        self.__idleSpeedState = None
        return

    def update(self, speedValue):
        if self.__curState:
            self.__curState.update(speedValue)
        if self.__idleSpeedState:
            self.__idleSpeedState.update(speedValue)

    def addState(self, stateID, stateObject):
        self.__states[stateID] = stateObject

    def setState(self, stateID):
        if stateID is not None:
            if stateID in self.__states:
                if self.__curState:
                    self.__curState.stop()
                self.__curState = self.__states[stateID]
                self.__curState.start()
                return True
            LOG_ERROR('Unknown state: ', stateID)
        return False

    def initIdleSpeedState(self):
        stateID = SpeedState.NORMAL
        if stateID in self.__states:
            self.__idleSpeedState = self.__states[stateID]
            self.__idleSpeedState.start()

    def destroy(self):
        if self.__curState:
            self.__curState.stop()
            self.__curState = None
        if self.__idleSpeedState:
            self.__idleSpeedState.stop()
            self.__idleSpeedState = None
        self.__states.clear()
        return


class CameraEffectManager:

    class CommonGameStates:
        FORSAGE_ACTIVATED = 1

    PS_STOP, PS_NORMAL, PS_FORSAGE = range(0, 3)
    __FORSAGE_STATES = set([CameraState.Empty,
     CameraState.NormalCombat,
     CameraState.MouseCombat,
     CameraState.JoystickCombat,
     CameraState.GamepadCombat,
     CameraState.NormalAssault,
     CameraState.MouseAssault,
     CameraState.JoystickAssault,
     CameraState.GamepadAssault])
    __NEAR_PLANE_AIRWAVE_CHECK_INTERVAL = 0.5
    __MAX_SHOOTING_FORCE_GUN_CALIBER = 50.0

    def __init__(self):
        player = BigWorld.player()
        visualSettings = player.settings.airplane.visualSettings
        aircraftVibrationMatrix = player.resMatrix.a.a
        customOutputSettings = BigWorld.player().settings.airplane.visualSettings.accelFovSettings.outputSettings
        customOutputHalflifes = {}
        for outputData in customOutputSettings.itervalues():
            customOutputHalflifes[outputData.id] = outputData.settingHalflife

        GameEnvironment.getCamera().getAircraftCam().effectController.init(CAMERAEFFECTS_PATH, visualSettings.camera, aircraftVibrationMatrix, customOutputHalflifes)
        self.__forsageValue = self.PS_NORMAL
        self.__paramPreprocessor = {}
        shootingEffectID = visualSettings.cameraEffects.shooting
        self.__paramPreprocessor[shootingEffectID] = self.__preprocessShootingParams
        self.__paramPreprocessor['NEAR_PLANE_AIRWAVE'] = self.__preprocessNearPlaneParams
        self.__speedStateMachine = SpeedStateMachine()
        self.__maxSpeed = VELLOCITY_OF_SOUND
        self.__initSpeedStateMachine(db.DBLogic.g_instance.cameraEffects.normSpeedAddRelNeigbourZone)
        self.__nearPlaneDistances = {}
        self.__wakePlaneForces = {}
        self.__cbUpdateNearPlaneEffects = None
        return

    def __initOscillations(self):
        accelFovSettings = BigWorld.player().settings.airplane.visualSettings.accelFovSettings
        oscParams = {}
        oscParams['worldScaling'] = WORLD_SCALING
        oscParams['speedScaling'] = SPEED_SCALING
        oscParams['gravityAcceleration'] = db.DBLogic.g_instance.aircrafts.environmentConstants.gravityAcceleration.length
        oscParams['minRelativeAcceleration'] = accelFovSettings.relativeAccelerationLimits.x
        oscParams['maxRelativeAcceleration'] = accelFovSettings.relativeAccelerationLimits.y
        strFighterType = str(accelFovSettings.cameraEffectID)
        if strFighterType != '':
            idx = strFighterType.index('_')
            if idx > 0:
                strFighterType = strFighterType[:strFighterType.index('_')]
                self.__setOscillationParams('player_accel_lag_' + strFighterType.lower(), oscParams)

    def __onCameraStateChanged(self):
        state = GameEnvironment.getCamera().getState()
        if state not in self.__class__.__FORSAGE_STATES:
            self.handleForsage(0)

    def __initSpeedStateMachine(self, normSpeedAddRelNeigbourZone):
        player = BigWorld.player()
        playerGID = player.globalID
        battleData = preparedBattleData.get(playerGID, None)
        if battleData:
            speedometer = battleData.speedometer
            if speedometer:
                if len(speedometer) == SPEEDOMETER_DATA_SIZE:
                    playerCameraID = player.settings.airplane.visualSettings.camera
                    camPresetInfo = db.DBLogic.g_instance.cameraEffects.camPresetInfo
                    if playerCameraID in camPresetInfo:
                        normSpeedShift = camPresetInfo[playerCameraID].normSpeedShift
                        curHullID = player.logicalParts[LOGICAL_PART.HULL]
                        curEngineID = player.logicalParts[LOGICAL_PART.ENGINE]
                        try:
                            stallSpeed = player.settings.airplane.flightModel.hull[curHullID].stallSpeed
                            normalSpeed = player.settings.airplane.flightModel.engine[curEngineID].maxSpeed
                            diveSpeed = player.settings.airplane.flightModel.hull[curHullID].diveSpeed
                        except:
                            LOG_ERROR('Failed to get speed values for current parts                                 (Airplane ID: {0}, Hull ID: {1}, Engine ID: {2}). Using default part values.'.format(player.settings.airplane.name, curHullID, curEngineID))
                            stallSpeed = player.settings.airplane.flightModel.hull[0].stallSpeed
                            normalSpeed = player.settings.airplane.flightModel.engine[0].maxSpeed
                            diveSpeed = player.settings.airplane.flightModel.hull[0].diveSpeed

                        slowZoneStart = stallSpeed / diveSpeed
                        normalZoneStart = (speedometer[SPEEDOMETER_NORMAL_START_SPEED_IDX] + speedometer[SPEEDOMETER_NORMAL_END_SPEED_IDX]) / 2
                        relativeNormalSpeed = normalSpeed / diveSpeed
                        if relativeNormalSpeed < normalZoneStart:
                            LOG_WARNING('Normal speed is less than default normal speed zone start. Swapping values.')
                            tmp = normalZoneStart
                            normalZoneStart = relativeNormalSpeed
                            relativeNormalSpeed = tmp
                        normalZoneStart = normalZoneStart * (1.0 - normSpeedShift) + relativeNormalSpeed * normSpeedShift
                        fastZoneStart = normalZoneStart
                        fastZoneEnd = 1.0
                        self.__maxSpeed = diveSpeed
                        fastZoneStart += (fastZoneEnd - fastZoneStart) * normSpeedAddRelNeigbourZone
                        normalZoneStart -= (normalZoneStart - slowZoneStart) * normSpeedAddRelNeigbourZone
                        slowSpeedState = SpeedState(slowZoneStart, fastZoneStart, 'SLOW_SPEED', None, SpeedState.FAST, self.__speedStateMachine)
                        self.__speedStateMachine.addState(SpeedState.SLOW, slowSpeedState)
                        fastSpeedState = SpeedState(fastZoneStart, fastZoneEnd, 'FAST_SPEED', SpeedState.SLOW, None, self.__speedStateMachine)
                        self.__speedStateMachine.addState(SpeedState.FAST, fastSpeedState)
                        idleSpeedState = SpeedState(SPEED_IDLE_EFFECT_START, SPEED_IDLE_EFFECT_END, 'NORMAL_SPEED', None, None, self.__speedStateMachine)
                        self.__speedStateMachine.addState(SpeedState.NORMAL, idleSpeedState)
                else:
                    LOG_ERROR('Speedometer wrong data length. Expected: {0}, Actual: {1}'.format(SPEEDOMETER_DATA_SIZE, len(speedometer)))
            else:
                LOG_ERROR("Can't get an speedometer data from the prepared battle data")
        else:
            LOG_ERROR("Can't get a battle data for global ID: ", playerGID)
        return

    def initSpeedSystem(self):
        self.__speedStateMachine.setState(SpeedState.FAST)
        self.__speedStateMachine.initIdleSpeedState()

    def init(self):
        self.initSpeedSystem()
        camera = GameEnvironment.getCamera()
        camera.eStateChanged += self.__onCameraStateChanged
        self.__initOscillations()
        self.startAccelerationEffect()

    def startAccelerationEffect(self):
        accelFovSettings = BigWorld.player().settings.airplane.visualSettings.accelFovSettings
        fovEffectID = accelFovSettings.cameraEffectID
        if fovEffectID != '':
            self.onCameraEffect(fovEffectID)

    def stopAccelerationEffect(self):
        accelFovSettings = BigWorld.player().settings.airplane.visualSettings.accelFovSettings
        fovEffectID = accelFovSettings.cameraEffectID
        if fovEffectID != '':
            self.onCameraEffect(fovEffectID, False)

    def destroy(self):
        self.stopNearPlaneEffects()
        self.__speedStateMachine.destroy()
        self.__paramPreprocessor.clear()
        camera = GameEnvironment.getCamera()
        camera.getAircraftCam().effectController.clear()
        camera.eStateChanged -= self.__onCameraStateChanged

    def __forsageValueToSignal(self, value):
        if value == -1.0:
            return self.PS_STOP
        elif value == 1.0:
            return self.PS_FORSAGE
        else:
            return self.PS_NORMAL

    def __setCommonGameState(self, state):
        effectController = GameEnvironment.getCamera().getAircraftCam().effectController
        effectController.scriptStates |= state

    def __unsetCommonGameState(self, state):
        effectController = GameEnvironment.getCamera().getAircraftCam().effectController
        effectController.scriptStates ^= state

    def handleForsage(self, value):
        cam = GameEnvironment.getCamera()
        cameraState = cam.getState()
        signal = self.__forsageValueToSignal(value)
        if signal != self.__forsageValue and (signal == self.PS_NORMAL or cameraState in self.__class__.__FORSAGE_STATES):
            if signal == self.PS_FORSAGE:
                self.onCameraEffect('FORSAGE', True)
                self.__setCommonGameState(self.__class__.CommonGameStates.FORSAGE_ACTIVATED)
                if self.__forsageValue == self.PS_STOP:
                    self.onCameraEffect('BRAKE', False)
            elif signal == self.PS_STOP:
                self.onCameraEffect('BRAKE', True)
                if self.__forsageValue == self.PS_FORSAGE:
                    self.onCameraEffect('FORSAGE', False)
                    self.__unsetCommonGameState(self.__class__.CommonGameStates.FORSAGE_ACTIVATED)
            elif self.__forsageValue == self.PS_FORSAGE:
                self.onCameraEffect('FORSAGE', False)
                self.__unsetCommonGameState(self.__class__.CommonGameStates.FORSAGE_ACTIVATED)
            elif self.__forsageValue == self.PS_STOP:
                self.onCameraEffect('BRAKE', False)
            self.__forsageValue = signal

    def handleSpeed(self, speedMPS, ignoreNonForsageStates = True):
        cam = GameEnvironment.getCamera()
        cameraState = cam.getState()
        isValidCameraState = cameraState in self.__class__.__FORSAGE_STATES if ignoreNonForsageStates else True
        if EntityStates.inState(BigWorld.player(), EntityStates.GAME | EntityStates.PRE_START_INTRO) and speedMPS > 0 and isValidCameraState:
            speedNorm = clamp(0.0, speedMPS / self.__maxSpeed, 1.0)
            self.__speedStateMachine.update(speedNorm)

    def onAirEffect(self, effectName, enable = True):
        LOG_DEBUG('### onCameraEffect: ', effectName, enable)
        effectController = GameEnvironment.getCamera().getAircraftCam().effectController
        if enable:
            effectController.startAirEffect(effectName)
        else:
            effectController.stopAirEffect(effectName)

    def onCameraEffect(self, effectName, enable = True, force = 1.0, dir = Math.Vector3(0.0, 0.0, 0.0), additionalParams = None):
        LOG_DEBUG('### onCameraEffect: ', effectName, enable)
        effectController = GameEnvironment.getCamera().getAircraftCam().effectController
        if enable:
            if effectName in self.__paramPreprocessor:
                newForce = self.__paramPreprocessor[effectName](force, additionalParams)
                if newForce is not None:
                    force = newForce
            effectController.startEffect(effectName, force, dir)
        else:
            effectController.stopEffect(effectName)
        return

    def stopAllEffects(self):
        effectController = GameEnvironment.getCamera().getAircraftCam().effectController
        effectController.stopAllEffects()

    def fadeOutAllEffects(self, duration):
        effectController = GameEnvironment.getCamera().getAircraftCam().effectController
        effectController.fadeOutEffects(duration)

    def setEffectParams(self, effectName, params):
        effectController = GameEnvironment.getCamera().getAircraftCam().effectController
        effectController.setEffectParams(effectName, params)

    def __setOscillationParams(self, oscName, params):
        effectController = GameEnvironment.getCamera().getAircraftCam().effectController
        effectController.setOscillationParams(oscName, params)

    def setEffectForce(self, effectName, val, additionalParams = None):
        force = val
        if effectName in self.__paramPreprocessor:
            force = self.__paramPreprocessor[effectName](force, additionalParams)
        effectController = GameEnvironment.getCamera().getAircraftCam().effectController
        effectController.setEffectForce(effectName, force)

    def startNearPlaneEffects(self):
        if not self.__cbUpdateNearPlaneEffects:
            self.__updateNearPlaneEffects()

    def stopNearPlaneEffects(self):
        if self.__cbUpdateNearPlaneEffects:
            BigWorld.cancelCallback(self.__cbUpdateNearPlaneEffects)
            self.__cbUpdateNearPlaneEffects = None
        self.__nearPlaneDistances.clear()
        self.__wakePlaneForces.clear()
        return

    def __updateNearPlaneEffects(self):
        prevWakePlanesNum = len(self.__wakePlaneForces)
        for target in BigWorld.player().visibleAvatars.values():
            self.__updateAirwave(target)
            self.__updateWakeTarget(target)

        self.__updateWakeEffect(prevWakePlanesNum)
        self.__cbUpdateNearPlaneEffects = BigWorld.callback(self.__class__.__NEAR_PLANE_AIRWAVE_CHECK_INTERVAL, self.__updateNearPlaneEffects)

    def __updateAirwave(self, target):
        AIRWAVE_DISTANCE = db.DBLogic.g_instance.cameraEffects.airwaveDistance
        if target.inWorld and EntityStates.inState(target, EntityStates.GAME):
            targetDir = target.position - BigWorld.player().position
            targetDist = targetDir.length
            if targetDist < AIRWAVE_DISTANCE:
                if target.id not in self.__nearPlaneDistances:
                    self.__nearPlaneDistances[target.id] = (targetDist, targetDir, target.id)
                else:
                    targetPrevInfo = self.__nearPlaneDistances[target.id]
                    if targetPrevInfo:
                        targetPrevDist = targetPrevInfo[0]
                        if targetPrevDist < targetDist:
                            self.__startAirwaveEffect(targetPrevInfo)
                            self.__nearPlaneDistances[target.id] = None
                        else:
                            self.__nearPlaneDistances[target.id] = (targetDist, targetDir, target.id)
                return
        if target.id in self.__nearPlaneDistances:
            targetInfo = self.__nearPlaneDistances[target.id]
            if targetInfo:
                self.__startAirwaveEffect(targetInfo)
            self.__nearPlaneDistances.pop(target.id)
        return

    def __startAirwaveEffect(self, targetInfo):
        targetDist = targetInfo[0]
        targetDir = targetInfo[1]
        targetID = targetInfo[2]
        AIRWAVE_DISTANCE = db.DBLogic.g_instance.cameraEffects.airwaveDistance
        force = 1.0 - targetDist / AIRWAVE_DISTANCE
        target = BigWorld.entities.get(targetID)
        targetCamPreset = target.settings.airplane.visualSettings.camera
        self.onCameraEffect('NEAR_PLANE_AIRWAVE', True, force, targetDir, {Param.TargetCamPreset: targetCamPreset})

    def __updateWakeTarget(self, target):
        if target.inWorld and EntityStates.inState(target, EntityStates.GAME):
            dirFromTarget = BigWorld.player().position - target.position
            distToTarget = dirFromTarget.length
            WAKE_HALF_ANGLE = db.DBLogic.g_instance.cameraEffects.wakeParams.angle * 0.5
            if distToTarget <= db.DBLogic.g_instance.cameraEffects.wakeParams.distance and not EntityStates.inState(target, EntityStates.OBSERVER | EntityStates.DESTROYED):
                targetDir = target.getRotation().getAxisZ()
                angleToTarget = math.pi - abs(dirFromTarget.angle(targetDir))
                if angleToTarget < WAKE_HALF_ANGLE:
                    playerCamPresetID = BigWorld.player().settings.airplane.visualSettings.camera
                    targetCamPresetID = target.settings.airplane.visualSettings.camera
                    camPresetInfo = db.DBLogic.g_instance.cameraEffects.camPresetInfo
                    if targetCamPresetID in camPresetInfo and playerCamPresetID in camPresetInfo:
                        targetFactor = camPresetInfo[targetCamPresetID].amplitudeFactor
                        playerFactor = camPresetInfo[playerCamPresetID].amplitudeFactor
                        force = playerFactor / targetFactor * (1.0 - distToTarget / db.DBLogic.g_instance.cameraEffects.wakeParams.distance)
                        self.__wakePlaneForces[target.id] = force
                    return
        if target.id in self.__wakePlaneForces:
            self.__wakePlaneForces.pop(target.id)

    def __updateWakeEffect(self, prevWakePlanesNum):
        curWakePlanesNum = len(self.__wakePlaneForces)
        if curWakePlanesNum > 0:
            maxForce = max(self.__wakePlaneForces.iteritems(), key=operator.itemgetter(1))[1]
            if prevWakePlanesNum == 0:
                self.onCameraEffect('NEAR_PLANE_WAKE', maxForce)
            else:
                self.setEffectForce('NEAR_PLANE_WAKE', maxForce)
        elif prevWakePlanesNum > 0:
            self.onCameraEffect('NEAR_PLANE_WAKE', False)

    def __preprocessNearPlaneParams(self, force, params):
        if params:
            if Param.TargetCamPreset in params:
                camPresetID = params[Param.TargetCamPreset]
                camPresetInfo = db.DBLogic.g_instance.cameraEffects.camPresetInfo
                if camPresetID in camPresetInfo:
                    factor = camPresetInfo[camPresetID].amplitudeFactor
                    camPresetAmpFactorMin = db.DBLogic.g_instance.cameraEffects.camPresetAmpFactorMin
                    return force * camPresetAmpFactorMin / factor
                LOG_ERROR('Cannot find camera preset factor for: ', camPresetID)
            else:
                LOG_ERROR('Cannot find camera effect param with id: ', Param.TargetCamPreset)
        else:
            LOG_ERROR('Param storage is empty')

    def __preprocessShootingParams(self, force, params):
        if params:
            paramCaliber = 'caliber'
            if paramCaliber in params:
                curCaliber = params[paramCaliber]
                return clamp(0.0, curCaliber / self.__class__.__MAX_SHOOTING_FORCE_GUN_CALIBER, 1.0)
            LOG_ERROR('Cannot find param: ', paramCaliber)
        else:
            LOG_ERROR('Param storage is empty')