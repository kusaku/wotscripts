# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/VehicleBuyWindowMeta.py
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class VehicleBuyWindowMeta(AbstractWindowView):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends AbstractWindowView
    """

    def submit(self, data):
        self._printOverrideError('submit')

    def selectTab(self, tabIndex):
        self._printOverrideError('selectTab')

    def onTradeInClearVehicle(self):
        self._printOverrideError('onTradeInClearVehicle')

    def as_setGoldS(self, gold):
        if self._isDAAPIInited():
            return self.flashObject.as_setGold(gold)

    def as_setCreditsS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setCredits(value)

    def as_setEnabledSubmitBtnS(self, enabled):
        if self._isDAAPIInited():
            return self.flashObject.as_setEnabledSubmitBtn(enabled)

    def as_setInitDataS(self, data):
        """
        :param data: Represented by VehicleBuyVo (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_updateTradeOffVehicleS(self, vehicleBuyTradeOffVo):
        """
        :param vehicleBuyTradeOffVo: Represented by VehicleBuyTradeOffVo (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateTradeOffVehicle(vehicleBuyTradeOffVo)

    def as_setTradeInWarningMessagegeS(self, message):
        if self._isDAAPIInited():
            return self.flashObject.as_setTradeInWarningMessagege(message)