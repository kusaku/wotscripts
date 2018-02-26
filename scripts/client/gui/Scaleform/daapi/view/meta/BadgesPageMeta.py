# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BadgesPageMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.meta.WrapperViewMeta import WrapperViewMeta

class BadgesPageMeta(WrapperViewMeta):

    def onCloseView(self):
        self._printOverrideError('onCloseView')

    def onSelectBadge(self, badgeID):
        self._printOverrideError('onSelectBadge')

    def onDeselectBadge(self):
        self._printOverrideError('onDeselectBadge')

    def onDummyButtonPress(self):
        self._printOverrideError('onDummyButtonPress')

    def as_setStaticDataS(self, data):
        """
        :param data: Represented by BadgesStaticDataVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setStaticData(data)

    def as_setReceivedBadgesS(self, data):
        """
        :param data: Represented by BadgesGroupVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setReceivedBadges(data)

    def as_setNotReceivedBadgesS(self, data):
        """
        :param data: Represented by BadgesGroupVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setNotReceivedBadges(data)

    def as_setSelectedBadgeImgS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setSelectedBadgeImg(value)