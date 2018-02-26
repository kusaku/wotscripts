# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/FMStatsMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class FMStatsMeta(BaseDAAPIComponent):

    def as_setSubTypeS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setSubType(value)