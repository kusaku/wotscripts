# Embedded file name: scripts/client/gui/Scaleform/LobbyAirplaneWeapons.py
import copy
import _airplanesConfigurations_db
import consts
import db.DBLogic
import operator
from debug_utils import LOG_DEBUG, LOG_INFO, LOG_ERROR, LOG_TRACE
from consts import UPGRADE_TYPE
from clientConsts import WEAPON_TYPE_TO_UPDATABLE_TYPE_MAP
from HelperFunctions import findIf
from Helpers.i18n import localizeComponents, localizeLobby
import Event
from Helpers.PerformanceSpecsHelper import ProjectileInfo
EMPTY_WEAPON_NAME_ID = 'empty'

class LobbyAirplaneWeapons(object):

    class __Configuration:

        def __init__(self):
            self.weaponName = ''
            self.weaponType = ''
            self.weaponNameID = ''
            self.description = ''
            self.neededCount = 0
            self.haveCount = 0
            self.installedCount = 0
            self.loadedBullets = 1
            self.weaponGroup = 0
            self.isInstalled = False
            self.isInstallAvailable = False
            self.weaponSlotID = -1
            self.configurationID = -1
            self.icoPath = ''
            self.priceCredits = 0
            self.priceGold = 0
            self.parentName = ''
            self.level = 1
            self.isDefault = False

    class ShellVO:

        def __init__(self, slotID, data):
            self.slotID = slotID
            self.weaponType = data['weaponType']
            self.storeCount = data['storeCount']
            self.maxCount = data['maxCount']
            self.curCount = data['curCount']
            self.title = localizeComponents('WEAPON_NAME_' + data['weaponID'])
            shellDBGroupID, shellDescription = db.DBLogic.g_instance.getShellComponentsGroupIDAndDescription(data['weaponID'])
            self.price = data['price']
            self.icoPath = shellDescription.hudIcoPath

    def __init__(self, aircraftID, upgradesList, installedWeapons, update = True):
        """
        
        @param aircraftID:
        @param upgradesList:
        @param installedWeapons: [(<slotID>, <slotConfigurationID>), ...]
        @param update:
        @return:
        """
        self.__eventManager = Event.EventManager()
        self.onChangeShellCount = Event.Event(self.__eventManager)
        self.__aircraftID = aircraftID
        self.__upgradesList = upgradesList
        self.__installedWeapons = installedWeapons
        self.__slotsInfo = None
        self.__slotsShellCount = {}
        self.__weaponSlotsMap = {}
        self.__slotsInfoMap = {}
        if update:
            self.update()
        return

    def __deepcopy__(self, var):
        clone = LobbyAirplaneWeapons(self.__aircraftID, None, None, False)
        for name, value in self.__dict__.iteritems():
            if name == 'onChangeShellCount' or name == '_LobbyAirplaneWeapons__eventManager':
                continue
            if value is None:
                setattr(clone, name, value)
            else:
                setattr(clone, name, copy.deepcopy(type(value)(value)))

        return clone

    @property
    def slotsInfo(self):
        return self.__slotsInfo

    def DEBUG_printSlots(self):
        print 'max_cn DEBUG_printSlots'
        for slotData in self.__slotsInfo:
            if slotData.__class__ == LobbyAirplaneWeapons.ShellVO:
                print slotData.weaponType, slotData.storeCount, slotData.maxCount, slotData.curCount
            else:
                print (slotData.slotID,
                 slotData.title,
                 slotData.curBelt,
                 slotData.beltsList)

    def updateSlotsInfo(self, serverData):
        self.__slotsInfo = [ LobbyAirplaneWeapons.ShellVO(slotID, slotData) for slotID, slotData in serverData.items() if slotData['weaponType'] == UPGRADE_TYPE.GUN ]
        self.__slotsShellCount = dict(((slotID, data['curCount']) for slotID, data in serverData.iteritems() if data['weaponType'] in (UPGRADE_TYPE.BOMB, UPGRADE_TYPE.ROCKET)))
        self.onChangeShellCount()

    def updateAmoSlotData(self, slotID, data):
        for slotData in self.__slotsInfo:
            if slotData.slotID == slotID:
                if slotData.weaponType == UPGRADE_TYPE.GUN:
                    slotData.curBelt = data
                else:
                    curCount, storeChangeCount = data
                    slotData.curCount = curCount
                    slotData.storeCount += storeChangeCount
                    self.__slotsShellCount[slotID] = curCount
                self.onChangeShellCount()
                return

    @property
    def slotsShellCount(self):
        return self.__slotsShellCount

    def destroy(self):
        self.__aircraftID = None
        self.__weaponSlotsMap = None
        self.__slotsInfoMap = None
        self.__slotsInfo = None
        self.__eventManager.clear()
        return

    def update(self, upgradesList = None):
        self.__upgradesList = upgradesList or self.__upgradesList
        weaponsSettings = self.__getWeaponsSettings(self.__aircraftID)
        if weaponsSettings is None:
            LOG_ERROR('weaponsSettings for aircraft not found. AircraftID', self.__aircraftID)
            return
        else:
            for slotSettings in weaponsSettings.slots.values():
                self.__fillSlot(slotSettings)

            self.__setInstalledWeapons()
            return

    def setInstalledWeapons(self, weaponsSlotList):
        """
        get weaponsSlotList from server and set by using private __setInstalledWeapons
        @param weaponsSlotList: [(<slotID>, <slotConfigurationID>), ...]
        """
        self.__installedWeapons = weaponsSlotList
        LOG_DEBUG('setInstalledWeapons', self.__installedWeapons)
        self.__setInstalledWeapons()

    def getSortedSlotWeaponsList(self, slotID):
        slotWeaponsMap = self.__weaponSlotsMap.get(slotID, None)
        if slotWeaponsMap is None:
            LOG_ERROR('Not weapons in slot. SlotID', slotID)
            return
        else:
            slotWeaponsMap.sort(key=operator.attrgetter('weaponGroup'))
            return slotWeaponsMap

    def getWeaponConfigurations(self, slotID, configurationID):
        if slotID not in self.__weaponSlotsMap:
            LOG_ERROR('Aircraft has not this slot. AircraftID, SlotID ', self.__aircraftID, slotID)
            return None
        elif configurationID >= len(self.__weaponSlotsMap[slotID]):
            LOG_ERROR('SlotID has not this configuration id. SlotID, ConfigurationID ', slotID, configurationID)
            return None
        else:
            return self.__weaponSlotsMap[slotID][configurationID]

    def getWeaponSlotConfigs(self, slotID):
        return self.__weaponSlotsMap[slotID]

    def getSortedWeaponsList(self):
        allConfigurationList = []
        for configurationList in self.__weaponSlotsMap.values():
            allConfigurationList += configurationList

        allConfigurationList.sort(key=operator.attrgetter('weaponSlotID', 'level', 'weaponGroup'))
        return allConfigurationList

    def getInstalledConfigurations(self):

        def generate():
            for slotID, configurationID in self.__installedWeapons:
                configuration = self.getWeaponConfigurations(slotID, configurationID)
                if configuration is not None and configuration.weaponName != '':
                    yield configuration

            return

        return list(generate())

    def getInstalledWeaponsList(self):
        """
        @return: [(<slotID>, slotConfigurationID), ...]
        """
        return self.__installedWeapons

    def getSlotsInfoMap(self):
        return self.__slotsInfoMap

    def getInstalledProjectiles(self):
        ret = []
        for slotID, configurationID in self.__installedWeapons:
            configuration = self.getWeaponConfigurations(slotID, configurationID)
            if configuration is not None and configuration.weaponNameID != '':
                upgrade = db.DBLogic.g_instance.upgrades.get(configuration.weaponNameID)
                if upgrade is None:
                    continue
                if upgrade.type == UPGRADE_TYPE.BOMB or upgrade.type == UPGRADE_TYPE.ROCKET:
                    ret.append(ProjectileInfo(slotID, configurationID, configuration.neededCount, configuration.installedCount))

        return ret

    def __fillConfiguration(self, slotSettings, configurationsSettings, configurationID):
        slotID = slotSettings.id
        if not self.__isConfigurationIDValid(configurationsSettings, configurationID):
            LOG_ERROR("ConfigurationID isn't valid. slotID, configurationID", slotID, configurationID)
            return
        else:
            weapons = configurationsSettings[configurationID].weapons
            configuration = LobbyAirplaneWeapons.__Configuration()
            configuration.isDefault = (slotID, configurationID) in _airplanesConfigurations_db.getDefaultAirplaneConfiguration(self.__aircraftID).weaponSlots
            configuration.weaponSlotID = slotID
            configuration.configurationID = configurationID
            if len(weapons) == 0:
                configuration.weaponNameID = EMPTY_WEAPON_NAME_ID
                configuration.weaponName = localizeLobby('WEAPON_NAME_EMPTY')
                self.__weaponSlotsMap[slotID].append(configuration)
            else:
                it = iter(weapons)
                weapon = it.next()
                configuration.weaponNameID = weapon.name
                configuration.weaponName = localizeComponents('WEAPON_NAME_' + weapon.name)
                configuration.neededCount = len(weapons)
                configuration.weaponGroup = weapon.weaponGroup
                weaponUpgradeMap = self.__getUpgrade(weapon.name)
                if weaponUpgradeMap is not None:
                    configuration.haveCount = weaponUpgradeMap['boughtCount']
                    configuration.installedCount = weaponUpgradeMap['installedCount']
                    configuration.parentName = weaponUpgradeMap['parent']
                upgrade = db.DBLogic.g_instance.upgrades.get(weapon.name, None)
                if upgrade is not None:
                    configuration.level = upgrade.level
                    weaponType = upgrade.type
                    configuration.weaponType = weaponType
                    if weaponType == UPGRADE_TYPE.GUN:
                        gunData = db.DBLogic.g_instance.getGunData(weapon.name)
                        if gunData is None:
                            LOG_ERROR('Weapon has not weapon settings. Weapon name', weapon.name)
                        else:
                            configuration.description = localizeLobby(gunData.gunProfileName.upper() + '_DESCRIPTION')
                    else:
                        configuration.description = localizeComponents(UPGRADE_TYPE.DESCRIPTION_MAP[weaponType])
                    configuration.icoPath = upgrade.typeIconPath
                self.__weaponSlotsMap[slotID].append(configuration)
            return

    def __fillSlot(self, slotSettings):
        slotID = slotSettings.id
        configurationsSettings = slotSettings.types
        if configurationsSettings is None:
            LOG_ERROR('Slot has not any configurations. SlotID', slotID)
            return False
        else:
            self.__weaponSlotsMap[slotID] = []
            self.__slotsInfoMap[slotID] = {'description': localizeLobby('AMMO_SLOT_' + slotSettings.name),
             'title': localizeLobby('AVAILABLE_' + slotSettings.name)}
            for configurationID in configurationsSettings.keys():
                self.__fillConfiguration(slotSettings, configurationsSettings, configurationID)

            return

    def __getUpgrade(self, weaponName):
        if self.__upgradesList is not None:
            return findIf(self.__upgradesList, lambda upgradeMap: upgradeMap['name'] == weaponName)
        else:
            return

    def __isConfigurationIDValid(self, configurationsSettings, configurationID):
        return configurationID in configurationsSettings.keys()

    def __getSlotSettings(self, weaponsSettings, slotID):
        if slotID in weaponsSettings.slots:
            return weaponsSettings.slots[slotID]
        else:
            return None

    def __getWeaponsSettings(self, aircraftID):
        settings = db.DBLogic.g_instance.getAircraftData(aircraftID)
        if settings is not None:
            return settings.components.weapons2
        else:
            return

    def __setInstalledWeapons(self):
        """
        Use internal self.__installedWeapons to set
        """
        for slot in self.__weaponSlotsMap.itervalues():
            for conf in slot:
                conf.isInstalled = (conf.weaponSlotID, conf.configurationID) in self.__installedWeapons

        if self.__upgradesList is not None:
            for upgradeMap in self.__upgradesList:
                if upgradeMap['isInstalled']:
                    for slotID, configurationsList in upgradeMap['slotList'].items():
                        for configurationID in configurationsList:
                            configuration = self.getWeaponConfigurations(slotID, configurationID)
                            if configuration is not None:
                                if configuration.weaponNameID == 'empty':
                                    configuration.isInstallAvailable = True
                                else:
                                    conf = findIf(self.__weaponSlotsMap[slotID], lambda conf: conf.weaponNameID == configuration.weaponNameID)
                                    count = configuration.haveCount + conf.installedCount if conf else configuration.haveCount
                                    configuration.isInstallAvailable = configuration.neededCount <= count

        return

    def canInstallBombsOrRockets(self):
        for slot in self.__weaponSlotsMap.itervalues():
            for conf in slot:
                if conf.weaponType in [consts.UPGRADE_TYPE.BOMB, consts.UPGRADE_TYPE.ROCKET]:
                    return True

        return False