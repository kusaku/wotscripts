# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/NYDecorationsPopoverMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.popover.SmartPopOverView import SmartPopOverView

class NYDecorationsPopoverMeta(SmartPopOverView):

    def onSlotClick(self, toyId, index):
        self._printOverrideError('onSlotClick')

    def goToTasks(self):
        self._printOverrideError('goToTasks')

    def onHideNew(self, toyId, index):
        self._printOverrideError('onHideNew')

    def onResetFilterClick(self):
        self._printOverrideError('onResetFilterClick')

    def onFilterChange(self, level, nation):
        self._printOverrideError('onFilterChange')

    def as_initFilterS(self, settingsData):
        """
        :param settingsData: Represented by Array (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_initFilter(settingsData)

    def as_setDataS(self, data, isInit):
        """
        :param data: Represented by NYDecorationsPopoverVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data, isInit)

    def as_setupS(self, arrowDirection):
        if self._isDAAPIInited():
            return self.flashObject.as_setup(arrowDirection)

    def as_breakToyS(self, index):
        if self._isDAAPIInited():
            return self.flashObject.as_breakToy(index)

    def as_breakToyFailS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_breakToyFail()

    def as_breakToyStartS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_breakToyStart()