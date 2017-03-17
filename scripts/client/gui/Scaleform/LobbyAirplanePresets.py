# Embedded file name: scripts/client/gui/Scaleform/LobbyAirplanePresets.py
import BigWorld
import db.DBLogic
from debug_utils import LOG_DEBUG, LOG_INFO, LOG_ERROR
from consts import UPGRADE_TYPE, PLANE_TYPE
from HelperFunctions import findIf
from Helpers.i18n import localizePresets, localizeComponents, localizeTooltips
from LobbyAirplaneHelper import getLobbyAirplane
from Helpers.PerformanceSpecsHelper import getPerformanceSpecsTableDeprecated
CUSTOM_PRESET_NAME = 'custom'
PENDANT_ARMS_ROLE = 'FIGHTER-BOMBER'
MAX_ROLES_IN_PRESET = 3
ROLES_ENABLED = False

class LobbyAirplanePresets(object):

    class __RolesVO:

        def __init__(self, icoPath = '', locDescription = ''):
            self.icoPath = icoPath
            self.locDescription = locDescription

    class __PresetVO:

        def __init__(self):
            self.name = ''
            self.title = ''
            self.isInstalled = False
            self.isAvailable = False
            self.modulesList = []
            self.weaponsList = []
            self.rolesList = []

    def __init__(self, aircraftID, modulesHelper, weaponsHelper, customPresetUpgrades = None, availablePresetList = [], installedPresetName = None):
        self.__aircraftID = aircraftID
        self.__installedPresetName = installedPresetName
        self.__modulesHelper = modulesHelper
        self.__weaponsHelper = weaponsHelper
        self.__presetsList = None
        self.__customPreset = None
        self.__customPresetUpgrades = customPresetUpgrades
        self.__availablePresetList = availablePresetList
        return

    def __deepcopy__(self, var):
        clone = LobbyAirplanePresets(self.__aircraftID, self.__modulesHelper, self.__weaponsHelper, self.__customPresetUpgrades, self.__availablePresetList, self.__installedPresetName)
        ignoreAttrList = ['_LobbyAirplanePresets__weaponsHelper',
         '_LobbyAirplanePresets__lobbyCarouselHelper',
         '_LobbyAirplanePresets__customPreset',
         '_LobbyAirplanePresets__modulesHelper']
        for name, value in self.__dict__.iteritems():
            if name in ignoreAttrList:
                continue
            if value is None:
                setattr(clone, name, value)
            else:
                setattr(clone, name, type(value)(value))

        return clone

    def destroy(self):
        self.__aircraftID = None
        self.__installedPresetName = None
        self.__modulesHelper = None
        self.__weaponsHelper = None
        self.__presetsList = None
        self.__customPreset = None
        self.__customPresetUpgrades = None
        self.__availablePresetList = None
        return

    def getInstalled(self):
        for p in self.__presetsList:
            if p.name == self.__installedPresetName:
                return p

        return None

    def getAll(self):
        return self.__presetsList

    def getNonEmpty(self):
        return filter(lambda p: len(p.modulesList) and len(p.weaponsList), self.__presetsList)

    def getCustomPreset(self):
        return self.__customPreset

    def findPreset(self, presetName):
        return next((preset for preset in self.__presetsList if preset.name == presetName), None)

    def __buildPreset(self, name, modules, weapons, rolesList):
        preset = LobbyAirplanePresets.__PresetVO()
        preset.name = name
        preset.title = localizeComponents('PRESET_NAME_%s' % name) if name == CUSTOM_PRESET_NAME else localizePresets('PRESET_NAME_%s' % name)
        preset.modulesList = modules
        preset.weaponsList = weapons
        preset.isAvailable = name in self.__availablePresetList
        preset.rolesList = rolesList
        return preset

    def fillPresets(self):
        presetsList = db.DBLogic.g_instance.getAircraftPresetsListByID(self.__aircraftID)
        self.__presetsList = []
        if presetsList is not None:
            for preset in presetsList:
                preset = self.__buildPreset(preset.name, [ item.name for item in preset.module ], [ {'slot': item.slot,
                 'configuration': item.configuration} for item in preset.weapon ], [ LobbyAirplanePresets.__RolesVO(self.__getRoleIcoPath(role.name), self.__getRolelocDescription(role.name)) for role in preset.role ] if ROLES_ENABLED and hasattr(preset, 'role') else [])
                self.__presetsList.append(preset)

        if self.__customPresetUpgrades is not None:
            modulesList, weapons = self.__customPresetUpgrades
            weaponsList = [ {'slot': item[0],
             'configuration': item[1]} for item in weapons ]
            rolesList = self.__getRolesForCustomPreset(presetsList, modulesList, weaponsList) if ROLES_ENABLED and presetsList is not None else []
            preset = self.__buildPreset(CUSTOM_PRESET_NAME, modulesList, weaponsList, rolesList)
        else:
            preset = self.__buildPreset(CUSTOM_PRESET_NAME, [], [], [])
        self.__presetsList.append(preset)
        self.__customPreset = preset
        installedPreset = self.getInstalled()
        if installedPreset is not None:
            installedPreset.isInstalled = True
        return

    def __getRolesForCustomPreset(self, presetsList, modulesList, weaponsList):
        rolesList = []
        from BWPersonality import g_lobbyCarouselHelper
        airplane = g_lobbyCarouselHelper.getCarouselAirplane(self.__aircraftID)
        if not airplane:
            airplane = getLobbyAirplane(self.__aircraftID)
        if airplane is not None:
            currentVehicleInfo = airplane.previewPreset(modulesList, weaponsList)
            currentCharacteristics = getPerformanceSpecsTableDeprecated(currentVehicleInfo, False)
            if currentCharacteristics is None:
                LOG_ERROR('__getRolesForCustomPreset - currentCharacteristics is None aircraftID=%s' % self.__aircraftID)
                return rolesList
            allListCharacteristics = []
            for preset in presetsList:
                modulesList = [ item.name for item in preset.module ]
                weaponsList = [ {'slot': item.slot,
                 'configuration': item.configuration} for item in preset.weapon ]
                vehicleInfo = airplane.previewPreset(modulesList, weaponsList)
                characteristics = getPerformanceSpecsTableDeprecated(vehicleInfo, False)
                if characteristics is not None:
                    allListCharacteristics.append(characteristics)
                else:
                    LOG_ERROR('__getRolesForCustomPreset - characteristics is None for modulesList=%s and weaponsList=%s' % (modulesList, weaponsList))

            if not allListCharacteristics:
                LOG_ERROR('__getRolesForCustomPreset - allListCharacteristics is empty')
                return rolesList
            attrList = ['dps', 'maxSpeed', 'averageTurnTime']
            presetIndex = PresetRolesStrategy.getMostAppropriateIndex(currentCharacteristics, allListCharacteristics, attrList)
            if presetIndex is None:
                LOG_ERROR('__getRolesForCustomPreset - error presetIndex')
            else:
                LOG_DEBUG('__getRolesForCustomPreset - set preset index:%s' % str(presetIndex))
                preset = presetsList[presetIndex]
                pendantArmsRoleAdded = False
                for role in preset.role:
                    if role.name == PENDANT_ARMS_ROLE:
                        if currentVehicleInfo.weapons.shellsCount and airplane.planeType != PLANE_TYPE.ASSAULT:
                            pendantArmsRoleAdded = True
                            rolesList.append(LobbyAirplanePresets.__RolesVO(self.__getRoleIcoPath(role.name), self.__getRolelocDescription(role.name)))
                    else:
                        rolesList.append(LobbyAirplanePresets.__RolesVO(self.__getRoleIcoPath(role.name), self.__getRolelocDescription(role.name)))

                if currentVehicleInfo.weapons.shellsCount and len(rolesList) < MAX_ROLES_IN_PRESET and airplane.planeType != PLANE_TYPE.ASSAULT and not pendantArmsRoleAdded:
                    rolesList.append(LobbyAirplanePresets.__RolesVO(self.__getRoleIcoPath(PENDANT_ARMS_ROLE), self.__getRolelocDescription(PENDANT_ARMS_ROLE)))
                if airplane.planeType != PLANE_TYPE.ASSAULT and not rolesList and len(preset.role) == 1:
                    roleName = preset.role[0].name
                    rolesList.append(LobbyAirplanePresets.__RolesVO(self.__getRoleIcoPath(roleName), self.__getRolelocDescription(roleName)))
        else:
            LOG_ERROR('__getRolesForCustomPreset - airplane object is None')
        return rolesList

    def __getRoleIcoPath(self, name):
        """
        @param: name - role name
        @return: path to role image
        """
        roleInfo = db.DBLogic.g_instance.getPresetRolesInfo(name.upper())
        if roleInfo is not None:
            return roleInfo.iconPath
        else:
            LOG_ERROR('__getRoleIcoPath - Error preset role name: %s' % name.upper())
            return ''
            return

    def __getRolelocDescription(self, name):
        """
        @param: name - role name
        @return: loc description
        """
        return localizeTooltips('TOOLTIP_ROLES_%s' % name.upper())


class PresetRolesStrategy:

    @staticmethod
    def getMostAppropriateIndex(currentCharacteristics, allListCharacteristics, attrList):
        """
        @param: currentCharacteristics - current characteristics object
        @param: allListCharacteristics - list of all characteristics
        @param: attrList - list of string attributes
        @return: int index from allListCharacteristics if success or None if False
        """
        res = []
        for airplaneCharacteristics in allListCharacteristics:
            summ = 0
            for attribute in attrList:
                currentValue = getattr(currentCharacteristics, attribute)
                airplaneValue = getattr(airplaneCharacteristics, attribute)
                try:
                    summ += abs(currentValue - airplaneValue) / currentValue
                except:
                    LOG_ERROR('getMostAppropriateIndex - attribute(%s) in PerformanceCharacteristic = 0' % attribute)

            res.append(summ * 100)

        if res:
            return res.index(min(res))
        else:
            return None