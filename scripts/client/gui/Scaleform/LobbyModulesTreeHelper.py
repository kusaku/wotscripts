# Embedded file name: scripts/client/gui/Scaleform/LobbyModulesTreeHelper.py
import copy
from functools import partial
import BigWorld
from HelperFunctions import findIf, select
from Helpers.i18n import localizeComponents, localizeAirplaneMid, localizeLobby, localizeUpgrade, localizeTooltips
from IfaceAPI import async, view
from OperationCodes import OPERATION_RETURN_CODE
import _airplanesConfigurations_db
from clientConsts import EMPTY_WEAPON_SLOT_ICON_PATH, HANGAR_MODE, PLANE_CLASS, PLANE_TYPE_ICO_PATH
from consts import UPGRADE_TYPE, DEFAULT_MODULE_GROUPS_ORDER_BY_TYPE, COMPONENT_TYPE
from db.DBLogic import createGlobalID
from debug_utils import LOG_DEBUG, LOG_ERROR, LOG_TRACE
from gui.Scaleform.LobbyAirplaneHelper import getLobbyAirplane, adjustPlaneConfig
import db
from gui.Scaleform.LobbyAirplaneWeapons import EMPTY_WEAPON_NAME_ID
from Helpers.PerformanceSpecsHelper import getPerformanceSpecsTable, getDescriptionList, getGroupedDescriptionFields
from CrewHelpers import previewCrewSpecList, getSpecializationName

class AircraftCharacteristicsDataVO:

    def __init__(self, characteristics):
        self.characteristics = characteristics
        self.rolesList = []


class CostVO:

    def __init__(self, credits, gold):
        self.credits = credits
        self.gold = gold


class NodeVO:

    def __init__(self):
        self.id = -1
        self.parentID = -1
        self.isBought = False
        self.isResearched = False
        self.isInstalled = False
        self.iconPath = False
        self.name = None
        self.level = 0
        self.researchExp = 0
        self.buyCost = None
        self.isAircraft = False
        self.aircraftID = -1
        self.isEmpty = False
        self.isWeapon = False
        self.requiredExp = 0
        self.requiredResearches = []
        self.requiredCount = 0
        self.availableCount = 0
        self.incompatibleModules = None
        self.upgradeName = None
        self.isAircraftAvailable = False
        self.aircraftGainedExp = 0
        self.aircraftTypeIconPath = None
        self.isAircraftElite = False
        self.planeBranchNum = 0
        self.weaponConfig = None
        self.slotID = None
        self.weaponGroup = -1
        self.weaponType = None
        self.defaultAmmoInstalled = True
        return


class GroupVO:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.nodes = []


class PresetVO:

    def __init__(self, id, name):
        self.id = id
        self.name = name


class AircraftInfoVO:

    def __init__(self):
        self.name = None
        self.description = None
        self.level = 0
        self.iconTypePath = None
        self.typeName = None
        self.iconPath = None
        self.buyCost = None
        self.researchExp = 0
        self.requiredExp = 0
        self.researchedParentID = None
        self.isBought = False
        self.isResearched = False
        self.isResearchAvailable = False
        self.requiredResearches = None
        self.isPremium = False
        self.isElite = False
        self.gainedExp = 0
        self.longName = None
        self.crew = None
        return


class CrewMemberVO:
    specIconPath = None

    def __init__(self):
        self.specIconPath = ''
        self.tooltip = ''


class DataVO:

    def __init__(self, nodes, groups, presets, selectedPresetID, aircraftInfo):
        self.nodes = nodes
        self.groups = groups
        self.presets = presets
        self.selectedPresetID = selectedPresetID
        self.aircraftInfo = aircraftInfo


class ResearchVO:

    def __init__(self, moduleName, typeName, exp):
        self.moduleName = moduleName
        self.typeName = typeName
        self.exp = exp


class AircraftCharacteristicsGroupVO:

    def __init__(self):
        self.main = None
        self.additional = None
        return


class NodeData:

    def __init__(self):
        self.vo = None
        self.upgrade = None
        self.upgradeVariant = None
        self.isEmptyWeapon = False
        self.compatibilityList = None
        self.groupIndex = None
        self.groupName = None
        self.isDefault = False
        return


class LobbyModulesTreeHelper(object):

    def __init__(self, lobby):
        self.__lobby = lobby
        self.__nodes = {}
        from BWPersonality import g_lobbyCarouselHelper
        self.__selectedAircraft = None
        self.__lobbyCarouselHelper = g_lobbyCarouselHelper
        self.__db = db.DBLogic.g_instance
        self.__initialized = False
        self.__originPlane = None
        self.__nonElite = None
        return

    def registerCallbacks(self):
        self.__lobby.addExternalCallbacks({'moduleTree.initialize': self.__onInitialized,
         'moduleTree.dispose': self.__onDispose,
         'moduleTree.selectModule': self.__onSelectModule,
         'moduleTree.researchModule': self.__onResearchModule,
         'moduleTree.installModule': self.__onInstallModule,
         'moduleTree.researchAircraft': self.__onResearchAircraft,
         'moduleTree.researchAircraftNode': self.__onResearchAircraftNode,
         'moduleTree.buyAndInstallModule': self.__onBuyAndInstallModule})

    @property
    def initialized(self):
        return self.__initialized

    def __onDispose(self):
        self.__selectedAircraft = None
        self.__originPlane = None
        self.__initialized = False
        return

    @async
    def __onInitialized(self, selectedAircraftID):
        self.__initialized = True
        self.__fillNodes(selectedAircraftID)
        if self.__selectedAircraft.isBought:
            planeID = self.__selectedAircraft.planeID
            installedBeltsData = yield view([ [{'IInstalledAmmoBelt': {}}, [[planeID, 'plane'], [slotID, 'weaponslot']]] for slotID in self.__getInstalledSlots() ])
            if self.__initialized and planeID == self.__selectedAircraft.planeID:
                installedBeltsDict = {}
                for item in installedBeltsData:
                    data, idTypeList = item
                    weaponSlotID = idTypeList[1][0]
                    installedBeltsDict[weaponSlotID] = data['IInstalledAmmoBelt']['objID']

                for moduleNode in self.__nodes.itervalues():
                    if moduleNode.vo.isWeapon and moduleNode.vo.weaponType == UPGRADE_TYPE.GUN and moduleNode.vo.isInstalled:
                        gun = db.DBLogic.g_instance.getComponentByName(COMPONENT_TYPE.GUNS, moduleNode.upgrade.name)
                        moduleNode.vo.defaultAmmoInstalled = installedBeltsDict[moduleNode.vo.slotID] == gun.defaultBelt

    def __getInstalledSlots(self):
        for weapon in self.__selectedAircraft.weapons.getSortedWeaponsList():
            if weapon.weaponNameID != EMPTY_WEAPON_NAME_ID:
                upgrade = self.__db.upgrades.get(weapon.weaponNameID, None)
                if upgrade.type == UPGRADE_TYPE.GUN:
                    if weapon.isInstalled:
                        yield weapon.weaponSlotID

        return

    def __fillNodes(self, selectedAircraftID):
        inventory = self.__lobbyCarouselHelper.inventory
        self.__originPlane = self.__lobbyCarouselHelper.getCarouselAirplane(selectedAircraftID)
        if self.__originPlane is None:
            self.__originPlane = getLobbyAirplane(selectedAircraftID)
        if self.__originPlane is None:
            LOG_ERROR('Aircraft %d not found' % selectedAircraftID)
            return
        else:
            LOG_DEBUG('__onInitialized selectedAircraftID = {0}'.format(selectedAircraftID))
            self.__selectedAircraft = copy.deepcopy(self.__originPlane)
            self.__selectedAircraft.presets.fillPresets()
            self.__selectedAircraft.experience = self.__lobbyCarouselHelper.inventory.getAircraftExp(selectedAircraftID)
            if (self.__selectedAircraft.isPremium or self.__selectedAircraft.isBought) and not self.__selectedAircraft.isResearched:
                self.__lobbyCarouselHelper.inventory.openAircraft(self.__selectedAircraft.planeID)
                self.__selectedAircraft.isResearched = True
            self.__nodes.clear()
            aircraftData = self.__db.getAircraftData(selectedAircraftID)
            groupedModules = {}
            groupsVOs = {}
            selectedAircraftName = self.__db.getAircraftName(self.__selectedAircraft.planeID)
            nodesCounter = 0
            for component in self.__selectedAircraft.modules.getSortedModules():
                upgrade = self.__db.upgrades.get(component['name'])
                if upgrade.type == UPGRADE_TYPE.AIRCRAFT:
                    aircraftChildData = self.__db.getAircraftData(self.__db.getAircraftIDbyName(upgrade.name))
                    if aircraftChildData.airplane.options.hidePlaneResearch:
                        continue
                moduleNode = NodeData()
                moduleNode.isDefault = component['isDefault']
                moduleNode.upgrade = upgrade
                moduleNode.upgradeVariant = findIf(moduleNode.upgrade.variant, lambda item: item.aircraftName == selectedAircraftName)
                moduleNode.vo = NodeVO()
                moduleNode.vo.upgradeName = moduleNode.upgrade.name
                moduleNode.vo.dbID = moduleNode.upgrade.id
                moduleNode.vo.name = localizeUpgrade(moduleNode.upgrade)
                moduleNode.vo.isInstalled = component['isInstalled'] and self.__selectedAircraft.isBought
                moduleNode.vo.id = nodesCounter
                nodesCounter += 1
                moduleNode.vo.iconPath = moduleNode.upgrade.typeIconPath
                moduleNode.vo.isBought = inventory.isUpgradeBought(moduleNode.upgrade.name) or moduleNode.vo.isInstalled
                moduleNode.vo.requiredCount = 1
                moduleNode.vo.availableCount = max(0, inventory.getUpgradeCount(moduleNode.upgrade.name))
                groupType = moduleNode.upgrade.type
                try:
                    moduleNode.groupIndex = aircraftData.airplane.options.moduleGroupsOrder.group.index(groupType)
                except:
                    moduleNode.groupIndex = DEFAULT_MODULE_GROUPS_ORDER_BY_TYPE[groupType]

                moduleNode.groupName = localizeComponents(UPGRADE_TYPE.DESCRIPTION_MAP[groupType])
                moduleNode.vo.level = moduleNode.upgrade.level
                groupedModules.setdefault(moduleNode.groupIndex, []).append(moduleNode)
                self.__nodes[moduleNode.vo.id] = moduleNode

            for weapon in self.__selectedAircraft.weapons.getSortedWeaponsList():
                moduleNode = NodeData()
                moduleNode.isDefault = weapon.isDefault
                moduleNode.vo = NodeVO()
                moduleNode.vo.weaponConfig = weapon.configurationID
                moduleNode.vo.slotID = weapon.weaponSlotID
                moduleNode.vo.id = nodesCounter
                moduleNode.vo.isInstalled = weapon.isInstalled and self.__selectedAircraft.isBought
                nodesCounter += 1
                if weapon.weaponNameID == EMPTY_WEAPON_NAME_ID:
                    moduleNode.isEmptyWeapon = True
                    moduleNode.vo.dbID = -1
                    moduleNode.vo.iconPath = EMPTY_WEAPON_SLOT_ICON_PATH
                    moduleNode.vo.isResearched = self.__selectedAircraft.isResearched
                    moduleNode.vo.researchExp = 0
                    moduleNode.vo.buyCost = CostVO(0, 0)
                    moduleNode.vo.isEmpty = True
                    moduleNode.vo.incompatibleModules = []
                    moduleNode.vo.name = localizeLobby('WEAPON_NAME_EMPTY')
                else:
                    moduleNode.upgrade = self.__db.upgrades.get(weapon.weaponNameID, None)
                    if moduleNode.upgrade is None:
                        LOG_ERROR('WeaponNameID = "{0}" cannot be found in db'.format(weapon.weaponNameID))
                        continue
                    moduleNode.vo.dbID = moduleNode.upgrade.id
                    moduleNode.upgradeVariant = findIf(moduleNode.upgrade.variant, lambda item: item.aircraftName == selectedAircraftName)
                    if moduleNode.upgradeVariant is None:
                        LOG_ERROR('WeaponNameID = "{0}" does not contains variant for aircraft = {1}'.format(weapon.weaponNameID, selectedAircraftName))
                        continue
                    moduleNode.vo.upgradeName = moduleNode.upgrade.name
                    moduleNode.vo.name = localizeUpgrade(moduleNode.upgrade)
                    moduleNode.vo.iconPath = weapon.icoPath
                    moduleNode.vo.requiredCount = weapon.neededCount
                    moduleNode.vo.level = moduleNode.upgrade.level
                    self.__updateWeaponAvailableCount(moduleNode)
                    moduleNode.vo.weaponType = moduleNode.upgrade.type
                    if moduleNode.upgrade.type == UPGRADE_TYPE.GUN:
                        gun = db.DBLogic.g_instance.getComponentByName(COMPONENT_TYPE.GUNS, moduleNode.upgrade.name)
                        moduleNode.vo.weaponGroup = gun.id
                moduleNode.vo.isWeapon = True
                groupType = 'slot_%s' % str(weapon.weaponSlotID)
                try:
                    moduleNode.groupIndex = aircraftData.airplane.options.moduleGroupsOrder.group.index(groupType)
                except:
                    moduleNode.groupIndex = DEFAULT_MODULE_GROUPS_ORDER_BY_TYPE[groupType]

                moduleNode.groupName = self.__selectedAircraft.weapons.getSlotsInfoMap()[weapon.weaponSlotID]['description']
                groupedModules.setdefault(moduleNode.groupIndex, []).append(moduleNode)
                self.__nodes[moduleNode.vo.id] = moduleNode

            aircraftConfigurations = [ _airplanesConfigurations_db.getAirplaneConfiguration(globalID) for globalID in _airplanesConfigurations_db.airplanesConfigurationsList[selectedAircraftID] ]
            for cSlotId, val in groupedModules.iteritems():
                for cIndex, cModule in enumerate(val):
                    if not groupsVOs.has_key(cModule.groupIndex):
                        groupsVOs[cModule.groupIndex] = GroupVO(cModule.groupIndex, cModule.groupName)
                    groupsVOs[cModule.groupIndex].nodes.append(cModule.vo.id)
                    incompatibleModules = self.__nodes.keys()
                    for aircraftConfig in aircraftConfigurations:
                        if not incompatibleModules:
                            break
                        if cModule.vo.isWeapon and (cModule.vo.slotID, cModule.vo.weaponConfig) in aircraftConfig.weaponSlots or not cModule.vo.isWeapon and cModule.upgrade.name in aircraftConfig.modules:
                            for node in self.__nodes.itervalues():
                                if node.vo.id in incompatibleModules:
                                    if node.vo.isWeapon and (node.vo.slotID, node.vo.weaponConfig) in aircraftConfig.weaponSlots or not node.vo.isWeapon and node.upgrade.name in aircraftConfig.modules:
                                        incompatibleModules.remove(node.vo.id)

                    cModule.vo.incompatibleModules = incompatibleModules
                    cModule.vo.isBought = self.__isBought(cModule)
                    parentNode = None
                    if not cModule.isEmptyWeapon:
                        cModule.vo.buyCost = CostVO(cModule.upgrade.credits, cModule.upgrade.gold)
                        if cModule.upgradeVariant.parentUpgrade:
                            parentUpgrade = cModule.upgradeVariant.parentUpgrade[0]
                            if hasattr(parentUpgrade, 'weaponConfig'):
                                parentNode = findIf(self.__nodes.itervalues(), lambda n: not n.isEmptyWeapon and n.vo.isWeapon and n.upgrade.name == parentUpgrade.name and parentUpgrade.weaponConfig.slotID == n.vo.slotID and parentUpgrade.weaponConfig.slotConfigID == n.vo.weaponConfig)
                            else:
                                parentNode = findIf(self.__nodes.itervalues(), lambda n: not n.isEmptyWeapon and n.upgrade.name == parentUpgrade.name)
                            if parentNode:
                                cModule.vo.parentID = parentNode.vo.id
                            cModule.vo.researchExp = cModule.upgradeVariant.parentUpgrade[0].experience
                            if not cModule.isDefault:
                                self.__updateNodeRequiredResearches(cModule)
                        self.__updateResearchStatus(cModule)
                    if cModule.vo.isWeapon:
                        if not cModule.isDefault:
                            requiredNodes = [ n for n in self.__nodes.itervalues() if not n.vo.isWeapon and any((s for s in n.upgradeVariant.slot if s.id == cModule.vo.slotID and cModule.vo.weaponConfig in s.typeId)) ]
                            if parentNode is None and len(requiredNodes) == 1 and len(groupedModules[requiredNodes[0].groupIndex]) != 1:
                                cModule.vo.parentID = requiredNodes[0].vo.id
                            elif cModule.vo.parentID == -1:
                                for node in groupedModules[cModule.groupIndex]:
                                    if node.vo.id != cModule.vo.id and cModule.vo.level > node.vo.level and (not parentNode or parentNode.vo.level < node.vo.level) or node.isDefault:
                                        parentNode = node

                                if parentNode:
                                    cModule.vo.parentID = parentNode.vo.id
                    else:
                        for slot in cModule.upgradeVariant.slot:
                            if len(slot.typeId) == 1 and self.__db.getWeaponInfo(selectedAircraftID, slot.id, slot.typeId[0]) is None:
                                node = findIf(self.__nodes.itervalues(), lambda n: n.isEmptyWeapon and not n.isDefault and n.vo.slotID == slot.id and n.vo.weaponConfig == slot.typeId[0])
                                if node is not None:
                                    node.vo.parentID = cModule.vo.id

            aircraftUpgrades, aircrafts = self.__db.getAircraftUpgrades(selectedAircraftID)
            if not aircraftData.airplane.options.hidePlaneResearch:
                for childUpgrade in aircrafts:
                    self.__addAircraftNode(childUpgrade.name, childUpgrade, nodesCounter, False, selectedAircraftID)
                    nodesCounter += 1

            selectedAircraftUpgrade = self.__db.upgrades.get(selectedAircraftName, None)
            if selectedAircraftUpgrade is not None and not aircraftData.airplane.options.hidePlaneResearch:
                parentAircraftUpgrades = [ self.__db.upgrades.get(variant.aircraftName, None) for variant in selectedAircraftUpgrade.variant ]
                for parentAircraftUpgrade in parentAircraftUpgrades:
                    if parentAircraftUpgrade:
                        self.__addAircraftNode(parentAircraftUpgrade.name, parentAircraftUpgrade, nodesCounter, True)
                    else:
                        self.__addAircraftNode(selectedAircraftUpgrade.variant[0].aircraftName, None, nodesCounter, True)
                    nodesCounter += 1

            self.__updateAircraftInfoVO()
            selectedPresetName = self.__selectedAircraft.presets.getInstalled().name if self.__selectedAircraft.isBought else self.__db.getAircraftDefaultPreset(selectedAircraftID).name
            self.__lobby.call_1('moduleTree.setData', DataVO([ n.vo for n in self.__nodes.itervalues() ], groupsVOs.values(), [ PresetVO(preset.name, preset.title) for preset in self.__selectedAircraft.presets.getAll() ], selectedPresetName, self.__selectedAircraft.vo))
            self.__previewSelectedModulesStats(-1)
            return

    def __isBought(self, node):
        isFree = not node.vo.isWeapon and node.upgrade.credits == 0 and node.upgrade.gold == 0
        onWarehouse = node.vo.availableCount >= node.vo.requiredCount
        return node.isEmptyWeapon or node.vo.isInstalled or onWarehouse or isFree

    def __addAircraftNode(self, aircraftName, upgrade, nodesID, isParent, parentPlaneID = None):
        aircraftID = self.__db.getAircraftIDbyName(aircraftName)
        airplaneData = self.__db.getAircraftData(aircraftID)
        dataMap = self.__lobbyCarouselHelper.inventory.getAircraftClientDataMap(aircraftID, self.__db.getAircraftName(parentPlaneID) if parentPlaneID else None)
        aircraftNode = NodeData()
        aircraftNode.upgrade = upgrade
        aircraftNode.vo = NodeVO()
        aircraftNode.vo.id = nodesID
        aircraftNode.vo.dbID = aircraftID
        aircraftNode.vo.isBought = dataMap['isBought']
        aircraftNode.vo.isResearched = dataMap['isResearched']
        aircraftNode.vo.buyCost = CostVO(dataMap['priceCredits'], dataMap['priceGold'])
        aircraftNode.vo.iconPath = airplaneData.airplane.treeIconPath
        aircraftNode.vo.level = airplaneData.airplane.level
        aircraftNode.vo.name = localizeAirplaneMid(airplaneData.airplane.name)
        aircraftNode.vo.isAircraft = True
        aircraftNode.vo.aircraftID = aircraftID
        if not isParent and dataMap['parent']:
            selectedAircraftName = self.__db.getAircraftName(self.__selectedAircraft.planeID)
            aircraftNode.upgradeVariant = findIf(upgrade.variant, lambda v: v.aircraftName == selectedAircraftName)
            parentNode = findIf(self.__nodes.itervalues(), lambda n: not n.isEmptyWeapon and n.upgrade.name == aircraftNode.upgradeVariant.parentUpgrade[0].name)
            aircraftNode.vo.parentID = parentNode.vo.id if parentNode else -1
        aircraftNode.vo.researchExp = dataMap['reqiuredExperiencePlane']
        aircraftNode.vo.aircraftGainedExp = dataMap['gotExperience']
        aircraftNode.vo.isAircraftAvailable = self.__lobbyCarouselHelper.inventory.isPlaneResearchAvailableOpened(aircraftID)
        isPremium = dataMap['isPremium']
        aircraftNode.vo.isAircraftElite = dataMap['isElite']
        planeStatus = isPremium * PLANE_CLASS.PREMIUM or aircraftNode.vo.isAircraftElite * PLANE_CLASS.ELITE or PLANE_CLASS.REGULAR
        aircraftNode.vo.aircraftTypeIconPath = PLANE_TYPE_ICO_PATH.icon(airplaneData.airplane.planeType, planeStatus)
        aircraftNode.vo.planeBranchNum = airplaneData.airplane.branch
        self.__updatePlaneRequiredResearches(aircraftNode.vo, aircraftID, parentPlaneID)
        self.__nodes[aircraftNode.vo.id] = aircraftNode
        return

    def __updateResearchStatus(self, node):
        node.vo.isResearched = self.__lobbyCarouselHelper.inventory.isUpgradeOpened(node.upgrade.name) or self.__selectedAircraft.isResearched and node.vo.researchExp == 0

    def __updateNodesResearches(self):
        nodesToUpdate = []
        for node in self.__nodes.itervalues():
            if node.vo.isAircraft:
                node.vo.isAircraftAvailable = self.__lobbyCarouselHelper.inventory.isPlaneResearchAvailableOpened(node.vo.aircraftID)
                self.__updatePlaneRequiredResearches(node.vo, node.vo.aircraftID)
            elif node.isEmptyWeapon:
                node.vo.isResearched = True
            else:
                self.__updateResearchStatus(node)
                self.__updateNodeRequiredResearches(node)
            nodesToUpdate.append(node.vo)

        return nodesToUpdate

    def __updateNodeRequiredResearches(self, node):
        node.vo.requiredResearches = []
        node.vo.requiredExp = 0
        if node.vo.isResearched:
            return
        else:
            requiredResearchesNames = set()
            for parent in self.__lobbyCarouselHelper.inventory.calculateRequiredUpgradesForUpgrade(node.upgrade, node.upgradeVariant):
                if parent != node.upgrade.name:
                    parentNode = findIf(self.__nodes.itervalues(), lambda n: not n.isEmptyWeapon and n.upgrade.name == parent)
                    if parentNode:
                        node.vo.requiredResearches.append(ResearchVO(parentNode.vo.name, parentNode.groupName, parentNode.upgradeVariant.parentUpgrade[0].experience))
                        requiredResearchesNames.add(parentNode.upgrade.name)

            node.vo.requiredExp = node.vo.researchExp + self.__lobbyCarouselHelper.inventory.calculateRequiredResourcesForUpgradePresset(self.__selectedAircraft.planeID, requiredResearchesNames, None)['exp']
            return

    def __updatePlaneRequiredResearches(self, aircraftVO, planeID, parentPlaneID = None):
        aircraftVO.requiredExp = dict()
        aircraftVO.requiredResearches = dict()
        if not self.__lobbyCarouselHelper.inventory.isAircraftOpened(planeID):
            for parentPlaneID, toResearch, _ in self.__lobbyCarouselHelper.inventory.calculateRequiredUpgradesForAircraft(planeID, parentPlaneID, onlyResearched=False):
                needResources = self.__lobbyCarouselHelper.inventory.calculateRequiredResourcesForUpgradePresset(parentPlaneID, toResearch, [])
                aircraftVO.requiredResearches[parentPlaneID] = [ ResearchVO(localizeUpgrade(self.__db.upgrades[u]), self.__getUpgradeGroupName(parentPlaneID, self.__db.upgrades[u]), needResources[u]['exp']) for u in toResearch ]
                aircraftVO.requiredExp[parentPlaneID] = needResources['exp'] + aircraftVO.researchExp[parentPlaneID]

    def updateAircraftNodePrices(self):
        updateList = []
        for node in self.__nodes.itervalues():
            if node.vo.isAircraft:
                price = self.__lobbyCarouselHelper.inventory.getAircraftPrice(node.vo.dbID)
                node.vo.buyCost = CostVO(price[0], price[1])
                updateList.append(node.vo)

        self.__lobby.call_1('moduleTree.updateNodes', updateList)

    def updateAircraftInfo(self):
        self.__updateAircraftInfoVO()
        self.__lobby.call_1('moduleTree.updateAircraftInfo', self.__selectedAircraft.vo)

    def __updateAircraftInfoVO(self):
        self.__selectedAircraft.updatePrice()
        if not getattr(self.__selectedAircraft, 'vo', None):
            self.__selectedAircraft.vo = AircraftInfoVO()
        dataMap = self.__lobbyCarouselHelper.inventory.getAircraftClientDataMap(self.__selectedAircraft.planeID)
        self.__selectedAircraft.vo.name = localizeAirplaneMid(self.__db.getAircraftName(self.__selectedAircraft.planeID))
        self.__selectedAircraft.vo.longName = self.__selectedAircraft.longName
        self.__selectedAircraft.vo.typeName = self.__selectedAircraft.type
        self.__selectedAircraft.vo.description = self.__selectedAircraft.getMainDescription()
        self.__selectedAircraft.vo.iconPath = self.__selectedAircraft.previewIconPath
        self.__selectedAircraft.vo.level = self.__selectedAircraft.level
        self.__selectedAircraft.vo.buyCost = CostVO(self.__selectedAircraft.price, self.__selectedAircraft.gold)
        self.__selectedAircraft.vo.researchExp = dataMap['reqiuredExperiencePlane']
        self.__selectedAircraft.vo.researchedParentID = dataMap['researchedParentID']
        self.__selectedAircraft.vo.isBought = self.__selectedAircraft.isBought
        self.__selectedAircraft.vo.isResearched = self.__selectedAircraft.isResearched or self.__selectedAircraft.isPremium
        self.__selectedAircraft.vo.isResearchAvailable = self.__selectedAircraft.isResearchAvailable()
        self.__selectedAircraft.vo.isPremium = self.__selectedAircraft.isPremium
        self.__selectedAircraft.isElite = self.__lobbyCarouselHelper.inventory.isAircraftElite(self.__selectedAircraft.planeID)
        self.__selectedAircraft.vo.isElite = self.__selectedAircraft.isElite
        self.__selectedAircraft.experience = dataMap['gotExperience']
        self.__selectedAircraft.vo.gainedExp = self.__selectedAircraft.experience
        planeStatus = self.__selectedAircraft.isPremium * PLANE_CLASS.PREMIUM or self.__selectedAircraft.isElite * PLANE_CLASS.ELITE or PLANE_CLASS.REGULAR
        self.__selectedAircraft.vo.iconTypePath = PLANE_TYPE_ICO_PATH.icon(self.__selectedAircraft.planeType, planeStatus)
        self.__updatePlaneRequiredResearches(self.__selectedAircraft.vo, self.__selectedAircraft.planeID)
        crewSpecList = previewCrewSpecList(self.__selectedAircraft.planeID)
        self.__selectedAircraft.vo.crew = []
        specIcoPath = 'icons/specialization/crew/hangPilotsIcon{0}.png'
        for crewSpec in crewSpecList:
            crewMember = CrewMemberVO()
            crewMember.specIconPath = specIcoPath.format(getSpecializationName(crewSpec))
            crewMember.tooltip = localizeTooltips('TOOLTIP_CREW_{0}'.format(getSpecializationName(crewSpec).upper()))
            self.__selectedAircraft.vo.crew.append(crewMember)

        return

    def __onSelectModule(self, oldSelectID, newSelectID):
        self.__previewSelectedModulesStats(newSelectID)

    def sendSpecsToAS(self, globalID = None, compare = False):
        if self.__originPlane is None:
            return
        else:
            carouselPlane = self.__lobbyCarouselHelper.getCarouselAirplaneSelected()
            carouselPlaneID = carouselPlane.planeID if carouselPlane is not None else carouselPlane
            if carouselPlaneID is not None and carouselPlaneID == self.__selectedAircraft.planeID:
                carouselGlobalID = self.__lobbyCarouselHelper.inventory.getInstalledUpgradesGlobalID(carouselPlaneID)
                projectiles = carouselPlane.weapons.getInstalledProjectiles()
                equipment = self.__lobbyCarouselHelper.inventory.getEquipment(carouselPlaneID)
                crew = self.__lobbyCarouselHelper.inventory.getCrewList(carouselPlaneID)
                compareSpecs = getPerformanceSpecsTable(carouselGlobalID, True, projectiles, equipment, crew)
                if globalID is None or not compare:
                    specs = compareSpecs
                    globalID = carouselGlobalID
                else:
                    specs = getPerformanceSpecsTable(globalID, True, None, equipment, crew)
            else:
                upgrades = [ upgrade['name'] for upgrade in self.__originPlane.modules.getInstalled() ]
                compareGlobalID = db.DBLogic.createGlobalID(self.__originPlane.planeID, upgrades, self.__originPlane.weapons.getInstalledWeaponsList())
                equipment = self.__lobbyCarouselHelper.inventory.getEquipment(self.__originPlane.planeID)
                crew = self.__lobbyCarouselHelper.inventory.getCrewList(self.__originPlane.planeID)
                if globalID is None:
                    upgrades = [ upgrade['name'] for upgrade in self.__selectedAircraft.modules.getInstalled() ]
                    globalID = db.DBLogic.createGlobalID(self.__selectedAircraft.planeID, upgrades, self.__selectedAircraft.weapons.getInstalledWeaponsList())
                specs = getPerformanceSpecsTable(globalID, True, None, equipment, crew)
                if not compare:
                    compareSpecs = specs
                else:
                    compareSpecs = getPerformanceSpecsTable(compareGlobalID, True, None, equipment, crew)
            descriptionFields = getGroupedDescriptionFields(getDescriptionList(specs, globalID, compareSpecs) + self.__selectedAircraft.getWeaponDescriptionList())
            self.__lobby.call_1('moduleTree.setAircraftCharacteristics', AircraftCharacteristicsDataVO(descriptionFields), globalID)
            return

    def __previewSelectedModulesStats(self, moduleID):
        if self.__originPlane is None:
            return
        else:
            modules = [ upgrade['name'] for upgrade in self.__originPlane.modules.getInstalled() ]
            weapons = self.__originPlane.weapons.getInstalledWeaponsList()
            node = self.__nodes[moduleID] if moduleID in self.__nodes else None
            if moduleID == -1 or node is None or node.vo.isInstalled or not self.__originPlane.isBought and node.isDefault:
                self.__selectedAircraft.modules.setInstalledModules(modules)
                self.__selectedAircraft.weapons.setInstalledWeapons(weapons)
                self.sendSpecsToAS(db.DBLogic.createGlobalID(self.__originPlane.planeID, modules, weapons), False)
                return
            replaceName = None
            useSlotID = None
            if node.isEmptyWeapon or node.upgrade.type in UPGRADE_TYPE.WEAPON:
                weaponDict = dict(weapons)
                if node.vo.slotID in weaponDict:
                    useSlotID = node.vo.slotID
                    weaponInfo = db.DBLogic.g_instance.getWeaponInfo(self.__originPlane.planeID, useSlotID, weaponDict[useSlotID])
                    if weaponInfo is not None:
                        _, replaceName, _ = weaponInfo
            globalID, modules, weapons = adjustPlaneConfig(self.__originPlane.planeID, modules, weapons, None if node.upgrade is None else node.upgrade.name, replaceName, useSlotID, node.vo.weaponConfig)
            if globalID in _airplanesConfigurations_db.airplanesConfigurationsList[self.__selectedAircraft.planeID]:
                self.__selectedAircraft.modules.setInstalledModules(modules)
                self.__selectedAircraft.partTypes = self.__selectedAircraft.modules.getPartTypes()
                self.__selectedAircraft.weapons.setInstalledWeapons(weapons)
                self.sendSpecsToAS(globalID, True)
            else:
                LOG_ERROR('previewSelectedModulesStats not valid globalID modules = {0}, weapons = {1}, planeID = {2}'.format(modules, weapons, self.__selectedAircraft.planeID))
            return

    def __onInstallModule(self, oldInstalledIDs, newInstalledIDs):
        installedModules = list(set(select((m['name'] for m in self.__originPlane.modules.getInstalled() if m['name'] not in (self.__nodes[id].upgrade.name for id in oldInstalledIDs if not self.__nodes[id].vo.isWeapon)), (self.__nodes[id].upgrade.name for id in newInstalledIDs if not self.__nodes[id].vo.isWeapon))))
        installedWeapons = list(set(select((w for w in self.__originPlane.weapons.getInstalledWeaponsList() if w not in ((self.__nodes[id].vo.slotID, self.__nodes[id].vo.weaponConfig) for id in oldInstalledIDs if self.__nodes[id].vo.isWeapon)), ((self.__nodes[id].vo.slotID, self.__nodes[id].vo.weaponConfig) for id in newInstalledIDs if self.__nodes[id].vo.isWeapon))))
        globalID = createGlobalID(self.__selectedAircraft.planeID, installedModules, installedWeapons)
        if globalID not in _airplanesConfigurations_db.airplanesConfigurationsList[self.__selectedAircraft.planeID]:
            LOG_ERROR('Trying to install not valid global id ({0}) on aircraft with id = {1}, installedModules = {2}, installedWeapons = {3}'.format(globalID, self.__selectedAircraft.planeID, installedModules, installedWeapons))
            return
        self.__lobbyCarouselHelper.onInstallAircraftConfiguration(globalID, partial(self.__onInstallModuleResponse, oldInstalledIDs, newInstalledIDs))
        self.__setInstalledModule(installedModules, installedWeapons, oldInstalledIDs, newInstalledIDs, globalID)

    def __onInstallModuleResponse(self, oldInstalledIDs, newInstalledIDs, operation, resultID, *args):
        if resultID != OPERATION_RETURN_CODE.SUCCESS:
            LOG_TRACE('Module installation failed: {0}'.format(resultID))
            self.__fillNodes(self.__originPlane.planeID)

    def __setInstalledModule(self, modules, weapons, oldInstalledIDs, newInstalledIDs, globalID):
        self.__selectedAircraft.modules.setInstalledModules(modules)
        upgradesList = self.__lobbyCarouselHelper.inventory.getAircraftUpgradesData(self.__selectedAircraft.planeID)
        self.__selectedAircraft.weapons.update(upgradesList)
        self.__selectedAircraft.weapons.setInstalledWeapons(weapons)
        self.__selectedAircraft.presets.fillPresets()
        self.__selectedAircraft.partTypes = _airplanesConfigurations_db.getAirplaneConfiguration(globalID).partTypes
        self.__originPlane = self.__selectedAircraft
        self.__selectedAircraft = copy.deepcopy(self.__originPlane)
        for nodeID in oldInstalledIDs:
            self.__nodes[nodeID].vo.isInstalled = False

        for nodeID in newInstalledIDs:
            node = self.__nodes[nodeID]
            node.vo.isInstalled = True
            node.vo.isBought = True
            if not node.vo.isWeapon:
                node.vo.availableCount = self.__lobbyCarouselHelper.inventory.getUpgradeCount(node.upgrade.name)

        for nodeID, node in self.__nodes.iteritems():
            if not node.isEmptyWeapon and node.vo.isWeapon:
                self.__updateWeaponAvailableCount(node)

        self.__lobby.call_1('moduleTree.updateNodes', [ node.vo for node in self.__nodes.itervalues() ])
        carouselSelectedPlane = self.__lobbyCarouselHelper.getCarouselAirplaneSelected()
        if carouselSelectedPlane is not None and carouselSelectedPlane.planeID == self.__selectedAircraft.planeID:
            self.__onModulesSynced(carouselSelectedPlane)
        return

    def __updateWeaponAvailableCount(self, node):
        node.vo.availableCount = self.__lobbyCarouselHelper.inventory.getUpgradeCount(node.upgrade.name)
        conf = findIf(self.__selectedAircraft.weapons.getWeaponSlotConfigs(node.vo.slotID), lambda wc: wc.weaponNameID == node.upgrade.name and wc.isInstalled)
        if conf and self.__selectedAircraft.isBought:
            node.vo.availableCount += self.__lobbyCarouselHelper.inventory.getInstalledWeaponCount(self.__selectedAircraft.planeID, conf.weaponSlotID, conf.configurationID)

    def __onModulesSynced(self, selectedPlane):
        self.__lobbyCarouselHelper.queryRefresh3DModel(selectedPlane)
        BigWorld.player().base.selectActivePlane(selectedPlane.planeID)

    def __onBuyAndInstallModule(self, buyModuleID, oldInstalledIDs, newInstalledIDs):
        self.__onInstallModule(oldInstalledIDs, newInstalledIDs)

    def __onResearchAircraft(self, parentPlaneID):
        self._initNonElite(self.__selectedAircraft.planeID)
        self.__lobby.researchTreeHelper.onAircraftResearch(self.__selectedAircraft.planeID, parentPlaneID, None, self.__onUpdatedEliteAfterResPlane)
        return

    def updatePlanesExperience(self):
        nodes = [ x for x in self.__nodes.itervalues() if x.vo.isAircraft ]
        if self.__selectedAircraft:
            self.__selectedAircraft.vo.aircraftGainedExp = self.__lobbyCarouselHelper.inventory.getAircraftExp(self.__selectedAircraft.planeID)
        for node in nodes:
            node.vo.aircraftGainedExp = self.__lobbyCarouselHelper.inventory.getAircraftExp(node.vo.aircraftID)

        self.__lobby.call_1('moduleTree.updateNodes', [ node.vo for node in nodes ])

    def __onUpdatedEliteAfterResPlane(self, planeID):
        updateNodes = self.__updateNodesResearches()
        node = findIf(self.__nodes.itervalues(), lambda n: n.vo.isAircraft and n.vo.aircraftID == planeID)
        if node:
            node.vo.aircraftGainedExp = self.__lobbyCarouselHelper.inventory.getAircraftExp(node.vo.aircraftID)
            node.vo.isResearched = True
            self.__lobby.call_1('moduleTree.updateNodes', [node.vo])
        if self.__selectedAircraft.planeID == planeID:
            self.__selectedAircraft.isResearched = True
            self.__selectedAircraft.vo.isResearched = True
        else:
            self.__updateAircraftInfoVO()
        self._updateElitePlanes(False)
        self.__lobby.call_1('moduleTree.updateNodes', updateNodes)
        self.__lobby.call_1('moduleTree.updateAircraftInfo', self.__selectedAircraft.vo)

    def __onResearchModule(self, nodeID):
        node = self.__nodes[nodeID]
        if node.upgrade is None:
            LOG_ERROR('Upgrade not found for nodeID {0}'.format(nodeID))
            return
        else:
            self._initNonElite(self.__selectedAircraft.planeID)
            node.vo.isResearched = True
            self.__lobby.call_1('moduleTree.updateNodes', [node.vo])
            BigWorld.player().accountCmd.researchUpgrade(self.__selectedAircraft.planeID, node.upgrade.name, partial(self.__onResearchModuleResponse, node))
            return

    def __onResearchModuleResponse(self, node, operation, returnCode, *args):
        """
        @type operation: SentOperation
        """
        if returnCode == OPERATION_RETURN_CODE.SUCCESS:
            self.__lobbyCarouselHelper.inventory.syncPlaneList(partial(self.__onUpdatedEliteAfterResModule, node, args))
        else:
            LOG_ERROR('Node research failed: {0}'.format(node.upgrade.__dict__))
            node.vo.isResearched = False
            self.__lobby.call_1('moduleTree.updateNodes', [node.vo])

    def __onUpdatedEliteAfterResModule(self, node, args):
        creds, gold, freeExp, planeExp = args
        toResearch = self.__lobbyCarouselHelper.inventory.calculateRequiredUpgradesForUpgrade(node.upgrade, node.upgradeVariant)
        self.__lobbyCarouselHelper.inventory.openUpgrades(toResearch)
        self.__lobbyCarouselHelper.inventory.setAircraftExp(self.__selectedAircraft.planeID, planeExp)
        self.__lobby.call_1('hangar.updateMoneyPanel', creds, gold, freeExp)
        self.__selectedAircraft.vo.gainedExp = planeExp
        self._updateElitePlanes()
        self.__lobby.call_1('moduleTree.updateNodes', self.__updateNodesResearches())
        self.__lobby.call_1('moduleTree.updateAircraftInfo', self.__selectedAircraft.vo)

    def _initNonElite(self, planeID):
        inv = self.__lobbyCarouselHelper.inventory
        self.__nonElite = [ x for x in self.__db.getAircraftList(self.__db.getNationIDbyAircraftID(planeID)) if not inv.isAircraftElite(x) ]

    def __onResearchAircraftNode(self, nodeID, parentPlaneID):
        planeID = self.__nodes[nodeID].vo.aircraftID
        self._initNonElite(planeID)
        self.__lobby.researchTreeHelper.onAircraftResearch(planeID, parentPlaneID, partial(self.__onResearchAircraftNodeResponse, self.__nodes[nodeID]), self.__updateParentsAfterPlaneResearch)

    def __updateParentsAfterPlaneResearch(self, planeID):
        exp = self.__lobbyCarouselHelper.inventory.getAircraftExp(self.__selectedAircraft.planeID)
        self.__selectedAircraft.vo.gainedExp = exp
        self.__lobby.call_1('moduleTree.updateAircraftInfo', self.__selectedAircraft.vo)

    def __onResearchAircraftNodeResponse(self, node, toResearch, returnCode):
        if returnCode == OPERATION_RETURN_CODE.SUCCESS:
            self.__lobbyCarouselHelper.inventory.syncPlaneList(partial(self.__onUpdatedEliteAfterResNode, node, toResearch))

    def __onUpdatedEliteAfterResNode(self, node, toResearch):
        node.vo.isResearched = True
        nodesToUpdate = [node.vo]
        for x in self.__nodes.itervalues():
            if x.vo.isAircraft:
                self.__updatePlaneRequiredResearches(x.vo, x.vo.aircraftID)
                nodesToUpdate.append(x.vo)

        for upgradeName in toResearch:
            for n in self.__nodes.itervalues():
                if n.upgrade and n.upgrade.name == upgradeName:
                    n.vo.isResearched = True
                    nodesToUpdate.append(n.vo)

        self._updateElitePlanes(False)
        self.__lobby.call_1('moduleTree.updateNodes', nodesToUpdate)
        self.__selectedAircraft.vo.isResearchAvailable = self.__selectedAircraft.isResearchAvailable()
        self.__lobby.call_1('moduleTree.updateAircraftInfo', self.__selectedAircraft.vo)

    def _updateElitePlanes(self, showMessage = True):
        if self.__nonElite is None:
            return
        else:
            for node in self.__nodes.itervalues():
                if node.vo.isAircraft and node.vo.aircraftID in self.__nonElite:
                    if self.__lobbyCarouselHelper.inventory.isAircraftElite(node.vo.aircraftID):
                        node.vo.isAircraftElite = True
                        planeData = self.__db.getAircraftData(node.vo.aircraftID)
                        node.vo.aircraftTypeIconPath = PLANE_TYPE_ICO_PATH.icon(planeData.airplane.planeType, PLANE_CLASS.ELITE)
                        self.__lobbyCarouselHelper.refreshAircraftData(node.vo.aircraftID, True)
                        if showMessage:
                            self.__lobby.call_1('hangar.eliteAircraft', node.vo.aircraftID, node.vo.aircraftTypeIconPath, node.vo.name)
                    self.__nonElite.remove(node.vo.aircraftID)

            for planeID in self.__nonElite:
                if self.__lobbyCarouselHelper.inventory.isAircraftElite(planeID):
                    if self.__selectedAircraft is not None and planeID == self.__selectedAircraft.planeID:
                        self.__selectedAircraft.makeElite()
                        self.__selectedAircraft.vo.isElite = True
                        self.__selectedAircraft.vo.iconTypePath = self.__selectedAircraft.planeTypeIconPath
                    self.__lobbyCarouselHelper.refreshAircraftData(planeID, True)
                    if showMessage:
                        planeData = self.__db.getAircraftData(planeID)
                        self.__lobby.call_1('hangar.eliteAircraft', planeID, PLANE_TYPE_ICO_PATH.icon(planeData.airplane.planeType, PLANE_CLASS.ELITE), planeData.airplane.name)

            self.__nonElite = None
            return

    def __getUpgradeGroupName(self, aircraftID, upgrade):
        if upgrade.type in UPGRADE_TYPE.MODULES:
            return localizeComponents(UPGRADE_TYPE.DESCRIPTION_MAP[upgrade.type])
        if upgrade.type in UPGRADE_TYPE.WEAPON:
            return localizeLobby('AMMO_SLOT_' + self.__db.getSlotsWeaponUpgrade(aircraftID, upgrade)[0].name)

    def getSelectedPlaneID(self):
        if self.__selectedAircraft is None:
            return
        else:
            return self.__selectedAircraft.planeID

    def destroy(self):
        self.__lobby = None
        self.__db = None
        self.__selectedAircraft = None
        self.__originPlane = None
        self.__nodes.clear()
        self.__nodes = None
        self.__lobbyCarouselHelper = None
        return