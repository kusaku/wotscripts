# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/LeviathanProgressPanelMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class LeviathanProgressPanelMeta(BaseDAAPIComponent):

    def as_updateLeviathanProgressS(self, progress):
        if self._isDAAPIInited():
            return self.flashObject.as_updateLeviathanProgress(progress)

    def as_updateLeviathanHealthS(self, percent):
        if self._isDAAPIInited():
            return self.flashObject.as_updateLeviathanHealth(percent)

    def as_setLeviathanHealthS(self, currHealth, maxHealth):
        if self._isDAAPIInited():
            return self.flashObject.as_setLeviathanHealth(currHealth, maxHealth)

    def as_isColorBlindS(self, isTrue):
        if self._isDAAPIInited():
            return self.flashObject.as_isColorBlind(isTrue)

    def as_hideS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hide()