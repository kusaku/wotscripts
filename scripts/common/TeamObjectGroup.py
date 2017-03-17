# Embedded file name: scripts/common/TeamObjectGroup.py
import sys
import math
from Math import Vector2, Vector3

def createTeamObjectsGroups(teamObjects):
    """
    :rtype: list[TeamObjectGroup]
    """
    groups = []
    processedTeamObjects = []
    for t in teamObjects:
        if t in processedTeamObjects:
            continue
        processedTeamObjects.append(t)
        neighbours = _findNeighbours(t, filter(lambda e: e not in processedTeamObjects, teamObjects))
        groups.append(TeamObjectGroup([t] + neighbours))
        processedTeamObjects.extend(neighbours)

    return groups


def _findNeighbours(teamObject, notProcessedTeamObjects):
    GROUP_DISTANCE = 150
    HEIGHT_DELTA = 10
    pos = Vector3(teamObject['matrix'].translation)
    neighbours = []
    for t in filter(lambda e: teamObject['teamID'] == e['teamID'], notProcessedTeamObjects):
        nextObjectPos = Vector3(t['matrix'].translation)
        heightDelta = math.fabs(nextObjectPos.y - pos.y)
        dist = nextObjectPos - pos
        distXZ = dist + Vector3(0, -dist.y, 0)
        if distXZ.length <= GROUP_DISTANCE and heightDelta <= HEIGHT_DELTA:
            neighbours.append(t)

    res = neighbours[:]
    for t in neighbours:
        nextNotProcessedTeamObjects = filter(lambda e: e not in res + [t], notProcessedTeamObjects)
        res.extend(_findNeighbours(t, nextNotProcessedTeamObjects))

    return res


class TeamObjectGroup:

    def __init__(self, teamObjects):
        self._teamObjects = teamObjects
        self._teamID = teamObjects[0]['teamID']
        self._boundingBox = (0, 0, 0, 0)
        self._calculateBoundingBox()

    @property
    def teamID(self):
        return self._teamID

    @property
    def teamObjects(self):
        return self._teamObjects

    @property
    def size(self):
        return len(self._teamObjects)

    @property
    def boundingBox(self):
        return self._boundingBox

    @property
    def center(self):
        """
        :rtype: Vector2
        """
        x = self._boundingBox[2] - self._boundingBox[0]
        z = self._boundingBox[3] - self._boundingBox[1]
        return Vector2(self._boundingBox[0] + x / 2, self._boundingBox[1] + z / 2)

    def _calculateBoundingBox(self):
        minX, minZ, maxX, maxZ = (sys.maxint,
         sys.maxint,
         -sys.maxint,
         -sys.maxint)
        for t in self._teamObjects:
            if t['matrix'].translation.x < minX:
                minX = t['matrix'].translation.x
            if t['matrix'].translation.z < minZ:
                minZ = t['matrix'].translation.z
            if t['matrix'].translation.x > maxX:
                maxX = t['matrix'].translation.x
            if t['matrix'].translation.z > maxZ:
                maxZ = t['matrix'].translation.z

        self._boundingBox = (minX,
         minZ,
         maxX,
         maxZ)
        size = (maxX - minX, maxZ - minZ)
        if size[0] * size[1] < 36:
            x = minX + size[0] / 2.0
            z = minZ + size[1] / 2.0
            self._boundingBox = (x - 3,
             z - 3,
             x + 3,
             z + 3)


if __name__ == '__main__':
    import unittest
    from Bot.tests import test_TeamObjectGroup
    suite = unittest.TestLoader().loadTestsFromModule(test_TeamObjectGroup)
    unittest.TextTestRunner(verbosity=2).run(suite)