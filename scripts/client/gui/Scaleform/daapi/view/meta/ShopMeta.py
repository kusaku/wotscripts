# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ShopMeta.py
from gui.Scaleform.daapi.view.lobby.store.StoreComponent import StoreComponent

class ShopMeta(StoreComponent):

    def buyItem(self, itemCD, allowTradeIn):
        self._printOverrideError('buyItem')