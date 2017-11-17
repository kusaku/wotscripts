# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/MissionsPageMeta.py
from gui.Scaleform.framework.entities.View import View

class MissionsPageMeta(View):

    def resetFilters(self):
        self._printOverrideError('resetFilters')

    def onTabSelected(self, alias):
        self._printOverrideError('onTabSelected')

    def onClose(self):
        self._printOverrideError('onClose')

    def as_setTabsDataProviderS(self, dataProvider):
        """
        :param dataProvider: Represented by DataProvider.<MissionTabVO> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setTabsDataProvider(dataProvider)

    def as_showFilterS(self, visible):
        if self._isDAAPIInited():
            return self.flashObject.as_showFilter(visible)

    def as_showFilterCounterS(self, countText, isFilterApplied):
        if self._isDAAPIInited():
            return self.flashObject.as_showFilterCounter(countText, isFilterApplied)

    def as_blinkFilterCounterS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_blinkFilterCounter()

    def as_setTabsCounterDataS(self, data):
        """
        :param data: Represented by Vector.<MissionTabCounterVO> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setTabsCounterData(data)