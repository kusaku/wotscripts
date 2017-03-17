# Embedded file name: scripts/common/db/DBSpawnGroup.py
import Math
from DBHelpers import readValues
from consts import WORLD_SCALING
from EntityHelpers import PLANE_TYPE_LETTER

class DBSpawnGroup:

    def __init__(self, data):
        if data:
            self.__points = [ SpawnPoint(sectionData) for sectionID, sectionData in data.items() if sectionID == 'spawnPoint' ]
        else:
            self.__points = []

    @property
    def points(self):
        return self.__points


class SpawnPoint:

    def __init__(self, data = None):
        if data:
            self.readData(data)

    def readData(self, data):
        params = (('airplaneClasses', ''), ('position', Math.Vector3()), ('rotation', Math.Vector3()))
        readValues(self, data, params)
        self.position *= WORLD_SCALING
        self.airplaneClasses = [ PLANE_TYPE_LETTER[c] for c in self.airplaneClasses.split(' ') if c != '' ]