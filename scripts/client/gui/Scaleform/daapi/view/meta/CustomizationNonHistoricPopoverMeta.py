# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/CustomizationNonHistoricPopoverMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.popover.SmartPopOverView import SmartPopOverView

class CustomizationNonHistoricPopoverMeta(SmartPopOverView):

    def remove(self, id):
        self._printOverrideError('remove')

    def removeAll(self):
        self._printOverrideError('removeAll')

    def as_setHeaderDataS(self, data):
        """
        :param data: Represented by CustomizationItemPopoverHeaderVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setHeaderData(data)

    def as_getDPS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getDP()