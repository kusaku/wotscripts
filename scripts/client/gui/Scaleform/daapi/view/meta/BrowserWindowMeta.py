# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BrowserWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class BrowserWindowMeta(AbstractWindowView):

    def as_configureS(self, title, showActionBtn, showCloseBtn, isSolidBorder):
        if self._isDAAPIInited():
            return self.flashObject.as_configure(title, showActionBtn, showCloseBtn, isSolidBorder)

    def as_setSizeS(self, width, height):
        if self._isDAAPIInited():
            return self.flashObject.as_setSize(width, height)