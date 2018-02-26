# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ConfirmDialogMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class ConfirmDialogMeta(AbstractWindowView):

    def submit(self, selected):
        self._printOverrideError('submit')

    def as_setSettingsS(self, data):
        """
        :param data: Represented by ConfirmDialogVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setSettings(data)