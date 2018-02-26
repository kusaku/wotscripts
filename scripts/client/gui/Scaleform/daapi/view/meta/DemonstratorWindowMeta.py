# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/DemonstratorWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class DemonstratorWindowMeta(AbstractWindowView):

    def onMapSelected(self, mapID):
        self._printOverrideError('onMapSelected')

    def as_setDataS(self, data):
        """
        :param data: Represented by DemonstratorVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)