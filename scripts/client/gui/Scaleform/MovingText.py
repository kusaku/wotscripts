# Embedded file name: scripts/client/gui/Scaleform/MovingText.py
__author__ = 's_karchavets'
import BigWorld
import time
from debug_utils import LOG_DEBUG
from Event import Event

class MovingText(object):
    UPDATE_INTERVAL = 600

    def __init__(self, url):
        self.__url = url
        self.__lastUpdateTime = -1
        self.__updateCbID = None
        self.onRssDownloadReceived = Event()
        self.onRssUrlOpen = Event()
        return

    def start(self):
        entries = self.getEntries()
        if entries:
            self.onRssDownloadReceived(entries)
        self.__updateCallback()

    def destroy(self):
        self.__clearDownloadCallback()
        self.__clearCallback()
        self.onRssUrlOpen.clear()
        self.onRssDownloadReceived.clear()

    def __clearCallback(self):
        if self.__updateCbID is not None:
            BigWorld.cancelCallback(self.__updateCbID)
            self.__updateCbID = None
        return

    def __updateCallback(self):
        self.__update()
        self.__clearCallback()
        self.__updateCbID = BigWorld.callback(self.UPDATE_INTERVAL, self.__updateCallback)

    def __update(self):
        LOG_DEBUG('Requesting RSS news')
        self.__lastUpdateTime = time.time()
        from gui.Scaleform.utils.RSSDownloader import g_downloader
        if g_downloader is not None:
            g_downloader.download(self.__rssDownloadReceived, self.__url)
        return

    def __rssDownloadReceived(self, *args):
        self.onRssDownloadReceived(self.getEntries())

    def __clearDownloadCallback(self):
        from gui.Scaleform.utils.RSSDownloader import g_downloader
        if g_downloader is not None:
            g_downloader.clearDownloadCallback(self.__rssDownloadReceived)
        return

    @property
    def __lastRSS(self):
        from gui.Scaleform.utils.RSSDownloader import g_downloader
        if g_downloader is not None:
            return g_downloader.lastRSS
        else:
            return dict()

    def getEntries(self):
        result = list()
        for entry in self.__lastRSS.get('entries', list()):
            result.append(dict(id=entry.get('id'), title=entry.get('title'), description=entry.get('summary')))

        return result

    def __findEntry(self, entryID):
        for entry in self.__lastRSS.get('entries', list()):
            if entry.get('id') == entryID:
                return entry

        return None

    def showBrowser(self, entryID):
        entry = self.__findEntry(entryID)
        if entry is not None:
            link = entry.get('link', None)
            if link is not None:
                self.onRssUrlOpen(link)
            else:
                LOG_DEBUG('showBrowser - entry has no "link"', entryID)
        return