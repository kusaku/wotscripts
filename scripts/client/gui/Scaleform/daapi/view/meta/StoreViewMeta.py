# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/StoreViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class StoreViewMeta(View):

    def onClose(self):
        self._printOverrideError('onClose')

    def onTabChange(self, tabId):
        self._printOverrideError('onTabChange')

    def onBackButtonClick(self):
        self._printOverrideError('onBackButtonClick')

    def as_showStorePageS(self, tabId):
        if self._isDAAPIInited():
            return self.flashObject.as_showStorePage(tabId)

    def as_initS(self, data):
        """
        :param data: Represented by StoreViewInitVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_init(data)

    def as_showBackButtonS(self, label, description):
        if self._isDAAPIInited():
            return self.flashObject.as_showBackButton(label, description)

    def as_hideBackButtonS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideBackButton()

    def as_setBtnTabCountersS(self, counters):
        """
        :param counters: Represented by Vector.<CountersVo> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setBtnTabCounters(counters)

    def as_removeBtnTabCountersS(self, counters):
        """
        :param counters: Represented by Vector.<String> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_removeBtnTabCounters(counters)