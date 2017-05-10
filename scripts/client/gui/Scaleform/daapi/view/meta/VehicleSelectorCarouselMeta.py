# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/VehicleSelectorCarouselMeta.py
from gui.Scaleform.daapi.view.lobby.vehicle_carousel.carousel_environment import CarouselEnvironment

class VehicleSelectorCarouselMeta(CarouselEnvironment):

    def setFilter(self, id):
        self._printOverrideError('setFilter')

    def as_initCarouselFilterS(self, data):
        """
        :param data: Represented by TankCarouselFilterInitVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_initCarouselFilter(data)