# Embedded file name: scripts/client/gui/Scaleform/ResearchTreeHelper.py
from OperationCodes import OPERATION_RETURN_CODE
import db.DBLogic
from debug_utils import LOG_DEBUG, LOG_ERROR
from Helpers.i18n import localizeAirplane, localizeComponents, localizeLobby, localizeAirplaneLong
from HelperFunctions import findIf
from consts import UPGRADE_TYPE
from clientConsts import PLANE_TYPE_ICO_PATH, DEFAULT_RESEARCH_NATION, HANGAR_MODE, PLANE_CLASS
from functools import partial
from gui.Scaleform.LobbyAirplaneHelper import getLobbyAirplane
from gui.Scaleform.LobbyAirplanePresets import LobbyAirplanePresets
from debug_utils import LOG_NOTE
from Helpers.i18n import localizeUpgrade

class ResearchAircraftVO:

    def __init__(self):
        self.id = 0
        self.longName = ''
        self.icoPath = ''
        self.icoTypePath = ''
        self.description = ''
        self.isResearched = False
        self.isResearchAvailable = False
        self.isBought = False
        self.isElite = False
        self.isPremium = False
        self.reqiuredExperience = 0
        self.reqiuredExperiencePlane = dict()
        self.gotExperience = 0
        self.priceCredits = 0
        self.priceGold = 0
        self.researchedParentID = {}
        self.level = -1
        self.parentName = ''


class ResearchModuleVO:

    def __init__(self):
        self.name = ''
        self.moduleTitle = ''
        self.moduleLongTitle = ''
        self.typeID = -1
        self.level = -1
        self.typeStr = ''
        self.icoPath = ''
        self.isResearched = False
        self.isResearchAvailable = False
        self.isBought = False
        self.isInstalled = False
        self.isInstallAvailable = False
        self.requiredExperience = -1
        self.priceCredits = -1
        self.priceGold = -1
        self.parentName = ''


class ResearchTreeHelper:

    def __init__(self, lobby):
        self.__lobby = lobby
        self.__isInitialized = False
        from BWPersonality import g_lobbyCarouselHelper
        self.__lobbyCarouselHelper = g_lobbyCarouselHelper
        self.enteredInAircraftID = None
        self.__researchPlaneID = None
        return

    def destroy(self):
        self.__lobby = None
        self.__isInitialized = None
        self.__lobbyCarouselHelper = None
        return

    def onInitialized(self):
        LOG_DEBUG('ResearchTreeHelper::onInitialized')
        self.__isInitialized = True
        self.__getPlayerCmd().updatePlayerResources(self.__updatePlayerResourcesResponse)
        if not hasattr(self.__lobby.getPlayer(), 'activeTreeNationID'):
            self.__lobby.getPlayer().activeTreeNationID = self.__lobby.getActiveTreeNationID()
        if self.__lobby.mode == HANGAR_MODE.RESEARCH:
            LOG_DEBUG('research.setActiveTree', self.__lobby.getPlayer().activeTreeNationID)
            self.__lobby.call_1('research.setActiveTree', self.__lobby.getPlayer().activeTreeNationID)

    def onEnteredAircrafID(self, id):
        LOG_DEBUG('onEnteredAircrafID', id)
        self.enteredInAircraftID = id

    def onBackToResearchTree(self):
        self.enteredInAircraftID = None
        return

    def onClose(self):
        self.__isInitialized = False

    def onGetAircraftsDataByNationID(self, nationID):
        LOG_DEBUG('ResearchTreeHelper::getAircraftsData', nationID)
        self.__lobby.setActiveTreeNationID(nationID)
        self.__lobby.getPlayer().activeTreeNationID = nationID
        self.__getAircraftsDataByNationIDResponse(nationID)

    def onAircraftResearch(self, aircraftID, fromAircraftID = None, onResponseCallback = None, onSyncPlaneDataCallback = None):
        LOG_DEBUG('ResearchTreeHelper::onAircraftResearch', aircraftID, fromAircraftID)
        self.__researchPlaneID = aircraftID
        self.__getPlayerCmd().aircraftResearch(aircraftID, fromAircraftID, partial(self.__aircraftResearchResponse, aircraftID, fromAircraftID, onResponseCallback, onSyncPlaneDataCallback))

    def onGetAircraftUpgrades(self, aircraftID):
        LOG_DEBUG('onGetAircraftUpgrades', aircraftID)
        self.__getAircraftUpgradesInfoResponse(aircraftID)

    def onInstalUpgradesPressetOnAircraft(self, upgradeNames, weaponConfigs, aircraftID):
        pass

    def getModulesInfoMap(self, modulesList, useTypeList = []):
        modulesInfoMap = {}
        for moduleMap in modulesList:
            moduleType = moduleMap['type']
            moduleTypeID = UPGRADE_TYPE.STRING_TO_INT_MAP[moduleType]
            if not useTypeList or moduleType in useTypeList:
                modulesInfoMap[moduleTypeID] = localizeLobby(UPGRADE_TYPE.TITLE_MAP[moduleType])

        return modulesInfoMap

    def __getAircraftUpgradesInfoResponse(self, aircraftID):
        customPresetUpgrades = self.__lobbyCarouselHelper.inventory.getCustomPreset(aircraftID)
        presetAvailableList = self.__lobbyCarouselHelper.inventory.getAvailablePresets(aircraftID, True)
        installedPreset = self.__lobbyCarouselHelper.inventory.getInstalledPreset(aircraftID)
        if self.__lobby.mode == HANGAR_MODE.RESEARCH:
            airplane = self.__lobbyCarouselHelper.getCarouselAirplane(aircraftID)
            if not airplane:
                airplane = getLobbyAirplane(aircraftID)
            airplane.presets = LobbyAirplanePresets(airplane.planeID, airplane.modules, airplane.weapons, customPresetUpgrades, presetAvailableList, installedPreset)
            airplane.presets.fillPresets()
            airplane.sendUpgradesListToAS(self.__lobby)

    def __updatePlayerResourcesResponse(self, operation, resultID, *args):
        playerResourcesMap = args[0]
        if self.__lobby.mode == HANGAR_MODE.RESEARCH:
            LOG_NOTE('hangar.updateMoneyPanel', playerResourcesMap['credits'], playerResourcesMap['gold'], playerResourcesMap['experience'])
            self.__lobby.call_1('hangar.updateMoneyPanel', playerResourcesMap['credits'], playerResourcesMap['gold'], playerResourcesMap['experience'])

    def __getAircraftsDataByNationIDResponse(self, nationID):
        aircraftsDataList = self.__lobbyCarouselHelper.inventory.getAircraftsDataByNationID(nationID)
        aircraftsDataASList = []
        for aircraftsDataMap in aircraftsDataList:
            researchAircraftVO = self.__getResearchAircraftVOfromMap(aircraftsDataMap)
            if researchAircraftVO is None:
                continue
            aircraftsDataASList.append(researchAircraftVO)

        if self.__lobby.mode == HANGAR_MODE.RESEARCH:
            LOG_DEBUG('research.setTree')
            self.__lobby.call_1('research.setTree', aircraftsDataASList)
        return

    def __checkEliteStatus(self, planeID, showMsg = True):
        """
        check and message elite status for planeID
        """
        airplaneData = db.DBLogic.g_instance.getAircraftData(planeID)
        if self.__lobbyCarouselHelper.inventory.isAircraftElite(planeID):
            self.__lobbyCarouselHelper.refreshAircraftData(planeID, True)
            if showMsg:
                self.__lobby.call_1('hangar.eliteAircraft', planeID, PLANE_TYPE_ICO_PATH.icon(airplaneData.airplane.planeType, PLANE_CLASS.ELITE), localizeAirplane(airplaneData.airplane.name))

    def __aircraftResearchResponse(self, aircraftID, fromAircraftID, onResponseCallback, onSyncPlaneDataCallback, operation, returnCode, *args):
        toResearch = None
        if returnCode == OPERATION_RETURN_CODE.SUCCESS:
            if self.__lobby.mode == HANGAR_MODE.RESEARCH:
                LOG_DEBUG('@ ResearchTreeHelper::__aircraftResearchResponse', returnCode, aircraftID, fromAircraftID)
                for _parentPlaneID, toResearch, _ in self.__lobbyCarouselHelper.inventory.calculateRequiredUpgradesForAircraft(aircraftID, fromAircraftID):
                    if _parentPlaneID == fromAircraftID:
                        break
                else:
                    toResearch = []

                self.__lobbyCarouselHelper.inventory.openUpgrades(toResearch)
                self.__lobbyCarouselHelper.inventory.openAircraft(aircraftID)
                parentPlaneIDs = self.__lobbyCarouselHelper.inventory.getParentAicraftID(aircraftID)
                if parentPlaneIDs is not None:
                    for planeID in parentPlaneIDs:
                        self.__lobbyCarouselHelper.updateCarouselAirplane(planeID)

                self.__getPlayerCmd().updatePlayerResources(self.__updatePlayerResourcesResponse)
                dbInst = db.DBLogic.g_instance
                nonElite = [ x for x in dbInst.getAircraftList(dbInst.getNationIDbyAircraftID(planeID)) if not self.__lobbyCarouselHelper.inventory.isAircraftElite(x) ]
                self.__lobbyCarouselHelper.inventory.syncPlaneList(partial(self.__onSyncedPlaneList, aircraftID, nonElite, onSyncPlaneDataCallback))
        if onResponseCallback:
            onResponseCallback(toResearch, returnCode)
        return

    def __onSyncedPlaneList(self, planeID, nonElite, callback):
        for x in nonElite:
            self.__checkEliteStatus(x)

        self.reloadCurrentBranch()
        if callback:
            callback(planeID)

    def __getResearchAircraftVOfromMap(self, aircraftsDataMap):
        airplaneID = aircraftsDataMap['id']
        airplaneData = db.DBLogic.g_instance.getAircraftData(airplaneID)
        if airplaneData is None:
            LOG_ERROR('ResearchTreeHelper::__getResearchAircraftVOfromMap. plane is wrong. Airplane = ', airplaneID)
            return
        else:
            shortName = localizeAirplane(airplaneData.airplane.name)
            longName = localizeAirplaneLong(airplaneData.airplane.name)
            if airplaneData.airplane.options.isDev:
                longName = ''.join([longName, ' (Dev)'])
                shortName = ''.join([shortName, ' (Dev)'])
            parentIDs = []
            requiredResearches = dict()
            if not (self.__lobbyCarouselHelper.inventory.isAircraftOpened(airplaneID) or db.DBLogic.g_instance.isPlanePremium(airplaneID)):
                from LobbyModulesTreeHelper import ResearchVO

                def getUpgradeGroupName(planeID, upgrade):
                    if upgrade.type in UPGRADE_TYPE.MODULES:
                        return localizeComponents(UPGRADE_TYPE.DESCRIPTION_MAP[upgrade.type])
                    if upgrade.type in UPGRADE_TYPE.WEAPON:
                        return localizeLobby('AMMO_SLOT_' + db.DBLogic.g_instance.getSlotsWeaponUpgrade(planeID, upgrade)[0].name)

                db_upgrades = db.DBLogic.g_instance.upgrades
                for parentPlaneID, toResearch, _ in self.__lobbyCarouselHelper.inventory.calculateRequiredUpgradesForAircraft(airplaneID, None, onlyResearched=False):
                    parentIDs.append(parentPlaneID)
                    needResources = self.__lobbyCarouselHelper.inventory.calculateRequiredResourcesForUpgradePresset(parentPlaneID, toResearch, [])
                    requiredResearches[parentPlaneID] = [ ResearchVO(localizeUpgrade(db_upgrades[u]), getUpgradeGroupName(parentPlaneID, db_upgrades[u]), needResources[u]['exp']) for u in toResearch ]

            isPremium = aircraftsDataMap['isPremium']
            isElite = aircraftsDataMap['isElite']
            planeStatus = isPremium * PLANE_CLASS.PREMIUM or isElite * PLANE_CLASS.ELITE or PLANE_CLASS.REGULAR
            researchAircraftVO = ResearchAircraftVO()
            researchAircraftVO.id = airplaneID
            researchAircraftVO.longName = longName
            researchAircraftVO.shortName = shortName
            researchAircraftVO.icoTypePath = PLANE_TYPE_ICO_PATH.icon(airplaneData.airplane.planeType, planeStatus)
            researchAircraftVO.icoPath = airplaneData.airplane.treeIconPath if airplaneData.airplane else 'n/a'
            researchAircraftVO.isResearched = aircraftsDataMap['isResearched'] or isPremium
            researchAircraftVO.isResearchAvailable = aircraftsDataMap['isResearchAvailable'] or isPremium
            researchAircraftVO.isBought = aircraftsDataMap['isBought']
            researchAircraftVO.isElite = aircraftsDataMap['isElite']
            researchAircraftVO.isPremium = isPremium
            researchAircraftVO.reqiuredExperience = aircraftsDataMap['reqiuredExperience']
            researchAircraftVO.reqiuredExperiencePlane = aircraftsDataMap['reqiuredExperiencePlane']
            researchAircraftVO.gotExperience = aircraftsDataMap['gotExperience']
            researchAircraftVO.priceCredits = aircraftsDataMap['priceCredits']
            researchAircraftVO.priceGold = aircraftsDataMap['priceGold']
            researchAircraftVO.researchedParentID = aircraftsDataMap['researchedParentID']
            researchAircraftVO.level = airplaneData.airplane.level
            researchAircraftVO.parentName = aircraftsDataMap['parent']
            researchAircraftVO.parentIDs = parentIDs
            researchAircraftVO.blockType = aircraftsDataMap['blockType']
            researchAircraftVO.sellPrice = aircraftsDataMap['sellPrice']
            researchAircraftVO.requiredResearches = requiredResearches
            return researchAircraftVO

    def __reloadAircraftUpgrades(self, aircraftID, operation, resultID, *args):
        self.__lobbyCarouselHelper.refreshSelectedPlane(fromServer=True)
        self.onGetAircraftUpgrades(aircraftID)
        self.__getPlayerCmd().updatePlayerResources(self.__updatePlayerResourcesResponse)

    def reloadCurrentBranch(self):
        if self.__isInitialized:
            self.onGetAircraftsDataByNationID(self.__lobby.getPlayer().activeTreeNationID)

    def __getPlayerCmd(self):
        player = self.__lobby.getPlayer()
        if player is not None:
            return player.accountCmd
        else:
            return