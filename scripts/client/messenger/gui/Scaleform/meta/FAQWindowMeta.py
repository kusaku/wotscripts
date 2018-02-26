# Embedded file name: scripts/client/messenger/gui/Scaleform/meta/FAQWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class FAQWindowMeta(AbstractWindowView):

    def onLinkClicked(self, name):
        self._printOverrideError('onLinkClicked')

    def as_appendTextS(self, text):
        if self._isDAAPIInited():
            return self.flashObject.as_appendText(text)