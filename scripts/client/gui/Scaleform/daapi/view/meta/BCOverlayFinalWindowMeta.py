# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCOverlayFinalWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class BCOverlayFinalWindowMeta(View):

    def animFinish(self):
        self._printOverrideError('animFinish')

    def as_msgTypeHandlerS(self, msgType, status):
        if self._isDAAPIInited():
            return self.flashObject.as_msgTypeHandler(msgType, status)