# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/MultiTurretHintPanelMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class MultiTurretHintPanelMeta(BaseDAAPIComponent):

    def onBattleLoadCompleted(self):
        self._printOverrideError('onBattleLoadCompleted')

    def as_showPanelS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_showPanel()

    def as_hidePanelS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hidePanel()

    def as_submitMessagesS(self, data):
        """
        :param data: Represented by MultiTurretHintVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_submitMessages(data)