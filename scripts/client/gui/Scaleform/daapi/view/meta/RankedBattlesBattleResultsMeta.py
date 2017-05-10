# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RankedBattlesBattleResultsMeta.py
from gui.Scaleform.daapi.view.meta.WrapperViewMeta import WrapperViewMeta

class RankedBattlesBattleResultsMeta(WrapperViewMeta):

    def closeView(self):
        self._printOverrideError('closeView')

    def ready(self):
        self._printOverrideError('ready')

    def as_setDataS(self, data):
        """
        :param data: Represented by RankedBattleResultsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)