# Embedded file name: scripts/client/eventhandlers/planeCrewEventHandler.py
import BigWorld
from HelperFunctions import createIMessage
from consts import MESSAGE_TYPE

def onEditPlaneCrew(event):
    pump = event.ob['acceleratedCrewPumping']
    prevPump = getattr(event, 'prevob', None)
    if prevPump is None:
        prevPump = {}
    prevPump = prevPump.get('acceleratedCrewPumping', -1)
    if prevPump != -1 and pump != prevPump and pump >= 0:
        player = BigWorld.player()
        msgid, ob = createIMessage(MESSAGE_TYPE.CREW_EXP_PUMPING, dict(isPumping=pump))
        player.responseSender([[msgid, 'message']], 'IMessage', ob)
    return


def onSetToCachePlaneCrew(event):
    planeID = event.idTypeList[0][0]
    import BWPersonality
    lch = BWPersonality.g_lobbyCarouselHelper
    planeData = lch.getCarouselAirplaneSelected()
    if planeData and planeID == planeData.planeID:
        lch.checkLobbyCrewAnimation()