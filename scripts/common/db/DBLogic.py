# Embedded file name: scripts/common/db/DBLogic.py
from itertools import ifilter
import BigWorld
from time import time
import _economics
import _upgrades_db
from config_consts import IS_DEVELOPMENT
from consts import AIRCRAFTS_PATH, BASES_PATH, IS_CLIENT, IS_EDITOR, IS_CELLAPP, IS_BASEAPP, ARENA_TYPE_PATH, TURRETS_PATH, EFFECTS_PATH, MATERIAL_NAMES_PATH, SPLINES_PATH, HELP_HINT_PATH, HUD_HINT_PATH, GUI_TEXTURES_PATH, LOGICAL_PART, CAMERA_MISC_PATH, ENTITY_COLOR_SCHEMA_PATH, UPGRADE_TYPE, LOGICAL_PART_STRING_TO_INT_TYPE, AIRPLANE_CAMERA_PRESETS_PATH, NAVIGATION_WINDOWS_PATH, TEAM_OBJECT_CLASS_NAMES, AVATAR_CLASS_NAMES, BLOCK_TYPE, BATTLE_DURATIONS, TIME_OUT_AFTER_BATTLE, COMPONENT_TYPE, calculateGunDPS, PLANE_KEYS, CREW_MEMBER, CAMERAEFFECTS_PATH, HANGAR_PATH, SOUND_SETTINGS_PATH, USER_HANGAR_SPACES_PATH, ARENA_TYPE, SPECS_KEY_MAP, LANDSCAPE_MATERIALS_PATH, FRACTION
from config_consts import DB_AIRCRAFT_CHECK
from Spline import Spline
from DBBaseObject import DBBaseObject
from DBHelpers import *
from DBArenaType import ArenaType
from DBTeamTurret import Turret
from DBEffects import Effects
from DBAirCrafts import AirCraft
from DBCamera import CameraSettings
from DBEntityColorScheme import EntityColorSchemes
from DBHelpHint import HelpHint
from DBNavigationWindows import NavigationWindows
from DBHUDHints import HudHints
from DBHangar import HangarConfig
from DBSoundsCommon import SoundsCommon
from DBCameraMisc import CameraMisc
from DBCameraEffects import CameraEffects
from _airplanesConfigurations_db import airplanesConfigurations, getDefaultAirplaneConfiguration, getAirplaneConfiguration, airplanesDefaultConfigurations, airplanesConfigurationsList
import _weapons
import _gunsProfiles
import os
from HelperFunctions import findIf, select, wowpRound
from db.DBComponents import ComponentsDB
from EntityHelpers import isAvatar, isTeamObject
from _weapons import AMMO_TYPE
import _performanceCharacteristics_db
import _warAction
try:
    from WWISE_ import audioPath
except ImportError:

    def audioPath():
        pass


from DBSoundSettings import *
if IS_CELLAPP or IS_BASEAPP:
    from _visibility import Visibility
import zlib
from _equipment_data import EquipmentDB
from _consumables_data import ConsumableDB
import _skills_data
from _skills_data import SkillDB, SkillWithRelationsDB
from _specializations_data import SpecializationsDB
from _crewnations_data import CrewNationsDB
from consts import CREW_BODY_TYPE
from DBPostInit import posInitDB
from debug_utils import CRITICAL_ERROR, LOG_TRACE, LOG_CURRENT_EXCEPTION
g_instance = None
CACHED_DB_FILE = 'scripts\\db\\cacheddb.bin'

def loadingProgressStep(name):
    pass


def tryPicleDB(db):
    import cPickle
    with open(CACHED_DB_FILE, 'wb') as stream:
        cPickle.dump(db, stream, protocol=2)


def tryUnpicleDB():
    import cPickle
    db = None
    try:
        with open(CACHED_DB_FILE, 'rb') as stream:
            db = cPickle.load(stream)
    except:
        pass

    return db


def initDB(onlyEntities = False, loadFromCache = False, skipEntities = False):
    global g_instance
    if g_instance == None:
        LOG_TRACE('start init DB')
        if loadFromCache:
            LOG_TRACE('load DB fromCahche')
            g_instance = tryUnpicleDB()
        if g_instance is None:
            g_instance = db(onlyEntities, skipEntities)
            if DB_AIRCRAFT_CHECK:
                checkAndPrintDBErrors()
        LOG_TRACE('end init DB')
    return g_instance


def checkAndPrintDBErrors():
    errors = g_instance.checkDB()
    LOG_TRACE('------------Start check db. DB_AIRCRAFT_CHECK == True--------------')
    for error in errors:
        DBLOG_ERROR(error[0] + ':' + ('bundleStop:' if getattr(error[1], 'bundleStop', False) else '') + error[1])

    LOG_TRACE('------------End check db------------')


def reinitDB():
    global g_instance
    g_instance = None
    return initDB()


def createGlobalID(id, upgrade, weaponSlots):
    """
    @param id: aircraft id
    @param upgrade: upgrades names list
    @param weaponSlots: <list of tuples of type (slotId, slotConfigurationId)>)
    @return:
    """
    upgrade.sort()
    weaponSlots.sort()
    return zlib.crc32(str((id, upgrade, weaponSlots)))


def slotLoadID(affectedSlots):
    return reduce(lambda acc, x: acc + 2 ** x, affectedSlots, 0)


def readEffectVariantData(data):
    effectData = {}
    usage = None
    for sName, sValue in data.items():
        if sName == 'usage':
            usage = sValue.readString('').upper()
        elif sName in ('instantHide', 'attachToTarget'):
            effectData[sName] = sValue.asBool
        elif sName in ('id', 'type', 'particleFile', 'SoundEffectID', 'texture', 'loftTexture', 'screenEffectID', 'attachType'):
            effectData[sName] = sValue.readString('')
        elif sName == 'delay':
            effectData[sName] = sValue.readVector2('')
        elif sName == 'decal':
            effectData[sName] = {}
            for dName, dValue in sValue.items():
                effectData[sName][dName] = dValue.readString('')

            try:
                effectData[sName]['size'] = float(effectData[sName]['size'])
            except:
                effectData[sName]['size'] = 1

        elif sName == 'effectSet':
            effectData[sName] = [ v.asString for k, v in sValue.items() if k == 'id' and v.asString != '' ]
            for k, v in sValue.items():
                if k == 'selectOne' and v.asBool:
                    effectData['selectOne'] = True
                    break

        else:
            effectData[sName] = float(sValue.readString(''))

    return (effectData, usage)


class NotExistingUpgradeVariant(Exception):

    def __init__(self, value):
        self.message = 'Cant find proper variant in installed upgrade %s' % str(value)


class EmptyInstalledUpgrades(Exception):

    def __init__(self, value):
        self.message = 'Not found installed upgrades on aircraft %s' % str(value)


class NotValidPreset(Exception):

    def __init__(self, value):
        self.message = 'Installed preset on aircraft %s not valid' % str(value)


class NotExistingUpgrade(Exception):

    def __init__(self, value):
        self.message = 'Installed not existing upgrade %s' % str(value)


class AircraftNotFoundException(Exception):
    """This exception is raised when trying to get an aircraft with illegal ID"""

    def __init__(self, wrongAircraftId):
        self.__wrongAircraftId = wrongAircraftId

    def __str__(self):
        return 'AircraftNotFoundException, aircraft Id ' + str(self.__wrongAircraftId) + ' not found in aircrafts database. Please fix list.xml or/and code.'


class UpgradeNotFoundException(Exception):
    """This exception is raised when trying to get an upgrade with illegal ID"""

    def __init__(self, wrongUpgradeId):
        self.__wrongUpgradeId = wrongUpgradeId

    def __str__(self):
        return 'UpgradeNotFoundException, upgrade Id ' + str(self.__wrongUpgradeId) + ' not found in upgrades database.'


class DBEntities:
    BASES = 0
    TURRETS = 1
    ARENAS = 2


class db:
    DUMMY_ENTITY_DATA_XML = ['server.todo.xml']

    @property
    def aircrafts(self):
        return self.__aircraftsDatabase

    @property
    def upgrades(self):
        """
        Returns upgrades as map where key - upgrade name, value - upgrade
        """
        return self.__upgradesDatabase

    def getAircraftPresetsListByID(self, aircraftID):
        """
        Get aircraft presets by aircraft id
        @param aircraftID: aircraft id
        @return list of aircraft presets
        """
        aircraftName = self.getAircraftData(aircraftID).airplane.name
        return self.getAircraftPresetsListByName(aircraftName)

    def getAircraftPresetsListByName(self, aircraftName):
        """
        Get aircraft presets by aircraft name
        @param aircraftID: aircraft id
        @return list of aircraft presets
        """
        if aircraftName in self.__presetsDatabase:
            return self.__presetsDatabase[aircraftName].preset
        else:
            return None

    def getAircraftPreset(self, aircraftName, presetName):
        if aircraftName in self.__presetsDatabase:
            for preset in self.__presetsDatabase[aircraftName].preset:
                if preset.name == presetName:
                    return preset

        return None

    def getAircraftDefaultPreset(self, aircraftID):
        return self.getAircraftDefaultPresetFromName(self.getAircraftData(aircraftID).airplane.name)

    def getAircraftDefaultPresetFromName(self, aircraftName):
        if aircraftName in self.__presetsDatabase:
            if self.__presetsDatabase[aircraftName].preset:
                return self.__presetsDatabase[aircraftName].preset[0]
        return None

    def getAircraftSound(self, name):
        if self.__soundSettings is None:
            return
        else:
            return self.__soundSettings.aircraftSound(name)

    def getAircraftEngineSet(self, profile):
        if self.__soundSettings is None:
            return
        else:
            return self.__soundSettings.engineSet.entries[profile]

    def getHangarSoundSet(self):
        if self.__soundSettings is None:
            return
        else:
            return self.__soundSettings.hangar.entries

    def getUI(self):
        if self.__soundSettings is None:
            return
        else:
            return self.__soundSettings.ui.entries

    def getWeaponSoundSet(self, wpnSndID):
        if self.__soundSettings is None:
            return
        else:
            profiles = self.__soundSettings.weapons.profiles
            if wpnSndID in profiles:
                return profiles[wpnSndID]
            return profiles['weapon_default']

    def getEffectSound(self, sndID):
        if self.__soundSettings is None:
            return
        else:
            profiles = self.__soundSettings.effects.sounds
            if sndID in profiles:
                return profiles[sndID]
            return

    def getAircraftSFX(self, profile):
        if self.__soundSettings is None:
            return
        else:
            return self.__soundSettings.aircraftSFX.entries[profile]

    def getAircraftStates(self, profile):
        if self.__soundSettings is None:
            return
        else:
            return self.__soundSettings.aircraftStates.entries[profile]

    def getAircraftAir(self, profile):
        if self.__soundSettings is None:
            return
        else:
            return self.__soundSettings.aircraftAir.entries[profile]

    def getAmbient(self, mapname):
        if self.__soundSettings is None:
            return
        else:
            events = self.__soundSettings.ambient.events
            if mapname in events:
                return events[mapname]
            return events['default']

    def getWoosh(self):
        if self.__soundSettings is None:
            return
        else:
            return self.__soundSettings.woosh.entries

    def getVO(self):
        if self.__soundSettings is None:
            return
        else:
            return self.__soundSettings.voice

    def getAirshowParameters(self):
        if self.__soundSettings is None:
            return
        else:
            return self.__soundSettings.airshow

    def getInteractiveMixParameters(self):
        if self.__soundSettings is None:
            return
        else:
            return self.__soundSettings.interactiveMix

    def getWindParameters(self):
        if self.__soundSettings is None:
            return
        else:
            return self.__soundSettings.wind

    def getSpline(self, splineName):
        lowerName = splineName.lower()
        spline = self.__splines.get(lowerName, None)
        if not spline and splineName:
            LOG_ERROR("can't find spline", lowerName)
        return spline

    def getSplines(self):
        return self.__splines

    def getArenaSplines(self, arenaName):
        return (spline for spline in self.__splines.values() if spline.checkArena(arenaName))

    def __loadSplines(self):
        splines = ResMgr.openSection(SPLINES_PATH)
        self.__splines = dict(((splineID.lower(), Spline(splineID.lower(), splineData)) for splineID, splineData in splines['mapActivities'].items()))
        ResMgr.purge(SPLINES_PATH)

    def getLandscapeMaterialName(self, materialID):
        return self.__landscapeMaterials.get(materialID)

    def __loadLandscapeMaterials(self):
        materials = ResMgr.openSection(LANDSCAPE_MATERIALS_PATH)
        if materials is None:
            return
        else:
            self.__landscapeMaterials = {v['material_id'].asInt:v['material_name'].asString for v in materials.values()}
            ResMgr.purge(LANDSCAPE_MATERIALS_PATH)
            return

    def __init__(self, onlyEntities = False, skipEntities = False):
        self.__exclusiveArenas = {}
        self.__landscapeMaterials = {}
        self.__initCommon()
        self.__loadSplines()
        loadingProgressStep('spline')
        self.__loadEffects()
        loadingProgressStep('effect')
        self.__loadLandscapeMaterials()
        loadingProgressStep('landscapeMaterials')
        if onlyEntities:
            self.__initEntities()
            return
        else:
            self.initAircraftsDatabase()
            loadingProgressStep('aircraftsDatabase')
            self.__nationIDs = dict(((country.name, country.id) for country in self.__aircraftsDatabase.country))
            if IS_CELLAPP or IS_BASEAPP:
                self.__observSectors = dict(((profile.name, profile.observSector) for profile in Visibility.scanSectorsProfile))
            for aircraft in self.__aircraftsDatabase.aircraft:
                if aircraft.options.isDev and not IS_DEVELOPMENT:
                    continue
                try:
                    pathName = filter(lambda country: country.name == aircraft.country, self.__aircraftsDatabase.country)[0].pathName
                    aircraftDataPath = os.path.join(pathName, aircraft.name + '.xml')
                except IndexError:
                    DBLOG_ERROR('Unknown country for plane. Skipped', aircraft.name, aircraft.country)
                    raise ValueError, (aircraft.country, [ x.name for x in self.__aircraftsDatabase.country ])
                    continue

                DBLOG_NOTE("\nLoading aircraft '%s%s'" % (AIRCRAFTS_PATH, aircraftDataPath))
                aircraftData = AirCraft(AIRCRAFTS_PATH + aircraftDataPath, self.__aircraftsDatabase)
                aircraftID = aircraft.id
                if aircraftData.airplane is None:
                    raise Exception, "Can't open '%s'" % aircraftDataPath
                self.shiftBBoxes(aircraftData)
                self.shiftPivots(aircraftData)
                self.__aircraftIDs[aircraft.name] = aircraftID
                self.__aircrafts[aircraftID] = aircraftData
                self._planeIDSByLevel.setdefault(aircraftData.airplane.level, set([])).add(aircraftID)
                self._planeIDSByNation.setdefault(self.__nationIDs[aircraft.country], set([])).add(aircraftID)
                self._planeIDSByType.setdefault(aircraftData.airplane.planeType, set([])).add(aircraftID)
                DBLOG_NOTE("Finished loading aircraft '%s', id %s" % (AIRCRAFTS_PATH + aircraftDataPath, str(aircraftID)))

            loadingProgressStep('patch database')
            self.__initUpgradesDatabase()
            loadingProgressStep('initUpgradesDatabase')
            self.__initPresetsDatabase()
            loadingProgressStep('initPresetsDatabase')
            self.__initAircraftUpgradesFromName()
            loadingProgressStep('initAircraftUpgradesFromName')
            self.initScenarioDatabase()
            loadingProgressStep('initScenarioDatabase')
            if not self.__aircraftsDatabase:
                DBLOG_ERROR('New style database is not loaded. Please see DBLogic.py and log output for possible errors.')
            if not self.__upgradesDatabase:
                DBLOG_ERROR('Upgrades database is not loaded. Please see DBLogic.py and log output for possible errors.')
            self.__components = ComponentsDB(_weapons.Weapons)
            loadingProgressStep('ComponentsDB')
            if not skipEntities:
                self.__initEntities()
            loadingProgressStep('initEntities')
            ResMgr.purge(AIRCRAFTS_PATH, True)
            if IS_CLIENT:
                materialsData = ResMgr.openSection(MATERIAL_NAMES_PATH)
                for key, value in materialsData.items():
                    matName = key
                    matId = int(value.readString(''))
                    self.__materialsIds[matName] = matId
                    self.__materialsNames[matId] = matName

                ResMgr.purge(MATERIAL_NAMES_PATH)
                loadingProgressStep('MATERIAL_NAMES_PATH')
                ssData = ResMgr.openSection(SOUND_SETTINGS_PATH)
                if ssData:
                    self.__soundSettings = SoundSettings(ssData)
                    ResMgr.purge(SOUND_SETTINGS_PATH, True)
                else:
                    self.__soundSettings = None
                    LOG_ERROR('SoundSetting: Failed to open ', SOUND_SETTINGS_PATH)
                loadingProgressStep('SOUND_SETTINGS_PATH')
                cmData = ResMgr.openSection(CAMERA_MISC_PATH)
                if cmData:
                    self.__cameraMiscDescription = CameraMisc(cmData)
                    ResMgr.purge(CAMERA_MISC_PATH, True)
                loadingProgressStep('CAMERA_MISC_PATH')
                textureData = ResMgr.openSection(GUI_TEXTURES_PATH)
                for key, value in textureData.items():
                    textures = dict([ (sName, sValue.readString('')) for sName, sValue in value.items() ])
                    self.__guiTextures[textures['id']] = textures['textureFile']

                ResMgr.purge(GUI_TEXTURES_PATH)
                loadingProgressStep('GUI_TEXTURES_PATH')
                self.__readAirplaneCameraPresets()
                loadingProgressStep('readAirplaneCameraPresets')
                ecsData = ResMgr.openSection(ENTITY_COLOR_SCHEMA_PATH)
                if ecsData:
                    self.__entityColorSchemes = EntityColorSchemes(ecsData)
                    ResMgr.purge(ENTITY_COLOR_SCHEMA_PATH, True)
                loadingProgressStep('ENTITY_COLOR_SCHEMA_PATH')
                helpHintData = ResMgr.openSection(HELP_HINT_PATH)
                if helpHintData:
                    self.__helpHint = HelpHint(helpHintData)
                    ResMgr.purge(HELP_HINT_PATH, True)
                print ('HELP_HINT_PATH', HELP_HINT_PATH, helpHintData)
                loadingProgressStep('HELP_HINT_PATH')
                hudHintData = ResMgr.openSection(HUD_HINT_PATH)
                if hudHintData:
                    self.__hudHints = HudHints(hudHintData)
                    ResMgr.purge(HUD_HINT_PATH, True)
                print ('HUD_HINT_PATH', HUD_HINT_PATH, hudHintData)
                loadingProgressStep('HUD_HINT_PATH')
                navWindowsData = ResMgr.openSection(NAVIGATION_WINDOWS_PATH)
                if navWindowsData:
                    self.__navWindows = NavigationWindows(navWindowsData)
                    ResMgr.purge(NAVIGATION_WINDOWS_PATH, True)
                loadingProgressStep('NAVIGATION_WINDOWS_PATH')
                camEffectsData = ResMgr.openSection(CAMERAEFFECTS_PATH)
                if camEffectsData:
                    self.__cameraEffectsDescription = CameraEffects(camEffectsData)
                    ResMgr.purge(CAMERAEFFECTS_PATH, True)
                loadingProgressStep('CAMERAEFFECTS_PATH')
                self.hangarConfigList = self.__readHangarConfig()
                self.userHangarSpaces = self.__readUserHangarSpaces()
                for upgrade in self.__upgradesDatabase.itervalues():
                    if upgrade.name in UPGRADE_TYPE.ICON_PATH_OVERRIDE:
                        upgrade.typeIconPath = UPGRADE_TYPE.ICON_PATH_OVERRIDE[upgrade.name]
                    elif upgrade.type != UPGRADE_TYPE.GUN:
                        upgrade.typeIconPath = UPGRADE_TYPE.ICON_PATH_MAP[upgrade.type]
                    else:
                        gunData = self.getGunData(upgrade.name)
                        if not hasattr(gunData, 'caliber'):
                            continue
                        upgrade.typeIconPath = ''
                        for minCaliber, maxCaliber, path in UPGRADE_TYPE.GUN_ICONS_PATH_INTERVALS:
                            if gunData.caliber <= maxCaliber and gunData.caliber > minCaliber:
                                upgrade.typeIconPath = path

            DBLOG_NOTE('Aircrafts database initialization is finished')
            return

    def __initCommon(self):
        self.start = time()
        DBLOG_NOTE('Aircrafts database initialization is starting')
        self.__effects = {}
        self.__effectByName = {}
        self.__aircrafts = {}
        self.__aircraftIDs = {}
        self._planeIDSByLevel = {}
        self._planeIDSByNation = {}
        self._planeIDSByType = {}
        self.__arenaTypes = {}
        self.__arenaList = {}
        self.__decals = {}
        self.__materialsNames = {}
        self.__materialsIds = {}
        self.__guiTextures = {}
        self.__globalIdToPresetNameDict = {}
        self.__presetNameToGlobalIdDict = {}
        self.__soundsCommonDescription = None
        self.__cameraMiscDescription = None
        self.__entityColorSchemes = None
        self.__helpHint = None
        self.__navWindows = None
        self.__hudHints = None
        self.__minMaxSpecsHash = {}
        self._planeMaxSpecsHash = {}
        return

    def __readHangarConfig(self):
        hangarConfigList = {}
        hangarFile = ResMgr.openSection(HANGAR_PATH)
        for hangarType, hdata in hangarFile.items():
            hangarConfigList[hangarType] = {}
            for key, data in hdata.items():
                hangarSize = data.readString('id')
                hangarConfigList[hangarType][hangarSize] = HangarConfig(data)

        ResMgr.purge(HANGAR_PATH)
        return hangarConfigList

    def __readUserHangarSpaces(self):
        LOG_INFO('User hangar spaces loading started')
        userHangarSpaces = {}
        index = 0
        for _, spaceData in ResMgr.openSection(USER_HANGAR_SPACES_PATH).items():
            spaceDict = {}
            for k, v in spaceData.items():
                if k == 'accessibilityConditions':
                    spaceDict['events'] = []
                    spaceDict['exceptEvents'] = []
                    spaceDict['accountTypes'] = []
                    for condName, condData in v.items():
                        if condName == 'event':
                            spaceDict['events'].append(condData.asString)
                        elif condName == 'exceptEvent':
                            spaceDict['exceptEvents'].append(condData.asString)
                        elif condName == 'accountType':
                            spaceDict['accountTypes'].append(condData.asString)
                        elif condName == 'activeTime':
                            from time import strptime, mktime, timezone
                            parts = str(condData.asString).split('_', 2)
                            spaceDict['startTime'] = mktime(strptime(parts[0], '%y%m%d-%H%M')) - timezone
                            if len(parts) > 1:
                                spaceDict['endTime'] = mktime(strptime(parts[1], '%y%m%d-%H%M')) - timezone

                elif k == 'spaceID':
                    spaceDict[k] = v.asString
                    userHangarSpaces[v.asString] = spaceDict
                elif k == 'isModal':
                    spaceDict[k] = True
                elif k == 'chooseHangarAfter':
                    spaceDict[k] = True
                elif k == 'switchOnActivation':
                    spaceDict[k] = True
                elif k == 'ambient':
                    spaceDict[k] = {}
                    for ambName, ambValue in v.items():
                        if ambName == 'name':
                            spaceDict[k][ambName] = ambValue.asString
                        elif ambName == 'rtpc':
                            spaceDict[k][ambName] = {}
                            for rtpcName, rtpcValue in ambValue.items():
                                if rtpcName == 'name':
                                    spaceDict[k][ambName][rtpcName] = rtpcValue.asString
                                elif rtpcName == 'value':
                                    spaceDict[k][ambName][rtpcName] = rtpcValue.asInt

                elif k == 'music':
                    spaceDict[k] = {}
                    for soundName, soundValue in v.items():
                        spaceDict[k][soundName] = soundValue.asString

                else:
                    spaceDict[k] = v.asString

            spaceDict['index'] = index
            index += 1

        ResMgr.purge(USER_HANGAR_SPACES_PATH)
        LOG_INFO('User hangar spaces loading finished. Loaded {0} spaces'.format(len(userHangarSpaces)))
        return userHangarSpaces

    def __loadEffects(self):

        def setNamesToIds(props):
            if 'effectSet' in props:
                props['effectSet'] = [ self.__effectByName[v] for v in props['effectSet'] if v in self.__effectByName ]

        effectsData = ResMgr.openSection(EFFECTS_PATH)
        if effectsData:
            effectId = 0
            for key, data in effectsData.items():
                effectProps = {}
                if 'variant' in data.keys():
                    effectProps['variant'] = {}
                    for sName, sValue in data.items():
                        if sName == 'variant':
                            varData, varUsage = readEffectVariantData(sValue)
                            if varUsage:
                                effectProps['variant'][varUsage] = varData
                        elif sName == 'id':
                            effectProps['id'] = sValue.readString('')

                else:
                    effectProps, varUsage = readEffectVariantData(data)
                self.__effectByName[effectProps['id']] = effectId
                self.__effects[effectId] = effectProps
                effectId += 1

            ResMgr.purge(EFFECTS_PATH)
            for effectProps in self.__effects.values():
                setNamesToIds(effectProps)
                if 'variant' in effectProps:
                    for props in effectProps['variant'].values():
                        setNamesToIds(props)

        else:
            CRITICAL_ERROR("Can't load or corrupted data file", EFFECTS_PATH)

    def getNavigationWindowData(self, navWindowsType):
        return self.__navWindows.getNavigationWindowData(navWindowsType)

    def getHelpHints(self):
        return self.__helpHint

    def getHudHint(self, id):
        return self.__hudHints.getHint(id)

    def getHudHints(self):
        return self.__hudHints.getAllHints()

    def getEntityColorSchemes(self):
        return self.__entityColorSchemes.getSchemes()

    def getEffectId(self, effectName):
        return self.__effectByName.get(effectName, None)

    def getEffectExists(self, effectName):
        return self.__effectByName.has_key(effectName)

    def shiftBBoxes(self, aircraftData):
        """
        shifting BBoxes to fit position into HPmass point
        """
        if IS_EDITOR:
            return
        if aircraftData.hpmass.mass:
            for part in aircraftData.airplane.partsSettings.getPartsOnlyList():
                for upgrade in part.upgrades.values():
                    upgrade.bboxes.shiftBBoxes(aircraftData.hpmass.mass.position)
                    for state in upgrade.states.values():
                        if state.bboxes:
                            state.bboxes.shiftBBoxes(aircraftData.hpmass.mass.position)

    def shiftPivots(self, aircraftData):
        """
        shifting pivots to fit position into HPmass point
        """
        if IS_EDITOR:
            return
        if aircraftData.hpmass.mass:
            i_pivots = aircraftData.pivots.mountPoints.itervalues()
            shift_vector = aircraftData.hpmass.mass.position
            for pivot in i_pivots:
                pivot.position -= shift_vector

    def getConfigurationRequiredUpgradesCount(self, configuration):
        """
        @param configuration:
        @return: requiredUpgrades as dict where {'upgradeName': <count>, ...}
        """
        requiredUpgrades = dict(((m, 1) for m in configuration.modules))
        for w in configuration.weaponSlots:
            weaponInfo = self.getWeaponInfo(configuration.planeID, w[0], w[1])
            if weaponInfo is not None:
                requiredUpgrades[weaponInfo[1]] = requiredUpgrades.get(weaponInfo[1], 0) + weaponInfo[2]

        return requiredUpgrades

    def getRequiredUpgradesCountByGlobalID(self, globalID):
        """
        @param globalID:
        @return: requiredUpgrades as dict where {'upgradeName': <count>, ...}
        """
        return self.getConfigurationRequiredUpgradesCount(getAirplaneConfiguration(globalID))

    def getCostModulesByConfiguration(self, configuration):
        """
        @param configuration:
        @return: requiredUpgrades as dict where {'upgradeName': <count>, ...}
        """
        modules = [ (m, 1) for m in configuration.modules ]
        for w in configuration.weaponSlots:
            weaponInfo = self.getWeaponInfo(configuration.planeID, w[0], w[1])
            if weaponInfo is not None:
                weaponType, weaponName, weaponCount = weaponInfo
                if not (weaponType == UPGRADE_TYPE.BOMB or weaponType == UPGRADE_TYPE.ROCKET):
                    modules.append((weaponName, weaponCount))

        return modules

    def getCostModulesByGlobalID(self, globalID):
        """
        @param globalID:
        @return: cost in credit
        """
        modules = self.getCostModulesByConfiguration(getAirplaneConfiguration(globalID))
        cost = 0
        for m in modules:
            cost += self.upgrades[m[0]].credits * m[1]

        return cost

    def getSellCostByGlobalID(self, globalID):
        """
        Calculate cost for sell plane in configuration
        @type globalID: int
        @param globalID: Global ID plane config
        @return: cost @rtype: int
        """
        planeID = getAirplaneConfiguration(globalID).planeID
        aircraftData = self.getAircraftData(planeID)
        gold = getattr(aircraftData.airplane.options, 'gold', 0) + getattr(aircraftData.airplane.options, 'tickets', 0) * _economics.Economics.goldPerTicket
        price = getattr(aircraftData.airplane.options, 'price', 0) + gold * _economics.Economics.goldRateForCreditBuys
        modulesCost = self.getCostModulesByGlobalID(globalID)
        modulesCostStok = self.getCostModulesByGlobalID(airplanesDefaultConfigurations.get(planeID, 0))
        sellPrice = _economics.Economics.sellCoeff * (price - modulesCostStok + modulesCost)
        return sellPrice

    def getPresetRequiredUpgradesCount(self, aircraftID, preset):
        """
        @param aircraftID:
        @param preset: preset object (see _presets_data.py)
        @return: requiredUpgrades as dict where {'upgradeName': <count>, ...}
        """
        requiredUpgrades = dict([ (m.name, 1) for m in preset.module ])
        for w in preset.weapon:
            weaponInfo = self.getWeaponInfo(aircraftID, w.slot, w.configuration)
            if weaponInfo is not None:
                requiredUpgrades[weaponInfo[1]] = requiredUpgrades.get(weaponInfo[1], 0) + weaponInfo[2]

        return requiredUpgrades

    def getGlobalIDByPreset(self, aircraftId, presetName):
        """
        Gets aircraft global id by preset id
        @param aircraftId:
        @param presetName: defined(not custom) preset name
        @type presetName: string
        """
        presetName = presetName.lower()
        globalID = self.__presetNameToGlobalIdDict.get(presetName, None)
        if globalID is None:
            preset = self.getAircraftPreset(self.getAircraftName(aircraftId), presetName)
            globalID = createGlobalID(aircraftId, list((module.name.lower() for module in preset.module)), list(((w.slot, w.configuration) for w in preset.weapon)))
            self.__presetNameToGlobalIdDict[presetName] = globalID
        return globalID

    def getPresetNameByGlobalID(self, globalID):
        """
        Returns preset name by GlobalID
        @param globalID:
        @return: Preset name or consts.CUSTOM_PRESET_NAME
        """
        presetName = self.__globalIdToPresetNameDict.get(globalID, None)
        if presetName is None:
            aircraftConfig = getAirplaneConfiguration(globalID)
            for preset in self.getAircraftPresetsListByName(self.getAircraftName(aircraftConfig.planeID)):
                if all((m.name in aircraftConfig.modules for m in preset.module)) and all(((w.slot, w.configuration) in aircraftConfig.weaponSlots for w in preset.weapon)):
                    self.__globalIdToPresetNameDict[globalID] = preset.name
                    presetName = preset.name
                    break

            if presetName is None:
                self.__globalIdToPresetNameDict[globalID] = consts.CUSTOM_PRESET_NAME
                presetName = consts.CUSTOM_PRESET_NAME
        return presetName

    def selectUpgradesNamesByGlobalID(self, globalID):
        """
        Returns an iterator to a sequence of upgrades names. Names could be duplicated
        @param globalID:
        @return: iterator
        """
        configuration = getAirplaneConfiguration(globalID)
        if configuration is None:
            LOG_ERROR('selectUpgradesNamesByGlobalID - configuration is None for globalID=%s' % globalID)
            return []
        else:
            return select(configuration.modules, (wInfo[1] for wInfo in (self.getWeaponInfo(configuration.planeID, *w) for w in configuration.weaponSlots) if wInfo is not None))

    def getUpgradesNamesByGlobalID(self, globalID):
        """
        Returns a set of upgrades names.
        @param globalID:
        @return: set() with upgrades names
        """
        return set(self.selectUpgradesNamesByGlobalID(globalID))

    def reloadAircraft(self, id):
        if IS_EDITOR:
            dataPath = self.__aircrafts[id].getDataPath()
            aircraftData = AirCraft(dataPath, self.__aircraftsDatabase)
            if aircraftData.airplane is None:
                raise Exception, "Can't open '%s'" % dataPath
            self.shiftBBoxes(aircraftData)
            self.__aircrafts[id] = aircraftData
        return

    def reloadBase(self, id):
        if IS_EDITOR:
            filePath = self.getBaseData(id).filePath
            name = self.getBaseData(id).typeName
            data = ResMgr.openSection(filePath)
            base = DBBaseObject(id, name, data)
            base.filePath = filePath
            self.__entities[DBEntities.BASES][1][id] = base
            self.__entities[DBEntities.BASES][0][name] = base
            ResMgr.purge(filePath, True)

    def getWeaponInfo(self, aircraftId, weaponSlotId, weaponSlotConfigurationId):
        """
        Return weapon type, name and count
        @param aircraftId:
        @param weaponSlotId:
        @param weaponSlotConfigurationId:
        @return: (<weapon type>, <weapon name>, <weapon count>) or None for empty configuration
        """
        aircraftData = self.getAircraftData(aircraftId)
        wType = aircraftData.components.weapons2.slots[weaponSlotId].types.get(weaponSlotConfigurationId, None)
        if wType is None:
            DBLOG_CRITICAL('getWeaponInfo() - Weapon slot not found: %d %d %d' % (aircraftId, weaponSlotId, weaponSlotConfigurationId))
        weapons = wType.weapons
        if weapons:
            return (self.upgrades[weapons[0].name].type, weapons[0].name, len(weapons))
        else:
            return

    def getWeaponCount(self, aircraftId, weaponSlotId, weaponSlotConfigurationId):
        aircraftData = self.getAircraftData(aircraftId)
        wType = aircraftData.components.weapons2.slots[weaponSlotId].types.get(weaponSlotConfigurationId, None)
        if wType is None:
            DBLOG_CRITICAL('getWeaponInfo() - Weapon slot not found: %d %d %d' % (aircraftId, weaponSlotId, weaponSlotConfigurationId))
        return len(wType.weapons)

    def getAllWeapons(self, aircraftId):
        aircraftData = self.getAircraftData(aircraftId)
        for slotID in xrange(len(aircraftData.components.weapons2.slots)):
            for configID in xrange(len(aircraftData.components.weapons2.slots[slotID].types)):
                yield (slotID, configID, aircraftData.components.weapons2.slots[slotID].types[configID])

    def getGunsCount(self, planeID, gunName, weaponSlot = None, weaponConfig = None):
        for slotID, configID, weapon in self.getAllWeapons(planeID):
            if weapon.weapons and weapon.weapons[0].name == gunName and (weaponConfig is None or configID == weaponConfig) and (weaponSlot is None or slotID == weaponSlot):
                return len(weapon.weapons)

        return

    def isEmptyWeaponSlot(self, aircraftId, weaponSlotId, weaponSlotConfigurationId):
        """
        Indicates if it is empty weapon slot configuration
        @param aircraftId:
        @param weaponSlotId:
        @param weaponSlotConfigurationId:
        @return:
        """
        return not self.getAircraftData(aircraftId).components.weapons2.slots[weaponSlotId].types[weaponSlotConfigurationId].weapons

    def getScanSectorsProfile(self, profileName):
        return self.__observSectors.get(profileName, None)

    def getVisibilitySettings(self):
        return Visibility

    def getAircraftClassDescription(self, classID):
        for cls in self.__aircraftsDatabase.aircraftClass:
            if cls.name == classID:
                return cls

    def getPresetRolesInfo(self, roleName):
        for role in self.__aircraftsDatabase.role:
            if role.name == roleName:
                return role

    def __initEntities(self):
        self.__entities = {DBEntities.BASES: self.__readDataListFromFolder(BASES_PATH, DBBaseObject),
         DBEntities.TURRETS: self.__readDataListFromFolder(TURRETS_PATH, Turret),
         DBEntities.ARENAS: self.__readDataWithFixedIDsFromFolder(ARENA_TYPE_PATH, ArenaType)}
        for arenaID, arenaData in self.__entities[DBEntities.ARENAS][1].iteritems():
            for arenaType in arenaData.exclusiveGameMods:
                if arenaType != ARENA_TYPE.TRAINING and arenaType not in ARENA_TYPE.ACTIVE_TYPES:
                    self.__exclusiveArenas.setdefault(arenaType, set()).add(arenaID)

        LOG_DEBUG_DEV('exclusiveArenas = ', self.__exclusiveArenas)
        from consts import PRINT_TURRETS_DATA
        if PRINT_TURRETS_DATA and IS_DEVELOPMENT:
            LOG_DEBUG('PRINT_TURRETS_DATA')
            for turretName, turretData in self.__entities[DBEntities.TURRETS][0].iteritems():
                print 'turretName: {0}, DPS: {1}, yawMin: {2}, yawMax: {3}, yawSpeed: {4}, pitchMin: {5}, pitchMax: {6},pitchSpeed: {6}, burstTime: {8}, burstDelay: {9}, reductionDelay: {10},fullReductionTime: {11}, aggroSwitchK: {12}, targetLockShootDistance: {13}, targetLostDistance: {14}'.format(turretName, turretData.DPS, turretData.yawMin, turretData.yawMax, turretData.yawSpeed, turretData.pitchMin, turretData.pitchMax, turretData.pitchSpeed, turretData.burstTime, turretData.burstDelay, turretData.reductionDelay, turretData.fullReductionTime, turretData.aggroSwitchK, turretData.targetLockShootDistance, turretData.targetLostDistance)

    def __readDataListFromFolder(self, folderPath, dataClass):
        elems = []
        d = {}
        i = 0
        listPath = '%slist.xml' % folderPath
        listData = ResMgr.openSection(listPath)
        names = listData.readStrings('name')
        for fileName in names:
            filePath = '%s%s.xml' % (folderPath, fileName)
            fileData = ResMgr.openSection(filePath)
            if fileData:
                elemDescription = dataClass(i, fileName, fileData)
                if IS_EDITOR:
                    elemDescription.filePath = filePath
                elems.append(elemDescription)
                d[fileName.lower()] = elemDescription
                ResMgr.purge(filePath, True)
                i += 1
            else:
                LOG_WARNING("can't find file", filePath)

        ResMgr.purge(listPath, True)
        return (d, elems)

    def __readDataWithFixedIDsFromFolder(self, folderPath, dataClass):
        intIDMap = {}
        strIDMap = {}
        listPath = '%slist.xml' % folderPath
        listData = ResMgr.openSection(listPath)
        for objSection in listData.values():
            if not objSection.has_key('name'):
                continue
            fileName = objSection.readString('name')
            intID = objSection.readInt('id')
            filePath = '%s%s.xml' % (folderPath, fileName)
            fileData = ResMgr.openSection(filePath)
            if fileData:
                if not fileData.readBool('isDev') or IS_DEVELOPMENT:
                    LOG_DEBUG('add %s from file %s' % (dataClass.__name__, filePath))
                    elemDescription = dataClass(intID, fileName, fileData)
                    intIDMap[intID] = elemDescription
                    strIDMap[fileName.lower()] = elemDescription
                ResMgr.purge(filePath)
            else:
                LOG_WARNING("can't find file", filePath, dataClass.__name__)

        ResMgr.purge(listPath)
        return (strIDMap, intIDMap)

    def getEntityDataByName(self, entityGroupID, name):
        groupDict = self.__entities[entityGroupID][0]
        data = groupDict.get(name.lower(), None)
        if data is None and name.lower() not in db.DUMMY_ENTITY_DATA_XML:
            LOG_WARNING("can't find data for", entityGroupID, name)
        return data

    def getEntityDataByIDFromMap(self, entityGroupID, iD):
        data = self.__entities[entityGroupID][1].get(iD, None)
        if data is None:
            LOG_WARNING('invalid id', iD, 'for', entityGroupID)
        return data

    def getEntityDataByIDFromList(self, entityGroupID, iD):
        try:
            return self.__entities[entityGroupID][1][iD]
        except IndexError:
            LOG_WARNING('invalid index', iD, 'for', entityGroupID)

    def getTurretData(self, name):
        return self.getEntityDataByName(DBEntities.TURRETS, name)

    def getBaseData(self, iD):
        return self.getEntityDataByIDFromList(DBEntities.BASES, iD)

    def getBases(self):
        if IS_EDITOR:
            return self.__entities[DBEntities.BASES][1]

    def getBaseDataByName(self, name):
        if IS_EDITOR:
            return self.getEntityDataByName(DBEntities.BASES, name)

    def getArenaList(self, arenaType = ARENA_TYPE.DEV):
        if arenaType == ARENA_TYPE.DEV:
            return self.__entities[DBEntities.ARENAS][1].values()
        if arenaType in self.__exclusiveArenas:
            return [ self.__entities[DBEntities.ARENAS][1][arenaID] for arenaID in self.__exclusiveArenas[arenaType] ]
        return [ data for data in self.__entities[DBEntities.ARENAS][1].values() if (not data.exclusiveGameMods or arenaType in data.exclusiveGameMods) and arenaType not in data.excludeArenaType ]

    def getPrebattleAvailableMaps(self):
        return [ arenaData.typeID for arenaData in self.getArenaList(ARENA_TYPE.TRAINING) if 0 <= arenaData.minPlayerCount <= 30 ]

    def getArenaData(self, iD):
        return self.getEntityDataByIDFromMap(DBEntities.ARENAS, iD)

    def isArenaValid(self, id):
        return id in self.__entities[DBEntities.ARENAS][1]

    def getArenaDataByName(self, name):
        return self.getEntityDataByName(DBEntities.ARENAS, name)

    def getArenaDataByGeometry(self, geometry):
        return next((arenaData for arenaData in self.__entities[DBEntities.ARENAS][1].itervalues() if arenaData.geometry == geometry), None)

    def getAicraftParts(self, aircraftID, upgradeNames):
        logicalParts = [0] * LOGICAL_PART.COUNT
        parts = {}
        aircraftData = self.getAircraftData(aircraftID)
        for upgName in upgradeNames:
            uprade = self.upgrades.get(upgName, None)
            if uprade is None:
                raise NotExistingUpgrade(upgName)
            if uprade.type not in UPGRADE_TYPE.WEAPON:
                aircraftName = aircraftData.airplane.name
                upgradeVariant = findIf(uprade.variant, lambda item: item.aircraftName == aircraftName)
                if upgradeVariant is None:
                    raise NotExistingUpgradeVariant(upgName)
                for logicalPart in upgradeVariant.logicalPart:
                    logicalPartType = LOGICAL_PART_STRING_TO_INT_TYPE[logicalPart.type]
                    logicalParts[logicalPartType] = self.getLogicalPartIndex(logicalPartType, logicalPart.name, aircraftID, 0)

                for part in upgradeVariant.part:
                    p = parts.get(part.id, None)
                    if not p or p.priority < part.priority:
                        parts[part.id] = part

        return (logicalParts, [ {'key': part.id,
          'value': part.variant} for part in parts.values() ])

    def getLogicalPartIndex(self, logicalPartType, logicalPartName, aircraftId, default = 0):
        """
        Returns logical part index in specified aircraft
        args:
            logicalPartName -
            nationId,
            aircraftId
        return:
            logical part index or default value
        @param logicalPartType: logical part type
        @type logicalPartType: LOGICAL_PART
        @param logicalPartName: logical part name,
        @param nationId:
        @param aircraftId:
        @param default:
        """
        logicalParts = None
        aircraft = self.getAircraftData(aircraftId)
        if aircraft:
            if logicalPartType == LOGICAL_PART.HULL:
                logicalParts = aircraft.airplane.flightModel.hull
            elif logicalPartType == LOGICAL_PART.ENGINE:
                logicalParts = aircraft.airplane.flightModel.engine
            elif logicalPartType == LOGICAL_PART.TURRET:
                logicalParts = aircraft.airplane.flightModel.turret
            if logicalParts:
                for index, value in enumerate(logicalParts):
                    if value.name == logicalPartName:
                        return index

        return default

    def __initUpgradesDatabase(self):
        """
        Importing predefined module _upgrades_db.py with upgrades data.
        Please see _upgrades_db.py for database structure.
        Returns reference to the dictionary with upgrades.
        """
        import _upgrades_db
        self.__upgradesDatabase = dict([ (upgrade.name, upgrade) for upgrade in _upgrades_db.DB.upgrade ])
        self.__upgradesIDName = dict([ (upgrade.id, upgrade.name) for upgrade in _upgrades_db.DB.upgrade ])

    def __initPresetsDatabase(self):
        import _presets_data
        self.__presetsDatabase = dict([ (aicraft.name, aicraft) for aicraft in _presets_data.PresetsData.aircraft ])

    def initScenarioDatabase(self, refresh = False):
        import _scenario_data
        if refresh:
            reload(_scenario_data)
        self.__scenarioDatabase = dict([ (scenario.name, scenario) for scenario in _scenario_data.ScenarioData.scenario ])
        self.__scenarioDatabaseShotProfile = {}
        self.__scenarioDatabaseShotBallisticProfile = {}
        if hasattr(_scenario_data.ScenarioData, 'shotProfile'):
            self.__scenarioDatabaseShotProfile = dict([ (shotProfile.name, shotProfile) for shotProfile in _scenario_data.ScenarioData.shotProfile ])
        if hasattr(_scenario_data.ScenarioData, 'shotBallisticProfile'):
            self.__scenarioDatabaseShotBallisticProfile = dict([ (shotBallisticProfile.name, shotBallisticProfile) for shotBallisticProfile in _scenario_data.ScenarioData.shotBallisticProfile ])

    def initAircraftsDatabase(self):
        """
        Importing predefined module _aircrafts_db.py with aircrafts data, making some checks and transformations to data.
        Please see _aircrafts_db.py for database structure.
        Returns reference to the loaded database object.
        """
        import _aircrafts_db
        if _aircrafts_db.isServerDatabase:
            DBLOG_NOTE('Aircrafts database is loaded in Server configuration')
        else:
            DBLOG_NOTE('Aircrafts database is loaded in Client configuration')
        if (IS_CLIENT or IS_EDITOR) and _aircrafts_db.isServerDatabase:
            DBLOG_ERROR('Server database is loaded at Client, which should not happen.')
        if (IS_BASEAPP or IS_CELLAPP) and not IS_EDITOR and not _aircrafts_db.isServerDatabase:
            DBLOG_ERROR('Client database is loaded at Server, which should not happen.')
        posInitDB(_aircrafts_db.DB, _weapons.Weapons, _gunsProfiles.GunsProfiles)
        self.environmentConstants = _aircrafts_db.DB.environmentConstants
        self.__checkGunProfileEffectNames(getattr(_aircrafts_db.DB, 'gunProfile', []))
        self.__aircraftsDatabase = _aircrafts_db.DB

    def reloadAircraftsDB(self):
        """
        Reloads new aircrafts database
        """
        import _aircrafts_db
        aircraftsDatabase = _aircrafts_db.DB
        self.__aircraftsDatabase = aircraftsDatabase
        for aircraftDB in self.__aircraftsDatabase.aircraft:
            aircraft = self.__aircrafts.get(aircraftDB.id, None)
            if aircraft is not None:
                aircraft.airplane.patch(aircraftDB)

        return

    def __checkGunProfileEffectNames(self, gunProfileList):
        for gunProfile in gunProfileList:
            for particleType in ['default',
             'aircraft',
             'tree',
             'water',
             'turret',
             'baseobject',
             'ground']:
                explosionParticle = getattr(gunProfile.explosionParticles, particleType)
                if not Effects.exists(explosionParticle):
                    DBLOG_ERROR("'%s' explosion particles %s not found for gun profile '%s'" % (particleType, explosionParticle, gunProfile.name))

    def getDefaultUpgradesDict(self, aircraftID):
        defaultAirplaneConfiguration = getDefaultAirplaneConfiguration(aircraftID)
        if defaultAirplaneConfiguration is None:
            LOG_ERROR('defaultAirplaneConfiguration for aircraft %d not found' % aircraftID)
            return
        else:
            allUpgrades = dict(map(lambda el: (el, 1), defaultAirplaneConfiguration.modules))
            aircraftData = self.getAircraftData(aircraftID)
            weapons = dict()
            for slot in defaultAirplaneConfiguration.weaponSlots:
                slotData = aircraftData.components.weapons2.slots.get(slot[0])
                if not slotData:
                    LOG_ERROR('Weapon slot data not found (aircraftName, slotId)', aircraftData.airplane.name, slot[0])
                    LOG_ERROR('Slots', aircraftData.components.weapons2.slots)
                    raise
                slotTypeData = slotData.types.get(slot[1])
                if not slotTypeData:
                    LOG_ERROR('Weapon slot type data not found (aircraftName, slotId, slotTypeId)', aircraftData.airplane.name, slot[0], slot[1])
                    LOG_ERROR('slotData.types', slotData.types)
                    raise
                for weaponData in slotTypeData.weapons:
                    if not weapons.has_key(weaponData.name):
                        weapons[weaponData.name] = 1
                    else:
                        weapons[weaponData.name] += 1

                allUpgrades.update(weapons)

            return allUpgrades

    def getAircraftUpgradesFromName(self, aircraftName, onlyDefault = False):
        if not (aircraftName in self.__cacheUpgradeModules and aircraftName in self.__cacheAircrafts and aircraftName in self.__cachedDefaultUpgrades):
            LOG_ERROR('getAircraftUpgradesFromName: has not correctly installer plane', aircraftName)
            if onlyDefault:
                return []
            return ([], [])
        if onlyDefault:
            return self.__cachedDefaultUpgrades[aircraftName]
        return (self.__cacheUpgradeModules[aircraftName], self.__cacheAircrafts[aircraftName])

    def __initAircraftUpgradesFromName(self):
        self.__cacheUpgradeModules = {}
        self.__cacheAircrafts = {}
        self.__cachedDefaultUpgrades = {}
        self.__cacheAircraftsUpgrade = {}
        for aircraftName in self.__aircraftIDs:
            self.__cacheUpgradeModules[aircraftName] = []
            self.__cacheAircrafts[aircraftName] = []
            for upgrade in self.upgrades.values():
                for upgradeVariant in upgrade.variant:
                    if upgradeVariant is None or upgradeVariant.aircraftName != aircraftName:
                        continue
                    if upgrade.type == UPGRADE_TYPE.AIRCRAFT:
                        planeData = self.getAircraftData(self.getAircraftIDbyName(upgrade.name)).airplane
                        if not planeData.options.hidePlaneResearch:
                            self.__cacheAircrafts[aircraftName].append(upgrade)
                    else:
                        self.__cacheUpgradeModules[aircraftName].append(upgrade)

            aircraftID = self.getAircraftIDbyName(aircraftName)
            preset = self.getAircraftDefaultPresetFromName(aircraftName)
            if preset is None:
                DBLOG_ERROR('Plane %s has no one preset' % aircraftName)
                continue
            self.__cachedDefaultUpgrades[aircraftName] = [ self.upgrades[m.name] for m in preset.module ]
            for w in preset.weapon:
                upgname = self.getWeaponUpgradeName(aircraftID, w.slot, w.configuration)
                if upgname:
                    self.__cachedDefaultUpgrades[aircraftName].append(self.upgrades[upgname])

        for upgrade in self.upgrades.values():
            if upgrade.type != UPGRADE_TYPE.AIRCRAFT:
                continue
            if upgrade.name in self.__aircraftIDs:
                self.__cacheAircraftsUpgrade[upgrade.name] = upgrade

        return

    def getUpgradeByAircraftID(self, aircraftID):
        name = self.getAircraftData(aircraftID).airplane.name
        return self.__cacheAircraftsUpgrade.get(name, None)

    def getWeaponUpgradeName(self, aircraftID, slot, configuration):
        ws = self.getAircraftData(aircraftID).components.weapons2.slots[slot].types[configuration].weapons
        if ws:
            return iter(ws).next().name
        else:
            return None

    def getAircraftUpgrades(self, aircraftID, onlyDefault = False):
        """
        Get aircraft upgrades
        @param aircraftID: aircraft id
        @param onlyDefault: if True - get only default aircraft upgrades. Otherwise get all aircraft upgrades
        @return list of aircraft upgrades
        """
        return self.getAircraftUpgradesFromName(self.getAircraftData(aircraftID).airplane.name, onlyDefault)

    def isPlaneOk(self, aircraftID):
        """ Check plane for correct data in database """
        try:
            airplaneData = self.getAircraftData(aircraftID)
            return not (airplaneData is None or airplaneData.airplane is None)
        except:
            DBLOG_ERROR("Can't find aircraft with id %s , please check list.xml and code." % str(aircraftID))
            return False

        return None

    def aircraftDataValidation(self, airplane, battlePlaneList):
        hasError = False
        if airplane[PLANE_KEYS.BLOCK_TYPE] & BLOCK_TYPE.LOCKED or airplane[PLANE_KEYS.PLANE] in battlePlaneList:
            if airplane[PLANE_KEYS.LAST_GAME_TIME] == 0 or airplane[PLANE_KEYS.LAST_GAME_TIME] + BATTLE_DURATIONS.DEFAULT_ROUND_TIMER + TIME_OUT_AFTER_BATTLE < time():
                if not IS_DEVELOPMENT:
                    LOG_ERROR('Aircraft block time > ', str(BATTLE_DURATIONS.DEFAULT_ROUND_TIMER + TIME_OUT_AFTER_BATTLE), airplane)
                airplane[PLANE_KEYS.BLOCK_TYPE] = (airplane[PLANE_KEYS.BLOCK_TYPE] | BLOCK_TYPE.LOADING_BATTLE) ^ BLOCK_TYPE.LOADING_BATTLE
                airplane[PLANE_KEYS.BLOCK_TYPE] = (airplane[PLANE_KEYS.BLOCK_TYPE] | BLOCK_TYPE.IN_BATTLE) ^ BLOCK_TYPE.IN_BATTLE
                if airplane[PLANE_KEYS.PLANE] in battlePlaneList:
                    battlePlaneList.remove(airplane[PLANE_KEYS.PLANE])
                hasError = True
        if airplane[PLANE_KEYS.BLOCK_TYPE] & BLOCK_TYPE.NEED_REPAIR and airplane[PLANE_KEYS.LOST_HIT_POINTS] <= 0:
            LOG_ERROR('lostHitPoints <= 0 , BLOCK_TYPE ==NEED_REPAIR  ', airplane)
            airplane[PLANE_KEYS.BLOCK_TYPE] = (airplane[PLANE_KEYS.BLOCK_TYPE] | BLOCK_TYPE.NEED_REPAIR) ^ BLOCK_TYPE.NEED_REPAIR
            airplane[PLANE_KEYS.REPAIR_COST] = 0
            airplane[PLANE_KEYS.LOST_HIT_POINTS] = 0
            hasError = True
        return hasError

    def isPlaneAvailableToBuy(self, planeID):
        options = self.getAircraftData(planeID).airplane.options
        return not getattr(options, 'isExclusive', False) and not getattr(options, 'isNPC', False) and not getattr(options, 'isDev', False)

    def isPlaneExclusive(self, aircraftID):
        return getattr(self.getAircraftData(aircraftID).airplane.options, 'isExclusive', False)

    def isPlaneNPC(self, aircraftID):
        return getattr(self.getAircraftData(aircraftID).airplane.options, 'isNPC', False)

    def isPlaneBotAcceptable(self, planeID):
        return getattr(self.getAircraftData(planeID).airplane.options, 'isBotAcceptable', True)

    def isPlaneDev(self, aircraftID):
        return bool(getattr(self.getAircraftData(aircraftID).airplane.options, 'isDev', False))

    def isWeaponConfigurationValid(self, upgrades, weaponCfg, aircraftName):
        for upgrade in upgrades:
            for variant in filter(lambda variant: variant.aircraftName == aircraftName, upgrade.variant):
                for slot in variant.slot:
                    for slotTypeId in slot.typeId:
                        slotCfg = (slot.id, slotTypeId)
                        if slotCfg in weaponCfg:
                            weaponCfg.remove(slotCfg)

        return len(weaponCfg) == 0

    def isUpgradesValid(self, aircraftName, upgrades):
        instaledUpgradeList = set()
        instaledUpgradeTypeList = set()
        for upgrade in upgrades:
            instaledUpgradeList.add(upgrade.name)
            instaledUpgradeTypeList.add(upgrade.type)

        for upgrade in upgrades:
            for variant in filter(lambda variant: variant.aircraftName == aircraftName, upgrade.variant):
                isValidRequired = any(map(lambda reqUpgrade: reqUpgrade in instaledUpgradeList, variant.requiredUpgrades)) or len(variant.requiredUpgrades) == 0
                if not isValidRequired:
                    return False

        return UPGRADE_TYPE.PLANER in instaledUpgradeTypeList and UPGRADE_TYPE.ENGINE in instaledUpgradeTypeList

    def __getAllCombination(self, upgradesByTypes, keyId):
        nextCombinations = self.__getAllCombination(upgradesByTypes, keyId + 1) if keyId + 1 < len(upgradesByTypes) else [[]]
        variants = []
        for upgrade in upgradesByTypes[upgradesByTypes.keys()[keyId]]:
            variants += map(lambda nextCombination: [upgrade] + nextCombination, nextCombinations)

        return variants

    def getFeaturesComponent(self, upgradeName):
        """
        """
        features = {}
        upgrade = self.upgrades[upgradeName]
        if upgrade.type == UPGRADE_TYPE.GUN:
            gunData = self.getGunData(upgradeName)
            features['name'] = upgradeName
            features['price'] = upgrade.credits if upgrade.credits != 0 else upgrade.gold
            features['caliber'] = gunData.caliber
            features['mass'] = gunData.mass
            features['RPM'] = gunData.RPM
            features['bulletSpeed'] = gunData.bulletSpeed
            features['DPS'] = gunData.DPS
        elif upgrade.type == UPGRADE_TYPE.ENGINE:
            upgradeVariant = upgrade.variant[0]
            planeID = self.getAircraftIDbyName(upgradeVariant.aircraftName)
            settings = self.getAircraftData(planeID)
            partname = findIf(upgradeVariant.logicalPart, lambda p: p.type == 'engine').name
            engineParameters = filter(lambda m: m.name == partname, settings.airplane.flightModel.engine)
            eng = engineParameters[0]
            power = eng.power if hasattr(eng, 'power') else eng.thrust / 10.0
            features['name'] = upgradeName
            features['price'] = upgrade.credits if upgrade.credits != 0 else upgrade.gold
            features['power'] = power
            features['mass'] = eng.mass
        elif upgrade.type == UPGRADE_TYPE.PLANER:
            upgradeVariant = upgrade.variant[0]
            planeID = self.getAircraftIDbyName(upgradeVariant.aircraftName)
            settings = self.getAircraftData(planeID)
            partname = findIf(upgradeVariant.logicalPart, lambda p: p.type == 'hull').name
            hullParameters = filter(lambda h: h.name == partname, settings.airplane.flightModel.hull)
            features['name'] = upgradeName
            features['price'] = upgrade.credits if upgrade.credits != 0 else upgrade.gold
            h = hullParameters[0]
            features['HP'] = h.HP
            features['mass'] = h.mass
        elif upgrade.type == UPGRADE_TYPE.ROCKET or upgrade.type == UPGRADE_TYPE.BOMB:
            shellDBGroupID, shellDescription = self.getShellComponentsGroupIDAndDescription(upgradeName)
            features['name'] = upgradeName
            features['price'] = upgrade.credits if upgrade.credits != 0 else upgrade.gold
            features['mass'] = shellDescription.mass
            features['explosionDamageMax'] = shellDescription.explosionDamageMax
            features['explosionRadius'] = shellDescription.explosionRadius / consts.WORLD_SCALING
        elif upgrade.type == UPGRADE_TYPE.TURRET:
            try:
                weapons = self.getTurretData(upgradeName).components.weapons2.slots[0].types[0].weapons
            except Exception as e:
                LOG_ERROR('Upgrade name: %s' % upgrade.name)
                LOG_CURRENT_EXCEPTION()
                raise

            features['name'] = upgradeName
            features['gunType'] = weapons[0].name
            features['gunsCount'] = len(weapons)
            features['price'] = upgrade.credits if upgrade.credits != 0 else upgrade.gold
        return features

    def getAllUpgradeVariantsByType(self, aircraftID, upgradeType):
        upgradeModules = self.getAircraftUpgrades(aircraftID)[0]
        res = []
        for upgradeModule in filter(lambda upgradeModule: upgradeModule.type == upgradeType, upgradeModules):
            res.append(upgradeModule.name)

        return res

    def getAllUpgradeVariants(self, aircraftID):
        aircraftName = self.getAircraftData(aircraftID).airplane.name
        upgradeModules = self.getAircraftUpgrades(aircraftID)[0]
        upgradeByTypes = {}
        for upgradeModule in filter(lambda upgradeModule: upgradeModule.type in UPGRADE_TYPE.MODULES, upgradeModules):
            upgradeByTypes[upgradeModule.type] = upgradeByTypes.get(upgradeModule.type, []) + [upgradeModule]

        if upgradeByTypes:
            combinations = filter(lambda combination: self.isUpgradesValid(aircraftName, combination), self.__getAllCombination(upgradeByTypes, 0))
            return map(lambda combination: map(lambda upgrade: upgrade.name, combination), combinations)
        return []

    def getDefaultUpgrades(self, aircraftID):
        return [ upgrade.name for upgrade in (upgradeModule for upgradeModule in self.getAircraftUpgrades(aircraftID, True) if upgradeModule.type in UPGRADE_TYPE.MODULES) ]

    def createGlobalIDForDefaultConfiguration(self, aircraftID):
        defaultPreset = self.getAircraftDefaultPreset(aircraftID)
        return createGlobalID(aircraftID, [ module.name for module in defaultPreset.module ], [ (weapon.slot, weapon.configuration) for weapon in defaultPreset.weapon ])

    def getAllWeaponVariants(self, aircraftID, upgrades):
        slotsTypes = {}
        aircraftName = self.getAircraftData(aircraftID).airplane.name
        for upgrade in upgrades:
            for variant in upgrade.variant:
                if variant.aircraftName == aircraftName:
                    for slot in variant.slot:
                        slotsTypes[slot.id] = slotsTypes.get(slot.id, []) + [ '[%s:%s]' % (str(slot.id), str(typeId)) for typeId in slot.typeId ]

        return self.__getAllCombination(slotsTypes, 0)

    def getAllWeaponVariantsTuple(self, aircraftID, upgrades):
        slotsTypes = {}
        aircraftName = self.getAircraftData(aircraftID).airplane.name
        for upgrade in upgrades:
            for variant in upgrade.variant:
                if variant.aircraftName == aircraftName:
                    for slot in variant.slot:
                        slotsTypes[slot.id] = slotsTypes.get(slot.id, []) + [ (slot.id, typeId) for typeId in slot.typeId ]

        return self.__getAllCombination(slotsTypes, 0)

    def getAircraftData(self, iD):
        """@note: raises AircraftNotFoundException if id is not found in the aircrafts database."""
        try:
            return self.__aircrafts[iD]
        except KeyError:
            DBLOG_ERROR("Can't find aircraft with id %s , please check list.xml and code." % str(iD))
            if IS_DEVELOPMENT:
                import traceback
                traceback.print_stack()
            raise AircraftNotFoundException(iD)
        except TypeError:
            DBLOG_ERROR('Wrong type of plane id {0}, type {1}'.format(iD, type(iD)))
            raise AircraftNotFoundException(iD)

    def getNationNameByPlaneID(self, planeID):
        try:
            settings = self.getAircraftData(planeID)
            return settings.airplane.country
        except AircraftNotFoundException:
            return -1

    def getAircraftsDict(self):
        return self.__aircrafts

    def isAircraftInDB(self, id):
        return int(id) in self.__aircrafts

    def checkDB(self):
        """validate db information. Out: error element id, error description"""
        errorsList = filter(lambda (x, y): bool(y), map(lambda aircraft: ('AIRCRAFT %s' % aircraft.airplane.name, aircraft.check()), self.__aircrafts.values()))
        upgradeErrors = ''
        for upgrade in self.upgrades.values():
            for variant in upgrade.variant:
                if variant.parentUpgrade[0].name != '':
                    if not self.upgrades.has_key(variant.parentUpgrade[0].name):
                        upgradeErrors += '\n upgrade %s has invalid parent %s' % (upgrade.name, variant.parentUpgrade[0].name)
                if not self.__aircraftIDs.has_key(variant.aircraftName):
                    upgradeErrors += '\n upgrade %s  has invalid aircrafName in variant %s' % (upgrade.name, variant.aircraftName)

        if upgradeErrors != '':
            errorsList.append(('UPGRADES ', upgradeErrors))
        errs = self.__checkDevPlaneInDatabase()
        if errs:
            errorsList.append((':bundleStop: DEV PLANES:', errs))
        return errorsList

    def getAircraftName(self, iD):
        """
        Return aircraft name by it's id
        @param id: aircraft id
        @rtype: string
        """
        aircraftData = self.getAircraftData(iD)
        return aircraftData.airplane.name

    def getDestructibleObjectData(self, obj):
        if isAvatar(obj):
            data = self.getAircraftData(obj.objTypeID)
            if data:
                return data.airplane
            return None
        elif isTeamObject(obj):
            return self.getBaseData(obj.objTypeID)
        else:
            return None

    def getPlanesByNationID(self, nationID):
        return self._planeIDSByNation[nationID]

    def getPlanesByLevel(self, level):
        return self._planeIDSByLevel[level]

    def getPlanesByType(self, planeType):
        return self._planeIDSByType[planeType]

    def isGoodNationID(self, nationID):
        return nationID in self._planeIDSByNation.iterkeys()

    def isGoodLevel(self, level):
        return level in self._planeIDSByLevel.iterkeys()

    def isGoodPlaneType(self, planeType):
        return planeType in self._planeIDSByType.iterkeys()

    def getNationList(self):
        return self.__nationIDs

    def getNationIDList(self):
        return self.__nationIDs.values()

    def getPlaneIDList(self):
        return self.__aircraftIDs.values()

    def getPlaneNameList(self):
        return self.__aircraftIDs.keys()

    def getAircraftList(self, nationID):
        countryName = self.getNationNamebyID(nationID)
        return dict(filter(lambda (iD, aircraft): aircraft.airplane.country == countryName, self.__aircrafts.iteritems()))

    def getPlaneNationID(self, planeID):
        """
        @type planeID: int
        @rtype: int
        """
        raise planeID in self.__aircrafts or AssertionError('Invalid planeID = %s' % planeID)
        return self.__nationIDs[self.__aircrafts[planeID].airplane.country]

    def getGunData(self, gunName):
        return self.__components.findComponent(COMPONENT_TYPE.GUNS, gunName)

    def getGunProfileName(self, gunDescription, planeID):
        planeName = self.getAircraftData(planeID).airplane.name
        return next((v.profileName for v in gunDescription.alternativeGunProfileName if v.plane == planeName), gunDescription.gunProfileName)

    def getGunProfileData(self, gunProfileName):
        return next((profile for profile in _gunsProfiles.GunsProfiles.gunProfile if profile.name == gunProfileName.lower()), None)

    def getAmmoData(self, ammoName):
        """Returns ammo description from aircrafts.xml,
        mat also return None if no ammo found"""
        return self.__components.findComponent(COMPONENT_TYPE.AMMO, ammoName)

    def getAmmoBeltData(self, ammoBeltName):
        """Returns ammo description from aircrafts.xml,
        mat also return None if no found"""
        return self.__components.findComponent(COMPONENT_TYPE.AMMOBELT, ammoBeltName)

    def getShellComponentsGroupIDAndDescription(self, shellName):
        """
        Determine type of shell and return ComponentID and it description
        """
        for componentID in [COMPONENT_TYPE.ROCKETS, COMPONENT_TYPE.BOMBS]:
            description = self.__components.findComponent(componentID, shellName)
            if description:
                return (componentID, description)

        return (-1, None)

    def getComponentByIndex(self, componentsGroupID, iD):
        return self.__components.getComponentByIndex(componentsGroupID, iD)

    def getComponents(self, componentsGroupID):
        return self.__components.getComponents(componentsGroupID)

    def getComponentByID(self, componentType, ID):
        """
        Get component by it id
        @type componentType: some of COMPONENT_TYPE const
        @param ID:
        @return:
        """
        return _weapons.WeaponsDB.get(componentType, {}).get(ID, None)

    def getComponentByName(self, componentType, name):
        """
        Get component by it name
        @type componentType: some of COMPONENT_TYPE const
        @param name:
        @return:
        """
        return self.__components.findComponent(componentType, name)

    def isPermit(self, groupIds, actionId):
        """
            Check is allowed action in group or group list
        """
        return self.permission.isAllow(groupIds, actionId)

    def verify(self):
        for k, v in db().__dict__.items():
            compareField(self.__dict__[k], v, k)

    def __getIDbyName(self, dic, name):
        data = dic.get(name, None)
        if data is None:
            DBLOG_ERROR('invalid name %s. Valid keys are: %s' % (str(name), str(dic.keys())))
        return data

    def __getNamebyID(self, dic, iD):
        for name, dictID in dic.items():
            if dictID == iD:
                return name

        DBLOG_ERROR('invalid id %s. Valid keys are: %s' % (str(iD), str(dic.values())))
        raise ValueError
        return None

    def getAircraftIDbyName(self, name):
        return self.__getIDbyName(self.__aircraftIDs, name.lower())

    def getNationIDbyName(self, name):
        return self.__getIDbyName(self.__nationIDs, name)

    def getNationIDbyAircraftID(self, aircraftID):
        """
        @deprecated: Use getPlaneNationID instead.
        """
        aircraft = self.getAircraftData(aircraftID)
        if aircraft:
            return self.getNationIDbyName(aircraft.airplane.country)
        else:
            return None

    def getNationNamebyID(self, nationID):
        return self.__getNamebyID(self.__nationIDs, nationID)

    def getAircraftFlagPath(self, aircraftName):
        """
        aircraftName shall be normalized (lower case)
        Returns path to aircraft's carousel background bitmap, image of country flag.
        """
        for aircraft in self.__aircraftsDatabase.aircraft:
            if aircraft.name == aircraftName:
                for country in self.__aircraftsDatabase.country:
                    if country.name == aircraft.country:
                        return country.flagBitmap

                DBLOG_ERROR("Cannot find country '%s' while looking for flag bitmap for aircraft '%s', please fix aircrafts.xml" % (aircraft.country, aircraft.name))

        DBLOG_ERROR("Cannot find aircraft '%s' in aircrafts database." % str(aircraftName))

    def __getEffectData(self, effectId):
        return self.__effects.get(effectId, None)

    def __getEffectDataByName(self, effectName):
        return self.__getEffectData(Effects.getEffectId(effectName))

    def getEffectDataVariant(self, effectID, variant):
        effectData = self.__getEffectData(effectID)
        if effectData and 'variant' in effectData:
            effectData = effectData['variant'].get(variant, None)
        return effectData

    def getEffectDataVariantNames(self, effectID):
        effectData = self.__getEffectData(effectID)
        if 'variant' in effectData:
            return effectData['variant'].keys()
        else:
            return ['OWN']

    def getEffectIds(self):
        return self.__effects.keys()

    def getDecalData(self, decalId):
        return self.__decals.get(decalId, None)

    def getDecalIds(self):
        return self.__decals.keys()

    def getMaterialId(self, name):
        return self.__getIDbyName(self.__materialsIds, name)

    def getMaterialName(self, iD):
        return self.__getIDbyName(self.__materialsNames, iD)

    @property
    def soundsCommon(self):
        return self.__soundsCommonDescription

    def getMiscSound(self, name):
        return getattr(self.__soundsCommonDescription.misc.sounds.get(name, None), 'path', None)

    def getUISound(self, name):
        return getattr(self.__soundsCommonDescription.ui.sounds.get(name, None), 'path', None)

    def getHitSound(self, hitType, gunCaliber, hitMaterialID):
        return self.__soundsCommonDescription.hit.getSound(hitType, gunCaliber, hitMaterialID)

    def getDSP(self):
        return self.__soundsCommonDescription.dsp

    def getSpeech(self):
        return self.__soundsCommonDescription.speech

    def getSpeechSound(self, name):
        return self.__soundsCommonDescription.speech.sounds.get(name, None)

    def getDucking(self):
        return self.__soundsCommonDescription.ducking

    def getCategoryDucking(self):
        return self.__soundsCommonDescription.categoryDucking.sounds

    def getCameraMisc(self):
        return self.__cameraMiscDescription

    @property
    def cameraEffects(self):
        return self.__cameraEffectsDescription

    def getGUITexture(self, name):
        return self.__getIDbyName(self.__guiTextures, name)

    def getPlaneIDByGlobalID(self, globalID):
        return airplanesConfigurations[globalID].planeID

    def getPlaneLevelByGlobalID(self, globalID):
        config = airplanesConfigurations.get(globalID, None)
        if config is None:
            return -1
        else:
            settings = self.getAircraftData(airplanesConfigurations[globalID].planeID)
            return settings.airplane.level

    def getPlaneLevelByID(self, planeID):
        settings = self.getAircraftData(planeID)
        return settings.airplane.level

    def getPlaneTypeByPlaneID(self, planeID):
        try:
            settings = self.getAircraftData(planeID)
            return settings.airplane.planeType
        except:
            LOG_ERROR('DBLogic.getPlaneTypeByPlaneID planeID={0}. Unknown planeID.'.format(planeID))
            return None

        return None

    def getAirplaneClassByGlobalID(self, globalID):
        settings = self.getAircraftData(airplanesConfigurations[globalID].planeID)
        planeType = settings.airplane.planeType
        return planeType

    def __readAirplaneCameraPresets(self):
        self.__airplaneCameraPresets = {}
        airplaneCameraPresetsFile = ResMgr.openSection(AIRPLANE_CAMERA_PRESETS_PATH)
        for key, pdata in airplaneCameraPresetsFile.items():
            presetID = pdata.readString('id')
            self.__airplaneCameraPresets[presetID] = CameraSettings(pdata)

        ResMgr.purge(AIRPLANE_CAMERA_PRESETS_PATH)

    def getAirplaneCameraPreset(self, id):
        return self.__airplaneCameraPresets[id]

    def getScenario(self, name):
        return self.__scenarioDatabase.get(name)

    def getScenarioShotProfile(self, name):
        return self.__scenarioDatabaseShotProfile.get(name)

    def getScenarioShotBallisticProfile(self, name):
        return self.__scenarioDatabaseShotBallisticProfile.get(name)

    def getUpgradeNameByID(self, upgradeID):
        upgName = self.__upgradesIDName.get(upgradeID, None)
        if upgName is None:
            LOG_ERROR('Upgrade not found by id: {0}'.format(upgradeID))
            raise UpgradeNotFoundException(upgradeID)
        return upgName

    def getUpgradeByName(self, upgradeName):
        upgrade = self.__upgradesDatabase.get(upgradeName, None)
        if upgrade is None:
            LOG_ERROR('Upgrade not found by name: {0}'.format(upgradeName))
            raise UpgradeNotFoundException(upgradeName)
        return upgrade

    def getUpgradeCompatibilityPlanes(self, upgradeName):
        upgrade = self.upgrades.get(upgradeName, None)
        if upgrade is None:
            LOG_ERROR('Upgrade not found by name: %s' % upgradeName)
            raise UpgradeNotFoundException(upgradeName)
        return (self.getAircraftIDbyName(variants.aircraftName) for variants in upgrade.variant)

    def getSlotsWeaponUpgrade(self, planeID, weaponUpgrade):
        """
        Returns slots settings object where this weapon upgrades could be installed
        @param planeID:
        @param weaponUpgrade:
        @return: array of slots settings
        """
        slots = []
        data = self.getAircraftData(planeID)
        for slotSettings in data.components.weapons2.slots.values():
            for conf in slotSettings.types.values():
                if conf.weapons and conf.weapons[0].name == weaponUpgrade.name:
                    slots.append(slotSettings)

        return slots

    def getPlaneParentPlaneID(self, planeID):
        """
        Returns parent plane id or None if no parents
        @param planeID:
        @return:
        """
        planeUpgrade = self.upgrades.get(self.getAircraftName(planeID), None)
        if planeUpgrade is not None and planeUpgrade.variant:
            return [ self.getAircraftIDbyName(variant.aircraftName) for variant in planeUpgrade.variant ]
        else:
            return []

    def getEquipmentByID(self, equipmentID):
        return EquipmentDB.get(equipmentID, None)

    def getConsumableByID(self, consumableID):
        return ConsumableDB.get(consumableID, None)

    def getSkillByID(self, skillID):
        return _skills_data.SkillDB.get(skillID, None)

    def getSkillWithRelations(self):
        return SkillWithRelationsDB.copy()

    def getSpecializationByID(self, specializationID):
        return SpecializationsDB.get(specializationID, None)

    def getCrewNationByID(self, nation, bodyType = CREW_BODY_TYPE.MALE):
        nationData = CrewNationsDB.get(nation, None)
        if nationData:
            return nationData.get(bodyType, None)
        else:
            return

    def getAvailableEquipmentByPlaneID(self, planeID):
        from _equipment_data import Filter
        plane = self.getAircraftData(planeID)
        ids = list(Filter['nation'].get(plane.airplane.country, set()).intersection(Filter['level'].get(plane.airplane.level, set())).intersection(Filter['planeType'].get(plane.airplane.planeType, set())).union(Filter['include'].get(planeID, set())).difference(Filter['exclude'].get(planeID, set())))
        ids.sort()
        return ids

    def getAvailablePlanesByEquipmentID(self, eID):
        from _equipment_data import Filter
        planes = []
        for planeID, plane in self.__aircrafts.iteritems():
            airplane = plane.airplane
            if eID in Filter['include'].get(planeID, set()) or eID in Filter['nation'].get(airplane.country, set()) and eID in Filter['level'].get(airplane.level, set()) and eID in Filter['planeType'].get(airplane.planeType, set()) and eID not in Filter['exclude'].get(planeID, set()):
                planes.append(planeID)

        return planes

    def getAvailableConsumablesByPlaneID(self, planeID):
        from _consumables_data import Filter
        plane = self.getAircraftData(planeID)
        ids = list(Filter['nation'].get(plane.airplane.country, set()).intersection(Filter['level'].get(plane.airplane.level, set())).intersection(Filter['planeType'].get(plane.airplane.planeType, set())).union(Filter['include'].get(planeID, set())).difference(Filter['exclude'].get(planeID, set())))
        ids.sort()
        return ids

    def getAvailablePlanesByConsumableID(self, cID):
        from _consumables_data import Filter
        planes = []
        for planeID, plane in self.__aircrafts.iteritems():
            airplane = plane.airplane
            if cID in Filter['include'].get(planeID, set()) or cID in Filter['nation'].get(airplane.country, set()) and cID in Filter['level'].get(airplane.level, set()) and cID in Filter['planeType'].get(airplane.planeType, set()) and cID not in Filter['exclude'].get(planeID, set()):
                planes.append(planeID)

        return planes

    def calculateBeltMinMaxDamage(self, gunData, beltData):
        """
        Returns min and max belt damage for specific gun
        @param gunData: gun db data
        @param beltData: belt db data
        @return: tuple of type (<minDamage>, <maxDamage>)
        """
        minDamage = 0
        maxDamage = 0
        for ammoName in self.getAmmoNames(gunData, beltData):
            ammo = self.getComponentByName(COMPONENT_TYPE.AMMO, ammoName)
            minDamage += (ammo.explosivePart + ammo.kineticPartMaxDist) * gunData.DPS
            maxDamage += (ammo.explosivePart + ammo.kineticPartMinDist) * gunData.DPS

        return (round(minDamage / len(beltData.ammo), 2), round(maxDamage / len(beltData.ammo), 2))

    def isDefaultBelt(self, beltData):
        for ammoType in beltData.ammo:
            if ammoType != AMMO_TYPE.BALL:
                return False

        return True

    def getDefaultAmmoName(self, gunData):
        for ammunition in gunData.ammunition:
            if ammunition.type == AMMO_TYPE.BALL:
                return ammunition.name

    def getBeltSuitableGuns(self, beltID):
        return filter(lambda x: beltID in x.compatibleBeltIDs, self.getComponents(consts.COMPONENT_TYPE.GUNS))

    def calculateBeltSpec(self, gunData, beltData, spec):
        """
        Returns belt fire chance for specific gun
        @param gunData: gun db data
        @param beltData: belt db data
        @param specName: AMMOBELT_SPECS field
        @rtype: float, float
        """
        ammoLen = len(beltData.ammo)
        if not ammoLen:
            return (0.0, 0.0)
        value = 0
        show = 0
        for ammoName in self.getAmmoNames(gunData, beltData):
            ammo = self.getComponentByName(COMPONENT_TYPE.AMMO, ammoName)
            value += getattr(ammo, spec.name)
            flag = getattr(ammo, spec.flag)
            if flag > 0:
                show = flag

        return (value / ammoLen, show)

    def getAmmoNames(self, gunData, beltData):
        """
        Return ammo names for specific gun and belt
        @param gunData:
        @param beltData:
        """
        for ammoType in beltData.ammo:
            ammo = next((a for a in gunData.ammunition if ammoType == a.type), None)
            if ammo is not None:
                yield ammo.name
            else:
                LOG_ERROR('Unknown ammoType = {0} in ammoBelt = {1}'.format(ammoType, beltData.name))

        return

    def __getMinMaxSpecsByLevel(self, level, specKey):
        import _performanceCharacteristics_db
        specValues = self.__minMaxSpecsHash.get(level, {})
        ret = specValues.get(specKey, None)
        if ret is not None:
            return (ret[0], ret[1])
        else:
            minValue = 1000000000.0
            maxValue = -1000000000.0
            for globalID, specs in _performanceCharacteristics_db.airplanes.iteritems():
                try:
                    planeLevel = self.getPlaneLevelByGlobalID(globalID)
                except AircraftNotFoundException:
                    planeLevel = -1

                if level != planeLevel:
                    continue
                planeID = self.getPlaneIDByGlobalID(globalID)
                if self.isPlaneNPC(planeID):
                    continue
                planeInfo = self.getAircraftData(planeID)
                if planeInfo.isDev():
                    continue
                value = specs.__dict__[specKey]
                maxValue = max(value, maxValue)
                minValue = min(value, minValue)

            specValues[specKey] = (minValue, maxValue)
            self.__minMaxSpecsHash[level] = specValues
            return (minValue, maxValue)

    def getSpecRatioValue(self, globalID, specKey, specTable = None):
        import _performanceCharacteristics_db
        minValue, maxValue = self.__getMinMaxSpecsByLevel(self.getPlaneLevelByGlobalID(globalID), specKey)
        if specTable:
            spec = specTable.__dict__[specKey]
        else:
            spec = _performanceCharacteristics_db.airplanes[globalID].__dict__[specKey]
        divider = maxValue - minValue
        if divider != 0:
            value = (spec - minValue) / divider
        else:
            value = 0
        return value

    def getShopPlaneList(self):
        return filter(lambda x: not self.isPlaneNPC(x), self.getPlaneIDList())

    def getPremiumPlaneList(self):
        return filter(lambda x: self.isPlanePremium(x), self.getShopPlaneList())

    def getExclusivePlaneList(self):
        return filter(lambda x: self.isPlaneExclusive(x), self.getShopPlaneList())

    def getTicketsPlanesList(self):
        """
        Return planes ids that could be bought by tickets
        @rtype: list[int]
        """
        return map(lambda i: i[0], ifilter(lambda p: not self.isPlaneNPC(p[0]) and getattr(p[1].airplane.options, 'tickets', 0) > 0, self.__aircrafts.iteritems()))

    def getSuitablePlanesForUpgrade(self, upgrade):
        planes = []
        if upgrade is None:
            return planes
        else:
            for upgradeVariant in upgrade.variant:
                planeID = self.getAircraftIDbyName(upgradeVariant.aircraftName)
                if planeID not in planes and planeID is not None:
                    planes.append(planeID)

            return planes

    def getUpgradeSellPrice(self, ob):
        if hasattr(ob, 'sellPrice') and ob.sellPrice:
            return int(ob.sellPrice)
        if hasattr(ob, 'price'):
            price = ob.price
        elif hasattr(ob, 'credits'):
            price = ob.credits
        else:
            price = 0
        price += getattr(ob, 'gold', 0) * _economics.Economics.goldRateForCreditBuys
        price += getattr(ob, 'tickets', 0) * _economics.Economics.creditsTicketSellPrice
        return int(price * _economics.Economics.sellCoeff)

    def getUpgradePrice(self, ob):
        if hasattr(ob, 'price'):
            price = ob.price
        elif hasattr(ob, 'credits'):
            price = ob.credits
        else:
            price = 0
        gold = getattr(ob, 'gold', 0)
        tickets = getattr(ob, 'tickets', 0)
        return (int(price), int(gold), int(tickets))

    def isPlanePremium(self, planeID):
        try:
            options = self.getAircraftData(planeID).airplane.options
        except AircraftNotFoundException:
            LOG_CURRENT_EXCEPTION()
            return False

        if getattr(options, 'gold', 0) or getattr(options, 'isExclusive', False) or getattr(options, 'tickets', 0):
            return True
        return False

    def __checkDevPlaneInDatabase(self):
        """
        @type errorList: list
        """
        tstart = time()
        LOG_WARNING('Start check DEV plane DB')
        print 'Start check DEV plane DB'
        errs = ''
        import _aircrafts_db
        import _presets_data
        import _airplanesConfigurations_db
        import _performanceCharacteristics_db
        import _camouflages_data
        import _consumables_data
        import _accounttypes
        devPlanes = [ aircraft.name for aircraft in _aircrafts_db.DB.aircraft if aircraft.options.isDev ]
        devPlanesID = [ aircraft.id for aircraft in _aircrafts_db.DB.aircraft if aircraft.options.isDev ]
        devPlanesStr = [ '{0}:{1}'.format(aircraft.id, aircraft.name) for aircraft in _aircrafts_db.DB.aircraft if aircraft.options.isDev ]
        if not IS_DEVELOPMENT:
            if devPlanes:
                errs += '\nList of dev planes:' + ';'.join(devPlanesStr) + ';'
            for upg in _upgrades_db.DB.upgrade:
                for i in xrange(len(upg.variant) - 1, -1, -1):
                    v = upg.variant[i]
                    if v.aircraftName in devPlanes:
                        errs += "\nError in module '{0}', variant #{1} for plane {2}".format(upg.name, i, v.aircraftName)

            for i in xrange(len(_presets_data.PresetsData.aircraft) - 1, -1, -1):
                p = _presets_data.PresetsData.aircraft[i]
                if p.name in devPlanes:
                    errs += "\nError _presets_data.PresetsData['{0}']".format(i)

            GlobalIDs = [ gID for gID, conf in _airplanesConfigurations_db.airplanesConfigurations.iteritems() if conf.planeID in devPlanesID ]
            if GlobalIDs:
                _GlobalIDs = [ str(gID) for gID, conf in _airplanesConfigurations_db.airplanesConfigurations.iteritems() if conf.planeID in devPlanesID ]
                errs += '\nList of dev globalID:' + ';'.join(_GlobalIDs) + ';'
            for gID in GlobalIDs:
                errs += "\nError _airplanesConfigurations_db.airplanesConfigurations['{0}']".format(gID)
                errs += "\nError _performanceCharacteristics_db.airplanes['{0}']".format(gID)

            for ID in devPlanesID:
                if _airplanesConfigurations_db.airplanesDefaultConfigurations.has_key(ID):
                    errs += "\nError _airplanesConfigurations_db.airplanesDefaultConfigurations['{0}']".format(ID)
                if _airplanesConfigurations_db.airplanesConfigurationsList.has_key(ID):
                    errs += "\nError _airplanesConfigurations_db.airplanesConfigurationsList['{0}']".format(ID)

            for i in xrange(len(_camouflages_data.Camouflages.camouflage) - 1, -1, -1):
                cam = _camouflages_data.Camouflages.camouflage[i]
                if cam.planeID in devPlanesID:
                    errs += "\nError Camouflages.camouflage['{0}'] for plane {1}".format(i, cam.planeID)

            for c in _consumables_data.Consumables.consumable:
                for i in xrange(len(c.excludeList) - 1, -1, -1):
                    p = c.excludeList[i]
                    if p in devPlanesID:
                        errs += "\nError in _consumables_data.Consumables.consumable['{0}'] for plane {1}".format(i, p)

            for i in xrange(len(_accounttypes.AccountTypesData.bonuses)):
                b = _accounttypes.AccountTypesData.bonuses[i]
                for p in b.initialAircraft:
                    if p in devPlanes:
                        errs += '\nError (DEV PLANE) in _accounttypes.AccountTypesData.bonuses[{0}].initialAircraft = {1}; .id={2}'.format(i, p, b.id)

        else:
            for upg in _upgrades_db.DB.upgrade:
                hasDev = False
                hasProd = False
                for i in xrange(len(upg.variant) - 1, -1, -1):
                    v = upg.variant[i]
                    if v.aircraftName in devPlanes:
                        hasDev = True
                    else:
                        hasProd = True

                if hasDev and hasProd:
                    errs += "\nError in module '{0}', module has variants for dev and prod planes!!!".format(upg.name)

        print 'Start check empty links'
        allPlanes = [ aircraft.name for aircraft in _aircrafts_db.DB.aircraft ]
        allPlanesID = [ aircraft.id for aircraft in _aircrafts_db.DB.aircraft ]
        for upg in _upgrades_db.DB.upgrade:
            for i in xrange(len(upg.variant) - 1, -1, -1):
                v = upg.variant[i]
                if v.aircraftName not in allPlanes:
                    errs += "\nError in module '{0}', variant #{1} for UNKNOWN plane {2}".format(upg.name, i, v.aircraftName)

        for i in xrange(len(_presets_data.PresetsData.aircraft) - 1, -1, -1):
            p = _presets_data.PresetsData.aircraft[i]
            if p.name not in allPlanes:
                errs += "\nError _presets_data.PresetsData['{0}'] - Unkown plane {1}".format(i, p.name)

        GlobalIDs = [ gID for gID, conf in _airplanesConfigurations_db.airplanesConfigurations.iteritems() if conf.planeID not in allPlanesID ]
        if GlobalIDs:
            _GlobalIDs = [ str(gID) for gID, conf in _airplanesConfigurations_db.airplanesConfigurations.iteritems() if conf.planeID not in allPlanesID ]
            errs += '\nList of globalID for unknown plane:' + ';'.join(_GlobalIDs) + ';'
        for gID in GlobalIDs:
            errs += "\nError _airplanesConfigurations_db.airplanesConfigurations['{0}']".format(gID)
            errs += "\nError _performanceCharacteristics_db.airplanes['{0}']".format(gID)

        for i in xrange(len(_camouflages_data.Camouflages.camouflage) - 1, -1, -1):
            cam = _camouflages_data.Camouflages.camouflage[i]
            if cam.planeID not in allPlanesID:
                errs += "\nError Camouflages.camouflage['{0}'] for unknown plane {1}".format(i, cam.planeID)

        for c in _consumables_data.Consumables.consumable:
            for i in xrange(len(c.excludeList) - 1, -1, -1):
                p = c.excludeList[i]
                if p not in allPlanesID:
                    errs += "\nError in _consumables_data.Consumables.consumable['{0}'] for unknown plane {1}".format(i, p)

        for i in xrange(len(_accounttypes.AccountTypesData.bonuses)):
            b = _accounttypes.AccountTypesData.bonuses[i]
            for p in b.initialAircraft:
                if p not in allPlanes:
                    errs += '\nError (UNKNOWN PLANE) in _accounttypes.AccountTypesData.bonuses[{0}].initialAircraft = {1}; .id={2}'.format(i, p, b.id)

        tlen = time() - tstart
        LOG_WARNING('Finish check DEV plane. Time = {0} sec'.format(tlen))
        print 'Finish check DEV plane. Time = {0} sec'.format(tlen)
        return errs

    def getGunBonusBelts(self, gunName, planeID = None):
        """
        Return ammobelts ids for specified gun
        @param gunName:
        @return: generator
        """
        if planeID:
            planeType = self.getAircraftData(planeID).airplane.planeType
            availableAmmoTypes = _weapons.AVAILABLE_BELTS_BY_PLANE_TYPE[planeType]
        else:
            availableAmmoTypes = AMMO_TYPE.ALL_TYPES
        for beltID in self.getComponentByName(COMPONENT_TYPE.GUNS, gunName).compatibleBeltIDs:
            beltData = self.getComponentByID(COMPONENT_TYPE.AMMOBELT, beltID)
            if beltData.gold > 0 and beltData.ammo[0] in availableAmmoTypes:
                yield beltID

    def getCrewMembersData(self, aircraftId):
        """
        Return the crew parts instances
        @param aircraftId:
        @return: generator
        """
        aircraftData = self.getAircraftData(aircraftId)
        return (part for part in aircraftData.airplane.partsSettings.getPartsOnlyList() if part.getFirstPartType().componentType in CREW_MEMBER.values())

    def getUpgradeByID(self, upgradeID):
        return self.getUpgradeByName(self.getUpgradeNameByID(upgradeID))

    def getParentVariantBelongsToPlane(self, upgrade, planeID = None, planeName = None):
        """
           upgrade - should be an upgrade instance or upgrade name or upgrade id - whatever fits,
                           it will be processed differently by argument type (int is id, str is name, otherwise is upgrade itself)
        """
        if not planeName and planeID:
            planeName = self.getAircraftName(planeID)
        if planeName:
            upgrade = upgrade if not isinstance(upgrade, (int, str)) else (self.getUpgradeByID if isinstance(upgrade, int) else self.getUpgradeByName)(upgrade)
            if upgrade:
                for variant in upgrade.variant:
                    if variant.aircraftName == planeName:
                        return variant.parentUpgrade[0]

        return None

    def getParentUpgradeBelongsToPlane(self, upgrade, planeID = None, planeName = None):
        """
           one of planeID or planeName is mandatory, if both given planeName takes precedence
        """
        variant = self.getParentVariantBelongsToPlane(upgrade, planeID, planeName)
        if variant and variant.name:
            return self.getUpgradeByName(variant.name)
        else:
            return None

    def getExperienceToOpenUpgrade(self, parentPlaneID, upgradeID = None, planeToUpgradeID = None):
        """
        returns experience you need to open particular upgrade/plane, without the dependencies
        if planeToUpgradeID is given it takes precedence over upgradeID
        """
        if planeToUpgradeID:
            upgradeID = self.getUpgradeByAircraftID(planeToUpgradeID)
        variant = self.getParentVariantBelongsToPlane(upgradeID, parentPlaneID)
        if variant:
            return variant.experience
        return 0

    def specializationCompatibleWithPlane(self, specializationID, planeID):
        """
        Checks if specialization is compatible with plane.
        """
        planeData = self.getAircraftData(planeID)
        planeGlobalID = airplanesDefaultConfigurations[planeID]
        planeConfig = getAirplaneConfiguration(planeGlobalID)
        from CrewHelpers import getCrewSpecialization
        planeSpecializations = getCrewSpecialization(planeData.airplane.partsSettings, planeConfig.partTypes)
        return specializationID in planeSpecializations

    def computeEliteStatus(self, planeID, pdata):
        if self.isPlanePremium(planeID):
            return True
        try:
            aircraftData = self.getAircraftData(planeID)
        except db.DBLogic.AircraftNotFoundException:
            LOG_CURRENT_EXCEPTION()
            return False

        for wSlot in aircraftData.components.weapons2.slots.values():
            for wType in wSlot.types.values():
                if len(wType.weapons) > 0 and wType.weapons[0].name not in pdata['inventory']['upgrades']:
                    return False

        upgrades, aircrafts = self.getAircraftUpgrades(planeID)
        for aircraft in aircrafts:
            if self.getAircraftIDbyName(aircraft.name) not in pdata['inventory']['openedAircrafts']:
                return False

        for upg in upgrades:
            if upg.type in consts.UPGRADE_TYPE.MODULES and upg.name not in pdata['inventory']['upgrades']:
                return False

        return True

    def getPlaneMaxSpec(self, planeID, tag):
        spec = self._planeMaxSpecsHash.get(planeID, {}).get(tag, None)
        if spec is not None:
            return spec
        else:
            specKey = SPECS_KEY_MAP[tag]
            spec = 0
            for globalID in airplanesConfigurationsList[planeID]:
                specs = _performanceCharacteristics_db.airplanes[globalID]
                cmpSpec = getattr(specs, specKey)
                if cmpSpec > spec:
                    spec = cmpSpec

            self._planeMaxSpecsHash.setdefault(planeID, {})[tag] = spec
            return spec

    def getShootingDistanceEffective(self, globalID):
        """
        Get effective shooting distance for specified plane configuration.
        @param globalID: Configuration, to process.
        @type globalID: int
        @return: Effective shooting distance
        @rtype: float
        """
        configuration = getAirplaneConfiguration(globalID)
        planeID, weaponSlots = configuration.planeID, configuration.weaponSlots
        maxShootingDistance = 0
        for slotID, slotConfigID in weaponSlots:
            weaponInfo = self.getWeaponInfo(planeID, slotID, slotConfigID)
            if not weaponInfo:
                continue
            wType, wName, _ = weaponInfo
            if wType != UPGRADE_TYPE.GUN:
                continue
            weapon = self.getComponentByName(COMPONENT_TYPE.GUNS, wName)
            maxShootingDistance = max(weapon.bulletFlyDist, maxShootingDistance)

        planeData = self.getAircraftData(planeID)
        return maxShootingDistance * planeData.airplane.flightModel.weaponOptions.bulletMinFlightDist

    def getBotPickWeightWithPlaneID(self, planeID):
        planeData = self.getAircraftData(planeID)
        return planeData.airplane.balancer.BotPickWeight

    def getFractionByPlaneID(self, planeID):
        if _warAction.checkPlaneInAllyCommandFilter(planeID):
            return FRACTION.ALLY
        if _warAction.checkPlaneInAxisCommandFilter(planeID):
            return FRACTION.AXIS
        return FRACTION.UNDEFINED

    def isPlaneInFraction(self, planeID, fraction):
        if fraction == FRACTION.ALLY:
            return _warAction.checkPlaneInAllyCommandFilter(planeID)
        if fraction == FRACTION.AXIS:
            return _warAction.checkPlaneInAxisCommandFilter(planeID)
        return _warAction.checkPlaneInGlobalFilter(planeID)

    def getOppositeFraction(self, fraction):
        if fraction == FRACTION.ALLY:
            return FRACTION.AXIS
        if fraction == FRACTION.AXIS:
            return FRACTION.ALLY
        return FRACTION.UNDEFINED