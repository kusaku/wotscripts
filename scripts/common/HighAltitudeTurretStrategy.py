# Embedded file name: scripts/common/HighAltitudeTurretStrategy.py
import BigWorld
import Math
import math
from CommonTurretStrategy import CommonTurretStrategy
from EntityHelpers import isTeamObject
from consts import DAMAGE_REASON, HEALTH_DAMAGE_PART_ID, ACTION_DEALER, TURRET_RATION_FOR_EXTREMUM_TARGET_ALTITUDE, IS_CLIENT
from random import random
TARGET_SPEED_K = 1.1

class HighAltitudeTurretStrategy(CommonTurretStrategy):

    def __init__(self, owner):
        super(HighAltitudeTurretStrategy, self).__init__(owner)
        if not IS_CLIENT:
            self.minTargetAltitude = self._ownerLogic.targetShootDistance * TURRET_RATION_FOR_EXTREMUM_TARGET_ALTITUDE.MIN
            self.maxTargetAltitude = self._ownerLogic.targetShootDistance * TURRET_RATION_FOR_EXTREMUM_TARGET_ALTITUDE.MAX

    def _isValidTarget(self, target):
        vDist = target.position.y - self._ownerEntity.position.y
        return self.minTargetAltitude <= vDist <= self.maxTargetAltitude and CommonTurretStrategy._isValidTarget(self, target)

    def processTileDamage(self, targetID, startPos, targetImaginePos, damagePerTile, aliveTurretsCount, reduction):
        closestParts = BigWorld.hm_closestParts(self._ownerEntity.spaceID, targetImaginePos, self._ownerLogic.explosionRadius)
        if closestParts:
            victimsMap = {}
            for victim, partID, closestPos, dist in closestParts:
                isFriendlyVictim = victim.teamIndex == self._ownerEntity.teamIndex
                if not (isFriendlyVictim or isTeamObject(victim)):
                    prevData = victimsMap.get(victim, (partID, dist))
                    if dist <= prevData[1]:
                        victimsMap[victim] = (partID, dist)

            for victim, victimData in victimsMap.items():
                partID, dist = victimData
                self.__onDamageToVictimPart(victim, dist, damagePerTile, aliveTurretsCount, reduction)

        else:
            victim = BigWorld.entities.get(targetID)
            if victim:
                self.__onDamageToVictimPart(victim, (targetImaginePos - victim.position).length, damagePerTile, aliveTurretsCount, reduction)

    def __onDamageToVictimPart(self, victim, dist, damagePerTile, aliveTurretsCount, reduction):
        settings = self._ownerLogic.settings
        planeTypeDamageK = settings.aircraftClassSettings.getDataForClassByGlobalID(victim.globalID)['damageK'] * self._ownerLogic.damageK
        distanceK = max(1.0 - dist / self._ownerLogic.explosionRadius, settings.minDamagePrc)
        damage = damagePerTile * distanceK * planeTypeDamageK * aliveTurretsCount * reduction
        if damage > 0:
            victim.receiveTurretDamage(self._ownerEntity, damage, self._ownerEntity.objTypeID, self._ownerEntity.entityGroupMask, self._ownerEntity.teamIndex, self._ownerEntity.unitNumber, settings.critAbility, self._ownerLogic.targetSkillModsActivity)
            self._ownerEntity.onHitTarget([victim], DAMAGE_REASON.AA_EXPLOSION, ACTION_DEALER.TURRET)

    def calculateTargetImaginePos(self, targetEntity):
        imaginePos = self._calculateTargetImaginePosCommon(targetEntity)
        if not imaginePos:
            return targetEntity.position
        targetDir = imaginePos - targetEntity.position
        targetDir.normalise()
        basePoint = imaginePos + targetDir * self._ownerLogic.settings.forestallingDist
        e2 = basePoint - imaginePos
        e2.normalise()
        e1 = Math.Vector3(0, 1, 0)
        e1 = e1.cross(e2)
        if e1.length == 0:
            e1 = Math.Vector3(1, 0, 0)
            e1 = e1.cross(e2)
        e1.normalise()
        randomAngle = random() * math.pi
        return basePoint + self._ownerLogic.settings.randomR * (e1 * math.cos(randomAngle) + e2 * math.sin(randomAngle))