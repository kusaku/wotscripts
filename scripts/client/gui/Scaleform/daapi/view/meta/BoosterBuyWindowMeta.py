# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BoosterBuyWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class BoosterBuyWindowMeta(AbstractWindowView):

    def buy(self, count):
        self._printOverrideError('buy')

    def setAutoRearm(self, autoRearm):
        self._printOverrideError('setAutoRearm')

    def as_setInitDataS(self, data):
        """
        :param data: Represented by BoosterBuyWindowVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_updateDataS(self, data):
        """
        :param data: Represented by BoosterBuyWindowUpdateVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateData(data)