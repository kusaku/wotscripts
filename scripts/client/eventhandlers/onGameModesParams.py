# Embedded file name: scripts/client/eventhandlers/onGameModesParams.py


def onGameModesParams(event):
    from gui.WindowsManager import g_windowsManager
    accountUI = g_windowsManager.getAccountUI()
    if accountUI:
        accountUI.onGameModesParams(event.ob)