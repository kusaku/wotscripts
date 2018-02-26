# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/WrapperViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class WrapperViewMeta(View):

    def onWindowClose(self):
        self._printOverrideError('onWindowClose')

    def as_showWaitingS(self, msg, props):
        if self._isDAAPIInited():
            return self.flashObject.as_showWaiting(msg, props)

    def as_hideWaitingS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideWaiting()