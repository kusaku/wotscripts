# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCBattleResultTransitionMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class BCBattleResultTransitionMeta(BaseDAAPIComponent):

    def as_msgTypeHandlerS(self, status):
        if self._isDAAPIInited():
            return self.flashObject.as_msgTypeHandler(status)

    def as_updateStageS(self, width, height):
        if self._isDAAPIInited():
            return self.flashObject.as_updateStage(width, height)