# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/NYScreenMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class NYScreenMeta(View):

    def onClose(self):
        self._printOverrideError('onClose')

    def onTabButtonClick(self, tabID):
        self._printOverrideError('onTabButtonClick')

    def onAwardsButtonClick(self):
        self._printOverrideError('onAwardsButtonClick')

    def onCraftButtonClick(self):
        self._printOverrideError('onCraftButtonClick')

    def onCollectionButtonClick(self):
        self._printOverrideError('onCollectionButtonClick')

    def onToyFragmentButtonClick(self):
        self._printOverrideError('onToyFragmentButtonClick')

    def moveSpace(self, x, y, delta):
        self._printOverrideError('moveSpace')

    def as_initS(self, nyData):
        """
        :param nyData: Represented by NYScreenDataVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_init(nyData)

    def as_enableBtnsS(self, isEnable):
        if self._isDAAPIInited():
            return self.flashObject.as_enableBtns(isEnable)

    def as_showViewByIdS(self, tabID):
        if self._isDAAPIInited():
            return self.flashObject.as_showViewById(tabID)

    def as_updateNYAwardsCounterS(self, counter):
        if self._isDAAPIInited():
            return self.flashObject.as_updateNYAwardsCounter(counter)

    def as_updateNYBoxCounterS(self, counter):
        if self._isDAAPIInited():
            return self.flashObject.as_updateNYBoxCounter(counter)

    def as_updateNYLevelS(self, level):
        if self._isDAAPIInited():
            return self.flashObject.as_updateNYLevel(level)

    def as_updateNYProgressS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_updateNYProgress(value)

    def as_updateNYTOYFragmentS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_updateNYTOYFragment(value)

    def as_setTabButtonCounterS(self, id, counter):
        if self._isDAAPIInited():
            return self.flashObject.as_setTabButtonCounter(id, counter)

    def as_onBreakStartS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_onBreakStart()

    def as_onBreakS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_onBreak()

    def as_onBreakFailS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_onBreakFail()