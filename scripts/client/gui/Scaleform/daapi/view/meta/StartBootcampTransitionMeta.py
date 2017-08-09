# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/StartBootcampTransitionMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class StartBootcampTransitionMeta(BaseDAAPIComponent):

    def as_setTransitionTextS(self, text):
        if self._isDAAPIInited():
            return self.flashObject.as_setTransitionText(text)

    def as_updateStageS(self, width, height):
        if self._isDAAPIInited():
            return self.flashObject.as_updateStage(width, height)