# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCLobbyHeaderMeta.py
from gui.Scaleform.daapi.view.lobby.header.LobbyHeader import LobbyHeader

class BCLobbyHeaderMeta(LobbyHeader):

    def BCLobbyViewMeta(self, ctx):
        self._printOverrideError('BCLobbyViewMeta')

    def startBattle(self):
        self._printOverrideError('startBattle')

    def as_doEnableNavigationS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_doEnableNavigation()

    def as_showAnimatedS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_showAnimated(data)

    def as_setHeaderButtonsS(self, data):
        """
        :param data: Represented by Array (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setHeaderButtons(data)

    def as_setHeaderKeysMapS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setHeaderKeysMap(data)

    def as_setMainMenuKeysMapS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setMainMenuKeysMap(data)