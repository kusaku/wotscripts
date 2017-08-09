# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCConsumablesPanelMeta.py
from gui.Scaleform.daapi.view.battle.shared.consumables_panel import ConsumablesPanel

class BCConsumablesPanelMeta(ConsumablesPanel):

    def as_setBigSizeS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setBigSize(value)