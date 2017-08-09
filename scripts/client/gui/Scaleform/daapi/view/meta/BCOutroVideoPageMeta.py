# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCOutroVideoPageMeta.py
from gui.Scaleform.framework.entities.View import View

class BCOutroVideoPageMeta(View):

    def videoFinished(self):
        self._printOverrideError('videoFinished')

    def handleError(self, data):
        self._printOverrideError('handleError')

    def as_playVideoS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_playVideo(data)