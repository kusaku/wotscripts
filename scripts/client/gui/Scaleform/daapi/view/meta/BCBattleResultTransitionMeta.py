# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCBattleResultTransitionMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class BCBattleResultTransitionMeta(BaseDAAPIComponent):

    def as_msgTypeHandlerS(self, status):
        if self._isDAAPIInited():
            return self.flashObject.as_msgTypeHandler(status)

    def as_updateStageS(self, width, height):
        if self._isDAAPIInited():
            return self.flashObject.as_updateStage(width, height)