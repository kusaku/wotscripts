# Embedded file name: scripts/client/Helpers/PerformanceSpecsHelper.py
from debug_utils import LOG_ERROR
import _performanceCharacteristics_db
import db
from consts import CHARACTERISTICS_LOCALIZATION_MAP, AIRCRAFT_CHARACTERISTIC, CHARACTERISTICS_HINTS_MAP, SPECS_KEY_MAP, MAIN_CHARACTERISTICS_LIST, ADDITIONAL_CHARACTERISTICS_PARENTS_MAP
from Helpers.i18n import localizeLobby, localizeTooltips
from gui.Scaleform.utils.MeasurementSystem import MeasurementSystem
from HelperFunctions import wowpRound
from _performanceCharacteristics_db import PC
import types
from _equipment_data import ModsTypeEnum as EquipmentModsTypeEnum
from _skills_data import ModsTypeEnum as SkillModsTypeEnum
from _skills_data import SkillDB
from Helpers.cache import getFromCache
from SkillsHelper import calculateCommonAndImprovedSkillValue
SpecsDescriptionList = [{'tag': AIRCRAFT_CHARACTERISTIC.HEALTH,
  'isPrimary': 1,
  'iconPath': 'icons/characteristics/iconCharStrength.png'},
 {'tag': AIRCRAFT_CHARACTERISTIC.MASS,
  'isPrimary': 0,
  'iconPath': 'icons/characteristics/iconCharMass.png'},
 {'tag': AIRCRAFT_CHARACTERISTIC.GUNS_FIRE_POWER,
  'isPrimary': 1,
  'iconPath': 'icons/characteristics/iconCharFirePower.png'},
 {'tag': AIRCRAFT_CHARACTERISTIC.SPEED,
  'isPrimary': 1,
  'iconPath': 'icons/characteristics/iconCharSpeed.png'},
 {'tag': AIRCRAFT_CHARACTERISTIC.MANEUVERABILITY,
  'isPrimary': 1,
  'iconPath': 'icons/characteristics/iconCharMobility.png'},
 {'tag': AIRCRAFT_CHARACTERISTIC.GROUND_MAX_SPEED,
  'isPrimary': 0,
  'iconPath': 'icons/characteristics/iconCharSpeedGround.png'},
 {'tag': AIRCRAFT_CHARACTERISTIC.HEIGHT_MAX_SPEED,
  'isPrimary': 0,
  'iconPath': 'icons/characteristics/iconCharSpeedSky.png'},
 {'tag': AIRCRAFT_CHARACTERISTIC.DIVE_SPEED,
  'isPrimary': 0,
  'iconPath': ''},
 {'tag': AIRCRAFT_CHARACTERISTIC.STALL_SPEED,
  'isPrimary': 0,
  'iconPath': ''},
 {'tag': AIRCRAFT_CHARACTERISTIC.RATE_OF_CLIMB,
  'isPrimary': 0,
  'iconPath': 'icons/characteristics/iconCharRateOfClimb.png'},
 {'tag': AIRCRAFT_CHARACTERISTIC.AVERAGE_TURN_TIME,
  'isPrimary': 0,
  'iconPath': 'icons/characteristics/iconCharTurnPeriod.png'},
 {'tag': AIRCRAFT_CHARACTERISTIC.OPTIMAL_MANEUVER_SPEED,
  'isPrimary': 0,
  'iconPath': 'icons/characteristics/iconCharTurnPeriod.png'},
 {'tag': AIRCRAFT_CHARACTERISTIC.ROLL_MANEUVERABILITY,
  'isPrimary': 0,
  'iconPath': ''},
 {'tag': AIRCRAFT_CHARACTERISTIC.CONTROLLABILITY,
  'isPrimary': 0,
  'iconPath': ''},
 {'tag': AIRCRAFT_CHARACTERISTIC.ALT_PERFORMANCE,
  'isPrimary': 1,
  'iconPath': ''},
 {'tag': AIRCRAFT_CHARACTERISTIC.OPTIMAL_HEIGHT,
  'isPrimary': 0,
  'iconPath': ''}]

class ProjectileInfo(object):

    def __init__(self, slotID, configID, maxCount, curCount):
        self.curCount = curCount
        self.maxCount = maxCount
        self.slotID = slotID
        self.configurationID = configID


def compareSpecsValue(specsTable, value, param):
    if specsTable is not None and value is not None:
        keyOther, valueOther, unitOther, largerIsBetterOther, isPrimary, iconPath = getAirplaneDescriptionPair(specsTable, param)
        comparsionValue = value - valueOther
        if comparsionValue != 0.0:
            comparsionValueStr = '%s%s' % ('+' if comparsionValue > 0 else '-', abs(comparsionValue))
            isImprove = (value > valueOther) == largerIsBetterOther
            return (comparsionValueStr, isImprove)
    return ('', True)


def getPerformanceSpecsDescriptions(globalID, modify = False, slotsInfo = None, equipment = None, maxHealth = None):
    specsTable = getPerformanceSpecsTable(globalID, modify, slotsInfo, equipment)
    ret = {}
    dbInst = db.DBLogic.g_instance
    for param in SpecsDescriptionList:
        key, value, unit, largerIsBetter, isPrimary, iconPath = getAirplaneDescriptionPair(specsTable, param, maxHealth=maxHealth)
        if not (key is None and value is None and unit is None):
            tag = param['tag']
            specKey = SPECS_KEY_MAP[tag]
            maxValue = dbInst.getPlaneMaxSpec(dbInst.getPlaneIDByGlobalID(globalID), tag)
            maxValue, _, _ = _adjustSpec(maxValue, tag)
            item = DescriptionField(key, str(value), str(maxValue), unit, '', False, isPrimary, False, iconPath, tag, localizeTooltips(CHARACTERISTICS_HINTS_MAP[tag]) if tag in CHARACTERISTICS_HINTS_MAP else None, dbInst.getSpecRatioValue(globalID, specKey, specsTable))
            ret[tag] = item

    return ret


def __getCorrections(projectiles, diffs):
    corrections = {}
    for weaponConfig in projectiles:
        load = 1.0 - float(weaponConfig.curCount) / float(weaponConfig.maxCount)
        correction = diffs.get(db.DBLogic.slotLoadID([weaponConfig.slotID]), None)
        if correction:
            for k in correction.__dict__.keys():
                if not corrections.has_key(k):
                    corrections[k] = 0
                corrections[k] += getattr(correction, k) * load

    return corrections


def getPerformanceSpecsTable(globalID, modify = False, projectiles = None, equipment = None, crewList = None, maxHealth = None):
    specs = _performanceCharacteristics_db.airplanes.get(globalID, None)
    if specs is None:
        LOG_ERROR('getPerformanceSpecsTable() GlobalID {0} was not found in db'.format(globalID))
        return
    elif not modify:
        return roundSpecs(dict(specs.__dict__))
    else:
        diffs = specs.diff
        corrections = None
        if projectiles is not None:
            corrections = __getCorrections(projectiles, diffs)
            if corrections:
                for k in corrections.keys():
                    corrections[k] = getattr(specs, k) - corrections[k]

        if not corrections:
            corrections = dict(specs.__dict__)
        if maxHealth is not None:
            corrections['hp'] = int(maxHealth)
        else:
            skillModification = __getEquipmentSkillModificator(crewList)
            if equipment:
                __equipmentHPModification(corrections, equipment, skillModification)
        return roundSpecs(corrections)


def __equipmentHPModification(specsDict, equipment, skillModification):
    for eid in equipment:
        entry = db.DBLogic.g_instance.getEquipmentByID(eid)
        if entry is not None:
            for mod in entry.mods:
                if mod.type == EquipmentModsTypeEnum.MAIN_HP:
                    specsDict['hp'] = specsDict['hp'] * (1 + (mod.value_ - 1) * skillModification)

    return


def __getEquipmentSkillModificator(crewList):
    retValue = 1.0
    if crewList is None:
        return retValue
    else:
        for _, memberID in crewList:
            member = getFromCache([[memberID, 'crewmember']], 'ICrewMember')
            if member is None:
                continue
            skillValue = member['skillValue']
            specValue = calculateCommonAndImprovedSkillValue(skillValue)
            for skillID in member['skills']:
                for mod in SkillDB[skillID].mods:
                    if hasattr(mod, 'relation') and any((modType == SkillModsTypeEnum.MAIN_HP for modType in mod.relation.type)):
                        modificator = mod.states.good if hasattr(mod.states, 'good') else mod.states[0]
                        retValue *= 1 + (modificator - 1) * specValue / 100.0

        return retValue


def roundSpecs(stuff):
    return PC(**dict(((k, v) for k, v in stuff.iteritems() if isinstance(v, (types.IntType, types.LongType, types.FloatType)))))


def getPerformanceSpecsTableDeprecated(lobbyAirplane, modify, lobbyAirplaneGlobalID = None):
    planeID = lobbyAirplane.planeID
    if not lobbyAirplaneGlobalID:
        upgrades = [ upgrade['name'] for upgrade in lobbyAirplane.modules.getInstalled() ]
        lobbyAirplaneGlobalID = db.DBLogic.createGlobalID(planeID, upgrades, lobbyAirplane.weapons.getInstalledWeaponsList())
    characteristics = _performanceCharacteristics_db.airplanes.get(lobbyAirplaneGlobalID, None)
    if characteristics is None:
        LOG_ERROR('getPerformanceSpecsTableDeprecated - GlobalID(%s) not found in db, planeID=%s' % (lobbyAirplaneGlobalID, planeID))
        return
    elif not modify:
        return roundSpecs(characteristics.__dict__)
    else:
        diffs = characteristics.diff
        projectiles = lobbyAirplane.weapons.getInstalledProjectiles()
        corrections = __getCorrections(projectiles, diffs)
        if corrections:
            for k in corrections.keys():
                corrections[k] = getattr(characteristics, k) - corrections[k]

        else:
            corrections = dict(characteristics.__dict__)
        import BWPersonality
        if BWPersonality.g_lobbyCarouselHelper is not None:
            inv = BWPersonality.g_lobbyCarouselHelper.inventory
            skillModification = __getEquipmentSkillModificator(inv.getCrewList(planeID))
            __equipmentHPModification(corrections, inv.getEquipment(planeID), skillModification)
        return roundSpecs(corrections)


def _adjustSpec(value, tag, measurementSystem = None):
    largerIsBetter = True
    unit = None
    ms = measurementSystem or MeasurementSystem()
    if tag == AIRCRAFT_CHARACTERISTIC.HEALTH:
        value = int(round(value))
    elif tag == AIRCRAFT_CHARACTERISTIC.MASS:
        value = int(round(ms.getKgs(value)))
        unit = ms.localizeMarket(CHARACTERISTICS_LOCALIZATION_MAP[tag])
        largerIsBetter = False
    elif tag == AIRCRAFT_CHARACTERISTIC.GROUND_MAX_SPEED:
        value = int(round(ms.getKmh(value)))
        unit = ms.localizeMarket(CHARACTERISTICS_LOCALIZATION_MAP[tag])
    elif tag == AIRCRAFT_CHARACTERISTIC.HEIGHT_MAX_SPEED:
        value = int(round(ms.getKmh(value)))
        unit = ms.localizeMarket(CHARACTERISTICS_LOCALIZATION_MAP[tag])
    elif tag in (AIRCRAFT_CHARACTERISTIC.OPTIMAL_HEIGHT, AIRCRAFT_CHARACTERISTIC.ALT_PERFORMANCE):
        value = int(round(ms.getMeters(value)))
        if tag == AIRCRAFT_CHARACTERISTIC.OPTIMAL_HEIGHT:
            unit = ms.localizeMarket(CHARACTERISTICS_LOCALIZATION_MAP[tag])
    elif tag == AIRCRAFT_CHARACTERISTIC.RATE_OF_CLIMB:
        value = wowpRound(ms.getMeters(value), 1)
        unit = ms.localizeMarket(CHARACTERISTICS_LOCALIZATION_MAP[tag])
    elif tag == AIRCRAFT_CHARACTERISTIC.AVERAGE_TURN_TIME:
        value = wowpRound(value, 1)
        unit = localizeLobby('MARKET_AIRPLANE_FULL_TURN_TIME_SEC')
        largerIsBetter = False
    elif tag == AIRCRAFT_CHARACTERISTIC.GUNS_FIRE_POWER:
        value = int(round(value))
    elif tag == AIRCRAFT_CHARACTERISTIC.SPEED:
        value = int(round(value))
    elif tag == AIRCRAFT_CHARACTERISTIC.MANEUVERABILITY:
        value = int(round(value))
    elif tag == AIRCRAFT_CHARACTERISTIC.DIVE_SPEED:
        value = int(round(ms.getKmh(value)))
        unit = ms.localizeMarket(CHARACTERISTICS_LOCALIZATION_MAP[tag])
    elif tag == AIRCRAFT_CHARACTERISTIC.STALL_SPEED:
        value = int(round(ms.getKmh(value)))
        unit = ms.localizeMarket(CHARACTERISTICS_LOCALIZATION_MAP[tag])
        largerIsBetter = False
    elif tag == AIRCRAFT_CHARACTERISTIC.OPTIMAL_MANEUVER_SPEED:
        value = wowpRound(ms.getKmh(value), 1)
        unit = ms.localizeMarket(CHARACTERISTICS_LOCALIZATION_MAP[tag])
    elif tag == AIRCRAFT_CHARACTERISTIC.ROLL_MANEUVERABILITY:
        value = int(round(value))
        unit = ms.localizeMarket(CHARACTERISTICS_LOCALIZATION_MAP[tag])
    elif tag == AIRCRAFT_CHARACTERISTIC.CONTROLLABILITY:
        value = int(round(value))
    return (value, unit, largerIsBetter)


def getAirplaneDescriptionPair(characteristicsTable, param, measurementSystem = None, maxHealth = None):
    tag = param['tag']
    key = localizeLobby(CHARACTERISTICS_LOCALIZATION_MAP[tag])
    name, unit = (key.split('#') + [None])[:2]
    if characteristicsTable is not None:
        if tag == AIRCRAFT_CHARACTERISTIC.HEALTH and maxHealth is not None:
            value = maxHealth
        else:
            value = getattr(characteristicsTable, SPECS_KEY_MAP[tag])
        value, newUnit, largerIsBetter = _adjustSpec(value, tag, measurementSystem)
    else:
        LOG_ERROR('Characteristics table is empty')
        value = 0
        newUnit = 0
    return (name,
     value,
     newUnit or unit,
     largerIsBetter,
     param['isPrimary'],
     param['iconPath'])


class DescriptionFieldsGroup:

    def __init__(self):
        self.main = None
        self.additional = []
        return


class DescriptionField:

    def __init__(self, name, value, maxPlaneValue, unit, comparisonValue, isImprove, isPrimary, isWeapon, iconPath, type, hint, stars):
        self.name = name
        self.value = value
        self.maxPlaneValue = maxPlaneValue
        self.unit = unit
        self.comparisonValue = comparisonValue
        self.isImprove = isImprove
        self.isPrimary = isPrimary
        self.isWeapon = isWeapon
        self.icoPath = iconPath
        self.type = type
        self.hint = hint
        self.stars = stars


def getDescriptionList(specsTable, globalID, compareSpecsTable, measurementSystem = None):
    ret = []
    dbInst = db.DBLogic.g_instance
    for param in SpecsDescriptionList:
        key, value, unit, largerIsBetter, isPrimary, iconPath = getAirplaneDescriptionPair(specsTable, param, measurementSystem)
        if not (key is None and value is None and unit is None):
            comparisonValueStr, isImprove = compareSpecsValue(compareSpecsTable, value, param)
            tag = param['tag']
            maxValue = dbInst.getPlaneMaxSpec(dbInst.getPlaneIDByGlobalID(globalID), tag)
            maxValue, _, _ = _adjustSpec(maxValue, tag, measurementSystem)
            item = DescriptionField(key, str(value), str(maxValue), unit, comparisonValueStr, isImprove, isPrimary, False, iconPath, tag, localizeTooltips(CHARACTERISTICS_HINTS_MAP[tag]) if tag in CHARACTERISTICS_HINTS_MAP else None, dbInst.getSpecRatioValue(globalID, SPECS_KEY_MAP[tag], specsTable))
            ret.append(item)

    return ret


def getGroupedDescriptionFields(descriptionList):
    """
    @param forceBuild:
    @param aircraftForCompare:
    @param installedGlobalID:
    @return: {<main characteristic type> : <DescriptionFieldsGroup>, ...}
    """
    descriptionGroups = []
    descriptionGroupDict = {}

    def getGroup(groupId):
        if groupId in descriptionGroupDict:
            return descriptionGroupDict[groupId]
        group = DescriptionFieldsGroup()
        descriptionGroupDict[groupId] = group
        descriptionGroups.append(group)
        return group

    for descriptionField in descriptionList:
        if descriptionField.type in MAIN_CHARACTERISTICS_LIST:
            group = getGroup(descriptionField.type)
            group.main = descriptionField
        else:
            group = getGroup(ADDITIONAL_CHARACTERISTICS_PARENTS_MAP[descriptionField.type])
            group.additional.append(descriptionField)

    return descriptionGroups