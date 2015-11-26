# Embedded file name: scripts/client/gui/customization_2_0/elements/available.py
import Math
from gui.shared import g_itemsCache
from helpers.i18n import makeString as _ms
from CurrentVehicle import g_currentVehicle

class Item(object):
    __slots__ = ('_qualifier', '_rawData', '_price', '__isInDossier', '__itemID', '__allowedVehicles', '__notAllowedVehicles')

    def __init__(self, itemID, rawData, qualifier, isInDossier, allowedVehicles, notAllowedVehicles):
        self.__isInDossier = isInDossier
        self.__itemID = itemID
        self.__allowedVehicles = allowedVehicles
        self.__notAllowedVehicles = notAllowedVehicles
        self._qualifier = qualifier
        self._rawData = rawData

    def getID(self):
        return self.__itemID

    def getTexturePath(self):
        raise NotImplementedError

    def getGroup(self):
        raise NotImplementedError

    def getName(self):
        raise NotImplementedError

    def getDescription(self):
        raise NotImplementedError

    def getIgrType(self):
        raise NotImplementedError

    @property
    def isInShop(self):
        raise NotImplementedError

    @property
    def isAllowedForCurrentVehicle(self):
        intCD = g_currentVehicle.item.intCD
        if not self.__allowedVehicles and not self.__notAllowedVehicles:
            return True
        if self.__allowedVehicles and intCD in self.__allowedVehicles:
            return True
        if self.__notAllowedVehicles and intCD not in self.__notAllowedVehicles:
            return True
        return False

    @property
    def isInDossier(self):
        return self.__isInDossier

    @property
    def qualifier(self):
        return self._qualifier

    def priceIsGold(self, duration):
        return not duration


class Emblem(Item):

    def __init__(self, itemID, rawData, qualifier, isInDossier, allowedVehicles, notAllowedVehicles):
        Item.__init__(self, itemID, rawData, qualifier, isInDossier, allowedVehicles, notAllowedVehicles)
        self._price = g_itemsCache.items.shop.playerEmblemCost

    def getTexturePath(self):
        return self._rawData[2].replace('gui/maps', '../maps')

    def getGroup(self):
        return self._rawData[0]

    def getName(self):
        return self._rawData[4]

    def getDescription(self):
        return self._qualifier.getDescription()

    def getIgrType(self):
        return self._rawData[1]

    @property
    def isInShop(self):
        return self.getGroup() not in g_itemsCache.items.shop.getEmblemsGroupHiddens()

    def getPrice(self, duration):
        return int(round(self._price[duration][0] * g_currentVehicle.item.level * g_itemsCache.items.shop.getEmblemsGroupPriceFactors()[self.getGroup()]))


class Inscription(Item):

    def __init__(self, itemID, rawData, qualifier, isInDossier, allowedVehicles, notAllowedVehicles):
        Item.__init__(self, itemID, rawData, qualifier, isInDossier, allowedVehicles, notAllowedVehicles)
        self._price = g_itemsCache.items.shop.playerInscriptionCost

    def getTexturePath(self):
        return self._rawData[2].replace('gui/maps', '../maps')

    def getGroup(self):
        return self._rawData[0]

    def getName(self):
        return self._rawData[4]

    def getDescription(self):
        return self._qualifier.getDescription()

    def getIgrType(self):
        return self._rawData[1]

    @property
    def isInShop(self):
        return self.getGroup() not in g_itemsCache.items.shop.getInscriptionsGroupHiddens(g_currentVehicle.item.nationID)

    def getPrice(self, duration):
        return int(round(self._price[duration][0] * g_currentVehicle.item.level * g_itemsCache.items.shop.getInscriptionsGroupPriceFactors(g_currentVehicle.item.nationID)[self.getGroup()]))


class Camouflage(Item):

    def __init__(self, itemID, rawData, qualifier, isInDossier, allowedVehicles, notAllowedVehicles):
        Item.__init__(self, itemID, rawData, qualifier, isInDossier, allowedVehicles, notAllowedVehicles)
        self._price = g_itemsCache.items.shop.camouflageCost

    def getTexturePath(self):
        colors = self._rawData.get('colors', (0, 0, 0, 0))
        weights = Math.Vector4((colors[0] >> 24) / 255.0, (colors[1] >> 24) / 255.0, (colors[2] >> 24) / 255.0, (colors[3] >> 24) / 255.0)
        return 'img://camouflage,{0:d},{1:d},"{2:>s}",{3[0]:d},{3[1]:d},{3[2]:d},{3[3]:d},{4[0]:n},{4[1]:n},{4[2]:n},{4[3]:n},{5:d}'.format(128, 128, self._rawData['texture'], colors, weights, self._rawData.get('armorColor', 0))

    def getGroup(self):
        return self._rawData['groupName']

    def getName(self):
        return _ms('{}/label'.format(self._rawData['description']))

    def getDescription(self):
        return _ms('{}/description'.format(self._rawData['description']))

    def getIgrType(self):
        return self._rawData['igrType']

    @property
    def isInShop(self):
        return self.getID() not in g_itemsCache.items.shop.getCamouflagesHiddens(g_currentVehicle.item.nationID)

    def getPrice(self, duration):
        return int(round(self._price[duration][0] * g_itemsCache.items.shop.getVehCamouflagePriceFactor(g_currentVehicle.item.descriptor.type.compactDescr) * g_itemsCache.items.shop.getCamouflagesPriceFactors(g_currentVehicle.item.nationID)[self.getID()]))