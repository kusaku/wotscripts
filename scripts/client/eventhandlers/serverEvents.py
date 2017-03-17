# Embedded file name: scripts/client/eventhandlers/serverEvents.py
import BWPersonality
from debug_utils import LOG_TRACE
import BigWorld

def onEventsChanged(event):
    if event.ob != event.prevob:
        player = BigWorld.player()
        from Account import PlayerAccount
        if player is not None and player.__class__ == PlayerAccount:
            if set(BWPersonality.g_initPlayerInfo.activeEvents).symmetric_difference(set(event.ob['activeEvents'])):
                BWPersonality.g_initPlayerInfo.activeEvents = event.ob['activeEvents']
                player.updateHangarSpace()
    return