# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCBattlePageMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.battle.classic.page import ClassicPage

class BCBattlePageMeta(ClassicPage):

    def onAnimationsComplete(self):
        self._printOverrideError('onAnimationsComplete')

    def as_showAnimatedS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_showAnimated(data)

    def as_setAppearConfigS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setAppearConfig(data)