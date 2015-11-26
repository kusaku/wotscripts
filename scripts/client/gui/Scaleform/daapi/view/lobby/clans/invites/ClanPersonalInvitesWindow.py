# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/clans/invites/ClanPersonalInvitesWindow.py
from gui.clans.clan_helpers import ClanListener
from gui.clans.settings import CLAN_CONTROLLER_STATES
from gui.Scaleform.daapi.view.meta.ClanPersonalInvitesWindowMeta import ClanPersonalInvitesWindowMeta
from gui.Scaleform.locale.CLANS import CLANS
from gui.shared.formatters import text_styles
from helpers.i18n import makeString as _ms

class ClanPersonalInvitesWindow(ClanPersonalInvitesWindowMeta, ClanListener):

    def __init__(self, *args):
        super(ClanPersonalInvitesWindow, self).__init__()

    def onClanStateChanged(self, oldStateID, newStateID):
        if not self.clansCtrl.isEnabled():
            self.onWindowClose()
        if not self.clansCtrl.isAvailable():
            pass

    def updateActualInvites(self, count):
        self.as_setActualInvitesTextS(_ms(CLANS.CLANPERSONALINVITESWINDOW_ACTUALINVITES, count=text_styles.stats(count)))

    def _populate(self):
        super(ClanPersonalInvitesWindow, self)._populate()
        self.startClanListening()

    def _dispose(self):
        super(ClanPersonalInvitesWindow, self)._dispose()
        self.stopClanListening()

    def _onRegisterFlashComponent(self, viewPy, alias):
        super(ClanPersonalInvitesWindow, self)._onRegisterFlashComponent(viewPy, alias)
        viewPy.setParentWindow(self)

    def onWindowClose(self):
        self.destroy()