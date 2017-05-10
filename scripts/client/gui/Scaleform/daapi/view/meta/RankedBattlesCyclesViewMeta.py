# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RankedBattlesCyclesViewMeta.py
from gui.Scaleform.daapi.view.meta.WrapperViewMeta import WrapperViewMeta

class RankedBattlesCyclesViewMeta(WrapperViewMeta):

    def onCloseBtnClick(self):
        self._printOverrideError('onCloseBtnClick')

    def onEscapePress(self):
        self._printOverrideError('onEscapePress')

    def onTabClick(self, tabID):
        self._printOverrideError('onTabClick')

    def onLadderBtnClick(self):
        self._printOverrideError('onLadderBtnClick')

    def as_setDataS(self, data):
        """
        :param data: Represented by RankedBattlesCyclesViewVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_updateTabContentS(self, data):
        """
        :param data: Represented by RankedBattlesCyclesViewVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateTabContent(data)