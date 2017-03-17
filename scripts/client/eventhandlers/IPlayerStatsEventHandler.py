# Embedded file name: scripts/client/eventhandlers/IPlayerStatsEventHandler.py
from functools import partial
import BigWorld
from consts import PLAYER_DOSSIER_CACHE_INVALIDATION_PERIOD
from debug_utils import LOG_DEBUG

def _invalidate(event):
    from Helpers.cache import deleteFromCache
    for pid in event.ob['planes']:
        idTypeList = [event.idTypeList[0], [pid, 'plane']]
        deleteFromCache(idTypeList, 'IPlayerShortPlaneStats')
        deleteFromCache(idTypeList, 'IPlayerPlaneStats')

    deleteFromCache(event.idTypeList, event.iface.ifacename)


def onPlayerStatsView(event):
    """
    @type event: exchangeapi.EventUtils.Event
    """
    if event.prevob is None:
        BigWorld.callback(PLAYER_DOSSIER_CACHE_INVALIDATION_PERIOD, partial(_invalidate, event))
    return