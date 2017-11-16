# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCIntroVideoPageMeta.py
from gui.Scaleform.framework.entities.View import View

class BCIntroVideoPageMeta(View):

    def videoFinished(self):
        self._printOverrideError('videoFinished')

    def goToBattle(self):
        self._printOverrideError('goToBattle')

    def skipBootcamp(self):
        self._printOverrideError('skipBootcamp')

    def handleError(self, data):
        self._printOverrideError('handleError')

    def as_playVideoS(self, data):
        """
        :param data: Represented by BCIntroVideoVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_playVideo(data)

    def as_updateProgressS(self, percent):
        if self._isDAAPIInited():
            return self.flashObject.as_updateProgress(percent)

    def as_loadedS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_loaded()

    def as_showIntroPageS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_showIntroPage(value)