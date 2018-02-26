# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/NYScreenCraftMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class NYScreenCraftMeta(View):

    def onClose(self):
        self._printOverrideError('onClose')

    def onCraft(self):
        self._printOverrideError('onCraft')

    def onGetShards(self):
        self._printOverrideError('onGetShards')

    def onFilterChange(self, type, index):
        self._printOverrideError('onFilterChange')

    def onToyCreatePlaySound(self, level):
        self._printOverrideError('onToyCreatePlaySound')

    def as_setInitDataS(self, data):
        """
        :param data: Represented by NYCraftInitVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_setCraftButtonEnableS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setCraftButtonEnable(value)

    def as_setShardsButtonShineS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setShardsButtonShine(value)

    def as_updateShardsS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_updateShards(value)

    def as_setPriceS(self, value, enoughMoney):
        if self._isDAAPIInited():
            return self.flashObject.as_setPrice(value, enoughMoney)

    def as_setCraftS(self, data):
        """
        :param data: Represented by NYToyFilterItemVo (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setCraft(data)