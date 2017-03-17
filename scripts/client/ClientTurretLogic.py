# Embedded file name: scripts/client/ClientTurretLogic.py
import BigWorld
import Math
from consts import SERVER_TICK_LENGTH, COLLISION_TYPE_TREE, COMPONENT_TYPE
from TurretLogic import TurretLogicBase, rotateAxisWithSpeed, rotateAxisWithSpeedEx, getRotationAnglesOnTarget
import db.DBLogic
from guns import AmmoBelt
from EntityHelpers import getBulletExplosionEffectFromMaterial, isTeamObject, isPlayerAvatar, isAvatar
from Event import Event, EventManager
from random import uniform

class Dummy:
    pass


class GunnerRecord(object):

    def __init__(self, partType, isAlive, yaw, pitch, ammoBelt, profile):
        self.partType = partType
        self.relativePos = partType.bboxes.getMainBBoxPosition()
        self.isAlive = isAlive
        self.yaw = yaw
        self.pitch = pitch
        self.position = Math.Vector3()
        self.rotation = Math.Quaternion()
        self.uniqueId = id(self)
        self.ammoBelt = ammoBelt
        ammoBelt.registerShotRender()
        self.gun = Dummy()
        self.gun.uniqueId = self.uniqueId
        self.gun.shellPath = profile.bulletShell if profile else ''
        self.gun.shellOutInterval = profile.shellOutInterval if profile else ''
        self.gun.shellSyncTime = 0


class ClientTurretLogic(TurretLogicBase):

    def __init__(self, owner, gunnersParts, turretName):
        TurretLogicBase.__init__(self, owner, gunnersParts, turretName)
        if owner:
            self.__setUpdateCallback()
        else:
            self.__updateCallBack = None
        self.__targetMatrix = None
        self.__isFiring = False
        self.__sound = None
        self.__soundWasStarted = False
        self._createEvents()
        return

    def _createEvents(self):
        self._eventManager = EventManager()
        self.eTurretTargetChanged = Event(self._eventManager)
        self.eGunnerStateChanged = Event(self._eventManager)
        return True

    def _initParts(self, gunnersParts):
        initYaw = (self.settings.yawMax + self.settings.yawMin) * 0.5
        initPitch = (self.settings.pitchMax + self.settings.pitchMin) * 0.5
        beltDescription = db.DBLogic.g_instance.getComponentByID(COMPONENT_TYPE.AMMOBELT, self.gunDescription.defaultBelt)
        gunProfile = db.DBLogic.g_instance.getGunProfileData(self.gunDescription.gunProfileName)
        self.__gunners = dict(((partID, GunnerRecord(data[1], data[0], initYaw, initPitch, AmmoBelt(self.gunDescription, beltDescription, self.gunDescription), gunProfile)) for partID, data in gunnersParts.items()))

    def linkSound(self, so):
        self.__sound = so

    @property
    def isFiring(self):
        return self.__isFiring

    @property
    def battleLevel(self):
        import Avatar
        if isAvatar(BigWorld.player()):
            return BigWorld.player().battleLevel
        return 0

    def _makeLocalProperties(self):
        if self._owner:
            TurretLogicBase._makeLocalProperties(self)
            self.__isFiring = False
            self.__reloadTimer = 0.0
            self.__reloadTime = 60.0 / self.gunDescription.RPM
            self.__gunProfile = db.DBLogic.g_instance.getGunProfileData(self.gunDescription.gunProfileName)

    @property
    def gunners(self):
        return self.__gunners

    def setOwner(self, owner):
        self._owner = owner
        self._strategy.setOwnerEntity(owner)
        if owner:
            self._makeLocalProperties()
            self.__setUpdateCallback()
        elif self.__updateCallBack:
            BigWorld.cancelCallback(self.__updateCallBack)
            self.__updateCallBack = None
        return

    def __setUpdateCallback(self):
        self.__updateCallBack = BigWorld.callback(SERVER_TICK_LENGTH, self.update)

    def destroy(self):
        TurretLogicBase.destroy(self)
        self._eventManager.clear()
        if self.__updateCallBack:
            BigWorld.cancelCallback(self.__updateCallBack)
            self.__updateCallBack = None
        return

    def onPartStateChanged(self, part):
        gunner = self.__gunners.get(part.partID, None)
        if gunner:
            from debug_utils import LOG_DEBUG_DEV
            LOG_DEBUG_DEV(self._owner.id, 'onGunnerStateChanged', part.partID, part.stateID)
            gunner.isAlive = part.isAlive
            self.eGunnerStateChanged(part.partID, part.isAlive)
        return

    def update(self, dt = 0):
        if not self._owner:
            return
        else:
            self.__setUpdateCallback()
            targetEntity = BigWorld.entities.get(self._owner.turretTargetID, None) if hasattr(self._owner, 'turretTargetID') else None
            playSound = False
            if targetEntity and targetEntity.inWorld:
                targetImaginePos = self._strategy.calculateTargetImaginePos(targetEntity)
            elif self.__targetMatrix is not None:
                targetImaginePos = self.__targetMatrix.translation
            else:
                targetImaginePos = None
            if targetImaginePos:
                ownerPosition = self._owner.position
                ownerRotation = Math.Quaternion()
                ownerRotation.fromEuler(self._owner.roll, self._owner.pitch, self._owner.yaw)
                for partId, gunner in self.__gunners.iteritems():
                    if gunner.isAlive:
                        gunner.position = ownerPosition + Math.Quaternion(ownerRotation).rotateVec(gunner.relativePos)
                        yawOnTarget, pitchOnTarget = getRotationAnglesOnTarget(ownerPosition, ownerRotation, targetImaginePos)
                        gunner.yaw = rotateAxisWithSpeed(gunner.yaw, yawOnTarget, self.settings.yawSpeed, self.settings.yawMin, self.settings.yawMax)
                        gunner.pitch = rotateAxisWithSpeedEx(gunner.pitch, pitchOnTarget, self.settings.pitchSpeed, self.settings.pitchMin, self.settings.pitchMax)
                        gunQuat = Math.Quaternion(ownerRotation)
                        gunQuat.normalise()
                        axisX = gunQuat.getAxisX()
                        axisY = gunQuat.getAxisY()
                        q = Math.Quaternion()
                        q.fromAngleAxis(-gunner.pitch, axisX)
                        gunQuat.mulLeft(q)
                        q.fromAngleAxis(gunner.yaw, axisY)
                        gunQuat.mulLeft(q)
                        gunner.rotation = gunQuat
                        if self.__isFiring:
                            self.__reloadTimer -= SERVER_TICK_LENGTH
                            if self.__reloadTimer <= 0.0:
                                self.__shoot(gunner, targetImaginePos)
                                playSound = True

            if playSound and self.__sound and not self.__soundWasStarted:
                self.__soundWasStarted = True
                self.__sound.play()
            return

    def onChangeFiring(self, flag):
        if self.__isFiring != flag:
            self.__isFiring = flag
            self.__reloadTimer = 0.0
            if self.__sound and not flag:
                self.__sound.stop(False)
                self.__soundWasStarted = False

    def setTargetMatrix(self, mat):
        self.__targetMatrix = mat

    def getEntityVector(self, entity):
        return getattr(entity.filter, 'vector', Math.Vector3())

    def __shoot(self, gunner, targetImaginePos):
        bulletDir = targetImaginePos - gunner.position
        dy = bulletDir.y
        bulletDir.normalise()
        bulletVelocity = self.getEntityVector(self._owner) + bulletDir * self.gunDescription.bulletSpeed
        bulletSpeed = bulletVelocity.length
        while self.__reloadTimer <= 0.0:
            data = {'gunID': self.gunDescription.index,
             'isPlayer': isPlayerAvatar(self._owner),
             'bullets': []}
            bulletTime = SERVER_TICK_LENGTH + self.__reloadTimer
            self.__reloadTimer += self.__reloadTime
            explosionEffect = getBulletExplosionEffectFromMaterial(self.__gunProfile, 'air')
            timeToLive = dy / ((bulletDir.y if bulletDir.y else 0.1) * self.gunDescription.bulletSpeed)
            if timeToLive < 0.0:
                timeToLive = self.gunDescription.bulletFlyDist / self.gunDescription.bulletSpeed
            bulletEndPos, terrainMatKind, treeEndPos = self._owner.addBulletBody(0, gunner.position, bulletVelocity, bulletTime, timeToLive, False, data)
            if terrainMatKind != -1:
                explosionEffect = getBulletExplosionEffectFromMaterial(self.__gunProfile, db.DBLogic.g_instance.getMaterialName(terrainMatKind))
            gunner.gun.shootInfo = gunner.ammoBelt.extract()
            if self.settings.flamePathes:
                for i, _ in enumerate(self.settings.flamePathes):
                    if self.checkCanShoot(gunner.gun.uniqueId + i):
                        asyncDelay = uniform(0.0, self.__gunProfile.asyncDelay)
                        actualFirePos = self.getFirePosition(gunner.gun.uniqueId + i)
                        data['bullets'].append(self._owner.addBullet(actualFirePos if actualFirePos else gunner.position, bulletEndPos, bulletSpeed, bulletTime, gunner.gun, explosionEffect, asyncDelay=asyncDelay, gunID=gunner.gun.uniqueId + i))

            else:
                asyncDelay = uniform(0.0, self.__gunProfile.asyncDelay)
                data['bullets'].append(self._owner.addBullet(gunner.position, bulletEndPos, bulletSpeed, bulletTime, gunner.gun, explosionEffect, asyncDelay=asyncDelay))
            if treeEndPos:
                data['bullets'].append(self._owner.addInvisibleBullet(gunner.position, treeEndPos, bulletSpeed, bulletTime, gunner.gun, getBulletExplosionEffectFromMaterial(self.__gunProfile, db.DBLogic.g_instance.getMaterialName(COLLISION_TYPE_TREE))))

    def checkCanShoot(self, gunId):
        if self._owner:
            if 'modelManipulator' in self._owner.controllers:
                mm = self._owner.controllers['modelManipulator']
                return mm.checkTurretCanShoot(gunId)
        return True

    def getFirePosition(self, gunId):
        if self._owner:
            if 'modelManipulator' in self._owner.controllers:
                mm = self._owner.controllers['modelManipulator']
                return mm.getTurretGunPos(gunId)
        return None

    def _onTargetChanged(self):
        self.eTurretTargetChanged(self._owner.turretTargetID) if hasattr(self._owner, 'turretTargetID') else None
        return