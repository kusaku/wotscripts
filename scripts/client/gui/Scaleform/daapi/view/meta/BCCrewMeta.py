# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCCrewMeta.py
from gui.Scaleform.daapi.view.lobby.hangar.Crew import Crew

class BCCrewMeta(Crew):

    def onTankmanClick(self, slotIndex):
        self._printOverrideError('onTankmanClick')

    def onDropDownClosed(self, slotIndex):
        self._printOverrideError('onDropDownClosed')