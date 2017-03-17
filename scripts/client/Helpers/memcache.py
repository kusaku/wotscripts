# Embedded file name: scripts/client/Helpers/memcache.py
import time
MEMCACHE = {}
ID_TYPE = int

def getFromCache(cacheID, expiringTime):
    if cacheID in MEMCACHE:
        data, dataTime = MEMCACHE[cacheID]
        if expiringTime and time.time() >= dataTime + expiringTime:
            data = None
            deleteFromCache(cacheID)
        return data
    else:
        return


def setToCache(cacheID, data):
    MEMCACHE[cacheID] = (data, time.time())
    return True


def deleteFromCache(cacheID):
    return bool(MEMCACHE.pop(cacheID, None))


def deleteCache():
    MEMCACHE.clear()