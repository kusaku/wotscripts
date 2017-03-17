# Embedded file name: scripts/common/Weapons.py
import BigWorld
import db.DBLogic
from random import choice, uniform, random
from EntityHelpers import EntityStates, getEntityBattleLevelProperty, getRotation, getEntityPartDataByID, isTeamObject, getBulletExplosionEffectFromMaterial, getEntityVector, isAvatar, PART_ENUM
from AvatarControllerBase import AvatarControllerBase
from db.DBEffects import Effects
from MathExt import repeatGauss, clamp
from consts import IS_CLIENT, WORLD_SCALING, LOGICAL_PART, SERVER_TICK_LENGTH, COMPONENT_TYPE, BOMB_ALLY_DAMAGE, GUN_TYPE, COLLISION_TYPE_TREE, BULLET_EFFECTIVE_DIST, DAMAGE_REASON, COLLISION_RECORDER, AUTOGIDER_ENABLED, ACTION_DEALER, AUTOGIDER_ANGLE_SCALE, FAM_PIVOT, FAM_SPEED_ETALON_MULT, FAM_CLAMP_MIN, FAM_CLAMP_MAX, BOMB_ENEMY_DAMAGE, AUTOGUIDER_SCALE_MINDIST, AUTOGUIDER_SCALE_MAXDIST, AUTOGUIDER_ANGLE_GROUND, DEAD_PILOT_ADD_DISPERSION
from guns import Guns
import Math
import math
import db.DBLogic
from db.DBEffects import Effects
from debug_utils import *
from _airplanesConfigurations_db import airplanesConfigurations
from WeaponsHelpers import normalizeVictimsPartsMap
from _skills_data import SpecializationEnum

class Weapons(AvatarControllerBase):

    def __init__(self, owner, weaponsInfo, settings, pivots, ammoBeltsMap = None):
        AvatarControllerBase.__init__(self, owner)
        self.__guns = Guns(weaponsInfo, settings.airplane.id, pivots, ammoBeltsMap)
        self.__middleBulletSpeed = self.__guns.calculateMiddleBulletSpeed()
        self.__bulletSpeedForMostLargeCaliberGroup = self.__guns.calculateBulletSpeedForMostLargeCaliberGroup()
        self.__id = id
        self.fireFlags = 0
        self.oneTickFireFlag = 0
        self.__tempQuat = Math.Quaternion()
        self.__tempVec3 = Math.Vector3()
        self.__prevControllerPosition = None
        self.__prevControllerRotation = None
        self.__storedArmament = 0
        self.__pastTime = 0.0
        if IS_CLIENT:
            self.__registerGunsRender()
            self.__updateCallBack = None
            maxGroup = max(self.__guns.groups, key=lambda g: g.gunDescription.caliber) if self.__guns.groups else None
            self.__maxCaliberGroups = [ g for g in self.__guns.groups if g.gunDescription.caliber == maxGroup.gunDescription.caliber ]
        if IS_CLIENT:
            self.__so = {}
            self.__playingSounds = set()
        self.setOwner(owner)
        self.__isPilotDead = False
        return

    @property
    def maxCaliber(self):
        if self.__maxCaliberGroups:
            return self.__maxCaliberGroups[0].gunDescription.caliber
        return 0

    @property
    def guns(self):
        return self.__guns

    def onPartStateChanged(self, part):
        self.onPartsStateChanged([part])

    def onPartsStateChanged(self, parts):
        for part in parts:
            if part.enumName == PART_ENUM.PILOT:
                self.__isPilotDead = not part.isAlive
                break

    def onExtModifiersChanged(self, modifiers):
        if self._owner.armamentFreeUse != (modifiers.FREE_GUNS_FIRING != 1):
            self._owner.armamentFreeUse = modifiers.FREE_GUNS_FIRING != 1
            self.onArmamentFreeUseChanged(self._owner.armamentFreeUse)

    def onArmamentFreeUseChanged(self, flag):
        for i, group in enumerate(self.__guns.groups):
            group.onArmamentFreeUseChanged(flag)

    def setOwner(self, owner):
        AvatarControllerBase.setOwner(self, owner)
        self.__pastTime = 0.0
        self.__isMainEntityAvatar = False if not owner else isAvatar(owner)
        if IS_CLIENT:
            if owner:
                self.__isPlayer = self._owner.isPlayer()
                self.__isOwnerAvatar = not isTeamObject(owner)
                self.__initClientUpdateCallBack()
            elif self.__updateCallBack:
                BigWorld.cancelCallback(self.__updateCallBack)
                self.__updateCallBack = None
        return

    def destroy(self):
        if IS_CLIENT:
            self.__maxCaliberGroups = None
            if self.__updateCallBack:
                BigWorld.cancelCallback(self.__updateCallBack)
                self.__updateCallBack = None
        self.__guns.destroy()
        AvatarControllerBase.destroy(self)
        return

    def stopFiring(self):
        self.oneTickFireFlag = 0
        self.changeFireFlags(0)

    def changeFireFlags(self, flag):
        if flag == 0:
            self._owner.lastFireTime = BigWorld.time()
        else:
            self._owner.lastFireTime = 0
        self.fireFlags = flag
        self.oneTickFireFlag |= flag

    def restart(self):
        self.__guns.restart()
        self.stopFiring()

    def __getGunID(self, bullet):
        return bullet[2].gunID

    def backup(self):
        return {'guns': self.__guns.backup(),
         'fireFlags': self.fireFlags,
         'storedArmament': self.__storedArmament}

    def restore(self, backupContainer):
        self.__guns.restoreFromBackup(backupContainer['guns'])
        self.fireFlags = backupContainer['fireFlags']
        self.__storedArmament = backupContainer['storedArmament']

    def getUsedGunsMask(self):
        """
        get used guns
        @return: {gunName: wasUsed}
        """
        return dict(((group.gunName, self.__storedArmament & 1 << i != 0) for i, group in enumerate(self.__guns.groups)))

    def getGunNames(self):
        return [ group.gunName for group in self.__guns.groups ]

    def update(self, dt):
        if EntityStates.inState(self._owner, EntityStates.GAME):
            if not self.__prevControllerPosition:
                self.__prevControllerPosition = Math.Vector3(self._owner.getShootingControllerPosition())
                self.__prevControllerRotation = Math.Quaternion(self._owner.getShootingControllerRotation())
            armaments = self.__guns.cellUpdate(dt, self.oneTickFireFlag | self.fireFlags)
            if COLLISION_RECORDER:
                self._owner.markPosition(0, self.__prevControllerPosition, self._owner.syncedRandom.getInfo())
            if armaments != 0:
                if armaments != self._owner.armamentStates:
                    self._owner.shootingSync = self._owner.syncedRandom.refresh()
                    self.syncGunsRandom()
                self._owner.onDisclosure()
                self.__storedArmament |= armaments
                readyGroups = self.__guns.shoot(armaments)
                if readyGroups:
                    self.__shootCell(dt, readyGroups)
            self.oneTickFireFlag = 0
            if armaments != self._owner.armamentStates:
                if self._owner.armamentStates:
                    self._owner.syncGunsWithClient(self.__guns.getSyncData())
                self._owner.armamentStates = armaments
            self.__prevControllerPosition = Math.Vector3(self._owner.getShootingControllerPosition())
            if COLLISION_RECORDER:
                self._owner.markPosition(1, self.__prevControllerPosition, self._owner.syncedRandom.getInfo())
            self.__prevControllerRotation = Math.Quaternion(self._owner.getShootingControllerRotation())

    def syncGunsRandom(self):
        for group in self.__guns.groups:
            group.syncedRandom.state = self._owner.syncedRandom.randint(0, 65535)

    def __calcGunShootData(self, historyLayer, group, gun, gd, shootPosition, shootOrientation, bulletTime, ownVelocity):
        bulletStartPos = shootPosition + shootOrientation.rotateVec(gun.posDelta)
        rnd = group.syncedRandom.random()
        externalModifiers = self._owner.controllers.get('externalModifiers', None) if hasattr(self._owner, 'controllers') else None
        autoAim = externalModifiers.modifiers.AUTO_AIM if externalModifiers else 1
        if AUTOGIDER_ENABLED and autoAim:
            aimAxis, aimAngle, entityId = self._owner.autoAim(historyLayer, bulletStartPos, ownVelocity, shootOrientation.rotateVec(gun.reductionDir), gd.bulletSpeed, gd.bulletFlyDist, bulletTime)
            entity = BigWorld.entities.get(entityId)
            if entity:
                autogiuderAngle = AUTOGUIDER_ANGLE_GROUND if isTeamObject(entity) else group.autoguiderAngle
                dist = (self._owner.position - entity.position).length
                norm = min(dist / gd.bulletFlyDist, 1.0)
                k = AUTOGUIDER_SCALE_MINDIST * (1 - norm) + AUTOGUIDER_SCALE_MAXDIST * norm
                autoAimAngleMod = externalModifiers.modifiers.AUTOAIM_ANGLE if externalModifiers else 1
                if aimAngle <= k * autogiuderAngle * autoAimAngleMod:
                    minAngle = aimAngle * math.pow(rnd, 2.0) * AUTOGIDER_ANGLE_SCALE
                    self.__tempQuat.fromAngleAxis(minAngle, aimAxis)
                    shootOrientation = self.__tempQuat.mul(shootOrientation)
        axisRnd, powRnd = group.syncedRandom.random(), group.syncedRandom.random()
        shootDirection = self.__calculateBulletDir(shootOrientation, group, gun, axisRnd, powRnd)
        bulletMinFlightDist = self._owner.settings.airplane.flightModel.weaponOptions.bulletMinFlightDist
        distDispersion = bulletMinFlightDist + (1 - bulletMinFlightDist) * rnd
        return (bulletStartPos,
         ownVelocity + shootDirection * gd.bulletSpeed,
         gd.bulletFlyDist * distDispersion / gd.bulletSpeed,
         axisRnd,
         powRnd)

    def __grid(self, a, base):
        if a > 0:
            ab = a / base
            c = int(ab)
            return c + int(ab - c - 1)
        return int(a / base) - 1

    def __shootCell(self, dt, weaponGroups):
        controllerRotation = self._owner.getShootingControllerRotation()
        shootOrientation = Math.Quaternion()
        firedBulletCount = 0
        modsActivity = self._owner.getTargetSkillModsActivity(SpecializationEnum.PILOT)
        for group in weaponGroups:
            gd = group.gunDescription
            while group.isReady():
                shootTime = group.shoot(dt) - self._owner.fmTimeOffset
                historyLayer = -(self.__grid(shootTime, dt) + 1)
                if historyLayer < 0 or historyLayer > 31:
                    prev, current = self.__prevControllerPosition, self._owner.getShootingControllerPosition()
                    if historyLayer < -1 or historyLayer > 31:
                        LOG_ERROR('Wrong history: dt = {0}, shootTime = {1}, historyLayer = {2}, fmTimeOffset = {3}'.format(dt, shootTime, historyLayer, self._owner.fmTimeOffset))
                        shootTime += self._owner.fmTimeOffset
                        historyLayer = -1
                else:
                    prev, current = self._owner.historyPosition(historyLayer)
                ownVelocity = (current - prev) / dt
                shootTime += (historyLayer + 1) * dt
                shootPosition = (current - prev) * shootTime / dt + prev
                if COLLISION_RECORDER:
                    self._owner.markPosition(2, shootPosition, 'shootTime = {0}\nbulletFlyDist = {1}\nbulletSpeed = {2}\n{3}'.format(shootTime, gd.bulletFlyDist, gd.bulletSpeed, group.syncedRandom.getInfo()))
                shootOrientation.slerp(self.__prevControllerRotation, controllerRotation, shootTime / dt)
                bulletTime = dt - shootTime
                for gun in group.guns:
                    bulletStartPos, bulletVelocity, timeToLive, axisRnd, powRnd = self.__calcGunShootData(historyLayer + 1, group, gun, gd, shootPosition, shootOrientation, bulletTime, ownVelocity)
                    firedBulletCount += 1
                    self._owner.addBulletBody(historyLayer + 1, bulletStartPos, bulletVelocity, bulletTime, timeToLive, gd.weaponType == GUN_TYPE.AA or gd.weaponType == GUN_TYPE.AA_NORMAL, {'ammoID': group.shootInfo.index,
                     'gunID': gd.index,
                     'shooterID': self._owner.id,
                     'modsActivity': modsActivity})

        if self.__isMainEntityAvatar:
            self._owner.p['statsCollector'].onShot(ACTION_DEALER.PILOT, firedBulletCount)

    def __shootClient(self, dt, weaponGroups):
        controllerPosition = self._owner.getShootingControllerPosition()
        controllerRotation = self._owner.getShootingControllerRotation()
        ownVelocity = (controllerPosition - self.__prevControllerPosition) / dt
        shootOrientation = Math.Quaternion()
        sounds = set()
        for group in weaponGroups:
            gd = group.gunDescription
            weaponSoundID = group.gunProfile.sounds.weaponSoundID
            sounds.add(weaponSoundID)
            while group.isReady():
                shootSyncTime = group.shoot(dt)
                if group.gunProfile.clientSkipBulletCount == 0 or group.clientProcessedBulletCount % group.gunProfile.clientSkipBulletCount == 0:
                    if COLLISION_RECORDER:
                        shootPosition = (controllerPosition - self.__prevControllerPosition) * shootSyncTime / dt + self.__prevControllerPosition
                        self._owner.markPosition(2, shootPosition, 'shootTime = {0}\nbulletFlyDist = {1}\nbulletSpeed = {2}\n{3}'.format(shootSyncTime, gd.bulletFlyDist, gd.bulletSpeed, group.syncedRandom.getInfo()))
                    for gun in group.guns:
                        asyncDelay = uniform(0.0, group.gunProfile.asyncDelay)
                        shootTime = shootSyncTime - asyncDelay
                        shootOrientation.slerp(self.__prevControllerRotation, controllerRotation, shootTime / dt)
                        bulletTime = dt - shootTime
                        shootPosition = (controllerPosition - self.__prevControllerPosition) * shootTime / dt + self.__prevControllerPosition
                        bulletStartPos, bulletVelocity, timeToLive, axisRnd, powRnd = self.__calcGunShootData(0, group, gun, gd, shootPosition, shootOrientation, bulletTime, ownVelocity)
                        data = {'gunID': gd.index,
                         'isPlayer': self.__isPlayer}
                        bulletEndPos, terrainMatKind, treeEndPos = self._owner.addBulletBody(0, bulletStartPos, bulletVelocity, bulletTime, timeToLive, False, data)
                        explosionEffect = terrainMatKind != -1 and getBulletExplosionEffectFromMaterial(group.gunProfile, db.DBLogic.g_instance.getMaterialName(terrainMatKind)) or None
                        bulletSpeed = bulletVelocity.length
                        gun.shootInfo = group.shootInfo
                        actualPosition = controllerPosition + controllerRotation.rotateVec(gun.posDelta)
                        actualDirection = self.__calculateBulletDir(controllerRotation, group, gun, axisRnd, powRnd)
                        if treeEndPos:
                            data['bullets'] = [self._owner.addBullet(bulletStartPos, bulletEndPos, bulletSpeed, bulletTime, gun, explosionEffect, asyncDelay, actualPosition, actualDirection), self._owner.addInvisibleBullet(bulletStartPos, treeEndPos, bulletSpeed, bulletTime, group, getBulletExplosionEffectFromMaterial(group.gunProfile, db.DBLogic.g_instance.getMaterialName(COLLISION_TYPE_TREE)))]
                        else:
                            data['bullets'] = [self._owner.addBullet(bulletStartPos, bulletEndPos, bulletSpeed, bulletTime, gun, explosionEffect, asyncDelay, actualPosition, actualDirection)]

                group.clientProcessedBulletCount += 1

        self.__playShootingSounds(sounds)
        return

    def getSyncData(self):
        return self.__guns.getSyncData()

    @staticmethod
    def doExplosiveDamage(owner, bulletPos, explosionRadius, explosionRadiusEffective, explosionDamage, damageReason = DAMAGE_REASON.COMMON_EXPLOSION):
        try:
            spaceID = owner.spaceID
        except:
            return

        closestParts = BigWorld.hm_closestParts(spaceID, bulletPos, explosionRadius)
        if not closestParts:
            return
        victimsMap = {}
        for victim, partId, closestPos, dist in closestParts:
            isFriendlyVictim = victim.teamIndex == owner.teamIndex
            if not (isFriendlyVictim and isTeamObject(victim)):
                victimParts = victimsMap.get(victim, [])
                if not victimParts:
                    victimsMap[victim] = victimParts
                victimParts.append((partId, dist))

        normalizeVictimsPartsMap(victimsMap)
        for victim, victimParts in victimsMap.items():
            victimData = db.DBLogic.g_instance.getDestructibleObjectData(victim)
            damagedParts = []
            storePartId = -1
            storeDamage = -1
            if isTeamObject(victim):
                numParts = len(victimParts)
            else:
                numParts = 1
            isFriendlyVictim = victim.teamIndex == owner.teamIndex
            for partId, dist in victimParts:
                victimPartData = getEntityPartDataByID(victim, partId, victimData)
                if victimPartData:
                    if isFriendlyVictim:
                        if damageReason == DAMAGE_REASON.BOMB_EXPLOSION:
                            damage = BOMB_ALLY_DAMAGE
                        elif damageReason == DAMAGE_REASON.ROCKET_EXPLOSION:
                            damage = owner.SETTINGS.ROCKET_ALLY_DAMAGE
                        else:
                            damage = 1.0
                    elif isAvatar(victim) and damageReason == DAMAGE_REASON.BOMB_EXPLOSION:
                        damage = BOMB_ENEMY_DAMAGE
                    else:
                        damage = 1.0
                    if dist < explosionRadiusEffective:
                        damage *= explosionDamage / numParts
                    elif dist <= explosionRadius:
                        damage *= explosionDamage * (explosionRadius - dist) / ((explosionRadius - explosionRadiusEffective) * numParts)
                    else:
                        LOG_ERROR('doExplosiveDamage : dist > explosionRadius, ', partId, 'for object', victim, victim.id)
                    if damage > 0:
                        damagedParts.append({'key': partId,
                         'value': damage})
                else:
                    LOG_ERROR('Invalid partID', partId, 'for object', victim, victim.id)

            if storeDamage > 0 and storePartId != -1:
                damagedParts.append({'key': storePartId,
                 'value': storeDamage})
            if damagedParts:
                victim.receiveExplosiveDamage(owner, damagedParts, owner.entityGroupMask, owner.teamIndex, damageReason, owner.unitNumber)

        owner.onHitTarget(victimsMap.iterkeys(), damageReason, ACTION_DEALER.PILOT)

    @staticmethod
    def onClientBulletExplosion(gd, contacts, isPlayer, victim, bulletDir):
        materialId = isTeamObject(victim) and 254 or 255
        materialName = db.DBLogic.g_instance.getMaterialName(materialId)
        if hasattr(gd.explosionParticles, materialName):
            explosionEffectName = gd.explosionParticles.__dict__[materialName]
        else:
            explosionEffectName = gd.explosionParticles.default
        if explosionEffectName:
            import Avatar
            for position, partID, bbox, armor in contacts:
                Avatar.onBulletExplosion(Effects.getEffectId(explosionEffectName), isPlayer, position, bulletDir if materialName == 'aircraft' else None, victim)

        return

    @staticmethod
    def calculateDistEffectiveness(gd, ad, bulletStartPos, bulletContactPoint):
        dist = (bulletContactPoint - bulletStartPos).length
        if dist > BULLET_EFFECTIVE_DIST:
            l = gd.bulletFlyDist - BULLET_EFFECTIVE_DIST
            if l > 0:
                bulletEffectivenessOnMaxDist = ad.kineticPartMaxDist / ad.kineticPartMinDist
                return (gd.bulletFlyDist - dist) / l * (1 - bulletEffectivenessOnMaxDist) + bulletEffectivenessOnMaxDist
        return 1.0

    @staticmethod
    def calculateBulletDamage(shooter, victim, gd, v0, shootInfo, distEffectiveness):
        k = max(0.0, v0 * distEffectiveness / (gd.bulletSpeed / WORLD_SCALING))
        damage = k * shootInfo.kineticPartMinDist * gd.DPS * 60.0 / gd.RPM
        distVector = victim.position - shooter.position
        v1 = getEntityVector(shooter)
        v2 = getEntityVector(victim)
        distLen = distVector.length
        vProjectionLen = 0 if distLen == 0 else (v1 - v2).dot(distVector) / distLen
        vSum = (Weapons.getEntityNominalSpeed(shooter) + Weapons.getEntityNominalSpeed(victim)) * WORLD_SCALING
        famK = 1.0 if vSum == 0.0 else FAM_PIVOT + (FAM_SPEED_ETALON_MULT - FAM_PIVOT) * vProjectionLen / vSum
        return damage * clamp(FAM_CLAMP_MIN, famK, FAM_CLAMP_MAX)

    @staticmethod
    def getEntityNominalSpeed(entity):
        if isAvatar(entity):
            settings = db.DBLogic.g_instance.getDestructibleObjectData(entity)
            return settings.flightModel.engine[airplanesConfigurations[entity.globalID].logicalParts[LOGICAL_PART.ENGINE]].maxSpeed
        else:
            return 0.0

    @staticmethod
    def onBulletCollision(victim, bulletStartPos, bulletSpeed, bulletDir, bulletPos, contacts, data):
        gunDescription = db.DBLogic.g_instance.getComponentByIndex(COMPONENT_TYPE.GUNS, data['gunID'])
        if IS_CLIENT:
            for bulletId in data['bullets']:
                if bulletId != None:
                    BigWorld.removeBullet(bulletId)

            Weapons.onClientBulletExplosion(gunDescription, contacts, data['isPlayer'], victim, bulletDir)
        else:
            shooter = BigWorld.entities.get(data['shooterID'], None)
            bIsTeamObject = isTeamObject(victim)
            if shooter and not victim.isDestroyed and (not bIsTeamObject or shooter.teamIndex != victim.teamIndex):
                ammoDescription = db.DBLogic.g_instance.getComponentByIndex(COMPONENT_TYPE.AMMO, data['ammoID'])
                distEffectiveness = Weapons.calculateDistEffectiveness(gunDescription, ammoDescription, bulletStartPos, bulletPos)
                damage = Weapons.calculateBulletDamage(shooter, victim, gunDescription, bulletSpeed / WORLD_SCALING, ammoDescription, distEffectiveness)
                parts = [ c[1] for c in contacts ]
                victim.receiveBullet(shooter, parts, shooter.entityGroupMask, shooter.teamIndex, data['ammoID'], data['gunID'], data['modsActivity'], shooter.objTypeID, shooter.unitNumber, damage)
                shooter.onHitTarget([victim], DAMAGE_REASON.BULLET, ACTION_DEALER.PILOT)
        return

    @staticmethod
    def onBulletEnd(bulletStartPos, bulletSpeed, bulletDir, bulletPos, data):
        pass

    def getGunGroupsInitialInfo(self):
        """return bullet counters for all weapon groups"""
        return self.__guns.getGunGroupsInitialInfo()

    def getGunGroupCounters(self):
        """return bullet counters for all weapon groups"""
        return self.__guns.getGunGroupCounters()

    def getGunGroupsStates(self):
        """return gun groups not able to shot now (overheated, destroyed etc)"""
        return self.__guns.getGunGroupsStates()

    def getMass(self):
        return self.__guns.getMass()

    def getDps(self):
        return self.__guns.getDps()

    def getFullDPS(self):
        return self.__guns.getFullDPS()

    def damagePerPass(self):
        return self.__guns.damagePerPass(self._owner.controllers['staticAttributesProxy'].stallSpeed)

    @property
    def middleBulletSpeed(self):
        return self.__middleBulletSpeed

    @property
    def bulletSpeedForMostLargeCaliberGroup(self):
        return self.__bulletSpeedForMostLargeCaliberGroup

    def getMaxVibroDispersionAngle(self):
        if self.__maxCaliberGroups:
            return sum((self.__getDispersion(g.dispersionAngle, g.reductionAngle) for g in self.__maxCaliberGroups)) / len(self.__maxCaliberGroups)
        return 0

    def __getDispersion(self, dispersionAngle, gunReduction):
        reduction, reductionMod = self._owner.dynamicalDispersionCfc()
        pilotReduction = DEAD_PILOT_ADD_DISPERSION if self.__isPilotDead else 0
        return (dispersionAngle + reduction + gunReduction + pilotReduction) * reductionMod

    def __calculateBulletDir(self, originalRotation, weaponGroup, gun, axisRnd, powRnd):
        axisAngle = axisRnd * math.pi * 2.0
        self.__tempVec3.set(math.sin(axisAngle), math.cos(axisAngle), 0)
        angle = math.pow(powRnd, 1.5) * self.__getDispersion(weaponGroup.dispersionAngle, weaponGroup.reductionAngle)
        self.__tempQuat.fromAngleAxis(angle, self.__tempVec3)
        gunRotation = originalRotation.mul(self.__tempQuat)
        return gunRotation.rotateVec(gun.reductionDir)

    def getWeaponGroupsMaxAttackRange(self):
        return self.__guns.getWeaponGroupsMaxAttackRange()

    def getGunGroups(self):
        return self.__guns.groups

    def syncGuns(self, data):
        self.__guns.syncGuns(data)

    def __initClientUpdateCallBack(self):
        """it's constructed to be called only for owner != None !!!"""
        if not self.__updateCallBack:
            self.__setClientUpdateCallBack()

    def __setClientUpdateCallBack(self):
        self.__updateCallBack = BigWorld.callback(SERVER_TICK_LENGTH, self.__clientUpdate)
        self.__lastUpdateTime = BigWorld.time()

    def __clientUpdate(self):
        dt = BigWorld.time() - self.__lastUpdateTime
        self.__setClientUpdateCallBack()
        if EntityStates.inState(self._owner, EntityStates.GAME):
            if not self.__prevControllerPosition:
                self.__prevControllerPosition = Math.Vector3(self._owner.getShootingControllerPosition())
                self.__prevControllerRotation = Math.Quaternion(self._owner.getShootingControllerRotation())
            armaments = self._owner.armamentStates
            if armaments or self.__isPlayer:
                if self.__pastTime > 0.0:
                    self.__guns.commonUpdate(self.__pastTime, 0)
                self.__guns.commonUpdate(dt, armaments)
                self.__pastTime = 0.0
                weaponGroups = self.__guns.shoot(armaments)
                if COLLISION_RECORDER:
                    self._owner.markPosition(0, self.__prevControllerPosition, self._owner.syncedRandom.getInfo())
                if weaponGroups:
                    self.__shootClient(dt, weaponGroups)
                else:
                    self.__stopShootingSounds()
            else:
                if self.__pastTime == 0.0:
                    self.__stopShootingSounds()
                self.__pastTime += dt
            self.__prevControllerPosition.set(self._owner.getShootingControllerPosition())
            if COLLISION_RECORDER:
                self._owner.markPosition(1, self.__prevControllerPosition, self._owner.syncedRandom.getInfo())
            self.__prevControllerRotation = self._owner.getShootingControllerRotation()
            if self.__isOwnerAvatar:
                self._owner.updateAmmo()

    def __registerGunsRender(self):
        for group in self.__guns.groups:
            group.ammoBelt.registerShotRender()

    def __playShootingSounds(self, arraySoundShot):
        for weaponSoundID, so in self.__so.iteritems():
            if weaponSoundID in arraySoundShot:
                if weaponSoundID not in self.__playingSounds:
                    self.__playingSounds.add(weaponSoundID)
                    for s in so:
                        s.play()

            elif weaponSoundID in self.__playingSounds:
                self.__playingSounds.remove(weaponSoundID)
                for s in so:
                    s.stop()

    def __stopShootingSounds(self):
        for weaponSoundID, so in self.__so.iteritems():
            if weaponSoundID in self.__playingSounds:
                self.__playingSounds.remove(weaponSoundID)
                for s in so:
                    s.stop()

    def linkSound(self, wid, so):
        if wid not in self.__so:
            self.__so[wid] = []
        self.__so[wid].append(so)

    def getSounds(self, weaponSoundID):
        if weaponSoundID in self.__so:
            return self.__so[weaponSoundID]
        else:
            return None

    def isGunsOverHeated(self, minTemp):
        for group in self.__guns.groups:
            if group.temperature >= minTemp:
                return True

        return False

    def clearGunsOverheat(self, prc):
        for group in self.__guns.groups:
            group.clearTemperature(prc)

    def reload(self):
        for group in self.__guns.groups:
            group.reload()

    def syncGunsWithClient(self):
        self._owner.syncGunsWithClient(self.__guns.getSyncData())