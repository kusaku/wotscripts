# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RankedBattlesCalendarPopoverMeta.py
from gui.Scaleform.daapi.view.lobby.popover.SmartPopOverView import SmartPopOverView

class RankedBattlesCalendarPopoverMeta(SmartPopOverView):

    def onDaySelect(self, date):
        self._printOverrideError('onDaySelect')

    def as_setDataS(self, data):
        """
        :param data: Represented by RankedBattlesCalendarVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_setDayDataS(self, data):
        """
        :param data: Represented by RankedBattlesCalendarDayVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setDayData(data)