# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/IngameHelpWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class IngameHelpWindowMeta(AbstractWindowView):

    def clickSettingWindow(self):
        self._printOverrideError('clickSettingWindow')

    def as_setKeysS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setKeys(data)