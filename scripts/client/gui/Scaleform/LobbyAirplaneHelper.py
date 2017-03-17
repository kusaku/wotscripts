# Embedded file name: scripts/client/gui/Scaleform/LobbyAirplaneHelper.py
import copy
from Helpers.i18n import localizeAirplane, localizeAirplaneLong, localizeComponents, localizeLobby, localizeAirplaneAny, localizeTooltips, localizeUpgrade
import _airplanesConfigurations_db
import consts
import db.DBLogic
import db.DBParts
from consts import BLOCK_TYPE, UPGRADE_TYPE, AIRCRAFT_CHARACTERISTIC, HANGAR_CHARACTERISTICS_LIST, calculateGunDPS, TURRET_DPS_TO_FIREPOWER_CFC, BULLET_FLY_DIST_CORRECTION
from clientConsts import PLANE_TYPE_ICO_PATH, PREBATTLE_PLANE_TYPE_NAME, PLANE_CLASS
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG
from gui.Scaleform.LobbyAirplaneWeapons import LobbyAirplaneWeapons
from gui.Scaleform.LobbyAirplaneModules import LobbyAirplaneModules
from Helpers.PerformanceSpecsHelper import getPerformanceSpecsTableDeprecated, DescriptionField, getDescriptionList, getGroupedDescriptionFields
from db.DBParts import buildPresentPartsMap
from gui.Scaleform.utils.MeasurementSystem import MeasurementSystem
from HelperFunctions import findIf
from operator import xor
from _airplanesConfigurations_db import airplanesConfigurationsList, airplanesConfigurations
import math
CAROUSEL_AIRPLANE = 0
SHOP_AIRPLANE = 1

class ModuleSpecsVO:
    TYPE_MASS = 0
    TYPE_DAMAGE = 1
    TYPE_EXPLOSION_RADIUS = 2
    TYPE_CALIBER = 3
    TYPE_ROUNDS_PER_SECOND = 4
    TYPE_SHELL_VELOCITY = 5
    TYPE_DPS = 6
    TYPE_HEALTH = 7
    TYPE_POWER = 8
    TYPE_MODULE_TYPE = 9
    TYPE_EFFECTIVE_DISTANCE = 10
    TYPE_YAW_SECTOR = 11
    TYPE_UP_SECTOR = 12
    TYPE_DOWN_SECTOR = 13

    def __init__(self, specType, name, value, unit, planeID, numericValue = None):
        self.specType = specType
        self.name = name
        self.value = value
        self.unit = unit
        self.planeID = planeID
        self.numericValue = value if numericValue is None else numericValue
        self.comparisonValue = None
        self.canCompare = self.specType != self.TYPE_MODULE_TYPE
        self.isImprove = False
        return

    def setCmpValue(self, cmpValue):
        self.comparisonValue = cmpValue
        if self.comparisonValue is None:
            self.isImprove = False
            return
        else:
            exlude = self.specType != self.TYPE_MASS and self.specType != self.TYPE_DOWN_SECTOR
            self.isImprove = xor(self.comparisonValue < 0, exlude)
            return


def _mkint(n):
    return int(round(n, 0))


def getTurretWeaponsList(planeID, turretID, partTypesMap = {}):
    weaponList = {}
    entity = db.DBLogic.g_instance.getAircraftData(planeID)
    presentPartsMap = buildPresentPartsMap(entity.airplane.partsSettings, partTypesMap)
    for partType in presentPartsMap.values():
        partName = partType.componentType
        if partName == 'Gunner1' or partName == 'Gunner2':
            turretSettings = db.DBLogic.g_instance.getTurretData(turretID)
            if turretSettings:
                weaponList[turretSettings.weaponName] = weaponList.get(turretSettings.weaponName, 0) + turretSettings.weaponCount
            else:
                LOG_ERROR("Can't find data for turret {0}, {1}. Check xml with same name or turrets list.xml", partName, turretID)
                continue

    return weaponList


def getShellDescription(shell, measurementSystem = None):
    specs = []
    ms = measurementSystem or MeasurementSystem()
    specs.append(ModuleSpecsVO(ModuleSpecsVO.TYPE_DAMAGE, localizeLobby('MODULES_CHARACTERISTICS_DAMAGE'), shell.explosionDamage, '', 0))
    specs.append(ModuleSpecsVO(ModuleSpecsVO.TYPE_EXPLOSION_RADIUS, localizeLobby('MODULES_CHARACTERISTICS_EXPLOSION_RADIUS'), _mkint(ms.getMeters(shell.explosionRadius / consts.WORLD_SCALING)), ', {0}'.format(ms.localizeHUD('ui_meter')), 0))
    return specs


def getSlotIdByWeaponName(planeID, weaponName, weaponList):
    retSlotID = None
    for slotID, configID in weaponList:
        weaponInfo = db.DBLogic.g_instance.getWeaponInfo(planeID, slotID, configID)
        if weaponInfo is not None:
            _, wName, _ = weaponInfo
            if wName == weaponName:
                retSlotID = slotID
                break
        elif weaponName is None:
            retSlotID = slotID
            break

    return retSlotID


def findSlotsByWeaponName(planeID, weaponName, upgradesSet = None):
    ret = []
    for cmpGlobalID in airplanesConfigurationsList[planeID]:
        planeConfig = airplanesConfigurations[cmpGlobalID]
        if upgradesSet is not None and set(planeConfig.modules) != upgradesSet:
            continue
        slotID = getSlotIdByWeaponName(planeID, weaponName, planeConfig.weaponSlots)
        if slotID is not None:
            ret.append(slotID)

    return ret


def getCommonSlot(planeID, weaponName, weaponNameNew, upgradesSet):
    slots1 = findSlotsByWeaponName(planeID, weaponName, upgradesSet)
    slots2 = findSlotsByWeaponName(planeID, weaponNameNew, None)
    commonSlot = list(set(slots1).intersection(set(slots2)))
    if commonSlot:
        return commonSlot[0]
    elif slots1:
        return slots1[0]
    else:
        return slots2[0]


def getConfigDistance(upgrades, newUpgrades, weapons, newWeapons):
    ret = abs(len(upgrades) - len(newUpgrades))
    ret = reduce(lambda acc, x: (acc + 1 if x not in upgrades else acc), newUpgrades, ret)
    ret = reduce(lambda acc, x: (acc + 1 if x not in weapons else acc), newWeapons, ret)
    return ret


def isWeaponInSameSlot(planeConfig, weaponName, slotID):
    for globalID in airplanesConfigurationsList[planeConfig.planeID]:
        cmpConfig = airplanesConfigurations[globalID]
        slots = dict(planeConfig.weaponSlots)
        cmpSlots = dict(cmpConfig.weaponSlots)
        if set(cmpConfig.modules) != set(planeConfig.modules) or slots == cmpSlots:
            continue
        if not all((slots[k] == v for k, v in cmpSlots.iteritems() if k != slotID)):
            continue
        weaponInfo = db.DBLogic.g_instance.getWeaponInfo(planeConfig.planeID, slotID, cmpSlots[slotID])
        if weaponInfo is not None:
            _, wName, _ = weaponInfo
            if wName == weaponName:
                return True

    return False


def adjustPlaneConfig(planeID, upgrades, weaponList, newUpgradeName, upgradeName, weaponSlot = None, newWeaponConfig = None):

    def retFunc(u, w):
        return (db.DBLogic.createGlobalID(planeID, u, w), u, w)

    oldUpgrade = db.DBLogic.g_instance.getUpgradeByName(upgradeName) if upgradeName else None
    if oldUpgrade is not None:
        isWeapon = oldUpgrade.type in UPGRADE_TYPE.WEAPON
    else:
        isWeapon = False
    if newUpgradeName is None and not isWeapon:
        return retFunc(upgrades, weaponList)
    upgrade = db.DBLogic.g_instance.getUpgradeByName(newUpgradeName) if newUpgradeName else None
    minConfig = None
    minConfigDistance = None
    if upgrade is not None:
        isWeapon = upgrade.type in UPGRADE_TYPE.WEAPON
    newUpgrades = upgrades[:]
    newWeaponList = None
    if upgradeName is None:
        if not isWeapon:
            for upgradeName in upgrades:
                replaceUpgrade = db.DBLogic.g_instance.getUpgradeByName(upgradeName)
                if replaceUpgrade is None:
                    continue
                if replaceUpgrade.type == upgrade.type:
                    break
                upgradeName = None

    if isWeapon:
        if weaponSlot is not None and newWeaponConfig is not None:
            newWeaponList = []
            for slotInfo in weaponList:
                if slotInfo[0] == weaponSlot:
                    newWeaponList.append((slotInfo[0], newWeaponConfig))
                else:
                    newWeaponList.append(slotInfo)

    else:
        if upgradeName in newUpgrades:
            newUpgrades.remove(upgradeName)
        newUpgrades.append(upgrade.name)
    newWeaponList = newWeaponList or weaponList
    upgrades = set(upgrades)
    weaponSet = set(weaponList)
    planeName = db.DBLogic.g_instance.getAircraftData(planeID).airplane.name
    for cmpGlobalID in airplanesConfigurationsList[planeID]:
        planeConfig = airplanesConfigurations[cmpGlobalID]
        if upgrades == set(planeConfig.modules) and weaponSet == set(planeConfig.weaponSlots):
            continue
        if isWeapon:
            if getSlotIdByWeaponName(planeID, newUpgradeName, planeConfig.weaponSlots) is None:
                continue
        elif newUpgradeName not in planeConfig.modules:
            continue
        distance = getConfigDistance(newUpgrades, planeConfig.modules, newWeaponList, planeConfig.weaponSlots)
        if distance == 0:
            return retFunc(newUpgrades, newWeaponList)
        if newUpgradeName:
            upgrade = db.DBLogic.g_instance.getUpgradeByName(newUpgradeName)
            upgradeVariant = findIf(upgrade.variant, lambda var: var.aircraftName == planeName)
            parentUpgradeName = upgradeVariant.parentUpgrade[0].name
            if parentUpgradeName:
                parentUpgrade = db.DBLogic.g_instance.getUpgradeByName(parentUpgradeName)
                if parentUpgrade:
                    if parentUpgrade.type not in UPGRADE_TYPE.WEAPON:
                        if parentUpgradeName not in planeConfig.modules and parentUpgrade.type != upgrade.type:
                            continue
                    elif getSlotIdByWeaponName(planeID, parentUpgradeName, planeConfig.weaponSlots) is None:
                        if weaponSlot is None or not isWeaponInSameSlot(planeConfig, parentUpgradeName, weaponSlot):
                            continue
        if minConfigDistance is None or distance < minConfigDistance:
            minConfigDistance = distance
            minConfig = planeConfig

    if minConfig is None:
        return retFunc(list(upgrades), weaponList)
    else:
        return retFunc(minConfig.modules, minConfig.weaponSlots)


def getDiffModules(globalID, globalIDCmp, discardUpgradeName = None, discardSlotConfig = None):
    config1 = airplanesConfigurations[globalID]
    config2 = airplanesConfigurations[globalIDCmp]
    weaponSet = set(config2.weaponSlots).difference(set(config1.weaponSlots))
    weaponSet.discard(discardSlotConfig)
    requiredModules = set(config2.modules).difference(set(config1.modules))
    requiredModules.discard(discardUpgradeName)
    dbInstance = db.DBLogic.g_instance
    for slotConfig in weaponSet:
        wInfo = dbInstance.getWeaponInfo(config1.planeID, slotConfig[0], slotConfig[1])
        if wInfo is not None:
            _, wName, _ = wInfo
            requiredModules.add(wName)

    return requiredModules


def getUpgradeSpecs(upgrade, forPlaneID = None, cmpUpgrade = None, weaponSlot = None, weaponConfig = None):
    """
    :param upgrade: upgrade from upgrades_db
    :returns: a tuple of localized name and specs array of ModuleSpecsVO
    """
    nameID = upgrade.name
    localizedName = ''
    suitablePlanes = set([])
    specs = []
    dbInstance = db.DBLogic.g_instance
    ms = MeasurementSystem()
    shortDescription = ''
    for upgradeVariant in upgrade.variant:
        planeID = dbInstance.getAircraftIDbyName(upgradeVariant.aircraftName)
        suitablePlanes.add(planeID)
        if planeID is None:
            LOG_ERROR('getUpgradeSpecs() cannot find planeID by aircraft name (%s), module name is %s, please, correct DB' % (upgradeVariant.aircraftName, nameID))
            continue
        if forPlaneID is not None and planeID != forPlaneID:
            continue
        if upgrade.type == UPGRADE_TYPE.GUN:
            count = dbInstance.getGunsCount(planeID, nameID, weaponSlot, weaponConfig)
            localizedName = localizeComponents('WEAPON_NAME_' + nameID)
            gunData = dbInstance.getGunData(nameID)
            dps = _mkint(gunData.DPS)
            specs.append(ModuleSpecsVO(ModuleSpecsVO.TYPE_DPS, localizeLobby('MODULES_CHARACTERISTICS_DPS'), dps, '', planeID))
            specs.append(ModuleSpecsVO(ModuleSpecsVO.TYPE_ROUNDS_PER_SECOND, localizeLobby('MODULES_CHARACTERISTICS_TEMPO_OF_FIRE'), _mkint(gunData.RPM), localizeLobby('MODULES_CHARACTERISTICS_RATE_OF_FIRE_UNITS'), planeID))
            specs.append(ModuleSpecsVO(ModuleSpecsVO.TYPE_EFFECTIVE_DISTANCE, localizeLobby('MODULES_CHARACTERISTICS_EFFECTIVE_DIST'), _mkint(ms.getMeters(BULLET_FLY_DIST_CORRECTION * gunData.bulletFlyDist / consts.WORLD_SCALING)), ms.localizeMarket('MARKET_AIRPLANE_TURN_RADIUS'), planeID))
            shortDescription = '{0}: {1}'.format(localizeTooltips('TOOLTIP_FIXED_DPS'), dps)
        elif upgrade.type == UPGRADE_TYPE.ENGINE:
            localizedName = localizeComponents('NAME_MODULE_' + nameID)
            settings = dbInstance.getAircraftData(planeID)
            part = findIf(upgradeVariant.logicalPart, lambda p: p.type == 'engine')
            if part is None:
                LOG_ERROR("Part of type 'engine' not found", upgrade.__dict__, [ x.__dict__ for x in upgradeVariant.logicalPart ])
            partname = part.name
            engineParameters = filter(lambda m: m.name == partname, settings.airplane.flightModel.engine)
            if not engineParameters:
                LOG_ERROR("Can't find settings for engine", nameID, localizedName, partname)
            for eng in engineParameters:
                value, unit = (eng.power, localizeLobby('MARKET_AIRPLANE_ENGINE_CAPACITY_LS')) if hasattr(eng, 'power') else (eng.thrust / 10.0, ms.localizeMarket('MARKET_AIRPLANE_ENGINE_CAPACITY_KGS'))
                locID = 'MODULES_CHARACTERISTICS_ERROR_ENGINE'
                if hasattr(eng, 'power'):
                    locID = 'MODULES_CHARACTERISTICS_POWER'
                elif hasattr(eng, 'thrust'):
                    locID = 'MODULES_CHARACTERISTICS_THRIST'
                specs.append(ModuleSpecsVO(ModuleSpecsVO.TYPE_POWER, localizeLobby(locID), _mkint(ms.getKgs(value)), unit, planeID))
                specs.append(ModuleSpecsVO(ModuleSpecsVO.TYPE_MASS, localizeLobby('MARKET_AIRPLANE_MASS'), _mkint(ms.getKgs(eng.mass)), ms.localizeMarket('MARKET_AIRPLANE_MASS'), planeID))
                specs.append(ModuleSpecsVO(ModuleSpecsVO.TYPE_MODULE_TYPE, localizeLobby('MODULES_CHARACTERISTICS_TYPE'), localizeLobby('MODULES_CHARACTERISTICS_%s' % upgrade.equipmentType), '', planeID, 0))
                if forPlaneID is None or planeID == forPlaneID:
                    shortDescription = '{0}{2}: {1}'.format(localizeLobby(locID), _mkint(ms.getKgs(value)), unit)

        elif upgrade.type == UPGRADE_TYPE.PLANER:
            localizedName = localizeComponents('NAME_MODULE_' + nameID)
            settings = dbInstance.getAircraftData(planeID)
            part = findIf(upgradeVariant.logicalPart, lambda p: p.type == 'hull')
            if part is None:
                LOG_ERROR("Part of type 'hull' not found", upgrade.__dict__, [ x.__dict__ for x in upgradeVariant.logicalPart ])
            partname = part.name
            hullParameters = filter(lambda h: h.name == partname, settings.airplane.flightModel.hull)
            if not hullParameters:
                LOG_ERROR("Can't find settings for hull", nameID, localizedName, partname)
            for h in hullParameters:
                mass = h.mass if hasattr(h, 'mass') else 0.0
                hp = h.HP if hasattr(h, 'HP') else 0.0
                specs.append(ModuleSpecsVO(ModuleSpecsVO.TYPE_HEALTH, localizeLobby('MARKET_AIRPLANE_HEALTH'), hp, '', planeID))
                specs.append(ModuleSpecsVO(ModuleSpecsVO.TYPE_MASS, localizeLobby('MARKET_AIRPLANE_MASS'), _mkint(ms.getKgs(mass)), ms.localizeMarket('MARKET_AIRPLANE_MASS'), planeID))

            shortDescription = '{0}: {1}'.format(localizeLobby('MARKET_AIRPLANE_HEALTH'), hp)
        elif upgrade.type == UPGRADE_TYPE.ROCKET or upgrade.type == UPGRADE_TYPE.BOMB:
            localizedName = localizeComponents('WEAPON_NAME_' + nameID)
            shellDBGroupID, shellDescription = dbInstance.getShellComponentsGroupIDAndDescription(nameID)
            if shellDescription:
                for spec in getShellDescription(shellDescription):
                    spec.planeID = planeID
                    specs.append(spec)

            else:
                LOG_ERROR("Can't find settings for shell", nameID, localizedName)
            shortDescription = '{0}: {1}'.format(localizeLobby('MODULES_CHARACTERISTICS_DAMAGE'), shellDescription.explosionDamage)
        elif upgrade.type == UPGRADE_TYPE.TURRET:
            turret = dbInstance.getTurretData(nameID)
            settings = dbInstance.getAircraftData(planeID)
            part = findIf(upgradeVariant.logicalPart, lambda p: p.type == 'turret')
            if part is None:
                LOG_ERROR("Part of type 'turret' not found", upgrade.__dict__, [ x.__dict__ for x in upgradeVariant.logicalPart ])
            partname = part.name
            turretParameters = filter(lambda h: h.name == partname, settings.airplane.flightModel.turret)
            if not turretParameters:
                LOG_ERROR("Can't find settings for turret", nameID, localizedName, partname)
            mass = 0.0
            for h in turretParameters:
                if hasattr(h, 'mass'):
                    mass = h.mass
                    break

            localizedName = localizeUpgrade(upgrade)
            gunData = dbInstance.getGunData(turret.hangarSimilarGun)
            dps = _mkint(turret.DPS * TURRET_DPS_TO_FIREPOWER_CFC)
            specs.append(ModuleSpecsVO(ModuleSpecsVO.TYPE_DPS, localizeLobby('MODULES_CHARACTERISTICS_DPS'), dps, '', planeID))
            if gunData:
                specs.append(ModuleSpecsVO(ModuleSpecsVO.TYPE_EFFECTIVE_DISTANCE, localizeLobby('MODULES_CHARACTERISTICS_EFFECTIVE_DIST'), _mkint(ms.getMeters(turret.targetLockShootDistance / consts.WORLD_SCALING)), ms.localizeMarket('MARKET_AIRPLANE_TURN_RADIUS'), planeID))
                specs.append(ModuleSpecsVO(ModuleSpecsVO.TYPE_YAW_SECTOR, localizeLobby('MODULES_CHARACTERISTICS_TURRET_HORIZONTAL'), _mkint(math.degrees((turret.yawMax - turret.yawMin) / 2.0)), localizeLobby('MARKET_AIRPLANE_DEGREES'), planeID))
                specs.append(ModuleSpecsVO(ModuleSpecsVO.TYPE_UP_SECTOR, localizeLobby('MODULES_CHARACTERISTICS_TURRET_UP'), _mkint(math.degrees(turret.pitchMax)), localizeLobby('MARKET_AIRPLANE_DEGREES'), planeID))
                specs.append(ModuleSpecsVO(ModuleSpecsVO.TYPE_DOWN_SECTOR, localizeLobby('MODULES_CHARACTERISTICS_TURRET_DOWN'), _mkint(math.degrees(turret.pitchMin)), localizeLobby('MARKET_AIRPLANE_DEGREES'), planeID))
            if turret.weaponCount > 1:
                dps = '{0}x {1}'.format(turret.weaponCount, dps)
            shortDescription = '{0}: {1}'.format(localizeTooltips('TOOLTIP_FIXED_DPS'), dps)

    if cmpUpgrade is None or cmpUpgrade.name == nameID:
        return (localizedName,
         specs,
         suitablePlanes,
         shortDescription)
    else:
        _, cmpSpecs, _, _ = getUpgradeSpecs(cmpUpgrade, forPlaneID)
        for mainSpec in specs:
            if not mainSpec.canCompare:
                continue
            cmpSpec = findIf(cmpSpecs, lambda x: x.specType == mainSpec.specType, None)
            if cmpSpec is not None and mainSpec.numericValue != cmpSpec.numericValue:
                mainSpec.setCmpValue(mainSpec.numericValue - cmpSpec.numericValue)
                if mainSpec.specType == ModuleSpecsVO.TYPE_CALIBER:
                    mainSpec.setCmpValue(round(mainSpec.comparisonValue, 2))

        return (localizedName,
         specs,
         suitablePlanes,
         shortDescription)


class ExchangeExpItemVO:

    def __init__(self, aircraftID, freeExp, isPremium, isElite):
        airplaneData = db.DBLogic.g_instance.getAircraftData(aircraftID)
        self.aircraftID = aircraftID
        self.planeName = localizeAirplane(airplaneData.airplane.name)
        self.planeIcoPath = airplaneData.airplane.iconPath if airplaneData.airplane else 'n/a'
        self.planeType = airplaneData.airplane.planeType
        self.freeExp = freeExp
        self.isElite = isElite
        self.isPremium = isPremium
        planeStatus = self.isPremium * PLANE_CLASS.PREMIUM or self.isElite * PLANE_CLASS.ELITE or PLANE_CLASS.REGULAR
        self.planeTypeIcoPath = PLANE_TYPE_ICO_PATH.icon(self.planeType, planeStatus)


def getAirplaneASList(lobbyAirplaneList, planeID):
    airplaneASList = []
    for lobbyAirplane in lobbyAirplaneList:
        if planeID == CAROUSEL_AIRPLANE:
            airplaneASList.append(lobbyAirplane.getCarouselAirplaneObject())
        elif planeID == SHOP_AIRPLANE:
            airplaneASList.append(lobbyAirplane.getShopAirplaneObject())

    return airplaneASList


def getLobbyAirplane(aircraftID):
    aircraftID = int(aircraftID)
    airplaneData = db.DBLogic.g_instance.getAircraftData(aircraftID)
    if airplaneData is None:
        LOG_ERROR('updateCarouselResponse. plane is wrong. Airplane = ', aircraftID)
        return
    else:
        nationID = db.DBLogic.g_instance.getNationIDbyAircraftID(aircraftID)
        airplane = LobbyAirplane()
        import BWPersonality
        inv = BWPersonality.g_lobbyCarouselHelper.inventory
        try:
            airplane.nationID = nationID
            airplane.planeID = aircraftID
            airplane.name = localizeAirplane(airplaneData.airplane.name)
            airplane.longName = localizeAirplaneLong(airplaneData.airplane.name)
            if airplaneData.airplane.options.isDev:
                airplane.longName += ' (Dev)'
            airplane.hudIconPath = airplaneData.airplane.hudIcoPath if airplaneData.airplane else 'n/a'
            airplane.planeIconPath = airplaneData.airplane.iconPath if airplaneData.airplane else 'n/a'
            airplane.previewIconPath = airplaneData.airplane.previewIconPath if airplaneData.airplane else 'n/a'
            airplane.nationFlagPath = db.DBLogic.g_instance.getAircraftFlagPath(airplaneData.airplane.name)
            airplane.level = airplaneData.airplane.level if airplaneData.airplane else 0
            airplane.levelRomanNum = airplane.level
            airplane.mass = 0.0
            airplane.hitPoints = 0.0
            airplane.type = localizeLobby(PREBATTLE_PLANE_TYPE_NAME[airplaneData.airplane.planeType])
            airplane.isPremium = db.DBLogic.g_instance.isPlanePremium(aircraftID)
            airplane.isElite = inv.isAircraftElite(aircraftID)
            airplane.experience = inv.getAircraftExp(aircraftID)
            airplane.planeType = airplaneData.airplane.planeType
            airplane.isResearched = inv.isAircraftOpened(aircraftID)
            airplane.isBought = inv.isAircraftBought(aircraftID)
            airplane.updatePrice()
            airplane.researchExp = 0
            upgrade = db.DBLogic.g_instance.upgrades.get(airplaneData.airplane.name, None)
            if upgrade is not None and upgrade.variant[0].parentUpgrade:
                airplane.researchExp = int(upgrade.variant[0].parentUpgrade[0].experience)
            planeStatus = airplane.isPremium * PLANE_CLASS.PREMIUM or airplane.isElite * PLANE_CLASS.ELITE or PLANE_CLASS.REGULAR
            airplane.planeTypeIconPath = PLANE_TYPE_ICO_PATH.icon(airplane.planeType, planeStatus)
            upgradesList, aircraftList = db.DBLogic.g_instance.getAircraftUpgrades(aircraftID)
            defaultConfiguration = _airplanesConfigurations_db.getDefaultAirplaneConfiguration(aircraftID)
            upgradeInfoMaps = []
            for upgrade in upgradesList:
                info = inv.getUpgradeInfoMap(aircraftID, upgrade)
                info['isInstalled'] = any((m == upgrade.name for m in defaultConfiguration.modules))
                upgradeInfoMaps.append(info)

            airplane.modules = LobbyAirplaneModules(aircraftID, upgradeInfoMaps)
            airplane.weapons = LobbyAirplaneWeapons(aircraftID, None, list(defaultConfiguration.weaponSlots))
            from gui.Scaleform.LobbyAirplanePresets import LobbyAirplanePresets
            airplane.presets = LobbyAirplanePresets(aircraftID, airplane.modules, airplane.weapons, None, [ preset.name for preset in db.DBLogic.g_instance.getAircraftPresetsListByName(airplaneData.airplane.name) ], db.DBLogic.g_instance.getAircraftDefaultPresetFromName(airplaneData.airplane.name).name)
            airplane.presets.fillPresets()
        except:
            LOG_CURRENT_EXCEPTION()
            return

        from Account import PLANE_BLOCK_TYPE
        airplane.blockType = PLANE_BLOCK_TYPE.get(airplane.planeID, BLOCK_TYPE.UNLOCKED)
        return airplane


class LobbyAirplane(object):

    class __ShopAirplane:

        def __init__(self):
            pass

    class __CarouselAirplane:

        def __init__(self):
            pass

    class __CharacteristicVO:

        def __init__(self):
            self.name = ''
            self.longName = ''
            self.level = -1
            self.planeType = ''
            self.experience = -1

    def __init__(self):
        self.nationID = -1
        self.planeID = -1
        self.name = ''
        self.longName = ''
        self.hudIconPath = ''
        self.planeIconPath = ''
        self.planeTypeIconPath = ''
        self.previewIconPath = ''
        self.nationFlagPath = ''
        self.level = -1
        self.levelRomanNum = ''
        self.blockType = BLOCK_TYPE.UNLOCKED
        self.price = -1
        self.gold = -1
        self.researchExp = -1
        self.experience = 0
        self.mass = -1
        self.hitPoints = -1
        self.type = ''
        self.repairCost = 0
        self.isPrimary = False
        self.isResearched = False
        self.isBought = False
        self.planeType = -1
        self.partTypes = []
        self.weaponsSlot = []
        self.__performanceCharacteristicTable = None
        self.__descriptionFieldList = []
        self.__descriptionMain = None
        self.autoRepair = True
        self.autoRefill = True
        self.modules = None
        self.weapons = None
        self.presets = None
        self.sellPrice = None
        self.isPremium = False
        self.isElite = False
        self.__carouselAirplane = None
        self.__shopAirplane = None
        self.customization = None
        self.extraExperience = 0
        self.extraRemains = 0
        return

    def clearSpecsTable(self):
        self.__performanceCharacteristicTable = None
        return

    def isResearchAvailable(self):
        import BWPersonality
        return BWPersonality.g_lobbyCarouselHelper.inventory.isPlaneResearchAvailableOpened(self.planeID)

    def updatePrice(self):
        import BWPersonality
        price = BWPersonality.g_lobbyCarouselHelper.inventory.getAircraftPrice(self.planeID)
        self.price = int(price[0])
        self.gold = int(price[1])

    def makeElite(self):
        """
        Make plane elite
        """
        self.isElite = True
        if not self.isPremium:
            self.planeTypeIconPath = PLANE_TYPE_ICO_PATH.icon(self.planeType, PLANE_CLASS.ELITE)

    def destroy(self):
        if self.customization:
            self.customization.destroy()
            self.customization = None
        return

    def getShopAirplaneObject(self):
        planeStatus = self.isPremium * PLANE_CLASS.PREMIUM or self.isElite * PLANE_CLASS.ELITE or PLANE_CLASS.REGULAR
        if self.__shopAirplane is None:
            self.__shopAirplane = LobbyAirplane.__ShopAirplane()
        self.__shopAirplane.planeId = self.planeID
        self.__shopAirplane.nationId = self.nationID
        self.__shopAirplane.longName = self.longName
        self.__shopAirplane.price = self.price
        self.__shopAirplane.gold = self.gold
        self.__shopAirplane.levelRomanNum = self.levelRomanNum
        self.__shopAirplane.hudIconPath = self.hudIconPath
        self.__shopAirplane.isResearched = self.isResearched
        self.__shopAirplane.planeType = self.planeType
        self.__shopAirplane.type = self.type
        self.__shopAirplane.planeTypeIcoPath = PLANE_TYPE_ICO_PATH.icon(self.planeType, planeStatus)
        LOG_DEBUG('=gsao=', self.name, self.isPremium, self.isElite, self.__shopAirplane.planeTypeIcoPath)
        return self.__shopAirplane

    def getCarouselAirplaneObject(self):
        planeStatus = self.isPremium * PLANE_CLASS.PREMIUM or self.isElite * PLANE_CLASS.ELITE or PLANE_CLASS.REGULAR
        if self.__carouselAirplane is None:
            self.__carouselAirplane = LobbyAirplane.__CarouselAirplane()
        self.__carouselAirplane.nationID = self.nationID
        self.__carouselAirplane.planeID = self.planeID
        self.__carouselAirplane.name = self.name
        self.__carouselAirplane.longName = self.longName
        self.__carouselAirplane.planeIconPath = self.planeIconPath
        self.__carouselAirplane.nationFlagPath = self.nationFlagPath
        self.__carouselAirplane.level = self.level
        self.__carouselAirplane.levelRomanNum = self.levelRomanNum
        self.__carouselAirplane.blockType = self.blockType
        self.__carouselAirplane.repairCost = self.repairCost
        self.__carouselAirplane.isPrimary = self.isPrimary
        self.__carouselAirplane.planeType = self.planeType
        self.__carouselAirplane.type = self.type
        self.__carouselAirplane.autoRepair = self.autoRepair
        self.__carouselAirplane.autoRefill = self.autoRefill
        self.__carouselAirplane.sellPrice = self.sellPrice
        self.__carouselAirplane.experience = self.experience
        self.__carouselAirplane.isPremium = self.isPremium
        self.__carouselAirplane.isElite = self.isElite
        self.__carouselAirplane.planeTypeIcoPath = PLANE_TYPE_ICO_PATH.icon(self.planeType, planeStatus)
        self.__carouselAirplane.extraExperience = self.extraExperience
        self.__carouselAirplane.extraRemains = self.extraRemains
        return self.__carouselAirplane

    def __getDescriptionFields(self, forceBuild, aircraftForCompare, installedGlobalID, modify, measurementSystem = None):
        """
        @param forceBuild:
        @param aircraftForCompare:
        @param installedGlobalID:
        @return:
        """
        performanceCharacteristic = getPerformanceSpecsTableDeprecated(self, modify, installedGlobalID)
        if forceBuild or self.__performanceCharacteristicTable is not performanceCharacteristic:
            if performanceCharacteristic is not None:
                self.__descriptionFieldList = self.__addAirplaneDescriptionToList(aircraftForCompare, installedGlobalID, modify, measurementSystem)
            else:
                self.__descriptionFieldList = []
            self.__performanceCharacteristicTable = performanceCharacteristic
        return self.__descriptionFieldList

    def getHangarDescriptionFields(self, forceBuild = False, aircraftForCompare = None, installedGlobalID = None):
        """
        Hangar descriptions list
        @param forceBuild:
        @param aircraftForCompare:
        @param installedGlobalID:
        @return:
        """
        return filter(lambda item: item.type in HANGAR_CHARACTERISTICS_LIST, self.__getDescriptionFields(forceBuild, aircraftForCompare, installedGlobalID, aircraftForCompare is None and installedGlobalID is None))

    def getGroupedDescriptionFields(self, forceBuild, aircraftForCompare, installedGlobalID, modify, measurementSystem = None):
        """
        @param forceBuild:
        @param aircraftForCompare:
        @param installedGlobalID:
        @return: {<main characteristic type> : <DescriptionFieldsGroup>, ...}
        """
        descriptionList = self.__getDescriptionFields(forceBuild, aircraftForCompare, installedGlobalID, modify, measurementSystem)
        return getGroupedDescriptionFields(descriptionList)

    def getCharacteristicVO(self):
        planeStatus = self.isPremium * PLANE_CLASS.PREMIUM or self.isElite * PLANE_CLASS.ELITE or PLANE_CLASS.REGULAR
        characteristicVO = LobbyAirplane.__CharacteristicVO()
        characteristicVO.name = self.name
        characteristicVO.longName = self.longName
        characteristicVO.level = self.level
        characteristicVO.planeType = self.type
        characteristicVO.planeTypeID = self.planeType
        characteristicVO.experience = self.experience
        characteristicVO.icoPath = PLANE_TYPE_ICO_PATH.icon(self.planeType, planeStatus)
        return characteristicVO

    def getMainDescription(self):
        if self.__descriptionMain is None:
            entity = db.DBLogic.g_instance.getAircraftData(self.planeID)
            descriptionLocalizeID = entity.airplane.description.textDescription
            self.__descriptionMain = localizeAirplaneAny(descriptionLocalizeID)
        return self.__descriptionMain

    def __addAirplaneDescriptionToList(self, aircraftForCompare, installedGlobalID, modify, measurementSystem = None):
        if aircraftForCompare is not None:
            compareSpecsTable = getPerformanceSpecsTableDeprecated(aircraftForCompare, False, None)
        else:
            compareSpecsTable = None
        specsTable = getPerformanceSpecsTableDeprecated(self, modify, installedGlobalID)
        if installedGlobalID is None:
            upgrades = [ upgrade['name'] for upgrade in self.modules.getInstalled() ]
            installedGlobalID = db.DBLogic.createGlobalID(self.planeID, upgrades, self.weapons.getInstalledWeaponsList())
        return getDescriptionList(specsTable, installedGlobalID, compareSpecsTable, measurementSystem) + self.getWeaponDescriptionList()

    def getWeaponDescriptionList(self):
        ret = []
        if self.weapons is not None:
            weaponConfigFinalData = {}
            weaponsInstalledConfigurationsList = self.weapons.getInstalledConfigurations()
            for weaponConfiguration in weaponsInstalledConfigurationsList:
                if weaponConfiguration.neededCount > 0:
                    weaponGroup = weaponConfiguration.weaponName
                    if weaponGroup in weaponConfigFinalData:
                        weaponConfigFinalData[weaponGroup].value = str(int(weaponConfigFinalData[weaponGroup].value) + weaponConfiguration.neededCount)
                        continue
                    t = db.DBLogic.g_instance.upgrades[weaponConfiguration.weaponNameID].type
                    if t == UPGRADE_TYPE.GUN:
                        gunData = db.DBLogic.g_instance.getGunData(weaponConfiguration.weaponNameID)
                        gunProfile = db.DBLogic.g_instance.getGunProfileData(gunData.gunProfileName)
                        iconPath = gunProfile.ttxIcoPath
                    else:
                        iconPath = UPGRADE_TYPE.TTX_ICON_PATH_MAP[t]
                    if t == UPGRADE_TYPE.BOMB or t == UPGRADE_TYPE.ROCKET:
                        value = localizeLobby('AMMO_TEMPLATE_HAVE-NEEDED', have=weaponConfiguration.installedCount, needed=weaponConfiguration.neededCount)
                    else:
                        value = weaponConfiguration.neededCount
                    weaponConfigFinalData[weaponGroup] = DescriptionField(weaponConfiguration.weaponName, str(value), '', '', '', False, 0, True, iconPath, AIRCRAFT_CHARACTERISTIC.WEAPON_LIST, None, 0)

            for weaponGroup in weaponConfigFinalData:
                ret.append(weaponConfigFinalData[weaponGroup])

        else:
            LOG_ERROR('weaponConfiguration not found for airplane', self.planeID)
        weaponList = self.getInstalledTurretsList()
        for upgradeName, count in weaponList.iteritems():
            item = DescriptionField(localizeLobby('MARKET_AIRPLANE_TURRET') + localizeUpgrade(db.DBLogic.g_instance.upgrades[upgradeName]), str(count), '', '', '', False, 0, True, UPGRADE_TYPE.TTX_ICON_PATH_MAP[UPGRADE_TYPE.TURRET], AIRCRAFT_CHARACTERISTIC.WEAPON_LIST, None, 0)
            ret.append(item)

        return ret

    def getInstalledTurretsList(self):
        """
        Installed turrets weapons list
        @return:
        """
        weaponList = {}
        for module in self.modules.getInstalled():
            upgrade = db.DBLogic.g_instance.upgrades[module['name']]
            if upgrade.type == UPGRADE_TYPE.TURRET:
                weaponList[upgrade.name] = weaponList.get(upgrade.name, 0) + 1

        return weaponList

    def sendUpgradesListToAS(self, sender):
        planeWeapons = self.weapons
        planeWeapons.update()

    def previewPreset(self, modulesList, weaponsList):
        """
        set modulesList and weaponsList to abstract LobbyAirplane <vehicleInfo>
        @param modulesList:  preset.module list for install
        @param weaponsList:  preset.weapon list for install
        @return: vehicle with installed modulesList and weaponsList
        """
        vehicleInfo = copy.deepcopy(self)
        vehicleInfo.modules.setInstalledModules(modulesList)
        vehicleInfo.partTypes = vehicleInfo.modules.getPartTypes()
        weaponList = [ (weapon['slot'], weapon['configuration']) for weapon in weaponsList ]
        if vehicleInfo.weapons is not None:
            vehicleInfo.weapons.setInstalledWeapons(weaponList)
            presetShellsCount = []
            for w in vehicleInfo.weapons.getInstalledConfigurations():
                u = db.DBLogic.g_instance.upgrades.get(w.weaponNameID, None)
                if u:
                    presetShellsCount.append(w.neededCount)

        return vehicleInfo