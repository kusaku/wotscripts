# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/CyberSportIntroMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.rally.BaseRallyIntroView import BaseRallyIntroView

class CyberSportIntroMeta(BaseRallyIntroView):

    def requestVehicleSelection(self):
        self._printOverrideError('requestVehicleSelection')

    def startAutoMatching(self):
        self._printOverrideError('startAutoMatching')

    def showSelectorPopup(self):
        self._printOverrideError('showSelectorPopup')

    def showStaticTeamStaff(self):
        self._printOverrideError('showStaticTeamStaff')

    def as_setSelectedVehicleS(self, data):
        """
        :param data: Represented by IntroVehicleVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setSelectedVehicle(data)

    def as_setTextsS(self, data):
        """
        :param data: Represented by CSIntroViewTextsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setTexts(data)

    def as_setNoVehiclesS(self, warnTooltip):
        if self._isDAAPIInited():
            return self.flashObject.as_setNoVehicles(warnTooltip)