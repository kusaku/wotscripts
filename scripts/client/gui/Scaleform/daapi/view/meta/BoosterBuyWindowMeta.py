# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BoosterBuyWindowMeta.py
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class BoosterBuyWindowMeta(AbstractWindowView):

    def buy(self, count):
        self._printOverrideError('buy')

    def as_setInitDataS(self, data):
        """
        :param data: Represented by BoosterBuyWindowVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_updateItemPriceDataS(self, data):
        """
        :param data: Represented by ItemPriceDataVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateItemPriceData(data)