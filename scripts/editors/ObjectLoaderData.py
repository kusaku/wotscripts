# Embedded file name: scripts/editors/ObjectLoaderData.py


class ObjectLoaderData:

    def __init__(self):
        self.manipulator = None
        self.weaponsData = []
        self.partsUpgrades = []
        self.partsStates = []
        self.weaponSlots = []
        return

    def clear(self):
        if self.manipulator != None:
            self.manipulator.destroy()
            self.manipulator = None
        self.weaponsData = None
        self.partsUpgrades = None
        self.partsStates = None
        self.weaponSlots = None
        return

    def getPartsHierarchy(self):
        if self.manipulator:
            return self.manipulator.partsHierarchy
        else:
            return None

    def getPartsNames(self):
        if self.manipulator:
            return self.manipulator.context.partsNames
        else:
            return None

    def getNodes(self):
        if self.manipulator:
            return self.manipulator.context.nodes
        else:
            return None

    def getPartsUpgrades(self):
        return dict(((it['key'], it['value']) for it in self.partsUpgrades))

    def getPartsStates(self):
        return dict(((partId, stateId) for partId, stateId in self.partsStates))

    def updatePartsUpgradesStates(self):
        self.partsUpgrades = []
        self.partsStates = []
        for partId, upgradeId in self.manipulator.context.partTypes.items():
            self.partsUpgrades.append({'key': partId,
             'value': upgradeId})

        for partId, stateId in self.manipulator.context.partsStates.items():
            self.partsStates.append((partId, stateId))

    def setManipulatorMatrix(self, matr):
        if self.manipulator:
            self.manipulator.setMatrixProvider(matr)

    def getEntityMatrix(self):
        if self.manipulator:
            return self.manipulator.getMatrixProvider()

    def getGroundDecalMap(self):
        if self.manipulator:
            return self.manipulator.groundDecalMap