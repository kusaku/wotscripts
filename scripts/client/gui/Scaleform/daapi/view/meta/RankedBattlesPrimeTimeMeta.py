# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RankedBattlesPrimeTimeMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.meta.WrapperViewMeta import WrapperViewMeta

class RankedBattlesPrimeTimeMeta(WrapperViewMeta):

    def closeView(self):
        self._printOverrideError('closeView')

    def apply(self):
        self._printOverrideError('apply')

    def selectServer(self, id):
        self._printOverrideError('selectServer')

    def as_setDataS(self, data):
        """
        :param data: Represented by PrimeTimeVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_getServersDPS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getServersDP()