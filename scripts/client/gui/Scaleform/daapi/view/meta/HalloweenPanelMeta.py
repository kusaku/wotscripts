# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/HalloweenPanelMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class HalloweenPanelMeta(BaseDAAPIComponent):

    def as_updateLeviathanProgressS(self, progress):
        if self._isDAAPIInited():
            return self.flashObject.as_updateLeviathanProgress(progress)

    def as_setObjectiveMsgS(self, msg):
        if self._isDAAPIInited():
            return self.flashObject.as_setObjectiveMsg(msg)