# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/EventBoardsVehiclesOverlayMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class EventBoardsVehiclesOverlayMeta(BaseDAAPIComponent):

    def changeFilter(self, id):
        self._printOverrideError('changeFilter')

    def applyFilters(self, nation, vehicleType, level, isMain, hangarOnly):
        self._printOverrideError('applyFilters')

    def as_setHeaderS(self, data):
        """
        :param data: Represented by EventBoardTableFilterVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setHeader(data)

    def as_setFiltersS(self, data):
        """
        :param data: Represented by VehicleSelectorFilterVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setFilters(data)

    def as_setVehiclesS(self, data):
        """
        :param data: Represented by EventBoardsVehiclesOverlayVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setVehicles(data)