# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/MissionsTokenPopoverMeta.py
from gui.Scaleform.daapi.view.lobby.popover.SmartPopOverView import SmartPopOverView

class MissionsTokenPopoverMeta(SmartPopOverView):

    def onQuestClick(self, idx):
        self._printOverrideError('onQuestClick')

    def onBuyBtnClick(self):
        self._printOverrideError('onBuyBtnClick')

    def as_setStaticDataS(self, data):
        """
        :param data: Represented by MissionsTokenPopoverVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setStaticData(data)

    def as_setListDataProviderS(self, data):
        """
        :param data: Represented by DataProvider.<TokenRendererVO> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setListDataProvider(data)