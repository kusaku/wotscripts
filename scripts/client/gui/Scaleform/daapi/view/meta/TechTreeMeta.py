# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/TechTreeMeta.py
from gui.Scaleform.daapi.view.lobby.techtree.ResearchView import ResearchView

class TechTreeMeta(ResearchView):

    def requestNationTreeData(self):
        self._printOverrideError('requestNationTreeData')

    def getNationTreeData(self, nationName):
        self._printOverrideError('getNationTreeData')

    def goToNextVehicle(self, vehCD):
        self._printOverrideError('goToNextVehicle')

    def onCloseTechTree(self):
        self._printOverrideError('onCloseTechTree')

    def request4VehCompare(self, vehCD):
        self._printOverrideError('request4VehCompare')

    def as_setAvailableNationsS(self, nations):
        """
        :param nations: Represented by DataProvider (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setAvailableNations(nations)

    def as_setSelectedNationS(self, nationName):
        if self._isDAAPIInited():
            return self.flashObject.as_setSelectedNation(nationName)

    def as_refreshNationTreeDataS(self, nationName):
        if self._isDAAPIInited():
            return self.flashObject.as_refreshNationTreeData(nationName)

    def as_setUnlockPropsS(self, data):
        """
        :param data: Represented by Array (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setUnlockProps(data)

    def as_hideNationsBarS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_hideNationsBar(value)

    def as_showMiniClientInfoS(self, description, hyperlink):
        if self._isDAAPIInited():
            return self.flashObject.as_showMiniClientInfo(description, hyperlink)