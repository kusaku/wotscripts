# Embedded file name: scripts/client/eventhandlers/onIGRChanged.py


def onIGRChanged(event):
    from BWPersonality import g_initPlayerInfo
    g_initPlayerInfo.igrRoomID = event.ob['roomID']
    g_initPlayerInfo.igrType = event.ob['type']