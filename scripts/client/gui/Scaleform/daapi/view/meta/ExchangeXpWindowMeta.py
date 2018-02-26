# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ExchangeXpWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.exchange.BaseExchangeWindow import BaseExchangeWindow

class ExchangeXpWindowMeta(BaseExchangeWindow):

    def as_vehiclesDataChangedS(self, data):
        """
        :param data: Represented by ExchangeXPWindowVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_vehiclesDataChanged(data)

    def as_totalExperienceChangedS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_totalExperienceChanged(value)

    def as_setWalletStatusS(self, walletStatus):
        if self._isDAAPIInited():
            return self.flashObject.as_setWalletStatus(walletStatus)