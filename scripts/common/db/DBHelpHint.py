# Embedded file name: scripts/common/db/DBHelpHint.py
__author__ = 's_karchavets'
from DBHelpers import readValue
from random import shuffle
HINTS_CHILD_INDEX = 3
AS_BOOL_DEFAULT = {'hasBombs': False,
 'hasRockets': False,
 'hasGunner': False,
 'hasRocketsOrBombs': False,
 'highRise': False}
AS_STRING_DEFAULT = {'type': 'ALL',
 'id': '0'}
AS_STRING_DEFAULT_LIST = ['imgPath', 'locText', 'imgPathBlind']

class _HintProvider:
    pass


class HelpHint:

    def __init__(self, data = None):
        self.unusedMessageIndexes = list()
        self.allHints = list()
        if data is not None:
            self.readData(data)
        return

    def readData(self, rootSection):
        hints = rootSection.child(HINTS_CHILD_INDEX)
        for hintIndex in range(len(hints.values())):
            objHint = hints.child(hintIndex)
            objHintProvider = _HintProvider()
            for key, defaultValue in AS_BOOL_DEFAULT.items():
                setattr(objHintProvider, key, defaultValue)

            for key, defaultValue in AS_STRING_DEFAULT.items():
                setattr(objHintProvider, key, defaultValue)

            for key in AS_STRING_DEFAULT_LIST:
                setattr(objHintProvider, key, list())

            for hintChildIndex in range(len(objHint.values())):
                name = objHint.childName(hintChildIndex)
                child = objHint.child(hintChildIndex)
                if name in AS_STRING_DEFAULT.keys():
                    setattr(objHintProvider, name, child.asString)
                elif name in AS_BOOL_DEFAULT.keys():
                    setattr(objHintProvider, name, child.asBool)
                elif name in AS_STRING_DEFAULT_LIST:
                    getattr(objHintProvider, name).append(child.asString)

            self.allHints.append(objHintProvider)

        shuffle(self.allHints)
        readValue(self, rootSection, 'time', 8)
        readValue(self, rootSection, 'count', 33)
        readValue(self, rootSection, 'unused', '')
        if self.unused != '':
            unusedMessagesString = unused.split(',')
            for index in unusedMessagesString:
                self.unusedMessageIndexes.append(int(index))