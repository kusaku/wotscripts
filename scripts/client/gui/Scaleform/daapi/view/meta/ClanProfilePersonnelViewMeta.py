# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ClanProfilePersonnelViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.clans.profile.ClanProfileBaseView import ClanProfileBaseView

class ClanProfilePersonnelViewMeta(ClanProfileBaseView):

    def as_getMembersDPS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getMembersDP()