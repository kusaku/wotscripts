# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/TradeInPopupMeta.py
from gui.Scaleform.daapi.view.lobby.popover.SmartPopOverView import SmartPopOverView

class TradeInPopupMeta(SmartPopOverView):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends SmartPopOverView
    """

    def onSelectVehicle(self, index):
        self._printOverrideError('onSelectVehicle')

    def as_setInitDataS(self, data):
        """
        :param data: Represented by TradeInVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_getDPS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getDP()