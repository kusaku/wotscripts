# Embedded file name: scripts/common/db/DBAirCrafts.py
import Math
import math
from BBoxes import BBoxes
from DBHelpers import readValue, readValues, readDataWithDependencies, findSection, updateValue, writeValue
from consts import WORLD_SCALING, AIRCRAFT_MODEL_SCALING, IS_EDITOR, NOT_AVAILABLE, LOGICAL_PART, IS_CLIENT, PLANE_LEVELS, IS_CELLAPP
from DBComponents import *
import ResMgr
import DBPatch
from debug_utils import DBLOG_ERROR, DBLOG_NOTE, LOG_ERROR
from DBParts import PartsTunes
from copy import deepcopy
import sys
from config_consts import IS_DEVELOPMENT

class CheckString(str):
    pass


class GunnerHeadAnimatorSettings():

    def __init__(self, data = None):
        self.__params = (('nodeName', 'Scene Root'),
         ('pitchMin', 0),
         ('pitchMax', 90),
         ('yawMin', -60),
         ('yawMax', 60),
         ('angularVelocity', 60),
         ('angularThreshold', 0.0),
         ('angularHalflife', 0.0),
         ('animatorDirectionDefault', Math.Vector3(0.0, 0.0, 0.0)),
         ('animatorDieDirection', Math.Vector3(0.0, 0.0, 0.0)),
         ('animatorDirectionOffset', Math.Vector3(0.0, 0.0, 0.0)),
         ('idleFrequencyScalerX', 0.5),
         ('idleAmplitudeScalerX', 0.1),
         ('idleFrequencyScalerY', 0.5),
         ('idleAmplitudeScalerY', 0.1),
         ('enableIdleAnimation', True))
        self.readData(data)

    def readData(self, data):
        readValues(self, data, self.__params)


class AirCraft():

    def __init__(self, dataPath, newDatabase):
        data = ResMgr.openSection(dataPath)
        self.airplane = None
        self.crew = None
        self.components = None
        self.pivots = None
        self.hpmass = None
        if IS_EDITOR:
            self.__data = data
            self.__dataPath = dataPath
        DBLOG_NOTE("Start loading aircraft '" + dataPath + "'")
        readDataWithDependencies(self, data, 'aircrafts', newDatabase=newDatabase)
        self.postLoadTransform()
        DBLOG_NOTE("Finished loading aircraft '" + dataPath + "'")
        ResMgr.purge(dataPath, True)
        return

    def check(self):
        import DBLogic
        dbLogic = DBLogic.g_instance
        errors = ''
        pivotsNames = []
        pivotsNamesWithId = []
        flightModel = self.airplane.flightModel
        for pivotName in self.pivots.mountPoints.keys():
            try:
                nameParts = pivotName.split('/', 4)
                partId = int(nameParts[0])
                partUpgradeId = int(nameParts[1])
                slotId = int(nameParts[2])
                slotTypeId = int(nameParts[3])
                pivotsNames.append(nameParts[4])
                pivotsNamesWithId.append(nameParts[2] + '/' + nameParts[3] + '/' + nameParts[4])
            except:
                errors += '\nWrong pivot, regenerate :' + pivotName

        for slot in self.components.weapons2.slots.values():
            has0type = False
            if slot.id >= len(flightModel.weaponSlot):
                errors += '\nSlot ' + str(slot.id) + '  is not in the flightModel.weaponSlot'
            for slotType in slot.types.values():
                has0type = has0type or slotType.id == 0
                fmSlotData = None
                if slot.id < len(flightModel.weaponSlot):
                    if slotType.id >= len(flightModel.weaponSlot[slot.id]):
                        errors += '\nIn Slot ' + str(slot.id) + ' type ' + str(slotType.id) + ' is not in the flightModel.weaponSlot'
                    else:
                        fmSlotData = flightModel.weaponSlot[slot.id][slotType.id]
                for weapon in slotType.weapons:
                    upgrade = dbLogic.upgrades.get(weapon.name, None)
                    if fmSlotData:
                        if upgrade.type == 'gun':
                            if fmSlotData.overheatingFullTime == 0:
                                errors += '\nSlot ' + str(slot.id) + ' type ' + str(slotType.id) + ' overheatingFullTime == 0 ' + weapon.name
                        name1 = fmSlotData.name
                        name2 = weapon.name
                        if name2 not in name1:
                            errors += '\nSlot ' + str(slot.id) + ' type ' + str(slotType.id) + ' has different name in ' + self.airplane.name + '.xml and in the aircraft.xml (' + name1 + ', ' + name2 + ')'
                    if not upgrade:
                        errors += '\nSlot ' + str(slot.id) + ' type ' + str(slotType.id) + " can't find upgrade " + weapon.name
                    elif self.airplane.name not in (variant.aircraftName for variant in upgrade.variant):
                        errors += '\nSlot ' + str(slot.id) + ' type ' + str(slotType.id) + ' for upgrade ' + upgrade.name + " can't find variant"
                    if not dbLogic.getGunData(weapon.name):
                        shellType, shell = dbLogic.getShellComponentsGroupIDAndDescription(weapon.name)
                        if not shell:
                            errors += '\nSlot ' + str(slot.id) + ' type ' + str(slotType.id) + " can't find shell " + weapon.name + '/' + upgrade.name
                    if weapon.flamePath not in pivotsNames:
                        errors += '\nSlot ' + str(slot.id) + ' type ' + str(slotType.id) + " can't find pivot " + weapon.flamePath
                    elif str(slot.id) + '/' + str(slotType.id) + '/' + weapon.flamePath not in pivotsNamesWithId:
                        errors += '\nSlot ' + str(slot.id) + ' type ' + str(slotType.id) + " can't find pivot for this slotType " + weapon.flamePath

            if not has0type:
                errors += '\nSlot ' + str(slot.id) + " has't slot type '0'"

        for part in self.airplane.partsSettings.getPartsOnlyList():
            if len(part.upgrades) == 0:
                errors += "\nPart don't have upgrades " + part.name
            for upgrade in part.upgrades.values():
                if len(upgrade.states) == 0:
                    errors += "\nPart upgrade don't have states " + part.name
                hasDefaultState = False
                for state in upgrade.states.values():
                    hasDefaultState = hasDefaultState or state.id == 1

                if not hasDefaultState:
                    errors += "\nPart upgrade don't have default state " + part.name

        if not IS_CLIENT and not dbLogic.getScanSectorsProfile(self.airplane.flightModel.visibility.scanSectorProfile):
            errors += "\nCan't find scanSectorProfile " + self.airplane.flightModel.visibility.scanSectorProfile
        presets = dbLogic.getAircraftPresetsListByName(self.airplane.name)
        if presets and len(presets) > 0:
            errors += ''.join([ self.__checkUpgradePreset(preset) for preset in presets ])
        else:
            errors += '\nAircraft dont have presets'
        errors += self.__checkUpgrades()
        if errors and not self.isDev():
            errors = CheckString(errors)
            errors.bundleStop = True
        return errors

    def __checkUpgrades(self):
        errors = ''
        import DBLogic
        dbLogic = DBLogic.g_instance
        modules, aircrafts = dbLogic.getAircraftUpgradesFromName(self.airplane.name)
        moduleNames = dict()
        defaultConfig = dict()
        notDefaultUpgradeCount = 0
        for module in modules:
            moduleNames[module.name] = module
            for variant in module.variant:
                if variant.aircraftName == self.airplane.name:
                    if variant.parentUpgrade[0].name == '':
                        if module.type not in ('gun', 'rocket', 'bomb'):
                            if defaultConfig.has_key(module.type):
                                errors += '\n dublicate default upgrades :' + defaultConfig[module.type].name + ',' + module.name
                            else:
                                defaultConfig[module.type] = module
                    else:
                        notDefaultUpgradeCount += 1
                        parent = dbLogic.upgrades.get(variant.parentUpgrade[0].name, None)
                        if not parent:
                            errors += '\n invalid parent upgrade ' + variant.parentUpgrade[0].name + ' for ' + module.name

        for aircraft in aircrafts:
            for variant in aircraft.variant:
                if variant.aircraftName == self.airplane.name:
                    if not moduleNames.has_key(variant.parentUpgrade[0].name):
                        errors += '\n parent upgrade for aircraft ' + aircraft.name + ' not in this airplane'

        for module in modules:
            for variant in module.variant:
                if variant.aircraftName == self.airplane.name:
                    if variant.parentUpgrade[0].name != '' and not moduleNames.has_key(variant.parentUpgrade[0].name):
                        errors += '\n parent upgrade for module ' + module.name + ' not in this airplane'

        if not dbLogic.isUpgradesValid(self.airplane.name, defaultConfig.values()):
            errors += '\n invalid part upgrade default configuration: ' + ''.join([ ', ' + module.name for module in defaultConfig.values() ])
        if self.airplane.level != PLANE_LEVELS.MAXIMUM_PLANE_LEVEL and notDefaultUpgradeCount > 0 and len(aircrafts) == 0 and not hasattr(self.airplane.options, 'gold'):
            errors += "\n aircraft don't have child aircrafts"
        return errors

    def __checkUpgradePreset(self, preset):
        errors = ''
        import DBLogic
        dbLogic = DBLogic.g_instance
        upgrades = []
        for module in preset.module:
            upgrade = dbLogic.upgrades.get(module.name, None)
            if not upgrade:
                errors += '\n invalid part upgrade name: preset ' + preset.name + ' upgrade ' + module.name
                return errors
            upgrades.append(upgrade)

        if not dbLogic.isUpgradesValid(self.airplane.name, upgrades):
            errors += '\n invalid part upgrade configuration: preset ' + preset.name
        weaponCfg = [ (weapon.slot, weapon.configuration) for weapon in preset.weapon ]
        if not dbLogic.isWeaponConfigurationValid(upgrades, weaponCfg, self.airplane.name):
            errors += '\n invalid weapon  configuration: preset ' + preset.name + ' cfg: ' + str(weaponCfg)
        return errors

    def postLoadTransform(self):
        if self.airplane:
            self.airplane.postLoadTransform()

    def readData(self, data, newDatabase = None):
        if self.hpmass:
            self.hpmass.readData(data)
        else:
            self.hpmass = MassTunes(data)
        if self.airplane:
            self.airplane.readData(data, newDatabase)
        else:
            self.airplane = AirCraftTunes(data, newDatabase)
        if self.components:
            self.components.readData(data)
        else:
            self.components = ComponentsTunes(data)
        if self.pivots:
            self.pivots.readData(data)
        else:
            self.pivots = PivotsTunes(data)

    def save(self):
        bResult = False
        if IS_EDITOR:
            self.airplane.save()
            self.saveMassPivotToXML()
            try:
                if self.__data != None:
                    self.__data.save()
                    bResult = True
            except IOError as e:
                print 'Exception raised {0}'.format(e)
                bResult = False

        return bResult

    def getDataPath(self):
        if IS_EDITOR:
            return self.__dataPath

    def isDev(self):
        return self.airplane.options.isDev

    def updatePivots(self, pivotsList):
        if IS_EDITOR:
            if self.__data != None:
                self.pivots = None
                sectionName = 'Pivots'
                pivotsData = findSection(self.__data, sectionName)
                if pivotsData:
                    self.__data.deleteSection(pivotsData)
                pivotsData = self.__data.createSection(sectionName)
                for flamename, position, direction in pivotsList:
                    pivotData = pivotsData.createSection('pivot')
                    pivotData.writeString('name', flamename)
                    pivotData.writeVector3('position', position)
                    pivotData.writeVector3('direction', Math.Vector3(direction[0], direction[1], direction[2]))

                self.pivots = PivotsTunes(self.__data)
        return

    def updateMassPivot(self, pivot):
        if IS_EDITOR:
            if self.__data != None:
                self.hpmass = None
                sectionName = 'HPmass'
                massData = findSection(self.__data, sectionName)
                if massData:
                    self.__data.deleteSection(massData)
                massData = self.__data.createSection(sectionName)
                massData.writeVector3('position', pivot[0])
                massData.writeVector3('direction', Math.Vector3(pivot[1][0], pivot[1][1], pivot[1][2]))
                self.hpmass = MassTunes(self.__data)
        return

    def saveMassPivotToXML(self):
        if IS_EDITOR:
            if self.__data != None and self.hpmass != None:
                sectionName = 'HPmass'
                massData = findSection(self.__data, sectionName)
                if massData:
                    self.__data.deleteSection(massData)
                massData = self.__data.createSection(sectionName)
                pos = deepcopy(self.hpmass.mass.position)
                pos /= AIRCRAFT_MODEL_SCALING
                massData.writeVector3('position', pos)
                massData.writeVector3('direction', self.hpmass.mass.direction)
        return

    def setHpMass(self, pivot):
        if IS_EDITOR:
            if self.__data != None and self.hpmass != None:
                self.hpmass.mass.position = pivot[0]
                self.hpmass.mass.direction = Math.Vector3(pivot[1][0], pivot[1][1], pivot[1][2])
                self.hpmass.mass.position *= AIRCRAFT_MODEL_SCALING
        return


class AirCraftVisualSettings():

    def __init__(self, data = None):
        self.surfaceSettings = None
        self.damageEffects = None
        self.cameraEffects = None
        self.accelFovSettings = None
        self.hangarScenario = None
        self.gunnerAnimatorSettings = {}
        self.readData(data)
        return

    def postLoadTransform(self):
        self.aileronMaxAngle = math.radians(self.aileronMaxAngle)
        self.elevatorMaxAngle = math.radians(self.elevatorMaxAngle)
        self.rudderMaxAngle = math.radians(self.rudderMaxAngle)
        self.flapperMaxAngle = math.radians(self.flapperMaxAngle)
        self.brakeMaxAngle = math.radians(self.brakeMaxAngle)
        self.cameraOffset *= WORLD_SCALING

    def readData(self, data):
        if data != None:
            readValue(self, data, 'aileronMaxAngle', 45.0)
            readValue(self, data, 'elevatorMaxAngle', 45.0)
            readValue(self, data, 'rudderMaxAngle', 45.0)
            readValue(self, data, 'flapperMaxAngle', 45.0)
            readValue(self, data, 'brakeMaxAngle', 45.0)
            readValue(self, data, 'slateOffset', 0.0)
            readValue(self, data, 'slateOnAngle', 10.0)
            readValue(self, data, 'brakeOffset', 0.0)
            readValue(self, data, 'aileronSpeed', 45.0)
            readValue(self, data, 'elevatorSpeed', 45.0)
            readValue(self, data, 'rudderSpeed', 45.0)
            readValue(self, data, 'flapperSpeed', 45.0)
            readValue(self, data, 'brakeSpeed', 45.0)
            readValue(self, data, 'slateSpeed', 0.4)
            readValue(self, data, 'brakeOffsetSpeed', 45.0)
            readValue(self, data, 'rotorSpeedBroken', 1)
            readValue(self, data, 'rotorSpeedFalling', 2)
            readValue(self, data, 'rotorSpeedLow', 5)
            readValue(self, data, 'rotorSpeedNormal', 10)
            readValue(self, data, 'rotorSpeedFosage', 20)
            readValue(self, data, 'hangarConfig', NOT_AVAILABLE)
            readValue(self, data, 'hangarLandingPart', NOT_AVAILABLE)
            readValue(self, data, 'camera', '')
            readValue(self, data, 'cameraOffset', Math.Vector3(0, 0, 0))
            readValue(self, data, 'speedwiseEngineEffect', 0.0)
            surfaceSettings = findSection(data, 'surfaceSettings')
            if surfaceSettings:
                if self.surfaceSettings:
                    self.surfaceSettings.readData(surfaceSettings)
                else:
                    self.surfaceSettings = SurfaceSettings(surfaceSettings)
            hangarScenario = findSection(data, 'hangarScenario')
            if hangarScenario:
                if self.hangarScenario:
                    self.hangarScenario.readData(surfaceSettings)
                else:
                    self.hangarScenario = HangarScenario(hangarScenario)
            damageEffects = findSection(data, 'damageEffects')
            if self.damageEffects:
                self.damageEffects.readData(damageEffects)
            else:
                self.damageEffects = DamageEffects(damageEffects)
            cameraEffectsData = findSection(data, 'cameraEffects')
            if self.cameraEffects:
                self.cameraEffects.readData(cameraEffectsData)
            else:
                self.cameraEffects = CameraEffects(cameraEffectsData)
            accelFovData = findSection(data, 'accelerationFov')
            if self.accelFovSettings:
                self.accelFovSettings.readData(accelFovData)
            else:
                self.accelFovSettings = AccelerationFovSettings(accelFovData)
            gunnerAnimatorSettingsSect = findSection(data, 'gunnerAnimatorSettings')
            if gunnerAnimatorSettingsSect is not None:
                for key, animatorSettingsSect in gunnerAnimatorSettingsSect.items():
                    id = animatorSettingsSect.readInt('partId', -1)
                    settings = self.gunnerAnimatorSettings.get(id)
                    if settings is not None:
                        settings.readData(animatorSettingsSect)
                    else:
                        settings = GunnerHeadAnimatorSettings(animatorSettingsSect)
                        self.gunnerAnimatorSettings[id] = settings

            if IS_EDITOR:
                self.__data = data
        return

    def save(self):
        if IS_EDITOR:
            temp = Math.Vector3(self.cameraOffset)
            self.cameraOffset /= WORLD_SCALING
            writeValue(self, self.__data, 'cameraOffset', Math.Vector3(0, 0, 0))
            self.cameraOffset = temp


class AirCraftSoundSettings():

    def __init__(self, data = None):
        self.readData(data)
        self.passbyBulletCollisionSphereRadius *= WORLD_SCALING
        self.downedTriggerAltitude *= WORLD_SCALING

    def readData(self, data):
        if data != None:
            readValue(self, data, 'rotor', '')
            readValue(self, data, 'rotorEnemy', '')
            readValue(self, data, 'rotorDamaged', '')
            readValue(self, data, 'rotorCockpitMono', '')
            readValue(self, data, 'rotorCockpitL', '')
            readValue(self, data, 'rotorCockpitR', '')
            readValue(self, data, 'rotorOverheat', '')
            readValue(self, data, 'rotorOverheatMax', '')
            readValue(self, data, 'rotorOverheatRelativeTempStart', 0.0)
            readValue(self, data, 'rotorSpectator', '')
            readValue(self, data, 'flaps', '')
            readValue(self, data, 'downed', '')
            readValue(self, data, 'downedEnv', '')
            readValue(self, data, 'downedTriggerAltitude', 0.0)
            readValue(self, data, 'windOutside', '')
            readValue(self, data, 'windCockpit', '')
            readValue(self, data, 'airplaneDamage', '')
            readValue(self, data, 'airplaneVibe', '')
            readValue(self, data, 'passbyBulletCollisionSphereRadius', 0.0)
            readValue(self, data, 'passbyBulletSoundInstanceNumMax', 0)
            readValue(self, data, 'rotorForceApplyTerm', 0.0)
            readValue(self, data, 'hitMaterialID', 0)
        return


class ObservSector():

    def __init__(self, data = None):
        if data != None:
            readValue(self, data, 'direction', Math.Vector3(0, 0, 0))
            readValue(self, data, 'angle', 360)
            readValue(self, data, 'range', 330)
            self.direction.normalise()
        return


class DamageEffects():

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data):
        updateValue(self, data, 'destroy_air', '')
        updateValue(self, data, 'destroy_water', '')
        updateValue(self, data, 'destroy_terrain', '')
        updateValue(self, data, 'crashed_fire', '')
        updateValue(self, data, 'receive_damage_own_1', '')
        updateValue(self, data, 'receive_damage_own_2', '')
        updateValue(self, data, 'receive_damage_other_1', '')
        updateValue(self, data, 'receive_damage_other_2', '')
        updateValue(self, data, 'receive_damage_terrain', '')
        updateValue(self, data, 'receive_damage_water', '')
        updateValue(self, data, 'receive_damage_tree', '')
        updateValue(self, data, 'effectFire', 'FIRING')


class CameraEffects():

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data):
        updateValue(self, data, 'shooting', '')
        updateValue(self, data, 'cameraEffectID', '')
        updateValue(self, data, 'relativeAccelerationLimits', Math.Vector2(0, 0))
        if data:
            outputSettingsSection = findSection(data, 'cameraEffectOutputSettings')
            if outputSettingsSection:
                for outputSettingsData in outputSettingsSection.values():
                    outputSettings = CameraEffectOutputSettings(outputSettingsData)
                    self.outputSettings[outputSettings.id] = outputSettings


class CameraEffectOutputSettings():

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data = None):
        updateValue(self, data, 'id', '')
        updateValue(self, data, 'settingHalflife', 0.0)


class AccelerationFovSettings():

    def __init__(self, data = None):
        self.outputSettings = {}
        self.readData(data)

    def readData(self, data):
        updateValue(self, data, 'cameraEffectID', '')
        updateValue(self, data, 'relativeAccelerationLimits', Math.Vector2(0, 0))
        if data:
            outputSettingsSection = findSection(data, 'cameraEffectOutputSettings')
            if outputSettingsSection:
                for outputSettingsData in outputSettingsSection.values():
                    outputSettings = CameraEffectOutputSettings(outputSettingsData)
                    self.outputSettings[outputSettings.id] = outputSettings


class DecalSettings():

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data = None):
        if data != None:
            readValue(self, data, 'id', -1)
            readValue(self, data, 'texture', '')
            readValue(self, data, 'icoPath', '')
            if data.has_key('bottomColor'):
                setattr(self, 'bottomColor', data.readVector4('bottomColor', Math.Vector4(0, 0, 0, 0)))
            if data.has_key('reflectionColor'):
                setattr(self, 'reflectionColor', data.readVector4('reflectionColor', Math.Vector4(0, 0, 0, 0)))
            if data.has_key('glossinessOffset'):
                readValue(self, data, 'glossinessOffset', 0.0)
        return


class DecalGroup():

    def __init__(self, data = None):
        self.decals = {}
        self.readData(data)

    def readData(self, data = None):
        if data != None:
            readValue(self, data, 'name', 'unknown')
            self.decals = {}
            decalsSection = findSection(data, 'decals')
            if decalsSection:
                for decalData in decalsSection.values():
                    decal = DecalSettings(decalData)
                    self.decals[decal.id] = decal

        return

    def getDecalTexNameByID(self, id):
        if id in self.decals:
            return self.decals[id].texture
        else:
            DBLOG_ERROR("Can't find decal with ID: " + str(id))
            return ''

    def getDecal(self, id):
        if id in self.decals:
            return self.decals[id]
        else:
            DBLOG_ERROR("Can't find decal with ID: " + str(id))
            return None


class DecalsSettings():

    def __init__(self, data = None):
        self.decalGroups = {}
        self.readData(data)

    def readData(self, data = None):
        self.decalGroups = {}
        if data != None:
            for decalGroupData in data.values():
                dg = DecalGroup(decalGroupData)
                self.decalGroups[dg.name] = dg

        return


class SurfaceSettings():

    def __init__(self, data = None):
        self.decalsSettings = None
        self.readData(data)
        if IS_EDITOR:
            self.__data = data
        return

    def readData(self, data):
        if data != None:
            readValue(self, data, 'detailTexture', '')
            decalSettingsData = findSection(data, 'decalsSettings')
            if self.decalsSettings:
                self.decalsSettings.readData(decalSettingsData)
            else:
                self.decalsSettings = DecalsSettings(decalSettingsData)
        return

    def updateCamouflages(self, decals):
        if IS_EDITOR:
            if self.__data != None:
                self.decalsSettings = None
                sectionName = 'decalsSettings'
                decalSettingsData = findSection(self.__data, sectionName)
                self.__data.deleteSection(decalSettingsData)
                decalSettingsData = self.__data.createSection(sectionName)
                for name, decalList in decals.items():
                    dacalGroupSection = decalSettingsData.createSection('decalGroup')
                    dacalGroupSection.writeString('name', name)
                    decalsSection = dacalGroupSection.createSection('decals')
                    for id, decal in decalList.items():
                        decalSection = decalsSection.createSection('decal')
                        decalSection.writeInt('id', id)
                        decalSection.writeString('texture', decal['texture'])
                        if decal['icoPath'] != '':
                            decalSection.writeString('icoPath', decal['icoPath'])
                        if 'bottomColor' in decal:
                            decalSection.writeVector4('bottomColor', decal['bottomColor'])
                        if 'reflectionColor' in decal:
                            decalSection.writeVector4('reflectionColor', decal['reflectionColor'])
                        if 'glossinessOffset' in decal:
                            decalSection.writeFloat('glossinessOffset', decal['glossinessOffset'])

                self.decalsSettings = DecalsSettings(decalSettingsData)
        return


class HangarScenario():

    def __init__(self, data = None):
        self.scenario = ''
        self.excludeEvents = []
        self.readData(data)
        if IS_EDITOR:
            self.__data = data

    def readData(self, data):
        if data != None:
            readValue(self, data, 'scenario', '')
            excludeEvents = findSection(data, 'excludeEvents')
            if excludeEvents:
                for event in excludeEvents.values():
                    self.excludeEvents.append(event.asString)

        return


class AirCraftTunes():

    def __init__(self, data = None, newDatabase = None):
        self.visualSettings = None
        self.soundSettings = None
        self.observSectors = None
        self.partsSettings = None
        self.price = None
        self.description = None
        self.readData(data, newDatabase)
        return

    def calculateHP(self, installedLogicalParts, modifier = 1):
        """
        Calculates aircraft's HP
        @param installedLogicalParts: parts that will be used in calculation or None for default parts
        """
        if installedLogicalParts is None:
            installedLogicalParts = [0] * LOGICAL_PART.COUNT
        hull = self.flightModel.hull[installedLogicalParts[LOGICAL_PART.HULL]]
        return hull.HP * modifier

    def calculateMass(self, installedLogicalParts = None):
        """
        Calculates aircraft's mass
        @param installedLogicalParts: parts that will be used in calculation or None for default parts
        """
        if installedLogicalParts is None:
            installedLogicalParts = [0] * LOGICAL_PART.COUNT
        hull = self.flightModel.hull[installedLogicalParts[LOGICAL_PART.HULL]]
        engine = self.flightModel.engine[installedLogicalParts[LOGICAL_PART.ENGINE]]
        turret = self.flightModel.turret[installedLogicalParts[LOGICAL_PART.TURRET]]
        return hull.mass + engine.mass + turret.mass

    def getPartsList(self):
        if self.partsSettings:
            return self.partsSettings.getPartsOnlyList()
        else:
            return None

    def getPartByID(self, partID):
        if self.partsSettings:
            return self.partsSettings.getPartByID(partID)
        else:
            return None

    def postLoadTransform(self):
        if self.visualSettings:
            self.visualSettings.postLoadTransform()

    def readData(self, data, newDatabase):
        r"""
                Loads tunes and some other data from XML.
                For newDatabase structure please refer to \depot        runc\game\hammer
        es\scripts\common\_aircrafts_db.py
                _aircrafts_db.py is autogenerated from aircrafts.xml
                Please see Confluence docs for more info.
        
                Also please note that flight model params are overloaded from newDatabase, see below at the end of method.
                """
        if data != None:
            airplaneData = findSection(data, 'Airplane')
            if airplaneData is None and newDatabase is not None:
                LOG_ERROR('No Airplane section for last .xml file. Set config_consts.DB_ENABLE_LOG to True for get more information')
                sys.exit()
            if IS_EDITOR:
                self.__data = airplaneData
            if airplaneData is not None:
                params = (('name', ''),
                 ('longName', ''),
                 ('model', ''),
                 ('stealthFactor', 1.0),
                 ('collisionDamageCfc', 0.001),
                 ('autoPilotStartAlt', 60.0),
                 ('autoPilotEndAlt', 100.0),
                 ('hudIcoPath', NOT_AVAILABLE),
                 ('iconPath', NOT_AVAILABLE),
                 ('previewIconPath', NOT_AVAILABLE),
                 ('treeIconPath', NOT_AVAILABLE))
                if IS_EDITOR:
                    self.__params = params
                readValues(self, airplaneData, params)
                visualSettingsData = findSection(airplaneData, 'visualSettings')
                if self.visualSettings:
                    self.visualSettings.readData(visualSettingsData)
                else:
                    self.visualSettings = AirCraftVisualSettings(visualSettingsData)
                partsSettingsData = findSection(airplaneData, 'parts')
                if self.partsSettings:
                    self.partsSettings.readData(partsSettingsData)
                else:
                    self.partsSettings = PartsTunes(partsSettingsData)
                if IS_DEVELOPMENT and IS_CELLAPP:
                    try:
                        requiredCritableStatesSet = set([1,
                         2,
                         3,
                         4])
                        from EntityHelpers import getPartEnum
                        from AvatarCritsSystem import AvatarCritsSystem

                        def checkAffectedPartsMissedStates(upgrade):
                            for state in upgrade.states.itervalues():
                                for aPartID, aPartMinState in state.affectedParts:
                                    aPart = self.partsSettings.getPartByID(aPartID)
                                    if aPart:
                                        for aUpgrade in aPart.upgrades.itervalues():
                                            if aPartMinState not in set(aUpgrade.states):
                                                yield (upgrade.id,
                                                 aPartID,
                                                 aUpgrade.id,
                                                 aPartMinState)

                                    else:
                                        yield (upgrade.id, aPartID)

                        for part in self.partsSettings.getPartsOnlyList():
                            for upgrade in part.upgrades.itervalues():
                                if getPartEnum(upgrade) in AvatarCritsSystem.CRITABLE_PARTS:
                                    absentStates = requiredCritableStatesSet.difference(set(upgrade.states))
                                    if absentStates:
                                        LOG_ERROR(part.partId, part.name, 'PARTS_VALIDATION_ERROR critable part has no all required states:', upgrade.id, absentStates)
                                missedStates = list(checkAffectedPartsMissedStates(upgrade))
                                if missedStates:
                                    LOG_ERROR(part.partId, part.name, upgrade.id, 'PARTS_VALIDATION_ERROR part has no such affected states:', missedStates)

                    except Exception as e:
                        import sys
                        LOG_DEBUG_DEV(sys.exc_info())

                soundSettingsData = findSection(airplaneData, 'soundSettings')
                if self.soundSettings:
                    self.soundSettings.readData(soundSettingsData)
                else:
                    self.soundSettings = AirCraftSoundSettings(soundSettingsData)
                self.bboxes = BBoxes(findSection(airplaneData, 'bBoxes'))
                descriptionData = findSection(airplaneData, 'description')
                if self.description:
                    self.description.readData(descriptionData)
                else:
                    self.description = AirCraftDescription(descriptionData)
                if newDatabase:
                    for aircraft in newDatabase.aircraft:
                        if aircraft.name == self.name.lower():
                            aircraftData = aircraft
                            break
                    else:
                        aircraftData = None

                    if aircraftData == None:
                        DBLOG_ERROR("No new style database data found for aircraft '" + self.name + ' (' + self.longName + ')' + "', Please check aircrafts.xml and _aircrafts_db.py.")
                    else:
                        DBLOG_NOTE("New style database data available for aircraft '" + self.name + "', Ok.")
                        self.patch(aircraftData)
        return

    def patch(self, aircraftDB):
        """
        Patch current instance with new database data (see _aircrafts_db)
        @param aircraftDB:aircraft data from new database (see _aircrafts_db)
        """
        DBPatch.update(self, aircraftDB)

    def save(self):
        if IS_EDITOR:
            self.partsSettings.save()
            self.visualSettings.save()


class PivotData():

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data = None):
        readValue(self, data, 'name', 'unknown')
        readValue(self, data, 'position', Math.Vector3(0, 0, 0))
        readValue(self, data, 'direction', Math.Vector3(0, 0, 0))
        self.position *= AIRCRAFT_MODEL_SCALING


class PivotsTunes():

    def __init__(self, data = None):
        self.mountPoints = {}
        self.readData(data)

    def readData(self, data = None):
        if data != None:
            pivotsData = findSection(data, 'Pivots')
            if pivotsData != None:
                for sName, sData in pivotsData.items():
                    if sName == 'pivot':
                        pivot = PivotData(sData)
                        self.mountPoints[pivot.name] = pivot

        return


class MassData():

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data = None):
        if data != None:
            readValue(self, data, 'position', Math.Vector3(0, 0, 0))
            readValue(self, data, 'direction', Math.Vector3(0, 0, 0))
        else:
            self.position = Math.Vector3(0, 0, 0)
            self.direction = Math.Vector3(0, 0, 0)
        self.position *= AIRCRAFT_MODEL_SCALING
        return


class MassTunes():

    def __init__(self, data = None):
        self.mass = {}
        self.readData(data)

    def readData(self, data = None):
        if data != None:
            massData = findSection(data, 'HPmass')
            self.mass = MassData(massData)
        return


class AirCraftDescription():

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data):
        if data != None:
            readValue(self, data, 'textDescription', '')
            readValue(self, data, 'engineCapasityUnit', '')
            readValue(self, data, 'MARKET_AIRPLANE_ENGINE_CAPACITY', '')
            readValue(self, data, 'MARKET_AIRPLANE_WING_AREA', '')
            readValue(self, data, 'MARKET_AIRPLANE_GROUND_MAX_SPEED', '')
            readValue(self, data, 'MARKET_AIRPLANE_HEIGHT_MAX_SPEED', '')
            readValue(self, data, 'MARKET_AIRPLANE_RATE_OF_CLIMB', '')
            readValue(self, data, 'MARKET_AIRPLANE_FULL_TURN_TIME', '')
            readValue(self, data, 'MARKET_AIRPLANE_TURN_RADIUS', '')
            readValue(self, data, 'MARKET_AIRPLANE_WEIGHT_SECOND_VOLLEY', '')
        return