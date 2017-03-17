# Embedded file name: scripts/client/Helpers/sqlcache.py
import os
import sqlite3
import wgPickle
import base64
import locale
import time
from shutil import rmtree
from debug_utils import LOG_ERROR, LOG_DEBUG
from exchangeapi.IfaceUtils import getIface
DB_NAME = 'cache.dat'
CACHE_TABLE_NAME = 'cache'
CHECK_TABLE_EXIST = 'SELECT count(*) FROM sqlite_master WHERE type="table" AND name="%s"' % CACHE_TABLE_NAME
CREATE_TABLE = 'CREATE table %s (id INTEGER PRIMARY KEY, data BLOB, expiringTime FLOAT)' % CACHE_TABLE_NAME
GET_DATA = 'SELECT data, expiringTime FROM %s WHERE id = ?' % CACHE_TABLE_NAME
SET_DATA = 'INSERT OR REPLACE INTO %s VALUES (?, ?, ?)' % CACHE_TABLE_NAME
DELETE_DATA = 'DELETE FROM %s WHERE id = ?' % CACHE_TABLE_NAME
REINDEX = 'REINDEX'
VACUUM = 'VACUUM'
SQL_CONNECTION = None
CACHE_PATH = None
ID_TYPE = int
encoder = lambda data: base64.b64encode(wgPickle.dumps(wgPickle.FromClientToClient, data, compress=False))
decoder = lambda data: wgPickle.loads(wgPickle.FromClientToClient, base64.b64decode(data))

def init(cachePath):
    global CACHE_PATH
    CACHE_PATH = cachePath
    __createCacheStorage()


def destroy():
    global CACHE_PATH
    CACHE_PATH = None
    closeConnection()
    return


def openConnection():
    global SQL_CONNECTION
    if not SQL_CONNECTION:
        try:
            SQL_CONNECTION = sqlite3.connect(os.path.join(CACHE_PATH, DB_NAME).decode(locale.getpreferredencoding()))
            SQL_CONNECTION.execute('PRAGMA synchronous=OFF')
            SQL_CONNECTION.execute('PRAGMA locking_mode = EXCLUSIVE')
            SQL_CONNECTION.execute('PRAGMA temp_store=MEMORY')
            SQL_CONNECTION.execute('PRAGMA journal_mode = OFF')
            __createCacheStorage()
        except sqlite3.Error as msg:
            LOG_ERROR(msg)
            if SQL_CONNECTION:
                SQL_CONNECTION.close()
            SQL_CONNECTION = None
            if os.path.isfile(os.path.join(CACHE_PATH, DB_NAME)):
                os.remove(os.path.join(CACHE_PATH, DB_NAME))
            return openConnection()

    return SQL_CONNECTION


def closeConnection():
    global SQL_CONNECTION
    if SQL_CONNECTION:
        SQL_CONNECTION.close()
        SQL_CONNECTION = None
    return


def sqlExecute(query, args = (), needForCommit = False):
    if not SQL_CONNECTION:
        openConnection()
    result = True
    cursor = None
    try:
        cursor = SQL_CONNECTION.execute(query, args)
        if needForCommit:
            SQL_CONNECTION.commit()
        else:
            result = cursor.fetchone()
            if not result:
                result = None
            elif len(result) == 1:
                result = result[0]
    except sqlite3.Error as msg:
        LOG_ERROR('SQL Lite Error:', msg, query)
        try:
            restoreCache()
        except:
            deleteCache()
            init(CACHE_PATH)

        sqlExecute(query, args, needForCommit)

    return result


def __createCacheStorage():
    if not os.path.exists(CACHE_PATH):
        os.makedirs(CACHE_PATH)
    if not sqlExecute(CHECK_TABLE_EXIST):
        sqlExecute(CREATE_TABLE)
    else:
        reindexAndVacuum()


def getFromCache(cacheID, expiringTime):
    data, dataTime = sqlExecute(GET_DATA, (cacheID,)) or (None, None)
    if expiringTime and dataTime and time.time() >= dataTime + expiringTime:
        data = None
        deleteFromCache(cacheID)
    if data:
        try:
            return decoder(data)
        except:
            data = None
            deleteFromCache(cacheID)

    return data


def setToCache(cacheID, data):
    return sqlExecute(SET_DATA, (cacheID, encoder(data), time.time()), True)


def deleteFromCache(cacheID):
    return sqlExecute(DELETE_DATA, (cacheID,), True)


def reindexAndVacuum():
    sqlExecute(VACUUM)
    sqlExecute(REINDEX)


def deleteCache():
    if os.path.exists(CACHE_PATH):
        closeConnection()
        _rmFiles()
        LOG_DEBUG('SQL cache invalidated. path: %s' % CACHE_PATH)


def _rmFiles(retries = 10):
    for ret in xrange(retries):
        try:
            rmtree(CACHE_PATH)
            break
        except WindowsError:
            time.sleep(1)
            LOG_ERROR("Can't delete cache {}, retry: {}".format(CACHE_PATH, ret))


def restoreCache():
    dbPath = os.path.join(CACHE_PATH, DB_NAME)
    backupPath = os.path.join(CACHE_PATH, 'backup.dat')
    backupConnection = sqlite3.connect(backupPath)

    def dump():
        try:
            for i in SQL_CONNECTION.iterdump():
                yield i

        except sqlite3.Error:
            yield 'END TRANSACTION;'

    try:
        backupConnection.executescript('\n'.join(dump()))
    except:
        backupConnection.close()
        raise

    backupConnection.close()
    closeConnection()
    os.remove(dbPath)
    os.rename(backupPath, dbPath)
    init(CACHE_PATH)
    LOG_DEBUG('SQL cache restored. path: %s' % CACHE_PATH)