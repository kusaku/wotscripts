# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/MissionDetailsContainerViewMeta.py
from gui.Scaleform.framework.entities.View import View

class MissionDetailsContainerViewMeta(View):

    def closeView(self):
        self._printOverrideError('closeView')

    def onChangePage(self, eventID):
        self._printOverrideError('onChangePage')

    def onTokenBuyClick(self, tokenId, questId):
        self._printOverrideError('onTokenBuyClick')

    def as_setInitDataS(self, data):
        """
        :param data: Represented by MissionDetailsContainerVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)