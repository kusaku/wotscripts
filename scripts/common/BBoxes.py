# Embedded file name: scripts/common/BBoxes.py
import Math
from consts import WORLD_SCALING, IS_EDITOR
from debug_utils import *
from MathExt import clamp
DEFAULT_ABSORPTION = 1.0

def isZeroQuaternion(quaternion):
    return quaternion.x == 0 and quaternion.y == 0 and quaternion.z == 0 and quaternion.w == 0


class BBox:

    def __init__(self, data = None, scaling = 1.0):
        self.pos = Math.Vector3()
        self.size = Math.Vector3()
        self.hasFixedRotation = False
        self.rotation = Math.Quaternion(0, 0, 0, 1)
        self.absorption = 0.0
        self.armorFront = Math.Vector3()
        self.armorBack = Math.Vector3()
        if data is not None:
            self.pos = data.readVector3('position', Math.Vector3())
            self.pos *= WORLD_SCALING * scaling
            self.size = data.readVector3('size', Math.Vector3())
            if self.size.x < 0.0 or self.size.y < 0.0 or self.size.z < 0.0:
                LOG_ERROR('BBOX incorrect size', self.size)
            self.size *= WORLD_SCALING * 0.5 * scaling
            self.rotation = Math.Quaternion(data.readVector4('rotation', Math.Vector4(0, 0, 0, 1)))
            if isZeroQuaternion(self.rotation):
                self.rotation = Math.Quaternion(Math.Vector4(0, 0, 0, 1))
                self.hasFixedRotation = True
            self.absorption = data.readFloat('absorption', DEFAULT_ABSORPTION)
            if self.absorption < 0.0 or self.absorption > 1.0:
                DBLOG_NOTE('invalid absorption ' + str(self.absorption))
                self.absorption = clamp(0.0, self.absorption, 1.0)
            self.armorFront = data.readVector3('armorFront', Math.Vector3())
            self.armorBack = data.readVector3('armorBack', Math.Vector3())
            if IS_EDITOR:
                self.__data = data
                self.__scaling = WORLD_SCALING * scaling
        return

    def save(self):
        if IS_EDITOR and self.__data:
            from db.DBHelpers import writeValue
            self.__data.writeVector3('position', self.pos / self.__scaling)
            self.__data.writeVector3('size', self.size / (self.__scaling * 0.5))
            self.__data.writeVector4('rotation', self.rotation.toVec4())
            writeValue(self, self.__data, 'absorption', DEFAULT_ABSORPTION)
            writeValue(self, self.__data, 'armorFront', Math.Vector3())
            writeValue(self, self.__data, 'armorBack', Math.Vector3())

    def getArmor(self, rayStartPoint, objPosition, objRotation):
        relRayStart = rayStartPoint - objPosition
        invRotation = Math.Quaternion(objRotation)
        invRotation.invert()
        relRayStart = invRotation.rotateVec(relRayStart)
        if relRayStart.x > 0 and relRayStart.x > abs(relRayStart.y) and relRayStart.x > abs(relRayStart.z):
            return self.armorFront.x
        if relRayStart.y > 0 and relRayStart.y > abs(relRayStart.x) and relRayStart.y > abs(relRayStart.z):
            return self.armorFront.y
        if relRayStart.z > 0 and relRayStart.z > abs(relRayStart.x) and relRayStart.z > abs(relRayStart.y):
            return self.armorFront.z
        if relRayStart.y < 0 and abs(relRayStart.x) > abs(relRayStart.y) and abs(relRayStart.x) > abs(relRayStart.z):
            return self.armorBack.x
        if relRayStart.y < 0 and abs(relRayStart.y) > abs(relRayStart.x) and abs(relRayStart.y) > abs(relRayStart.z):
            return self.armorBack.y
        if relRayStart.z < 0 and abs(relRayStart.z) > abs(relRayStart.x) and abs(relRayStart.z) > abs(relRayStart.y):
            return self.armorBack.z
        return min(self.armorFront.x, self.armorFront.y, self.armorFront.z, self.armorBack.x, self.armorBack.y, self.armorBack.z)

    def copyContructor(srcBbox):
        copy = BBox()
        copy.pos = srcBbox.pos
        copy.size = srcBbox.size
        copy.rotation = srcBbox.rotation


class BBoxes:
    DEFAULT_POSITION = Math.Vector3()

    def __init__(self, section = None, scaling = 1.0):
        self.list = []
        self.fixedBBoxesCounter = 0
        if section != None:
            for id, data in section.items():
                box = BBox(data, scaling)
                if box.hasFixedRotation:
                    self.fixedBBoxesCounter += 1
                if box.size.lengthSquared < 0.01:
                    continue
                if id != 'mainBBox':
                    self.list.append(box)
                else:
                    self.list.insert(0, box)

        return

    def save(self):
        if IS_EDITOR:
            for box in self.list:
                box.save()

    def getMainBBoxSize(self):
        return self.list[0].size

    def getMainBBoxPosition(self):
        return len(self.list) > 0 and self.list[0].pos or BBoxes.DEFAULT_POSITION

    def getMainBBoxAbsorption(self):
        if self.list:
            return self.list[0].absorption
        return DEFAULT_ABSORPTION

    def shiftBBoxes(self, position):
        if self.list:
            for box in self.list:
                box.pos -= position

    def getList(self):
        return self.list

    def copy(self):
        copyObj = BBoxes()
        for v in self.list:
            copyObj.list.append(BBox.copyContructor(v))

        return copyObj