# Embedded file name: scripts/common/db/DBSoundsStingers.py
from DBHelpers import *

class SoundsStingers:

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data):
        if data != None:
            readValue(self, data, 'duckingStartStageTerm', 0.0)
            readValue(self, data, 'duckingIdleStageTerm', 0.0)
            readValue(self, data, 'duckingFinishStageTerm', 0.0)
            readValue(self, data, 'duckingLevelNorm', 0.0)
        return