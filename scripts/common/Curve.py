# Embedded file name: scripts/common/Curve.py
try:
    import BigWorld
    import debug_utils
except:
    pass

import Math
import math
from MathExt import *

class CurveIsEmptyException(Exception):
    """This exception is raised when trying to make calculations on empty (uninitialized) curve"""

    def __init__(self):
        pass


class Curve:
    """This class produces a cubic interpolation of a set of points"""

    def __init__(self, p = [], pointCount = 10, multiplier = 1.0):
        self.p = p
        self.pointCount = pointCount
        self.dX = 0.0
        self.intX = 0.0
        self.multiplier = multiplier
        self.scale = 1.0
        self.refresh()

    def __getSplinePos(self, coefs, x):
        return ((coefs[0] * x + coefs[1]) * x + coefs[2]) * x + coefs[3]

    def __getCoefs(self, p0, p1, p2, p3):
        df0 = 0.0
        df1 = 0.0
        dx = p2.x - p1.x
        if p1.y != p2.y and dx != 0.0:
            dx = 1.0 / dx
            if p2.x - p0.x != 0.0 and (p0.y > p1.y) == (p1.y > p2.y) and p0.y != p1.y:
                df0 = (p2.y - p0.y) / ((p2.x - p0.x) * dx)
            if p3.x - p1.x != 0.0 and (p3.y > p2.y) == (p2.y > p1.y) and p3.y != p2.y:
                df1 = (p3.y - p1.y) / ((p3.x - p1.x) * dx)
        return (2.0 * p1.y - 2.0 * p2.y + df0 + df1,
         -3.0 * p1.y + 3.0 * p2.y - 2.0 * df0 - df1,
         df0,
         p1.y)

    def refresh(self):
        self.__buffer = []
        if len(self.p) > 0:
            if len(self.p) == 1:
                self.__buffer.append(self.p[0].y * self.multiplier)
                return
            tx = self.p[0].x
            pointId = -1
            self.intX = self.p[-1].x - self.p[0].x
            self.dX = self.intX / float(self.pointCount - 1)
            last_index_p = len(self.p) - 1
            coefs = None
            for i in range(0, self.pointCount):
                if pointId < last_index_p and tx >= self.p[pointId + 1].x:
                    pointId += 1
                    coefs = self.__getCoefs(self.p[max(pointId - 1, 0)], self.p[pointId], self.p[min(pointId + 1, last_index_p)], self.p[min(pointId + 2, last_index_p)])
                dx = self.p[min(pointId + 1, last_index_p)].x - self.p[pointId].x
                x = 0.0
                if dx != 0.0:
                    x = (tx - self.p[pointId].x) / dx
                self.__buffer.append(self.__getSplinePos(coefs, x) * self.multiplier)
                tx += self.dX

        return

    def calc(self, x):
        x = x * self.scale
        bufferLen = len(self.__buffer)
        if bufferLen > 0:
            if self.intX == 0:
                return self.p[0].y
            id = int((x - self.p[0].x) / float(self.intX) * float(self.pointCount - 1))
            norm = (x - float(id) * self.dX - self.p[0].x) / self.dX
            if id < 0:
                return self.p[0].y
            elif id >= bufferLen - 1:
                return self.p[-1].y
            else:
                return self.__buffer[id] * (1.0 - norm) + self.__buffer[id + 1] * norm
        else:
            raise CurveIsEmptyException()
        return 0.0

    def copy(self):
        copyObj = Curve()
        copyObj.p = self.p[:]
        copyObj.__buffer = self.__buffer[:]
        copyObj.pointCount = self.pointCount
        return copyObj


class Curve2(Curve):

    def __init__(self, knots = [], pointCount = 10):
        self.knots = list(knots)
        Curve.__init__(self, self.__stretch(), pointCount)

    def setPoints(self, knots):
        self.knots = list(knots)
        self.p = self.__stretch()
        self.refresh()

    def getPoints(self):
        return self.knots

    def __stretch(self):
        if len(self.knots) <= 1:
            return self.knots
        v1 = self.knots[0] - self.knots[1]
        v2 = self.knots[-1] - self.knots[-2]
        newKnots = [v1 * 2.0 + self.knots[0], v1 + self.knots[0]] + self.knots + [v2 + self.knots[-1], v2 * 2.0 + self.knots[-1]]
        return newKnots


class AkimaInterpolation:
    """
    This class initiate Hiroshi Akima method of points interpolation.
    For correct use this method, you need on create input more then 5 points: [Math.Vector2(), Math.Vector2(), ..]
    http://www.leg.ufpr.br/lib/exe/fetch.php/wiki:internas:biblioteca:akima.pdf
    """

    def __init__(self, points = list(), coarse = 1):
        self.__clientPoints = points
        self.__coarse = coarse
        self.__points = []
        self.__slops = []
        self.__refresh()

    def setPoints(self, points):
        self.__clientPoints = points
        self.__refresh()

    def getPoints(self):
        return self.__clientPoints

    def __dataValidation(self):
        if self.__clientPoints.__len__() < 2:
            raise ValueError('number of points is not correct ( < 2)')
        self.__clientPoints = sorted(self.__clientPoints, key=lambda p: p.x)
        for i in xrange(self.__clientPoints.__len__() - 1):
            if self.__clientPoints[i].x > self.__clientPoints[i + 1].x:
                raise ValueError('duplicated point')

    def __multiplyPoints(self):
        v1 = self.__clientPoints[0] - self.__clientPoints[1]
        v2 = self.__clientPoints[-1] - self.__clientPoints[-2]
        stretchStart = [v1 * 3.0 + self.__clientPoints[0], v1 + self.__clientPoints[0]]
        stretchEnd = [v2 + self.__clientPoints[-1], v2 * 3.0 + self.__clientPoints[-1]]
        self.__points += stretchStart
        if self.__coarse > 0:
            for index in xrange(self.__clientPoints.__len__() - 1):
                vector = (self.__clientPoints[index + 1] - self.__clientPoints[index]) / self.__coarse
                addList = [ self.__clientPoints[index] + vector * n for n in xrange(self.__coarse) ]
                self.__points += addList

            self.__points.append(self.__clientPoints[-1])
        else:
            raise ValueError('Not correct "coarse" value...')
        self.__points += stretchEnd

    def __refresh(self):
        self.__dataValidation()
        self.__multiplyPoints()
        POINTS = [None, None] + self.__points + [None, None]
        for index in xrange(self.__points.__len__()):
            self.__slops.append(self._getSlop(POINTS[index:index + 5]))

        return

    def calc(self, x):
        if x < self.__points[0].x or x > self.__points[-1].x:
            raise ValueError('x is not in range')
        for index, p in enumerate(self.__points):
            nextP = self.__points[index + 1]
            if x >= p.x and x <= nextP.x:
                if p.y == nextP.y:
                    return 0.5 * (p.y + nextP.y)
                return self._localCalc(x, p, nextP, self.__slops[index], self.__slops[index + 1])

    def _localCalc(self, x, p1, p2, t1, t2):
        localIntervalX = p2.x - p1.x
        median = (p2.y - p1.y) / localIntervalX
        q0 = p1.y
        q1 = t1
        q2 = (3.0 * median - 2.0 * t1 - t2) / localIntervalX
        q3 = (t1 + t2 - 2.0 * median) / localIntervalX ** 2
        dx = x - p1.x
        return q0 + (q1 + (q2 + q3 * dx) * dx) * dx

    def _getSlop(self, args):
        point1 = args[0]
        point2 = args[1]
        point3 = args[2]
        point4 = args[3]
        point5 = args[4]
        m = lambda p2, p1: (p2.y - p1.y) / (p2.x - p1.x)
        if point1 is None:
            m4 = m(point5, point4)
            m3 = m(point4, point3)
            m2 = 2.0 * m3 - m4 if point2 is None else m(point3, point2)
            m1 = 3.0 * m3 - 2.0 * m4 if point2 is None else 2.0 * m3 - m4
        elif point5 is None:
            m1 = m(point2, point1)
            m2 = m(point3, point2)
            m3 = 2.0 * m2 - m1 if point4 is None else m(point4, point3)
            m4 = 3.0 * m2 - 2.0 * m1 if point4 is None else 2.0 * m2 - m1
        else:
            m1 = m(point2, point1)
            m2 = m(point3, point2)
            m3 = m(point4, point3)
            m4 = m(point5, point4)
        numerator = m2 * abs(m4 - m3) + m3 * abs(m2 - m1)
        denominator = abs(m4 - m3) + abs(m2 - m1)
        if denominator:
            return numerator / denominator
        else:
            return 0.5 * (m2 + m3)
            return


class CubicBezier:

    def __init__(self, knots = list(), z = 0.4, angleFactor = 0.95):
        self.__knots = knots
        self.__controlPts = []
        self.__z = z
        self.__angleFactor = angleFactor
        self.__bottomBorder = Math.Vector2(0.0, 0.0)
        self.__topBorder = Math.Vector2(1.0, 1.0)
        self.__refresh()

    def getPoints(self):
        return self.__knots

    def setPoints(self, points):
        self.__knots = points
        self.__refresh()

    def __initBorders(self):
        Y = sorted(self.__knots, key=lambda p: p.y)
        self.__bottomBorder = Math.Vector2(self.__knots[0].x, Y[0].y)
        self.__topBorder = Math.Vector2(self.__knots[-1].x, Y[-1].y)

    def __refresh(self):
        self.__initBorders()
        _len_ = lambda v2: math.sqrt(v2.x ** 2 + v2.y ** 2)
        polar = lambda r, fi: Math.Vector2(r * math.cos(fi), r * math.sin(fi))
        if len(self.__knots) > 2:
            for i in xrange(self.__knots.__len__()):
                p0 = self.__knots[-1] if i - 1 < 0 else self.__knots[i - 1]
                p1 = self.__knots[i]
                p2 = self.__knots[1] if i + 1 == len(self.__knots) else self.__knots[i + 1]
                a = max(0.001, _len_(p0 - p1))
                b = max(0.001, _len_(p1 - p2))
                c = max(0.001, _len_(p0 - p2))
                cos = clamp(-1.0, (b * b + a * a - c * c) / (2 * b * a), 1.0)
                angle = math.acos(cos)
                aPt = p0 - p1
                bPt = Math.Vector2(p1.x, p1.y)
                cPt = p2 - p1
                if a > b:
                    aPt = aPt * b / _len_(aPt)
                elif b > a:
                    cPt = cPt * a / _len_(cPt)
                aPt = aPt + p1
                cPt = cPt + p1
                va = bPt - aPt
                vb = bPt - cPt
                r = va + vb
                if _len_(r) == 0:
                    r = Math.Vector2(-vb.x, vb.y)
                if va.y == 0 and vb.y == 0:
                    r = Math.Vector2(0, 1)
                elif va.x == 0 and vb.x == 0:
                    r = Math.Vector2(1, 0)
                theta = math.atan2(r.y, r.x)
                controlDist = self.__z * min(a, b)
                controlScaleFactor = angle / math.pi
                controlDist *= 1 - self.__angleFactor + self.__angleFactor * controlScaleFactor
                controlAngle = theta + 0.5 * math.pi
                controlPoint2 = polar(controlDist, controlAngle)
                controlPoint1 = polar(controlDist, controlAngle + math.pi)
                controlPoint1 = controlPoint1 + p1
                controlPoint2 = controlPoint2 + p1
                hypot2 = _len_(p2 - controlPoint2)
                hypot1 = _len_(p2 - controlPoint1)
                if hypot2 > hypot1:
                    self.__controlPts.append([controlPoint2, controlPoint1])
                else:
                    self.__controlPts.append([controlPoint1, controlPoint2])

    def getValue(self, t, a, b, c, d):
        ax = a.x
        x = (t * t * (d.x - ax) + 3 * (1 - t) * (t * (c.x - ax) + (1 - t) * (b.x - ax))) * t + ax
        ay = a.y
        y = (t * t * (d.y - ay) + 3 * (1 - t) * (t * (c.y - ay) + (1 - t) * (b.y - ay))) * t + ay
        return Math.Vector2(x, y)

    def calc(self, x):
        if x < self.__bottomBorder.x or x > self.__topBorder.x:
            raise ValueError('x is not in range')
        for index, p in enumerate(self.__knots):
            nextP = self.__knots[index + 1]
            if x >= p.x and x <= nextP.x:
                if p.y == nextP.y:
                    return 0.5 * (p.y + nextP.y)
                if len(self.__knots) == 2:
                    return p.y + (x - p.x) / (nextP.x - p.x) * (nextP.y - p.y)
                if len(self.__knots) < 2:
                    raise ValueError('number of points < 2')
                func = lambda t: self.getValue(t, p, self.__controlPts[index][1], self.__controlPts[index + 1][0], nextP).x - x
                t = self.__nullFunction(func, 0, 1.0, 0.001)[0]
                value = self.getValue(t, p, self.__controlPts[index][1], self.__controlPts[index + 1][0], nextP)
                return clamp(self.__bottomBorder.y, value.y, self.__topBorder.y)

    def __nullFunction(self, function, minX, maxX, eps = 0.001):
        if function(minX) > function(maxX):
            tempX = minX
            minX = maxX
            maxX = tempX
        if function(minX) > 0.0 and function(maxX) > 0.0 or function(minX) < 0.0 and function(maxX) < 0.0:
            return (0, 0)
        X = (minX + maxX) * 0.5
        func = function(X)
        from itertools import count
        for _ in count(1):
            if func < 0.0 - eps:
                minX = X
            elif func > 0.0 + eps:
                maxX = X
            else:
                break
            X = (minX + maxX) * 0.5
            func = function(X)

        return (X, func)


def printSpline(_str_, p, _class_):
    with open(_str_, 'w+') as f:
        dX = p[-1].x - p[0].x
        x0 = p[0].x
        for i in xrange(201):
            a = x0 + dX * i / 200.0
            b = _class_.calc(a)
            s = ' '.join((str(a), str(b))) + '\n'
            f.write(s)


if __name__ == '__main__':
    pointsList = [Math.Vector2(0, 10),
     Math.Vector2(1, 10),
     Math.Vector2(2, 10),
     Math.Vector2(3, 10),
     Math.Vector2(4, 10),
     Math.Vector2(5, 10),
     Math.Vector2(6, 10.5),
     Math.Vector2(7, 15),
     Math.Vector2(8, 50),
     Math.Vector2(9, 60),
     Math.Vector2(10, 85)]
    printSpline('akima.txt', pointsList, AkimaInterpolation(pointsList))
    printSpline('curve2.txt', pointsList, Curve2(pointsList, 100))
    printSpline('curve.txt', pointsList, Curve(pointsList, 100))
    printSpline('bezier.txt', pointsList, CubicBezier(pointsList[:]))