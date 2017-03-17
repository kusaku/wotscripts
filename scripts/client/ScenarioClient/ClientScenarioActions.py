# Embedded file name: scripts/client/ScenarioClient/ClientScenarioActions.py
import BigWorld
import EffectManager
from db.DBEffects import Effects
import Math
import math
from debug_utils import LOG_ERROR, LOG_DEBUG
from functools import partial
from clientConsts import BULLET_PARAM, TEAMOBJECT_SIMPLIFICATION_DISTANCE, TEAMOBJECT_SIMPLIFICATION_FILTER, TURRET_TRACKER_AXIS
from consts import UPDATABLE_TYPE
import db.DBLogic
from random import random, uniform
import GameEnvironment
from EntityHelpers import isClientReadyToPlay

class Dummy:
    pass


def onBulletExplosion(effectName, end):
    EffectManager.g_instance.createWorldEffect(Effects.getEffectId(effectName), end, {})


def applyRadius(pos, actionData):
    if hasattr(actionData, 'maxRadius') and actionData.maxRadius:
        angle = random() * 2 * math.pi
        radius = uniform(actionData.minRadius if hasattr(actionData, 'minRadius') else 0, actionData.maxRadius)
        return Math.Vector3(pos.x + radius * math.cos(angle), pos.y, pos.z + radius * math.sin(angle))
    else:
        return pos


def getTerrainPointAndMaterial(spaceID, position):
    waterLevel = GameEnvironment.getClientArena().getWaterLevel()
    res = Math.Vector3(position)
    materialName = None
    heightCollide = BigWorld.hm_collideSimple(spaceID, position + Math.Vector3(0, 1500, 0), position - Math.Vector3(0, 1500, 0))
    if heightCollide is not None:
        try:
            materialName = db.DBLogic.g_instance.getMaterialName(heightCollide[1])
        except:
            pass

        res = heightCollide[0]
    if res.y < waterLevel:
        res.y = waterLevel
    return (res, materialName)


def delayedAction(fn):

    def wrapped(*args, **kw):
        if not isClientReadyToPlay():
            if hasattr(args[0], 'waitStart') and args[0].waitStart:
                ClientScenarioActions.delayedActions.append((fn, args, kw))
                LOG_DEBUG('ClientScenarioActions::delayed', fn)
            else:
                LOG_DEBUG('ClientScenarioActions::skip', fn)
        else:
            return fn(*args, **kw)

    return wrapped


class ClientScenarioActions:
    """
    Class stores client actions logic for scenarios 
    """
    gunShotRenderType = {}
    delayedActions = []

    @staticmethod
    def refreshDelayedActions():
        LOG_DEBUG('ClientScenarioActions::refreshDelayedActions', len(ClientScenarioActions.delayedActions))
        for fn, args, kw in ClientScenarioActions.delayedActions:
            fn(*args, **kw)

        ClientScenarioActions.delayedActions = []

    @staticmethod
    def triggeredEffect(actionData, environmentData):
        r"""turn on\off some triggered effect on parent destructible object"""
        modelManipulator = environmentData.destructableObject.controllers['modelManipulator']
        modelManipulator.setEffectVisible(actionData.effectName, actionData.effectVisible)

    @staticmethod
    @delayedAction
    def relativeEffect(actionData, environmentData):
        """create some effect with transformation, relative to parent destructible transformation"""
        matrix = Math.Matrix(environmentData.destructableObject.resMatrix)
        position = applyRadius(matrix.applyPoint(actionData.position), actionData)
        EffectManager.g_instance.createWorldEffect(Effects.getEffectId(actionData.effectName), position, {'rotation': actionData.rotation} if hasattr(actionData, 'rotation') else {})

    @staticmethod
    @delayedAction
    def worldEffect(actionData, environmentData):
        """create some effect with world transformation"""
        position = applyRadius(actionData.position, actionData)
        EffectManager.g_instance.createWorldEffect(Effects.getEffectId(actionData.effectName), position, {'rotation': actionData.rotation} if hasattr(actionData, 'rotation') else {})

    @staticmethod
    @delayedAction
    def attachedEffect(actionData, environmentData):
        """attach some effect to object's mountPoint"""
        modelManipulator = environmentData.destructableObject.controllers['modelManipulator']
        pathList = actionData.mountPoint.split('/')
        node = None
        partModel = 1
        if len(pathList) == 2 and pathList[0] in modelManipulator.namedParts:
            partModel = modelManipulator.namedParts[pathList[0]].getMainModel()
            if partModel:
                try:
                    node = partModel.model.node(pathList[1])
                except:
                    pass

        if node:
            EffectManager.g_instance.createNodeAttachedEffect(Effects.getEffectId(actionData.effectName), node, {})
        elif partModel:
            LOG_ERROR('ClientScenarioActions: Wrong path for scenario attachedEffect!', environmentData.destructableObject._settings.typeName, environmentData.destructableObject.scenarioName, actionData.mountPoint)
        return

    @staticmethod
    @delayedAction
    def gunShot(actionData, environmentData):
        """do shoot: """
        shotProfile = db.DBLogic.g_instance.getScenarioShotProfile(actionData.profile)
        if shotProfile:
            if shotProfile.name not in ClientScenarioActions.gunShotRenderType:
                ClientScenarioActions.gunShotRenderType[shotProfile.name] = BigWorld.registerBulletType(shotProfile.name, (shotProfile.bulletThinkness, shotProfile.bulletLen, shotProfile.bulletLenExpand), (shotProfile.smokeSizeX, shotProfile.smokeSizeY), shotProfile.smokeTillingLength, shotProfile.smokeRadiusScale, (shotProfile.bulletColour, shotProfile.smokeColour), shotProfile.textureIndex, shotProfile.passbySound)
        modelManipulator = environmentData.destructableObject.controllers['modelManipulator']
        modelManipulator.setEffectVisible(actionData.trigger, True)
        if shotProfile:
            startPos = modelManipulator.getEffectCoordinate(actionData.trigger)
            if startPos is None:
                startPos = environmentData.destructableObject.position
            endPos = applyRadius(actionData.position, actionData)
            explosionF = partial(onBulletExplosion, actionData.effectName) if actionData.effectName else None
            BigWorld.addBullet(startPos, endPos, shotProfile.bulletSpeed, 0.1, ClientScenarioActions.gunShotRenderType[shotProfile.name], BULLET_PARAM.FOREIGN, explosionF)
        return

    @staticmethod
    @delayedAction
    def ballisticShot(actionData, environmentData):

        def getStartPos(environmentData, modelManipulator):
            objPos = environmentData.destructableObject.position
            if (BigWorld.camera().position - objPos).length > TEAMOBJECT_SIMPLIFICATION_DISTANCE:
                startPos = objPos
            else:
                startPos = modelManipulator.getEffectCoordinate(actionData.trigger)
                if startPos is None or (startPos - objPos).length > TEAMOBJECT_SIMPLIFICATION_FILTER:
                    startPos = objPos
            return startPos

        def launchUpdatable(actionData, environmentData, startPos, endPos, startVector, effect):
            import updatable.UpdatableManager
            if updatable.UpdatableManager.g_instance and not environmentData.destructableObject.isDestroyed:
                modelManipulator = environmentData.destructableObject.controllers['modelManipulator']
                modelManipulator.setEffectVisible(actionData.trigger, True)
                updatable.UpdatableManager.g_instance.createUpdatableLocal(UPDATABLE_TYPE.BALLISTIC, actionData.profile, startPos, startVector, startVector, endPos, actionData.height, effect)

        def delayedLaunchUpdatable(actionData, environmentData, endPos, effect):
            if not environmentData.destructableObject.isDestroyed:
                modelManipulator = environmentData.destructableObject.controllers['modelManipulator']
                startPos = getStartPos(environmentData, modelManipulator)
                startVector = endPos - startPos
                startVector.normalise()
                import updatable.UpdatableManager
                if updatable.UpdatableManager.g_instance:
                    modelManipulator.setEffectVisible(actionData.trigger, True)
                    updatable.UpdatableManager.g_instance.createUpdatableLocal(UPDATABLE_TYPE.BALLISTIC, actionData.profile, startPos, startVector, startVector, endPos, actionData.height, effect)

        profile = db.DBLogic.g_instance.getScenarioShotBallisticProfile(actionData.profile)
        if profile:
            endPos = None
            if hasattr(actionData, 'targetName'):
                target = GameEnvironment.getClientArena().getScenarioObjectByDSName(actionData.targetName)
                if target:
                    movementStrategy = target[0].get('movementStrategy')
                    if movementStrategy and movementStrategy.matrixProvider:
                        m = Math.Matrix(movementStrategy.matrixProvider)
                        endPos = m.translation
                    else:
                        targetEntity = BigWorld.entities.get(target[2])
                        if targetEntity:
                            endPos = targetEntity.position
                        else:
                            endPos = target[1]['matrix'].applyToOrigin()
                else:
                    LOG_ERROR('ClientScenarioActions: Wrong targetName in ballisticShot:', actionData.targetName)
            elif hasattr(actionData, 'position'):
                endPos = actionData.position
            if endPos:
                modelManipulator = environmentData.destructableObject.controllers['modelManipulator']
                modelManipulator.setEffectVisible(actionData.trigger, False)
                endPos, material = getTerrainPointAndMaterial(environmentData.destructableObject.spaceID, applyRadius(endPos, actionData))
                effect = actionData.effectName if hasattr(actionData, 'effectName') else profile.explosionParticles.__dict__.get(material, profile.explosionParticles.default)
                startPos = getStartPos(environmentData, modelManipulator)
                startVector = endPos - startPos
                startVector.normalise()
                scenarioGunner = Dummy()
                scenarioGunner.yaw = startVector.yaw - environmentData.destructableObject.yaw
                scenarioGunner.pitch = math.radians(actionData.height)
                modelManipulator.setAxisValue(TURRET_TRACKER_AXIS, {actionData.trigger: scenarioGunner})
                BigWorld.callback(0.5, partial(delayedLaunchUpdatable, actionData, environmentData, endPos, effect))
        return

    @staticmethod
    def cinematic(actionData, environmentData):
        camera = GameEnvironment.getCamera()
        from CameraStates import CameraState
        if camera.getState() == CameraState.SpectatorSide:
            camera.getStateObject().updateParams(actionData)
        else:
            camera.setState(CameraState.SpectatorSide, actionData)

    def destroy(self):
        ClientScenarioActions.gunShotRenderType = {}
        ClientScenarioActions.delayedActions = []


ACTION_TABLE = {'triggeredEffect': ClientScenarioActions.triggeredEffect,
 'relativeEffect': ClientScenarioActions.relativeEffect,
 'worldEffect': ClientScenarioActions.worldEffect,
 'attachedEffect': ClientScenarioActions.attachedEffect,
 'gunShot': ClientScenarioActions.gunShot,
 'ballisticShot': ClientScenarioActions.ballisticShot}
PLAYER_CAMERA_ACTION_TABLE = {'cinematic': ClientScenarioActions.cinematic}