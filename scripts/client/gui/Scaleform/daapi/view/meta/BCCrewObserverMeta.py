# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCCrewObserverMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class BCCrewObserverMeta(BaseDAAPIComponent):

    def onTankmanClick(self, slotIndex):
        self._printOverrideError('onTankmanClick')

    def onDropDownClosed(self, slotIndex):
        self._printOverrideError('onDropDownClosed')