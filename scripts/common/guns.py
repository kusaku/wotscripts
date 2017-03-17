# Embedded file name: scripts/common/guns.py
import BigWorld
import db.DBLogic
import Math
import math
from EntityHelpers import getReductionPointVector
from consts import COOLING_PER_SEC_TEMPERATURE_PRC, GUN_OVERHEATING_TEMPERATURE, GUN_STATE, calculateGunDPS, COMPONENT_TYPE, GUN_REDUCTION_FROM_DIST_K, IS_CELLAPP
from debug_utils import *
import Event
from SyncedRandom import SyncedRandom
from WeaponsHelpers import isGunGroupShooting

def getPivot(pivotName, pivots):
    pivot = pivots.mountPoints.get(pivotName, None)
    if not pivot:
        LOG_ERROR('Unkown pivot for gun:' + pivotName)
    return pivot


class Guns:

    def __init__(self, weaponsInfo, planeID, pivots, ammoBeltsMap = None):

        def generateGroups():
            groupID = 0
            for weaponGroup, infos in gunInfos.iteritems():
                gunName = infos[0].name
                gunDescription = db.DBLogic.g_instance.getGunData(gunName)
                belt = None
                if ammoBeltsMap:
                    if gunName in ammoBeltsMap:
                        beltID = ammoBeltsMap[gunName]
                        belt = db.DBLogic.g_instance.getComponentByID(COMPONENT_TYPE.AMMOBELT, beltID)
                    else:
                        LOG_ERROR("Can't find belt for gun", gunName, 'in', ammoBeltsMap)
                else:
                    belt = db.DBLogic.g_instance.getComponentByID(COMPONENT_TYPE.AMMOBELT, gunDescription.defaultBelt)
                group = WeaponGroup(groupID, pivots, gunDescription, infos, belt, planeID)
                if IS_CELLAPP:
                    group.eGunOverHeat += self.__onGroupOverHeat
                else:
                    group.eGunOverHeat += self.__onGroupOverHeatClient
                yield group
                groupID += 1

            return

        self.__eventManager = Event.EventManager()
        if IS_CELLAPP:
            self.eTotalRecoilGunsThrust = Event.Event(self.__eventManager)
            self.__wasOverHeated = 0
        self.eGunOverHeat = Event.Event(self.__eventManager)
        self.__ammoStartWeight = 0
        self.__totalRecoilThrust = 0.0
        gunInfos = {}
        for gunInfo in weaponsInfo:
            gunDescription = db.DBLogic.g_instance.getGunData(gunInfo.name)
            if gunDescription:
                gunInfos.setdefault(gunInfo.weaponGroup, []).append(gunInfo)

        self.__weaponGroups = list(generateGroups())
        self.__weaponGroups.sort(key=lambda group: group.gunDescription.RPM)
        self.__weaponGroups.sort(key=lambda group: group.gunDescription.caliber, reverse=True)

    def destroy(self):
        for group in self.__weaponGroups:
            group.destroy()

        self.__eventManager.clear()

    def restart(self):
        for group in self.__weaponGroups:
            group.restart()

    def shoot(self, armamentStates):

        def generateList():
            for bit, group in enumerate(self.__weaponGroups):
                if armamentStates & 1 << bit and group.isReady():
                    group.shootInfo = group.ammoBelt.extract()
                    yield group

        return list(generateList())

    def cellUpdate(self, dt, fireFlags):
        armaments = 0
        for bit, group in enumerate(self.__weaponGroups):
            if isGunGroupShooting(fireFlags, bit):
                armaments |= 1 << bit

        self.commonUpdate(dt, armaments)
        self.eTotalRecoilGunsThrust(self.__totalRecoilThrust)
        return armaments

    def commonUpdate(self, dt, armaments):
        self.__totalRecoilThrust = 0.0
        for bit, group in enumerate(self.__weaponGroups):
            isGroupFiring = armaments & 1 << bit != 0
            group.update(dt, isGroupFiring)
            self.__totalRecoilThrust += group.recoilThrust

    def backup(self):
        return {'gunsBackup': [ group.backup() for group in self.__weaponGroups ],
         'wasOverheated': not self.__wasOverHeated}

    def restoreFromBackup(self, bp):
        for i, groupData in enumerate(bp['gunsBackup']):
            self.__weaponGroups[i].restoreFromBackup(groupData)

        self.__wasOverHeated = bp['wasOverheated']

    def calculateMiddleBulletSpeed(self):
        if self.__weaponGroups:
            return sum((group.gunDescription.bulletSpeed for group in self.__weaponGroups)) / len(self.__weaponGroups)
        return 1000

    def calculateBulletSpeedForMostLargeCaliberGroup(self):
        speed, caliber, dps = (0.0, 0.0, 0.0)
        for weaponGroup in self.__weaponGroups:
            if weaponGroup.gunDescription.caliber > caliber or 0.0 < caliber == weaponGroup.gunDescription.caliber and weaponGroup.dps > dps:
                caliber = weaponGroup.gunDescription.caliber
                speed = weaponGroup.gunDescription.bulletSpeed
                dps = weaponGroup.dps

        return speed

    def getGunGroupsInitialInfo(self):
        """return bullet counters for all group of guns"""

        def generateData():
            for i, group in enumerate(self.__weaponGroups):
                uiGroupID = i + 1
                yield (uiGroupID, {'initialCount': GUN_OVERHEATING_TEMPERATURE,
                  'description': group.gunDescription,
                  'shellID': -1,
                  'weaponName': group.gunDescription.name,
                  'ammoBeltType': group.ammoBelt.ammoBelt.beltType,
                  'objCount': len(group.guns)})

        return dict(generateData())

    def getGunGroupCounters(self):
        """return bullet counters for all group of guns"""

        def generateData():
            for i, group in enumerate(self.__weaponGroups):
                uiGroupID = i + 1
                yield (uiGroupID, int(min(group.temperature, GUN_OVERHEATING_TEMPERATURE)))

        return dict(generateData())

    def getGunGroupsStates(self):

        def generateData():
            for i, group in enumerate(self.__weaponGroups):
                uiGroupID = i + 1
                yield (uiGroupID, GUN_STATE.OVERHEATED if group.temperature == GUN_OVERHEATING_TEMPERATURE else GUN_STATE.READY)

        return dict(generateData())

    def getWeaponGroupsMaxAttackRange(self):
        """return - maxFlyDist by group"""
        if self.__weaponGroups:
            return max((group.gunDescription.bulletFlyDist for group in self.__weaponGroups))
        return 0

    def getSyncData(self):
        """This function used on cell side to sync bullets with client"""
        syncData = []
        for group in self.__weaponGroups:
            syncData.append(group.temperature)
            syncData.append(group.getReloadTimer())

        return syncData

    def syncGuns(self, data):
        for i, group in enumerate(self.__weaponGroups):
            temperature, reloadTimer = data[2 * i], data[2 * i + 1]
            group.sync(temperature, reloadTimer)

    def __onGroupOverHeat(self):
        self.__wasOverHeated += 1
        self.eGunOverHeat()

    def __onGroupOverHeatClient(self):
        self.eGunOverHeat()

    @property
    def wasOverHeated(self):
        return self.__wasOverHeated

    @property
    def groups(self):
        return self.__weaponGroups

    def getDps(self):
        if self.__weaponGroups:
            return sum((group.dps for group in self.__weaponGroups))
        return 0

    def getFullDPS(self):
        if self.__weaponGroups:
            return sum((group.fullDPS for group in self.__weaponGroups))
        return 0

    def damagePerPass(self, stallSpeed):
        if self.__weaponGroups:
            return sum((group.fullDPS * group.gunDescription.bulletFlyDist / stallSpeed for group in self.__weaponGroups))
        return 0

    def getMass(self):
        if self.__weaponGroups:
            return sum((group.gunDescription.mass * group.size for group in self.__weaponGroups))
        return 0


class Gun(object):

    def __init__(self, gunInfo, pivots, gunDescription):
        self.uniqueId = id(self)
        pivot = getPivot(gunInfo.flamePath, pivots)
        self.posDelta = Math.Vector3()
        self.addRotation = Math.Vector3()
        if pivot:
            self.posDelta.set(pivot.position)
            self.addRotation.set(pivot.direction)
        reductionPointVector = Math.Vector3(0.0, 0.0, gunDescription.bulletFlyDist * GUN_REDUCTION_FROM_DIST_K)
        self.reductionDir = reductionPointVector - pivot.position if pivot else Math.Vector3(reductionPointVector)
        self.reductionDir.normalise()
        self.flamePath = gunInfo.flamePath
        self.shellPath = gunInfo.shellPath if hasattr(gunInfo, 'shellPath') else None
        if self.shellPath == '_':
            self.shellPath = self.flamePath.replace('HP_flame', 'HP_shell')
        self.shellOutInterval = gunDescription.shellOutInterval if hasattr(gunDescription, 'shellOutInterval') else 1.0
        self.shellSyncTime = 0
        return


class WeaponGroup(object):

    def __init__(self, containerID, pivots, gunDescription, gunInfos, ammoBelt, planeID):
        self.NOT_FREE_GUNS_FIRING = True
        self.__guns = [ Gun(gunInfo, pivots, gunDescription) for gunInfo in gunInfos ]
        self.__size = len(self.__guns)
        self.__containerID = containerID
        self.__groupID = gunInfos[0].weaponGroup
        self.gunDescription = gunDescription
        self.__dispersionAngle = gunInfos[0].dispersionAngle
        self.__autoguiderAngle = gunInfos[0].autoguiderAngle
        self.__recoilDispersion = gunInfos[0].recoilDispersion
        self.__overheatingFullTime = gunInfos[0].overheatingFullTime
        self.gunName = gunInfos[0].name
        self.__coolingCFC = gunInfos[0].coolingCFC
        self.__gunOverheatingK = 1.0
        self.__reductionAngle = 0.0
        self.__recoilThrust = 0.0
        self.syncedRandom = SyncedRandom()
        self.clientProcessedBulletCount = 0
        gunProfileName = db.DBLogic.g_instance.getGunProfileName(gunDescription, planeID)
        self.__gunProfile = db.DBLogic.g_instance.getGunProfileData(gunProfileName)
        if not self.__gunProfile:
            LOG_ERROR('invalid gun profile', gunProfileName)
        self.__eventManager = Event.EventManager()
        self.eGunOverHeat = Event.Event(self.__eventManager)
        self.ammoBelt = AmmoBelt(self.gunDescription, ammoBelt, self.__gunProfile)
        self.restart()

    def destroy(self):
        self.__eventManager.clear()

    @property
    def guns(self):
        return self.__guns

    @property
    def groupID(self):
        return self.__groupID

    @property
    def size(self):
        return self.__size

    @property
    def gunProfile(self):
        return self.__gunProfile

    @property
    def dispersionAngle(self):
        return self.__dispersionAngle

    @property
    def reductionAngle(self):
        return self.__reductionAngle

    @property
    def recoilThrust(self):
        return self.__recoilThrust * self.__size

    @property
    def autoguiderAngle(self):
        return self.__autoguiderAngle

    def __dispersionCalc(self, dt, vibr, ampl, angBraking):
        return (vibr - ampl) * math.exp(-dt / angBraking) + ampl

    def reductionIncrease(self, dt):
        self.__reductionAngle = self.__dispersionCalc(dt, self.__reductionAngle, self.__recoilDispersion, self.__overheatingFullTime / 3.0)

    def reductionDecrease(self, dt):
        self.__reductionAngle = self.__dispersionCalc(dt, self.__reductionAngle, 0.0, self.__overheatingFullTime / 6.0)

    @property
    def dps(self):
        """
        calculate DPS for this Gun with current ammo belt
        function does the heavy calculations if necessary reuse caches the result
        """
        dps = calculateGunDPS('firePower', self.ammoBelt.shotData, self.gunDescription, self.__dispersionAngle, self.__recoilDispersion, self.__overheatingFullTime)
        return dps * self.__size

    @property
    def fullDPS(self):
        """
        calculate fullDPS for this Gun with current ammo belt
        """
        return self.gunDescription.DPS * self.__size

    def backup(self):
        return {'temperature': self.temperature,
         'timers': self.getReloadTimer()}

    def restoreFromBackup(self, backup):
        self.setReloadTimer(backup['timers'])
        self.temperature = backup['temperature']

    def restart(self):
        self.reload()
        self.temperature = 0.0
        self.__reductionAngle = 0.0
        self.__recoilThrust = 0.0

    def getSyncData(self):
        return self.temperature

    def sync(self, temperature, reloadTimer):
        self.temperature = temperature
        self.__reloadTimer = reloadTimer

    def reload(self):
        self.__reloadTimer = 0.0

    def update(self, dt, isFiring):
        if isFiring:
            self.__reloadTimer -= dt
            self.reductionIncrease(dt)
            gunData = self.gunDescription
            self.__recoilThrust = gunData.bulletMass * gunData.bulletSpeed * gunData.RPM / 60.0
        else:
            if self.__reloadTimer > 0:
                self.__reloadTimer -= dt
            if self.__reloadTimer <= 0:
                self.__reloadTimer = 0.0
                self.temperature = max(self.temperature - COOLING_PER_SEC_TEMPERATURE_PRC * dt * self.__coolingCFC, 0.0)
            self.reductionDecrease(dt)
        if isFiring:
            self.reductionIncrease(dt)
            gunData = self.gunDescription
            self.__recoilThrust = gunData.bulletMass * gunData.bulletSpeed * gunData.RPM / 60.0
        else:
            self.reductionDecrease(dt)
            self.__recoilThrust = 0

    def clearTemperature(self, prc):
        if self.temperature > 0:
            self.temperature = max(0, self.temperature - GUN_OVERHEATING_TEMPERATURE * prc)
            return True
        return False

    def isReady(self):
        return self.__reloadTimer <= 0

    def shoot(self, dt):
        shootTime = dt + self.__reloadTimer
        reloadTime = 60.0 / (self.gunDescription.RPM if self.temperature < GUN_OVERHEATING_TEMPERATURE else self.gunDescription.RPM * self.gunDescription.overheatedRPM)
        self.__reloadTimer += reloadTime
        if self.NOT_FREE_GUNS_FIRING:
            newTemp = min(self.temperature + GUN_OVERHEATING_TEMPERATURE / self.__overheatingFullTime * self.__gunOverheatingK * reloadTime, GUN_OVERHEATING_TEMPERATURE)
            if newTemp == GUN_OVERHEATING_TEMPERATURE and self.temperature < GUN_OVERHEATING_TEMPERATURE:
                self.temperature = GUN_OVERHEATING_TEMPERATURE
                self.eGunOverHeat()
            else:
                self.temperature = newTemp
        return shootTime

    def getReloadTimer(self):
        return self.__reloadTimer

    def setReloadTimer(self, v):
        self.__reloadTimer = v

    def onArmamentFreeUseChanged(self, flag):
        self.NOT_FREE_GUNS_FIRING = not flag


class AmmoBelt:

    def __init__(self, gunDescription, ammoBelt, gunProfile):
        self.__ammoBelt = ammoBelt
        self.__gunDescription = gunDescription
        self.__gunProfile = gunProfile
        self.__shotData = []
        self.__index = 0
        for ammoName in db.DBLogic.g_instance.getAmmoNames(gunDescription, ammoBelt):
            self.addBullet(ammoName)

        if len(self.__shotData) == 0:
            if len(gunDescription.ammunition) > 0:
                ammoName = gunDescription.ammunition[0].name
                self.addBullet(ammoName)
                LOG_ERROR('ShootData empty fo gun id: {0}. Setup ammo: {1}'.format(gunDescription.id, ammoName))
            else:
                LOG_ERROR('Gun id: {0} does not have any ammunition!'.format(gunDescription.id))
        self.restart()

    def addBullet(self, ammoName):
        shot = db.DBLogic.g_instance.getAmmoData(ammoName)
        if shot:
            shot.bulletRenderType = -1
            self.__shotData.append(shot)
        else:
            LOG_ERROR('Unknown ammunition in gunDescription', self.__gunDescription.name, ammoName)
        return shot

    def restart(self):
        self.__index = 0

    def extract(self):
        index = self.__index
        self.__index += 1
        if self.__index >= len(self.__shotData):
            self.__index = 0
        return self.__shotData[index]

    @property
    def ammoBelt(self):
        return self.__ammoBelt

    @property
    def gunDescription(self):
        return self.__gunDescription

    @gunDescription.setter
    def gunDescription(self, description):
        self.__gunDescription = description

    @property
    def shotData(self):
        return self.__shotData

    @shotData.setter
    def shotData(self, data):
        self.__shotData = data

    def registerShotRender(self, nameID = None):
        for shot in self.__shotData:
            if shot.bulletRenderType == -1 or nameID is not None:
                name = str(id(shot))
                if nameID is not None:
                    name = str(nameID)
                shot.bulletRenderType = BigWorld.registerBulletType(name, (self.__gunProfile.bulletThinkness, self.__gunProfile.bulletLen, self.__gunProfile.bulletLenExpand), self.__gunProfile.bulletThicknessExpand, (self.__gunProfile.smokeSizeX, self.__gunProfile.smokeSizeY), self.__gunProfile.smokeTillingLength, self.__gunProfile.smokeRadiusScale, (shot.bulletColour, shot.smokeColour), self.__gunProfile.textureIndex, self.__gunDescription.passbySound)

        return