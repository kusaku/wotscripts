# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/NYScreenViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class NYScreenViewMeta(BaseDAAPIComponent):

    def onSlotClick(self, slotID):
        self._printOverrideError('onSlotClick')

    def onHide(self):
        self._printOverrideError('onHide')

    def onShow(self):
        self._printOverrideError('onShow')

    def as_initS(self, slotsData):
        """
        :param slotsData: Represented by Vector.<NYToySlotVo> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_init(slotsData)

    def as_slotsIDS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_slotsID()

    def as_slotsPositionS(self, x1, x2):
        if self._isDAAPIInited():
            return self.flashObject.as_slotsPosition(x1, x2)

    def as_breakToyS(self, index):
        if self._isDAAPIInited():
            return self.flashObject.as_breakToy(index)