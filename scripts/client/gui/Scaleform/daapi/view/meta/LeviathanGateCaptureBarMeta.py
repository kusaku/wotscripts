# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/LeviathanGateCaptureBarMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class LeviathanGateCaptureBarMeta(BaseDAAPIComponent):

    def as_isColorBlindS(self, isTrue):
        if self._isDAAPIInited():
            return self.flashObject.as_isColorBlind(isTrue)

    def as_showS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_show()

    def as_hideS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hide()

    def as_setCommentS(self, comment):
        if self._isDAAPIInited():
            return self.flashObject.as_setComment(comment)

    def as_updateTimeDisplayS(self, formattedTimeString):
        if self._isDAAPIInited():
            return self.flashObject.as_updateTimeDisplay(formattedTimeString)

    def as_updateHealthS(self, val):
        if self._isDAAPIInited():
            return self.flashObject.as_updateHealth(val)

    def as_setLeviathanHealthS(self, maxHealth, currentHealth):
        if self._isDAAPIInited():
            return self.flashObject.as_setLeviathanHealth(maxHealth, currentHealth)