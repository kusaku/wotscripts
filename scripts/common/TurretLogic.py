# Embedded file name: scripts/common/TurretLogic.py
import math
import BigWorld
import Math
from CommonTurretStrategy import CommonTurretStrategy
from HighAltitudeTurretStrategy import HighAltitudeTurretStrategy
from MathExt import *
from consts import SERVER_TICK_LENGTH, GUN_TYPE, IS_CLIENT, COLLISION_TYPE_WATER, TURRET_LOCK_TARGET_FROM_SHOOT_K
from AvatarControllerBase import AvatarControllerBase
from EntityHelpers import isTeamObject
import db.DBLogic
from debug_utils import LOG_ERROR
TURRET_TARGET_SEARCH_DELAY = 1.8

def getRotationAnglesOnTarget(pos, rotation, targetPos):
    ownerRotationInv = Math.Quaternion(rotation)
    ownerRotationInv.invert()
    localPos = ownerRotationInv.rotateVec(targetPos - pos)
    localPos.normalise()
    yawOnTarget = clampAngle2Pi(math.atan2(localPos.x, localPos.z))
    pitchOnTarget = math.asin(localPos.y)
    return (yawOnTarget, pitchOnTarget)


def calcDeltaAngle(curAngle, angleOnTarget):
    dAngle = angleOnTarget - curAngle
    if abs(dAngle) > math.pi:
        return dAngle - math.copysign(math.pi * 2.0, dAngle)
    else:
        return dAngle


def rotateAxisWithSpeed(var, angleOnTarget, speed, minValue, maxValue):
    speedDeltaAngle = speed * SERVER_TICK_LENGTH
    curDeltaAngle = calcDeltaAngle(var, angleOnTarget)
    if speedDeltaAngle > abs(curDeltaAngle):
        var = angleOnTarget
    else:
        var += math.copysign(speedDeltaAngle, curDeltaAngle)
    var = clampAngle2Pi(var)
    if var < minValue:
        var = minValue
    elif var > maxValue:
        var = maxValue
    return var


def rotateAxisWithSpeedEx(var, angleOnTarget, speed, minValue, maxValue):
    speedDeltaAngle = speed * SERVER_TICK_LENGTH
    curDeltaAngle = calcDeltaAngle(var, angleOnTarget)
    if speedDeltaAngle > abs(curDeltaAngle):
        var = angleOnTarget
    else:
        var += math.copysign(speedDeltaAngle, curDeltaAngle)
    if var < minValue:
        var = minValue
    elif var > maxValue:
        var = maxValue
    return var


class TurretLogicBase(AvatarControllerBase):

    @staticmethod
    def isHighAltitudeTurret(turretEntityData):
        turretSettings = db.DBLogic.g_instance.getTurretData(turretEntityData.turretName)
        if not turretSettings:
            return False
        elif hasattr(turretSettings, 'gunName'):
            gunDescription = db.DBLogic.g_instance.getGunData(turretSettings.gunName)
            return gunDescription.weaponType == GUN_TYPE.AA
        else:
            LOG_ERROR('FIX!!! Turret do not have gunName!', turretEntityData.turretName)
            return False

    def __init__(self, owner, gunnersParts, turretName):
        """
        @param owner: owner entity of Avatar or TeamObject class
        @param turretSettings:
        @param gunnersParts: {partID: partTypeData}
        """
        AvatarControllerBase.__init__(self, owner)
        turretSettings = db.DBLogic.g_instance.getTurretData(turretName)
        if not turretSettings:
            self._onInvalidSettings('object has invalid turretName: %s' % turretName)
        self.settings = turretSettings
        if hasattr(turretSettings, 'gunName'):
            self.gunDescription = db.DBLogic.g_instance.getGunData(turretSettings.gunName)
        else:
            self.gunDescription = None
            LOG_ERROR('FIX!!! Turret do not have gunName!', turretName)
        if not self.gunDescription:
            self._onInvalidSettings('object has invalid gunName: %s' % turretSettings.gunName)
        if gunnersParts:
            self._initParts(gunnersParts)
        else:
            self._onInvalidSettings('object has no Gunner parts')
        self._makeLocalProperties()
        if self.gunDescription.weaponType == GUN_TYPE.AA:
            self._strategy = HighAltitudeTurretStrategy(self)
        else:
            self._strategy = CommonTurretStrategy(self)
        self.TURRET_FOCUS = 1.0
        self.TURRET_INFLICT_CRIT = 1.0
        self.GUNNER_ENEMYHP_WATCHER = False
        return

    def destroy(self):
        self._strategy.destroy()
        AvatarControllerBase.destroy(self)

    def _onInvalidSettings(self, message):
        if self._owner:
            if isTeamObject(self._owner):
                if IS_CLIENT:
                    arenaSettings = db.DBLogic.g_instance.getArenaData(BigWorld.player().arenaType)
                else:
                    arenaSettings = db.DBLogic.g_instance.getArenaData(self._owner.arenaType)
                objData = arenaSettings.getTeamObjectData(self._owner.arenaObjID)
                LOG_ERROR('TeamObject', message, objData['guid'])
            else:
                LOG_ERROR('Avatar', message, self._owner.globalID)
        else:
            LOG_ERROR(message)

    def _initParts(self, gunnersParts):
        pass

    @property
    def battleLevel(self):
        return 0

    @property
    def targetSkillModsActivity(self):
        return 0

    def _makeLocalProperties(self):
        self._battleSettings = self.settings.battleLevelsSettingsTurrets.getDataForLevel(self.battleLevel)
        self.targetLockDistance = self.settings.targetLockShootDistance * self._battleSettings.get('targetLockShootDistanceK', 0) * TURRET_LOCK_TARGET_FROM_SHOOT_K
        self.targetShootDistance = self.settings.targetLockShootDistance * self._battleSettings.get('targetLockShootDistanceK', 0)
        self.targetLostDistance = self.settings.targetLostDistance * self._battleSettings.get('targetLostDistanceK', 0)

    def restart(self):
        self._makeLocalProperties()

    @property
    def curTargetID(self):
        return self._owner.turretTargetID

    def setCurTarget(self, curEntity):
        prevTargetID = self._owner.turretTargetID
        self._owner.turretTargetID = curEntity.id if curEntity else -1
        if prevTargetID != self._owner.turretTargetID:
            self._onTargetChanged()

    def _getTurretRangeModifier(self):
        return 1.0

    def _onTargetChanged(self):
        pass

    def _isPossibleToFire(self, gunPos, targetImagePos, gunYaw, gunPitch, distToTarget, yawOnTarget, pitchOnTarget):
        return distToTarget <= self.targetShootDistance * self._getTurretRangeModifier() and abs(calcDeltaAngle(gunYaw, yawOnTarget)) <= self.settings.targetShootDeltaAngle and abs(calcDeltaAngle(gunPitch, pitchOnTarget)) <= self.settings.targetShootDeltaAngle and not BigWorld.hm_collide(self._owner.spaceID, gunPos, targetImagePos, COLLISION_TYPE_WATER, True)

    def getEntityVector(self, entity):
        pass