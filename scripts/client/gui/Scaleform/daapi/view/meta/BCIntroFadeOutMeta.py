# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCIntroFadeOutMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class BCIntroFadeOutMeta(View):

    def finished(self):
        self._printOverrideError('finished')

    def as_startFadeoutS(self, animationTime):
        if self._isDAAPIInited():
            return self.flashObject.as_startFadeout(animationTime)