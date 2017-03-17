# Embedded file name: scripts/client/gui/Scaleform/LobbyShopHelper.py
from OperationCodes import OPERATION_RETURN_CODE
import BigWorld
import db.DBLogic
import operator
from gui.Scaleform.LobbyAirplaneHelper import getAirplaneASList
from gui.Scaleform.LobbyAirplaneHelper import SHOP_AIRPLANE
from gui.Scaleform.LobbyAirplaneHelper import getLobbyAirplane
from gui.Scaleform.LobbyAirplaneWeapons import LobbyAirplaneWeapons
from gui.Scaleform.LobbyAirplaneModules import LobbyAirplaneModules
from gui.Scaleform.Waiting import Waiting
from HelperFunctions import findIf
from debug_utils import LOG_DEBUG, LOG_ERROR
from clientConsts import HANGAR_MODE
from functools import partial
from SyncOperationKeeper import SyncOperationKeeper, FLAGS_CODE
from Helpers.i18n import localizeOptions, localizeMessages, localizeLobby, localizeAirplane

class LobbyShopHelper:

    def __init__(self, lobby):
        self.__lobby = lobby
        self.__shopAirplaneList = None
        self.__selectedNationID = None
        self.__selectedPlaneType = None
        from BWPersonality import g_lobbyCarouselHelper
        self.__lobbyCarouselHelper = g_lobbyCarouselHelper
        self.__planeIndex = 0
        return

    def destroy(self):
        self.__lobby = None
        self.__shopAirplaneList = None
        self.__selectedNationID = None
        self.__selectedPlaneType = None
        self.__lobbyCarouselHelper = None
        return

    def onGetShopAirlanesRequest(self, nationID, planeType):
        LOG_DEBUG('Lobby::getShopAirlanesRequest', nationID, planeType)
        if nationID is None or planeType is None:
            return
        else:
            self.__selectedNationID = nationID
            self.__selectedPlaneType = planeType
            if self.__shopAirplaneList is None:
                self.getShopAirplanesResponse(OPERATION_RETURN_CODE.SUCCESS, self.__lobbyCarouselHelper.inventory.getShopAircrafts(nationID, planeType))
            else:
                self.getShopAirplanesResponse(OPERATION_RETURN_CODE.SUCCESS)
            return

    def getShopAirplanesResponse(self, resultID, airplanesList = []):
        if self.__shopAirplaneList is None:
            self.__shopAirplaneList = []
            for airplaneMap in airplanesList:
                airplane = getLobbyAirplane(airplaneMap['airplaneID'])
                airplane.price = airplaneMap['price']
                airplane.gold = airplaneMap['gold']
                airplane.isResearched = airplaneMap['isResearched']
                airplane.experience = airplaneMap['planeXP']
                airplane.modules = LobbyAirplaneModules(airplaneMap['airplaneID'], airplaneMap['defaultModulesList'])
                airplane.weapons = LobbyAirplaneWeapons(airplaneMap['airplaneID'], None, airplaneMap['defaultWeaponsMap'])
                airplane.isPremium = airplaneMap['isPremium']
                airplane.isElite = airplaneMap['isElite']
                if airplane is None:
                    LOG_ERROR('Airplane not found', airplaneMap['airplaneID'])
                    continue
                self.__shopAirplaneList.append(airplane)

        self.__shopAirplaneList.sort(key=operator.attrgetter('level', 'type', 'price'))
        airplaneASList = getAirplaneASList(self.__shopAirplaneList, SHOP_AIRPLANE)
        if self.__lobby.mode == HANGAR_MODE.STORE:
            self.__lobby.call_1('shop.updateShopPlanes', airplaneASList)
        return

    def onUpdateShopAirplaneDescription(self, shopAirplaneIndex):
        LOG_DEBUG('Lobby:onUpdateShopAirplaneDescription', shopAirplaneIndex)
        if self.__shopAirplaneList is None:
            return
        elif shopAirplaneIndex < 0 or shopAirplaneIndex >= len(self.__shopAirplaneList):
            LOG_ERROR('Lobby::onUpdateShopAirplaneDescription. slotID out of range')
            return
        else:
            shopAirplane = self.__shopAirplaneList[shopAirplaneIndex]
            descriptionFieldList = shopAirplane.getHangarDescriptionFields(True)
            descriptionMain = shopAirplane.getMainDescription()
            if self.__lobby.mode == HANGAR_MODE.STORE:
                self.__lobby.call_1('shop.updateDescription', descriptionFieldList, shopAirplane.longName, descriptionMain, shopAirplane.planeIconPath, shopAirplane.nationFlagPath)
            return

    def getShopAirplane(self, airplaneID):
        return findIf(self.__shopAirplaneList, lambda airplane: airplane.planeID == airplaneID)

    def __buyPlaneResponse(self, resultID, airplaneID):
        if resultID == 0 and self.__lobbyCarouselHelper.inventory.getAircraftPData(airplaneID):
            self.__lobbyCarouselHelper.addCarouselAirplane(airplaneID)
            if self.__shopAirplaneList is not None:
                airplane = self.getShopAirplane(airplaneID)
                self.__shopAirplaneList.remove(airplane)
            self.__lobby.updateMoneyPanelRequest()
            self.__lobby.planeLoaded(airplaneID)
        else:
            SyncOperationKeeper.stop(FLAGS_CODE.BUY_PLANE)
        if self.__lobby.mode == HANGAR_MODE.STORE:
            pass
        return

    def onBuyPlaneResponse(self, resultID, aircraftID):
        """see AccountCommands.py for actual resultID format"""
        LOG_DEBUG('onBuyPlaneResponse', aircraftID, resultID)
        self.__lobbyCarouselHelper.inventory.syncAircraftsData([aircraftID], partial(self.__buyPlaneResponse, resultID, aircraftID))

    def __sellPlaneResponse(self, resultID, aircraftID):
        self.__lobby.call_1('hangar.removePlaneCarousel', aircraftID)
        self.reloadShop()
        self.__lobby.researchTreeHelper.reloadCurrentBranch()
        self.__lobby.updateMoneyPanelRequest()
        if SyncOperationKeeper.getFlagStatus(FLAGS_CODE.SELL_PLANE):
            self.__lobby.call_1('shop.sellPlaneResponse', resultID)
            SyncOperationKeeper.stop(FLAGS_CODE.SELL_PLANE)

    def onSellPlaneResponse(self, resultID, aircraftID):
        """see AccountCommands.py for actual resultID format"""
        LOG_DEBUG('shop.sellPlaneResponse', resultID)
        if resultID == OPERATION_RETURN_CODE.SUCCESS:
            self.__lobbyCarouselHelper.removeCarouselAirplane(aircraftID)
            self.__lobbyCarouselHelper.inventory.syncAircraftsData([aircraftID], partial(self.__sellPlaneResponse, resultID, aircraftID))
        else:
            if SyncOperationKeeper.getFlagStatus(FLAGS_CODE.SELL_PLANE):
                self.__lobby.call_1('shop.sellPlaneResponse', resultID)
                SyncOperationKeeper.stop(FLAGS_CODE.SELL_PLANE)
            if resultID == OPERATION_RETURN_CODE.FAILURE_MAX_SOLD_PLANES_PER_DAY_REACHED:
                msgHeader = localizeMessages('SYSTEM_MESSAGE_ERROR_HEADER')
                planeName = localizeAirplane(db.DBLogic.g_instance.getAircraftName(aircraftID))
                msgData = localizeLobby('LOBBY_ERROR_SELL_LIMIT', plane=planeName)
                self.__lobby.showMessageBox(msgHeader, msgData, localizeOptions('SAVE_SETTINGS_BUTTON'), None, None, None, False)
        return

    def reloadShop(self):
        self.__shopAirplaneList = None
        if self.__lobby.mode == HANGAR_MODE.STORE:
            self.onGetShopAirlanesRequest(self.__selectedNationID, self.__selectedPlaneType)
        return

    def __getShopAirplaneByID(self, aircraftID):
        if self.__shopAirplaneList is None:
            return
        else:
            for airplane in self.__shopAirplaneList:
                if airplane.planeID == aircraftID:
                    return airplane

            return