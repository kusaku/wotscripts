# Embedded file name: scripts/common/Spline.py
from consts import WORLD_SCALING, IS_CLIENT, IS_CELLAPP
from debug_utils import *
import BigWorld
from Math import Matrix, Quaternion, Vector3
import math
from MathExt import clamp

def ramerdouglas(line, dist):
    """Does Ramer-Douglas-Peucker simplification of
    a line with `dist` threshold.
    `line` must be a list of Vec objects,
    all of the same type (either 2d or 3d)."""
    if len(line) < 3:
        return line
    begin, end = line[0], line[-1]
    distSq = [ (curr - begin).lengthSquared - (end - begin).dot(curr - begin) ** 2 / (end - begin).lengthSquared for curr in line[1:-1] ]
    maxdist = max(distSq)
    if maxdist < dist ** 2:
        return [begin, end]
    pos = distSq.index(maxdist)
    return ramerdouglas(line[:pos + 2], dist) + ramerdouglas(line[pos + 1:], dist)[1:]


class Spline:

    def __init__(self, id, pointsData):
        self.__id = id
        self.__time = 0.0
        self.__speeds = []
        self.__basePoints = list()
        self.__teleports = []
        if pointsData:
            self.__arenas = pointsData.readStrings('arena')
            self.__isCircle = pointsData.readBool('isCircle', False)
            for nodeID, pointData in pointsData.items():
                if nodeID.lower() == 'point':
                    self.__basePoints.append(pointData.readVector3('position'))
                    isTeleport = pointData.readBool('teleport', False)
                    if isTeleport:
                        self.__teleports.append(len(self.__basePoints) - 1)
                    self.__speeds.append(pointData.readFloat('speed0', 1.0) * WORLD_SCALING)

            if len(self.__basePoints) > 0:
                self.__buildCurves(self.__basePoints)
                self.__bwSpline = (IS_CLIENT or IS_CELLAPP) and BigWorld.SplineHolder(id, self.__points, self.__time, self.__isCircle) or None
        return

    def buildCurves(self, basePoints, speeds):
        self.__basePoints = basePoints
        self.__speeds = speeds
        self.__buildCurves(basePoints)

    @property
    def bwSpline(self):
        return self.__bwSpline

    @property
    def averageSpeed(self):
        if self.__speeds:
            return sum(self.__speeds) / len(self.__speeds)
        return 0

    def getScenarioEvents(self):
        return {}

    def move(self, vec):
        self.__points = map(lambda x: (x[0], x[1] + vec), self.__points)
        self.__basePoints = map(lambda x: x + vec, self.__basePoints)

    def rotate(self, quaternion):
        self.__points = map(lambda x: (x[0], quaternion.rotateVec(x[1])), self.__points)
        self.__basePoints = map(lambda x: quaternion.rotateVec(x), self.__basePoints)

    def setPositionAndDirection(self, endPoint, direction):
        points = self.getBasePoints()
        if len(points) < 2:
            return
        self.move(-points[-1])
        splineEndDirection = points[-1] - points[-2]
        splineEndDirection.y = 0
        splineEndDirection.normalise()
        V = splineEndDirection + direction
        V.normalise()
        angle = V.dot(direction)
        axis = V.cross(direction)
        self.rotate(Quaternion(axis[0], axis[1], axis[2], angle))
        self.move(endPoint)

    def drawSpline(self, groupName, dt = 3.0):
        t = 0
        prevPoint = self.getPointForTime(t)
        while t < self.__time:
            t += dt
            point = self.getPointForTime(t)
            BigWorld.addDrawLine(groupName, prevPoint, point, 4294901760L)
            prevPoint = point

        for i, point in enumerate(self.__basePoints):
            m = Matrix()
            m.setTranslate(point)
            color = 4278255360L
            if i == 0:
                color = 4278190335L
            elif i == 1:
                color = 4278255615L
            elif i == len(self.__basePoints) - 1:
                color = 4294967295L
            BigWorld.addPoint(groupName, m, color, False)

    def checkArena(self, name):
        return name in self.__arenas

    def getBasePoints(self):
        """
        Return list of spline base points
        @rtype: list
        """
        return self.__basePoints

    def getPoints(self):
        return self.__points

    def getSpeeds(self):
        return self.__speeds

    def getTeleportIndicies(self):
        return self.__teleports

    def __buildCurves(self, points):
        self.__points = list()
        firstPoint = points[0]
        lastPoint = firstPoint
        self.__time = 0
        self.__points.append((0.0, firstPoint))
        for i in range(1, len(points)):
            scaledPoint = points[i]
            dist = scaledPoint.distTo(lastPoint)
            self.__time += dist / self.__speeds[i - 1]
            self.__points.append((self.__time, scaledPoint))
            lastPoint = scaledPoint

    def getLastPointTime(self):
        return self.__points[-1][0]

    def getPointForTime(self, t):
        t = self.__normalizeTime(t)
        prevPointTime = 0.0
        pointsLen = len(self.__points)
        for i in range(0, pointsLen):
            pointTime = self.__points[i][0]
            if pointTime > t:
                norm = (t - prevPointTime) / (pointTime - prevPointTime)
                if self.__isCircle:
                    p_1 = self.__points[(i - 2) % pointsLen][1]
                    p0 = self.__points[(i - 1) % pointsLen][1]
                    p2 = self.__points[(i + 1) % pointsLen][1]
                else:
                    p_1 = self.__points[max(i - 2, 0) % pointsLen][1]
                    p0 = self.__points[max(i - 1, 0) % pointsLen][1]
                    p2 = self.__points[min(i + 1, pointsLen - 1) % pointsLen][1]
                p1 = self.__points[i][1]
                dist12 = (p0 - p1).length
                v01 = p0 - p_1
                dist01Sq = v01.lengthSquared
                if dist01Sq > 0:
                    v01 = dist12 * v01 / math.sqrt(dist01Sq)
                v23 = p2 - p1
                dist23Sq = v23.lengthSquared
                if dist23Sq > 0:
                    v23 = dist12 * v23 / math.sqrt(dist23Sq)
                v0_ok = p0 - v01
                v3_ok = p1 + v23
                return self.spline_4p(norm, v0_ok, p0, p1, v3_ok)
            prevPointTime = pointTime

        return self.__points[-1][1]

    def __getPointsForTimeLinear(self, t):
        t = self.__normalizeTime(t)
        prevPointTime = 0.0
        pointsLen = len(self.__points)
        for i in range(0, pointsLen):
            pointTime = self.__points[i][0]
            if pointTime > t:
                norm = (t - prevPointTime) / (pointTime - prevPointTime)
                if self.__isCircle:
                    p0 = self.__points[(i - 1) % pointsLen][1]
                else:
                    p0 = self.__points[max(i - 1, 0) % pointsLen][1]
                p1 = self.__points[i][1]
                return (p0, p0 + (p1 - p0) * norm, p1)
            prevPointTime = pointTime

        return (self.__points[-2][1], self.__points[-1][1], self.__points[-1][1])

    def __normalizeTime(self, t):
        if t > self.__time:
            if self.__isCircle:
                t -= int(t / self.__time) * self.__time
            else:
                t = self.__time
        if t < 0:
            if self.__isCircle:
                t += self.__time
            else:
                t = 0.0
        return t

    def getSafePointAndRotationForTime(self, t, minPos, maxPos, newSplineEnd = None, rotate = None, offset = 10.0):
        if not newSplineEnd:
            newSplineEnd = Vector3()
        if not rotate:
            rotate = Vector3()
        pos, rot = self.getPointAndRotationForTime(t)
        points = self.getBasePoints()
        pos = pos - points[-1]
        splineEndDirection = points[-1] - points[-2]
        splineEndDirection.normalise()
        splineEndDirection.y = 0
        V = splineEndDirection + rotate
        V.normalise()
        angle = V.dot(rotate)
        axis = V.cross(rotate)
        endRotation = Quaternion(axis[0], axis[1], axis[2], angle)
        pos = endRotation.rotateVec(pos)
        pos = pos + newSplineEnd
        if not (minPos[0] < pos.x < maxPos[0] and minPos[1] < pos.z < maxPos[1]):
            LOG_WARNING_DEBUG('BAD SPLINE POSITION, OUT OF WORLD BOUNDS!!! Spline id: {0}, pos: {1}'.format(self.__id, pos))
        x = clamp(minPos[0] + offset, pos.x, maxPos[0] - offset)
        z = clamp(minPos[1] + offset, pos.z, maxPos[1] - offset)
        y = pos.y
        return (Vector3(x, y, z), endRotation.mul(rot))

    def getPointAndRotationForTime(self, t):
        t = self.__normalizeTime(t)
        A = self.getPointForTime(t - 1.0)
        B = self.getPointForTime(t)
        C = self.getPointForTime(t + 1.0)
        D = self.getPointForTime(t + 10)
        newLookVector = Vector3(C.x - A.x, C.y - A.y, C.z - A.z).getNormalized()
        DBproj = Vector3(D.x - B.x, 0, D.z - B.z).getNormalized()
        BAproj = Vector3(B.x - A.x, 0, B.z - A.z).getNormalized()
        rollMagnitude = math.acos(clamp(-1, DBproj.dot(BAproj), 1)) * 3
        rollDirection = 1 if DBproj.cross(BAproj).y > 0 else -1
        roll = clamp(-math.pi / 6, rollMagnitude * rollDirection, math.pi / 6)
        pitch = -math.asin(clamp(-1.0, newLookVector.y, 1.0))
        yaw = math.atan2(newLookVector.x, newLookVector.z)
        if self.__time - t < self.__time * 0.1:
            norm = clamp(0, (self.__time - t) / (self.__time * 0.1), 1)
            roll *= norm
            pitch *= norm
        rotation = Quaternion()
        rotation.fromEuler(roll, pitch, yaw)
        return (B, rotation)

    def spline_4p(self, t, p_1, p0, p1, p2):
        """ Catmull-Rom
            (Ps can be numpy vectors or arrays too: colors, curves ...)
        """
        v1, v2 = p0, p1
        t1 = (p1 - p_1) / 2
        t2 = (p2 - p0) / 2
        return (2 * t * t * t - 3 * t * t + 1) * v1 + (-2 * t * t * t + 3 * t * t) * v2 + (t * t * t - 2 * t * t + t) * t1 + (t * t * t - t * t) * t2

    @property
    def totalTime(self):
        return self.__time

    def cutSpline(self, norm, newTime = None):
        if not newTime:
            newTime = self.__time
        totalDistance = sum(map(lambda x, y: (x - y).length, self.__basePoints[1:], self.__basePoints[:-1]))
        cutDistance = totalDistance * norm
        lastPoint = self.__basePoints[0]
        processedDistance = 0.0
        self.__time = newTime / WORLD_SCALING
        for i in xrange(1, len(self.__basePoints)):
            scaledPoint = self.__basePoints[i]
            dist = scaledPoint.distTo(lastPoint)
            if processedDistance + dist > cutDistance:
                offset = (cutDistance - processedDistance) / dist
                startPoint = lastPoint + (scaledPoint - lastPoint) * offset
                self.__basePoints = [startPoint] + self.__basePoints[i:]
                break
            processedDistance += dist
            lastPoint = scaledPoint

        newTotalDistance = sum(map(lambda x, y: (x - y).length, self.__basePoints[1:], self.__basePoints[:-1]))
        lastPoint = self.__basePoints[0]
        processedDistance = 0.0
        self.__points = [(0, lastPoint)]
        for i in range(1, len(self.__basePoints)):
            scaledPoint = self.__basePoints[i]
            processedDistance += scaledPoint.distTo(lastPoint)
            time = self.__time * processedDistance / newTotalDistance
            self.__points.append((time, scaledPoint))
            lastPoint = scaledPoint

        self.__speeds = [ newTotalDistance / self.__time for i in xrange(len(self.__basePoints)) ]