# Embedded file name: scripts/client/gui/Scaleform/BeforeStartScreen.py
from gui.Scaleform.Waiting import Waiting
from gui.Scaleform.windows import UIInterface

class BeforeStartScreen(UIInterface):

    def __init__(self):
        UIInterface.__init__(self)
        self.isModalMovie = False

    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.uiHolder.movie.backgroundAlpha = 0.0

    def dispossessUI(self):
        UIInterface.dispossessUI(self)