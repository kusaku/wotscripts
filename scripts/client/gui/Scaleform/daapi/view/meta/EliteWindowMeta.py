# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/EliteWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class EliteWindowMeta(AbstractWindowView):

    def as_setVehicleS(self, vehicle):
        """
        :param vehicle: Represented by VehicleVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setVehicle(vehicle)