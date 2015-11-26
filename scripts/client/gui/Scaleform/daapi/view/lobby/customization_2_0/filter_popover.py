# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/customization_2_0/filter_popover.py
from gui.Scaleform.daapi.view.meta.CustomizationFiltersPopoverMeta import CustomizationFiltersPopoverMeta
from gui.Scaleform.locale.CUSTOMIZATION import CUSTOMIZATION
from gui.Scaleform.locale.VEHICLE_CUSTOMIZATION import VEHICLE_CUSTOMIZATION
from gui.shared.utils.functions import makeTooltip
from helpers.i18n import makeString as _ms
from gui.Scaleform.locale.TOOLTIPS import TOOLTIPS
from gui.shared.formatters import text_styles, icons
from gui.customization_2_0 import g_customizationController
from gui.customization_2_0.data_aggregator import CUSTOMIZATION_TYPE
from gui.customization_2_0.filter import FILTER_TYPE, QUALIFIER_TYPE_INDEX, PURCHASE_TYPE
from gui.customization_2_0.elements.qualifier import QUALIFIER_TYPE
from gui.customization_2_0.elements.qualifier import getIcon16x16ByType as _getQualifierIcon

class FilterPopover(CustomizationFiltersPopoverMeta):

    def __init__(self, ctx = None):
        super(FilterPopover, self).__init__()
        self.__filter = g_customizationController.carousel.filter
        self.__tooltipsMap = {QUALIFIER_TYPE.ALL: self.__createTooltip(VEHICLE_CUSTOMIZATION.CUSTOMIZATION_TOOLTIP_BONUS_ENTIRECREW),
         QUALIFIER_TYPE.COMMANDER: self.__createTooltip(VEHICLE_CUSTOMIZATION.CUSTOMIZATION_TOOLTIP_BONUS_COMMANDER),
         QUALIFIER_TYPE.GUNNER: self.__createTooltip(VEHICLE_CUSTOMIZATION.CUSTOMIZATION_TOOLTIP_BONUS_AIMER),
         QUALIFIER_TYPE.DRIVER: self.__createTooltip(VEHICLE_CUSTOMIZATION.CUSTOMIZATION_TOOLTIP_BONUS_DRIVER),
         QUALIFIER_TYPE.RADIOMAN: self.__createTooltip(VEHICLE_CUSTOMIZATION.CUSTOMIZATION_TOOLTIP_BONUS_RADIOMAN),
         QUALIFIER_TYPE.LOADER: self.__createTooltip(VEHICLE_CUSTOMIZATION.CUSTOMIZATION_TOOLTIP_BONUS_LOADER)}
        self.__groupsMap = {CUSTOMIZATION_TYPE.INSCRIPTION: (CUSTOMIZATION.FILTER_POPOVER_GROUPS_ALL,),
         CUSTOMIZATION_TYPE.CAMOUFLAGE: (CUSTOMIZATION.FILTER_POPOVER_GROUPS_ALL,
                                         VEHICLE_CUSTOMIZATION.CAMOUFLAGE_WINTER,
                                         VEHICLE_CUSTOMIZATION.CAMOUFLAGE_SUMMER,
                                         VEHICLE_CUSTOMIZATION.CAMOUFLAGE_DESERT),
         CUSTOMIZATION_TYPE.EMBLEM: (CUSTOMIZATION.FILTER_POPOVER_GROUPS_ALL,
                                     VEHICLE_CUSTOMIZATION.EMBLEM_ANIMALS,
                                     VEHICLE_CUSTOMIZATION.EMBLEM_BATTLE,
                                     VEHICLE_CUSTOMIZATION.EMBLEM_COOL,
                                     VEHICLE_CUSTOMIZATION.EMBLEM_SIGNS)}
        self.__purchaseTypeMap = {PURCHASE_TYPE.PURCHASE: CUSTOMIZATION.FILTER_POPOVER_WAYSTOBUY_BUY,
         PURCHASE_TYPE.QUEST: CUSTOMIZATION.FILTER_POPOVER_WAYSTOBUY_MISSIONS,
         PURCHASE_TYPE.ACTION: CUSTOMIZATION.FILTER_POPOVER_WAYSTOBUY_EVENT,
         PURCHASE_TYPE.IGR: icons.premiumIgrSmall()}

    def _populate(self):
        super(FilterPopover, self)._populate()
        self.as_setInitDataS(self.createInitVO())
        self.as_enableDefBtnS(not self.__filter.isDefaultFilterSet())

    def changeFilter(self, filterGroup, filterItemIdx):
        if filterGroup == FILTER_TYPE.GROUP:
            filterItemIdx -= 1
        self.__filter.set(filterGroup, filterItemIdx)
        self.__filter.apply()
        self.as_enableDefBtnS(not self.__filter.isDefaultFilterSet())

    def createInitVO(self):
        return {'lblTitle': text_styles.highTitle(CUSTOMIZATION.FILTER_POPOVER_TITLE),
         'lblBonusType': text_styles.standard(CUSTOMIZATION.FILTER_POPOVER_BONUSTYPE_TITLE),
         'lblCustomizationType': text_styles.standard(CUSTOMIZATION.FILTER_POPOVER_GROUPS_TITLE),
         'lblPurchaseType': text_styles.standard(CUSTOMIZATION.FILTER_POPOVER_WAYSTOBUY_TITLE),
         'btnDefault': CUSTOMIZATION.FILTER_POPOVER_GETDEFAULTSETTINGS,
         'customizationTypeVisible': self.__filter.currentType == CUSTOMIZATION_TYPE.EMBLEM,
         'customizationBonusTypeVisible': self.__filter.currentType != CUSTOMIZATION_TYPE.CAMOUFLAGE,
         'bonusTypeId': FILTER_TYPE.QUALIFIER,
         'bonusType': self.__getBonusTypeVO(),
         'customizationTypeId': FILTER_TYPE.GROUP,
         'customizationType': self.__groupsMap[self.__filter.currentType],
         'customizationTypeSelectedIndex': self.__filter.currentGroup + 1,
         'refreshTooltip': makeTooltip(TOOLTIPS.CUSTOMIZATION_FILTERPOPOVER_REFRESH_HEADER, TOOLTIPS.CUSTOMIZATION_FILTERPOPOVER_REFRESH_BODY),
         'purchaseTypeId': FILTER_TYPE.PURCHASE_TYPE,
         'purchaseType': self.__getPurchaseTypeVO(),
         'purchaseTypeSelectedIndex': self.__filter.currentPurchaseType}

    def __getPurchaseTypeVO(self):
        rez = []
        for purchaseType in self.__filter.purchaseTypes:
            rez.append({'label': self.__purchaseTypeMap[purchaseType]})

        return rez

    def __getBonusTypeVO(self):
        rez = []
        qualifierFilter = self.__filter.qualifierFilter
        for bonusType in QUALIFIER_TYPE_INDEX:
            vo = {'selected': qualifierFilter[bonusType],
             'value': _getQualifierIcon(bonusType),
             'tooltip': self.__tooltipsMap[bonusType]}
            rez.append(vo)

        return rez

    def __createTooltip(self, value):
        return makeTooltip(_ms(TOOLTIPS.CUSTOMIZATION_FILTERPOPOVER_BONUSDESCRIPTION_HEADER, bonus=_ms(value)), _ms(TOOLTIPS.CUSTOMIZATION_FILTERPOPOVER_BONUSDESCRIPTION_BODY, bonus=_ms(value)))

    def setDefaultFilter(self):
        self.__filter.setDefaultFilter()
        self.__filter.apply()
        qualifierFilter = self.__filter.qualifierFilter
        bonusTypeSelected = []
        for bonusType in QUALIFIER_TYPE_INDEX:
            bonusTypeSelected.append(qualifierFilter[bonusType])

        data = {'customizationTypeSelectedIndex': self.__filter.currentGroup + 1,
         'purchaseTypeSelectedIndex': self.__filter.currentPurchaseType,
         'bonusTypeSelected': bonusTypeSelected}
        self.as_setStateS(data)
        self.as_enableDefBtnS(False)