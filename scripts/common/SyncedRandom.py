# Embedded file name: scripts/common/SyncedRandom.py
from random import Random
from consts import COLLISION_RECORDER

class SyncedRandom(object):

    def __init__(self):
        if COLLISION_RECORDER:
            self.__refreshCount = 0
            self.__setStateCount = 0
            self.__randomCount = 0
            self.__randomInStateCount = 0
        self.__random = Random()
        self.refresh()

    def refresh(self):
        if COLLISION_RECORDER:
            self.__refreshCount += 1
            self.__randomInStateCount = 0
        self.__state = self.__random.randint(0, 65535)
        self.__random.seed(self.__state)
        return self.__state

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        if self.__state != value:
            if COLLISION_RECORDER:
                self.__setStateCount += 1
                self.__randomInStateCount = 0
            self.__state = value
            self.__random.seed(self.__state)
            return True
        else:
            return False

    def random(self):
        if COLLISION_RECORDER:
            self.__randomCount += 1
            self.__randomInStateCount += 1
        return self.__random.random()

    def randint(self, a, b):
        if COLLISION_RECORDER:
            self.__randomCount += 1
            self.__randomInStateCount += 1
        return self.__random.randint(a, b)

    if COLLISION_RECORDER:

        def getInfo(self):
            return 'random:\nstate = {0}\nrandomInStateCount = {1}\nrefreshCount = {2}\nsetStateCount = {3}\nrandomCount = {4}'.format(self.__state, self.__randomInStateCount, self.__refreshCount, self.__setStateCount, self.__randomCount)