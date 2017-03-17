# Embedded file name: scripts/common/db/DBSoundsCommon.py
from DBHelpers import *
from DBSoundsMisc import SoundsMisc
from DBSoundsHit import SoundsHit
from DBSoundsDSP import SoundsDSP
from DBSoundsSpeech import SoundsSpeech

class SoundsDucking:

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data):
        if data != None:
            readValue(self, data, 'startStageTerm', 0.0)
            readValue(self, data, 'finishStageTerm', 0.0)
            readValue(self, data, 'duckingLevelNorm', 0.0)
        return


class CategoryDuckingEntry:

    def __init__(self, data = None):
        self.slaves = []
        self.readData(data)

    def readData(self, data):
        if data != None:
            readValue(self, data, 'mainCategory', '')
            slaveCategories = findSection(data, 'slaveCategories')
            if slaveCategories:
                for slave in slaveCategories.values():
                    self.slaves.append(slave.asString)

            readValue(self, data, 'startStageTerm', 0.0)
            readValue(self, data, 'finishStageTerm', 0.0)
            readValue(self, data, 'duckingLevelNorm', 0.0)
        return


class CategoryDucking:

    def __init__(self, data = None):
        self.sounds = []
        self.readData(data)

    def readData(self, data):
        if data != None:
            for entry in data.values():
                catDucking = CategoryDuckingEntry(entry)
                catDuckingReadyToParse = (catDucking.mainCategory,
                 catDucking.slaves,
                 catDucking.startStageTerm,
                 catDucking.finishStageTerm,
                 catDucking.duckingLevelNorm)
                self.sounds.append(catDuckingReadyToParse)

        return


class ZoomStateParamMap:

    def __init__(self, data = None):
        self.map = {}
        self.readData(data)

    def readData(self, data):
        if data != None:
            for cfgEntry in data.values():
                entry = ZoomStateParamEntry(cfgEntry)
                self.map[entry.zoomStateIdx] = entry.soundParamValue

        return


class ZoomStateParamEntry:

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data):
        if data != None:
            readValue(self, data, 'zoomStateIdx', 0)
            readValue(self, data, 'soundParamValue', 0.0)
        return


class IngroupVolumeBalancer:

    def __init__(self, data = None):
        self.categories = set()
        self.readData(data)

    def readData(self, data):
        if data != None:
            for dataEntry in data.values():
                category = dataEntry.readString('')
                self.categories.add(category)

        return


class SoundsCommon:

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data):
        if data != None:
            self.hit = SoundsHit(findSection(data, 'hit'))
            self.misc = SoundsMisc(findSection(data, 'misc'))
            self.dsp = SoundsDSP(findSection(data, 'dsp'))
            self.ui = SoundsMisc(findSection(data, 'ui'))
            self.speech = SoundsSpeech(findSection(data, 'speech'))
            self.ducking = SoundsDucking(findSection(data, 'engineDamageDucking'))
            self.categoryDucking = CategoryDucking(findSection(data, 'categoryDucking'))
            self.zoomStateParam = ZoomStateParamMap(findSection(data, 'zoomStateParamMap'))
            self.ingroupVolumeBalancer = IngroupVolumeBalancer(findSection(data, 'ingroupVolumeBalancer'))
            readValue(self, data, 'allSoundsFadeOutTime', 0.0)
            readValue(self, data, 'ambientUpdateInterval', 1.0)
        return