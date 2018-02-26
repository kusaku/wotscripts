# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RankedBattlesWelcomeViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.meta.WrapperViewMeta import WrapperViewMeta

class RankedBattlesWelcomeViewMeta(WrapperViewMeta):

    def onCloseBtnClick(self):
        self._printOverrideError('onCloseBtnClick')

    def onNextBtnClick(self):
        self._printOverrideError('onNextBtnClick')

    def onEscapePress(self):
        self._printOverrideError('onEscapePress')

    def onAnimationFinished(self, forced):
        self._printOverrideError('onAnimationFinished')

    def onSoundTrigger(self, trigerName):
        self._printOverrideError('onSoundTrigger')

    def as_setDataS(self, data):
        """
        :param data: Represented by WelcomeViewVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)