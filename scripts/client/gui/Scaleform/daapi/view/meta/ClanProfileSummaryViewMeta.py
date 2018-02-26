# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ClanProfileSummaryViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.clans.profile.ClanProfileBaseView import ClanProfileBaseView

class ClanProfileSummaryViewMeta(ClanProfileBaseView):

    def hyperLinkGotoMap(self):
        self._printOverrideError('hyperLinkGotoMap')

    def hyperLinkGotoDetailsMap(self):
        self._printOverrideError('hyperLinkGotoDetailsMap')

    def sendRequestHandler(self):
        self._printOverrideError('sendRequestHandler')

    def as_updateStatusS(self, data):
        """
        :param data: Represented by ClanProfileSummaryViewStatusVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateStatus(data)

    def as_updateGeneralBlockS(self, data):
        """
        :param data: Represented by ClanProfileSummaryBlockVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateGeneralBlock(data)

    def as_updateFortBlockS(self, data):
        """
        :param data: Represented by ClanProfileSummaryBlockVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateFortBlock(data)

    def as_updateGlobalMapBlockS(self, data):
        """
        :param data: Represented by ClanProfileSummaryBlockVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateGlobalMapBlock(data)