# Embedded file name: scripts/common/db/DBTeamTurret.py
import Math
import math
import ResMgr
from consts import WORLD_SCALING, GUN_TYPE, IS_AIRPLANE_EDITOR, IS_CLIENT, IS_EDITOR
from DBHelpers import *
from DBComponents import ComponentsTunes
from DBAirCrafts import PivotsTunes
from DBBaseObject import DamageEffects
import DBLogic
from DBBaseClass import DBBaseClass
from Curve import Curve
from debug_utils import LOG_DEBUG

class BattleLevelsSettingsTurrets:
    DEFAULT_VALUE = {'damageK': 1.0}

    def __init__(self, data):
        self.__data = {}
        self.readData(data)

    def readData(self, data):
        if data:
            for sectionData in data.values():
                battleLevel = sectionData.readInt('battleLevel', -1)
                if battleLevel != -1:
                    if self.__data.has_key(battleLevel):
                        self.__data[battleLevel]['damageK'] = sectionData.readFloat('damageK', self.__data[battleLevel]['damageK'])
                        self.__data[battleLevel]['targetLockShootDistanceK'] = sectionData.readFloat('targetLockShootDistanceK', self.__data[battleLevel]['targetLockShootDistanceK'])
                        self.__data[battleLevel]['targetLostDistanceK'] = sectionData.readFloat('targetLostDistanceK', self.__data[battleLevel]['targetLostDistanceK'])
                        self.__data[battleLevel]['explosionRadiusK'] = sectionData.readFloat('explosionRadiusK', self.__data[battleLevel]['explosionRadiusK'])
                        self.__data[battleLevel]['minDamageRadiusK'] = sectionData.readFloat('minDamageRadiusK', self.__data[battleLevel]['minDamageRadiusK'])
                    else:
                        self.__data[battleLevel] = {'damageK': sectionData.readFloat('damageK', 1.0),
                         'targetLockShootDistanceK': sectionData.readFloat('targetLockShootDistanceK', 1.0),
                         'targetLostDistanceK': sectionData.readFloat('targetLostDistanceK', 1.0),
                         'explosionRadiusK': sectionData.readFloat('explosionRadiusK', 1.0),
                         'minDamageRadiusK': sectionData.readFloat('minDamageRadiusK', 1.0)}

    def getDataForLevel(self, battleLevel):
        return self.__data.get(battleLevel, BattleLevelsSettingsTurrets.DEFAULT_VALUE)


class AircraftClassSettings:
    DEFAULT_VALUE = {'aggroK': 1.0,
     'damageK': 1.0}

    def __init__(self, data):
        self.__data = {}
        self.readData(data)

    def readData(self, data):

        def generateListOfTuple():
            for sectionID, sectionData in data.items():
                if sectionID != 'damageBaseK':
                    aircraftClass = sectionData.readString('aircraftClass', 'None')
                    aircraftClass = aircraftClass.lower()
                    for key, val in consts.PLANE_TYPE_NAME.iteritems():
                        if aircraftClass == val.lower():
                            yield (key, {'aggroK': sectionData.readFloat('aggroK', 1.0),
                              'damageK': sectionData.readFloat('damageK', 1.0) * self.damageBaseK})
                            break

        if data:
            readValue(self, data, 'damageBaseK', 1.0)
            self.__data = dict(list(generateListOfTuple()))

    def getDataForClass(self, aircraftClass):
        return self.__data.get(aircraftClass, AircraftClassSettings.DEFAULT_VALUE)

    def getDataForClassByGlobalID(self, globalID):
        return self.getDataForClass(DBLogic.g_instance.getAirplaneClassByGlobalID(globalID))


class TurretVisualSettings:
    DEFAULT_RECOIL_CURVE = Curve([Math.Vector2(0.0, 0.0), Math.Vector2(0.1, -0.005), Math.Vector2(1.0, 0.0)])

    def __init__(self, data):
        self.trackYawMin = 0
        self.trackYawMax = 360
        self.trackPitchMin = -180
        self.trackPitchMax = 180
        self.yawMin = -180
        self.yawMax = 180
        self.pitchMin = -180
        self.pitchMax = 180
        self.animatorDirectionOffset = Math.Vector3(0, 0, 0)
        self.animatorDirectionDefault = Math.Vector3(0, 0, 0)
        self.axisDirections = Math.Vector3(2, 1, 0)
        self.angularVelocity = 1800000
        self.angularThreshold = 0.0
        self.angularHalflife = 0.0
        self.pitchNodeName = 'joint3'
        self.yawNodeName = 'joint2'
        self.directionNodeName = 'joint3_BlendBone'
        self.shootingNodeName = 'joint4'
        self.idleFrequencyScalerX = 1.0
        self.idleAmplitudeScalerX = 0.02
        self.idleFrequencyScalerY = 1.0
        self.idleAmplitudeScalerY = 0.02
        self.shootTime = 0.25
        self.shootCooldownTime = 0.75
        self.shootingAmplitudeScaler = 0.05
        self.enableIdleAnimation = False
        self.recoilCurve = TurretVisualSettings.DEFAULT_RECOIL_CURVE.copy()
        self.useGunProfile = True
        self.readData(data)

    def readData(self, data):
        if data is None:
            return
        else:
            readValue(self, data, 'yawMin', -179.99)
            readValue(self, data, 'yawMax', 180.0)
            readValue(self, data, 'pitchMin', -179.99)
            readValue(self, data, 'pitchMax', 180.0)
            readValue(self, data, 'trackYawMin', -179.99)
            readValue(self, data, 'trackYawMax', 180.0)
            readValue(self, data, 'trackPitchMin', -179.99)
            readValue(self, data, 'trackPitchMax', 180.0)
            readValue(self, data, 'animatorDirectionOffset', Math.Vector3(0, 0, 0))
            readValue(self, data, 'animatorDirectionDefault', Math.Vector3(0, 0, 0))
            readValue(self, data, 'animatorDieDirection', Math.Vector3(0, 0, 0))
            readValue(self, data, 'axisDirections', Math.Vector3(2, 1, 0))
            readValue(self, data, 'angularVelocity', math.pi)
            readValue(self, data, 'angularThreshold', 0.0)
            readValue(self, data, 'angularHalflife', 0.0)
            readValue(self, data, 'pitchNodeName', 'joint3')
            readValue(self, data, 'yawNodeName', 'joint2')
            readValue(self, data, 'directionNodeName', 'joint3_BlendBone')
            readValue(self, data, 'shootingNodeName', 'joint4')
            readValue(self, data, 'idleFrequencyScalerX', 1.0)
            readValue(self, data, 'idleAmplitudeScalerX', 0.02)
            readValue(self, data, 'idleFrequencyScalerY', 1.0)
            readValue(self, data, 'idleAmplitudeScalerY', 0.02)
            readValue(self, data, 'shootTime', 0.25)
            readValue(self, data, 'shootCooldownTime', 0.75)
            readValue(self, data, 'enableIdleAnimation', False)
            readValue(self, data, 'recoilCurve', TurretVisualSettings.DEFAULT_RECOIL_CURVE)
            readValue(self, data, 'useGunProfile', True)
            for i in range(0, 3):
                self.animatorDirectionOffset[i] = self.animatorDirectionOffset[i]

            for i in range(0, 3):
                self.animatorDirectionDefault[i] = self.animatorDirectionDefault[i]

            if self.pitchMin > self.pitchMax:
                if self.pitchMax < 0:
                    self.pitchMax += 360
                else:
                    self.pitchMin -= 360
            return

    def save(self, data):
        if IS_AIRPLANE_EDITOR:
            writeValue(self, data, 'yawMin', -179.99)
            writeValue(self, data, 'yawMax', 180.0)
            writeValue(self, data, 'pitchMin', -179.99)
            writeValue(self, data, 'pitchMax', 180.0)
            writeValue(self, data, 'trackYawMin', 0.0)
            writeValue(self, data, 'trackYawMax', 360.0)
            writeValue(self, data, 'trackPitchMin', -180.0)
            writeValue(self, data, 'trackPitchMax', 180.0)
            writeValue(self, data, 'animatorDirectionOffset', Math.Vector3(0, 0, 0))
            writeValue(self, data, 'animatorDirectionDefault', Math.Vector3(0, 0, 0))
            writeValue(self, data, 'animatorDieDirection', Math.Vector3(0, 0, 0))
            writeValue(self, data, 'axisDirections', Math.Vector3(2, 1, 0))
            writeValue(self, data, 'angularVelocity', math.pi)
            writeValue(self, data, 'angularThreshold', 0.0)
            writeValue(self, data, 'angularHalflife', 0.0)
            writeValue(self, data, 'pitchNodeName', 'joint3')
            writeValue(self, data, 'yawNodeName', 'joint2')
            writeValue(self, data, 'directionNodeName', 'joint3_BlendBone')
            writeValue(self, data, 'shootingNodeName', 'joint4')
            writeValue(self, data, 'idleFrequencyScalerX', 1.0)
            writeValue(self, data, 'idleAmplitudeScalerX', 0.02)
            writeValue(self, data, 'idleFrequencyScalerY', 1.0)
            writeValue(self, data, 'idleAmplitudeScalerY', 0.02)
            writeValue(self, data, 'shootTime', 0.25)
            writeValue(self, data, 'shootCooldownTime', 0.75)
            writeValue(self, data, 'shootingAmplitudeScaler', 0.05)
            writeValue(self, data, 'enableIdleAnimation', True)
            writeValue(self, data, 'useGunProfile', True)
            writeValue(self, data, 'recoilCurve', Curve())


class Turret(DBBaseClass):

    def __init__(self, typeID, fileName, data):
        DBBaseClass.__init__(self, typeID, fileName)
        self.components = None
        self.pivots = None
        self.damageEffects = None
        self.battleLevelsSettingsTurrets = None
        self.aircraftClassSettings = None
        self.ik = []
        self.visualSettings = {}
        readDataWithDependencies(self, data, 'turrets')
        if data:
            self.gunName = self.gunName.lower()
            self.weaponName = self.weaponName.lower()
            self.hangarName = self.hangarName.lower()
            self.hangarSimilarGun = self.hangarSimilarGun.lower()
            self.weaponCount = int(self.weaponCount)
            self.explosionRadius *= WORLD_SCALING
            self.minDamageRadius *= WORLD_SCALING
            self.targetLockShootDistance *= WORLD_SCALING
            self.targetLostDistance *= WORLD_SCALING
            self.randomR *= WORLD_SCALING
            self.minTargetAltitude *= WORLD_SCALING
            self.maxTargetAltitude *= WORLD_SCALING
            self.forestallingDist *= WORLD_SCALING
            self.randomR *= WORLD_SCALING
            self.yawMin = math.radians(self.yawMin)
            self.yawMax = math.radians(self.yawMax)
            self.yawSpeed = math.radians(self.yawSpeed)
            self.pitchMin = math.radians(self.pitchMin)
            self.pitchMax = math.radians(self.pitchMax)
            self.pitchSpeed = math.radians(self.pitchSpeed)
            self.targetShootDeltaAngle = math.radians(self.targetShootDeltaAngle)
            if self.pitchMin > self.pitchMax:
                if self.pitchMax < 0:
                    self.pitchMax += 2 * math.pi
                else:
                    self.pitchMin -= 2 * math.pi
        if IS_AIRPLANE_EDITOR:
            self.fileName = fileName
            self.__data = data
        return

    def readData(self, data):
        if data:
            readValue(self, data, 'weaponCount', 1)
            readValue(self, data, 'weaponName', '')
            readValue(self, data, 'hangarName', '')
            readValue(self, data, 'hangarSimilarGun', '')
            readValue(self, data, 'hangarDPS', 0)
            readValue(self, data, 'gunName', '')
            readValue(self, data, 'flamePath', 'HP_antiaircraft_gunFlame')
            readValue(self, data, 'bulletShot', 'particles/shot_gun_bullet_fire.xml')
            readValue(self, data, 'explosionRadius', 0.0)
            readValue(self, data, 'burstTime', 4.0)
            readValue(self, data, 'serverRPS', 0.0)
            readValue(self, data, 'DPS', 1.0)
            readValue(self, data, 'critAbility', 1.0)
            readValue(self, data, 'burstDelay', 3.0)
            readValue(self, data, 'minDamageRadius', 10.0)
            readValue(self, data, 'minDamagePrc', 0.2)
            readValue(self, data, 'reductionDelay', 3.0)
            readValue(self, data, 'fullReductionTime', 20.0)
            readValue(self, data, 'weaponType', 'GUN_AA_NORMAL')
            self.weaponType = GUN_TYPE.AA if self.weaponType == 'GUN_AA' else GUN_TYPE.AA_NORMAL
            readValue(self, data, 'yawMin', 0.0)
            readValue(self, data, 'yawMax', 0.0)
            readValue(self, data, 'yawSpeed', 0.0)
            readValue(self, data, 'pitchMin', 0.0)
            readValue(self, data, 'pitchMax', 0.0)
            readValue(self, data, 'pitchSpeed', 0.0)
            readValue(self, data, 'targetLockShootDistance', 0.0)
            readValue(self, data, 'targetLostDistance', 1000.0)
            readValue(self, data, 'targetShootDeltaAngle', 0.0)
            readValue(self, data, 'isScenarioAnimator', False)
            if self.hangarName == 'G7mm-Vickers-K-T':
                pass
            flamesData = findSection(data, 'flames')
            if flamesData:
                self.flamePathes = flamesData.readStrings('flamePath')
            else:
                self.flamePathes = []
            shellsData = findSection(data, 'shells')
            if shellsData:
                self.shellPathes = shellsData.readStrings('shellPath')
            else:
                self.shellPathes = []
            if self.components:
                self.components.readData(data)
            else:
                self.components = ComponentsTunes(data)
            if self.pivots:
                self.pivots.readData(data)
            else:
                self.pivots = PivotsTunes(data)
            readValue(self, data, 'burstTime', 3.0)
            readValue(self, data, 'forestallingDist', 5.0)
            readValue(self, data, 'randomR', 4.0)
            readValue(self, data, 'searchNewTargetDelay', 5.0)
            readValue(self, data, 'rangingDeltaValue', 0.35)
            readValue(self, data, 'rangingMinValue', 0.3)
            readValue(self, data, 'minTargetAltitude', 0.0)
            readValue(self, data, 'maxTargetAltitude', 1000.0)
            readValue(self, data, 'targetingDelay', 3.0)
            readValue(self, data, 'targetingGrowth', 0.05)
            readValue(self, data, 'aggroSwitchK', 0.5)
            if self.damageEffects:
                self.damageEffects.readData(findSection(data, 'damageEffects'))
            else:
                self.damageEffects = DamageEffects(findSection(data, 'damageEffects'))
            if self.battleLevelsSettingsTurrets:
                self.battleLevelsSettingsTurrets.readData(findSection(data, 'battleLevelsSettingsTurrets'))
            else:
                self.battleLevelsSettingsTurrets = BattleLevelsSettingsTurrets(findSection(data, 'battleLevelsSettingsTurrets'))
            if self.aircraftClassSettings:
                self.aircraftClassSettings.readData(findSection(data, 'aircraftClassSettings'))
            else:
                self.aircraftClassSettings = AircraftClassSettings(findSection(data, 'aircraftClassSettings'))
            visualSettingsSect = findSection(data, 'visualSettings', missingCheck=False)
            if visualSettingsSect is None:
                visualSettings = TurretVisualSettings(visualSettingsSect)
                visualSettings.yawMin = self.yawMin
                visualSettings.yawMax = self.yawMax
                visualSettings.pitchMin = self.pitchMin
                visualSettings.pitchMax = self.pitchMax
                self.visualSettings[''] = visualSettings
            else:
                for key, settings in visualSettingsSect.items():
                    if key == 'turret':
                        mountPoint = settings.readString('mountPoint', '')
                        if mountPoint in self.visualSettings:
                            self.visualSettings[mountPoint].readData(settings)
                        else:
                            self.visualSettings[mountPoint] = TurretVisualSettings(settings)
                    else:
                        LOG_WARNING('Wrong format of turret visualSettings section %s'.format(self.typeName))

            if IS_CLIENT or IS_EDITOR:
                self.ik = []
                ikSection = findSection(data, 'ik', missingCheck=False)
                if ikSection:
                    self.modelIk = ikSection.readString('model')
                    self.ik.append(BigWorld.loadIKDataFromFile(self.modelIk))
        return

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['ik']
        return state

    def __setstate__(self, dict):
        modelIk = dict.get('modelIk')
        self.__dict__.update(dict)
        self.ik = []
        if modelIk:
            self.ik.append(BigWorld.loadIKDataFromFile(modelIk))

    def reloadIk(self):
        if IS_CLIENT or IS_EDITOR:
            ikSection = findSection(self.__data, 'ik', missingCheck=False)
            if ikSection is not None:
                self.ik = []
                self.modelIk = ikSection.readString('model')
                self.ik.append(BigWorld.loadIKDataFromFile(self.modelIk))
        return

    def save(self):
        if IS_AIRPLANE_EDITOR:
            try:
                visualSettingsSect = findSection(self.__data, 'visualSettings', missingCheck=False)
                if visualSettingsSect is None:
                    visualSettingsSect = self.__data.createSection('visualSettings')
                    for mountPoint, visualSettings in self.visualSettings.items():
                        turret = visualSettingsSect.createSection('turret')
                        turret.writeString('mountPoint', mountPoint)
                        self.visualSettings[mountPoint].save(turret)

                for key, settings in visualSettingsSect.items():
                    if key == 'turret':
                        mountPoint = settings.readString('mountPoint', '')
                        if mountPoint in self.visualSettings:
                            self.visualSettings[mountPoint].save(settings)

                self.__data.save()
            except Exception as e:
                print e

        return