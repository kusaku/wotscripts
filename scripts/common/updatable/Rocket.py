# Embedded file name: scripts/common/updatable/Rocket.py
import BigWorld
from UpdatableObjectBase import *
import Math
import math
from Weapons import Weapons
from consts import *
from consts import COMPONENT_TYPE
import db.DBLogic
from EntityHelpers import EntityStates
from debug_utils import *
from TeamObject import TeamObject
from random import random
from MathExt import lerp
from UpdatableObjectSound import UpdatableObjectSound
if IS_CLIENT:
    import EffectManager
    from db.DBEffects import Effects

class RocketUpdatable(UpdatableObjectBase):
    EXPLODED_DURATION = 5
    SEND_SIGNATURE_STRING = '16sfffffffff'
    BACKUP_SIGNATURE_STRING = 'fffffffff'

    def __init__(self, owner):
        UpdatableObjectBase.__init__(self, owner)
        self.model = None
        self.__maxFlightDist = 1000.0
        self.__tickMovement = 0.0
        self.__totalMovement = 0.0
        self.__direction = None
        self.matrix = None
        self.position = Math.Vector3(0, 0, 0)
        self._startPosition = Math.Vector3(0, 0, 0)
        self._startVector = Math.Vector3(0, 0, 0)
        self._startRotation = Math.Vector3(0, 0, 0)
        self.__shellDescription = None
        self.aliveTill = 0
        self._rocketEffect = None
        self.__modifiers = Modifiers(ROCKET_SPLASH=1.0, ROCKET_DAMAGE=1.0)
        return

    def __findPartCollisionTeamObject(self, start, end):
        partsCollider = BigWorld.hm_collideParts(self._owner.spaceID, start, end, self._owner)
        if partsCollider:
            for entity, partId, position in partsCollider:
                if issubclass(entity.__class__, TeamObject):
                    return (entity, partId, position)

    def __findPartCollisionHealth(self, start, end):
        partsCollider = BigWorld.hm_collideParts(self._owner.spaceID, start, end, self._owner)
        if partsCollider:
            for entity, partId, position in partsCollider:
                if hasattr(entity, 'health') and EntityStates.inState(entity, EntityStates.GAME):
                    return (entity, partId, position)

    def __findNearestCollision(self, start, end):
        terrainCollision = BigWorld.hm_collide(self._owner.spaceID, start, end, COLLISION_TYPE_TREE, True)
        partCollision = self.__findPartCollisionTeamObject(start, end)
        if terrainCollision and partCollision:
            if start.distTo(terrainCollision[0]) < start.distTo(partCollision[2]):
                return (terrainCollision[0], terrainCollision[2])
            else:
                return (partCollision[2], None)
        else:
            if terrainCollision:
                return (terrainCollision[0], terrainCollision[2])
            if partCollision:
                return (partCollision[2], None)
        return None

    def setState(self, state, timeShift = 0.0):
        UpdatableObjectBase.setState(self, state, timeShift)
        if IS_CLIENT and self._owner:
            if self.getState() == UPDATABLE_STATE.EXPLODED:
                if self.model:
                    mesh = self.model
                    self.model = None
                    self.model = BigWorld.Model('objects/fake_model.model')
                    if self.model.motors:
                        self.model.delMotor(self.model.motors[0])
                    self.model.addMotor(BigWorld.Servo(self.matrix))
                    BigWorld.addModel(self.model)
                    self._rocketEffect.reAttachToNode(self.model.root)
                    BigWorld.delModel(mesh)
                if self._stateCB:
                    self._stateCB(UPDATABLE_STATE_CB.EXPLODED, self._updatableTypeId, self)
                    self._stateCB = None
                if self._rocketEffect:
                    self._rocketEffect.stopEmission()
                position = self.position
                materialName = None
                nearestCollision = self.__findNearestCollision(self.position - self._startVector * 2, self.position + self._startVector * 2)
                if nearestCollision:
                    position, matId = nearestCollision
                    if matId != None:
                        materialName = db.DBLogic.g_instance.getMaterialName(matId)
                explosionParticle = self.__shellDescription.explosionParticles.water if materialName == 'water' else self.__shellDescription.explosionParticles.default
                EffectManager.g_instance.createWorldEffect(Effects.getEffectId(explosionParticle), position, {})
                if self._owner == BigWorld.player():
                    BigWorld.player().eOwnShellExplosion(position, self.__shellDescription)
            elif self.getState() == UPDATABLE_STATE.DESTROY:
                self.destroy()
            elif self.getState() == UPDATABLE_STATE.CREATE:
                if self.model:
                    self.model.visible = True
        return

    def destroy(self):
        if self._stateCB:
            self._stateCB = None
        UpdatableObjectBase.destroy(self)
        if self.model:
            BigWorld.delModel(self.model)
            self.model = None
        return

    def backup(self):
        bp = UpdatableObjectBase.backup(self)
        sendList = self._startPosition.list() + self._startVector.list() + self._startRotation.list()
        add = pack(RocketUpdatable.BACKUP_SIGNATURE_STRING, *sendList)
        bp.append(add)
        bp.append(self.position)
        bp.append(self.__maxFlightDist)
        bp.append(self.aliveTill)
        bp.append(self.__modifiers.ROCKET_SPLASH)
        bp.append(self.__modifiers.ROCKET_DAMAGE)
        return bp

    def restore(self, data):
        self.__modifiers.ROCKET_DAMAGE = data.pop()
        self.__modifiers.ROCKET_SPLASH = data.pop()
        self.aliveTill = data.pop()
        self.__maxFlightDist = data.pop()
        self.position = data.pop()
        rocketData = data.pop()
        rocketData = unpack(RocketUpdatable.BACKUP_SIGNATURE_STRING, rocketData)
        self._startPosition.x = rocketData[0]
        self._startPosition.y = rocketData[1]
        self._startPosition.z = rocketData[2]
        self._startVector.x = rocketData[3]
        self._startVector.y = rocketData[4]
        self._startVector.z = rocketData[5]
        self._startRotation.x = rocketData[6]
        self._startRotation.y = rocketData[7]
        self._startRotation.z = rocketData[8]
        UpdatableObjectBase.restore(self, data)
        self.__direction = Math.Vector3(self._startVector)
        self.__direction.normalise()
        self.__shellDescription = db.DBLogic.g_instance.getComponentByIndex(COMPONENT_TYPE.ROCKETS, self._resourceID)

    def update1sec(self):
        super(RocketUpdatable, self).update1sec()
        if self.aliveTill and BigWorld.time() >= self.aliveTill:
            self.aliveTill = 0
            self.setState(UPDATABLE_STATE.DESTROY)

    def __doExplosion(self, timeShift = 0.0):
        self.setState(UPDATABLE_STATE.EXPLODED, timeShift)
        self.aliveTill = BigWorld.time() + self.EXPLODED_DURATION
        if not IS_CLIENT:
            explosionRadius = self.__shellDescription.explosionRadius * self.__modifiers.ROCKET_SPLASH
            explosionDamage = self.__shellDescription.explosionDamage * self.__modifiers.ROCKET_DAMAGE
            Weapons.doExplosiveDamage(self._owner, self.position, explosionRadius, self.__shellDescription.explosionRadiusEffective, explosionDamage, DAMAGE_REASON.ROCKET_EXPLOSION)

    def __getPositionForTime(self, t):
        return self._startPosition + self.__direction * self.__getDistForTime(t)

    def __getDistForTime(self, t):
        startSpeed = self._startVector.length
        startAcceleration = self.__shellDescription.startAcceleration
        accelerationScale = self.__shellDescription.accelerationScale
        return (accelerationScale * (accelerationScale * startSpeed * t - startAcceleration * t) + (startAcceleration * accelerationScale * t + startAcceleration) * math.log(accelerationScale * t + 1)) / (accelerationScale * accelerationScale)

    def _positionUpdate(self):
        t = self._getCurrentTime()
        if t >= 0.0:
            curState = self.getState()
            if curState == UPDATABLE_STATE.CREATE:
                newMovement = self.__getDistForTime(t)
                self.__tickMovement = newMovement - self.__totalMovement
                self.__totalMovement = newMovement
                self.position = self._startPosition + self.__direction * self.__totalMovement
                if not IS_CLIENT:
                    r = self.__shellDescription.lockRange * self._owner.controllers['externalModifiers'].modifiers.ACTIVATE_ROCKET_DETONATOR
                    if next((e for e in self._owner.entitiesInRange(r, 'Avatar', self.position) + self._owner.entitiesInRange(r, 'AvatarBot', self.position) if EntityStates.inState(e, EntityStates.GAME) and self._owner.teamIndex != e.teamIndex), None):
                        self.__doExplosion()
                        return
                    if self.__findPartCollisionHealth(self.position - self.__direction * self.__tickMovement * 0.5, self.position + self.__direction * self.__tickMovement * 0.5):
                        self.__doExplosion()
                        return
                if self.__totalMovement >= self.__maxFlightDist:
                    normal = Math.Vector3(self._startVector)
                    normal.normalise()
                    self.position = self.__maxFlightDist * normal + self._startPosition
                    self.__doExplosion()
                    return
            if IS_CLIENT:
                self.__updatableSound.updatePosition()
        if IS_CLIENT:
            if self.model:
                self.matrix.translation = self.position
        return

    def _onBaseCreate(self, args):
        UpdatableObjectBase.setUnpackArgs(self, args[:2])
        self._startPosition = Math.Vector3(*args[2])
        self._startVector = Math.Vector3(*args[3])
        self._startRotation = Math.Vector3(*args[4])
        self.position = self._startPosition
        self.__direction = Math.Vector3(self._startVector)
        self.__direction.normalise()
        self.__shellDescription = db.DBLogic.g_instance.getComponentByIndex(COMPONENT_TYPE.ROCKETS, self._resourceID)
        norm = random()
        maxFlightTime = lerp(self.__shellDescription.minFlightTime, self.__shellDescription.maxFlightTime, norm)
        self.__maxFlightDist = self.__getDistForTime(maxFlightTime)
        nearestCollision = self.__findNearestCollision(self._startPosition, self._startPosition + self.__direction * self.__maxFlightDist)
        if nearestCollision:
            self.__maxFlightDist = (self._startPosition - nearestCollision[0]).length
        self.__modifiers.ROCKET_SPLASH = self._owner.controllers['externalModifiers'].modifiers.ROCKET_SPLASH
        self.__modifiers.ROCKET_DAMAGE = self._owner.controllers['externalModifiers'].modifiers.ROCKET_DAMAGE

    def _onCreate(self, args):
        args = unpack(RocketUpdatable.SEND_SIGNATURE_STRING, args)
        UpdatableObjectBase.setUnpackArgs(self, args[0])
        self._startPosition.x = args[1]
        self._startPosition.y = args[2]
        self._startPosition.z = args[3]
        self._startVector.x = args[4]
        self._startVector.y = args[5]
        self._startVector.z = args[6]
        self._startRotation.x = args[7]
        self._startRotation.y = args[8]
        self._startRotation.z = args[9]
        self.position = self._startPosition
        self.__direction = Math.Vector3(self._startVector)
        self.__direction.normalise()
        self.__shellDescription = db.DBLogic.g_instance.getComponentByIndex(COMPONENT_TYPE.ROCKETS, self._resourceID)
        self.__loadRocketModel()
        if IS_CLIENT:
            self.__updatableSound = UpdatableObjectSound('Rocket', self.creatorOwnerID())

    def __loadRocketModel(self):
        BigWorld.loadResourceListBG((self.__shellDescription.model,), self.__onRocketModelLoaded)

    def __onRocketModelLoaded(self, resourceRefs):
        if self._owner is not None:
            modelName = self.__shellDescription.model
            if modelName not in resourceRefs.failedIDs:
                self.model = resourceRefs[modelName]
                self.__setModel()
                if IS_CLIENT:
                    self.__updatableSound.startSound(self.__shellDescription, self.position, self.getState())
            else:
                LOG_ERROR("Can't load rocket model", modelName)
        return

    def __setModel(self):
        self.model.position = self.position
        scaleMatrix = Math.Matrix()
        scaleMatrix.setScale((AIRCRAFT_MODEL_SCALING, AIRCRAFT_MODEL_SCALING, AIRCRAFT_MODEL_SCALING))
        self.matrix = Math.Matrix()
        self.matrix.setRotateYPR((self._startVector.yaw, self._startVector.pitch, 0.0))
        self.matrix.preMultiply(scaleMatrix)
        self.matrix.translation = self.position
        servo = BigWorld.Servo(self.matrix)
        self.model.addMotor(servo)
        BigWorld.addModel(self.model)
        self.model.visible = self.getState() == UPDATABLE_STATE.CREATE
        self._rocketEffect = EffectManager.g_instance.createNodeAttachedEffect(Effects.getEffectId(self.__shellDescription.particleSmoke), self.model.node('HP_flame'), {'uniqueId': str(self._id)})
        if self._stateCB:
            self._stateCB(UPDATABLE_STATE_CB.MODEL_LOADED, self._updatableTypeId, self)

    def getCreationArgs(self):
        sendList = [UpdatableObjectBase.getPackArgs(self)]
        sendList += self._startPosition.list() + self._startVector.list() + self._startRotation.list()
        return (self._updatableTypeId, self._resourceID, pack(RocketUpdatable.SEND_SIGNATURE_STRING, *sendList))