# Embedded file name: scripts/client/eventhandlers/refreshCarouselPlane.py
from functools import partial
import BWPersonality
from debug_utils import LOG_TRACE

def refreshCarouselPlane(event):
    planeID = next((iD for iD, typ in event.idTypeList if typ == 'plane'), None)
    if planeID is not None:
        if event.prevob and event.ob != event.prevob:
            carouselHelper = BWPersonality.g_lobbyCarouselHelper
            LOG_TRACE('refreshCarouselPlane()', planeID)
            carouselHelper.updateCarouselAirplane(planeID, partial(lambda carousel, planeID: carousel.onGetUpgradesList(callbacksList=[partial(carouselHelper.updateInBattleButton, True)]), carouselHelper), False, True, False)
        for upgName, upgCount in event.ob.get('updates', {}).iteritems():
            carouselHelper.inventory.setUpgradeCount(upgName, upgCount)

    return