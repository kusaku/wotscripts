# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RankedBattlesBattleResultsMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.meta.WrapperViewMeta import WrapperViewMeta

class RankedBattlesBattleResultsMeta(WrapperViewMeta):

    def closeView(self):
        self._printOverrideError('closeView')

    def animationCheckBoxSelected(self, value):
        self._printOverrideError('animationCheckBoxSelected')

    def as_setDataS(self, data):
        """
        :param data: Represented by RankedBattleResultsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)