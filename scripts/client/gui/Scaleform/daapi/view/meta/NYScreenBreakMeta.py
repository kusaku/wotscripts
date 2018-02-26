# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/NYScreenBreakMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class NYScreenBreakMeta(View):

    def onClose(self):
        self._printOverrideError('onClose')

    def onBack(self):
        self._printOverrideError('onBack')

    def onBackClick(self):
        self._printOverrideError('onBackClick')

    def onCraftClick(self):
        self._printOverrideError('onCraftClick')

    def onBreak(self):
        self._printOverrideError('onBreak')

    def resetFilters(self):
        self._printOverrideError('resetFilters')

    def onToySelectChange(self, toyId, index, isSelected):
        self._printOverrideError('onToySelectChange')

    def as_setInitDataS(self, data):
        """
        :param data: Represented by NYScreenBreakVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_setBreakToyFragmentS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setBreakToyFragment(value)

    def as_setLackToyFragmentS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setLackToyFragment(value)

    def as_setBalanceToyFragmentS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setBalanceToyFragment(value)

    def as_setLackToyFragmentTypeS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setLackToyFragmentType(value)

    def as_setBreakButtonLabelS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setBreakButtonLabel(value)

    def as_setToysS(self, data):
        """
        :param data: Represented by DataProvider.<NYToyFilterItemVo> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setToys(data)

    def as_setBreakToysIndexS(self, data):
        """
        :param data: Represented by Vector.<int> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setBreakToysIndex(data)

    def as_setToysAmountStrS(self, value, isFilterActive):
        if self._isDAAPIInited():
            return self.flashObject.as_setToysAmountStr(value, isFilterActive)

    def as_onToysBreakFailedS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_onToysBreakFailed()

    def as_onToyBreakStartS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_onToyBreakStart()