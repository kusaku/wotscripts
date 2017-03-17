# Embedded file name: scripts/common/db/DBSoundsHit.py
from DBHelpers import *

class SoundHit:

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data):
        if data != None:
            readValue(self, data, 'name', '')
            readValue(self, data, 'gunCaliber', '')
            readValue(self, data, 'hitMaterialID', 0)
            readValue(self, data, 'hitType', '')
        return


class SoundsHit:

    def __init__(self, data = None):
        self.__sounds = {}
        self.readData(data)

    def readData(self, data):
        if data != None:
            readValue(self, data, 'caliberSmallMax', 0.0)
            readValue(self, data, 'caliberMediumMax', 0.0)
            soundsSection = findSection(data, 'sounds')
            if soundsSection:
                for v in soundsSection.values():
                    s = SoundHit(v)
                    id = self.__makeSoundID(s.hitType, s.gunCaliber, s.hitMaterialID)
                    self.__sounds[id] = s.name

        return

    def __makeSoundID(self, hitType, caliberType, material):
        return hitType + caliberType + str(material)

    def __makeCaliberType(self, caliberValue):
        if caliberValue < self.caliberSmallMax:
            return 'small'
        elif caliberValue < self.caliberMediumMax:
            return 'medium'
        else:
            return 'big'

    def getSound(self, hitType, caliber, material):
        caliberType = self.__makeCaliberType(caliber)
        id = self.__makeSoundID(hitType, caliberType, material)
        return self.__sounds.get(id, None)