# Embedded file name: scripts/client/gui/customization_2_0/elements/installed.py


class Item(object):
    __slots__ = ('_rawData', '_spot', '_qualifier')

    def __init__(self, rawData, spot, qualifier):
        self._qualifier = qualifier
        self._rawData = rawData
        self._spot = spot

    def getID(self):
        raise NotImplementedError

    def howManyDays(self):
        raise NotImplementedError

    def timeOfApplication(self):
        raise NotImplementedError

    def getSpot(self):
        raise NotImplementedError

    @property
    def qualifier(self):
        return self._qualifier


class Emblem(Item):

    def __init__(self, rawData, spot, qualifier):
        Item.__init__(self, rawData, spot, qualifier)

    def getID(self):
        return self._rawData[0]

    def howManyDays(self):
        return self._rawData[2]

    def timeOfApplication(self):
        return self._rawData[1]

    def getSpot(self):
        return self._spot


class Inscription(Item):

    def __init__(self, rawData, spot, qualifier):
        Item.__init__(self, rawData, spot, qualifier)

    def getID(self):
        return self._rawData[0]

    def howManyDays(self):
        return self._rawData[2]

    def timeOfApplication(self):
        return self._rawData[1]

    def getSpot(self):
        return self._spot


class Camouflage(Item):

    def __init__(self, rawData, spot, qualifier):
        Item.__init__(self, rawData, spot, qualifier)

    def getID(self):
        return self._rawData[0]

    def howManyDays(self):
        return self._rawData[2]

    def timeOfApplication(self):
        return self._rawData[1]

    def getSpot(self):
        return self._spot