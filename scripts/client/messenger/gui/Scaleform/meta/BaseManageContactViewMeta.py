# Embedded file name: scripts/client/messenger/gui/Scaleform/meta/BaseManageContactViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from messenger.gui.Scaleform.view.lobby.BaseContactView import BaseContactView

class BaseManageContactViewMeta(BaseContactView):

    def checkText(self, txt):
        self._printOverrideError('checkText')

    def as_setLabelS(self, msg):
        if self._isDAAPIInited():
            return self.flashObject.as_setLabel(msg)

    def as_setInputTextS(self, msg):
        if self._isDAAPIInited():
            return self.flashObject.as_setInputText(msg)