# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/PopOverViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.meta.WrapperViewMeta import WrapperViewMeta

class PopOverViewMeta(WrapperViewMeta):

    def as_setArrowDirectionS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setArrowDirection(value)

    def as_setArrowPositionS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setArrowPosition(value)