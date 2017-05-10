# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RankedBattlesPrimeTimeMeta.py
from gui.Scaleform.framework.entities.View import View

class RankedBattlesPrimeTimeMeta(View):

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

    def as_setSelectedServerIndexS(self, index):
        if self._isDAAPIInited():
            return self.flashObject.as_setSelectedServerIndex(index)

    def as_getServersDPS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getServersDP()