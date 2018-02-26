# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCOutroVideoPageMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class BCOutroVideoPageMeta(View):

    def videoFinished(self):
        self._printOverrideError('videoFinished')

    def handleError(self, data):
        self._printOverrideError('handleError')

    def as_playVideoS(self, data):
        """
        :param data: Represented by BCOutroVideoVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_playVideo(data)