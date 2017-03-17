# Embedded file name: scripts/client/gui/ClientHangarSpace.py
import MathExt
import GUI
import CompoundSystem
import gui.GUIHelper
from debug_utils import *
from functools import partial
import math
from consts import *
from config_consts import DB_AIRCRAFT_CHECK
import db.DBLogic
import Settings
from EntityHelpers import convertArray2Dictionary, EntityStates
from DestructibleObjectFactory import DestructibleObjectFactory
from MathExt import clamp
from CameraStates import CameraState, CameraStateMachine
from random import seed, randrange
from clientConsts import BULLET_PARAM, TURRET_TRACKER_AXIS, DISABLE_HANGAR_TURRET_ANIMATION, FORCE_AXIS_STOPPED_VALUE
from Event import Event, EventManager
from HangarScripts import getHangarScriptsByName
from eventhandlers import planeBirthdayEvents
import db.DBLogic
import _camouflages_data
from ScenarioClient.HangarVehicleCinematicHelper import HangarVehicleCinematicHelper
from audio import GameSound
HANGAR_CINEMATIC_NAME = 'hangar_cinematic'
HANGAR_NODE = 'HP_hangar'
SHADOW_SCALE_CFC = 29.5 * AIRCRAFT_MODEL_SCALING

class HangarCameraStateMachine(CameraStateMachine):

    def __init__(self):
        CameraStateMachine.__init__(self)
        self.addState(CameraState.Free, CameraStateFree())
        self.addState(CameraState.SuperFree, CameraStateSuperFree())
        self.addState(CameraState.SpectatorSide, CameraStateSpectatorSide())


class CameraStateSuperFree(CameraState):

    @property
    def distance(self):
        if self.strategy:
            return self.strategy.distance
        else:
            return 0.0

    @distance.setter
    def distance(self, value):
        self.__currentDistance = value
        if self.strategy:
            self.strategy.distance = value

    def enter(self, params = None):
        self.strategy = BigWorld.CameraStrategySuperFree(BigWorld.dcursor().matrix)
        self._context.cameraInstance.setStrategy(self.strategy, self._context.interpolationDuration)


class CameraStateFree(CameraState):

    def __init__(self):
        self.__scheduledFov = 0.0
        self.__targetShifted = False

    @property
    def targetShifted(self):
        return self.__targetShifted

    @property
    def distance(self):
        if self.strategy:
            return self.strategy.distance
        else:
            return 0.0

    @distance.setter
    def distance(self, value):
        if self.strategy:
            self.strategy.distance = value
            self.__setFovByDistance(self.strategy.distance, self._context.cameraSettings.cam_fov_interpolation_time)

    def __setFovByDistance(self, distance, rampTime):
        settings = self._context.cameraSettings
        distMin = settings.cam_dist_constr[0]
        distMed = settings.cam_dist_constr[1]
        distMax = settings.cam_dist_constr[2]
        distanceK = clamp(distMin, distance, distMax)
        newFov = 0
        if distanceK < distMed:
            k = (distMed - distanceK) / (distMed - distMin) if distMed != distMin else 0
            fovDelta = settings.cam_fov_constr[0] - settings.cam_fov_constr[1]
            newFov = fovDelta * k + settings.cam_fov_constr[1]
        else:
            k = (distanceK - distMed) / (distMax - distMed) if distMed != distMax else 0
            fovDelta = settings.cam_fov_constr[2] - settings.cam_fov_constr[1]
            newFov = fovDelta * k + settings.cam_fov_constr[1]
        if self.__scheduledFov != newFov:
            self.__scheduledFov = newFov
            BigWorld.projection().rampFov(newFov, rampTime, 1.0)

    def enter(self, params = None):
        self.__scheduledFov = 0.0
        settings = self._context.cameraSettings
        cameraInstance = self._context.cameraInstance
        distMin = settings.cam_dist_constr[0]
        distMax = settings.cam_dist_constr[2]
        distance = settings.cam_start_dist
        self.strategy = BigWorld.CameraStrategyFree(distance, BigWorld.dcursor().matrix, distMin, distMax, cameraInstance.parentMatrix, settings.cam_ellipticity)
        self.strategy.aroundLocalAxes = False
        self.strategy.turningHalflife = settings.cam_fluency_rotation
        self.strategy.distanceHalflife = settings.cam_fluency_zooming
        self.distance = distance
        self.strategy.screenShiftInterval = 0.0
        cameraInstance.setStrategy(self.strategy, self._context.interpolationDuration)

    def reEnter(self, params = None):
        settings = self._context.cameraSettings
        cameraInstance = self._context.cameraInstance
        self.strategy.distanceMin = settings.cam_dist_constr[0]
        self.strategy.distanceMax = settings.cam_dist_constr[2]
        val = self.strategy.distance
        if self._context.setNewDist:
            val = settings.cam_start_dist
        self.strategy.ellipticity = settings.cam_ellipticity
        self.strategy.sourceProvider = cameraInstance.parentMatrix
        self.distance = val

    def setCameraTargetShift(self, shiftEnabled):
        self.__targetShifted = shiftEnabled
        self.strategy.screenShiftInterval = self._context.cameraSettings.cam_lobby_win_screen_shift_interval
        self.strategy.screenShiftX = self._context.cameraSettings.cam_lobby_win_screen_shift_x if self.__targetShifted else 0.0


class CameraStateSpectatorSide(CameraState):
    GROUND_NODE_UPDATE_TIME = 1.5

    def __init__(self):
        CameraState.__init__(self)
        self.__hpModel = None
        self.__cbExitState = None
        self.__returnToNormal = -1.0
        self.__lagHalfLife = 0.0
        self.__finishTime = 0.0
        self.__isNodeTimeline = False
        return

    def __parseData(self, data):
        if self.__cbExitState:
            BigWorld.cancelCallback(self.__cbExitState)
            self.__cbExitState = None
        if data.finishTime > 0.0:
            self.__finishTime = data.finishTime
            self.__cbExitState = BigWorld.callback(self.__finishTime, self._context.cameraManager.leaveState)
            self.__returnToNormal = data.finishLength
        if hasattr(data, 'lagHalfLife'):
            self.__lagHalfLife = data.lagHalfLife
        strategyData = {}
        self.__parseNodePositions(data, strategyData)
        self.__parseNodeTargets(data, strategyData)
        self.__parseTargets(data, strategyData)
        self.__parseFOVs(data, strategyData)
        self.__parsePositions(data, strategyData)
        self.__parseRotations(data, strategyData)
        self.__parseEffects(data, strategyData)
        if hasattr(data, 'linkingType'):
            strategyData['linkingType'] = data.linkingType
        else:
            LOG_ERROR("Linking type isn't exist!")
        return strategyData

    def __parseNodePositions(self, data, parsedData):
        if hasattr(data, 'nodePositionTimeline'):
            parsedData['nodePositions'] = self.__parseNodeTimeline(data.nodePositionTimeline)

    def __parseNodeTargets(self, data, parsedData):
        if hasattr(data, 'nodeTargetTimeline'):
            parsedData['nodeTargets'] = self.__parseNodeTimeline(data.nodeTargetTimeline)

    def __parseTargets(self, data, parsedData):
        if hasattr(data, 'targetTimeline'):
            parsedData['targets'] = self.__parsePositionTimeline(data.targetTimeline)

    def __parseFOVs(self, data, parsedData):
        parsedData['fov'] = self.__parseFOVTimeline(data.fovTimeline)

    def __parsePositions(self, data, parsedData):
        if hasattr(data, 'positionTimeline'):
            parsedData['positions'] = self.__parsePositionTimeline(data.positionTimeline)

    def __parseRotations(self, data, parsedData):
        if hasattr(data, 'rotationTimeline'):
            parsedData['rotations'] = self.__parseRotationTimeline(data.rotationTimeline)

    def __parseEffects(self, data, parsedData):
        if hasattr(data, 'effectTimeline'):
            parsedData['effects'] = self.__parseEffectTimeline(data.effectTimeline)

    def __parsePositionTimeline(self, data):
        positionKeytimes = []
        for keytime in data.keytime:
            try:
                coord = keytime.position * self._context.cameraSettings.v_scale + self._context.cameraSettings.v_start_pos
                fadeinTime = keytime.fadeinTime if hasattr(keytime, 'fadeinTime') else 0.0
                fadeoutTime = keytime.fadeoutTime if hasattr(keytime, 'fadeoutTime') else 0.0
                positionKeytimes.append((keytime.time,
                 coord,
                 0,
                 keytime.type,
                 keytime.duration,
                 fadeinTime,
                 fadeoutTime))
            except:
                LOG_CURRENT_EXCEPTION()
                continue

        return positionKeytimes

    def __parseRotationTimeline(self, data):
        rotationKeytimes = []
        for keytime in data.keytime:
            try:
                fadeinTime = keytime.fadeinTime if hasattr(keytime, 'fadeinTime') else 0.0
                fadeoutTime = keytime.fadeoutTime if hasattr(keytime, 'fadeoutTime') else 0.0
                rotationKeytimes.append((keytime.time,
                 keytime.rotation,
                 0,
                 keytime.type,
                 keytime.duration,
                 fadeinTime,
                 fadeoutTime))
            except:
                LOG_CURRENT_EXCEPTION()
                continue

        return rotationKeytimes

    def __parseNodeTimeline(self, data):
        nodeKeytimes = []
        for keytime in data.keytime:
            try:
                from clientConsts import NODE_TIMELINE_NODE_FLAGS
                from clientConsts import NODE_TIMELINE_NEAREST_NODE
                flags = NODE_TIMELINE_NODE_FLAGS.NONE
                try:
                    coord = self.__hpModel.node(keytime.node).nodeLocalTransform.applyToOrigin() * self._context.cameraSettings.v_scale
                except Exception as e:
                    x, y, z, flags = BigWorld.getCameraNode(keytime.node)
                    coord = Math.Vector3(x, y, z)

                fadeinTime = keytime.fadeinTime if hasattr(keytime, 'fadeinTime') else 0.0
                fadeoutTime = keytime.fadeoutTime if hasattr(keytime, 'fadeoutTime') else 0.0
                nodeKeytimes.append((keytime.time,
                 coord,
                 flags,
                 keytime.type,
                 keytime.duration,
                 fadeinTime,
                 fadeoutTime))
            except:
                LOG_CURRENT_EXCEPTION()
                continue

        return nodeKeytimes

    def __parseFOVTimeline(self, data):
        fovKeytimes = []
        for keytime in data.keytime:
            fadeinTime = keytime.fadeinTime if hasattr(keytime, 'fadeinTime') else 0.0
            fadeoutTime = keytime.fadeoutTime if hasattr(keytime, 'fadeoutTime') else 0.0
            fovKeytimes.append((keytime.time,
             keytime.fov,
             keytime.duration,
             fadeinTime,
             fadeoutTime))

        return fovKeytimes

    def __parseEffectTimeline(self, data):
        effectKeytimes = []
        for keytime in data.keytime:
            weight = keytime.weight if hasattr(keytime, 'weight') else 1.0
            effectKeytimes.append((keytime.time,
             keytime.id,
             weight,
             keytime.enable))

        return effectKeytimes

    def enter(self, params = None):
        if params:
            animationData = self.__parseData(params)
            self.__isNodeTimeline = 'nodePositions' in animationData
            if not self.__isNodeTimeline:
                source = Math.Matrix()
                source.translation = Math.Vector3(0.0, 0.0, 0.0)
            else:
                source = Math.Matrix()
                source.setTranslate(self._context.cameraSettings.cam_start_target_pos)
            self.strategy = BigWorld.CameraStrategyCinematic(animationData, Math.Vector3(0.0, 1.0, 0.0), source, self.__cbExitState is None, self._context.cameraInstance.effectController, self.__lagHalfLife)
            self.strategy.staticNodeUpdateTime = self.__class__.GROUND_NODE_UPDATE_TIME
            self._context.cameraInstance.setStrategy(self.strategy, self._context.interpolationDuration)
        return

    def exit(self):
        CameraState.exit(self)
        self.__clear()

    def __clear(self):
        if self.__cbExitState:
            BigWorld.cancelCallback(self.__cbExitState)
            self.__cbExitState = None
        self.__finishTime = 0.0
        return

    def reEnter(self, params = None):
        self.updateParams(params)

    def updateParams(self, params = None):
        self.__clear()
        self.enter(params)

    def getReturnToNormalTime(self):
        return self.__returnToNormal

    def setReturnToNormalTime(self, val):
        self.__returnToNormal = val

    def setCinematicTime(self, value):
        self.strategy.setTime(value)
        if self.__finishTime > 0.0:
            if value < self.__finishTime:
                leaveTime = self.__finishTime - value
                if self.__cbExitState:
                    BigWorld.cancelCallback(self.__cbExitState)
                self.__cbExitState = BigWorld.callback(leaveTime, self._context.cameraManager.leaveState)


class HangarCamera(object):

    class CameraContext(object):
        pass

    def __init__(self):
        self.__cam = None
        self.__camView = 'default'
        self.__boundingRadius = None
        self.__hangarCfg = None
        self.__hangarSize = ''
        self.__cameraStateMachine = None
        self.__eventManager = EventManager()
        em = self.__eventManager
        self.eParentMatrixChanged = Event(em)
        self.eOnDestroy = Event(em)
        self.eStateChanged = Event(em)
        return

    def getAircraftCam(self):
        return self.__cam

    def destroy(self):
        self.eOnDestroy()
        if self.__cam == BigWorld.camera():
            self.__cam.spaceID = 0
            BigWorld.camera(None)
        self.__cam = None
        self.__hangarSize = ''
        self.__hangarCfg = None
        self.__cameraStateMachine = None
        context = HangarCamera.CameraContext()
        self.__fillStateInitParams(context)
        CameraState.setInitParams(context)
        self.__eventManager.clear()
        return

    def __fillStateInitParams(self, context, hangarSize = ''):
        context.cameraInstance = self.__cam
        context.cameraManager = self
        context.cameraSettings = self.__hangarCfg
        context.interpolationDuration = 0.0
        context.setNewDist = hangarSize != '' and self.__hangarSize != hangarSize
        self.__hangarSize = hangarSize

    def setState(self, cameraType, params = None):
        if self.getState() != CameraState.SuperFree and self.__cameraStateMachine:
            self.__cameraStateMachine.setState(cameraType, params)

    def leaveState(self, state = None):
        if self.__cameraStateMachine:
            self.__cameraStateMachine.leaveState(state)

    def getState(self):
        if self.__cameraStateMachine:
            return self.__cameraStateMachine.getState()

    def getStateStrategy(self):
        sObj = self.getStateObject()
        if sObj:
            return sObj.strategy

    def getStateObject(self):
        if self.__cameraStateMachine:
            return self.__cameraStateMachine.getCurStateObject()

    def createCamera(self, spaceID):
        self.__cam = BigWorld.AircraftCamera()
        self.__cam.spaceID = spaceID
        BigWorld.camera(self.__cam)

    def __setCameraParentMatrix(self, mat):
        self.__cam.parentMatrix = mat
        self.eParentMatrixChanged(mat)

    def setupCamera(self, hangarCfg, hangarSize):
        if not self.__cameraStateMachine:
            self.__cameraStateMachine = HangarCameraStateMachine()
        self.__hangarCfg = hangarCfg
        context = HangarCamera.CameraContext()
        self.__fillStateInitParams(context, hangarSize)
        CameraState.setInitParams(context)
        mat = Math.Matrix()
        mat.setTranslate(self.__hangarCfg.cam_start_target_pos)
        self.__setCameraParentMatrix(mat)
        self.setState(CameraState.Free)
        self.switchCameraView(self.__camView)

    def switchCameraView(self, camView):
        if camView in self.__hangarCfg.cam_views:
            self.__camView = camView
            view = self.__hangarCfg.cam_views[camView]
            mat = Math.Matrix()
            mat.setTranslate(self.__hangarCfg.cam_start_target_pos + view.cam_offset)
            self.__setCameraParentMatrix(mat)
            if view.cam_dist:
                self.getStateObject().distance = view.cam_dist
            if view.cam_fov:
                BigWorld.projection().fov = math.radians(view.cam_fov)
            if hasattr(view, 'cam_angles'):
                BigWorld.dcursor().pitch = math.radians(view.cam_angles[0])
                BigWorld.dcursor().yaw = math.radians(view.cam_angles[1])

    def updateCameraByMouseMove(self, dx, dy, dz):
        sourceMat = Math.Matrix(BigWorld.dcursor().matrix)
        yaw = sourceMat.yaw + dx * self.__hangarCfg.cam_sens_rotation
        pitch = sourceMat.pitch + dy * self.__hangarCfg.cam_sens_rotation
        if dz != 0:
            deltaDistance = math.copysign((self.__hangarCfg.cam_dist_constr[2] - self.__hangarCfg.cam_dist_constr[0]) / self.__hangarCfg.cam_zooming_steps, dz)
            self.getStateObject().distance -= deltaDistance
        pitch = _clamp(math.radians(self.__hangarCfg.cam_pitch_constr[0]), math.radians(self.__hangarCfg.cam_pitch_constr[1]), pitch)
        BigWorld.dcursor().pitch = pitch
        BigWorld.dcursor().yaw = yaw

    def updateStartDirection(self):
        BigWorld.dcursor().pitch = math.radians(self.__hangarCfg.cam_start_angles[0])
        BigWorld.dcursor().yaw = math.radians(self.__hangarCfg.cam_start_angles[1])

    def setDirectAngle(self, yaw, pitch):
        BigWorld.dcursor().pitch = pitch
        BigWorld.dcursor().yaw = yaw

    def getInterpolationDuration(self):
        return CameraState._context.interpolationDuration

    def setInterpolationDuration(self, value):
        CameraState._context.interpolationDuration = value


class HangarShootingAvatar(object):

    class FilterDummy:
        pass

    def __init__(self, hangarSpace, planeID):
        self.globalID = -1
        self.filter = HangarShootingAvatar.FilterDummy()
        self.matrix = Math.Matrix()
        self.__hangarSpace = hangarSpace
        self.__spaceId = self.__hangarSpace.spaceID
        self.__armamentStates = 0
        self.settings = db.DBLogic.g_instance.getAircraftData(planeID)
        self.controllers = {}

    def destroy(self):
        self.__hangarSpace = None
        return

    @property
    def yaw(self):
        return self.rotation.getYaw()

    @property
    def pitch(self):
        return self.rotation.getPitch()

    @property
    def roll(self):
        return self.rotation.getRoll()

    @property
    def position(self):
        return self.getShootingControllerPosition()

    @property
    def rotation(self):
        return self.getShootingControllerRotation()

    def getShootingControllerPosition(self):
        return self.matrix.translation

    def getShootingControllerRotation(self):
        res = Math.Quaternion()
        res.fromEuler(self.matrix.roll, self.matrix.pitch, self.matrix.yaw)
        return res

    def dynamicalDispersionCfc(self):
        return (0.0, 1.0)

    def autoAim(self, historyLayer, bulletStartPos, ownVelocity, reductionDir, bulletSpeed, autoguiderMaxDist, bulletTime):
        return (Math.Vector3(1, 0, 0), 0, -1)

    def addBulletBody(self, historyLayer, bulletStartPos, bulletVelocity, bulletTime, timeToLive, callbackOnRemove, data):
        return (bulletStartPos + bulletVelocity * timeToLive, -1, None)

    def getWorldVector(self):
        return Math.Vector3(0.0, 0.0, 0.0)

    @property
    def spaceID(self):
        return self.__spaceId

    @property
    def id(self):
        return 0

    @property
    def state(self):
        return EntityStates.GAME_CONTROLLED

    @property
    def armamentStates(self):
        return self.__armamentStates

    def setArmamentStates(self, armamentStates):
        self.__armamentStates = armamentStates

    def addBullet(self, startPos, endPos, bulletSpeed, time, gun, explosionEffect, asyncDelay = 0, gunPos = None, gunDir = None, gunID = 0):
        gunID = gunID or gun.uniqueId
        self.__hangarSpace.getModelManipulator().onAddBullet(gunID, asyncDelay)
        explosionF = None
        bullet = BigWorld.addBullet(startPos, endPos, bulletSpeed, time, gun.shootInfo.bulletRenderType, BULLET_PARAM.OWN, explosionF)
        self.__hangarSpace.getModelManipulator().onAddBullet(gunID, asyncDelay, 'SHELL_EFFECT????')
        return bullet

    def isPlayer(self):
        return True

    def updateAmmo(self):
        pass

    def onLoaded(self):
        mm = self.__hangarSpace.getModelManipulator()
        mp = mm.getMatrixProvider() if mm else Math.Matrix()
        self.matrix = mp


class ClientHangarSpace():
    AMPTY_HANGAR_SIZE = 'large'
    CLEAR_AFTER_LOAD_TIMES = 128

    class DebugParams:

        def __init__(self):
            self.camuflage = 1
            self.decals = [1,
             1,
             1,
             1,
             1,
             (1, 1),
             1,
             1,
             1,
             1]
            self.partStates = {}
            self.fullLoading = False

    def __init__(self):
        self.__planeID = -1
        self.__spaceId = None
        self.__waitCallback = None
        self.__loadingStatus = 0.0
        self.__destroyFunc = None
        self.__spaceMappingId = None
        self.__onLoadedCallback = None
        self.__modelManipulator = None
        self.__shellController = None
        self.__vehicleInfo = None
        self.__weaponController = None
        self.__turretController = None
        self.__mainModel = None
        self.__compoundId = -1
        self.__loadingCounter = 0
        self.__hangarCfg = None
        self.__hpHangerName = None
        self.__hpHangarPos = None
        self.__settings = None
        self.__needCameraReset = True
        self.__debugOverrides = dict()
        self.__dummyDebugAvatar = None
        self.__dbgHangarFlyingMode = False
        self.__camTergetMatrix = Math.Matrix()
        self.__hangarCamera = HangarCamera()
        self.__cbDrawCinematic = None
        self.__spaceName = None
        self.__hangarVehicleScenarioController = None
        self.__vsePlansStarted = False
        self.__turretName = ''
        return

    @property
    def hangarCamera(self):
        return self.__hangarCamera

    @property
    def camTergetMatrix(self):
        return self.__camTergetMatrix

    @property
    def spaceName(self):
        return self.__spaceName

    @property
    def vsePlansStarted(self):
        return self.__vsePlansStarted

    def create(self, hangarConfig, onSpaceLoadedCallback = None, overrideSpace = None):
        LOG_TRACE('ClientHangarSpace:: create', hangarConfig, onSpaceLoadedCallback, overrideSpace)
        self.__vsePlansStarted = False
        self.__needCameraReset = True
        self.__spaceId = BigWorld.createSpace()
        self.__hangarCamera.createCamera(self.__spaceId)
        self.__hangarConfig = hangarConfig
        self.__selectHangarType(self.__settings.airplane.visualSettings.hangarConfig if self.__settings else ClientHangarSpace.AMPTY_HANGAR_SIZE)
        self.__spaceName = self.__hangarCfg.space_name
        if overrideSpace:
            self.__spaceName = overrideSpace
        self.__spaceName = self.__spaceName[self.__spaceName.rfind('/') + 1:]
        self.__scriptsObj = getHangarScriptsByName(self.__spaceName)
        import BWPersonality
        if not BWPersonality.g_settings.hangarSpaceSettings['spaceID']:
            BWPersonality.g_settings.hangarSpaceSettings['spaceID'] = self.__spaceName
        self.__onLoadedCallback = onSpaceLoadedCallback
        try:
            self.__spaceMappingId = BigWorld.addSpaceGeometryMapping(self.__spaceId, None, 'spaces/{0}'.format(self.__spaceName))
        except:
            LOG_CURRENT_EXCEPTION()

        self.__waitCallback = BigWorld.callback(0.1, self.__waitLoadingSpace)
        self.__createDebugLabel()
        if self.__hangarCfg.static_rotor:
            self.__initialAngleL = 0
            self.__initialAngleR = 0
        else:
            seed()
            self.__initialAngleL = randrange(0, 360) / 180.0 * math.pi
            self.__initialAngleR = randrange(0, 360) / 180.0 * math.pi
        isPremium = hangarConfig != 'basic'
        LOG_DEBUG_DEV('play music', overrideSpace if overrideSpace else self.__hangarCfg.space_name)
        GameSound().music.playHangar(isPremium, overrideSpace if overrideSpace else self.__hangarCfg.space_name)
        return

    def __debug_drawKeytimes(self, model, kt, lineColor, nodeColor):
        if not kt:
            return
        hpHangar = self.__modelManipulator.getNodeMatrix(self.__hpHangerName)
        hangarTransform = Math.Matrix()
        if hpHangar:
            hangarTransform = Math.Matrix(hpHangar)
            hangarTransform.invert()
            hangarScale = Math.Matrix()
            hangarScale.setScale((self.__hangarCfg.v_scale, self.__hangarCfg.v_scale, self.__hangarCfg.v_scale))
            hangarTransform.postMultiply(hangarScale)
        mat = Math.Matrix()
        mat.setTranslate(self.__hangarCfg.cam_start_target_pos)
        rmp = self.getModelManipulator().getMatrixProvider()
        m = Math.Matrix(hpHangar)
        m.postMultiply(rmp)
        nodeKeytimes = []
        for keytime in kt:
            try:
                from clientConsts import NODE_TIMELINE_NODE_FLAGS
                from clientConsts import NODE_TIMELINE_NEAREST_NODE
                flags = NODE_TIMELINE_NODE_FLAGS.NONE
                try:
                    if hasattr(keytime, 'node'):
                        nodePos = model.node(keytime.node).nodeLocalTransform.applyToOrigin()
                        nodePos *= self.__hangarCfg.v_scale
                    else:
                        nodePos = keytime.position * self.__hangarCfg.v_scale
                    offs = self.__hangarCfg.v_start_pos
                    vec = nodePos + offs
                    mat1 = Math.Matrix()
                    mat1.setTranslate(vec)
                    BigWorld.addPoint('cinematicPath', mat1, nodeColor)
                    coord = vec
                except Exception as e:
                    return

                fadeinTime = keytime.fadeinTime if hasattr(keytime, 'fadeinTime') else 0.0
                fadeoutTime = keytime.fadeoutTime if hasattr(keytime, 'fadeoutTime') else 0.0
                nodeKeytimes.append((keytime.time,
                 coord,
                 flags,
                 keytime.type,
                 keytime.duration,
                 fadeinTime,
                 fadeoutTime))
            except:
                LOG_CURRENT_EXCEPTION()
                continue

        for kfIdx in range(1, len(nodeKeytimes)):
            pt1 = nodeKeytimes[kfIdx - 1][1]
            pt2 = nodeKeytimes[kfIdx][1]
            BigWorld.addDrawLine('cinematicPath', pt1, pt2, lineColor)

    def onSpaceLoaded(self):
        if not BigWorld.is_outside_hangar():
            BigWorld.addEffectRemap('shaders/hammer/aircraft_lod0.fx', 'shaders/hammer/aircraft_hangar.fx')
            BigWorld.addEffectRemap('shaders/hammer/aircraft_lod0_skinned.fx', 'shaders/hammer/aircraft_hangar_skinned.fx')
            BigWorld.addEffectRemap('shaders/hammer/aircraft_damaged_lod0.fx', 'shaders/hammer/aircraft_damaged_hangar.fx')
            BigWorld.addEffectRemap('shaders/hammer/aircraft_damaged_lod0_skinned.fx', 'shaders/hammer/aircraft_damaged_hangar.fx')
            BigWorld.addEffectRemap('shaders/std_effects/normalmap_specmap_alpha.fx', 'shaders/hammer/normalspec_mulitilight_alpha.fx')
            BigWorld.addEffectRemap('shaders/hammer/aircraft_glass_alpha.fx', 'shaders/hammer/aircraft_glass_hangar.fx')
            BigWorld.addEffectRemap('shaders/hammer/aircraft_glass_alpha_skinned.fx', 'shaders/hammer/aircraft_glass_hangar_skinned.fx')
            BigWorld.addEffectRemap('shaders/hammer/aircraft_object.fx', 'shaders/hammer/aircraft_object_hangar.fx')
            BigWorld.addEffectRemap('shaders/hammer/aircraft_internal.fx', 'shaders/hammer/aircraft_internal_hangar.fx')
            BigWorld.addEffectRemap('shaders/hammer/aircraft_internal_skinned.fx', 'shaders/hammer/aircraft_internal_hangar_skinned.fx')
            BigWorld.addEffectRemap('shaders/hammer/aircraft_mesh_propeller.fx', 'shaders/hammer/aircraft_mesh_propeller_hangar.fx')
        else:
            BigWorld.addEffectRemap('shaders/hammer/aircraft_mesh_propeller.fx', 'shaders/hammer/aircraft_mesh_propeller_hangar_open.fx')

    def __createDebugLabel(self):
        if DB_AIRCRAFT_CHECK:
            self.__debugLabel = gui.GUIHelper.createTextLabel((0.2, 0.0, 1), '')
            self.__debugLabel.multiline = True
            self.__debugLabel.colourFormatting = True
            GUI.addRoot(self.__debugLabel)

    def __updateDebugLabel(self, vehicleInfo):
        if DB_AIRCRAFT_CHECK:
            text = ''
            if vehicleInfo:
                text = '\\cFFFFFFFF;Debug airplane data:\n'
                text += 'Parts: ' + str(convertArray2Dictionary(vehicleInfo.partTypes)) + '\n'
                text += 'Weapons: ' + str(dict(vehicleInfo.weapons.getInstalledWeaponsList())) + '\n'
                text += 'Errors:'
                text += '\\cFF0000FF;' + db.DBLogic.g_instance.getAircraftData(vehicleInfo.planeID).check()
            self.__debugLabel.text = text

    def __delDebugLabel(self):
        if DB_AIRCRAFT_CHECK:
            GUI.delRoot(self.__debugLabel)

    def setShootingEnable(self, enable):
        if self.__dummyDebugAvatar is None:
            self.__dummyDebugAvatar = HangarShootingAvatar(self, self.__planeID)
        if self.__weaponController:
            self.__weaponController.setOwner(self.__dummyDebugAvatar)
        setArmamentStates = 65535 if enable else 0
        self.__dummyDebugAvatar.setArmamentStates(setArmamentStates)
        return

    def getModelManipulator(self):
        return self.__modelManipulator

    def setPartStates(self, partStates):
        if self.__modelManipulator:
            self.__modelManipulator.updateStatesNet(partStates, True)
            debugOverrides = self.getDebugOverrides(self.__planeID, True)
            debugOverrides.partStates = partStates

    def setAxisValue(self, axisId, value):
        if self.__modelManipulator:
            self.__modelManipulator.setAxisValue(axisId, value)

    def setDecals(self, camuflageId, decals):
        if self.__modelManipulator:
            debugOverrides = self.getDebugOverrides(self.__planeID, True)
            debugOverrides.camuflage = camuflageId
            debugOverrides.decals = decals
            self.__modelManipulator.surface.setDecalsByIds(camuflageId, decals)
            self.__modelManipulator.surface.applySurfaces()

    def setCustomization(self, camouflages):
        if self.__modelManipulator:
            camouflage = camouflages[CAMOUFLAGE_GROUPS.HULL]
            camouflageID = _camouflages_data.generateID(self.__vehicleInfo.planeID, camouflage, _camouflages_data.camouflageTypeEnum.HULL)
            import BWPersonality
            inventory = BWPersonality.g_lobbyCarouselHelper.inventory
            customNationDecalID = inventory.getCamouflageNationDecalID(camouflageID)
            killDecals = (self.__vehicleInfo.decalPKills, self.__vehicleInfo.decalSKills)
            decals = [1,
             1,
             1,
             1,
             1,
             killDecals,
             camouflages[CAMOUFLAGE_GROUPS.NOSE],
             camouflages[CAMOUFLAGE_GROUPS.WINGS],
             1,
             1,
             customNationDecalID]
            self.__modelManipulator.surface.setDecalsByIds(camouflage, decals)
            self.__modelManipulator.surface.applySurfaces()

    def __getHangerPartStates(self):
        usageID = PART_STATE_IDHANGAR
        preferredState = 2 if self.__blockType & BLOCK_TYPE.NEED_REPAIR else None
        partTypes = dict(((it['key'], it['value']) for it in self.__vehicleInfo.partTypes))
        partStates = []
        for partID, partDB in self.__settings.airplane.partsSettings.getPartsList():
            partTypeDb = partDB.getPartType(partTypes[partID]) if partID in partTypes else partDB.getFirstPartType()
            partStateId = -1
            if usageID > 0:
                for partStateID, partStateData in partTypeDb.states.iteritems():
                    if partStateData.stateFlag & usageID:
                        partStateId = partStateID
                        break

            if partStateId == -1:
                if 0 < preferredState <= len(partTypeDb.states):
                    partStateId = preferredState
                else:
                    partStateId = 1
            partStates.append((partID, partStateId))

        return partStates

    def getDebugOverrides(self, aircraftId, createIfNotExist = False):
        if aircraftId in self.__debugOverrides:
            return self.__debugOverrides[aircraftId]
        elif createIfNotExist:
            self.__debugOverrides[aircraftId] = ClientHangarSpace.DebugParams()
            return self.__debugOverrides[aircraftId]
        else:
            return None

    @property
    def spaceID(self):
        return self.__spaceId

    def setStateLoadingDepth(self, depth):
        debugOverrides = self.getDebugOverrides(self.__planeID, True)
        debugOverrides.fullLoading = depth == 0

    def needReloadForDebug(self):
        return not self.getDebugOverrides(self.__planeID, True).fullLoading

    def recreateVehicle(self, vehicleInfo, loadedCallback, dbgHangarFlyingMode = False):
        LOG_TRACE('ClientHangarSpace::recreateVehicle', vehicleInfo, self.__compoundId)
        self.__loadingCounter += 1
        if self.__loadingCounter > ClientHangarSpace.CLEAR_AFTER_LOAD_TIMES:
            BigWorld.removeAllShadowEntities()
            CompoundSystem.removeAllModels()
            self.__loadingCounter = 0
        self.__vehicleInfo = vehicleInfo
        self.__updateDebugLabel(vehicleInfo)
        prevPlaneID = self.__planeID
        self.__planeID = vehicleInfo.planeID
        self.__blockType = vehicleInfo.blockType
        self.__settings = db.DBLogic.g_instance.getAircraftData(self.__planeID)
        self.__selectHangarType(self.__settings.airplane.visualSettings.hangarConfig, self.__planeID != prevPlaneID)
        partStates = {}
        partTypes = vehicleInfo.partTypes
        weaponsSlotsStates = vehicleInfo.weapons.getInstalledWeaponsList() if vehicleInfo.weapons else []
        fullLoading = False
        debugOverrides = self.getDebugOverrides(self.__planeID)
        if debugOverrides is not None:
            partStates = debugOverrides.partStates
            fullLoading = fullLoading or debugOverrides.fullLoading
        else:
            partStates = self.__getHangerPartStates()
        callback = partial(BigWorld.callback, 0.0, partial(self.__onVehicleLoaded, loadedCallback, vehicleInfo))
        self.__hpHangerName = self.__getHangarNodeName()
        self.__dbgHangarFlyingMode = dbgHangarFlyingMode
        fullLoading = fullLoading or dbgHangarFlyingMode
        turret = self.__settings.airplane.partsSettings.getPartByName('turret')
        if turret:
            if len(partStates) > 0:
                for partState in partStates:
                    if partState[0] == turret.partId:
                        upgrade = turret.upgrades.get(partState[1], None)
                        self.__turretName = upgrade.componentXml if upgrade else ''
                        break

            elif len(partTypes) > 0:
                for partType in partTypes:
                    key = partType['key']
                    val = partType['value']
                    if turret.partId == key:
                        upgrade = turret.upgrades.get(val, None)
                        self.__turretName = upgrade.componentXml if upgrade else ''
                        break

            else:
                for key, upgrade in turret.upgrades.iteritems():
                    if upgrade.componentXml:
                        self.__turretName = upgrade.componentXml
                        break

        if self.__dummyDebugAvatar is None:
            self.__dummyDebugAvatar = HangarShootingAvatar(self, self.__planeID)
        controllersData = DestructibleObjectFactory.createControllers(BigWorld.player().id, self.__settings, self.__settings.airplane, partTypes, partStates, weaponsSlotsStates, self.__dummyDebugAvatar, fullLoading, callback, turretName=self.__turretName)
        self.__dummyDebugAvatar.controllers['modelManipulator'] = controllersData['modelManipulator']
        if self.__modelManipulator:
            self.__modelManipulator.destroy()
        if self.__weaponController:
            self.__weaponController.destroy()
        if self.__shellController:
            self.__shellController.destroy()
            vehicleInfo.weapons.onChangeShellCount -= self.__onChangeShellsCount
        if self.__turretController:
            self.__turretController.destroy()
        self.__modelManipulator = controllersData['modelManipulator']
        self.__shellController = controllersData['shellController']
        self.__weaponController = controllersData['weapons']
        self.__turretController = controllersData.get('turretsLogic', None)
        self.__onChangeShellsCount()
        if self.__modelManipulator is not None:
            self.__modelManipulator.onlyDecals = True
        if self.__dummyDebugAvatar is not None:
            self.__weaponController.setOwner(self.__dummyDebugAvatar)
        self.__modelManipulator.setAxisValue(FORCE_AXIS, FORCE_AXIS_STOPPED_VALUE)
        self.__modelManipulator.setPropellorAngle(self.__initialAngleL, self.__initialAngleR)
        currentCamouflages = vehicleInfo.customization and vehicleInfo.customization.currentCamouflages or {CAMOUFLAGE_GROUPS.HULL: 0,
         CAMOUFLAGE_GROUPS.NOSE: 0,
         CAMOUFLAGE_GROUPS.WINGS: 0}
        if debugOverrides is not None:
            self.__modelManipulator.surface.setDecalsByIds(debugOverrides.camuflage, debugOverrides.decals)
        else:
            self.setCustomization(currentCamouflages)
        self.__modelManipulator.setExternalNodeNames([self.__hpHangerName])
        vehicleInfo.weapons.onChangeShellCount += self.__onChangeShellsCount
        return

    @property
    def weaponController(self):
        return self.__weaponController

    @property
    def hangarCfg(self):
        return self.__hangarCfg

    @property
    def scenarioController(self):
        return self.__hangarVehicleScenarioController

    @property
    def turretController(self):
        return self.__turretController

    @property
    def shellsCount(self):
        return self.__shellController.getShellCountersForSlots(self.__vehicleInfo.weapons.slotsShellCount)

    def __onChangeShellsCount(self):
        self.__modelManipulator.setShelsCount(self.shellsCount)

    def __getHangarNodeName(self):
        hangarLandingPart = self.__settings.airplane.visualSettings.hangarLandingPart
        hangarLandingPartDb = self.__settings.airplane.partsSettings.getPartByName(hangarLandingPart)
        if hangarLandingPartDb:
            partTypes = dict(((it['key'], it['value']) for it in self.__vehicleInfo.partTypes))
            return HANGAR_NODE + str('_%02d' % partTypes.get(hangarLandingPartDb.partId, hangarLandingPartDb.getFirstPartType().id))
        return HANGAR_NODE

    def __onVehicleLoaded(self, callBack, vehicleInfo):
        LOG_TRACE('ClientHangarSpace::__onVehicleLoaded', self.__compoundId)
        if self.__modelManipulator:
            self.removeVehicle()
            self.__mainModel = self.__modelManipulator.getRootModel()
            self.__compoundId = self.__modelManipulator.compoundID
            self.__setUpPosition()
            self.__onChangeShellsCount()
            BigWorld.addModel(self.__mainModel, self.__spaceId)
            BigWorld.addShadowEntity(self.__compoundId, False)
            BigWorld.setHangarShadow(callBack)
            self.__scriptsObj.onVehicleLoaded()
            vehicleInfo.isVehicleLoaded = True
            if not self.__vsePlansStarted:
                self.__vsePlansStarted = True
                BigWorld.startArenaScripts()
            planeBirthdayEvents.updateHangar(vehicleInfo)
            if self.__dummyDebugAvatar is not None:
                self.__dummyDebugAvatar.onLoaded()
            self.__modelManipulator.onOwnerChanged(self.__dummyDebugAvatar)
        return

    def getHangarHPPos(self):
        return self.__hpHangarPos

    def getHangarPos(self):
        return self.__hangarCfg.v_start_pos

    def __setUpPosition(self):
        hpHangar = self.__modelManipulator.getNodeMatrix(self.__hpHangerName)
        if hpHangar:
            transform = Math.Matrix(hpHangar)
            transform.invert()
            matrix = Math.Matrix()
            matrix.setScale((self.__hangarCfg.v_scale, self.__hangarCfg.v_scale, self.__hangarCfg.v_scale))
            matrix.translation = Math.Vector3(self.__hangarCfg.v_start_pos)
            transform.postMultiply(matrix)
            self.__modelManipulator.setMatrixProvider(transform)
            self.__hpHangarPos = transform.translation
            self.__showPlaneShadow(self.__hangarCfg.v_start_pos)

    def removeVehicle(self):
        LOG_TRACE('ClientHangarSpace::removeVehicle, __mainModel:', self.__mainModel, self.__compoundId)
        self.__scriptsObj.onVehicleUnloaded()
        self.__hidePlaneShadow()
        if self.__mainModel:
            BigWorld.delModel(self.__mainModel)
            self.__mainModel = None
        if self.__compoundId != -1:
            BigWorld.removeAllShadowEntities()
            CompoundSystem.changeCompoundActive(self.__compoundId, 0)
            CompoundSystem.clearCompound(self.__compoundId)
            self.__compoundId = -1
        getHangarScriptsByName('planeBirthday').onHangarUnloaded()
        return

    def destroy(self):
        if self.__vehicleInfo:
            self.__vehicleInfo.weapons.onChangeShellCount -= self.__onChangeShellsCount
            self.__vehicleInfo = None
        self.__delDebugLabel()
        if self.__dummyDebugAvatar:
            self.__dummyDebugAvatar.destroy()
            self.__dummyDebugAvatar = None
        if self.__waitCallback is not None and not self.spaceLoaded():
            self.__destroyFunc = self.__destroy
            return
        else:
            BigWorld.worldDrawEnabled(False)
            self.removeVehicle()
            if self.__modelManipulator:
                self.__modelManipulator.destroy()
                self.__modelManipulator = None
            if self.__shellController:
                self.__shellController.destroy()
                self.__shellController = None
            if self.__weaponController:
                self.__weaponController.destroy()
                self.__weaponController = None
            if self.__turretController:
                self.__turretController.destroy()
                self.__turretController = None
            CompoundSystem.removeAllModels()
            if not BigWorld.is_outside_hangar():
                BigWorld.removeEffectRemap('shaders/hammer/aircraft_lod0.fx')
                BigWorld.removeEffectRemap('shaders/hammer/aircraft_lod0_skinned.fx')
                BigWorld.removeEffectRemap('shaders/hammer/aircraft_damaged_lod0.fx')
                BigWorld.removeEffectRemap('shaders/hammer/aircraft_damaged_lod0_skinned.fx')
                BigWorld.removeEffectRemap('shaders/std_effects/normalmap_specmap_alpha.fx')
                BigWorld.removeEffectRemap('shaders/hammer/aircraft_glass_alpha.fx')
                BigWorld.removeEffectRemap('shaders/hammer/aircraft_glass_alpha_skinned.fx')
                BigWorld.removeEffectRemap('shaders/hammer/aircraft_object.fx')
                BigWorld.removeEffectRemap('shaders/hammer/aircraft_internal.fx')
                BigWorld.removeEffectRemap('shaders/hammer/aircraft_internal_skinned.fx')
                BigWorld.removeEffectRemap('shaders/hammer/aircraft_mesh_propeller.fx')
            else:
                BigWorld.removeEffectRemap('shaders/hammer/aircraft_mesh_propeller.fx')
            BigWorld.clearHangarShadow()
            self.__destroy()
            self.__hidePlaneShadow()
            BigWorld.cleanCombinedDiffuseTextures()
            return

    def handleMouseEvent(self, dx, dy, dz):
        if self.spaceLoaded():
            self.__hangarCamera.updateCameraByMouseMove(dx, dy, dz)
            return True
        else:
            return False

    def spaceLoaded(self):
        return not self.__loadingStatus < 1

    def spaceLoading(self):
        return self.__waitCallback is not None

    def __destroy(self):
        self.__vsePlansStarted = False
        BigWorld.stopArenaScripts()
        if self.__hangarVehicleScenarioController:
            self.__hangarVehicleScenarioController.destroy()
            self.__hangarVehicleScenarioController = None
        self.__hangarCamera.destroy()
        self.__loadingStatus = 0.0
        if self.__modelManipulator:
            self.__modelManipulator.destroy()
            self.__modelManipulator = None
        self.__onLoadedCallback = None
        if BigWorld.clentSpaceExists(self.__spaceId):
            if self.__spaceId is not None and self.__spaceMappingId is not None:
                BigWorld.delSpaceGeometryMapping(self.__spaceId, self.__spaceMappingId)
            if self.__spaceId is not None:
                BigWorld.clearSpace(self.__spaceId)
                BigWorld.releaseSpace(self.__spaceId)
        self.__spaceMappingId = None
        self.__spaceId = None
        GameSound().stopHangar()
        self.__scriptsObj.onHangarUnloaded()
        getHangarScriptsByName('planeBirthday').onHangarUnloaded()
        LOG_DEBUG('Hangar successfully destroyed.')
        return

    def __waitLoadingSpace(self):
        self.__waitCallback = None
        self.__loadingStatus = BigWorld.spaceLoadStatus()
        LOG_TRACE('ClientHangarSpace::__waitLoadingSpace', self.__loadingStatus)
        if self.__loadingStatus < 1:
            self.__waitCallback = BigWorld.callback(0.1, self.__waitLoadingSpace)
        else:
            if self.__onLoadedCallback is not None:
                callBack = self.__onLoadedCallback
                self.__onLoadedCallback = None
                callBack()
            if self.__destroyFunc:
                self.__destroyFunc()
                self.__destroyFunc = None
            self.__scriptsObj.onHangarLoaded()
        return

    def __selectHangarType(self, hangarSize = 'large', resetCamera = True):
        if hangarSize not in db.DBLogic.g_instance.hangarConfigList[self.__hangarConfig]:
            LOG_ERROR('Load hangar: unknown size', self.__hangarConfig, hangarSize)
            hangarSize = 'large'
        self.__hangarCfg = db.DBLogic.g_instance.hangarConfigList[self.__hangarConfig][hangarSize]
        if resetCamera or self.__needCameraReset:
            self.__hangarCamera.setupCamera(self.__hangarCfg, hangarSize if self.__needCameraReset else '')
            if self.__needCameraReset:
                self.__hangarCamera.updateStartDirection()
            if self.__vehicleInfo is not None:
                self.__needCameraReset = False
            self.__camTergetMatrix.setTranslate(self.__hangarCfg.cam_start_target_pos)
            if self.__settings:
                scenarionName = ''
                excludeEvents = []
                if self.__settings.airplane.visualSettings.hangarScenario:
                    scenarionName = self.__settings.airplane.visualSettings.hangarScenario.scenario
                    excludeEvents = self.__settings.airplane.visualSettings.hangarScenario.excludeEvents
                scenarioData = db.DBLogic.g_instance.getScenario(HANGAR_CINEMATIC_NAME + '_' + str(hangarSize) if scenarionName == '' else scenarionName)
                if scenarioData:
                    self.__hangarVehicleScenarioController = HangarVehicleCinematicHelper(self, scenarioData, excludeEvents)
                    self.__hangarVehicleScenarioController.setDefaultView(math.radians(self.__hangarCfg.cam_start_angles[0]), math.radians(self.__hangarCfg.cam_start_angles[1]))
                else:
                    LOG_TRACE('ClientHangarSpace::__selectHangarType - hangar scenario not found!')
        return

    def __hidePlaneShadow(self):
        BigWorld.set_hangar_shadow_params(0.0, 0.0, 0.0)

    def __showPlaneShadow(self, casterPos):
        BigWorld.set_hangar_shadow_params(casterPos[0], casterPos[2], SHADOW_SCALE_CFC)

    def dbgShowVehicleShadow(self, show = True):
        if not show:
            self.__hidePlaneShadow()
        elif show:
            self.__showPlaneShadow(self.__hangarCfg.v_start_pos)

    def dbgSwitchCameraView(self, camView):
        self.__hangarCamera.switchCameraView(camView)

    def dbgSetCameraAngle(self, yaw, pitch):
        self.__hangarCamera.setDirectAngle(math.radians(yaw), math.radians(pitch))

    def dbgRotateTurrets(self, command):
        if not hasattr(self, 'trcYaw') or command == '5':
            self.trcYaw = 0.0
            self.trcPitch = 0.0
        trStep = 1
        if command == '1':
            self.trcYaw += trStep
        elif command == '2':
            self.trcYaw -= trStep
        elif command == '3':
            self.trcPitch += trStep
        elif command == '4':
            self.trcPitch -= trStep
        self.trcYaw = _clampCyclic(-180, 180, self.trcYaw)
        self.trcPitch = _clampCyclic(-180, 180, self.trcPitch)
        self.yaw = math.radians(self.trcYaw)
        self.pitch = math.radians(self.trcPitch)
        LOG_DEBUG('!!!@@@ dbgRotateTurrets:', self.trcYaw, self.trcPitch)
        self.__modelManipulator.setAxisValue(TURRET_TRACKER_AXIS, {11: self,
         14: self})


def _clamp(minVal, maxVal, val):
    tmpVal = max(minVal, val)
    tmpVal = min(maxVal, tmpVal)
    return tmpVal


def _clampCyclic(minVal, maxVal, val):
    tmpVal = val
    if tmpVal < minVal:
        tmpVal = maxVal
    elif tmpVal > maxVal:
        tmpVal = minVal
    return tmpVal


def _degToRadVec3(inVec):
    outVec = Math.Vector3()
    for i in range(0, 3):
        outVec[i] = math.radians(inVec[i])

    return outVec