# Embedded file name: scripts/common/db/DBEntityColorScheme.py
__author__ = 's_karchavets'
from consts import WORLD_SCALING

class _EntityColorScheme:

    def __init__(self, distance, color, scale, arrowAlpha):
        self.distance = distance
        self.color = color
        self.scale = scale
        self.arrowAlpha = arrowAlpha


class EntityColorSchemes:

    def __init__(self, data = None):
        self.__schemes = dict()
        if data is not None:
            self.readData(data)
        return

    def readData(self, rootSection):
        for name, data in rootSection.items():
            for subName, subdata in data.items():
                if subName == 'point':
                    if name not in self.__schemes:
                        self.__schemes[name] = list()
                    self.__schemes[name].append(_EntityColorScheme(subdata.readFloat('distance', 0.0) * WORLD_SCALING, subdata.readVector4('color', (0, 0, 0, 0)), subdata.readFloat('scale', 16.0), subdata.readFloat('arrowAlpha', 1.0)))

    def getScheme(self, name):
        return self.__schemes.get(name, None)

    def getSchemes(self):
        return self.__schemes