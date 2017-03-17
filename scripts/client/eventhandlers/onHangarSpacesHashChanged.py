# Embedded file name: scripts/client/eventhandlers/onHangarSpacesHashChanged.py
from Helpers.cache import setToCache
from consts import EMPTY_IDTYPELIST
from gui.WindowsManager import g_windowsManager

def onHangarSpacesHashChanged(event):
    import BWPersonality
    from clientConsts import GUI_TYPES
    activeEventsCRC32 = BWPersonality.g_settings.hangarSpaceSettings['eventsHash']
    if event.ob.get('hash', '') != activeEventsCRC32 and BWPersonality.g_initPlayerInfo.useGUIType == GUI_TYPES.PREMIUM:
        accountUI = g_windowsManager.getAccountUI()
        if accountUI:
            data = dict(hash=activeEventsCRC32)
            accountUI.editIFace([[{event.iface.ifacename: data}, EMPTY_IDTYPELIST]])
            setToCache(EMPTY_IDTYPELIST, event.iface.ifacename, data)