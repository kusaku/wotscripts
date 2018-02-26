# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/NYCraftPopoverMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.popover.SmartPopOverView import SmartPopOverView

class NYCraftPopoverMeta(SmartPopOverView):

    def filterChange(self, index, type):
        self._printOverrideError('filterChange')

    def as_setDataS(self, data):
        """
        :param data: Represented by NYCraftPopoverVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)