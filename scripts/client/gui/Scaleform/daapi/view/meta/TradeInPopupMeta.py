# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/TradeInPopupMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.popover.SmartPopOverView import SmartPopOverView

class TradeInPopupMeta(SmartPopOverView):

    def onSelectVehicle(self, index):
        self._printOverrideError('onSelectVehicle')

    def as_setInitDataS(self, data):
        """
        :param data: Represented by TradeInVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_getDPS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getDP()