# Embedded file name: scripts/client/eventhandlers/responseEvents.py
from consts import EMPTY_IDTYPELIST, MAX_SENT_PKG_COUNT
from functools import partial
import BigWorld
from debug_utils import LOG_DEBUG
_CHAIN_CB_ID = None
_movieInited = False
_startQueried = False

def onMovieInitialized():
    global _startQueried
    global _movieInited
    _movieInited = True
    if _startQueried:
        startPackageChain()


def startPackageChain():
    global _startQueried
    global _CHAIN_CB_ID
    _startQueried = True
    if not _movieInited:
        return
    elif _CHAIN_CB_ID is not None:
        return
    else:
        from exchangeapi.AdapterUtils import getAdapter
        lastResponse = getAdapter('ILastProcessedResponse', ['account'])(None, None)
        rid = lastResponse['rid'] + 1
        LOG_DEBUG('Starting package chain, setting callback for package id: {0}'.format(rid))
        _execResponse([[rid, 'response']])
        return


def disposePackageChain():
    global _CHAIN_CB_ID
    if _CHAIN_CB_ID is not None:
        BigWorld.cancelCallback(_CHAIN_CB_ID)
        _CHAIN_CB_ID = None
    return


def responseAdded(event):
    from exchangeapi.AdapterUtils import getAdapter
    lastResponse = getAdapter('ILastProcessedResponse', ['account'])(None, None)
    currentId = event.idTypeList[0][0]
    if lastResponse['rid'] + 1 != currentId and (lastResponse['rid'] != MAX_SENT_PKG_COUNT or currentId != 1):
        LOG_DEBUG('Skipping package processing, received {0}, last processed {1}'.format(currentId, lastResponse['rid']))
        return
    elif _CHAIN_CB_ID is not None:
        LOG_DEBUG('Already processing package chain, skipping for {0}'.format(currentId))
        return
    else:
        LOG_DEBUG('Processing package chain, received {0}'.format(currentId))
        _execResponse(event.idTypeList)
        return


def responseDeleted(event):
    global _CHAIN_CB_ID
    from exchangeapi.AdapterUtils import getAdapter
    rid = event.idTypeList[0][0]
    getAdapter('ILastProcessedResponse', ['account']).edit(None, None, EMPTY_IDTYPELIST, {'rid': rid})
    if rid == MAX_SENT_PKG_COUNT:
        rid = 1
    else:
        rid += 1
    LOG_DEBUG('Setting callback for package id: {0}'.format(rid))
    _CHAIN_CB_ID = BigWorld.callback(0, partial(_execResponse, [[rid, 'response']]))
    return


def _execResponse(idTypeList):
    global _CHAIN_CB_ID
    if _CHAIN_CB_ID is not None:
        BigWorld.cancelCallback(_CHAIN_CB_ID)
        _CHAIN_CB_ID = None
    LOG_DEBUG('Executing package from chain, id: {0}'.format(idTypeList[0][0]))
    from exchangeapi.AdapterUtils import getAdapter
    getAdapter('IResponse', ['response']).delete(None, None, idTypeList)
    return