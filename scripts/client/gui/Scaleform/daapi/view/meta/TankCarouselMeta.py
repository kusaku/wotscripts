# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/TankCarouselMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.vehicle_carousel.carousel_environment import CarouselEnvironment

class TankCarouselMeta(CarouselEnvironment):

    def buyTank(self):
        self._printOverrideError('buyTank')

    def buySlot(self):
        self._printOverrideError('buySlot')

    def setFilter(self, id):
        self._printOverrideError('setFilter')

    def updateHotFilters(self):
        self._printOverrideError('updateHotFilters')

    def as_setCarouselFilterS(self, data):
        """
        :param data: Represented by TankCarouselFilterSelectedVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setCarouselFilter(data)

    def as_initCarouselFilterS(self, data):
        """
        :param data: Represented by TankCarouselFilterInitVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_initCarouselFilter(data)

    def as_rowCountS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_rowCount(value)

    def as_setSmallDoubleCarouselS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setSmallDoubleCarousel(value)