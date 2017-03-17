# Embedded file name: scripts/client/gui/Scaleform/LobbyCarouselHelper.py
from Helpers.ExchangeObBuilder import ExchangeObBuilder
from OperationCodes import OPERATION_RETURN_CODE
import BigWorld
import _airplanesConfigurations_db
import consts
import db.DBLogic
from debug_utils import LOG_DEBUG, LOG_ERROR, LOG_TRACE
from exchangeapi.CommonUtils import METHODTOINDEX, idFromList, splitIDTypeList
from gui.Scaleform.LobbyAirplaneHelper import getAirplaneASList, getLobbyAirplane
from gui.Scaleform.LobbyAirplaneHelper import CAROUSEL_AIRPLANE
from gui.Scaleform.LobbyAirplaneWeapons import LobbyAirplaneWeapons
from gui.Scaleform.LobbyAirplaneModules import LobbyAirplaneModules
from gui.Scaleform.LobbyAirplanePresets import LobbyAirplanePresets
from gui.Scaleform.utils.HangarSpace import g_hangarSpace
from gui.Scaleform.Waiting import Waiting, WaitingFlags
from gui.Scaleform.PartSender import PartSender
from HelperFunctions import findIf
from functools import partial
from clientConsts import PLANE_TYPE_ICO_PATH, HANGAR_MODE, PLANE_CLASS, PLANE_TYPE, HANGAR_LOBBY_WAITING_SCREEN_MESSAGE
from consts import CUSTOM_PRESET_NAME, BLOCK_TYPE, CREW_BODY_TYPE
from SyncOperationKeeper import SyncOperationKeeper, FLAGS_CODE
from exchangeapi.Connectors import getObject
from Helpers.i18n import localizeLobby
from Helpers.cache import deleteFromCache
from exchangeapi.UICallbackUtils import UI_CALLBACKS
from gui.WindowsManager import g_windowsManager
import Settings
from audio import GameSound

class Customization(object):

    def __init__(self, camouflages):
        self.currentCamouflages = camouflages

    def destroy(self):
        self.currentCamouflages = None
        return


class LobbyCarouselHelper:

    def __init__(self):
        self.__lobby = None
        self.__airplanesList = []
        self.__slotsCount = -1
        self.__planeSelected = None
        self.__isCached = False
        self.__upgradesList = None
        self.__installedWeapons = None
        self.inventory = None
        self.__queue = set([])
        self.__isInventoryReady = False
        self.__deferredVehicleInfo = None
        self.__deferredRefresh3DModel = False
        self.__lastPlaneBlockState = False
        self.__deferredUpdatingPlaneIDs = set([])
        self._prizesWindowShown = False
        self._pendingAddList = []
        return

    def prizesWindowShown(self, value):
        self._prizesWindowShown = value
        if not self._prizesWindowShown and self._pendingAddList:
            self.addPendingPlanes()

    def addPendingPlanes(self):
        for x in self._pendingAddList:
            self.addCarouselAirplane(x, True)

        self._pendingAddList = []

    def onLobbyModeChanged(self, mode):
        if mode in (HANGAR_MODE.HOME,
         HANGAR_MODE.MODULES,
         HANGAR_MODE.CUSTOMIZATION,
         HANGAR_MODE.AMMUNITION):
            self.refreshSelectedPlane(False, False)

    def destroy(self):
        self.__lobby = None
        for airplane in self.__airplanesList:
            airplane.destroy()

        self.__deferredVehicleInfo = None
        self.__airplanesList = None
        self.__slotsCount = None
        self.__planeSelected = None
        self.__isCached = None
        self.__upgradesList = None
        self.__installedWeapons = None
        self.inventory = None
        self.__isInventoryReady = None
        return

    def clearQueue(self):
        self.__queue = set([])

    def syncServData(self):
        LOG_TRACE('syncServData')
        if self.inventory is None:
            waitingSyncID = Waiting.show('LOBBY_LOAD_HANGAR_SPACE_VEHICLE', WaitingFlags.WORLD_DRAW_DISABLE)
            from InventoryClient import InventoryClient
            self.inventory = InventoryClient(BigWorld.player().accountCmd, partial(self.onFinishSyncServData, waitingSyncID))
            self.inventory.setOpSender(BigWorld.player().accountCmd)
        BigWorld.player().syncActionList()
        return

    def onFinishSyncServData(self, waitingSyncID):
        LOG_TRACE('onFinishSyncServData')
        self.__isInventoryReady = True
        self.inventory.setFinishCallback(None)
        while len(self.__queue):
            self.__queue.pop()()

        Waiting.hide(waitingSyncID)
        return

    def getAirplanesListRequest(self):
        LOG_DEBUG('getAirplanesListRequest isCached', self.__isCached)
        if self.__isCached:
            self.__sendCarouselDataToAS()
            if self.__lobby is not None:
                self.__lobby.onCarouselLoaded()
        elif not self.__isInventoryReady:
            self.__queue.add(self.__getAirplanesListResponse)
        else:
            self.__getAirplanesListResponse()
        return

    def updateCarouselAirplaneRequest(self, airplaneID):
        if airplaneID == -1:
            return
        BigWorld.player().base.updateCarouselSlotRequest(airplaneID)

    def refreshAircraftData(self, aircraftID, sendASCallbacks):
        """
        Refresh bought aircraft inventory data
        """
        carouselAirplane = self.getCarouselAirplane(aircraftID)
        if carouselAirplane is not None:
            self.__updateCarouselAirplane(carouselAirplane, self.inventory.getCarouselAircraft(aircraftID))
            if sendASCallbacks and self.__lobby is not None:
                self.__lobby.call_1('hangar.updateCarouselSlot', aircraftID, carouselAirplane.getCarouselAirplaneObject())
        return

    def __syncAircraftsData(self, aircraftID, onSyncedCallback, sendASCallbacks = True):
        if aircraftID < 0:
            self.queryRefresh3DModel(None)
            return
        else:
            carouselAirplane = self.getCarouselAirplane(aircraftID)
            if self.__lobby is not None:
                if carouselAirplane:
                    airplane = self.inventory.getCarouselAircraft(aircraftID)
                    self.__updateCarouselAirplane(carouselAirplane, airplane)
                    if self.inventory.isAircraftBought(aircraftID):
                        if carouselAirplane.blockType & BLOCK_TYPE.IN_BATTLE:
                            GameSound().ui.onPlaneBlocked(aircraftID)
                        elif carouselAirplane.blockType == BLOCK_TYPE.UNLOCKED:
                            GameSound().ui.onPlaneUnlocked(aircraftID)
                        if sendASCallbacks:
                            self.__lobby.call_1('hangar.updateCarouselSlot', aircraftID, carouselAirplane.getCarouselAirplaneObject())
                    else:
                        self.inventory.addAircrafttoBoughtList(aircraftID)
                        if sendASCallbacks:
                            LOG_TRACE('Added new plane to carousel: planeID {0}'.format(carouselAirplane.planeID))
                            self.__lobby.call_1('hangar.addPlaneCarousel', carouselAirplane.getCarouselAirplaneObject(), self.airplanesCount())
                            self.__lobby.call_1('hangar.setSelectedAircraftID', aircraftID)
                            self.queryRefresh3DModel(carouselAirplane)
                        SyncOperationKeeper.stop(FLAGS_CODE.BUY_PLANE)
                if self.__lobby.mode == HANGAR_MODE.RESEARCH:
                    if self.__lobby.researchTreeHelper.enteredInAircraftID:
                        pass
                    else:
                        self.__lobby.researchTreeHelper.reloadCurrentBranch()
            if onSyncedCallback is not None:
                onSyncedCallback(aircraftID)
                if self.__lobby is not None and self.__lobby.mode == HANGAR_MODE.AMMUNITION:
                    self.updateSpecs()
            return

    def updateCarouselAirplane(self, aircraftID, onPlaneDataSyncedCallback = None, sendASCallbacks = True, syncData = True, syncStats = True):
        if not self.__isInventoryReady:
            self.__queue.add(partial(self.updateCarouselAirplane, aircraftID, onPlaneDataSyncedCallback, sendASCallbacks, syncData, syncStats))
            return
        elif self.__lobby is None:
            self.__deferredUpdatingPlaneIDs.add(partial(self.updateCarouselAirplane, aircraftID, onPlaneDataSyncedCallback, sendASCallbacks, syncData, syncStats))
            return
        else:
            if syncData:
                self.inventory.syncAircraftsData([aircraftID], partial(self.__syncAircraftsData, aircraftID, onPlaneDataSyncedCallback, sendASCallbacks))
            return

    def processDefferdUpdatingPlaneIDs(self):
        while len(self.__deferredUpdatingPlaneIDs):
            self.__deferredUpdatingPlaneIDs.pop()()

    def updatePlaneAfterBattle(self, aircraftID):
        LOG_TRACE('hangar.updatePlaneAfterBattle', aircraftID)
        if self.__isInventoryReady:
            GameSound().ui.onPLaneReturnFromBattle(aircraftID)
        else:
            self.__queue.add(partial(self.updatePlaneAfterBattle, aircraftID))

    def onRequestRepairPlane(self, planeID = None, imsgid = 0):
        pass

    def setHandler(self, handler):
        self.__lobby = handler

    def getHandler(self):
        return self.__lobby

    def airplanesCount(self):
        return len(self.__airplanesList)

    def getCarouselAirplane(self, airplaneID):
        return findIf(self.__airplanesList, lambda airplane: airplane.planeID == airplaneID)

    def getCarouselAirplaneSelected(self):
        return self.__planeSelected

    def removeCarouselAirplane(self, aircraftID):
        airplane = findIf(self.__airplanesList, lambda airplane: airplane.planeID == aircraftID)
        if airplane is None:
            return
        else:
            self.__airplanesList.remove(airplane)
            self.inventory.removeAircraftFromBoughtList(aircraftID)
            return

    def addCarouselAirplane(self, aircraftID, ignorePrizesWindow = False):
        if self._prizesWindowShown and not ignorePrizesWindow:
            if aircraftID not in self._pendingAddList:
                self._pendingAddList.append(aircraftID)
            return
        else:
            carouselAirplane = getLobbyAirplane(aircraftID)
            carouselAirplane.isBought = True
            if not filter(lambda x: x.planeID == aircraftID, self.__airplanesList):
                self.__airplanesList.append(carouselAirplane)
                self.updateCarouselAirplane(aircraftID, None)
                self.onGetUpgradesList([], aircraftID)
                presetName = self.inventory.getInstalledPreset(aircraftID)
                if presetName == CUSTOM_PRESET_NAME:
                    upgrades = [ upgrade['name'] for upgrade in carouselAirplane.modules.getInstalled() ]
                    gID = db.DBLogic.createGlobalID(carouselAirplane.planeID, upgrades, carouselAirplane.weapons.getInstalledWeaponsList())
                    self.inventory.setCustomPreset(aircraftID, gID)
            return carouselAirplane

    def isCarouselEmpty(self):
        return len(self.__airplanesList) == 0

    def reloadCarousel(self):
        self.__isCached = False
        self.__isInventoryReady = False
        self.inventory.syncAllAircrafts()
        self.getAirplanesListRequest()

    def refreshSelectedPlane(self, fromServer = False, reload3DModel = True):
        selectedPlaneID = -1 if self.__planeSelected is None else self.__planeSelected.planeID
        if fromServer:
            self.updateCarouselAirplaneRequest(selectedPlaneID)
        else:
            self.onSelectedPlaneID(selectedPlaneID, reload3DModel)
        if not reload3DModel:
            self.__refresh3DModel()
        else:
            self.__deferredRefresh3DModel = False
        return

    def onSetAirplanePrimary(self, aircraftID, isPrimary):
        LOG_DEBUG('onSetPrimary', aircraftID, isPrimary)
        BigWorld.player().accountCmd.setSlotPrimary(aircraftID, isPrimary)
        self.inventory.setPrimary(aircraftID, isPrimary)
        self.getCarouselAirplane(aircraftID).isPrimary = isPrimary

    def onSelectedPlaneID(self, planeID, reload3DModel = True):
        LOG_DEBUG('onSelectPlaneID', planeID)
        if planeID == -1:
            self.queryRefresh3DModel(None)
            g_hangarSpace.refreshVehicle(None)
            self.__planeSelected = None
            if self.__lobby is not None:
                LOG_TRACE('onSelectPlaneID() disabling battle button')
                self.__lobby.call_1('hangar.isInBattleEnabled', False)
        BigWorld.player().base.selectActivePlane(planeID)
        self.inventory.setCurrentAircraftID(planeID)
        self.__planeSelected = self.getCarouselAirplane(planeID)
        if self.__planeSelected is not None:
            self.updateInBattleButton()
            self.onGetUpgradesList([], None, reload3DModel)
            self.checkLobbyCrewAnimation()
        return

    def updateInBattleButton(self, additionalCheck = True):
        if self.__lobby is None:
            return
        else:
            from BWPersonality import g_lastBattleType
            from Account import PLANE_BLOCK_TYPE
            trainingCheck = True
            if g_lastBattleType == consts.ARENA_TYPE.TRAINING or self.__lobby.inTrainingRoom:
                _trainHelper = self.__lobby.trainingRoomHelper
                if _trainHelper:
                    trainingCheck = _trainHelper.positionInUI == _trainHelper.TrainingRoomUI.IN_TRAINING_ROOM and _trainHelper.isReadyToButtleForCreator()
            _block = PLANE_BLOCK_TYPE.get(self.__planeSelected.planeID, consts.BLOCK_TYPE.UNLOCKED) if self.__planeSelected else consts.BLOCK_TYPE.UNLOCKED
            isPlaneUnlocked = self.__planeSelected and not _block
            LOG_TRACE('hangar.isInBattleEnabled', isPlaneUnlocked, _block, trainingCheck, self.__planeSelected.planeID if self.__planeSelected else None)
            self.__lobby.call_1('hangar.isInBattleEnabled', additionalCheck and trainingCheck and isPlaneUnlocked)
            return

    def getUpgradesList(self, callbacksList, planeID, reload3DModel):
        LOG_TRACE('getUpgradesList(planeID)', planeID)
        if self.__planeSelected is None and planeID is None:
            return
        else:
            aircraftID = planeID or self.__planeSelected.planeID
            upgradesList = self.inventory.getAircraftUpgradesData(aircraftID)
            installedWeapons = self.inventory.getSlotsConfiguration(aircraftID)
            slotsInfo = self.inventory.getAircraftInstalledWeaponsData(aircraftID)
            customPresetUpgrades = self.inventory.getCustomPreset(aircraftID)
            presetAvailableList = self.inventory.getAvailablePresets(aircraftID, True)
            installedPreset = self.inventory.getInstalledPreset(aircraftID)
            if planeID is not None:
                plane = self.getCarouselAirplane(planeID)
                if plane is None:
                    plane = getLobbyAirplane(planeID)
            else:
                plane = self.__planeSelected
            if plane is None or plane.planeID not in self.inventory.aircraftsData:
                LOG_ERROR('getUpgradesList() error', plane is None, plane is not None and plane.planeID not in self.inventory.aircraftsData)
                return
            plane.modules = LobbyAirplaneModules(plane.planeID, upgradesList)
            plane.weapons = LobbyAirplaneWeapons(plane.planeID, upgradesList, installedWeapons)
            plane.weapons.updateSlotsInfo(slotsInfo)
            plane.presets = LobbyAirplanePresets(plane.planeID, plane.modules, plane.weapons, customPresetUpgrades, presetAvailableList, installedPreset)
            plane.presets.fillPresets()
            plane.partTypes = plane.modules.getPartTypes()
            if planeID is None:
                if reload3DModel:
                    self.queryRefresh3DModel(self.__planeSelected)
                self.sendUpgradesListToAS()
            for callback in callbacksList:
                callback()

            return

    def __refresh3DModel(self):
        from Account import PLANE_BLOCK_TYPE
        vehicleInfo = self.__deferredVehicleInfo
        if vehicleInfo is not None:
            LOG_TRACE('__refresh3DModel() block type is {0} for {1}'.format(PLANE_BLOCK_TYPE.get(vehicleInfo.planeID, -1), vehicleInfo.planeID))
        planeBlocked = vehicleInfo and PLANE_BLOCK_TYPE.get(vehicleInfo.planeID, consts.BLOCK_TYPE.UNLOCKED) & consts.BLOCK_TYPE.IN_BATTLE
        if not self.__deferredRefresh3DModel and not self.__lastPlaneBlockState:
            return
        else:
            self.__lastPlaneBlockState = planeBlocked
            self.__deferredRefresh3DModel = False
            vehicleInfo = None if planeBlocked else vehicleInfo
            if vehicleInfo is None:
                g_hangarSpace.refreshVehicle(None)
            else:

                def _onResponse(vehicleInfo, obj):
                    if vehicleInfo.blockType & BLOCK_TYPE.IN_BATTLE:
                        LOG_ERROR('Cannot refresh plane {0}. Plane locked'.format(vehicleInfo.planeID))
                    elif not isinstance(obj, basestring):
                        if self.__deferredVehicleInfo == vehicleInfo:
                            dec = self.__getDecalByKills(obj[0][0]['IPlaneStats']['row'])
                            vehicleInfo.decalPKills = dec[0]
                            vehicleInfo.decalSKills = dec[1]
                            vehicleInfo.customization = Customization(obj[0][0]['IInstalledCamouflage']['ids'])
                            vehicleInfo.planeBirthdayOb = obj[0][0]['IPlaneBirthday']
                            g_hangarSpace.refreshVehicle(vehicleInfo)
                            self.__deferredVehicleInfo = None
                    else:
                        LOG_ERROR('__refresh3DModel::_onResponse. obj error: {0}'.format(obj))
                    return

                accountUI = g_windowsManager.getAccountUI()
                if accountUI:
                    accountUI.viewIFace([[{'IPlaneStats': {},
                       'IInstalledCamouflage': {},
                       'IPlaneBirthday': {}}, [[vehicleInfo.planeID, 'plane']]]], dbgCallback=partial(_onResponse, vehicleInfo))
            return

    def __getDecalByKills(self, stats):
        decalKill = [0, 0]
        myKills = stats['totalKilled']
        myKills = 0 if myKills is None else myKills
        sKills = stats['totalGroundObjectsDestroyed']
        myKills += stats['bonusKill'][0]
        sKills += stats['bonusKill'][1]
        for dKilld in consts.DECAL_BY_KILLS:
            if myKills >= dKilld:
                decalKill[0] += 1
            else:
                break

        for dBased in consts.DECAL_BY_TEAM_OBJECTS_DESTROYED:
            if sKills >= dBased:
                decalKill[1] += 1
            else:
                break

        return decalKill

    def queryRefresh3DModel(self, vehicleInfo, defer = False, force = False):
        LOG_DEBUG('queryRefresh3DModel', vehicleInfo.partTypes if vehicleInfo else None)
        self.__deferredVehicleInfo = vehicleInfo
        self.__deferredRefresh3DModel = True
        if not defer:
            if force:
                self.__lastPlaneBlockState = True
            if self.__lobby and (self.__lobby.mode in HANGAR_MODE.REFRESH_MODEL_MODES or force):
                self.__refresh3DModel()
        return

    def onGetUpgradesList(self, callbacksList = [], planeID = None, reload3DModel = True):
        if not self.__isInventoryReady:
            self.__queue.add(partial(self.onGetUpgradesList, callbacksList, planeID, reload3DModel))
            return
        self.getUpgradesList(callbacksList, planeID, reload3DModel)

    def getPreset(self, presetName, planeID):
        plane = self.getCarouselAirplane(planeID)
        if plane is None:
            plane = getLobbyAirplane(planeID)
        return plane.presets.findPreset(presetName)

    def onInstallAircraftConfiguration(self, globalID, callback):
        LOG_DEBUG('@ onInstallAircraftConfiguration (globalID)'.format(globalID))
        BigWorld.player().accountCmd.installPresetOnAircraft(globalID, partial(self.__installAircraftConfigurationResp, globalID, callback))
        self.__setInstalledPreset(globalID)

    def __installAircraftConfigurationResp(self, globalID, callback, operation, resultID, *args):
        if resultID != OPERATION_RETURN_CODE.SUCCESS:
            aircraftConfig = _airplanesConfigurations_db.getAirplaneConfiguration(globalID)
            planeID = aircraftConfig.planeID
            self.inventory.setFinishCallback(partial(self.__onRollBackPresset, planeID, callback, operation, resultID, *args))
            self.inventory.syncInventoryData()
            self.inventory.syncAircraftsData([planeID])
        else:
            callback(operation, resultID, *args)

    def __onRollBackPresset(self, planeID, callback, operation, resultID, *args):
        self.inventory.setFinishCallback(None)
        self.onSelectedPlaneID(planeID)
        callback(operation, resultID, *args)
        return

    def onGetAirplaneDescription(self, planeID):
        LOG_DEBUG('onGetAirplaneDescription', planeID)
        self.onGetUpgradesList([partial(self.sendDescriptionToAS, planeID)], planeID)

    def sendDescriptionToAS(self, planeID):
        airplane = self.getCarouselAirplane(planeID)
        if airplane is None:
            airplane = getLobbyAirplane(planeID)
        if self.__lobby is not None:
            isElite = self.inventory.isAircraftElite(planeID)
            isPremium = db.DBLogic.g_instance.isPlanePremium(planeID)
            planeStatus = isPremium * PLANE_CLASS.PREMIUM or isElite * PLANE_CLASS.ELITE or PLANE_CLASS.REGULAR
            shouldInstallRocketsOrBombs = airplane.weapons.canInstallBombsOrRockets() and airplane.planeType == PLANE_TYPE.ASSAULT
            isEffectiveAgainstArmoredObjects = 3 if shouldInstallRocketsOrBombs else 0
            for slotID, configID in airplane.weapons.getInstalledWeaponsList():
                weaponInfo = db.DBLogic.g_instance.getWeaponInfo(airplane.planeID, slotID, configID)
                if weaponInfo and weaponInfo[0] in [consts.UPGRADE_TYPE.BOMB, consts.UPGRADE_TYPE.ROCKET]:
                    isEffectiveAgainstArmoredObjects = 2
                    break
                if weaponInfo and weaponInfo[0] == consts.UPGRADE_TYPE.GUN:
                    gunData = db.DBLogic.g_instance.getGunData(weaponInfo[1])
                    if gunData.caliber >= consts.MIN_CALIBER:
                        isEffectiveAgainstArmoredObjects = 4 if shouldInstallRocketsOrBombs else 1

            self.__lobby.call_1('hangar.planeInfoResponse', planeID, airplane.getHangarDescriptionFields(True), None, airplane.getMainDescription(), airplane.longName, airplane.type, airplane.level, PLANE_TYPE_ICO_PATH.icon(airplane.planeType, planeStatus), isEffectiveAgainstArmoredObjects)
        return

    def onRepairPlaneResponse(self, resultID, planeID):
        LOG_DEBUG('onRepairPlaneResponse', resultID, planeID, self.__lobby)
        if resultID == 0 and self.__lobby:
            self.updateCarouselAirplaneRequest(planeID)
            self.__lobby.updateMoneyPanelRequest()
            self.queryRefresh3DModel(self.__planeSelected, True)

    def onPreviewPreset(self, presetName, planeID, onlyDescription = False):
        LOG_DEBUG('onPreviewPreset', onlyDescription)
        self.isPreviewPreset = True
        plane = self.getCarouselAirplane(planeID)
        if plane is None:
            plane = getLobbyAirplane(planeID)
        preset = plane.presets.findPreset(presetName)
        if preset is not None:
            self.previewPreset(plane, preset.modulesList, preset.weaponsList, onlyDescription)
        else:
            LOG_ERROR("couldn't find preset")
        return

    def getAirplaneBySlotID(self, slotID):
        return self.__airplanesList[slotID]

    def __sendCarouselDataToAS(self, selectedAircraftID = -1):
        LOG_DEBUG('Sending planes to flash')
        waitingID = Waiting.show('LOBBY_LOAD_HANGAR_SPACE_VEHICLE')
        airplanesASList = getAirplaneASList(self.__airplanesList, CAROUSEL_AIRPLANE)
        nOrd = [0] + [ country.id for country in sorted(db.DBLogic.g_instance.aircrafts.country, cmp=lambda x, y: cmp(x.priority, y.priority)) ]
        airplanesASList.sort(key=lambda elem: (-elem.isPrimary,
         nOrd[elem.nationID],
         elem.level,
         elem.planeType))
        selectedPlaneID = selectedAircraftID if self.__planeSelected is None else self.__planeSelected.planeID
        if self.__lobby is not None:
            self.__lobby.call_1('hangar.removeCarouselPlanes')
            PartSender().clearPool(PartSender.POOL_TYPE_CAROUSEL_AIRPLANES)
            PartSender().addToPool(PartSender.POOL_TYPE_CAROUSEL_AIRPLANES, airplanesASList)
            PartSender().setPartSize(PartSender.POOL_TYPE_CAROUSEL_AIRPLANES, PartSender.DEFAULT_PART_SIZE)
            PartSender().setRemoveFromPoolCallback(PartSender.POOL_TYPE_CAROUSEL_AIRPLANES, self.__partCallback)
            PartSender().setFinishCallback(PartSender.POOL_TYPE_CAROUSEL_AIRPLANES, partial(self.__finishCallback, waitingID))
            PartSender().removeFromPool(PartSender.POOL_TYPE_CAROUSEL_AIRPLANES)
            self.__lobby.call_1('hangar.setSelectedAircraftID', selectedPlaneID)
        return

    def getNextAircraftsPart(self):
        PartSender().removeFromPool(PartSender.POOL_TYPE_CAROUSEL_AIRPLANES)

    def __partCallback(self, aircraftsList):
        if self.__lobby is not None:
            self.__lobby.call_1('hangar.addCarouselPlanes', aircraftsList)
        return

    def __finishCallback(self, waitingID):
        LOG_DEBUG('Sending planes to flash finished')
        if self.__lobby is not None:
            self.__lobby.call_1('hangar.planesTransferFinished')
        Waiting.hide(waitingID)
        return

    def __getAirplanesListResponse(self):
        """ See CAROUSEL_DATA in alias.xml for actual data """
        carouselList = self.inventory.getCarouselAircrafts()
        self.__airplanesList = []
        for airplane in carouselList:
            carouselAirplane = getLobbyAirplane(airplane['plane'])
            self.__updateCarouselAirplane(carouselAirplane, airplane)
            self.__airplanesList.append(carouselAirplane)

        self.__isCached = True
        self.__slotsCount = self.inventory.getSlotCount()
        aircraftID = self.inventory.getCurrentAircraftID() or -1
        self.__sendCarouselDataToAS(aircraftID)
        if self.__lobby is not None:
            self.__lobby.onCarouselLoaded()
        return

    def sendUpgradesListToAS(self, planeID = None):
        LOG_DEBUG('sendUpgradesListToAS called', planeID)
        if self.__lobby is None or self.__lobby.mode != HANGAR_MODE.HOME and self.__lobby.mode != HANGAR_MODE.RESEARCH:
            return
        else:
            planeID = planeID or self.__lobby.researchTreeHelper.enteredInAircraftID
            if planeID is not None:
                plane = self.getCarouselAirplane(planeID)
                if plane is None:
                    plane = getLobbyAirplane(planeID)
                if self.__lobby.researchTreeHelper.enteredInAircraftID:
                    plane.sendUpgradesListToAS(self.__lobby)
            else:
                if self.__planeSelected is None:
                    LOG_ERROR('Plane object is None')
                    return
                if self.__planeSelected.modules is None or self.__planeSelected.weapons is None or self.__planeSelected.presets is None:
                    self.onGetUpgradesList()
                else:
                    self.__planeSelected.sendUpgradesListToAS(self.__lobby)
            return

    def __installWeaponResponse(self, operation, resultID, *args):
        """
        @type operation: ReceivedOperation
        """
        LOG_DEBUG('installWeaponResponse', operation.invocationId, resultID, args)
        self.onGetUpgradesList()

    def __setInstalledPreset(self, globalID):
        if self.__lobby is not None:
            self.__lobby.updateMoneyPanelRequest()
            aircraftConfig = _airplanesConfigurations_db.getAirplaneConfiguration(globalID)
            upgDict = self.inventory.getPresetRequiredUpgrades(aircraftConfig.planeID, aircraftConfig.modules, aircraftConfig.weaponSlots)
            self.inventory.addRequiredUpgrades(upgDict)
            self.inventory.installAircraftConfiguration(globalID)
            if self.__lobby.mode == HANGAR_MODE.RESEARCH or self.__lobby.mode == HANGAR_MODE.MODULES:
                self.onGetUpgradesList([], aircraftConfig.planeID, reload3DModel=False)
                self.__lobby.researchTreeHelper.onGetAircraftUpgrades(aircraftConfig.planeID)
        return

    def __getSlotIDByAirplaneID(self, airplaneID):
        return self.__airplanesList.index(self.getCarouselAirplane(airplaneID))

    def __updateCarouselAirplane(self, carouselAirplane, airplane):
        if carouselAirplane is None:
            LOG_ERROR('Airplane not found', airplane['plane'])
            return
        elif airplane is None:
            return
        else:
            LOG_TRACE('__updateCarouselAirplane() setting block type {0} for {1}'.format(airplane['blockType'], carouselAirplane.planeID))
            from Account import PLANE_BLOCK_TYPE
            PLANE_BLOCK_TYPE[carouselAirplane.planeID] = airplane['blockType']
            carouselAirplane.blockType = airplane['blockType']
            carouselAirplane.repairCost = airplane['repairCost']
            carouselAirplane.experience = airplane['planeXP']
            carouselAirplane.isPrimary = airplane['isPrimary']
            carouselAirplane.autoRepair = airplane['autoRepair']
            carouselAirplane.autoRefill = airplane['autoRefill']
            if carouselAirplane.weapons is not None:
                carouselAirplane.weapons.setInstalledWeapons(airplane['weaponsSlot'])
            if carouselAirplane.modules is not None:
                carouselAirplane.modules.setInstalledModules(airplane['modules'])
            carouselAirplane.sellPrice = airplane['sellPrice']
            carouselAirplane.isPremium = airplane['isPremium']
            carouselAirplane.isElite = airplane['isElite']
            carouselAirplane.extraExperience = airplane['dailyFirstWinXPFactor']
            carouselAirplane.extraRemains = airplane['dailyFirstWinRemains']
            carouselAirplane.isBought = True
            return

    def updateSpecs(self):
        if self.__lobby is None:
            return
        else:
            selectedPlane = self.getCarouselAirplaneSelected()
            if selectedPlane:
                selectedPlane.clearSpecsTable()
                globalID = self.inventory.getInstalledUpgradesGlobalID(selectedPlane.planeID)
                player = self.__lobby.getPlayer()
                if player is not None:
                    from exchangeapi.ErrorCodes import SUCCESS
                    idTypeList = [[globalID, 'planePreset'], [Settings.g_instance.gameUI['measurementSystem'], 'measurementSystem']]
                    player.responseSender(idTypeList, 'IConfigSpecs', getObject(idTypeList), SUCCESS, 'view')
                    idTypeList = [[globalID, 'planePreset']]
                    player.responseSender(idTypeList, 'IShortConfigSpecs', getObject(idTypeList), SUCCESS, 'view')
            return

    def setPlaneBlockType(self, planeID, blockType):
        if self.__isInventoryReady:
            self.inventory.setPlaneBlockType(planeID, blockType)
        else:
            self.__queue.add(partial(self.setPlaneBlockType, planeID, blockType))

    def invalidateQuestList(self, planeID = None):

        def _invalidate(planeIDs):
            ifacename = 'IQuestList'
            accountUI = g_windowsManager.getAccountUI()

            def data():
                for planeID in planeIDs:
                    idTypeList = [[planeID, 'plane']]
                    deleteFromCache(idTypeList, ifacename)
                    ids, types = map(idFromList, splitIDTypeList(idTypeList))
                    if accountUI and set(UI_CALLBACKS.get(ids, {}).get(types, {}).get(ifacename, [])):
                        yield [{ifacename: {}}, idTypeList]

            request = list(data())
            if request:
                accountUI.viewIFace(request)

        if planeID is not None:
            _invalidate([planeID])
        _invalidate((plane.planeID for plane in self.__airplanesList))
        return

    @property
    def isInventoryReady(self):
        return self.__isInventoryReady

    def checkLobbyCrewAnimation(self):
        from Helpers.cache import getFromCache
        from BWPersonality import g_lobbyCrewBodyType, g_lobbyCrewLastNationID
        from _specializations_data import SpecializationEnum
        from _skills_data import SkillDB
        selectedPlane = self.getCarouselAirplaneSelected()
        if not selectedPlane:
            BigWorld.sendVisualScriptEvent('HANGAR_PILOT_BODY', dict(nation_id=0, body_type=0, icon_id=0))
            return
        idTypeList = [[selectedPlane.planeID, 'plane']]
        ob = getFromCache(idTypeList, 'IPlaneCrew')
        nationID = db.DBLogic.g_instance.getPlaneNationID(selectedPlane.planeID)
        if ob:
            bodyParam = dict(nation_id=nationID, body_type=CREW_BODY_TYPE.MALE, icon_id=1)
            pilotCrew = [-1, 0]
            for planeCrew in ob['crewMembers']:
                memberID, specSkill = planeCrew['id'], planeCrew['specialization']
                if specSkill != SkillDB[specSkill].mainForSpecialization != SpecializationEnum.PILOT:
                    continue
                idTypeList = [[memberID, 'crewmember']]
                member = getFromCache(idTypeList, 'ICrewMember')
                if member:
                    nationID = db.DBLogic.g_instance.getPlaneNationID(member['planeSpecializedOn'])
                    bodyType = member['bodyType']
                    icoIndex = member['icoIndex']
                    pilotCrew = [bodyType, icoIndex]
                    bodyParam = dict(nation_id=nationID, body_type=bodyType, icon_id=icoIndex)

            if g_lobbyCrewBodyType[0][SpecializationEnum.PILOT] != pilotCrew or g_lobbyCrewLastNationID != nationID:
                g_lobbyCrewBodyType[0][SpecializationEnum.PILOT] = pilotCrew
                import BWPersonality
                BWPersonality.g_lobbyCrewLastNationID = nationID
                LOG_DEBUG('EVENT: HANGAR_PILOT_BODY', bodyParam)
                BigWorld.player().callVSE('HANGAR_PILOT_BODY', bodyParam)