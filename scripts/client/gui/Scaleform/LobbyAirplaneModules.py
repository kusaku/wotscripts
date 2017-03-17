# Embedded file name: scripts/client/gui/Scaleform/LobbyAirplaneModules.py
import db.DBLogic
import operator
from debug_utils import LOG_DEBUG, LOG_INFO, LOG_ERROR
from consts import UPGRADE_TYPE
from HelperFunctions import findIf, findSuitableIndex
from Helpers.i18n import localizeHUD, localizeComponents
from _airplanesConfigurations_db import getAirplaneConfiguration

class LobbyAirplaneModules(object):

    def __init__(self, aircraftID, upgradesList):
        self.__aircraftID = aircraftID
        self.__modulesList = filter(lambda upgrade: upgrade['type'] in UPGRADE_TYPE.MODULES, upgradesList)

    def destroy(self):
        self.__aircraftID = None
        self.__modulesList = None
        return

    def getInstalled(self):
        return filter(lambda module: module['isInstalled'], self.__modulesList)

    def setInstalledModules(self, moduleNameList):
        for m in self.__modulesList:
            m['isInstalled'] = m['name'] in moduleNameList

    def getAll(self):
        return self.__modulesList

    def getSortedModules(self):
        dbInstance = db.DBLogic.g_instance
        settings = dbInstance.getAircraftData(self.__aircraftID)
        planeName = dbInstance.getAircraftName(self.__aircraftID)

        def sortModules(module):
            if 'level' not in module:
                return (0, 0, 0)
            elif 'type' not in module:
                return (module['level'], 0, 0)
            upgrade = dbInstance.upgrades.get(module['name'], None)
            if module['type'] == UPGRADE_TYPE.PLANER or module['type'] == UPGRADE_TYPE.TURRET:
                return (module['level'], 0, upgrade.id)
            elif module['type'] == UPGRADE_TYPE.ENGINE:
                upgradeVariantIndex = findSuitableIndex(upgrade.variant, lambda v: v.aircraftName == planeName)
                if upgradeVariantIndex is None:
                    return (module['level'], 0, upgrade.id)
                partName = findIf(upgrade.variant[upgradeVariantIndex].logicalPart, lambda p: p.type == module['type']).name
                value = 0
                for eng in filter(lambda m: m.name == partName, settings.airplane.flightModel.engine):
                    value = eng.power if hasattr(eng, 'power') else eng.thrust
                    break

                return (module['level'], value, upgrade.id)
            else:
                return (module['level'], 0, 0)

        self.__modulesList.sort(key=sortModules)
        return self.__modulesList

    def getPartTypes(self, moduleNamesList = None):
        from BWPersonality import g_lobbyCarouselHelper
        inv = g_lobbyCarouselHelper.inventory
        if inv.isAircraftBought(self.__aircraftID):
            aircraftConfiguration = getAirplaneConfiguration(g_lobbyCarouselHelper.inventory.getInstalledUpgradesGlobalID(self.__aircraftID))
            return aircraftConfiguration.partTypes
        return []