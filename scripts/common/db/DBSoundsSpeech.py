# Embedded file name: scripts/common/db/DBSoundsSpeech.py
from DBHelpers import *

class SoundSpeech:

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data):
        if data != None:
            readValue(self, data, 'name', '')
            readValue(self, data, 'path', '')
            readValue(self, data, 'priority', 0)
            readValue(self, data, 'repeatDelay', 0.0)
            readValue(self, data, 'expiryTime', 0.0)
            readValue(self, data, 'triggerDelay', 0.0)
            readValue(self, data, 'canStopTime', 0.0)
        return


class SoundsSpeech:

    def __init__(self, data = None):
        self.sounds = {}
        self.readData(data)

    def readData(self, data):
        if data != None:
            readValue(self, data, 'expertGamesNum', 0)
            readValue(self, data, 'delayBetweenDifferentSpeeches', 0.0)
            for v in data.values():
                sound = SoundSpeech(v)
                self.sounds[sound.name] = sound

        return