# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCLobbyObserverMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class BCLobbyObserverMeta(BaseDAAPIComponent):

    def onAnimationsComplete(self):
        self._printOverrideError('onAnimationsComplete')

    def registerAppearManager(self, component):
        self._printOverrideError('registerAppearManager')

    def as_setBootcampDataS(self, data):
        """
        :param data: Represented by BCLobbySettingsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setBootcampData(data)

    def as_showAnimatedS(self, data):
        """
        :param data: Represented by Vector.<String> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_showAnimated(data)

    def as_setAppearConfigS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setAppearConfig(data)