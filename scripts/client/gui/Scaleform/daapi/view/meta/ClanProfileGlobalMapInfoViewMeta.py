# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ClanProfileGlobalMapInfoViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class ClanProfileGlobalMapInfoViewMeta(BaseDAAPIComponent):

    def as_setDataS(self, data):
        """
        :param data: Represented by ClanProfileGlobalMapInfoVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)