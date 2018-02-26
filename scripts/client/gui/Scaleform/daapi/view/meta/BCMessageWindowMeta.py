# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCMessageWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class BCMessageWindowMeta(View):

    def onMessageRemoved(self):
        self._printOverrideError('onMessageRemoved')

    def onMessageAppear(self, rendrerer):
        self._printOverrideError('onMessageAppear')

    def onMessageDisappear(self, rendrerer):
        self._printOverrideError('onMessageDisappear')

    def onMessageButtonClicked(self):
        self._printOverrideError('onMessageButtonClicked')

    def as_setMessageDataS(self, value):
        """
        :param value: Represented by Array (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setMessageData(value)