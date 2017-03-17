# Embedded file name: scripts/client/Login.py
import BigWorld
from debug_utils import *
from gui.WindowsManager import g_windowsManager
from ConnectionManager import connectionManager

class PlayerLogin(BigWorld.Entity):

    def __init__(self):
        pass

    def onRepeatCheckOut(self, attemptsLeft):
        """
        callback when checkout failed
        @param attemptsLeft: checkout attempts count left
        """
        loginUI = g_windowsManager.loginUI
        if loginUI is not None:
            loginUI.onRepeatCheckOut(attemptsLeft)
        return

    def onBecomePlayer(self):
        pass

    def onBecomeNonPlayer(self):
        pass

    def receiveLoginQueueNumber(self, queueNumber):
        LOG_MX('receiveLoginQueueNumber', queueNumber)
        loginUI = g_windowsManager.loginUI
        if loginUI is not None:
            loginUI.receiveLoginQueueNumber(queueNumber)
        return

    def onKickedFromServer(self, checkoutPeripheryID):
        LOG_MX('onKickedFromServer', checkoutPeripheryID)
        from gui.Scaleform.Disconnect import Disconnect
        if checkoutPeripheryID == 0:
            Disconnect.show('#system_messages:checkout_error', False, 0)
        else:
            Disconnect.show('#system_messages:another_periphery', False, 0)

    def handleKeyEvent(self, event):
        return False

    def isGUIBlocked(self, event):
        return False


Login = PlayerLogin