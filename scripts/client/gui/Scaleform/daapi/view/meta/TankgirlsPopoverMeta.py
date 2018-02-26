# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/TankgirlsPopoverMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.popover.SmartPopOverView import SmartPopOverView

class TankgirlsPopoverMeta(SmartPopOverView):

    def onRecruitClick(self, idx):
        self._printOverrideError('onRecruitClick')

    def as_setListDataProviderS(self, data):
        """
        :param data: Represented by DataProvider.<TankgirlVO> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setListDataProvider(data)