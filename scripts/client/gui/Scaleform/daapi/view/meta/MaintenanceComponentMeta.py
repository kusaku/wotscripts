# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/MaintenanceComponentMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class MaintenanceComponentMeta(BaseDAAPIComponent):

    def refresh(self):
        self._printOverrideError('refresh')