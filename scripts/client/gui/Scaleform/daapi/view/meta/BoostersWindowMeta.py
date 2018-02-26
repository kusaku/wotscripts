# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BoostersWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class BoostersWindowMeta(AbstractWindowView):

    def requestBoostersArray(self, tabIndex):
        self._printOverrideError('requestBoostersArray')

    def onBoosterActionBtnClick(self, boosterID, questID):
        self._printOverrideError('onBoosterActionBtnClick')

    def onFiltersChange(self, filters):
        self._printOverrideError('onFiltersChange')

    def onResetFilters(self):
        self._printOverrideError('onResetFilters')

    def as_setDataS(self, data):
        """
        :param data: Represented by BoostersWindowVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_setStaticDataS(self, data):
        """
        :param data: Represented by BoostersWindowStaticVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setStaticData(data)

    def as_setListDataS(self, boosters, scrollToTop):
        """
        :param boosters: Represented by DataProvider.<BoostersTableRendererVO> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setListData(boosters, scrollToTop)