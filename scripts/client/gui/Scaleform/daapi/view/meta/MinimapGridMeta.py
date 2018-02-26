# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/MinimapGridMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class MinimapGridMeta(BaseDAAPIComponent):

    def setClick(self, x, y):
        self._printOverrideError('setClick')

    def as_clickEnabledS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_clickEnabled(value)

    def as_addPointS(self, x, y):
        if self._isDAAPIInited():
            return self.flashObject.as_addPoint(x, y)