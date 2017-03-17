# Embedded file name: scripts/client/gui/Scaleform/Disconnect.py
import BigWorld, datetime
from gui.Scaleform.Waiting import Waiting
from Helpers.i18n import getFormattedTime, makeString, convert, localizeMessages, localizeMenu
from debug_utils import *
from gui import Cursor
from gui.Scaleform.windows import ModalWindow
import Settings

class _Disconnect(ModalWindow):

    def __init__(self):
        ModalWindow.__init__(self, 'disconnect.swf')
        self.component.position.z = -0.1
        self.movie.backgroundAlpha = 0.0
        self.addExternalCallback('logoff', self.logoff)

    def show(self, reason, isBan = None, expiryTime = None):
        BigWorld.disconnect()
        Cursor.forceShowCursor(True)
        message = ''
        if isBan:
            if reason.upper().startswith('#'):
                if len(reason) == 0:
                    reason = 'connection_lost'
                reason = makeString(reason.upper())
                if not isinstance(reason, unicode):
                    convert(reason)
            if expiryTime:
                strExpireTime = getFormattedTime(expiryTime)
                message = localizeMenu('LOGIN/STATUS/LOGIN_REJECTED_BAN')
                message = message % {'time': strExpireTime,
                 'reason': reason}
            else:
                message = localizeMenu('LOGIN/STATUS/LOGIN_REJECTED_BAN_UNLIMITED')
                message = message % {'reason': reason}
        else:
            message = localizeMessages('DISCONNECT/' + reason)
        self.call_1('setMessage', message, localizeMessages('DISCONNECT_TITLE'), localizeMessages('DISCONNECT_ENTER_BUTTON'))
        self.active(True)
        BigWorld.worldDrawEnabled(False)

    def logoff(self):

        def logOff():
            LOG_TRACE('logoff')
            Disconnect.hide()
            BigWorld.clearEntitiesAndSpaces()
            from gui.WindowsManager import g_windowsManager
            g_windowsManager.showLogin()

        BigWorld.callback(0.1, logOff)


class Disconnect:
    __window = None

    @staticmethod
    def show(reason = 'connection_lost', isBan = None, expiryTime = None):
        if Disconnect.__window is None:
            Disconnect.__window = _Disconnect()
            Disconnect.__window.show(reason, isBan, expiryTime)
            Waiting.hideAll()
        return

    @staticmethod
    def hide():
        if Disconnect.__window is not None:
            Disconnect.__window.close()
            Disconnect.__window = None
        return

    @staticmethod
    def getWindow():
        return Disconnect.__window