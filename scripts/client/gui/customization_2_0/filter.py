# Embedded file name: scripts/client/gui/customization_2_0/filter.py
from Event import Event
from CurrentVehicle import g_currentVehicle
from debug_utils import LOG_DEBUG
from gui import GUI_SETTINGS
import nations
from data_aggregator import CUSTOMIZATION_TYPE
from constants import IGR_TYPE
from elements.qualifier import QUALIFIER_TYPE
_GROUPS = {CUSTOMIZATION_TYPE.CAMOUFLAGE: ('winter', 'summer', 'desert', 'IGRwinter', 'IGRsummer', 'IGRdesert'),
 CUSTOMIZATION_TYPE.EMBLEM: ('group1', 'group2', 'group3', 'group4')}
_GROUPS_IGR_CAMOUFLAGE = 3

class FILTER_TYPE:
    QUALIFIER = 0
    GROUP = 1
    PURCHASE_TYPE = 2
    IS_IN_DOSSIER = 3


QUALIFIER_TYPE_INDEX = (QUALIFIER_TYPE.ALL,
 QUALIFIER_TYPE.COMMANDER,
 QUALIFIER_TYPE.GUNNER,
 QUALIFIER_TYPE.DRIVER,
 QUALIFIER_TYPE.RADIOMAN,
 QUALIFIER_TYPE.LOADER)

class PURCHASE_TYPE:
    PURCHASE = 0
    QUEST = 1
    ACTION = 2
    IGR = 3


class Filter(object):

    def __init__(self, type_ = CUSTOMIZATION_TYPE.CAMOUFLAGE):
        self.changed = Event()
        self.__isQualifiersDefault = True
        self.__currentType = type_
        self.__currentPurchaseType = 0
        self.__currentGroup = -1
        self.__isInDossier = False
        self.__rules = {CUSTOMIZATION_TYPE.EMBLEM: [self.__itemIsInGroup,
                                     self.__checkBonusType,
                                     self.__purchaseType,
                                     self.__checkIsInDossier,
                                     self.__isAllowedForCurrentVehicle],
         CUSTOMIZATION_TYPE.CAMOUFLAGE: [self.__itemIsInGroup,
                                         self.__purchaseType,
                                         self.__checkIsInDossier,
                                         self.__isAllowedForCurrentVehicle],
         CUSTOMIZATION_TYPE.INSCRIPTION: [self.__inscriptionIsNational,
                                          self.__itemIsInGroup,
                                          self.__checkBonusType,
                                          self.__purchaseType,
                                          self.__checkIsInDossier,
                                          self.__isAllowedForCurrentVehicle]}
        self.__purchaseTypes = [PURCHASE_TYPE.PURCHASE, PURCHASE_TYPE.QUEST]
        self.__qualifierFilter = {QUALIFIER_TYPE.ALL: False,
         QUALIFIER_TYPE.COMMANDER: False,
         QUALIFIER_TYPE.GUNNER: False,
         QUALIFIER_TYPE.DRIVER: False,
         QUALIFIER_TYPE.RADIOMAN: False,
         QUALIFIER_TYPE.LOADER: False}
        if GUI_SETTINGS.igrEnabled:
            self.__purchaseTypes.append(PURCHASE_TYPE.IGR)

    def isDefaultFilterSet(self):
        return self.__isQualifiersDefault and self.__currentGroup == -1 and self.__currentPurchaseType == 0

    def setDefaultFilter(self):
        self.__currentGroup = -1
        for key in QUALIFIER_TYPE_INDEX:
            self.__qualifierFilter[key] = False

        self.__isQualifiersDefault = True
        self.__currentPurchaseType = 0

    @property
    def qualifierFilter(self):
        return self.__qualifierFilter

    @property
    def purchaseTypes(self):
        return self.__purchaseTypes

    @property
    def currentType(self):
        return self.__currentType

    @property
    def currentPurchaseType(self):
        return self.__currentPurchaseType

    @property
    def currentGroup(self):
        return self.__currentGroup

    def fini(self):
        self.__rules = None
        return

    def check(self, item):
        for rule in self.__rules[self.__currentType]:
            if not rule(item):
                return False

        return True

    def set(self, filterGroup, filterItemIdx):
        if filterGroup == FILTER_TYPE.QUALIFIER:
            self.__qualifierFilter[QUALIFIER_TYPE_INDEX[filterItemIdx]] ^= True
            self.__updateQualifiersFilter()
        elif filterGroup == FILTER_TYPE.GROUP:
            self.__currentGroup = filterItemIdx
        elif filterGroup == FILTER_TYPE.PURCHASE_TYPE:
            self.__currentPurchaseType = filterItemIdx
        elif filterGroup == FILTER_TYPE.IS_IN_DOSSIER:
            self.__isInDossier = filterItemIdx

    def setType(self, type_):
        if self.__currentType != type_:
            self.__currentType = type_
            self.setDefaultFilter()

    def apply(self):
        self.changed()

    def __inscriptionIsNational(self, item):
        if self.__purchaseTypes[self.__currentPurchaseType] != PURCHASE_TYPE.IGR:
            return item.getGroup() == nations.NAMES[g_currentVehicle.item.nationID]
        else:
            return True

    def __checkBonusType(self, item):
        if self.__isQualifiersDefault:
            return True
        if item.qualifier.getType() == QUALIFIER_TYPE.CAMOUFLAGE:
            return True
        return self.__qualifierFilter[item.qualifier.getType()]

    def __itemIsInGroup(self, item):
        if self.__currentGroup < 0:
            return True
        elif self.__purchaseTypes[self.__currentPurchaseType] == PURCHASE_TYPE.IGR and self.__currentType == CUSTOMIZATION_TYPE.CAMOUFLAGE:
            return item.getGroup() == _GROUPS[self.__currentType][self.__currentGroup + _GROUPS_IGR_CAMOUFLAGE]
        else:
            return item.getGroup() == _GROUPS[self.__currentType][self.__currentGroup]

    def __updateQualifiersFilter(self):
        for key in QUALIFIER_TYPE_INDEX:
            if self.__qualifierFilter[key]:
                self.__isQualifiersDefault = False
                return

        self.__isQualifiersDefault = True

    def __purchaseType(self, item):
        if self.__isInShop(item):
            if self.__purchaseTypes[self.__currentPurchaseType] == PURCHASE_TYPE.PURCHASE:
                return item.getIgrType() == IGR_TYPE.NONE
            if self.__purchaseTypes[self.__currentPurchaseType] == PURCHASE_TYPE.IGR:
                return item.getIgrType() != IGR_TYPE.NONE
        return False

    def __isInShop(self, item):
        return item.isInShop

    def __checkIsInDossier(self, item):
        if self.__isInDossier and self.__purchaseTypes[self.__currentPurchaseType] != PURCHASE_TYPE.IGR:
            return item.isInDossier
        else:
            return True

    def __isAllowedForCurrentVehicle(self, item):
        return item.isAllowedForCurrentVehicle