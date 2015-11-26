# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/clans/profile/ClanProfileTableStatisticsView.py
import operator
import BigWorld
from debug_utils import LOG_ERROR
from gui.shared.utils import sortByFields
from helpers.i18n import makeString as _ms
from adisp import process
from gui.shared.formatters import icons, text_styles
from gui.Scaleform.daapi.view.meta.ClanProfileTableStatisticsViewMeta import ClanProfileTableStatisticsViewMeta
from gui.Scaleform.framework.entities.DAAPIDataProvider import SortableDAAPIDataProvider
from gui.Scaleform.genConsts.CLANS_ALIASES import CLANS_ALIASES
from gui.Scaleform.locale.CLANS import CLANS
from helpers import time_utils

def _packColumn(columndID, label, buttonWidth, tooltip, enabled, icon = '', sortOrder = -1, showSeparator = True, textAlign = 'left'):
    return {'id': columndID,
     'label': _ms(label),
     'iconSource': icon,
     'buttonWidth': buttonWidth,
     'toolTip': tooltip,
     'sortOrder': sortOrder,
     'defaultSortDirection': 'ascending',
     'buttonHeight': 34,
     'showSeparator': showSeparator,
     'textAlign': textAlign,
     'enabled': enabled}


class _SORT_IDS:
    FRONT = 'front'
    PROVINCE = 'province'
    MAP = 'map'
    PRIMETIME = 'primeTime'
    DAYS = 'days'
    INCOME = 'income'


class ClanProfileTableStatisticsView(ClanProfileTableStatisticsViewMeta):

    def __init__(self):
        super(ClanProfileTableStatisticsView, self).__init__()
        self.__provincesDP = None
        return

    @process
    def setProxy(self, proxy, clanDossier):
        proxy.showWaiting()
        provinces = yield clanDossier.requestProvinces()
        isMyClan = clanDossier.isMyClan()
        hasProvinces = len(provinces) > 0
        if self.isDisposed():
            return
        headers = self._prepareHeaders(clanDossier.isMyClan(), hasProvinces)
        if isMyClan:
            listItemRendererLinkage = CLANS_ALIASES.CLAN_PROFILE_SELF_PROVINCE_RENDERER
        else:
            listItemRendererLinkage = CLANS_ALIASES.CLAN_PROFILE_PROVINCE_RENDERER
        data = {'rendererLinkage': listItemRendererLinkage,
         'headers': headers,
         'isListVisible': hasProvinces,
         'additionalText': text_styles.standard(_ms(CLANS.GLOBALMAPVIEW_TOTALINCOME, icon=icons.gold(), value=text_styles.gold(BigWorld.wg_getIntegralFormat(sum(map(operator.methodcaller('getRevenue'), provinces)))))),
         'isAdditionalTextVisible': hasProvinces and isMyClan,
         'noDataText': text_styles.highTitle(_ms(CLANS.GLOBALMAPVIEW_NOPROVINCE)),
         'isNoDataTextVisible': not hasProvinces}
        if hasProvinces:
            data['defaultSortField'] = _SORT_IDS.PROVINCE
            data['defaultSortDirection'] = 'ascending'
        self.as_setDataS(data)
        self.__provincesDP = _ClanProfileProvinceDataProvider(isMyClan)
        self.__provincesDP.setFlashObject(self.as_getDPS())
        self.__provincesDP.buildList(provinces)
        proxy.hideWaiting()

    def _dispose(self):
        if self.__provincesDP is not None:
            self.__provincesDP.fini()
            self.__provincesDP = None
        super(ClanProfileTableStatisticsView, self)._populate()
        return

    def _prepareHeaders(self, isMyClan, enabled):
        headers = [_packColumn(_SORT_IDS.FRONT, CLANS.GLOBALMAPVIEW_TABLE_FRONT, 200, CLANS.GLOBALMAPVIEW_TABLE_FRONT_TOOLTIP, enabled), _packColumn(_SORT_IDS.PROVINCE, CLANS.GLOBALMAPVIEW_TABLE_PROVINCE, 200, CLANS.GLOBALMAPVIEW_TABLE_PROVINCE_TOOLTIP, enabled), _packColumn(_SORT_IDS.MAP, CLANS.GLOBALMAPVIEW_TABLE_MAP, 200, CLANS.GLOBALMAPVIEW_TABLE_MAP_TOOLTIP, enabled)]
        if isMyClan:
            headers.extend([_packColumn(_SORT_IDS.PRIMETIME, CLANS.GLOBALMAPVIEW_TABLE_PRIMETIME, 130, CLANS.GLOBALMAPVIEW_TABLE_PRIMETIME_TOOLTIP, enabled, textAlign='right'), _packColumn(_SORT_IDS.DAYS, CLANS.GLOBALMAPVIEW_TABLE_DAYS, 130, CLANS.GLOBALMAPVIEW_TABLE_DAYS_TOOLTIP, enabled, textAlign='right'), _packColumn(_SORT_IDS.INCOME, CLANS.GLOBALMAPVIEW_TABLE_INCOME, 118, CLANS.GLOBALMAPVIEW_TABLE_INCOME, enabled, textAlign='right')])
        else:
            headers.extend([_packColumn(_SORT_IDS.PRIMETIME, CLANS.GLOBALMAPVIEW_TABLE_PRIMETIME, 200, CLANS.GLOBALMAPVIEW_TABLE_PRIMETIME_TOOLTIP, enabled, textAlign='right'), _packColumn(_SORT_IDS.DAYS, CLANS.GLOBALMAPVIEW_TABLE_DAYS, 178, CLANS.GLOBALMAPVIEW_TABLE_DAYS_TOOLTIP, enabled, textAlign='right')])
        return headers


class _ClanProfileProvinceDataProvider(SortableDAAPIDataProvider):

    def __init__(self, isMyClan):
        super(_ClanProfileProvinceDataProvider, self).__init__()
        self._list = []
        self.__mapping = {}
        self.__selectedID = None
        self.__isMyClan = isMyClan
        self.__dataList = []
        self.__sortMapping = {_SORT_IDS.FRONT: self.__getFront,
         _SORT_IDS.PROVINCE: self.__getProvinceName,
         _SORT_IDS.MAP: self.__getMap,
         _SORT_IDS.PRIMETIME: self.__getPrimeTime,
         _SORT_IDS.DAYS: self.__getDays,
         _SORT_IDS.INCOME: self.__getIncome}
        return

    @property
    def collection(self):
        return self._list

    @property
    def sortedCollection(self):
        return self._list

    def emptyItem(self):
        return None

    def clear(self):
        self._list = []
        self.__dataList = []
        self.__mapping.clear()
        self.__selectedID = None
        return

    def fini(self):
        self.clear()
        self._dispose()

    def getSelectedIdx(self):
        if self.__selectedID in self.__mapping:
            return self.__mapping[self.__selectedID]
        return -1

    def setSelectedID(self, id):
        self.__selectedID = id

    def getVO(self, index):
        vo = None
        if index > -1:
            try:
                vo = self.sortedCollection[index]
            except IndexError:
                LOG_ERROR('Item not found', index)

        return vo

    def buildList(self, provinces):
        self.clear()
        self.__dataList = provinces
        for p in provinces:
            self._list.append(self._makeVO(p))

    def rebuildList(self, cache):
        self.buildList(cache)
        self.refresh()

    def refreshItem(self, cache, clanDBID):
        isSelected = self.__selectedID == clanDBID
        self.buildList(cache)
        if isSelected and clanDBID not in self.__mapping:
            return True
        return False

    def pyGetSelectedIdx(self):
        return self.getSelectedIdx()

    def pySortOn(self, fields, order):
        super(_ClanProfileProvinceDataProvider, self).pySortOn(fields, order)
        if self.__dataList:
            self.__dataList = sortByFields(self._sort, self.__dataList, valueGetter=self.__sortingMethod)
            self.buildList(self.__dataList)
            self.refresh()

    def _makeVO(self, province):
        result = {'front': self.__getFront(province),
         'province': self.__getProvinceName(province),
         'map': self.__getMap(province),
         'primeTime': text_styles.main(province.getUserPrimeTime()),
         'days': text_styles.main(BigWorld.wg_getIntegralFormat(self.__getDays(province)))}
        if self.__isMyClan:
            result.update({'income': text_styles.gold(BigWorld.wg_getIntegralFormat(self.__getIncome(province))),
             'noIncomeIconVisible': not province.isHqConnected(),
             'noIncomeTooltip': CLANS.GLOBALMAPVIEW_NOINCOME_TOOLTIP})
        return result

    def __sortingMethod(self, item, field):
        valueGetter = self.__sortMapping[field]
        return valueGetter(item)

    def __getFront(self, province):
        return province.getFrontName()

    def __getProvinceName(self, province):
        return province.getName()

    def __getMap(self, province):
        return province.getArenaName()

    def __getPrimeTime(self, province):
        primeTime = province.getPrimeTime()
        return primeTime.hour * time_utils.ONE_MINUTE + primeTime.minute

    def __getDays(self, province):
        return province.getTurnsOwned()

    def __getIncome(self, province):
        return province.getRevenue()