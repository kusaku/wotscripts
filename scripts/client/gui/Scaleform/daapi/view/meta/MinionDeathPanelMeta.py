# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/MinionDeathPanelMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class MinionDeathPanelMeta(BaseDAAPIComponent):

    def onBattleLoadCompleted(self):
        self._printOverrideError('onBattleLoadCompleted')

    def as_showPanelS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_showPanel()

    def as_hidePanelS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hidePanel()

    def as_updateDeadCountS(self, newValue, total):
        if self._isDAAPIInited():
            return self.flashObject.as_updateDeadCount(newValue, total)

    def as_initPanelS(self, data):
        """
        :param data: Represented by MinionDeathVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_initPanel(data)