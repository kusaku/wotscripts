# Embedded file name: scripts/common/db/DBObjectGroups.py
from MathExt import sampleListByWeights
from debug_utils import *
from DBHelpers import readValue, findSection
from copy import copy

class SpawnSequenceRecord:

    def __init__(self, data):
        self.count = data.readInt('count', -1)
        self.priority = data.readInt('priority', 1)
        self.array = []
        for sID, sData in data.items():
            if sID == 'selectGroups':
                self.array.append(SpawnSequenceRecord(sData))
            elif sID == 'group':
                self.array.append(SpawnGroupRecord(sData))

    def generateRandomGroups(self):
        return set((id for id in self.createGroupListGenerator()))

    def createGroupListGenerator(self):
        maxCount = len(self.array)
        count = min(self.count if self.count >= 0 else maxCount, maxCount)
        if count > 0:
            if count == maxCount:
                for obj in self.array:
                    if isinstance(obj, SpawnSequenceRecord):
                        for groupID in obj.createGroupListGenerator():
                            yield groupID

                    else:
                        yield obj.groupID

            else:
                for obj in sampleListByWeights(self.array, [ obj.priority for obj in self.array ], self.count):
                    if isinstance(obj, SpawnSequenceRecord):
                        for groupID in obj.createGroupListGenerator():
                            yield groupID

                    else:
                        yield obj.groupID


class SpawnGroupRecord:

    def __init__(self, data):
        self.groupID = data.readString('id', '')
        self.priority = data.readInt('priority', 0)


class SomeGameGroups:

    def __init__(self, groups, spawnSequence):

        def buildDestroyToSpawn(group):
            for dGroupID in group.destroyToSpawn:
                if dGroupID in spawnSequence or self.__checkCouldBeSpawned(groups, spawnSequence, groups.get(dGroupID, None)):
                    yield dGroupID

            return

        self.__validGroups = {}
        for groupID, group in groups.items():
            if group.customSpawn or groupID in spawnSequence or self.__checkCouldBeSpawned(groups, spawnSequence, group):
                gameGroup = copy(group)
                gameGroup.destroyToSpawn = set(buildDestroyToSpawn(group))
                self.__validGroups[groupID] = gameGroup
                self.setAlive(groupID, 2, False)

        LOG_DEBUG('prepare game with such groups:', [ (gID, g.destroyToSpawn) for gID, g in self.__validGroups.items() ])

    def __checkCouldBeSpawned(self, groups, spawnSequence, group):
        if group:
            if group.customSpawn:
                return True
            for gID in group.destroyToSpawn:
                if gID in spawnSequence or self.__checkCouldBeSpawned(groups, spawnSequence, groups.get(gID, None)):
                    return True

        return

    def getGroupData(self, groupID):
        return self.__validGroups.get(groupID, None)

    def setAlive(self, groupID, teamIndex, flag):
        group = self.getGroupData(groupID)
        if teamIndex == 2:
            group.alive = 2 * [flag]
        else:
            group.alive[teamIndex] = flag

    def destroyGroup(self, groupID, teamIndex):

        def generateSpawnList():
            for gID, g in self.__validGroups.items():
                if not g.alive[teamIndex] and groupID in g.destroyToSpawn:
                    allDestoyed = True
                    for lgID in g.destroyToSpawn:
                        if self.__validGroups[lgID].alive[teamIndex]:
                            allDestoyed = False
                            break

                    if allDestoyed:
                        tIndex = g.allTeamSpawn and 2 or teamIndex
                        self.setAlive(gID, tIndex, True)
                        yield (gID, tIndex)

        self.setAlive(groupID, teamIndex, False)
        if 1 >= teamIndex >= 0:
            return generateSpawnList()
        else:
            return []


class ObjectGroups:

    def __init__(self):
        self.groups = {}
        self.__spawnSequence = None
        return

    def addGroup(self, groupID, groupData):
        LOG_DEBUG('add group', groupID)
        self.groups[groupID] = ObjectGroup(groupID, groupData)

    def readSpawnSequence(self, data):
        self.__spawnSequence = SpawnSequenceRecord(data)

    def generateGameGroups(self):
        return SomeGameGroups(self.groups, self.__spawnSequence and self.__spawnSequence.generateRandomGroups() or set())


class ObjectGroup:

    def __init__(self, groupID, data):
        self.groupID = groupID
        readValue(self, data, 'initialSpawnDelay', -1.0)
        readValue(self, data, 'bomberIndex', -1)
        readValue(self, data, 'bomberDelay', 0.0)
        readValue(self, data, 'objectsAreaIndex', -1)
        readValue(self, data, 'allTeamSpawn', False)
        readValue(self, data, 'customSpawn', False)
        self.destroyToSpawn = set()
        initOnSection = findSection(data, 'initOnDestruction')
        if initOnSection:
            self.destroyToSpawn = set((sectionData.asString for sectionData in initOnSection.values()))