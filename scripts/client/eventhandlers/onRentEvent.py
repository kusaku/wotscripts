# Embedded file name: scripts/client/eventhandlers/onRentEvent.py
import BigWorld
from Helpers.cache import deleteFromCache
from exchangeapi.CommonUtils import idFromList, splitIDTypeList
from exchangeapi.UICallbackUtils import UI_CALLBACKS
from gui.WindowsManager import g_windowsManager
from debug_utils import LOG_ERROR
from functools import partial
RENT_CALLBACKS = {}

def _calculateUpdatePeriod():
    DEFAULT_PERIOD = 600
    ifacename = 'IRent'
    typeList = ['plane']
    from exchangeapi.AdapterUtils import getOblocationDBObject
    for rate in getattr(getOblocationDBObject(ifacename, typeList), 'requestsRate', []):
        if rate.method == 'view':
            return rate.timelapse

    return DEFAULT_PERIOD


UPDATER_PERIOD = _calculateUpdatePeriod()

def onRentEvent(event):
    global RENT_CALLBACKS
    planeID = event.idTypeList[0][0]
    if planeID not in RENT_CALLBACKS:
        _updateRentedPlane(planeID)
    elif event.ob['expiryTime'] <= 0:
        BigWorld.cancelCallback(RENT_CALLBACKS[planeID])
        del RENT_CALLBACKS[planeID]


def clearRentCallbacks():
    for cbID in RENT_CALLBACKS:
        BigWorld.cancelCallback(cbID)

    RENT_CALLBACKS.clear()


def _updateRentedPlane(planeID):
    ifacename = 'IRent'
    idTypeList = [[planeID, 'plane']]
    ids, types = map(idFromList, splitIDTypeList(idTypeList))
    deleteFromCache(idTypeList, ifacename)
    if set(UI_CALLBACKS.get(ids, {}).get(types, {}).get(ifacename, [])):
        accountUI = g_windowsManager.getAccountUI()
        if accountUI:
            accountUI.viewIFace([[{ifacename: {}}, idTypeList]])
        else:
            LOG_ERROR('accountUI is not ready. IRent not called')
    if planeID in RENT_CALLBACKS:
        BigWorld.cancelCallback(RENT_CALLBACKS[planeID])
    RENT_CALLBACKS[planeID] = BigWorld.callback(UPDATER_PERIOD, partial(_updateRentedPlane, planeID))