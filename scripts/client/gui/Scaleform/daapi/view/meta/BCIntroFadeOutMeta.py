# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCIntroFadeOutMeta.py
from gui.Scaleform.framework.entities.View import View

class BCIntroFadeOutMeta(View):

    def finished(self):
        self._printOverrideError('finished')

    def handleError(self, data):
        self._printOverrideError('handleError')

    def as_StartFadeoutS(self, animationTime):
        if self._isDAAPIInited():
            return self.flashObject.as_StartFadeout(animationTime)