# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/UseAwardSheetWindowMeta.py
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class UseAwardSheetWindowMeta(AbstractWindowView):

    def accept(self):
        self._printOverrideError('accept')

    def cancel(self):
        self._printOverrideError('cancel')

    def as_setSettingsS(self, value):
        """
        :param value: Represented by DialogSettingsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setSettings(value)

    def as_setDataS(self, value):
        """
        :param value: Represented by UseAwardSheetWindowVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(value)