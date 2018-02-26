# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCPrebattleHintsMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class BCPrebattleHintsMeta(View):

    def as_setHintsVisibilityS(self, visible, hidden):
        """
        :param visible: Represented by Vector.<String> (AS)
        :param hidden: Represented by Vector.<String> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setHintsVisibility(visible, hidden)