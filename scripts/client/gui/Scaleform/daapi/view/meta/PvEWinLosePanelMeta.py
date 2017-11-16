# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/PvEWinLosePanelMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class PvEWinLosePanelMeta(BaseDAAPIComponent):

    def as_setCombatEndStateS(self, data):
        """
        :param data: Represented by PvEWinLoseVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setCombatEndState(data)