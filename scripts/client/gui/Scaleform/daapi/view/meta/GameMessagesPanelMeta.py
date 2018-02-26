# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/GameMessagesPanelMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class GameMessagesPanelMeta(BaseDAAPIComponent):

    def onMessageStarted(self):
        self._printOverrideError('onMessageStarted')

    def onMessageEnded(self):
        self._printOverrideError('onMessageEnded')

    def as_addMessageS(self, messageVO):
        """
        :param messageVO: Represented by GameMessageVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_addMessage(messageVO)