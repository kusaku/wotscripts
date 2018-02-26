# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/MissionsVehicleSelectorMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class MissionsVehicleSelectorMeta(BaseDAAPIComponent):

    def as_setInitDataS(self, data):
        """
        :param data: Represented by MissionVehicleSelectorVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_showSelectedVehicleS(self, vehData):
        """
        :param vehData: Represented by VehicleCarouselVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_showSelectedVehicle(vehData)

    def as_hideSelectedVehicleS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideSelectedVehicle()

    def as_closeS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_close()