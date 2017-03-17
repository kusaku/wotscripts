# Embedded file name: scripts/common/updatable/Bomb.py
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
from random import choice
from MathExt import sign, clamp
from UpdatableObjectSound import UpdatableObjectSound
if IS_CLIENT:
    import EffectManager
    from db.DBEffects import Effects

class Bomb(UpdatableObjectBase):
    SEND_SIGNATURE_STRING = '16sfffffffffffI'
    BACKUP_SIGNATURE_STRING = 'fffffffffff'
    CLIENT_COLLISION_EXPANDING = 5.0

    def __init__(self, owner):
        UpdatableObjectBase.__init__(self, owner)
        self.accelerationV = WORLD_SCALING * db.DBLogic.g_instance.aircrafts.environmentConstants.gravityAcceleration
        self.model = None
        self.__enemyList = []
        self.matrix = None
        self.position = Math.Vector3(0, 0, 0)
        self.prevPos = Math.Vector3(0, 0, 0)
        self.__shellDescription = None
        self.__collider = None
        self.__ownerID = 0
        self._startPosition = Math.Vector3(0, 0, 0)
        self._startVector = Math.Vector3(0, 0, 0)
        self._startRotation = Math.Vector3(0, 0, 0)
        self.__dispersionAccel = Math.Vector3(0, 0, 0)
        self.__modifiers = Modifiers(BOMB_SPLASH=1.0, BOMB_DAMAGE=1.0)
        return

    def __findPartCollisionHealth(self, start, end):
        if IS_CLIENT:
            partsCollider = BigWorld.hm_collideParts(self._owner.spaceID, start, end, None)
            if partsCollider:
                for entity, partId, position in partsCollider:
                    if hasattr(entity, 'health') and EntityStates.inState(entity, EntityStates.GAME) and entity.id != self.__ownerID:
                        return (entity, partId, position)

        else:
            partsCollider = BigWorld.hm_collideParts(self._owner.spaceID, start, end, self._owner)
            if partsCollider:
                for entity, partId, position in partsCollider:
                    if hasattr(entity, 'health') and EntityStates.inState(entity, EntityStates.GAME):
                        return (entity, partId, position)

        return

    def setState(self, state, timeShift = 0.0):
        UpdatableObjectBase.setState(self, state, timeShift)
        if IS_CLIENT and self._owner:
            curState = self.getState()
            if curState == UPDATABLE_STATE.DESTROY:
                if self._stateCB:
                    self._stateCB(UPDATABLE_STATE_CB.EXPLODED, self._updatableTypeId, self)
                    self._stateCB = None
                if IS_CLIENT:
                    self.__updatableSound.stopSound()
                self.__collider = self.__collider or self.__getClientCollision()
                explosionParticle = self.__shellDescription.explosionParticles.default
                if self.__collider:
                    self.position, materialName = self.__collider
                    if materialName == 'water':
                        explosionParticle = self.__shellDescription.explosionParticles.water
                    elif materialName == 'object':
                        explosionParticle = getattr(self.__shellDescription.explosionParticles, 'object', explosionParticle)
                else:
                    LOG_ERROR("Can't find collision for UPDATABLE_STATE.DESTROY")
                EffectManager.g_instance.createWorldEffect(Effects.getEffectId(explosionParticle), self.position, {})
                if self._owner == BigWorld.player():
                    BigWorld.player().eOwnShellExplosion(self.position, self.__shellDescription)
                self.destroy()
            elif curState == UPDATABLE_STATE.CREATE:
                if self.model:
                    self.model.visible = True
            elif curState == UPDATABLE_STATE.ON_THE_GROUND:
                self.__collider = self.__getClientCollision()
                if self.__collider:
                    self.position, materialName = self.__collider
                    if materialName == 'water':
                        self.__hideModel()
                        EffectManager.g_instance.createWorldEffect(Effects.getEffectId('EFFECT_hit_water_rocket_bomb'), self.position, {})
                    elif materialName == 'object':
                        self.__hideModel()
                        EffectManager.g_instance.createWorldEffect(Effects.getEffectId('EFFECT_hit_smoke'), self.position, {})
                else:
                    LOG_ERROR("Can't find collision for UPDATABLE_STATE.ON_THE_GROUND")
                if IS_CLIENT:
                    self.__updatableSound.stopSound()
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
        sendList = self._startPosition.list() + self._startVector.list() + self._startRotation.list() + [self.__dispersionAccel.x, self.__dispersionAccel.z]
        add = pack(Bomb.BACKUP_SIGNATURE_STRING, *sendList)
        bp.append(add)
        bp.append(self.position)
        bp.append(self.__modifiers.BOMB_SPLASH)
        bp.append(self.__modifiers.BOMB_DAMAGE)
        return bp

    def restore(self, data):
        self.__modifiers.BOMB_DAMAGE = data.pop()
        self.__modifiers.BOMB_SPLASH = data.pop()
        self.position = data.pop()
        bombData = data.pop()
        bombData = unpack(Bomb.BACKUP_SIGNATURE_STRING, bombData)
        self._startPosition.x = bombData[0]
        self._startPosition.y = bombData[1]
        self._startPosition.z = bombData[2]
        self._startVector.x = bombData[3]
        self._startVector.y = bombData[4]
        self._startVector.z = bombData[5]
        self._startRotation.x = bombData[6]
        self._startRotation.y = bombData[7]
        self._startRotation.z = bombData[8]
        self.__dispersionAccel.x = bombData[9]
        self.__dispersionAccel.z = bombData[10]
        UpdatableObjectBase.restore(self, data)
        self.__shellDescription = db.DBLogic.g_instance.getComponentByIndex(COMPONENT_TYPE.BOMBS, self._resourceID)

    def __doExplosion(self, stateTimeShift = 0.0):
        self.setState(UPDATABLE_STATE.DESTROY, stateTimeShift)
        explosionRadius = self.__shellDescription.explosionRadius * self.__modifiers.BOMB_SPLASH
        explosionDamage = self.__shellDescription.explosionDamage * self.__modifiers.BOMB_DAMAGE
        Weapons.doExplosiveDamage(self._owner, self.position, explosionRadius, self.__shellDescription.explosionRadiusEffective, explosionDamage, DAMAGE_REASON.BOMB_EXPLOSION)

    def __getClientCollision(self):
        collisionTime = self._getCurrentTime()
        prevPos = self.__calcPos(max(0, collisionTime - SERVER_TICK_LENGTH * Bomb.CLIENT_COLLISION_EXPANDING))
        position = self.__calcPos(collisionTime + SERVER_TICK_LENGTH * Bomb.CLIENT_COLLISION_EXPANDING)
        terrainCollider = self.getTerrainCollider(prevPos, position)
        objCollider = self.getObjectCollider(prevPos, position)
        if terrainCollider and objCollider:
            if (self.position - terrainCollider[0]).length > (self.position - objCollider[0]).length:
                return terrainCollider
            else:
                return (objCollider[0], 'object')
        else:
            if terrainCollider:
                return terrainCollider
            if objCollider:
                return (objCollider[0], 'object')

    def getTerrainCollider(self, p1, p2):
        """
        Try to find collision with ground or water between previous and current bomb's positions
        @return:
        (collisionPosition, materialName) or
        None - when no collision
        """
        terrainCollider = BigWorld.hm_collideSimple(self._owner.spaceID, p1, p2)
        if terrainCollider:
            return (terrainCollider[0], db.DBLogic.g_instance.getMaterialName(terrainCollider[1]))
        else:
            return None

    def getObjectCollider(self, p1, p2):
        """
        Try to find collision with some game object between previous and current bomb's positions
        @return:
        (collisionPosition, entityClassName) or
        None - when no collision
        """
        partsCollider = self.__findPartCollisionHealth(p1, p2)
        if partsCollider:
            entity, partId, position = partsCollider
            return (position, entity.__class__.__name__)
        else:
            return None

    def __updateServerCollisions(self):
        terrainCollider = self.getTerrainCollider(self.prevPos, self.position)
        objCollider = self.getObjectCollider(self.prevPos, self.position)
        if terrainCollider and objCollider:
            if (self.position - terrainCollider[0]).length > (self.position - objCollider[0]).length:
                self.__onCollision(terrainCollider[0])
            else:
                self.__onCollideWithObject(objCollider)
        elif terrainCollider:
            self.__onCollision(terrainCollider[0])
        elif objCollider:
            self.__onCollideWithObject(objCollider)

    def __isAvatarClassName(self, className):
        return className in ('Avatar', 'AvatarBot')

    def __onCollideWithObject(self, collider):
        if self.__isAvatarClassName(collider[1]):
            self.position = collider[0]
            self.__doExplosion()
        else:
            self.__onCollision(collider[0])

    def __onCollision(self, pos):
        self.position = pos
        explosionTimeShift = self.__getExplosionTimeShift()
        if explosionTimeShift < 0.1:
            self.__doExplosion()
        else:
            self.setState(UPDATABLE_STATE.ON_THE_GROUND)

    def __getExplosionTimeShift(self):
        t = self._getCurrentTime()
        dt = self.__shellDescription.explosionDelay - t
        if dt > 0.1:
            return dt
        return 0.0

    def __hideModel(self):
        if self.model:
            self.model.visible = False

    def _positionUpdate(self):
        t = self._getCurrentTime()
        if t >= 0.0:
            curState = self.getState()
            if curState == UPDATABLE_STATE.CREATE:
                self.prevPos = self.position
                self.position = self.__calcPos(t)
                if IS_CLIENT:
                    if self.model:
                        self.__bombMatrixUpdate(t)
                else:
                    self.__updateServerCollisions()
            elif curState == UPDATABLE_STATE.ON_THE_GROUND and not IS_CLIENT:
                explosionTimeShift = self.__getExplosionTimeShift()
                if explosionTimeShift < 0.1:
                    self.__doExplosion()
            if IS_CLIENT:
                self.__updatableSound.updatePosition()

    def __bombMatrixUpdate(self, t):
        yaw = self._startVector.yaw + self.__startYawBombAmplitude * math.sin(BOMB_YAW_ROTATE_SPEED * t) / (1.0 + t)
        pitch = min(self._startVector.pitch + t * BOMB_PITCH_ROTATE_SPEED, 0.5 * math.pi)
        self.matrix.setRotateYPR((yaw, pitch, 0.0))
        self.matrix.preMultiply(self.__scaleMatrix)
        self.matrix.translation = self.position

    def __calcPos(self, t):
        addPosition = (self._startVector + self.__dispersionAccel * t) * (1.0 - math.exp(-AIR_RESISTANCE * t)) / AIR_RESISTANCE
        addPosition.y = self._startVector.y * t + self.accelerationV.y * t ** 2 / 2.0
        addPosition = self._startPosition + addPosition
        return addPosition

    def _onBaseCreate(self, args):
        UpdatableObjectBase.setUnpackArgs(self, args[:2])
        self._startPosition = Math.Vector3(*args[2])
        self._startVector = Math.Vector3(*args[3])
        self._startRotation = Math.Vector3(*args[4])
        self.__dispersionAccel.x = args[5]
        self.__dispersionAccel.z = args[6]
        Q = Math.Quaternion()
        Q.fromAngleAxis(self._startVector.yaw, Math.Vector3(0, 1, 0))
        self.__dispersionAccel = Q.rotateVec(self.__dispersionAccel)
        self.__shellDescription = db.DBLogic.g_instance.getComponentByIndex(COMPONENT_TYPE.BOMBS, self._resourceID)
        self.position = self._startPosition
        self.prevPos = self._startPosition
        self.__startYawBombAmplitude = math.radians(choice([-10,
         -5,
         5,
         10]))
        self.__modifiers.BOMB_SPLASH = self._owner.controllers['externalModifiers'].modifiers.BOMB_SPLASH
        self.__modifiers.BOMB_DAMAGE = self._owner.controllers['externalModifiers'].modifiers.BOMB_DAMAGE

    def _onCreate(self, args):
        args = unpack(Bomb.SEND_SIGNATURE_STRING, args)
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
        self.__dispersionAccel.x = args[10]
        self.__dispersionAccel.z = args[11]
        self.__ownerID = args[12]
        Q = Math.Quaternion()
        Q.fromAngleAxis(self._startVector.yaw, Math.Vector3(0, 1, 0))
        self.__dispersionAccel = Q.rotateVec(self.__dispersionAccel)
        self.__shellDescription = db.DBLogic.g_instance.getComponentByIndex(COMPONENT_TYPE.BOMBS, self._resourceID)
        self.position = self._startPosition
        self.prevPos = self._startPosition
        self.__startYawBombAmplitude = math.radians(choice([-10,
         -5,
         5,
         10]))
        self.__loadRocketModel()
        if IS_CLIENT:
            self.__updatableSound = UpdatableObjectSound('Bomb', self.creatorOwnerID())

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
                LOG_ERROR("Can't load bomb model", modelName)
        return

    def __setModel(self):
        self.model.position = self.position
        self.__scaleMatrix = Math.Matrix()
        self.__scaleMatrix.setScale((AIRCRAFT_MODEL_SCALING, AIRCRAFT_MODEL_SCALING, AIRCRAFT_MODEL_SCALING))
        self.matrix = Math.Matrix()
        self.matrix.setRotateYPR((self._startVector.yaw, self._startVector.pitch, 0.0))
        self.matrix.preMultiply(self.__scaleMatrix)
        servo = BigWorld.Servo(self.matrix)
        self.model.addMotor(servo)
        BigWorld.addModel(self.model)
        self.model.visible = self.getState() == UPDATABLE_STATE.CREATE
        if self._stateCB:
            self._stateCB(UPDATABLE_STATE_CB.MODEL_LOADED, self._updatableTypeId, self)

    def getCreationArgs(self):
        sendList = [UpdatableObjectBase.getPackArgs(self)]
        sendList += self._startPosition.list() + self._startVector.list() + self._startRotation.list() + [self.__dispersionAccel.x, self.__dispersionAccel.z] + [self._owner.id]
        return (self._updatableTypeId, self._resourceID, pack(Bomb.SEND_SIGNATURE_STRING, *sendList))