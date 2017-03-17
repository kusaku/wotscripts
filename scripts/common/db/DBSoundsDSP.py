# Embedded file name: scripts/common/db/DBSoundsDSP.py
from DBHelpers import *

class ParamEQItem:

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data):
        if data != None:
            readValue(self, data, 'category', '')
            readValue(self, data, 'centerFrequency', 0)
            readValue(self, data, 'octaveRange', 0)
            readValue(self, data, 'frequencyGain', 0)
        return


class ParamEQ:

    def __init__(self, data = None):
        self.items = {}
        self.readData(data)

    def readData(self, data):
        if data != None:
            items = findSection(data, 'paramEQ')
            if items != None:
                for v in items.values():
                    item = ParamEQItem(v)
                    self.items[item.category] = item

        return


class SoundsDSP:

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data):
        if data != None:
            readValue(self, data, 'lowPassCutOff', 5000.0)
            self.paramEQ = ParamEQ(data)
        return