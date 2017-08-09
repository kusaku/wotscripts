# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCHangarMeta.py
from gui.Scaleform.daapi.view.lobby.hangar.Hangar import Hangar

class BCHangarMeta(Hangar):

    def as_setBootcampDataS(self, data):
        """
        :param data: Represented by BCLobbySettingsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setBootcampData(data)

    def as_showAnimatedS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_showAnimated(data)