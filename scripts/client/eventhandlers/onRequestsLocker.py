# Embedded file name: scripts/client/eventhandlers/onRequestsLocker.py


def onRequestsLocker(event):
    from gui.WindowsManager import g_windowsManager
    import BigWorld
    accountUI = g_windowsManager.getAccountUI()
    if accountUI:
        for req in accountUI.requestsQueue:
            req()

    BigWorld.player().requestsAvailable = True