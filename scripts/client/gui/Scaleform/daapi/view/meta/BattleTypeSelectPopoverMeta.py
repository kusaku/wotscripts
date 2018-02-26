# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BattleTypeSelectPopoverMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.popover.SmartPopOverView import SmartPopOverView

class BattleTypeSelectPopoverMeta(SmartPopOverView):

    def selectFight(self, actionName):
        self._printOverrideError('selectFight')

    def demoClick(self):
        self._printOverrideError('demoClick')

    def getTooltipData(self, itemData, itemIsDisabled):
        self._printOverrideError('getTooltipData')

    def as_updateS(self, items, isShowDemonstrator, demonstratorEnabled):
        """
        :param items: Represented by DataProvider.<ItemSelectorRendererVO> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_update(items, isShowDemonstrator, demonstratorEnabled)

    def as_showMiniClientInfoS(self, description, hyperlink):
        if self._isDAAPIInited():
            return self.flashObject.as_showMiniClientInfo(description, hyperlink)