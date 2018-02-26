# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/EventBoardsAwardsOverlayMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class EventBoardsAwardsOverlayMeta(BaseDAAPIComponent):

    def changeFilter(self, id):
        self._printOverrideError('changeFilter')

    def as_setHeaderS(self, data):
        """
        :param data: Represented by EventBoardTableFilterVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setHeader(data)

    def as_setVehicleS(self, data):
        """
        :param data: Represented by VehicleVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setVehicle(data)

    def as_setDataS(self, data):
        """
        :param data: Represented by EventBoardsAwardsOverlayVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)