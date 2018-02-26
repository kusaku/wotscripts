# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ButtonWithCounterMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class ButtonWithCounterMeta(BaseDAAPIComponent):

    def as_setCountS(self, num):
        if self._isDAAPIInited():
            return self.flashObject.as_setCount(num)