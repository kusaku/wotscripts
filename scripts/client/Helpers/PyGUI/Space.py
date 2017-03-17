# Embedded file name: scripts/client/Helpers/PyGUI/Space.py
import BigWorld

class Space(BigWorld.Entity):

    def __init__(self, nearbyEntity):
        BigWorld.Entity.__init__(self)
        raise nearbyEntity is None or AssertionError
        return

    def onDestroy(self):
        self.destroySpace()

    def addGeometryMapping(self, geometryToMap):
        BigWorld.addSpaceGeometryMapping(self.spaceID, None, geometryToMap)
        return