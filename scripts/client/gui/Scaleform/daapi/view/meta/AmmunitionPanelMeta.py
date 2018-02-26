# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/AmmunitionPanelMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.meta.ModulesPanelMeta import ModulesPanelMeta

class AmmunitionPanelMeta(ModulesPanelMeta):

    def showTechnicalMaintenance(self):
        self._printOverrideError('showTechnicalMaintenance')

    def showCustomization(self):
        self._printOverrideError('showCustomization')

    def toRentContinue(self):
        self._printOverrideError('toRentContinue')

    def as_setAmmoS(self, shells, stateWarning):
        """
        :param shells: Represented by Vector.<ShellButtonVO> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setAmmo(shells, stateWarning)

    def as_updateVehicleStatusS(self, data):
        """
        :param data: Represented by VehicleMessageVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateVehicleStatus(data)