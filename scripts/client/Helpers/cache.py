# Embedded file name: scripts/client/Helpers/cache.py
import zlib
import os
import sys
import tempfile
import BigWorld
from Helpers import memcache as memCacheUtility
from consts import EMPTY_IDTYPELIST
from exchangeapi._ifaces import CACHE_TYPE
from exchangeapi.IfaceUtils import getIface, IfaceNotFound, getChildIfaceNames
from debug_utils import LOG_ERROR, LOG_DEBUG
from Helpers import sqlcache as cacheUtility
from exchangeapi.CommonUtils import generateUUID, generateID, splitIDTypeList, idFromList
from Helpers.i18n import localizeLobby
from _functools import partial
from exchangeapi.UICallbackUtils import UI_CALLBACKS
SESSION_KEY = 'session_key'
SERVER_SESSION_KEY = 0
INITIALIZED = False
EXPIRING_CALLBACKS = []

def getPlayer():
    from Account import PlayerAccount
    player = BigWorld.player()
    if player != None and player.__class__ == PlayerAccount:
        return player
    else:
        LOG_ERROR('ResearchTreeHelper::getPlayer. Player =', player)
        return
        return


def getFromCache(idTypeList, ifaceName):
    global INITIALIZED
    if not INITIALIZED:
        LOG_ERROR('Cache is not initialized')
        return
    else:
        try:
            from exchangeapi.AdapterUtils import getOblocationDBObject
            _, typeList = splitIDTypeList(idTypeList)
            expiringTime = getOblocationDBObject(ifaceName, typeList).expiringTime
        except:
            expiringTime = None

        cacheID = generateID(idTypeList, ifaceName)
        data = memCacheUtility.getFromCache(cacheID, expiringTime)
        if data is None:
            data = cacheUtility.getFromCache(cacheID if cacheUtility.ID_TYPE == int else generateUUID(idTypeList, ifaceName), expiringTime)
            if data:
                memCacheUtility.setToCache(cacheID, data)
        return data


def getCacheIdsFromData(data):

    def formIds():
        for ifaces, idTypeList in data:
            for ifaceName in ifaces:
                yield generateID(idTypeList, ifaceName)

    return set(formIds())


def dataToId(data = None, ids = set()):
    return zlib.crc32('_'.join((str(item) for item in sorted(list(getCacheIdsFromData(data) if data else ids)))))


def setRespdataToCache(respdata, ids = None, cacheID = None):
    ids = ids or getCacheIdsFromData(respdata)
    cacheID = cacheID or dataToId(ids=ids)
    memCacheUtility.MEMCACHE.setdefault(0, {})[cacheID] = {'data': respdata,
     'ids': ids}
    return True


def getRespdataFromCache(requestdata):
    ids = getCacheIdsFromData(requestdata)
    cacheID = dataToId(ids=ids)
    return (ids, cacheID, memCacheUtility.MEMCACHE.get(0, {}).get(cacheID, {}).get('data', None))


def deleteRespDataFromCache(respdata = None, idTypeList = None, ifaceName = None):
    if respdata:
        return bool(memCacheUtility.MEMCACHE.get(0, {}).pop(dataToId(respdata), None))
    elif idTypeList and ifaceName:
        cacheIDs = getCacheIDsByParentIfaceName(idTypeList, ifaceName)
        for iD in [ iD for iD, respdata in memCacheUtility.MEMCACHE.get(0, {}).iteritems() if cacheIDs.intersection(respdata['ids']) ]:
            del memCacheUtility.MEMCACHE[0][iD]

        return True
    else:
        return False


def getCacheIDsByParentIfaceName(idTypeList, parentIfaceName):
    cacheIDs = set((generateID(idTypeList, ifaceName) for ifaceName in getChildIfaceNames(parentIfaceName)))
    cacheIDs.add(generateID(idTypeList, parentIfaceName))
    return cacheIDs


def updateRespDataInCache(idTypeList, ifaceName, data):
    cacheIDs = getCacheIDsByParentIfaceName(idTypeList, ifaceName)
    updated = False
    for respkey, respdata in memCacheUtility.MEMCACHE.get(0, {}).items():
        if cacheIDs.intersection(respdata['ids']):
            try:
                for ifaces, itemidTypeList in respdata['data']:
                    if idTypeList == [ [obid, obtype if obid or obtype != 'account' else None] for obid, obtype in itemidTypeList ]:
                        for iface in ifaces:
                            if ifaceName == iface or iface in getChildIfaceNames(ifaceName):
                                ifaces[iface].update(data)
                                updated = True

            except ValueError:
                LOG_ERROR('Got wrong data in cache, deleted for key: {0}, data: {1}'.format(respkey, respdata['data']))
                del memCacheUtility.MEMCACHE[0][respkey]
            except:
                LOG_ERROR('Got exception {0} ({1}). Cache deleted for key: {2}, data: {3}'.format(sys.exc_info()[0], sys.exc_info()[1], respkey, respdata['data']))
                del memCacheUtility.MEMCACHE[0][respkey]

    return updated


def setToCache(idTypeList, ifaceName, data, event = True):
    global EXPIRING_CALLBACKS
    if not INITIALIZED:
        LOG_ERROR('Cache is not initialized')
        return False
    else:
        try:
            cacheType = getIface(ifaceName).cacheType
        except IfaceNotFound:
            cacheType = CACHE_TYPE.FULL_CACHE

        if cacheType == CACHE_TYPE.NONE:
            return False
        try:
            from exchangeapi.AdapterUtils import getOblocationDBObject
            _, typeList = splitIDTypeList(idTypeList)
            expiringTime = getOblocationDBObject(ifaceName, typeList).expiringTime
        except:
            expiringTime = None

        if expiringTime:
            EXPIRING_CALLBACKS.append(BigWorld.callback(expiringTime, partial(actualizeCacheData, idTypeList, ifaceName)))
        cacheID = generateID(idTypeList, ifaceName)
        memCacheUtility.setToCache(cacheID, data)
        if cacheType == CACHE_TYPE.FULL_CACHE:
            cacheUtility.setToCache(cacheID if cacheUtility.ID_TYPE == int else generateUUID(idTypeList, ifaceName), data)
        if event:
            from exchangeapi.EventUtils import generateEvent
            generateEvent('', 'settocache', ifaceName, idTypeList, None, data, None)
        return True


def deleteFromCache(idTypeList, ifaceName):
    if not INITIALIZED:
        LOG_ERROR('Cache is not initialized')
        return False
    cacheID = generateID(idTypeList, ifaceName)
    memCacheUtility.deleteFromCache(cacheID)
    return cacheUtility.deleteFromCache(cacheID if cacheUtility.ID_TYPE == int else generateUUID(idTypeList, ifaceName))


def init():
    global INITIALIZED
    global SERVER_SESSION_KEY
    global EXPIRING_CALLBACKS
    player = getPlayer()
    if player:
        EXPIRING_CALLBACKS = []
        import BWPersonality
        cacheUtility.init(os.path.join(os.path.abspath(tempfile.gettempdir()), 'wargaming.net', 'wowp', 'cache', str(BWPersonality.g_initPlayerInfo.databaseID)))
        SERVER_SESSION_KEY = BWPersonality.g_initPlayerInfo.serverSessionKey
        LOG_DEBUG('Initialized server session key, {}'.format(SERVER_SESSION_KEY))
        INITIALIZED = True


def destroy():
    global INITIALIZED
    global EXPIRING_CALLBACKS
    INITIALIZED = False
    for callbackID in EXPIRING_CALLBACKS:
        BigWorld.cancelCallback(callbackID)

    EXPIRING_CALLBACKS = []
    memCacheUtility.deleteCache()
    cacheUtility.destroy()


def signByServerSessionKey(sessionKey):
    """Emulate signing key by concating global SERVER_SESSION_KEY and
    client sessionKey
    """
    return SERVER_SESSION_KEY + sessionKey


def getSessionKey():
    """Get sessionKey from cache on Client, using interface system"""
    return getFromCache(EMPTY_IDTYPELIST, SESSION_KEY)


def isSessionKeyValid(sessionKey):
    sessionKey = signByServerSessionKey(sessionKey)
    return sessionKey == getSessionKey()


def saveSessionKey(sessionKey):
    sessionKey = signByServerSessionKey(sessionKey)
    return setToCache(EMPTY_IDTYPELIST, SESSION_KEY, sessionKey, False)


def deleteCache():
    memCacheUtility.deleteCache()
    cacheUtility.deleteCache()
    init()
    setToCache(EMPTY_IDTYPELIST, 'ILocalizationLanguage', dict(lang=localizeLobby('LOCALIZATION_LANGUAGE')))


def actualizeCacheData(idTypeList, ifaceName):
    deleteFromCache(idTypeList, ifaceName)
    ids, types = map(idFromList, splitIDTypeList(idTypeList))
    deleteFromCache(idTypeList, ifaceName)
    if set(UI_CALLBACKS.get(ids, {}).get(types, {}).get(ifaceName, [])):
        from gui.WindowsManager import g_windowsManager
        accountUI = g_windowsManager.getAccountUI()
        if accountUI:
            accountUI.viewIFace([[{ifaceName: {}}, idTypeList]])
        else:
            LOG_ERROR("accountUI is not ready. data hasn't been updated on subscribed list")