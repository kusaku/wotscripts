# Embedded file name: scripts/client/gui/Scaleform/utils/RSSDownloader.py
__author__ = 's_karchavets'
import threading
import BigWorld
import ResMgr
from Helpers import feedparser
from debug_utils import LOG_CURRENT_EXCEPTION
from gui.Version import Version
_CLIENT_VERSION = Version().getVersion()
feedparser.PARSE_MICROFORMATS = 0
feedparser.SANITIZE_HTML = 0

class RSSDownloader:
    UPDATE_INTERVAL = 0.1
    MIN_INTERVAL_BETWEEN_DOWNLOAD = 60.0

    def __init__(self):
        self.__thread = None
        self.__lastDownloadTime = 0
        self.__cbID = BigWorld.callback(RSSDownloader.UPDATE_INTERVAL, self.__update)
        self.__lastRSS = {}
        self.__onCompleteCallbacks = set()
        return

    lastRSS = property(lambda self: self.__lastRSS)
    isBusy = property(lambda self: self.__thread is not None)

    def destroy(self):
        self.__lastRSS.clear()
        self.__lastRSS = None
        self.__thread = None
        self.__onCompleteCallbacks.clear()
        if self.__cbID is not None:
            BigWorld.cancelCallback(self.__cbID)
            self.__cbID = None
        return

    def download(self, callback, url):
        if callback is None:
            return
        else:
            if self.__thread is not None:
                self.__onCompleteCallbacks.add(callback)
            else:
                time = BigWorld.time()
                if self.__lastDownloadTime != 0 and time - self.__lastDownloadTime < RSSDownloader.MIN_INTERVAL_BETWEEN_DOWNLOAD:
                    callback(self.__lastRSS)
                else:
                    self.__lastDownloadTime = time
                    self.__thread = _WorkerThread(url)
                    self.__onCompleteCallbacks.add(callback)
            return

    def clearDownloadCallback(self, callback):
        if callback in self.__onCompleteCallbacks:
            self.__onCompleteCallbacks.remove(callback)

    def __update(self):
        self.__cbID = BigWorld.callback(RSSDownloader.UPDATE_INTERVAL, self.__update)
        if self.__thread is None or self.__thread.isAlive():
            return
        else:
            if self.__thread.result is not None:
                self.__lastRSS = self.__thread.result
            for callback in self.__onCompleteCallbacks:
                try:
                    callback(self.__lastRSS)
                except:
                    LOG_CURRENT_EXCEPTION()

            self.__onCompleteCallbacks = set()
            self.__thread = None
            return


class _WorkerThread(threading.Thread):

    def __init__(self, url):
        super(_WorkerThread, self).__init__()
        self.url = url
        self.result = None
        self.name = 'RSS Downloader thread'
        self.start()
        return

    def run(self):
        try:
            self.result = feedparser.parse(self.url, None, None, _CLIENT_VERSION)
        except:
            LOG_CURRENT_EXCEPTION()

        return


g_downloader = None

def init():
    global g_downloader
    g_downloader = RSSDownloader()