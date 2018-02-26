# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/PrebattleTimerMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class PrebattleTimerMeta(BaseDAAPIComponent):

    def as_setTimerS(self, totalTime):
        if self._isDAAPIInited():
            return self.flashObject.as_setTimer(totalTime)

    def as_setMessageS(self, msg):
        if self._isDAAPIInited():
            return self.flashObject.as_setMessage(msg)

    def as_hideTimerS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideTimer()

    def as_hideAllS(self, speed):
        if self._isDAAPIInited():
            return self.flashObject.as_hideAll(speed)

    def as_setWinConditionTextS(self, msg):
        if self._isDAAPIInited():
            return self.flashObject.as_setWinConditionText(msg)