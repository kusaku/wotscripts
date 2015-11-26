# Embedded file name: scripts/client/gui/customization_2_0/controller.py
from carousel import Carousel
from data_aggregator import DataAggregator, CUSTOMIZATION_TYPE
from gui.shared.utils.HangarSpace import g_hangarSpace

class Controller(object):

    def __init__(self):
        self.__aData = None
        self.__carousel = None
        self.__header = None
        self.__cart = None
        return

    def init(self):
        self.__aData = DataAggregator()
        self.__carousel = Carousel(self.__aData)

    def fini(self):
        self.__carousel.fini()
        self.__aData.fini()
        self.__aData = None
        self.__carousel = None
        self.__header = None
        return

    def updateTank3DModel(self, isReset = False):
        if isReset:
            newViewData = self.__aData.initialViewModel
        else:
            newViewData = self.__aData.viewModel[1:3]
        g_hangarSpace.space.updateVehicleCamouflage(camouflageID=self.__aData.installed[CUSTOMIZATION_TYPE.CAMOUFLAGE][0].getID())
        g_hangarSpace.space.updateVehicleSticker(newViewData)

    @property
    def carousel(self):
        return self.__carousel


g_customizationController = Controller()