# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCBattleTopHintMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class BCBattleTopHintMeta(BaseDAAPIComponent):

    def animFinish(self):
        self._printOverrideError('animFinish')

    def as_showHintS(self, msgId, msgStr, isCompleted):
        if self._isDAAPIInited():
            return self.flashObject.as_showHint(msgId, msgStr, isCompleted)

    def as_hideHintS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideHint()

    def as_closeHintS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_closeHint()