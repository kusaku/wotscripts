# Embedded file name: scripts/common/Inventory.py
from abc import abstractmethod, ABCMeta
from copy import deepcopy
from collections import Counter
import _economics
import consts
import db.DBLogic
from Interfaces import ISYNC_AIRCRAFT, ISYNC_INVENTORY, ISYNC_STATS, ISYNC_PLANE_LIST
from consts import MAX_PARENT_UPGRADES_CHECK_DEPTH, UPGRADE_TYPE, BLOCK_TYPE, CUSTOM_PRESET_NAME, PLANE_KEYS, NATION_DECAL_ID_DEFAULT, COMPONENT_TYPE, IS_CLIENT
from config_consts import IS_DEVELOPMENT
from debug_utils import LOG_WARNING, CRITICAL_ERROR, LOG_ERROR, DBLOG_ERROR, LOG_DEBUG, LOG_TRACE
from HelperFunctions import findIf, select
from _airplanesConfigurations_db import airplanesConfigurations, airplanesDefaultConfigurations, getAirplaneConfiguration, airplanesConfigurationsList, getDefaultAirplaneConfiguration
from CrewHelpers import getCrewSpecialization
from _skills_data import SpecializationSkillDB
import _camouflages_data
from functools import partial

class Inventory():
    __metaclass__ = ABCMeta
    PRESET_STATUS_NONE = 0
    PRESET_STATUS_RESEARCHED = 1
    PRESET_STATUS_BOUGHT = 2

    def __init__(self):
        self._aircraftsData = dict()
        self._inventoryData = dict()
        self._elitePlaneList = []
        self._inventoryDataInitialized = False
        self._stats = dict()
        self._db = db.DBLogic.g_instance
        self._sellPrices = {}
        self._aircraftIDs = [ airplaneID for airplaneID, aircraftData in self._db.getAircraftsDict().items() if not (not IS_DEVELOPMENT and aircraftData.airplane.options.isDev or self._db.isPlaneNPC(airplaneID)) ]
        self._sycnInventoryQuerry = [('ISYNC_INVENTORY', [])]

    def destroy(self):
        self._aircraftsData = None
        self._inventoryData = None
        self._db = None
        self._aircraftIDs = None
        self._sycnInventoryQuerry = None
        return

    @property
    def aircraftsData(self):
        return self._aircraftsData

    @property
    def inventoryData(self):
        return self._inventoryData

    @property
    def inventoryDataInitialized(self):
        return self._inventoryDataInitialized

    def addSlotShellsData(self, aircraftID, weaponSlotID, count, storedCount):
        self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT][PLANE_KEYS.SHELLS][weaponSlotID] = {'count': int(count),
         'storedCount': storedCount}

    def getSlotShellsData(self, aircraftID, weaponSlotID):
        planeData = self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT]
        return planeData[PLANE_KEYS.SHELLS].setdefault(weaponSlotID, {'count': 0})

    def __getBeltsData(self, aircraftID):
        return self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT][PLANE_KEYS.BELTS]

    def __setBeltsData(self, aircraftID, data):
        self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT][PLANE_KEYS.BELTS] = data

    def __setShellsData(self, aircraftID, data):
        self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT][PLANE_KEYS.SHELLS] = data

    def __getShellsData(self, planeID):
        return self._aircraftsData[planeID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT][PLANE_KEYS.SHELLS]

    def setShellsStoredCount(self, aircraftID, weaponSlotID, storedCount):
        self.getSlotShellsData(aircraftID, weaponSlotID)['storedCount'] = storedCount

    def getShellsCurrentCount(self, aircraftID, weaponSlotID):
        return int(self.getSlotShellsData(aircraftID, weaponSlotID).get('count', 0))

    def setPlaneEquipment(self, aircraftID, equipmentIDs):
        pdata = self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT]
        if pdata:
            pdata[PLANE_KEYS.EQUIPMENT] = equipmentIDs

    def getShellsStoredCount(self, aircraftID, weaponSlotID):
        return int(self.getSlotShellsData(aircraftID, weaponSlotID).get('storedCount', 0))

    def setShellsCount(self, planeID, weaponSlotID, count):
        self.getSlotShellsData(planeID, weaponSlotID)['count'] = count

    def setPlaneBelt(self, aircraftID, weaponSlotID, beltID, count):
        """
        
        @param aircraftID:
        @param weaponSlotID:
        @param beltID:
        @param count:
        """
        self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT][PLANE_KEYS.BELTS][weaponSlotID] = [beltID, count]

    def getPlaneBeltID(self, aircraftID, weaponSlotID):
        """
        Return installed belt id or None
        @param aircraftID:
        @param weaponSlotID:
        @return:
        """
        belt = self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT][PLANE_KEYS.BELTS].get(weaponSlotID, None)
        if belt is None:
            return
        else:
            return belt[0]

    def getPlaneBeltCount(self, aircraftID, weaponSlotID, default = 0):
        """
        Return installed belt count or default
        @param aircraftID:
        @param weaponSlotID:
        @param default:
        @return:
        """
        belt = self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT][PLANE_KEYS.BELTS].get(weaponSlotID, None)
        if belt is None:
            return default
        else:
            return belt[1]

    def getInstalledBeltCountByID(self, beltID):
        ret = 0
        for planeID in self.getBoughtAircraftsList():
            data = self.getAircraftPData(planeID)
            belts = data[PLANE_KEYS.BELTS] if data is not None else data
            if belts:
                ret += reduce(lambda acc, x: (acc + x[1] if x[0] == beltID else acc), belts.itervalues(), 0)

        return ret

    def getInstalledShellsCountByName(self, shellName):
        ret = 0
        for planeID in self.getBoughtAircraftsList():
            for slot in self.getInstalledWeapons(planeID):
                wInfo = db.DBLogic.g_instance.getWeaponInfo(planeID, *slot)
                if wInfo is not None:
                    if shellName == wInfo[1]:
                        ret += self.getShellsStoredCount(planeID, slot[0])

        return ret

    def getInstalledUpgradesCountByName(self, upgradeName):
        ret = 0
        for planeID in self.getBoughtAircraftsList():
            config = self.__getInstalledConfiguration(planeID)
            if upgradeName in config.modules:
                ret += 1

        return ret

    def getInstalledConsumablesCountByID(self, consumableID):
        ret = 0
        for planeID in self.getBoughtAircraftsList():
            ret += reduce(lambda acc, x: (acc + x['count'] if x['id'] == consumableID else acc), self.getConsumables(planeID), 0)

        return ret

    def getInstalledEquipmentCountByID(self, equipmentID):
        ret = 0
        for planeID in self.getBoughtAircraftsList():
            ret += reduce(lambda acc, x: (acc + 1 if x == equipmentID else acc), self.getEquipment(planeID), 0)

        return ret

    def hasPlaneMissingBelts(self, aircraftID):
        for slotID in self.getAircraftGunsSlots(aircraftID):
            beltID, count = self.getPlaneMissingBelt(aircraftID, slotID)
            if count > 0:
                return True

        return False

    def getPlaneMissingBelt(self, aircraftID, weaponSlotID):
        eType, wName, wCount = self.getInstalledWeaponInfo(aircraftID, weaponSlotID)
        return (self.getPlaneBeltID(aircraftID, weaponSlotID), wCount - self.getPlaneBeltCount(aircraftID, weaponSlotID))

    def __getPlaneBeltData(self, aircraftID, weaponSlotID):
        """
        @param aircraftID:
        @param weaponSlotID:
        @return:
        """
        return self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT][PLANE_KEYS.BELTS].get(weaponSlotID, None)

    def getCustomPresetGlobalID(self, aircraftID):
        return self.inventoryData[ISYNC_INVENTORY.CUSTOM_PRESETS].get(aircraftID, None)

    def __setInstalledGlobalID(self, aircraftID, globalID):
        self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT][PLANE_KEYS.INSTALLED_GLOBAL_ID] = globalID

    def __getInstalledConfiguration(self, aircraftID):
        globalID = self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT][PLANE_KEYS.INSTALLED_GLOBAL_ID]
        if globalID not in airplanesConfigurationsList[aircraftID]:
            globalID = airplanesDefaultConfigurations[aircraftID]
            LOG_ERROR('global aircraft ID is failed, replaced on default: aircraft name - ', aircraftID, globalID)
        return getAirplaneConfiguration(globalID)

    def getInstalledWeaponConfigurationBySlotID(self, planeID, slotID):
        return findIf(self.__getInstalledConfiguration(planeID).weaponSlots, lambda conf: conf[0] == slotID, None)

    def __getWeaponInfo(self, aircraftID, weaponSlotID, weaponConfigurationID = None):
        """
        Returns two values (<weapon type>, <weapon name>, <count>) or None if empty configuration
        NOTE: this function returns DEFAULT weapon count
        @param aircraftID:
        @param slotID:
        @param weaponConfigurationID:
        @return:
        """
        if weaponConfigurationID is None:
            weaponConfiguration = self.getInstalledWeaponConfigurationBySlotID(aircraftID, weaponSlotID)
            if weaponConfiguration is None:
                LOG_ERROR('Weapon slot type data not found (aircraftID, slotId, slotTypeId)', aircraftID, weaponSlotID, weaponConfigurationID)
                return
            weaponConfigurationID = weaponConfiguration[1]
        return self._db.getWeaponInfo(aircraftID, weaponSlotID, weaponConfigurationID)

    def _setAicraftsData(self, args):
        for resp_arr in args:
            for resp in resp_arr:
                planeID = resp[ISYNC_AIRCRAFT.AIRCRAFT_ID]
                self._aircraftsData[planeID] = resp
                self._onAicraftsDataUpdated(planeID)

    def _onAicraftsDataUpdated(self, planeID):
        """
        Addinional action on plane data updated
        @param planeID: id of updated plane
        @type planeID: int
        """
        pass

    def addRequiredUpgrades(self, upgDict):
        self.openUpgrades(upgDict['toResearch'])
        for upgName, upgCount in upgDict['toBuy'].items():
            self.addUpgradeToDepot(upgName, upgCount)

    def getInstalledWeaponInfo(self, aircraftID, slotID, slotConfigurationID = None):
        """
        Returns two values (<weapon type>, <weapon name>, <count>) or None if empty configuration or not slotID not installed
        NOTE: this function returns CURRENTLY INSTALLED weapon count
        @param aircraftID:
        @param slotID:
        @param slotConfigurationID:
        @return:
        """
        wInfo = self.__getWeaponInfo(aircraftID, slotID, slotConfigurationID)
        if wInfo is not None:
            if wInfo[0] == UPGRADE_TYPE.GUN:
                count = wInfo[2]
            else:
                count = self.getShellsCurrentCount(aircraftID, slotID)
            return (wInfo[0], wInfo[1], count)
        else:
            return

    def installAircraftConfiguration(self, globalID, fillShells = None):
        aircraftConfiguration = getAirplaneConfiguration(globalID)
        aircraftID = aircraftConfiguration.planeID
        upgrades, weaponConfig = aircraftConfiguration.modules, aircraftConfiguration.weaponSlots
        installedAircraftConfiguration = self.__getInstalledConfiguration(aircraftID)
        for uName in installedAircraftConfiguration.modules:
            self.addUpgradeToDepot(uName)

        for w in installedAircraftConfiguration.weaponSlots:
            info = self.getInstalledWeaponInfo(aircraftID, w[0], w[1])
            if info is not None:
                self.addUpgradeToDepot(info[1], info[2])
            beltData = self.__getPlaneBeltData(aircraftID, w[0])
            if beltData is not None:
                self.addBeltsToDepot(*beltData)

        for upg in upgrades:
            self.removeUpgradeFromDepot(upg)

        oldBeltsData = self.__getBeltsData(aircraftID)
        self.__setBeltsData(aircraftID, {})
        self.__setShellsData(aircraftID, {})
        for slotID, slotConfID in weaponConfig:
            weapon = self._db.getWeaponInfo(aircraftID, slotID, slotConfID)
            if weapon is None:
                continue
            wType, wName, wCount = weapon
            if wType == UPGRADE_TYPE.GUN:
                self.removeUpgradeFromDepot(wName, wCount)
                gun = db.DBLogic.g_instance.getComponentByName(consts.COMPONENT_TYPE.GUNS, wName)
                beltID = gun.defaultBelt
                oldBeltData = oldBeltsData.get(slotID, None)
                if oldBeltData and oldBeltData[0] in gun.compatibleBeltIDs:
                    beltID = oldBeltData[0]
                if self.getAmmoBeltCount(beltID) >= wCount:
                    self.removeBeltsFromDepot(beltID, wCount)
                    self.setPlaneBelt(aircraftID, slotID, beltID, wCount)
                else:
                    self.setPlaneBelt(aircraftID, slotID, gun.defaultBelt, wCount)
            elif wType == UPGRADE_TYPE.ROCKET or wType == UPGRADE_TYPE.BOMB:
                if fillShells is not None:
                    if wName not in fillShells:
                        depotCount = self.getUpgradeCountInDepot(wName)
                        if depotCount < wCount:
                            wCount = depotCount
                self.removeUpgradeFromDepot(wName, wCount)
                self.addSlotShellsData(aircraftID, slotID, wCount, wCount)

        slotsByWeaponNames = {}
        oldSlotConfigs = dict(installedAircraftConfiguration.weaponSlots)
        newSlotConfigs = dict(aircraftConfiguration.weaponSlots)
        oldConfigGunsCount, newConfigGunsCount = Counter(), Counter()
        for slotID in newSlotConfigs:
            oldWInfo = self._db.getWeaponInfo(aircraftID, slotID, oldSlotConfigs[slotID])
            if oldWInfo:
                wType, wName, wCount = oldWInfo
                if wType == UPGRADE_TYPE.GUN:
                    oldConfigGunsCount[wName] += wCount
            newWInfo = self._db.getWeaponInfo(aircraftID, slotID, newSlotConfigs[slotID])
            if newWInfo:
                wType, wName, wCount = newWInfo
                if wType == UPGRADE_TYPE.GUN:
                    newConfigGunsCount[wName] += wCount
                    slotsByWeaponNames.setdefault(wName, []).append(slotID)

        rechargedWeapons = set()
        for wName, wCount in newConfigGunsCount.iteritems():
            if oldConfigGunsCount[wName] != wCount:
                weapon = self._db.getComponentByName(COMPONENT_TYPE.GUNS, wName)
                for slotID in slotsByWeaponNames[wName]:
                    beltID, count = self.__getPlaneBeltData(aircraftID, slotID)
                    if beltID != weapon.defaultBelt:
                        self.addBeltsToDepot(beltID, count)
                        _, _, countInSlot = self._db.getWeaponInfo(aircraftID, slotID, newSlotConfigs[slotID])
                        self.setPlaneBelt(aircraftID, slotID, weapon.defaultBelt, countInSlot)
                        rechargedWeapons.add(wName)

        LOG_DEBUG('Weapons recharged: {0}'.format(rechargedWeapons))
        self.__setInstalledGlobalID(aircraftID, globalID)
        rechargedWeapons = rechargedWeapons if any((oldConfigGunsCount[w] for w in rechargedWeapons)) else None
        return rechargedWeapons

    def openAircraft(self, aircraftID, onlyDefault = True):
        if not self.isAircraftOpened(aircraftID):
            self.inventoryData[ISYNC_INVENTORY.OPENED_AIRCRAFTS_LIST].append(aircraftID)
        upgrades = self._db.getUpgradesNamesByGlobalID(airplanesDefaultConfigurations[aircraftID])
        aircraftName = self._db.getAircraftName(aircraftID)
        for u in self._db.getAircraftUpgradesFromName(aircraftName)[0]:
            if u.name not in upgrades:
                variant = findIf(u.variant, lambda v: v.aircraftName == aircraftName)
                upgradeUnlockCost = variant.parentUpgrade[0].experience
                if not variant.parentUpgrade or upgradeUnlockCost == 0 or not onlyDefault:
                    upgrades.add(u.name)

        self.openUpgrades(upgrades)
        return upgrades

    def openUpgrades(self, upgradeNamesList):
        self.inventoryData[ISYNC_INVENTORY.DEPOT_UPGRADES_DICT].update(((name, 0) for name in upgradeNamesList if name not in self.inventoryData[ISYNC_INVENTORY.DEPOT_UPGRADES_DICT]))

    def getInstalledUpgradesGlobalID(self, planeID):
        """
        @param planeID:
        @return:
        """
        if planeID:
            return self._aircraftsData[planeID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT][PLANE_KEYS.INSTALLED_GLOBAL_ID]
        else:
            return None

    def getRequiredPressetResources(self, aircraftID, upgradeNames, weaponConfig):
        aircraftName = self._db.getAircraftData(aircraftID).airplane.name
        upgrades = [ self._db.upgrades.get(upgradeName, None) for upgradeName in upgradeNames ]
        if not self._db.isUpgradesValid(aircraftName, upgrades):
            LOG_ERROR('getRequiredPresetResources. Upgrades is invalid', upgradeNames)
            return
        else:
            upgDict = self.getPresetRequiredUpgrades(aircraftID, upgradeNames, weaponConfig)
            neededResources = self.calculateRequiredResourcesForUpgradePresset(aircraftID, upgDict['toResearch'], upgDict['toBuy'])
            return neededResources

    def getPresetData(self, aircraftID, presetName):
        """
        Returns two values: (<list of modules names>, <list of tuples of type (<slotID>, <slotConfigurationID>)>)
        @param aircraftID:
        @param presetName:
        @return:
        """
        if presetName == CUSTOM_PRESET_NAME:
            return self.getCustomPreset(aircraftID)
        else:
            config = airplanesConfigurations.get(self._db.getGlobalIDByPreset(aircraftID, presetName), None)
            return (config.modules, config.weaponSlots)
            return

    def getCustomPreset(self, aircraftID):
        config = airplanesConfigurations.get(self.getCustomPresetGlobalID(aircraftID), None)
        if config is None:
            return
        else:
            return (config.modules, config.weaponSlots)

    def getAircraftExp(self, aircraftID):
        return self.aircraftsData[aircraftID][ISYNC_AIRCRAFT.EXPERIENCE]

    def setAircraftExp(self, aircraftID, exp):
        self.aircraftsData[aircraftID][ISYNC_AIRCRAFT.EXPERIENCE] = exp

    def getFreeExp(self):
        return self._stats[ISYNC_STATS.EXPERIENCE]

    def getSlotCount(self):
        return self._stats[ISYNC_STATS.SLOTS_COUNT]

    def getCurrentAircraftID(self):
        return self.getAircraftIDBySlotIndex(self._stats[ISYNC_STATS.SELECTED_AIRCRAFT])

    def setCurrentAircraftID(self, aircraftID):
        self._stats[ISYNC_STATS.SELECTED_AIRCRAFT] = self.getAircraftSlotIndexById(aircraftID)

    def getCreatedAt(self):
        return self._stats[ISYNC_STATS.CREATED_AT]

    def getLastGameTime(self, airPlaneID, default = -1):
        """
        @param airPlaneID: plane id or -1 for account last game time
        @param default:
        @return:
        @rtype:
        """
        if airPlaneID == -1:
            lgt = -1
            for k in self._aircraftsData.keys():
                tmp = self.getLastGameTime(k)
                if tmp > lgt:
                    lgt = tmp

            return lgt
        pd = self._aircraftsData.get(airPlaneID, None)
        if pd is None:
            return default
        planeData = pd.get(ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT, None)
        if planeData is None:
            return default
        else:
            return planeData[PLANE_KEYS.LAST_GAME_TIME]

    def setCustomPreset(self, aircraftID, globalID):
        """
        @param aircraftID:
        @param globalID: (<list of upgrades names>, <list of tuples of type (slotId, slotConfigurationId)>)
        @return:
        """
        self.inventoryData[ISYNC_INVENTORY.CUSTOM_PRESETS][aircraftID] = globalID

    def clearOpenedAircrafts(self):
        while len(self.inventoryData[ISYNC_INVENTORY.OPENED_AIRCRAFTS_LIST]) > 0:
            del self.inventoryData[ISYNC_INVENTORY.OPENED_AIRCRAFTS_LIST][0]

    def clearOpenedUpgrades(self):
        self.inventoryData[ISYNC_INVENTORY.DEPOT_UPGRADES_DICT].clear()

    def isAircraftOpened(self, aircraftID):
        return aircraftID in self.inventoryData[ISYNC_INVENTORY.OPENED_AIRCRAFTS_LIST]

    def isPlaneResearchAvailableOpened(self, planeID):
        parentIDs = self._db.getPlaneParentPlaneID(planeID)
        return not parentIDs or any((self.isAircraftOpened(parentID) for parentID in parentIDs))

    def isUpgradeOpened(self, upgradeName):
        return upgradeName in self.inventoryData[ISYNC_INVENTORY.DEPOT_UPGRADES_DICT]

    def isUpgradeInstalled(self, aircraftID, upgradeName):
        if not self.aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT]:
            return False
        return upgradeName in self._db.selectUpgradesNamesByGlobalID(self.getInstalledUpgradesGlobalID(aircraftID))

    def isWeaponConfigurationInstalled(self, aircraftID, weaponSlotID, weaponConfigurationID):
        return (weaponSlotID, weaponConfigurationID) in self.__getInstalledConfiguration(aircraftID).weaponSlots

    def getUpgradeCountInDepot(self, upgradeName):
        return self.inventoryData[ISYNC_INVENTORY.DEPOT_UPGRADES_DICT].get(upgradeName, 0)

    def addUpgradeToDepot(self, upgradeName, count = 1):
        dep = self.inventoryData[ISYNC_INVENTORY.DEPOT_UPGRADES_DICT]
        dep[upgradeName] = dep.get(upgradeName, 0) + count

    def removeUpgradeFromDepot(self, upgradeName, count = 1):
        dep = self.inventoryData[ISYNC_INVENTORY.DEPOT_UPGRADES_DICT]
        dep[upgradeName] = dep[upgradeName] - count

    def isUpgradeBought(self, upgName):
        if self.getUpgradeCount(upgName) > 0:
            return True
        for aircraft in self._aircraftsData.itervalues():
            if aircraft[ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT]:
                if upgName in self._db.selectUpgradesNamesByGlobalID(aircraft[ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT][PLANE_KEYS.INSTALLED_GLOBAL_ID]):
                    return True

        return False

    def getUpgradeCount(self, upgradeName):
        if self.isUpgradeOpened(upgradeName):
            return self.inventoryData[ISYNC_INVENTORY.DEPOT_UPGRADES_DICT][upgradeName]
        return -1

    def getBoughtUpgradeIDs(self):
        return (x.id for x in db.DBLogic.g_instance.upgrades.itervalues() if x.type not in UPGRADE_TYPE.SHELL and self.getUpgradeCount(x.name) > 0)

    def getBoughtUpgrades(self):
        return (x for x in db.DBLogic.g_instance.upgrades.itervalues() if x.type not in UPGRADE_TYPE.SHELL and self.getUpgradeCount(x.name) > 0)

    def setUpgradeCount(self, upgradeName, count):
        self.inventoryData[ISYNC_INVENTORY.DEPOT_UPGRADES_DICT][upgradeName] = count

    def isIntalledRequiredUpgrades(self, aircraftID, upgrade):
        upgradeVariant = next(iter(filter(lambda var: var.aircraftName == self._db.getAircraftData(aircraftID).airplane.name, upgrade.variant)), None)
        if hasattr(upgradeVariant, 'requiredUpgrades') and len(upgradeVariant.requiredUpgrades) > 0:
            for upgradeName in upgradeVariant.requiredUpgrades:
                if self.isUpgradeInstalled(aircraftID, upgradeName):
                    return True

            return False
        else:
            return True

    def isAircraftElite(self, planeID):
        return self._db.isPlanePremium(planeID) or planeID in self._elitePlaneList

    def getInstalledUpgrades(self, aircraftID):
        return self.__getInstalledConfiguration(aircraftID).modules

    def getInstalledWeapons(self, aircraftID):
        return self.__getInstalledConfiguration(aircraftID).weaponSlots

    def getInstalledPreset(self, aircraftID):
        pdata = self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT]
        if pdata:
            return self._db.getPresetNameByGlobalID(self.getInstalledUpgradesGlobalID(aircraftID))
        else:
            return None

    def getInstalledCamouflages(self, aircraftID):
        return self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.CAMOUFLAGES_DICT]

    def getCamouflageNationDecalID(self, camouflageID):
        """
        Return custom nation decalID for specified camouflage.
        @type camouflageID: int
        @rtype: int
        """
        camouflage = _camouflages_data.getCamouflage(camouflageID)
        if not camouflage:
            return NATION_DECAL_ID_DEFAULT
        return camouflage.nationDecalID

    def isPrimary(self, aircraftID):
        pdata = self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT]
        if pdata:
            return pdata[PLANE_KEYS.IS_PRIMARY]
        else:
            return None

    def setPrimary(self, aircraftID, isPrimary):
        pdata = self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT]
        pdata[PLANE_KEYS.IS_PRIMARY] = isPrimary

    def dailyFirstWinXPFactor(self, aircraftID):
        return self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.DAILY_FIRST_WIN_XP_FACTOR]

    def dailyFirstWinRemains(self, aircraftID):
        return self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.DAILY_FIRST_WIN_REMAINS]

    def getAvailableUpgrades(self):
        return self._inventoryData[ISYNC_INVENTORY.DEPOT_UPGRADES_DICT]

    def getAircraftSlotIndexById(self, aircraftID):
        l = self._inventoryData[ISYNC_INVENTORY.BOUGHT_AIRCRAFTS_LIST]
        if aircraftID in l:
            return l.index(aircraftID)
        else:
            return None

    def getAircraftIDBySlotIndex(self, slotIndex):
        l = self._inventoryData[ISYNC_INVENTORY.BOUGHT_AIRCRAFTS_LIST]
        if slotIndex is not None and slotIndex >= 0 and slotIndex < len(l):
            return l[slotIndex]
        else:
            return

    def getBoughtAircraftsList(self):
        """
        List of bought planes ids
        @rtype: list
        """
        return self._inventoryData[ISYNC_INVENTORY.BOUGHT_AIRCRAFTS_LIST]

    def openedAircrafts(self):
        return self._inventoryData[ISYNC_INVENTORY.OPENED_AIRCRAFTS_LIST]

    def inBattlePlaneList(self):
        return self._inventoryData[ISYNC_INVENTORY.BATTLE_AIRCRAFTS_LIST]

    def getUnlockPlanes(self):
        return self._inventoryData[ISYNC_INVENTORY.UNLOCK_AIRCRAFTS]

    def addPlaneToUnlocks(self, aircraftID):
        self._inventoryData[ISYNC_INVENTORY.UNLOCK_AIRCRAFTS][aircraftID] = None
        if aircraftID in self.inBattlePlaneList():
            self._inventoryData[ISYNC_INVENTORY.BATTLE_AIRCRAFTS_LIST].remove(aircraftID)
        return

    def removePlaneFromUnlocks(self, aircraftID):
        del self._inventoryData[ISYNC_INVENTORY.UNLOCK_AIRCRAFTS][aircraftID]

    def isAircraftBought(self, aircraftID):
        return aircraftID in self.inventoryData[ISYNC_INVENTORY.BOUGHT_AIRCRAFTS_LIST]

    def __getPresetStatus(self, aircraftID, moduleNames, weapons):
        upgDict = self.getPresetRequiredUpgrades(aircraftID, moduleNames, weapons)
        neededResources = self.calculateRequiredResourcesForUpgradePresset(aircraftID, upgDict['toResearch'], upgDict['toBuy'])
        if not any(neededResources.values()):
            return Inventory.PRESET_STATUS_BOUGHT
        if neededResources['exp'] < 1 and self.isAircraftOpened(aircraftID):
            return Inventory.PRESET_STATUS_RESEARCHED
        return Inventory.PRESET_STATUS_NONE

    def getConfigurationRequiredUpgrades(self, globalID):
        """
        Return aircrafts configuration required upgrades as dict {'toResearch': <list of names>, 'toBuy': <list of names>}
        @param globalID:
        @return:
        """
        aircraftConfig = getAirplaneConfiguration(globalID)
        return self.getPresetRequiredUpgrades(aircraftConfig.planeID, aircraftConfig.modules, aircraftConfig.weaponSlots)

    def getPresetRequiredUpgrades(self, aircraftID, upgradeNames, weaponSlots, targetConfig = None):
        """
        Return aircrafts configuration required upgrades as dict {'toResearch': <list of names>, 'toBuy': <list of names>}
        @param aircraftID:
        @param upgradeNames:
        @param weaponSlots:
        @return:
        """
        aircraftName = self._db.getAircraftData(aircraftID).airplane.name
        requiredUpgrades = dict([ (m, 1) for m in upgradeNames ])
        for slotConfiguration in weaponSlots:
            weapon = self._db.getWeaponInfo(aircraftID, slotConfiguration[0], slotConfiguration[1])
            if weapon is not None:
                requiredUpgrades[weapon[1]] = requiredUpgrades.get(weapon[1], 0) + weapon[2]

        invUpgrades = deepcopy(self.inventoryData[ISYNC_INVENTORY.DEPOT_UPGRADES_DICT])
        if self.aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT]:
            installedConfiguration = self.__getInstalledConfiguration(aircraftID)
            for slotID in xrange(len(installedConfiguration.weaponSlots)):
                slotConfig = installedConfiguration.weaponSlots[slotID]
                wInfo = self.getInstalledWeaponInfo(aircraftID, slotConfig[0], slotConfig[1])
                if wInfo is not None:
                    changeInv = True
                    if targetConfig is not None:
                        targetSlotConfig = targetConfig.weaponSlots[slotID]
                        if targetSlotConfig == slotConfig:
                            upgrade = db.DBLogic.g_instance.upgrades[wInfo[1]]
                            if upgrade.type in UPGRADE_TYPE.SHELL:
                                invUpgrades[wInfo[1]] = invUpgrades.get(wInfo[1], 0) + requiredUpgrades[wInfo[1]]
                                changeInv = False
                    if changeInv:
                        invUpgrades[wInfo[1]] = invUpgrades.get(wInfo[1], 0) + wInfo[2]

            for moduleName in installedConfiguration.modules:
                invUpgrades[moduleName] = invUpgrades.get(moduleName, 0) + 1

        toResearch = filter(lambda k: k not in invUpgrades, requiredUpgrades)
        for upgName in toResearch:
            upgrade = self._db.upgrades.get(upgName, None)
            if upgrade:
                self.__addUpgradeParentToResearch(aircraftName, invUpgrades, upgrade, toResearch)

        toBuy = dict(filter(lambda tp: tp[1] > 0, map(lambda k: (k, requiredUpgrades[k] - invUpgrades[k]), filter(lambda k: k in invUpgrades, requiredUpgrades))))
        toBuy.update(dict(map(lambda k: (k, requiredUpgrades[k] if k in requiredUpgrades else 0), toResearch)))
        return {'toResearch': toResearch,
         'toBuy': toBuy}

    def getMissingShells(self, aircraftID, weaponSlotID, slotData = None):
        """
        Get shellID and it count to refill player required amount for some slot
        @param aircraftID:
        @param weaponSlotID:
        @param slotData:
        @return:
        """
        wData = self.getSlotShellsData(aircraftID, weaponSlotID)
        if wData is not None:
            weaponType, weaponName, weaponCount = self.__getWeaponInfo(aircraftID, weaponSlotID)
            if weaponType == UPGRADE_TYPE.ROCKET or weaponType == UPGRADE_TYPE.BOMB:
                slotData = slotData if slotData is not None else wData.get('storedCount', weaponCount)
                upgName = self.__getInstalledWeaponUpgradeName(aircraftID, weaponSlotID)
                diffCount = slotData - wData['count']
                depotCount = self.getUpgradeCount(upgName)
                toBuyCount = diffCount - depotCount
                return (upgName, toBuyCount, diffCount)
        return (None, None, None)

    def isParentOpened(self, planeID):
        planeData = self._db.getAircraftData(planeID)
        if planeData.airplane.options.hidePlaneResearch:
            return True
        upgrade = self._db.getUpgradeByAircraftID(planeID)
        if upgrade is None:
            return False
        elif all(map(lambda var: not self.isAircraftOpened(self._db.getAircraftIDbyName(var.aircraftName)), upgrade.variant)):
            return False
        else:
            return True

    def getChildPlanes(self, planeID):
        ret = []
        planeData = self._db.getAircraftData(planeID)
        if planeData.airplane.options.hidePlaneResearch:
            return ret
        else:
            planeUpgrade = self._db.getUpgradeByAircraftID(planeID)
            if planeUpgrade is None:
                return ret
            for upgrade in self._db.upgrades.values():
                if upgrade.type != UPGRADE_TYPE.AIRCRAFT:
                    continue
                if filter(lambda x: planeUpgrade.name == x.aircraftName, upgrade.variant):
                    ret.append(self._db.getAircraftIDbyName(upgrade.name))

            return ret

    def calculateRequiredResourcesForUpgradePresset(self, aircraftID, toResearch, toBuy):
        """
        @param aircraftID: aircraft id
        @param toResearch:
        @param toBuy:
        @return: (requiredMoney, requiredExp) for this configuration
        """
        neededResources = {'credits': 0,
         'gold': 0,
         'exp': 0}
        aircraftName = self._db.getAircraftData(aircraftID).airplane.name
        if toResearch:
            for upgName in toResearch:
                upgrade = self._db.upgrades.get(upgName, None)
                if upgrade is not None:
                    upgradeVariant = filter(lambda var: var.aircraftName == aircraftName, upgrade.variant)[0]
                    exp = upgradeVariant.parentUpgrade[0].experience
                    if upgName in neededResources:
                        neededResources[upgName]['exp'] = neededResources[upgName].get('exp', 0) + exp
                    else:
                        neededResources[upgName] = {'exp': exp}
                    neededResources['exp'] += exp

        if toBuy:
            for upgName in toBuy:
                upgrade = self._db.upgrades.get(upgName, None)
                if upgrade is not None:
                    cred = getattr(upgrade, 'credits', 0) * toBuy[upgName]
                    gold = getattr(upgrade, 'gold', 0) * toBuy[upgName]
                    if upgName in neededResources:
                        neededResources[upgName]['credits'] = neededResources[upgName].get('credits', 0) + cred
                        neededResources[upgName]['gold'] = neededResources[upgName].get('gold', 0) + gold
                    else:
                        neededResources[upgName] = {'credits': cred,
                         'gold': gold}
                    neededResources['credits'] += cred
                    neededResources['gold'] += gold

        return neededResources

    def calculateRequiredUpgradesForAircraft(self, aircraftID, parentPlaneID = None, onlyResearched = True):
        """
        @param aircraftID:
        @return:
        """
        aircraftName = self._db.getAircraftName(aircraftID)
        aircraftUpgrade = self._db.upgrades.get(aircraftName, None)
        if aircraftUpgrade is None:
            LOG_ERROR('Upgrade for aircraft {0} not found'.format(aircraftName))
            return
        else:

            def calculateRequiredVairantUpgrades(variant):
                parentPlaneName = variant.aircraftName
                toResearch = []
                parentPlaneID = self._db.getAircraftIDbyName(parentPlaneName)
                res = (parentPlaneID, toResearch, self.isAircraftOpened(self._db.getAircraftIDbyName(parentPlaneName)))
                parentName = variant.parentUpgrade[0].name
                counter = MAX_PARENT_UPGRADES_CHECK_DEPTH
                while parentName and counter > 0:
                    counter -= 1
                    if not self.isUpgradeOpened(parentName):
                        toResearch.append(parentName)
                    parentUpgrade = self._db.upgrades.get(parentName, None)
                    if parentUpgrade is None:
                        DBLOG_ERROR('Cannot find parent upgrade {0} of upgrade {1} in db'.format(parentName, aircraftUpgrade.name))
                        return res
                    pi = findIf(parentUpgrade.variant, lambda item: item.aircraftName == parentPlaneName)
                    parentName = None if pi is None else pi.parentUpgrade[0].name

                if counter == 0:
                    DBLOG_ERROR('Seems that parents of upgrade {0} have recursive dependencies'.format(aircraftUpgrade.name))
                return res

            def getRequiredUpgradesMinPrice(calculatedRequiredUpgrades):
                """
                Function to determine parent's plane will researching from
                :param calculatedRequiredUpgrades:
                """

                def getResearchExp(parentID, toResearch):
                    res = self.calculateRequiredResourcesForUpgradePresset(parentID, toResearch, [])
                    res['exp'] += self.getParentPlaneVariant(aircraftID, parentID).parentUpgrade[0].experience
                    return res['exp']

                def minExp(iterable):
                    d = min(iterable, key=lambda it: it['researchExp'])
                    return (d['parentID'], d['toResearch'])

                parentInfo = [ dict(parentID=parentID, isParentResearched=isParentResearched, researchExp=getResearchExp(parentID, toResearch), toResearch=toResearch) for parentID, toResearch, isParentResearched in calculatedRequiredUpgrades ]
                parentResearched = [ d for d in parentInfo if d['isParentResearched'] ]
                if parentResearched:
                    parentEnoughExp = [ d for d in parentResearched if d['researchExp'] <= self.getAircraftExp(d['parentID']) + self.getFreeExp() ]
                    parentCount = len(parentEnoughExp)
                    if parentCount > 1:
                        enoughParentExp = [ d for d in parentResearched if d['researchExp'] <= self.getAircraftExp(d['parentID']) ]
                        if len(enoughParentExp) >= 1:
                            return minExp(enoughParentExp)
                        return minExp([min(parentEnoughExp, key=lambda it: it['researchExp'] - self.getAircraftExp(it['parentID']))])
                    if parentCount == 1:
                        return minExp(parentEnoughExp)
                    if parentCount == 0:
                        return minExp(parentResearched)
                return minExp(parentInfo)

            variants = aircraftUpgrade.variant if parentPlaneID is None else [ item for item in aircraftUpgrade.variant if item.aircraftName == self._db.getAircraftName(parentPlaneID) ]
            return (calculateRequiredVairantUpgrades(variant) for variant in variants)

    def calculateRequiredUpgradesForUpgrade(self, upgrade, upgradeVariant):
        """
        Returns upgrades that should be research to be able to research the given.
        NOTE: check that aircraft is already researched before
        @param upgrade: upgrade that should be researched
        @param upgradeVariant: corresponding upgrade variant
        @return: upgrades names list
        """
        toResearch = []
        aircraftName = upgradeVariant.aircraftName
        defaultUpgrades = self._db.getAircraftUpgradesFromName(aircraftName, True)
        while upgrade is not None:
            if not self.isUpgradeOpened(upgrade.name):
                toResearch.append(upgrade.name)
            if not findIf(defaultUpgrades, lambda du: du.name == upgrade.name) and upgradeVariant.parentUpgrade[0].name:
                parentUpgrade = self._db.upgrades.get(upgradeVariant.parentUpgrade[0].name, None)
                if parentUpgrade is None:
                    DBLOG_ERROR('Cannot find parent upgrade {0} in db'.format(upgradeVariant.parentUpgrade[0].name))
                parentVariant = findIf(parentUpgrade.variant, lambda item: item.aircraftName == aircraftName)
                if parentVariant is None:
                    DBLOG_ERROR('Parent upgrade {0} of upgrade {1} in does not contain variant for aircraft {2}'.format(parentUpgrade.name, upgrade.name, aircraftName))
                upgrade = parentUpgrade
                upgradeVariant = parentVariant
            else:
                upgrade = None

        return toResearch

    def getAircraftsDataByNationID(self, nationID):
        aircraftMap = self._db.getAircraftList(nationID)
        aircraftClientDataList = []
        for aircraftID in aircraftMap.keys():
            if aircraftID is None:
                LOG_ERROR('Found aircraft with ID == None. Check aircrafts list of nationID {0}'.format(nationID))
            if not self._db.isPlaneExclusive(aircraftID) and not self._db.isPlaneNPC(aircraftID):
                aircraftClientDataList.append(self.getAircraftClientDataMap(aircraftID))

        return aircraftClientDataList

    def getParentAicraftID(self, aircraftID):
        upgrade = self._db.getUpgradeByAircraftID(aircraftID)
        if upgrade is None:
            return
        else:
            upgradeVariant = filter(lambda u: u.aircraftName, upgrade.variant)
            if upgradeVariant:
                return [ self._db.getAircraftIDbyName(u.aircraftName) for u in upgradeVariant ]
            return

    def getParentPlaneVariant(self, planeID, parentPlaneID):
        upgrade = self._db.getUpgradeByAircraftID(planeID)
        parentPlaneName = self._db.getAircraftName(parentPlaneID)
        variant = findIf(upgrade.variant, lambda var: var.aircraftName == parentPlaneName)
        return variant

    def getAircraftClientDataMap(self, planeID, parentAircraftName = None):
        upgrade = self._db.getUpgradeByAircraftID(planeID)
        isAircraftOpened = self.isAircraftOpened(planeID)
        requiredExperience = dict()
        requiredExperiencePlane = dict()
        parentPlaneID = 0
        if upgrade is None:
            isResearchedAvailable = False
            parentNames = []
            parentAircraftNames = []
        else:
            isResearchedAvailable = self.isPlaneResearchAvailableOpened(planeID)
            for _parentPlaneID, toResearch, _ in self.calculateRequiredUpgradesForAircraft(planeID, onlyResearched=False):
                neededResources = self.calculateRequiredResourcesForUpgradePresset(_parentPlaneID, toResearch, [])
                parentVariant = self.getParentPlaneVariant(planeID, _parentPlaneID)
                requiredExperience[_parentPlaneID] = parentVariant.parentUpgrade[0].experience + neededResources['exp']
                requiredExperiencePlane[_parentPlaneID] = parentVariant.parentUpgrade[0].experience

            parentNames = [ variant.parentUpgrade[0].name for variant in upgrade.variant ]
            parentAircraftNames = [ variant.aircraftName for variant in upgrade.variant ]
        blockType = BLOCK_TYPE.UNLOCKED
        isBought = self.isAircraftBought(planeID)
        if isBought:
            blockType = self.aircraftsData[planeID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT][PLANE_KEYS.BLOCK_TYPE]
        price = self.getAircraftPrice(planeID)
        aicraftClientDataMap = {'id': planeID,
         'isResearched': isAircraftOpened,
         'isResearchAvailable': isResearchedAvailable,
         'isBought': isBought,
         'isPremium': db.DBLogic.g_instance.isPlanePremium(planeID),
         'isElite': self.isAircraftElite(planeID),
         'reqiuredExperience': requiredExperience,
         'reqiuredExperiencePlane': requiredExperiencePlane,
         'gotExperience': self.getAircraftExp(planeID),
         'researchedParentID': parentPlaneID,
         'priceCredits': price[0],
         'parent': parentNames,
         'parentAircraft': parentAircraftNames,
         'priceGold': price[1],
         'blockType': blockType,
         'sellPrice': self.__getAircraftSellPrice(planeID) if isBought else -1}
        return aicraftClientDataMap

    def __addUpgradeParentToResearch(self, aircraftName, invUpgrades, upgrade, whereToAdd):
        upgradeVariants = filter(lambda var: var.aircraftName == aircraftName, upgrade.variant)
        if len(upgradeVariants) == 0:
            LOG_ERROR("Upgrade's variant not found for upgrade %s" % upgrade.name)
            return
        else:
            upgradeVariant = upgradeVariants[0]
            parentName = upgradeVariant.parentUpgrade[0].name
            if parentName != '':
                if parentName not in invUpgrades and parentName not in whereToAdd:
                    whereToAdd.append(parentName)
                upgrade = self._db.upgrades.get(parentName, None)
                if upgrade is None:
                    LOG_ERROR('Attempt to add not existing upgrade ', parentName)
                    return
                self.__addUpgradeParentToResearch(aircraftName, invUpgrades, upgrade, whereToAdd)
            return

    def getAircraftUpgradesData(self, aircraftID):
        aircraftUpgrades, aircrafts = self._db.getAircraftUpgrades(aircraftID)
        return [ self.getUpgradeInfoMap(aircraftID, upgrade) for upgrade in aircraftUpgrades ]

    def getAircraftData(self, aircraftID):
        aircraftName = self._db.getAircraftData(aircraftID).airplane.name
        upgradeAircraftsInfoList = []
        aircraftUpgrades, aircrafts = self._db.getAircraftUpgrades(aircraftID)
        for upgrade in aircrafts:
            childAircraftID = self._db.getAircraftIDbyName(upgrade.name)
            if childAircraftID is None:
                LOG_ERROR("Invalid aircraft's name %s in Upgrades.xml" % upgrade.name)
                continue
            upgradeAircraftsInfoList.append(self.getAircraftClientDataMap(childAircraftID, aircraftName))

        currentAircraftData = self.getAircraftClientDataMap(aircraftID)
        upgradeAircraftsInfoList.append(currentAircraftData)
        if currentAircraftData['parentAircraft'] != '':
            parentAircraftId = self._db.getAircraftIDbyName(currentAircraftData['parentAircraft'])
            upgradeAircraftsInfoList.append(self.getAircraftClientDataMap(parentAircraftId))
        return upgradeAircraftsInfoList

    def getAvailablePresets(self, aircraftID, getResearchedOnly = False):
        presetAvailableList = []
        presetsList = self._db.getAircraftPresetsListByID(aircraftID)
        for p in presetsList:
            configuration = airplanesConfigurations.get(self._db.getGlobalIDByPreset(aircraftID, p.name), None)
            if configuration is None:
                CRITICAL_ERROR('Invalid preset found. aircraftID = {0}, presetName = {1}'.format(aircraftID, p.name))
            status = self.__getPresetStatus(aircraftID, configuration.modules, configuration.weaponSlots)
            if getResearchedOnly and status == Inventory.PRESET_STATUS_RESEARCHED or status == Inventory.PRESET_STATUS_BOUGHT:
                presetAvailableList.append(p.name)

        configuration = airplanesConfigurations.get(self.getCustomPresetGlobalID(aircraftID), None)
        if configuration:
            status = self.__getPresetStatus(aircraftID, configuration.modules, configuration.weaponSlots)
            if getResearchedOnly and status == Inventory.PRESET_STATUS_RESEARCHED or status == Inventory.PRESET_STATUS_BOUGHT:
                presetAvailableList.append(CUSTOM_PRESET_NAME)
        return presetAvailableList

    def getSlotsConfiguration(self, aircraftID):
        """
        Returns weapon slots configuration
        @param aircraftID:
        @return: [(<slotID>, slotConfigurationID), ...]
        """
        if self.aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT] is None:
            return []
        else:
            return self.__getInstalledConfiguration(aircraftID).weaponSlots

    def getAircraftSlotsBattleData(self, aircraftID):
        shells = []
        guns = {}
        for slotID, configurationID in self.__getInstalledConfiguration(aircraftID).weaponSlots:
            weaponInfo = self.getInstalledWeaponInfo(aircraftID, slotID, configurationID)
            if weaponInfo is not None:
                if weaponInfo[0] in (UPGRADE_TYPE.BOMB, UPGRADE_TYPE.ROCKET):
                    shells.append({'key': slotID,
                     'value': weaponInfo[2]})
                else:
                    guns[weaponInfo[1]] = self.getPlaneBeltID(aircraftID, slotID)

        return (shells, guns)

    def shellSlotsGenerator(self, aircraftID):
        for slotID, configurationID in self.__getInstalledConfiguration(aircraftID).weaponSlots:
            weaponType = self.getInstalledWeaponsType(aircraftID, slotID)
            if weaponType in (UPGRADE_TYPE.BOMB, UPGRADE_TYPE.ROCKET):
                yield slotID

    def getAircraftGunsSlots(self, aircraftID):
        for slotID, configurationID in self.__getInstalledConfiguration(aircraftID).weaponSlots:
            if self.getInstalledWeaponsType(aircraftID, slotID) == UPGRADE_TYPE.GUN:
                yield slotID

    def getAircraftShellsPresent(self, aircraftID):
        for globalID in airplanesConfigurationsList[aircraftID]:
            airCraftConfiguration = getAirplaneConfiguration(globalID)
            for slotID, configurationID in airCraftConfiguration.weaponSlots:
                weaponType = self.getInstalledWeaponsType(aircraftID, slotID, configurationID)
                if weaponType == UPGRADE_TYPE.BOMB:
                    return True
                if weaponType == UPGRADE_TYPE.ROCKET:
                    return True

        return False

    def getInstalledWeaponsType(self, aircraftID, weaponSlotID, weaponConfigurationID = None):
        """
        Return configurations type. Should be one of consts.UPGRADE_TYPE.WEAPON type
        """
        wInfo = self.__getWeaponInfo(aircraftID, weaponSlotID, weaponConfigurationID)
        if wInfo is None:
            return
        else:
            return wInfo[0]

    def getInstalledWeaponCount(self, aircraftID, weaponSlotID, weaponConfigurationID):
        """
        Return configurations type. Should be one of consts.UPGRADE_TYPE.WEAPON type
        """
        wInfo = self.getInstalledWeaponInfo(aircraftID, weaponSlotID, weaponConfigurationID)
        if wInfo is None:
            LOG_ERROR('Weapon slot type data not found (aircraftID, slotId, slotTypeId)', aircraftID, weaponSlotID, weaponConfigurationID)
            return 0
        else:
            return wInfo[2]

    def __getInstalledWeaponUpgradeName(self, aircraftID, weaponSlotID, weaponConfigurationID = None):
        """
        Return upgrade name of shells that installed in (weaponSlotID, configurationID)
        """
        wInfo = self.__getWeaponInfo(aircraftID, weaponSlotID, weaponConfigurationID)
        if wInfo is None:
            LOG_ERROR('Weapon slot type data not found (aircraftID, slotId, slotTypeId)', aircraftID, weaponSlotID, weaponConfigurationID)
            return
        else:
            return wInfo[1]

    def getAircraftInstalledWeaponsData(self, aircraftID):
        """
        @param aircraftID:
        @return:
        """
        if not self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT]:
            return {}
        else:
            installedConfiguration = self.__getInstalledConfiguration(aircraftID)
            if installedConfiguration is None:
                LOG_ERROR('Installed configurations for plane: %d not found' % aircraftID)
                return
            data = {}
            for slotID, configurationID in installedConfiguration.weaponSlots:
                wInfo = self.__getWeaponInfo(aircraftID, slotID, configurationID)
                if wInfo is not None:
                    weaponType, weaponName, weaponCount = wInfo
                    upgrade = self._db.upgrades.get(weaponName, None)
                    price = 0 if upgrade is None else upgrade.credits
                    if weaponType == UPGRADE_TYPE.BOMB or weaponType == UPGRADE_TYPE.ROCKET:
                        data[slotID] = {'weaponType': weaponType,
                         'weaponID': weaponName,
                         'storeCount': self.getUpgradeCount(weaponName),
                         'maxCount': weaponCount,
                         'curCount': self.getShellsCurrentCount(aircraftID, slotID),
                         'price': price}

            return data

    def setAircraftWeaponSlotData(self, aircraftID, weaponSlotID, slotData = None):
        """
        @param aircraftID:
        @param weaponSlotID:
        @param slotData: beltId or weapon count
        """
        weaponType, weaponName, weaponCount = self.__getWeaponInfo(aircraftID, weaponSlotID)
        if weaponType is None:
            LOG_ERROR('Invalid weaponSlotID = {0} for aircraftID = {1}'.format(weaponSlotID, aircraftID))
            return
        else:
            if weaponType == UPGRADE_TYPE.ROCKET or weaponType == UPGRADE_TYPE.BOMB:
                shellsDataMap = self.getSlotShellsData(aircraftID, weaponSlotID)
                slotData = slotData if slotData is not None else shellsDataMap.get('storedCount', weaponCount)
                diffCount = slotData - shellsDataMap['count']
                shellsDataMap['storedCount'] = slotData
                shellsDataMap['count'] = slotData
                self.removeUpgradeFromDepot(weaponName, diffCount)
            return

    def getInstalledUpgradesCount(self, aircraftID):
        """
        Returns list of all upgrades that are on the airplane
        This list includes modules and weapons upgrades
        @param aircraftID:
        @return: iterator for items of type (<upgrade name>, <count>)
        """
        installedConfig = self.__getInstalledConfiguration(aircraftID)
        return select(((moduleName, 1) for moduleName in installedConfig.modules), ((wInfo[1], wInfo[2]) for wInfo in (self.getInstalledWeaponInfo(aircraftID, w[0], w[1]) for w in installedConfig.weaponSlots) if wInfo is not None))

    def getUpgradeInfoMap(self, aircraftID, upgrade):
        upgradeName = upgrade.name
        isUpgradeOpened = self.isUpgradeOpened(upgradeName)
        parentInfo = self.__getOpenedParentUpgrade(aircraftID, upgrade)
        requiredExperience = 0
        isResearchedAvailable = False
        if parentInfo is not None:
            isResearchedAvailable = self.isAircraftOpened(aircraftID)
        upgradeVariant = next(iter(filter(lambda var: var.aircraftName == self._db.getAircraftData(aircraftID).airplane.name, upgrade.variant)), None)
        parentName = ''
        slotsList = dict()
        if upgradeVariant is not None:
            parentName = upgradeVariant.parentUpgrade[0].name
            requiredExperience = upgradeVariant.parentUpgrade[0].experience
            for slot in upgradeVariant.slot:
                slotsList[slot.id] = slot.typeId

        isInstalled = self.isUpgradeInstalled(aircraftID, upgradeName)
        isInstallAvailable = self.isIntalledRequiredUpgrades(aircraftID, upgrade)
        installedCount = 0
        pdata = self.aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT]
        if pdata:
            for w in self.getInstalledWeapons(aircraftID):
                weapon = self._db.getWeaponInfo(aircraftID, w[0], w[1])
                if weapon is not None and weapon[1] == upgradeName:
                    installedCount += self.getInstalledWeaponCount(aircraftID, w[0], w[1])

        return {'name': upgradeName,
         'type': upgrade.type,
         'level': getattr(upgrade, 'level', 1),
         'isResearched': isUpgradeOpened,
         'isResearchAvailable': isResearchedAvailable,
         'isBought': self.isUpgradeBought(upgradeName),
         'isInstalled': isInstalled,
         'isInstallAvailable': isInstallAvailable,
         'requiredExperience': requiredExperience,
         'priceCredits': upgrade.credits,
         'priceGold': upgrade.gold,
         'slotList': slotsList,
         'boughtCount': self.getUpgradeCount(upgradeName) + installedCount,
         'installedCount': installedCount,
         'parent': parentName,
         'gotExperience': self.getAircraftExp(aircraftID),
         'isDefault': upgrade.name in getDefaultAirplaneConfiguration(aircraftID).modules}

    def __getOpenedParentUpgrade(self, aircraftID, upgrade):
        upgradeVariant = next(iter(filter(lambda var: var.aircraftName == self._db.getAircraftData(aircraftID).airplane.name, upgrade.variant)), None)
        parentInfo = upgradeVariant.parentUpgrade[0]
        parentName = parentInfo.name
        counter = MAX_PARENT_UPGRADES_CHECK_DEPTH
        while parentName and counter > 0:
            counter -= 1
            if not self.isUpgradeOpened(parentName):
                return
            parentUpgrade = self._db.upgrades.get(parentName, None)
            if parentUpgrade is None:
                DBLOG_ERROR('Cannot find parent upgrade {0} of upgrade {1} in db'.format(parentName, upgrade.name))
                return
            pi = next(iter(filter(lambda var: var.aircraftName == self._db.getAircraftData(aircraftID).airplane.name, parentUpgrade.variant)), None)
            parentName = None
            if pi is not None:
                parentName = pi.parentUpgrade[0].name

        if counter == 0:
            DBLOG_ERROR('Seems that parents of upgrade {0} have recursive dependencies'.format(upgrade.name))
        return parentInfo

    def getShopAircrafts(self, nationID, planeType):
        airplanesList = []
        if nationID == -1:
            nationIDList = db.DBLogic.g_instance.getNationIDList()
        else:
            nationIDList = [nationID]
        for nationID in nationIDList:
            airplaneMap = db.DBLogic.g_instance.getAircraftList(nationID)
            d = db.DBLogic.g_instance
            for airplaneID, aircraftData in airplaneMap.items():
                if not IS_DEVELOPMENT and aircraftData.airplane.options.isDev or d.isPlaneExclusive(airplaneID) or d.isPlaneNPC(airplaneID):
                    continue
                price = self.getAircraftPrice(airplaneID)
                priceGold = price[1]
                if priceGold <= 0:
                    continue
                defaultUpgradesList = d.getAircraftUpgrades(airplaneID, True)
                aircraftName = aircraftData.airplane.name
                defaultWeaponsMap = dict()
                defaultModulesList = []
                for upgrade in defaultUpgradesList:
                    defaultModulesList.append({'name': upgrade.name,
                     'type': upgrade.type,
                     'isInstalled': True})
                    upgradeVariant = findIf(upgrade.variant, lambda var: var.aircraftName == aircraftName)
                    for slot in upgradeVariant.slot:
                        defaultWeaponsMap[slot.id] = 0

                if not self.isAircraftBought(airplaneID):
                    airplaneInfoMap = {'airplaneID': airplaneID,
                     'price': price[0],
                     'gold': priceGold,
                     'isResearched': self.isAircraftOpened(airplaneID),
                     'planeXP': self.getAircraftExp(airplaneID),
                     'defaultModulesList': defaultModulesList,
                     'defaultWeaponsMap': defaultWeaponsMap,
                     'isPremium': db.DBLogic.g_instance.isPlanePremium(airplaneID),
                     'isElite': self.isAircraftElite(airplaneID)}
                    airplanesList.append(airplaneInfoMap)

        return airplanesList

    def getCarouselAircrafts(self):
        airplaneList = []
        for aircraftID in self._aircraftsData:
            if self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.SLOT_INDEX] is None:
                continue
            if not self._db.isPlaneOk(aircraftID) or self._db.isPlaneNPC(aircraftID):
                LOG_WARNING('Account(base)::onUpdateAccountInfoResponse. Data of the airplane is NOT correctly. Please check airplane ID ', aircraftID, ')')
                self.removeAircraftFromBoughtList(aircraftID)
                continue
            airplaneMap = self.__getCarouselAirplaneMap(aircraftID)
            if airplaneMap is not None:
                airplaneList.append(airplaneMap)

        return airplaneList

    def getCarouselAircraft(self, aircraftID):
        if not self._db.isPlaneOk(aircraftID) or self._db.isPlaneNPC(aircraftID):
            LOG_WARNING('Account(base)::onUpdateAccountInfoResponse. Data of the airplane is NOT correctly. Please check airplane ID ', aircraftID, ')')
            self.removeAircraftFromBoughtList(aircraftID)
            return None
        else:
            return self.__getCarouselAirplaneMap(aircraftID)

    def __getCarouselAirplaneMap(self, aircraftID):
        pdata = self.aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT]
        if pdata is None:
            return
        else:
            carouselAirplaneMap = {'plane': aircraftID,
             'isPrimary': self.isPrimary(aircraftID),
             'blockType': pdata[PLANE_KEYS.BLOCK_TYPE],
             'repairCost': pdata[PLANE_KEYS.REPAIR_COST],
             'planeXP': self.getAircraftExp(aircraftID),
             'weaponsSlot': self.__getInstalledConfiguration(aircraftID).weaponSlots,
             'modules': self.__getInstalledConfiguration(aircraftID).modules,
             'autoRepair': pdata[PLANE_KEYS.AUTO_REPAIR],
             'autoRefill': pdata[PLANE_KEYS.AUTO_REFILL],
             'sellPrice': self.__getAircraftSellPrice(aircraftID),
             'isPremium': db.DBLogic.g_instance.isPlanePremium(aircraftID),
             'isElite': self.isAircraftElite(aircraftID),
             'dailyFirstWinXPFactor': self.dailyFirstWinXPFactor(aircraftID),
             'dailyFirstWinRemains': self.dailyFirstWinRemains(aircraftID)}
            return carouselAirplaneMap

    def __getAircraftSellPrice(self, planeID):
        price = self._sellPrices.get(planeID, None)
        if price is not None:
            return price
        else:
            from Helpers.cache import getFromCache
            price = getFromCache([[planeID, 'plane']], 'ISellPrice')
            if price is not None:
                return price['credits']
            globalID = self.getInstalledUpgradesGlobalID(planeID)
            return self._db.getSellCostByGlobalID(globalID)

    def getPlaneEquipmentsSellPrice(self, planeID):
        return sum((db.DBLogic.g_instance.getUpgradeSellPrice(self._db.getEquipmentByID(equipmentID)) for equipmentID in self.getEquipment(planeID)))

    def getPlaneConsumablesSellPrice(self, planeID):
        return sum((db.DBLogic.g_instance.getUpgradeSellPrice(self._db.getConsumableByID(consumableDict['id'])) for consumableDict in self.getConsumables(planeID)))

    def getPlaneBeltsSellPrice(self, planeID):
        from exchangeapi.Connectors import getObject
        beltsSellPrice = 0
        weapons = self.getInstalledWeapons(planeID)
        for slotInfo in weapons:
            wInfo = db.DBLogic.g_instance.getWeaponInfo(planeID, *slotInfo)
            if wInfo is not None:
                weaponType, weaponName, weaponCount = wInfo
                upgrade = db.DBLogic.g_instance.upgrades.get(weaponName, None)
                if upgrade is not None:
                    if weaponType == UPGRADE_TYPE.GUN:
                        beltID = self.getPlaneBeltID(planeID, slotInfo[0])
                        beltCount = self.getPlaneBeltCount(planeID, slotInfo[0])
                        beltob = getObject([[beltID, 'ammobelt']])
                        beltsSellPrice += db.DBLogic.g_instance.getUpgradeSellPrice(beltob) * beltCount

        return beltsSellPrice

    def unloadConsumablesToDepot(self, planeID):
        depotConsumables = self.getDepotConsumables()
        planeConsumables = self.getConsumables(planeID)
        toDepot = dict(((item['id'], item['count']) for item in planeConsumables if item['id'] != -1 and item['count']))
        for consumableID, count in toDepot.iteritems():
            depotConsumables[consumableID] = depotConsumables.get(consumableID, 0) + count
            for x in planeConsumables:
                if x['id'] == consumableID:
                    x['count'] = 0

    def unloadEquipmentsToDepot(self, planeID):
        depotEquipments = self.getDepotEquipment()
        planeEquimpents = self.getEquipment(planeID)
        toDepotIDs = [ eqid for eqid in planeEquimpents if eqid != -1 ]
        for equipmentID in toDepotIDs:
            depotEquipments[equipmentID] = depotEquipments.get(equipmentID, 0) + 1

        self.setPlaneEquipment(planeID, [-1] * len(planeEquimpents))

    def getSellPriceWithConfiguration(self, planeID):
        globalID = self.getInstalledUpgradesGlobalID(planeID)
        return self._db.getSellCostByGlobalID(globalID)

    def _getUpgradesPrice(self, upgradesMap):
        price = [0, 0]
        for name, count in upgradesMap.items():
            upgrade = db.DBLogic.g_instance.upgrades.get(name, None)
            if upgrade:
                price[0] += getattr(upgrade, 'credits', 0) * count
                price[1] += getattr(upgrade, 'gold', 0) * count

        return price

    def _sellPrice(self, price):
        return (price[0] + price[1] * _economics.Economics.goldRateForCreditBuys) * _economics.Economics.sellCoeff

    def addAircrafttoBoughtList(self, aircraftID):
        self._inventoryData[ISYNC_INVENTORY.BOUGHT_AIRCRAFTS_LIST].append(aircraftID)

    def removeAircraftFromBoughtList(self, aircraftID):
        del self._inventoryData[ISYNC_INVENTORY.BOUGHT_AIRCRAFTS_LIST][self.getAircraftSlotIndexById(aircraftID)]

    def getDepotWeapons(self):
        """ () -> dict of {str: int}
        Return weapons in depot
        - a dict of {weaponName: weaponCount}
        """
        return dict(((upgName, upgCount) for upgName, upgCount in self._inventoryData[ISYNC_INVENTORY.DEPOT_UPGRADES_DICT].iteritems() if getattr(self._db.upgrades.get(upgName, None), 'type', '') in UPGRADE_TYPE.WEAPON))

    def getDepotEquipment(self):
        """ () -> dict of {int: int}
        Return equipment in depot
        - a dict of {equipmentID: equipmentCount}
        """
        return self._inventoryData[ISYNC_INVENTORY.DEPOT_EQUIPMENT_DICT]

    def getDepotConsumables(self):
        """ () -> dict of {int: int}
        Return consumables in depot
        - a dict of {consumableID: consumableCount}
        """
        return self._inventoryData[ISYNC_INVENTORY.DEPOT_CONSUMABLES_DICT]

    @abstractmethod
    def removeBeltsFromDepot(self, beltID, count):
        pass

    @abstractmethod
    def addBeltsToDepot(self, beltID, count):
        pass

    @abstractmethod
    def getAmmoBeltCount(self, beltID, default = 0):
        pass

    @abstractmethod
    def getAircraftPData(self, aircraftID):
        pass

    def getCrewMember(self, memberID):
        pass

    def getDefaultCrewSkills(self, aircraftID):
        config = getAirplaneConfiguration(airplanesDefaultConfigurations[aircraftID])
        settings = db.DBLogic.g_instance.getAircraftData(aircraftID)
        crewSpecialization = getCrewSpecialization(settings.airplane.partsSettings, config.partTypes)
        return [ {'specializationID': specialization,
         'skills': [{'key': SpecializationSkillDB[specialization].id,
                     'value': 50}]} for specialization in crewSpecialization ]

    def getEquipment(self, aircraftID):
        if aircraftID in self.getBoughtAircraftsList():
            return self.getAircraftPData(aircraftID)[PLANE_KEYS.EQUIPMENT]
        return []

    def getCrewList(self, planeID):
        """        
        :param planeID:
        return [ [spec, memberID], ...]
        On client Inventory not synced for pilot. Just temporary solution get from cache
        """
        if planeID in self.getBoughtAircraftsList():
            if IS_CLIENT:
                from Helpers.cache import getFromCache
                planeCrew = getFromCache([[planeID, 'plane']], 'IPlaneCrew')
                if planeCrew:
                    return [ [m['specialization'], m['id']] for m in planeCrew['crewMembers'] if m['id'] != -1 ]
            else:
                return self.getAircraftPData(planeID)[PLANE_KEYS.CREW][:]
        return []

    def getConsumables(self, aircraftID):
        return self.getAircraftPData(aircraftID)[PLANE_KEYS.CONSUMABLES]


class InventoryClientBase(Inventory):

    def __init__(self, operationSender, onFinishCallback):
        Inventory.__init__(self)
        self.__opsender = operationSender
        self.__querryCount = 0
        self.__onFinishCallback = onFinishCallback
        self.__aircraftPrices = {}
        self.syncInventoryData()
        self.syncAllAircrafts()
        self.syncStats()
        self.syncPlaneList()

    def setFinishCallback(self, onFinishCallback):
        self.__onFinishCallback = onFinishCallback

    def setAircrafsPrices(self, aircraftsPrices, sellPrices):
        if not aircraftsPrices:
            self.__aircraftPrices.clear()
            self._sellPrices.clear()
            return
        for planeID, (cr, gd, _) in aircraftsPrices.iteritems():
            self.__aircraftPrices[planeID] = [cr, gd]

        self._sellPrices = sellPrices

    def getAircraftPrice(self, aircraftID):
        aircraftPrice = self.__aircraftPrices.get(aircraftID, None)
        if aircraftPrice is not None:
            return aircraftPrice
        else:
            aircraftData = self._db.getAircraftData(aircraftID)
            return [getattr(aircraftData.airplane.options, 'price', 0), getattr(aircraftData.airplane.options, 'gold', 0)]

    def setOpSender(self, operationSender):
        self.__opsender = operationSender

    def syncInventoryData(self):
        self.__querryCount += 1
        self.__opsender.getInterfaceData(self.__syncInventoryDataResponse, self._sycnInventoryQuerry)

    def __syncInventoryDataResponse(self, op, res_id, *args):
        self.__querryCount -= 1
        self._inventoryDataInitialized = True
        self._inventoryData = args[0][0]
        if self.__querryCount == 0 and self.__onFinishCallback:
            self.__onFinishCallback()

    def syncAllAircrafts(self):
        self.syncAircraftsData(self._aircraftIDs)

    def syncAircraftsData(self, aircraftIDs, callback = None):
        self.__querryCount += 1
        self.__opsender.getInterfaceData(partial(self.__syncAicraftResponse, callback), [('ISYNC_AIRCRAFT', aircraftIDs)])

    def __syncAicraftResponse(self, callback, op, res_id, *args):
        self.__querryCount -= 1
        self._setAicraftsData(args[0])
        if callback:
            callback()
        if self.__querryCount == 0 and self.__onFinishCallback:
            self.__onFinishCallback()

    def syncPlaneList(self, callback = None):
        self.__querryCount += 1
        self.__opsender.getInterfaceData(partial(self.__syncPlaneListResponse, callback), [('ISYNC_PLANE_LIST', [])])

    def __syncPlaneListResponse(self, callback, op, res_id, *args):
        self.__querryCount -= 1
        self._elitePlaneList = args[0][0][ISYNC_PLANE_LIST.ELITE_PLANES_LIST]
        if callback:
            callback()
        if self.__querryCount == 0 and self.__onFinishCallback:
            self.__onFinishCallback()

    def syncStats(self, callback = None):
        self.__querryCount += 1
        self.__opsender.getInterfaceData(partial(self.__syncStatsResponse, callback), [('ISYNC_STATS', [])])

    def __syncStatsResponse(self, callback, op, res_id, *args):
        self.__querryCount -= 1
        self._stats = args[0][0]
        if callback:
            callback()
        if self.__querryCount == 0 and self.__onFinishCallback:
            self.__onFinishCallback()

    def setDailyFirstWinRemains(self, aircraftID, val):
        self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.DAILY_FIRST_WIN_REMAINS] = val

    def setDailyFirstWinXPCoeff(self, aircraftID, val):
        self._aircraftsData[aircraftID][ISYNC_AIRCRAFT.DAILY_FIRST_WIN_XP_FACTOR] = val

    def removeBeltsFromDepot(self, beltID, count):
        pass

    def addBeltsToDepot(self, beltID, count):
        pass

    def getAmmoBeltCount(self, beltID, default = 0):
        return 0

    def getAircraftPData(self, aircraftID):
        if aircraftID in self.aircraftsData:
            return self.aircraftsData[aircraftID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT]
        else:
            return None

    def setPlaneBlockType(self, planeID, blockType):
        if planeID in self.aircraftsData:
            if self.isAircraftBought(planeID):
                LOG_TRACE('setPlaneBlockType() setting block type {0} for {1}'.format(blockType, planeID))
                self.aircraftsData[planeID][ISYNC_AIRCRAFT.PDATA_AIRCRAFT_DICT][PLANE_KEYS.BLOCK_TYPE] = blockType
        else:
            LOG_ERROR("Plane {0} isn't in aircraftsData".format(planeID))