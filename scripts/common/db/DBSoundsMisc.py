# Embedded file name: scripts/common/db/DBSoundsMisc.py
from DBHelpers import *

class SoundMisc:

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data):
        if data != None:
            readValue(self, data, 'name', '')
            readValue(self, data, 'path', '')
        return


class SoundsMisc:

    def __init__(self, data = None):
        self.sounds = {}
        self.readData(data)

    def readData(self, data):
        if data != None:
            for v in data.values():
                sound = SoundMisc(v)
                self.sounds[sound.name] = sound

        return