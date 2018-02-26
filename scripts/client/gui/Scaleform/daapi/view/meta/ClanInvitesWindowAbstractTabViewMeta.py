# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ClanInvitesWindowAbstractTabViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.clans.invites.ClanInvitesViewWithTable import ClanInvitesViewWithTable

class ClanInvitesWindowAbstractTabViewMeta(ClanInvitesViewWithTable):

    def filterBy(self, filterName):
        self._printOverrideError('filterBy')

    def as_updateFilterStateS(self, data):
        """
        :param data: Represented by ClanInvitesWindowTableFilterVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateFilterState(data)