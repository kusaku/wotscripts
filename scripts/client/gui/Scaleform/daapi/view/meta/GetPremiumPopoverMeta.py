# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/GetPremiumPopoverMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.popover.SmartPopOverView import SmartPopOverView

class GetPremiumPopoverMeta(SmartPopOverView):

    def onActionBtnClick(self, arenaUniqueID):
        self._printOverrideError('onActionBtnClick')

    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)