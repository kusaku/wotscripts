# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ClanSearchWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class ClanSearchWindowMeta(AbstractWindowView):

    def search(self, text):
        self._printOverrideError('search')

    def previousPage(self):
        self._printOverrideError('previousPage')

    def nextPage(self):
        self._printOverrideError('nextPage')

    def dummyButtonPress(self):
        self._printOverrideError('dummyButtonPress')

    def as_getDPS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getDP()

    def as_setInitDataS(self, data):
        """
        :param data: Represented by ClanSearchWindowInitDataVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_setStateDataS(self, data):
        """
        :param data: Represented by ClanSearchWindowStateDataVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setStateData(data)

    def as_setDummyS(self, data):
        """
        :param data: Represented by DummyVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setDummy(data)

    def as_setDummyVisibleS(self, visible):
        if self._isDAAPIInited():
            return self.flashObject.as_setDummyVisible(visible)