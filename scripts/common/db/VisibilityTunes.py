# Embedded file name: scripts/common/db/VisibilityTunes.py
from DBHelpers import readValues

class VisibilityTunes:

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data):
        if data:
            params = (('scanSectorProfile', 'default'),
             ('planeCloudIgnoreFactor', 1.0),
             ('planeCloudVisibilityFactor', 1.0),
             ('scanRangeCfc', 1.0),
             ('detectabilityCfc', 1.0),
             ('ignoreVisibilitySystem', False),
             ('trackingCfc', 1.5))
            readValues(self, data, params)