# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/VehicleInfoMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class VehicleInfoMeta(AbstractWindowView):

    def getVehicleInfo(self):
        self._printOverrideError('getVehicleInfo')

    def onCancelClick(self):
        self._printOverrideError('onCancelClick')

    def addToCompare(self):
        self._printOverrideError('addToCompare')

    def as_setVehicleInfoS(self, data):
        """
        :param data: Represented by VehicleInfoDataVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setVehicleInfo(data)

    def as_setCompareButtonDataS(self, data):
        """
        :param data: Represented by VehCompareButtonDataVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setCompareButtonData(data)