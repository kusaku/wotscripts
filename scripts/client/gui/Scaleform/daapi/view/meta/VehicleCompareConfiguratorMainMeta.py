# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/VehicleCompareConfiguratorMainMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.meta.VehicleCompareCommonViewMeta import VehicleCompareCommonViewMeta

class VehicleCompareConfiguratorMainMeta(VehicleCompareCommonViewMeta):

    def as_showViewS(self, alias):
        if self._isDAAPIInited():
            return self.flashObject.as_showView(alias)