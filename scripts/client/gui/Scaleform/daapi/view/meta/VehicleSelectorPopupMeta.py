# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/VehicleSelectorPopupMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class VehicleSelectorPopupMeta(AbstractWindowView):

    def onFiltersUpdate(self, nation, vehicleType, isMain, level, compatibleOnly):
        self._printOverrideError('onFiltersUpdate')

    def onSelectVehicles(self, items):
        self._printOverrideError('onSelectVehicles')

    def as_setFiltersDataS(self, data):
        """
        :param data: Represented by VehicleSelectorFilterVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setFiltersData(data)

    def as_setListDataS(self, listData, selectedItems):
        """
        :param listData: Represented by DataProvider.<VehicleSelectorItemVO> (AS)
        :param selectedItems: Represented by Array.<VehicleAlertVO> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setListData(listData, selectedItems)

    def as_setListModeS(self, isMultipleSelect):
        if self._isDAAPIInited():
            return self.flashObject.as_setListMode(isMultipleSelect)

    def as_setTextsS(self, titleText, infoText, selectButtonLabel, cancelButtonLabel):
        if self._isDAAPIInited():
            return self.flashObject.as_setTexts(titleText, infoText, selectButtonLabel, cancelButtonLabel)