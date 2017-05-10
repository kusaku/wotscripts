# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/store/actions_helpers.py
import BigWorld
import operator
import time
import constants
import nations
from gui.Scaleform.locale.QUESTS import QUESTS
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.Scaleform.locale.TOOLTIPS import TOOLTIPS
from gui.server_events.event_items import ActionData
from gui.server_events.events_helpers import EventInfoModel
from gui.Scaleform.daapi.view.lobby.missions.conditions_formatters import formatters
from gui.server_events.formatters import formatStrDiscount, formatPercentValue, formatMultiplierValue, DECORATION_SIZES, formatGoldPrice, formatGoldPriceBig, formatCreditPrice, formatCreditPriceBig, formatVehicleLevel
from gui.shared.formatters import icons
from gui.shared.formatters import text_styles
from gui.server_events import settings as quest_settings
from gui.shared.money import Currency
from helpers import i18n, dependency, time_utils
from skeletons.gui.server_events import IEventsCache
from skeletons.gui.shared import IItemsCache
_DT = formatters.DISCOUNT_TYPE
_VEHICLE_NATION_ICON_PATH = '../maps/icons/filters/nations/%s.png'
_MAX_ITEMS_IN_TABLE = 3
_PRIORITY_FOR_FUTURE_ACTION = 4
_MULTIPLIER = 'Multiplier'
_PREMIUM_PACKET = 'premiumPacket'
_gold_bonus_list = ('slotsPrices',
 'berthsPrices',
 'premiumPacket1Cost',
 'premiumPacket3Cost',
 'premiumPacket7Cost',
 'premiumPacket14Cost',
 'premiumPacket30Cost',
 'premiumPacket90Cost',
 'premiumPacket180Cost',
 'premiumPacket360Cost')

class ActionInfo(EventInfoModel):
    """Data model for action card on action store view
    """
    __slots__ = ('event', 'discount', 'priority', '_id', '_maxDiscount', '_packedDiscounts')

    def __init__(self, event, actionData):
        super(ActionInfo, self).__init__(event)
        self.discount = actionData.discountObj
        self.priority = actionData.priority
        self.uiDecoration = actionData.uiDecoration
        self._id = ''
        self._maxDiscount = None
        self._packedDiscounts = None
        return

    @property
    def visualPriority(self):
        """Visual priority for view
        :return: int (1 - hero, 2 - normal, 3 - small)
        """
        return self.priority

    @visualPriority.setter
    def visualPriority(self, value):
        """Visual priority for view
        """
        self.priority = value

    def getID(self):
        """Unique id for action card
        """
        if not self._id:
            self._id = '{}/{}/{}'.format(self.event.getID(), self.discount.getName(), self.discount.getParamName())
        return self._id

    def isAvailable(self):
        """Dump method, used for self.getIsNew()
        """
        return (True, None)

    def isCompleted(self):
        """Dump method, used for self.getIsNew()
        """
        return False

    def isOutOfDate(self):
        """Dump method, used for self.getIsNew()
        """
        return False

    def getStartTime(self):
        """Return action start time
        """
        return self.event.getStartTime()

    def getFinishTime(self):
        """Return action finish time
        """
        return BigWorld.wg_getLongDateFormat(self.event.getFinishTime())

    def getTitle(self):
        """Return card title
        """
        return self.event.getUserName()

    def getIsNew(self):
        """Is card viewed before
        """
        return quest_settings.isNewCommonEvent(self)

    def getAutoDescription(self, useBigIco = False):
        """Automatic description for all cards
        :param useBigIco: use big or small currency icons
        :return: i18n formatted text
        """
        discountValue = self._getAutoDescriptionData(useBigIco)
        return self._getShortDescription(self.discount.getParamName(), discount=discountValue)

    def getAdditionalDescription(self, useBigIco = False):
        """Additional description, automatically showed for hero card
        on hover show for normal cards
        :param useBigIco: use big or small currency icons
        :return: i18n formatted text
        """
        discount = self._getAdditionalDescriptionData(useBigIco)
        return self._getFullDescription(self.discount.getParamName(), discount)

    def getComingSoonDescription(self):
        pass

    def getTooltipInfo(self):
        """Get str for card tooltip
        """
        return self.event.getDescription()

    def isDiscountVisible(self):
        discount = self._getMaxDiscount()
        if discount:
            if discount.discountType == _DT.MULTIPLIER:
                return not (discount.discountValue == 0 or discount.discountValue == 1)
            else:
                return discount.discountValue > 0
        return False

    def getDiscount(self):
        """Calculate action discount
        :return: formatted text with discount info or empty string if can't calculate
        """
        discount = self._getMaxDiscount()
        if discount:
            return formatStrDiscount(discount)
        return ''

    def getBattleQuestsInfo(self):
        """Get linked quests and format button text
        """
        linkedQuests = self.event.linkedQuests
        if linkedQuests:
            return i18n.makeString(QUESTS.ACTION_LABEL_BATTLEQUESTS, count=len(linkedQuests))
        return ''

    def getLinkBtnLabel(self):
        """Formatted web link text
        """
        pass

    def getActionBtnLabel(self):
        """Get formatted button text
        """
        return self._getButtonName(self.discount.getParamName())

    def getPicture(self):
        """Get img for action
        """
        picture = getDecoration(self.uiDecoration)
        if picture:
            return {'isWeb': True,
             'src': picture}
        paramName = self.discount.getParamName()
        if paramName.endswith(_MULTIPLIER):
            paramName = paramName[:-len(_MULTIPLIER)]
        return {'isWeb': False,
         'src': _PARAM_TO_IMG_DICT.get(paramName, '')}

    def getTriggerChainID(self):
        """Gets chapter ID to run tutorial system for sales
        :return: str
        """
        raise NotImplementedError

    def getTableData(self):
        """If card contains tabled data, format and return data
        """
        return []

    def getActionTime(self):
        return {'id': self.getID(),
         'isTimeOver': not self.event.isAvailable()[0],
         'timeLeft': self._getActiveTimeDateText(),
         'isShowTimeIco': self._showTimerIco()}

    def _showTimerIco(self):
        """Show timer icon when action comes to end
        :return:
        """
        return self.event.getFinishTimeLeft() <= time_utils.ONE_DAY

    def _getActiveTimeDateText(self):
        """
        Gets formatted mission's active time
        """
        timeStr = self._getActiveDateTimeString()
        return text_styles.stats(timeStr)

    @classmethod
    def _getAutoDescription(cls, stepName):
        """Card description text
        Used only for coming soon cards
        :param stepName: step name
        :return: i18n description string
        """
        formatter = 'auto/{}'.format(stepName)
        return i18n.makeString(QUESTS.getActionDescription(formatter))

    @classmethod
    def _getFullDescription(cls, stepName, discount = None):
        formatter = 'full/{}'.format(stepName)
        return i18n.makeString(QUESTS.getActionDescription(formatter), discount=discount)

    @classmethod
    def _getShortDescription(cls, stepName, **kwargs):
        """Card description text
        Used for small cards
        :param stepName: step name
        :param kwargs: dict params for text
        :return: i18n description string
        """
        formatter = 'short/{}'.format(stepName)
        return i18n.makeString(QUESTS.getActionDescription(formatter), **kwargs)

    @classmethod
    def _getButtonName(cls, stepName):
        """Button text
        :param stepName: step name
        :return: i18n button text
        """
        formatter = 'button/{}'.format(stepName)
        return i18n.makeString(QUESTS.getActionDescription(formatter))

    @classmethod
    def _formatPriceIcon(cls, item, useBigIco):
        """Convert price to text with currency icon
        :param item: vehicle, camuflage, etc...
        :param useBigIco: show small or big icon format
        :return: formatted price
        """
        if hasattr(item, 'buyPrice'):
            sellPrice = item.buyPrice.toDict()
            if sellPrice[Currency.GOLD]:
                if useBigIco:
                    return formatGoldPriceBig(sellPrice[Currency.GOLD])
                else:
                    return formatGoldPrice(sellPrice[Currency.GOLD])
            if sellPrice[Currency.CREDITS]:
                if useBigIco:
                    return formatCreditPriceBig(sellPrice[Currency.CREDITS])
                else:
                    return formatCreditPrice(sellPrice[Currency.CREDITS])
        return ''

    def _getPackedDiscounts(self):
        """Gather info about all discounts for card
        :return:
        """
        if not self._packedDiscounts:
            self._packedDiscounts = self.discount.packDiscounts()
        return self._packedDiscounts

    def _getMaxDiscount(self):
        """Get best discount value for action
        :return: discount with max value
        """
        if not self._maxDiscount:
            discounts = self._getPackedDiscounts()
            if discounts:
                self._maxDiscount = max(discounts.values(), key=operator.itemgetter(1))
        return self._maxDiscount

    def _getAutoDescriptionData(self, useBigIco = False):
        """format string with auto description about action
        :param useBigIco: big/small icon in text
        :return: i18n string
        """
        return 0

    def _getAdditionalDescriptionData(self, useBigIco = False):
        """format string with short description about action
        :param useBigIco: big/small icon in text
        :return: i18n string
        """
        return 0

    def _formatFinishTime(self):
        """Format string with finish time for action
        """
        return '{} {}'.format(text_styles.main(i18n.makeString(QUESTS.ACTION_TIME_FINISH)), self.getFinishTime())

    def _getActiveDateTimeString(self):
        """Format time in 'hh mm' format
        """
        if self.event.getFinishTimeLeft() <= time_utils.ONE_DAY:
            gmtime = time.gmtime(self.event.getFinishTimeLeft())
            if gmtime.tm_hour > 0:
                fmt = i18n.makeString(QUESTS.ITEM_TIMER_TILLFINISH_LONGFORMAT)
            else:
                fmt = i18n.makeString(QUESTS.ITEM_TIMER_TILLFINISH_SHORTFORMAT)
            fmt %= {'hours': time.strftime('%H', gmtime),
             'min': time.strftime('%M', gmtime)}
            return '{} {}'.format(text_styles.main(i18n.makeString(QUESTS.ACTION_TIME_LEFT)), fmt)
        return self._formatFinishTime()


class EconomicsActionsInfo(ActionInfo):
    """Economics actions
    """

    def getTriggerChainID(self):
        """Gets chapter ID to run tutorial system for sales
        :return: str
        """
        if 'winXPFactorMode' in self.discount.getParamName():
            return 'winXPFactorMode'
        return self.discount.getParamName()

    def getDiscount(self):
        """Calculate action discount
        :return: formatted text with discount info or '' if can't calculate
        """
        paramName = self.discount.getParamName()
        if 'winXPFactorMode' in paramName:
            discount = self.__handleWinXPFactorMode()
        else:
            discounts = self._getPackedDiscounts()
            discount = discounts.get(paramName) if discounts else None
        if discount:
            return formatStrDiscount(discount)
        else:
            return ''

    def getActionBtnLabel(self):
        """Get formatted button text
        """
        if self.discount.getParamName() in ('clanCreationCost',):
            return ''
        if _PREMIUM_PACKET in self.discount.getParamName():
            isPremium = getEconomicalStatsDict().get('isPremium', False)
            if isPremium:
                return self._getButtonName('{}/continue'.format(_PREMIUM_PACKET))
            else:
                return self._getButtonName('{}/new'.format(_PREMIUM_PACKET))
        return super(EconomicsActionsInfo, self).getActionBtnLabel()

    def getLinkBtnLabel(self):
        """Formatted web link text
        """
        if self.discount.getParamName() == 'clanCreationCost':
            return self._getButtonName(self.discount.getParamName())
        return ''

    def _getAutoDescriptionData(self, useBigIco = False):
        """format string with auto description about action
        :param useBigIco: big/small icon in text
        :return: i18n string
        """
        paramName = self.discount.getParamName()
        if 'exchangeRate' in paramName:
            discountValue = self.__getExchangeRateBonusIco()
        elif paramName in ('freeXPConversionDiscrecity', 'freeXPToTManXPRate'):
            discountValue = self.getDiscount()
        else:
            discountValue = self._getAdditionalDescriptionData(useBigIco=True)
        return discountValue

    def _getAdditionalDescriptionData(self, useBigIco = False):
        """format string with short description about action
        :param useBigIco: big/small icon in text
        :return: i18n string
        """
        paramName = self.discount.getParamName()
        if paramName.endswith(_MULTIPLIER):
            paramName = paramName[:-len(_MULTIPLIER)]
        if 'winXPFactorMode' in paramName:
            discountValue = getEconomicalStatsDict().get('dailyXPFactor', None)
        elif 'exchangeRate' in paramName:
            discountValue = self.__getExchangeRateBonusIco()
        else:
            discountValue = getEconomicalStatsDict().get(paramName, None)
        if paramName in _gold_bonus_list:
            if useBigIco:
                discountValue = formatGoldPriceBig(discountValue)
            else:
                discountValue = formatGoldPrice(discountValue)
        if not discountValue:
            discount = self._getMaxDiscount()
            discountValue = formatPercentValue(discount.discountValue) if discount else None
        return discountValue

    def __handleWinXPFactorMode(self):
        return self.discount.handlerWinXPFactorMode()

    def __getExchangeRateBonusIco(self, useBigIco = False):
        credits = getEconomicalStatsDict().get('exchangeRate')
        if useBigIco:
            goldIcon = formatGoldPriceBig(1)
            creditsIcon = formatCreditPriceBig(credits)
        else:
            goldIcon = formatGoldPrice(1)
            creditsIcon = formatCreditPrice(credits)
        return i18n.makeString(QUESTS.ACTION_EXCHANGERATE_GOLD2CREDIT, gold=goldIcon, credits=creditsIcon)


class VehPriceActionInfo(ActionInfo):

    def getTriggerChainID(self):
        """Gets chapter ID to run tutorial system for sales
        :return: str
        """
        return 'vehicleBuyPrice'

    def getAutoDescription(self, useBigIco = False):
        """Return card description
        :param useBigIco: use big or small currency icon
        :return: formatted text
        """
        vehs = self._getAdditionalDescriptionData(useBigIco)
        vehsLen = len(vehs)
        if vehsLen == 1:
            paramName = '{}/{}'.format(self.discount.getParamName(), 'one')
            veh = vehs[0]
            values = {'vehicles': veh['title'],
             'discount': veh['price']}
            return self._getShortDescription(paramName, **values)
        if vehsLen > 1:
            paramKey = 'two' if vehsLen == 2 else 'more'
            paramName = '{}/{}'.format(self.discount.getParamName(), paramKey)
            values = {'vehicles': '{}, {}'.format(vehs[0]['title'], vehs[1]['title']),
             'discount': formatPercentValue(vehs[0]['discount'])}
            return self._getShortDescription(paramName, **values)
        return ''

    def getAdditionalDescription(self, useBigIco = False):
        """Format table description
        :return: formatted text
        """
        vehiclesCount = len(self._getPackedDiscounts())
        if vehiclesCount > _MAX_ITEMS_IN_TABLE:
            return i18n.makeString(QUESTS.ACTION_DISCOUNT_MORE, deviceName=i18n.makeString(QUESTS.ACTION_MORE_TYPE_VEHICLES), count=vehiclesCount - _MAX_ITEMS_IN_TABLE)
        return ''

    def getTableData(self):
        """If card contains tabled data, format and return data
        """
        result = []
        for item in self.__sortVehicles():
            veh = item.discountName
            if veh.isPremium or veh.isElite:
                iconFunc = RES_ICONS.maps_icons_vehicletypes_elite
            else:
                iconFunc = RES_ICONS.maps_icons_vehicletypes
            item = {'icon': _VEHICLE_NATION_ICON_PATH % nations.NAMES[veh.nationID],
             'additionalIcon': iconFunc(veh.type + '.png'),
             'title': '{} {}'.format(i18n.makeString(TOOLTIPS.level(veh.level)), veh.shortUserName),
             'discount': formatStrDiscount(item),
             'price': self._formatPriceIcon(veh, False)}
            result.append(item)

        return result

    def _getAdditionalDescriptionData(self, useBigIco = False):
        """format string with short description about action
        :param useBigIco: big/small icon in text
        :return: i18n string
        """
        result = []
        for item in self.__sortVehicles():
            veh = item.discountName
            level = formatVehicleLevel(i18n.makeString(TOOLTIPS.level(veh.level)))
            item = {'title': '{} {}'.format(level, veh.shortUserName),
             'discount': item.discountValue,
             'price': self._formatPriceIcon(veh, useBigIco)}
            result.append(item)

        return result

    def __sortVehicles(self):

        def __sortByNameFunc(item):
            raise item.discountName or AssertionError
            raise item.discountName.shortUserName or AssertionError
            return item.discountName.shortUserName

        def __sortByVehicleParams(item):
            raise item.discountName or AssertionError
            raise item.discountName.buyPrice or AssertionError
            raise item.discountName.level or AssertionError
            raise item.discountValue or AssertionError
            veh = item.discountName
            dscnt = item.discountValue
            return (dscnt, (veh.buyPrice.gold, veh.buyPrice.credits), veh.level)

        discountItems = self._getPackedDiscounts()
        return sorted(sorted(discountItems.values(), key=__sortByNameFunc), key=__sortByVehicleParams, reverse=True)[:3]


class VehRentActionInfo(VehPriceActionInfo):

    def getTriggerChainID(self):
        """Gets chapter ID to run tutorial system for sales
        :return: str
        """
        return 'vehicleRentPrice'

    def getAdditionalDescription(self, useBigIco = False):
        """Format table description
        :return: formatted text
        """
        return self._getFullDescription(self.discount.getParamName())

    def getTableData(self):
        """If card contains tabled data, format and return data
        """
        return None


class EquipmentActionInfo(ActionInfo):

    def getTriggerChainID(self):
        """Gets chapter ID to run tutorial system for sales
        :return: str
        """
        return 'equipmentPrice'

    def getAdditionalDescription(self, useBigIco = False):
        """Format table description
        """
        equipCount = len(self._getPackedDiscounts())
        if equipCount > _MAX_ITEMS_IN_TABLE:
            return i18n.makeString(QUESTS.ACTION_DISCOUNT_MORE, deviceName=i18n.makeString(QUESTS.ACTION_MORE_TYPE_EQUIPMENT), count=equipCount - _MAX_ITEMS_IN_TABLE)
        return ''

    def getTableData(self):
        """If card contains tabled data, format and return data
        """
        items = self._getPackedDiscounts()
        res = []
        for intCD, data in items.iteritems():
            equip = data.discountName
            item = {'icon': '',
             'additionalIcon': '',
             'title': '{} {}'.format(icons.makeImageTag(equip.icon, vSpace=-3), equip.userName),
             'discount': formatStrDiscount(data),
             'price': self._formatPriceIcon(equip, False)}
            res.append(item)

        return res[:3]


class OptDeviceActionInfo(ActionInfo):

    def getTriggerChainID(self):
        """Gets chapter ID to run tutorial system for sales
        :return: str
        """
        return 'optionalDevicePrice'

    def getAdditionalDescription(self, useBigIco = False):
        """Format table description
        :return: formatted text
        """
        optDeviceCount = len(self._getPackedDiscounts())
        if optDeviceCount > _MAX_ITEMS_IN_TABLE:
            return i18n.makeString(QUESTS.ACTION_DISCOUNT_MORE, deviceName=i18n.makeString(QUESTS.ACTION_MORE_TYPE_OPTIONALDEVICES), count=optDeviceCount - _MAX_ITEMS_IN_TABLE)
        return ''

    def getTableData(self):
        """If card contains tabled data, format and return data
        """
        items = self._getPackedDiscounts()
        res = []
        for intCD, data in items.iteritems():
            optDevice = data.discountName
            item = {'icon': '',
             'additionalIcon': '',
             'title': '{} {}'.format(icons.makeImageTag(optDevice.icon, vSpace=-3), optDevice.userName),
             'discount': formatStrDiscount(data),
             'price': self._formatPriceIcon(optDevice, False)}
            res.append(item)

        return sorted(res, key=lambda x: x['discount'], reverse=True)[:3]


class ShellPriceActionInfo(ActionInfo):

    def getTriggerChainID(self):
        """Gets chapter ID to run tutorial system for sales
        :return: str
        """
        return 'shellsPrice'


class CamouflagePriceActionInfo(ActionInfo):

    def getTriggerChainID(self):
        """Gets chapter ID to run tutorial system for sales
        :return: str
        """
        return 'camouflagePacketInfCostMultiplier'

    def getAdditionalDescription(self, useBigIco = False):
        """Format table description
        """
        fmtList = self._getAdditionalDescriptionData()
        discountValue = fmtList[0]['discount'] if fmtList else None
        return self._getFullDescription(self.discount.getParamName(), discountValue)

    def getAutoDescription(self, useBigIco = False):
        """Return text description on hover for small card
        """
        vehs = self._getAdditionalDescriptionData()
        if vehs:
            values = {'discount': vehs[0]['discount'],
             'vehicles': ', '.join([ veh['title'] for veh in vehs ])}
            return self._getShortDescription(self.discount.getParamName(), **values)
        return ''

    def _getAdditionalDescriptionData(self, useBigIco = False):
        vehicles = self._getPackedDiscounts()
        res = []
        for _, data in vehicles.iteritems():
            veh = data.discountName
            item = {'title': veh.shortUserName,
             'discount': formatPercentValue(data.discountValue)}
            res.append(item)

        return sorted(res, key=lambda x: x['discount'], reverse=True)


class InscriptionPriceActionInfo(ActionInfo):

    def getTriggerChainID(self):
        """Gets chapter ID to run tutorial system for sales
        :return: str
        """
        return 'inscriptionPacketInfCostMultiplier'

    def getAdditionalDescription(self, useBigIco = False):
        """Format table description
        """
        inscriptionsCount = len(self._getPackedDiscounts())
        if inscriptionsCount > _MAX_ITEMS_IN_TABLE:
            return i18n.makeString(QUESTS.ACTION_DISCOUNT_MORE, count=inscriptionsCount - _MAX_ITEMS_IN_TABLE)
        return ''

    def getTableData(self):
        """If card contains tabled data, format and return data
        """
        items = self._getPackedDiscounts()
        res = []
        for intCD, data in items.iteritems():
            veh = data.discountName
            item = {'icon': '',
             'additionalIcon': '',
             'title': '{} {}'.format(icons.makeImageTag(veh.icon, vSpace=-3), veh.userName),
             'discount': formatStrDiscount(data),
             'price': self._formatPriceIcon(veh, False)}
            res.append(item)

        return sorted(res, key=lambda x: x['discount'], reverse=True)[:3]


class EmblemPriceByGroupsActionInfo(ActionInfo):

    def getTriggerChainID(self):
        """Gets chapter ID to run tutorial system for sales
        :return: str
        """
        return 'emblemPacketInfCostMultiplier'


class BoosterPriceActionInfo(ActionInfo):

    def getTriggerChainID(self):
        """Gets chapter ID to run tutorial system for sales
        :return: str
        """
        return 'goodiePrice'

    def getAdditionalDescription(self, useBigIco = False):
        """Format table description
        """
        boostersCount = len(self._getPackedDiscounts())
        if boostersCount > _MAX_ITEMS_IN_TABLE:
            return i18n.makeString(QUESTS.ACTION_DISCOUNT_MORE, deviceName=i18n.makeString(QUESTS.ACTION_MORE_TYPE_GOODIES), count=boostersCount - _MAX_ITEMS_IN_TABLE)
        return ''

    def getTableData(self):
        """If card contains tabled data, format and return data
        """
        res = []
        for data in self.__sortBoosters():
            booster = data.discountName
            guiType = booster.boosterGuiType
            formatter = 'booster/{}'.format(guiType)
            busterName = i18n.makeString(QUESTS.getActionDescription(formatter))
            busterSmallIcon = RES_ICONS.getBusterSmallIcon(guiType)
            item = {'icon': busterSmallIcon,
             'vehTypeIcon': '',
             'title': busterName,
             'discount': formatStrDiscount(data),
             'price': self._formatPriceIcon(booster, False)}
            res.append(item)

        return res

    def __sortBoosters(self):

        def __sortByNameFunc(item):
            raise item.discountName or AssertionError
            raise item.discountName.userName or AssertionError
            return item.discountName.userName

        def __sortByParams(item):
            raise item.discountName or AssertionError
            raise item.discountName.buyPrice or AssertionError
            raise item.discountValue or AssertionError
            booster = item.discountName
            dscnt = item.discountValue
            return (dscnt, (booster.buyPrice.gold, booster.buyPrice.credits))

        discountItems = self._getPackedDiscounts()
        return sorted(sorted(discountItems.values(), key=__sortByNameFunc), key=__sortByParams, reverse=True)[:3]


class ComingSoonActionInfo(ActionInfo):
    """Future actions with limited fields to show
    """

    def __init__(self, info):
        self.__name = info['name']
        self.__startTime = info['startTime']
        self.__announceTime = info['announceTime']
        self.__params = info['params']
        super(ComingSoonActionInfo, self).__init__(object, ActionData(object, _PRIORITY_FOR_FUTURE_ACTION, 0))

    def getID(self):
        return '{}/{}/{}'.format(self.__announceTime, self.__startTime, self._getParamName())

    def getStartTime(self):
        return self.__startTime

    def getFinishTime(self):
        pass

    def getActionTime(self):
        return {'id': self.getID(),
         'isTimeOver': False,
         'timeLeft': self._getStartTime(),
         'isShowTimeIco': False}

    def getTriggerChainID(self):
        pass

    def getPicture(self):
        picture = getDecoration(self.uiDecoration)
        if picture:
            return {'isWeb': True,
             'src': picture}
        return {'isWeb': False,
         'src': _PARAM_TO_IMG_DICT.get(self._getParamName(), '')}

    def getTitle(self):
        return i18n.makeString(QUESTS.ACTION_COMINGSOON_LABEL)

    def getIsNew(self):
        return False

    def getAutoDescription(self, useBigIco = False):
        pass

    def getAdditionalDescription(self, useBigIco = False):
        pass

    def getComingSoonDescription(self):
        return self._getAutoDescription(self._getParamName())

    def getTooltipInfo(self):
        return ''

    def getDiscount(self):
        return ''

    def getBattleQuestsInfo(self):
        return ''

    def getLinkBtnLabel(self):
        pass

    def getActionBtnLabel(self):
        pass

    def _getStartTime(self):
        startTimeStr = BigWorld.wg_getLongDateFormat(self.__startTime)
        if startTimeStr is not None:
            return text_styles.main(i18n.makeString(QUESTS.ACTION_COMINGSOON_TIME, startTime=startTimeStr))
        else:
            return ''

    def _getParamName(self):
        """Get step name for images, texts...
        :return: str
        """
        paramName = self.__name
        if 'Economics' in paramName:
            paramName = self.__params[0] if self.__params else ''
        if paramName.endswith(_MULTIPLIER):
            paramName = paramName[:-len(_MULTIPLIER)]
        return paramName


def getEconomicalStatsDict():
    itemsCache = dependency.instance(IItemsCache)
    shop = itemsCache.items.shop
    return {'exchangeRate': shop.exchangeRate,
     'slotsPrices': shop.slotsPrices[1][0],
     'berthsPrices': shop.berthsPrices[2][0],
     'premiumPacket1Cost': shop.getPremiumPacketCost(1),
     'premiumPacket3Cost': shop.getPremiumPacketCost(3),
     'premiumPacket7Cost': shop.getPremiumPacketCost(7),
     'premiumPacket14Cost': shop.getPremiumPacketCost(14),
     'premiumPacket30Cost': shop.getPremiumPacketCost(30),
     'premiumPacket90Cost': shop.getPremiumPacketCost(90),
     'premiumPacket180Cost': shop.getPremiumPacketCost(180),
     'premiumPacket360Cost': shop.getPremiumPacketCost(360),
     'winXPFactorMode': shop.winXPFactorMode,
     'freeXPToTManXPRate': shop.freeXPToTManXPRate,
     'dailyXPFactor': shop.dailyXPFactor,
     'freeXPConversionDiscrecity': shop.freeXPConversion[0],
     'isPremium': itemsCache.items.stats.isPremium}


def getDecoration(uiDecoration):
    """ Get external decoration for the discount.
    """
    eventsCache = dependency.instance(IEventsCache)
    prefetcher = eventsCache.prefetcher
    return prefetcher.getMissionDecoration(uiDecoration, DECORATION_SIZES.DISCOUNT)


_PARAM_TO_IMG_DICT = {'exchangeRate': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CONVERT_GOLD,
 'paidRemovalCost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_REMOVE_EQUIPMENT,
 'changeRoleCost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CREW_CHANGE_MAIN_SKILL,
 'freeXPConversionDiscrecity': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CONVERT_EXP,
 'slotsPrices': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_SLOT,
 'berthsPrices': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_PLACE_IN_BARRACKS,
 'goldTankmanCost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CREW_EDUCATION,
 'creditsTankmanCost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CREW_EDUCATION,
 'creditsDropSkillsCost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CREW_SKILL_RESET,
 'goldDropSkillsCost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CREW_SKILL_RESET,
 'passportChangeCost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CREW_CHANGE_PROFILE,
 'femalePassportChangeCost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CREW_CHANGE_PROFILE,
 'premiumPacket1Cost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_PREM_1,
 'premiumPacket3Cost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_PREM_3,
 'premiumPacket7Cost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_PREM_7,
 'premiumPacket14Cost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_PREM_14,
 'premiumPacket30Cost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_PREM_30,
 'premiumPacket90Cost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_PREM_90,
 'premiumPacket180Cost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_PREM_180,
 'premiumPacket360Cost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_PREM_360,
 'emblemPacketInfCost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CUSTOM_EMBLEM,
 'emblemPacket7Cost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CUSTOM_EMBLEM,
 'emblemPacket30Cost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CUSTOM_EMBLEM,
 'inscriptionPacketInfCost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CUSTOM_LABEL,
 'inscriptionPacket30Cost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CUSTOM_LABEL,
 'inscriptionPacket7Cost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CUSTOM_LABEL,
 'camouflagePacketInfCost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CUSTOM_CAMOUFLAGE,
 'camouflagePacket30Cost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CUSTOM_CAMOUFLAGE,
 'camouflagePacket7Cost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CUSTOM_CAMOUFLAGE,
 'winXPFactorMode/always': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_TANK_EXP,
 'winXPFactorMode/daily': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_TANK_EXP,
 'freeXPToTManXPRate': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CREW_EXP,
 'clanCreationCost': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CLAN,
 'cond_VehPrice': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_VEHICLES,
 'mul_VehPrice': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_VEHICLES,
 'set_VehPrice': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_VEHICLES,
 'mul_VehPriceAll': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_VEHICLES,
 'mul_VehPriceNation': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_VEHICLES,
 'set_VehSellPrice': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_VEHICLES,
 'cond_VehRentPrice': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_TANK_CLOCK,
 'mul_VehRentPrice': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_TANK_CLOCK,
 'set_VehRentPrice': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_TANK_CLOCK,
 'mul_VehRentPriceAll': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_TANK_CLOCK,
 'mul_VehRentPriceNation': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_TANK_CLOCK,
 'mul_EquipmentPriceAll': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CONSUMABLES,
 'mul_EquipmentPrice': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CONSUMABLES,
 'set_EquipmentPrice': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CONSUMABLES,
 'mul_OptionalDevicePriceAll': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_EQUIPMENT,
 'mul_OptionalDevicePrice': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_EQUIPMENT,
 'set_OptionalDevicePrice': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_EQUIPMENT,
 'mul_ShellPriceAll': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_SHELLS,
 'mul_ShellPriceNation': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_SHELLS,
 'mul_ShellPrice': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_SHELLS,
 'set_ShellPrice': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_SHELLS,
 'mul_CamouflagePriceFactor': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CUSTOM_CAMOUFLAGE,
 'mul_EmblemPriceFactorByGroups': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_CUSTOM_CAMOUFLAGE,
 'set_GoodiePrice': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_RESERVE,
 'mul_GoodiePrice': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_RESERVE,
 'mul_GoodiePriceAll': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_RESERVE,
 'tradeInSellPriceFactor': RES_ICONS.MAPS_ICONS_ACTIONS_480X280_TRADE_IN}
_MODIFIERS_DICT = {'mul_EconomicsParams': EconomicsActionsInfo,
 'set_EconomicsParams': EconomicsActionsInfo,
 'mul_EconomicsPrices': EconomicsActionsInfo,
 'set_EconomicsPrices': EconomicsActionsInfo,
 'set_TradeInParams': EconomicsActionsInfo,
 'cond_VehPrice': VehPriceActionInfo,
 'mul_VehPrice': VehPriceActionInfo,
 'mul_VehRentPrice': VehRentActionInfo,
 'set_VehRentPrice': VehRentActionInfo,
 'mul_EquipmentPriceAll': EquipmentActionInfo,
 'mul_OptionalDevicePriceAll': OptDeviceActionInfo,
 'mul_ShellPriceAll': ShellPriceActionInfo,
 'mul_CamouflagePriceFactor': CamouflagePriceActionInfo,
 'mul_EmblemPriceFactorByGroups': EmblemPriceByGroupsActionInfo,
 'set_GoodiePrice': BoosterPriceActionInfo,
 'mul_GoodiePrice': BoosterPriceActionInfo,
 'mul_GoodiePriceAll': BoosterPriceActionInfo}

def getModifierObj(name, event, modifier):
    if name in _MODIFIERS_DICT:
        return _MODIFIERS_DICT[name](event, modifier)
    else:
        return None


def getActionInfoData(event):
    if event.getType() == constants.EVENT_TYPE.ACTION:
        return _parseAction(event)
    return []


def getAnnouncedActionInfo(info):
    return ComingSoonActionInfo(info)


def _parseAction(event):
    result = []
    modifiers = event.getActions()
    for modifierName, modifierData in modifiers.iteritems():
        for actionData in modifierData:
            modifier = getModifierObj(modifierName, event, actionData)
            if modifier:
                result.append(modifier)

    return result