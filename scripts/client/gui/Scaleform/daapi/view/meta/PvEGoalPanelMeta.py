# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/PvEGoalPanelMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class PvEGoalPanelMeta(BaseDAAPIComponent):

    def onBattleLoadCompleted(self):
        self._printOverrideError('onBattleLoadCompleted')

    def as_showPanelS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_showPanel()

    def as_hidePanelS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hidePanel()

    def as_setMessageS(self, title, msg):
        if self._isDAAPIInited():
            return self.flashObject.as_setMessage(title, msg)