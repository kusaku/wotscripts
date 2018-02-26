# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/StoreComponentMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class StoreComponentMeta(BaseDAAPIComponent):

    def requestTableData(self, nation, actionsSelected, type, filters):
        self._printOverrideError('requestTableData')

    def requestFilterData(self, filterType):
        self._printOverrideError('requestFilterData')

    def onShowInfo(self, itemCD):
        self._printOverrideError('onShowInfo')

    def getName(self):
        self._printOverrideError('getName')

    def onAddVehToCompare(self, itemCD):
        self._printOverrideError('onAddVehToCompare')

    def as_initFiltersDataS(self, nations, actionsFilterName):
        """
        :param nations: Represented by Array (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_initFiltersData(nations, actionsFilterName)

    def as_completeInitS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_completeInit()

    def as_updateS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_update()

    def as_setFilterTypeS(self, data):
        """
        :param data: Represented by ShopNationFilterDataVo (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setFilterType(data)

    def as_setSubFilterS(self, data):
        """
        :param data: Represented by ShopSubFilterData (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setSubFilter(data)

    def as_setFilterOptionsS(self, data):
        """
        :param data: Represented by FiltersDataVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setFilterOptions(data)

    def as_scrollPositionS(self, index):
        if self._isDAAPIInited():
            return self.flashObject.as_scrollPosition(index)

    def as_setVehicleCompareAvailableS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setVehicleCompareAvailable(value)

    def as_setActionAvailableS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setActionAvailable(value)