# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/FreeSheetPopoverMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.popover.SmartPopOverView import SmartPopOverView

class FreeSheetPopoverMeta(SmartPopOverView):

    def onTaskClick(self, idx):
        self._printOverrideError('onTaskClick')

    def as_setDataS(self, data):
        """
        :param data: Represented by FreeSheetPopoverVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_setListDataProviderS(self, data):
        """
        :param data: Represented by DataProvider.<PawnedSheetVO> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setListDataProvider(data)