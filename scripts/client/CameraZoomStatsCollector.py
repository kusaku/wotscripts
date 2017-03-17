# Embedded file name: scripts/client/CameraZoomStatsCollector.py
__author__ = 'm_antipov'
import BigWorld
from debug_utils import *
g_cameraZoomStatsCollector = None
ZOOM_STATE_DICTIONARY = {0: 'ZOOM_STATE_FAR',
 1: 'ZOOM_STATE_MID',
 2: 'ZOOM_STATE_NEAR',
 3: 'ZOOM_STATE_SNIPER',
 4: 'ZOOM_STATE_SNIPER'}

class CameraZoomStatsCollector:

    def __init__(self):
        global g_cameraZoomStatsCollector
        self.__curZoomIdx = None
        self.__profiles = dict()
        self.__zoomData = dict()
        self.__allowProfiling = False
        g_cameraZoomStatsCollector = self
        return

    def retrieve(self):
        return None

    def touch(self, zoomIdx, newVal):
        if zoomIdx is None:
            return
        else:
            idx = self.__zoomData.get(zoomIdx)
            if newVal:
                self.__zoomData[zoomIdx] = newVal
            return idx

    def onChangeZoom(self, zoomIdx):
        if not self.__allowProfiling:
            return
        else:
            if zoomIdx != self.__curZoomIdx:
                val = self.touch(self.__curZoomIdx, None)
                thisTime = BigWorld.serverTime()
                if val:
                    time = thisTime - val
                    key = ZOOM_STATE_DICTIONARY.get(self.__curZoomIdx)
                    if key is None:
                        key = 'UNKNOWN'
                    if self.__profiles.get(key) is None:
                        self.__profiles[key] = time
                    else:
                        self.__profiles[key] += time
                self.touch(zoomIdx, thisTime)
            self.__curZoomIdx = zoomIdx
            return

    def getZoomStats(self):
        idx = self.__curZoomIdx
        self.onChangeZoom(None)
        self.__curZoomIdx = idx
        return self.__profiles

    def resetStats(self):
        self.__profiles = dict()

    def allowProfiling(self, val):
        if not val:
            self.onChangeZoom(None)
        self.__allowProfiling = val
        return