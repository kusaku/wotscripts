# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/VehicleCompareConfiguratorBaseViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class VehicleCompareConfiguratorBaseViewMeta(BaseDAAPIComponent):

    def applyConfig(self):
        self._printOverrideError('applyConfig')

    def resetConfig(self):
        self._printOverrideError('resetConfig')

    def onCloseView(self):
        self._printOverrideError('onCloseView')

    def as_setResetEnabledS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setResetEnabled(value)

    def as_setApplyEnabledS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setApplyEnabled(value)

    def as_setInitDataS(self, data):
        """
        :param data: Represented by VehicleCompareConfiguratorInitDataVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)