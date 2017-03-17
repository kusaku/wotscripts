# Embedded file name: scripts/client/account_helpers/ClanEmblemsCache.py
import os
import time
import calendar
import base64
import urllib2
import BigWorld
import Settings
import threading
from debug_utils import *
from functools import partial
from gui.Version import Version
from clientConsts import ENABLE_CLAN_EMBLEMS
from debug_utils import LOG_DEBUG, LOG_CURRENT_EXCEPTION
import sqlite3
g_clanEmblemsCache = None
_EXPIRE_PERIOD = 300
_EMBLEM_TEMPLATE = 'clan_emblem_%s_%s.dds'
CLAN_EMBLEM_64X64 = 0
CLAN_EMBLEM_128X128 = 1
CLAN_EMBLEM_256X256 = 2
EMBLEM_MIP_LEVELS = [1, 7, 8]
ID_IDX = 0
SIZE_IDX = 1
LAST_MODIFIED_IDX = 2
EXPIRES_IDX = 3
FILE_IDX = 4

def makeHash(id, size):
    uid = str(id) + str(size)
    hash = base64.b32encode(uid)
    if len(hash) > 32:
        LOG_WARNING('makeHash: hash is too long!')
    return hash


def emblemSizeToStr(sz):
    if sz == CLAN_EMBLEM_64X64:
        return '64x64'
    if sz == CLAN_EMBLEM_128X128:
        return '128x128'
    if sz == CLAN_EMBLEM_256X256:
        return '256x256'


def _LOG_EXECUTING_TIME(startTime, methodName, deltaTime = 0.1):
    finishTime = time.time()
    if finishTime - startTime > deltaTime:
        LOG_WARNING('Method "%s" takes too much time %s' % (methodName, finishTime - startTime))


def parseHttpTime(t):
    if t is None:
        return
    elif type(t) == int:
        return t
    else:
        if type(t) == str:
            try:
                parts = t.split()
                weekdays = ['mon',
                 'tue',
                 'wed',
                 'thu',
                 'fri',
                 'sat',
                 'sun']
                months = ['jan',
                 'feb',
                 'mar',
                 'apr',
                 'may',
                 'jun',
                 'jul',
                 'aug',
                 'sep',
                 'oct',
                 'nov',
                 'dec']
                tm_wday = weekdays.index(parts[0][:3].lower())
                tm_day = int(parts[1])
                tm_month = months.index(parts[2].lower()) + 1
                tm_year = int(parts[3])
                tm = parts[4].split(':')
                tm_hour = int(tm[0])
                tm_min = int(tm[1])
                tm_sec = int(tm[2])
                t = calendar.timegm((tm_year,
                 tm_month,
                 tm_day,
                 tm_hour,
                 tm_min,
                 tm_sec,
                 tm_wday,
                 0,
                 -1))
            except Exception as e:
                LOG_WARNING('Failed to parse http time.', e, t)
                t = None

        return t


def makeHttpTime(dt):
    try:
        weekday = ['Mon',
         'Tue',
         'Wed',
         'Thu',
         'Fri',
         'Sat',
         'Sun'][dt.tm_wday]
        month = ['Jan',
         'Feb',
         'Mar',
         'Apr',
         'May',
         'Jun',
         'Jul',
         'Aug',
         'Sep',
         'Oct',
         'Nov',
         'Dec'][dt.tm_mon - 1]
        t = '%s, %02d %s %04d %02d:%02d:%02d GMT' % (weekday,
         dt.tm_mday,
         month,
         dt.tm_year,
         dt.tm_hour,
         dt.tm_min,
         dt.tm_sec)
    except Exception as e:
        LOG_ERROR(e, dt)
        t = None

    return t


def parseTimeStamp(s):
    tm = 0
    try:
        if type(s) == str and len(s) == 19:
            dd = int(s[0:2])
            mm = int(s[3:5])
            yy = int(s[6:10])
            hh = int(s[11:13])
            mmm = int(s[14:16])
            ss = int(s[17:19])
            tm = calendar.timegm((yy,
             mm,
             dd,
             hh,
             mmm,
             ss,
             -1,
             -1,
             -1))
    except:
        LOG_CURRENT_EXCEPTION()

    return tm


class NotModifiedHandler(urllib2.BaseHandler):

    def http_error_304(self, req, fp, code, message, headers):
        addinfourl = urllib2.addinfourl(fp, headers, req.get_full_url())
        addinfourl.code = code
        return addinfourl


class CFC_OP_TYPE:
    DOWNLOAD = 1
    SCAN = 2
    CHECK = 3


def ExtractIdAndSizeFromFileName(filename):
    id = size = None
    filename = filename.lower()
    if filename.startswith('clan_emblem_'):
        dot = filename.rfind('.')
        if dot > 0:
            infor_str = filename[12:dot]
            id_pos = infor_str.find('_')
            id = infor_str[0:id_pos]
            size_str = infor_str[id_pos + 1:]
            if size_str == '64x64':
                size = 0
            elif size_str == '128x128':
                size = 1
            elif size_str == '256x256':
                size = 2
    return (id, size)


def buildFileNameFromId(id, size):
    url = _EMBLEM_TEMPLATE % (id, emblemSizeToStr(size))
    return url


def buildUrlFromId(serverPath, id, size = CLAN_EMBLEM_256X256):
    idStr = str(id)
    url = serverPath + '/' + idStr + '/emblem_' + emblemSizeToStr(size) + '.png'
    return url


VERSION_TABLE_NAME = u'version'
EMBLEMS_TABLE_NAME = u'emblems'
CHECK_TABLE_EXIST = u'SELECT count(*) FROM sqlite_master WHERE type="table" AND name="%s"'
DROP_TABLE = u'drop table %s'
CHECK_VERSION_TABLE_EXIST = u'SELECT count(*) FROM sqlite_master WHERE type="table" AND name="%s"' % VERSION_TABLE_NAME
CHECK_EMBLEMS_TABLE_EXIST = u'SELECT count(*) FROM sqlite_master WHERE type="table" AND name="%s"' % EMBLEMS_TABLE_NAME
CREATE_VERSION_TABLE = u'CREATE table %s (version TEXT)' % VERSION_TABLE_NAME
CREATE_EMBLEMS_TABLE = u'CREATE table %s (id VARCHAR(32) PRIMARY KEY, id_clan INTEGER, size INTEGER, last_modified FLOAT, expires FLOAT, data BLOB)' % EMBLEMS_TABLE_NAME
GET_VERSION = u'SELECT version FROM %s' % VERSION_TABLE_NAME
SET_VERSION = u'INSERT OR REPLACE INTO %s VALUES (?)' % VERSION_TABLE_NAME
GET_EMBLEM = u'SELECT id_clan, size, last_modified, expires, data FROM %s WHERE id = ?' % EMBLEMS_TABLE_NAME
GET_EMBLEMS = u'SELECT id, id_clan, size, last_modified, expires, data FROM %s' % EMBLEMS_TABLE_NAME
SET_EMBLEMS_DATA = u'INSERT OR REPLACE INTO %s VALUES (?, ?, ?, ?, ?, ?)' % EMBLEMS_TABLE_NAME

class SQLiteEmblemDB:

    def __init__(self):
        self.__connection = None
        return

    def open(self, dbname):
        if self.__connection:
            raise Exception()
        try:
            self.__connection = sqlite3.connect(unicode(dbname).encode('utf-8', 'ignore'))
            self.__connection.execute(u'PRAGMA synchronous=OFF')
            self.__connection.execute(u'PRAGMA locking_mode = NORMAL')
            self.__connection.execute(u'PRAGMA temp_store=MEMORY')
            self.__connection.execute(u'PRAGMA journal_mode = OFF')
            if self.__isTable(VERSION_TABLE_NAME):
                version = self.__query(GET_VERSION)
                if version:
                    version = version[0]
                    if len(version) == 0 or version[0] != Version().getVersion():
                        self.__execute(DROP_TABLE % EMBLEMS_TABLE_NAME, (), True)
            else:
                self.__execute(CREATE_VERSION_TABLE, (), True)
            if not self.__isTable(EMBLEMS_TABLE_NAME):
                self.__execute(SET_VERSION, [unicode(Version().getVersion())], True)
                self.__execute(CREATE_EMBLEMS_TABLE, (), True)
        except sqlite3.Error as msg:
            LOG_ERROR(msg)
            if self.__connection:
                self.__connection.close()
            self.__connection = None
            if os.path.isfile(dbname):
                os.remove(dbname)

        return

    def insert(self, hash, id, size, last_modified, expires, data):
        if not self.__connection:
            return False
        return self.__execute(SET_EMBLEMS_DATA, [unicode(hash),
         id,
         size,
         last_modified,
         expires,
         unicode(data)], True)

    def update(self, hash, last_modified = None, expires = None, data = None):
        if not self.__connection:
            return False
        query = u''
        if last_modified:
            query += u'last_modified = "%s"' % unicode(last_modified)
        if expires:
            if query != u'':
                query += u', '
            query += u'expires = "%s"' % unicode(expires)
        if data:
            if query != u'':
                query += u', '
            query += u'data = "%s"' % unicode(data)
        query = u'update ' + EMBLEMS_TABLE_NAME + u' set ' + query + u' where id = "%s"' % unicode(hash)
        return self.__execute(query, (), True)

    def get_all(self):
        if not self.__connection:
            return False
        else:
            result = self.__query(GET_EMBLEMS, (), -1)
            if result and len(result) > 0:
                return result
            return None

    def get(self, hash):
        if not self.__connection:
            return False
        else:
            result = self.__query(GET_EMBLEM, [hash], 1)
            if result and len(result) == 1:
                return result[0]
            return None

    def close(self):
        if not self.__connection:
            return False
        else:
            self.__connection.close()
            self.__connection = None
            return True

    def __isTable(self, table):
        if not self.__connection:
            return False
        try:
            cursor = self.__connection.execute(CHECK_TABLE_EXIST % table)
            result = cursor.fetchone()
            if result:
                return result[0] > 0
        except sqlite3.Error as msg:
            LOG_ERROR('SQL Lite Error:', msg, query)

        return False

    def __execute(self, query, args = (), needForCommit = False):
        if not self.__connection:
            return -1
        try:
            cursor = self.__connection.execute(query, args)
            if needForCommit:
                self.__connection.commit()
            if hasattr(cursor, 'rowcount'):
                return cursor.rowcount
            return 0
        except sqlite3.Error as msg:
            LOG_ERROR('SQL Lite Error:', msg, query)

        return -1

    def __query(self, query, args = (), size = -1, needForCommit = False):
        if not self.__connection:
            return
        else:
            result = None
            try:
                cursor = self.__connection.cursor()
                cursor.execute(query, args)
                result = cursor.fetchall() if size == -1 else cursor.fetchmany(size)
                if not result:
                    result = None
            except sqlite3.Error as msg:
                LOG_ERROR('SQL Lite Error:', msg, query)

            return result


class ClanEmblemsCache(object):

    def __init__(self):
        global g_clanEmblemsCache
        self.__cache = {}
        self.__processedCache = {}
        self.__db = None
        self.__dbFileName = None
        g_clanEmblemsCache = self
        if not ENABLE_CLAN_EMBLEMS:
            return
        else:
            self.__prefsFilePath = BigWorld.getUserDataDirectory()
            self.__clanEmblemServerPath = Settings.g_instance.scriptConfig.clanEmblemsConfig.get('emblemServerPath', 'http://127.0.0.1:8080/')
            self.__clanEmblemCacheResDir = Settings.g_instance.scriptConfig.clanEmblemsConfig.get('emblemLocalDir', 'emblems')
            self.__cacheDir = os.path.join(os.path.dirname(self.__prefsFilePath), self.__clanEmblemCacheResDir)
            self.__cacheDir = os.path.normpath(self.__cacheDir)
            self.__mutex = threading.RLock()
            self.__dbFileName = os.path.join(self.__cacheDir, 'emblems.dat')
            self.__prepareCache()
            return

    def overrideEmblemServerPath(self, newPath):
        self.__clanEmblemServerPath = newPath

    def overrideEmblemLocalPath(self, newPath):
        self.close()
        self.__clanEmblemCacheResDir = newPath
        self.__cacheDir = os.path.join(os.path.dirname(self.__prefsFilePath), self.__clanEmblemCacheResDir)
        self.__cacheDir = os.path.normpath(self.__cacheDir)
        self.__dbFileName = os.path.join(self.__cacheDir, 'emblems.dat')
        self.__prepareCache()

    def close(self):
        if not ENABLE_CLAN_EMBLEMS:
            return
        self.__cache = {}
        self.__processedCache = {}
        self.__db.close()

    def cancellCallback(self, id, size = CLAN_EMBLEM_256X256):
        id_str = makeHash(id, size)
        if self.__processedCache.get(id_str) is not None:
            self.__processedCache[id_str] = []
        return

    def get(self, id, callback, useLocalOnly = False, size = CLAN_EMBLEM_256X256):
        if not ENABLE_CLAN_EMBLEMS:
            return False
        else:
            if self.__db is None:
                self.__prepareCache()
            hash = makeHash(id, size)
            item = self.__cache.get(hash, None)
            if useLocalOnly:
                if item is None:
                    return False
                else:
                    BigWorld.callback(0.001, partial(callback, int(id), file, size))
                    return
            processing = True if hash in self.__processedCache else False
            self.__processedCache.setdefault(hash, []).append(callback)
            if processing:
                return True
            if item is None:
                self.__readRemoteFile(id, None, size)
            else:
                id_clan, size, last_modified, expires, file = item
                fileName = os.path.basename(file)
                fullPath = os.path.join(self.__prefsFilePath, os.path.join(self.__clanEmblemCacheResDir, fileName))
                fileExists = os.path.isfile(fullPath)
                if not fileExists or expires < time.time():
                    self.__readRemoteFile(id, last_modified if fileExists else None, size)
                else:
                    self.__postTask(id, file, size)
            return True

    def __readRemoteFile(self, id, modified_time, size):
        url = buildUrlFromId(self.__clanEmblemServerPath, id, size)
        localPath = '\\' + self.__clanEmblemCacheResDir + '\\' + str(int(time.time())) + '_' + buildFileNameFromId(id, size)
        ifModifiedHeader = ['If-Modified-Since: ' + makeHttpTime(time.gmtime(modified_time))] if modified_time else None
        BigWorld.fetchURL(url, partial(self.__onReadRemoteFile, id, size, localPath), ifModifiedHeader)
        return

    def __onReadRemoteFile(self, id, size, localPath, response):
        responseCode = response.responseCode
        last_modified = response.fileTime
        body = response.body if responseCode == 200 else None
        if responseCode not in (200, 304):
            LOG_WARNING('__onReadRemoteFile, Error occurred. Release callbacks.')
            self.__postTask(id, None, size)
            return
        else:
            hash = makeHash(id, size)
            try:
                self.__mutex.acquire()
                expires = int(time.time()) + _EXPIRE_PERIOD
                if responseCode == 304:
                    item = self.__cache.get(hash)
                    if item:
                        if self.__db.update(hash, expires=expires):
                            self.__cache[hash] = (item[ID_IDX],
                             item[SIZE_IDX],
                             item[LAST_MODIFIED_IDX],
                             expires,
                             item[FILE_IDX])
                            self.__postTask(id, item[FILE_IDX], size)
                    else:
                        self.__postTask(id, None, size)
                else:
                    localPath = unicode(localPath).encode('utf-8', 'ignore')
                    file = (localPath, last_modified, expires)
                    if size == CLAN_EMBLEM_256X256:
                        width = 256
                        height = 256
                        safeWidth = 176
                        safeHeight = 176
                    elif size == CLAN_EMBLEM_128X128:
                        width = 128
                        height = 128
                        safeWidth = width
                        safeHeight = height
                    elif size == CLAN_EMBLEM_64X64:
                        width = 64
                        height = 64
                        safeWidth = width
                        safeHeight = height
                    else:
                        LOG_DEBUG('Wrong emblem size!')
                        return
                    BigWorld.connvertTextureToDDSAsync(body, localPath, width, height, safeWidth, safeHeight, EMBLEM_MIP_LEVELS[size], partial(self.__onConvertTexture, hash, id, size, last_modified, expires))
            except Exception as e:
                LOG_CURRENT_EXCEPTION()
            finally:
                self.__mutex.release()

            return

    def __onConvertTexture(self, hash, id, size, last_modified, expires, localPath):
        try:
            self.__mutex.acquire()
            if localPath:
                item = self.__cache.get(hash)
                if item:
                    oldFile = self.__cache[hash][FILE_IDX]
                    if oldFile and oldFile.startswith('\\' + self.__clanEmblemCacheResDir + '\\'):
                        oldFileName = os.path.basename(oldFile)
                        fullPath = os.path.join(self.__prefsFilePath, os.path.join(self.__clanEmblemCacheResDir, oldFileName))
                        if os.path.isfile(fullPath):
                            LOG_INFO('Deleting old file %s' % fullPath)
                            try:
                                os.remove(fullPath)
                            except:
                                LOG_WARNING('Failed to delete old file %s' % fullPath)

                    if self.__db.update(hash, expires=expires, data=localPath):
                        self.__cache[hash] = (item[ID_IDX],
                         item[SIZE_IDX],
                         item[LAST_MODIFIED_IDX],
                         expires,
                         localPath)
                elif self.__db.insert(hash, id, size, last_modified, expires, localPath):
                    self.__cache[hash] = (id,
                     size,
                     last_modified,
                     expires,
                     localPath)
                self.__postTask(id, localPath, size)
            else:
                self.__postTask(id, None, size)
        except Exception as e:
            LOG_CURRENT_EXCEPTION()
        finally:
            self.__mutex.release()

        return

    def __postTask(self, id, file, size):
        BigWorld.callback(0.001, partial(self.__onPostTask, int(id), file, size))

    def __onPostTask(self, id, file, size):
        cbs = self.__processedCache.pop(makeHash(id, size), [])
        for cb in cbs:
            cb(id, file, size)

    def __prepareCache(self):
        try:
            self.__cache = {}
            if not os.path.isdir(self.__cacheDir):
                os.makedirs(self.__cacheDir, 511)
            self.__db = SQLiteEmblemDB()
            self.__db.open(self.__dbFileName)
            items = self.__db.get_all()
            if items:
                for value in items:
                    hash = str(value[0])
                    self.__cache[hash] = (int(value[ID_IDX + 1]),
                     int(value[SIZE_IDX + 1]),
                     float(value[LAST_MODIFIED_IDX + 1]),
                     float(value[EXPIRES_IDX + 1]),
                     unicode(value[FILE_IDX + 1]).encode('utf-8', 'ignore'))

        except Exception as e:
            if self.__db is not None:
                try:
                    self.__db.close()
                except:
                    pass

            self.__db = None
            try:
                for f in os.listdir(self.__cacheDir):
                    os.remove(os.path.join(self.__cacheDir, f))

            except Exception as e:
                LOG_CURRENT_EXCEPTION()

        return