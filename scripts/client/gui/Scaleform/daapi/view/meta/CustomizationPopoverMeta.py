# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/CustomizationPopoverMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class CustomizationPopoverMeta(BaseDAAPIComponent):

    def popupClosed(self):
        self._printOverrideError('popupClosed')