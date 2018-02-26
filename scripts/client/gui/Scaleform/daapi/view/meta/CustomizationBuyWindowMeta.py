# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/CustomizationBuyWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class CustomizationBuyWindowMeta(AbstractWindowView):

    def buy(self):
        self._printOverrideError('buy')

    def selectItem(self, id):
        self._printOverrideError('selectItem')

    def deselectItem(self, id):
        self._printOverrideError('deselectItem')

    def changePriceItem(self, id, priceMode):
        self._printOverrideError('changePriceItem')

    def applyToTankChanged(self, selected):
        self._printOverrideError('applyToTankChanged')

    def as_getPurchaseDPS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getPurchaseDP()

    def as_setInitDataS(self, data):
        """
        :param data: Represented by InitBuyWindowVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_setTotalDataS(self, data):
        """
        :param data: Represented by PurchasesTotalVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setTotalData(data)

    def as_setBuyBtnStateS(self, isEnabled, label):
        if self._isDAAPIInited():
            return self.flashObject.as_setBuyBtnState(isEnabled, label)