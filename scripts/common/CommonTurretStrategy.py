# Embedded file name: scripts/common/CommonTurretStrategy.py
import BigWorld
import Math
import math
from debug_utils import *
from EntityHelpers import EntityStates, isTeamObject
from consts import HEALTH_DAMAGE_PART_ID, DAMAGE_REASON, ACTION_DEALER, TEAM_OBJECT_CLASS_NAMES

class CommonTurretStrategy(object):

    def __init__(self, owner):
        self._ownerLogic = owner
        self._ownerEntity = owner._owner
        self._ignoreList = []

    def setIgnoreTargetsList(self, ignoreList):
        self._ignoreList = ignoreList

    def setOwnerEntity(self, entity):
        self._ownerEntity = entity

    def destroy(self):
        self._ownerLogic = None
        self._ownerEntity = None
        return

    def _specConditions(self, pos):
        return True

    def _findTarget(self):
        maxDist = self._ownerLogic.targetLockDistance
        turretSettings = self._ownerLogic.settings
        rangeEntities = self._ownerLogic.getEntitiesInRange()
        aggroMax = -1
        aggroCur = -1
        newTarget = None
        curTarget = BigWorld.entities.get(self._ownerLogic.curTargetID, None)

        def distAggro(distance):
            return max(0, 1 - distance / maxDist)

        def sectorAggro(e):
            onOwnerDir = self._ownerEntity.position - e.position
            staticAggro = 0.05
            return 1 - onOwnerDir.angle(e.vector) / math.pi * (1 - staticAggro)

        def hpAggro(target):
            if target.health > 0:
                return 1 / target.health
            return 1

        aggroSwitchK = turretSettings.aggroSwitchK
        for entity in rangeEntities:
            if self._isValidTarget(entity):
                planeWeight = turretSettings.aircraftClassSettings.getDataForClassByGlobalID(entity.globalID)['aggroK']
                dist = self._ownerEntity.position.distTo(entity.position)
                aggro = planeWeight * distAggro(dist) * sectorAggro(entity)
                if self._ownerLogic.GUNNER_ENEMYHP_WATCHER:
                    aggro *= hpAggro(entity)
                    aggroSwitchK = 1.0
                if curTarget and entity.id == curTarget.id:
                    aggroCur = aggro
                if aggro <= aggroMax:
                    continue
                newTarget = entity
                aggroMax = aggro

        if curTarget and aggroCur == -1:
            curTarget = None
        if aggroMax > 0 and aggroCur <= aggroMax * aggroSwitchK:
            return newTarget
        else:
            return curTarget

    def _isValidTarget(self, target):
        return EntityStates.inState(target, EntityStates.GAME) and self._ownerEntity.teamIndex != target.teamIndex and self._ownerLogic.targetInTurretSector(target) and not BigWorld.hm_collideSimple(self._ownerEntity.spaceID, self._ownerEntity.position, target.position) and target.id not in self._ignoreList

    def processTileDamage(self, targetID, startPos, targetImaginePos, damagePerTile, aliveTurretsCount, reduction):
        settings = self._ownerLogic.settings
        tileDir = targetImaginePos - startPos
        tileDir.normalise()
        tileNextTickPos = targetImaginePos + self._ownerLogic.gunDescription.bulletSpeed * 0.1 * tileDir
        tilePrevTickPos = targetImaginePos - self._ownerLogic.gunDescription.bulletSpeed * 0.1 * tileDir
        collidedParts = BigWorld.hm_collideParts(self._ownerEntity.spaceID, tilePrevTickPos, tileNextTickPos, self._ownerEntity)
        victim = None
        victimDist = 0
        precisionK = 1.0
        if collidedParts:
            for entity, partID, position in collidedParts:
                dist = (targetImaginePos - position).length
                if not isTeamObject(entity) and (not victim or dist < victimDist):
                    victim = entity
                    victimDist = dist

        else:
            victim = BigWorld.entities.get(targetID)
            if victim:
                victimDist = (victim.position - targetImaginePos).length
                precisionK = max(1 - victimDist / self._ownerLogic.minDamageRadius, settings.minDamagePrc)
        if victim:
            planeTypeDamageK = settings.aircraftClassSettings.getDataForClassByGlobalID(victim.globalID)['damageK'] * self._ownerLogic.damageK
            damage = damagePerTile * precisionK * self._ownerLogic.TURRET_FOCUS * planeTypeDamageK * aliveTurretsCount * reduction
            if damage > 0:
                victim.receiveTurretDamage(self._ownerEntity, damage, self._ownerEntity.objTypeID, self._ownerEntity.entityGroupMask, self._ownerEntity.teamIndex, self._ownerEntity.unitNumber, settings.critAbility * self._ownerLogic.TURRET_INFLICT_CRIT, self._ownerLogic.targetSkillModsActivity)
                actionDealer = ACTION_DEALER.TURRET if self._ownerEntity.className in TEAM_OBJECT_CLASS_NAMES else ACTION_DEALER.GUNNER
                self._ownerEntity.onHitTarget([victim], DAMAGE_REASON.AA_EXPLOSION, actionDealer)
        return

    def calculateTargetImaginePos(self, targetEntity):
        return self._calculateTargetImaginePosCommon(targetEntity)

    def calculateServerTargetImaginePos(self, targetEntity):
        return self._calculateTargetImaginePosCommon(targetEntity)

    def _calculateTargetImaginePosCommon(self, targetEntity):
        oVector = self._ownerLogic.getEntityVector(self._ownerEntity)
        tVector = self._ownerLogic.getEntityVector(targetEntity)
        targetHitTime = BigWorld.collisionTime(self._ownerEntity.position, oVector, targetEntity.position, tVector, self._ownerLogic.gunDescription.bulletSpeed)
        if targetHitTime >= 0:
            return targetEntity.position + targetHitTime * tVector
        LOG_MX('Target is too fast')