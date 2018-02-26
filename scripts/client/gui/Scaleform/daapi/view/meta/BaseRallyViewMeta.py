# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BaseRallyViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.rally.AbstractRallyView import AbstractRallyView

class BaseRallyViewMeta(AbstractRallyView):

    def as_setCoolDownS(self, value, requestId):
        if self._isDAAPIInited():
            return self.flashObject.as_setCoolDown(value, requestId)