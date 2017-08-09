# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCLobbyViewMeta.py
from gui.Scaleform.daapi.view.lobby.LobbyView import LobbyView

class BCLobbyViewMeta(LobbyView):

    def startBattle(self):
        self._printOverrideError('startBattle')

    def onAnimationsComplete(self):
        self._printOverrideError('onAnimationsComplete')

    def as_setBootcampDataS(self, data):
        """
        :param data: Represented by BCLobbySettingsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setBootcampData(data)

    def as_showAnimatedS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_showAnimated(data)

    def as_setAppearConfigS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setAppearConfig(data)