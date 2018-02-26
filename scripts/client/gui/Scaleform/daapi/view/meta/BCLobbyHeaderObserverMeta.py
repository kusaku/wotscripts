# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCLobbyHeaderObserverMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class BCLobbyHeaderObserverMeta(BaseDAAPIComponent):

    def as_doEnableNavigationS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_doEnableNavigation()

    def as_showAnimatedS(self, data):
        """
        :param data: Represented by Vector.<String> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_showAnimated(data)

    def as_setBootcampDataS(self, data):
        """
        :param data: Represented by BCLobbySettingsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setBootcampData(data)

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