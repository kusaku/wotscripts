# Embedded file name: scripts/common/db/DBHelpers.py
import BigWorld
import Math
from Curve import Curve, Curve2
from consts import IS_CLIENT, IS_EDITOR
import consts
import ResMgr
from debug_utils import *

def compareField(curV, etalonV, path):
    t = type(etalonV)
    ct = type(curV)
    if ct != t:
        LOG_WARNING('!!!DB verification - data structure changed', ct, t, path)
    elif t == int or t == float or t == bool or t == str:
        if curV != etalonV:
            LOG_WARNING('!!!DB verification ', curV, ' != ', etalonV, path)
    elif t == list or t == tuple:
        for i, v in enumerate(etalonV):
            compareField(curV[i], v, path + '[' + str(i) + ']')

    elif t == dict:
        for k, v in etalonV.items():
            compareField(curV[k], v, path + '{' + str(k) + '}')

    elif etalonV.__class__ == Math.Vector2:
        if etalonV.x != curV.x or etalonV.y != curV.y:
            LOG_WARNING('!!!DB verification ', curV, ' != ', etalonV, path)
    elif etalonV.__class__ == Math.Vector3:
        if etalonV.x != curV.x or etalonV.y != curV.y or etalonV.z != curV.z:
            LOG_WARNING('!!!DB verification ', curV, ' != ', etalonV, path)
    elif etalonV.__class__ == Math.Vector4:
        if etalonV.x != curV.x or etalonV.y != curV.y or etalonV.z != curV.z or etalonV.w != curV.w:
            LOG_WARNING('!!!DB verification ', curV, ' != ', etalonV, path)
    elif etalonV is not None:
        for k, v in etalonV.__dict__.items():
            compareField(curV.__dict__[k], v, path + '.' + k)

    return


def fillDictionaryByNodes(dict, sectionData):
    if sectionData is not None:
        for id in sectionData.keys():
            if id not in dict:
                dict[id] = 1

    return


def fillDictionaryByValues(dict, sectionData):
    if sectionData is not None:
        for id in sectionData.keys():
            dict[id] = sectionData.readString(id)

    return


def updateValue(self, data, name, default):
    if data != None:
        if not hasattr(self, name) or data.has_key(name):
            readValue(self, data, name, default)
    elif not hasattr(self, name):
        setattr(self, name, default)
    return


def readValue(self, data, name, default = None, isTuple = False, missingCheck = True):
    if missingCheck and not data.has_key(name):
        if not hasattr(self, name):
            if IS_CLIENT:
                dbIntegrityError(data, 'field', name)
        else:
            return False
    if not isTuple:
        if isinstance(default, Math.Vector3):
            setattr(self, name, data.readVector3(name, default))
        elif type(default) == Math.Vector2:
            setattr(self, name, data.readVector2(name, default))
        elif type(default) == str:
            setattr(self, name, data.readString(name, default))
        elif default.__class__.__name__ == 'Curve2':
            readCurve2(self, data, name, default)
        elif isinstance(default, Curve):
            readCurve(self, data, name, default)
        elif type(default) == int:
            setattr(self, name, data.readInt(name, default))
        elif type(default) == bool:
            setattr(self, name, data.readBool(name, default))
        else:
            setattr(self, name, data.readFloat(name, default))
    elif isinstance(default, Math.Vector3):
        setattr(self, name, data.readVector3s(name))
    elif isinstance(default, Math.Vector2):
        setattr(self, name, data.readVector2s(name))
    else:
        setattr(self, name, data.readFloats(name))
    return True


def readValues(self, data, values):
    for value in values:
        readValue(self, data, *value)


def writeValue(self, data, name, default, isTuple = False):
    value = getattr(self, name, default)
    if value is None:
        return
    else:
        if not isTuple:
            if isinstance(value, Math.Vector3):
                data.writeVector3(name, value)
            elif isinstance(value, Math.Vector2):
                data.writeVector2(name, value)
            elif type(value) == str:
                data.writeString(name, value)
            elif isinstance(value, Curve2):
                writeCurve2(self, data, name, value)
            elif isinstance(value, Curve):
                writeCurve(self, data, name, value)
            elif type(value) == bool:
                data.writeBool(name, value)
            elif type(value) == int:
                data.writeInt(name, value)
            else:
                data.writeFloat(name, value)
        elif isinstance(default, Math.Vector3):
            data.writeVector3s(name, value)
        else:
            data.writeFloats(name, value)
        return


def writeValues(self, data, values):
    for value in values:
        writeValue(self, data, *value)


def readColor(self, data, name, default):
    r = data.readVector4(name, default)
    res = int(r.w) << 24 | int(r.x) << 16 | int(r.y) << 8 | int(r.z)
    setattr(self, name, res)


def readCurve(self, data, name, default):
    if hasattr(self, name):
        parrentAttr = getattr(self, name)
    else:
        parrentAttr = None
    section = findSection(data, name)
    if section != None:
        default.p = section.readVector2s('p')
        if len(default.p) == 0:
            if hasattr(parrentAttr, 'p') and len(parrentAttr.p) != 0:
                default.p = parrentAttr.p
        if hasattr(parrentAttr, 'pointCount'):
            def_pointCount = parrentAttr.pointCount
        else:
            def_pointCount = 10
        default.pointCount = section.readInt('pointCount', def_pointCount)
        if hasattr(parrentAttr, 'multiplier'):
            def_multiplier = parrentAttr.multiplier
        else:
            def_multiplier = 1
        default.multiplier = section.readFloat('multiplier', def_multiplier)
        default.refresh()
    elif IS_CLIENT:
        dbIntegrityError(data, 'field', name)
    setattr(self, name, default)
    return


def writeCurve(self, data, name, value):
    section = findSection(data, name)
    if section is not None:
        if hasattr(value, 'p'):
            for i in range(len(section.readVector2s('p'))):
                section.deleteSection('p')

            section.writeVector2s('p', value.p)
        if hasattr(value, 'pointCount'):
            section.writeInt('pointCount', value.pointCount)
        if hasattr(value, 'multiplier'):
            section.writeFloat('multiplier', value.multiplier)
    return


def findSection(data, sectionID, missingCheck = True):
    if data.has_key(sectionID):
        return data[sectionID]
    else:
        if IS_CLIENT and missingCheck:
            dbIntegrityError(data, 'section', sectionID)
        return None


def dbIntegrityError(data, dType, field):
    if consts.ENABLE_DB_VERIFICATION:
        LOG_ERROR('DB integrity error - missing {dType} {field}'.format(dType=dType, field=data.name + '.' + field))


def readDataWithDependencies(customer, data, parentFolder, rootFolder = consts.DB_PATH, newDatabase = None):
    if data:
        parentPath = data.readString('parent')
        if len(parentPath) > 0:
            parentPath = rootFolder + parentFolder + '/' + parentPath
            parent = ResMgr.openSection(parentPath)
            if parent:
                readDataWithDependencies(customer, parent, parentFolder, rootFolder, None)
        if newDatabase:
            customer.readData(data, newDatabase)
        else:
            customer.readData(data)
    return


def readValueOnCondition(self, data, name, condition, default, missingCheck = True):
    """ You can use this function for next value types: int, false, string, Vector2, Vector3, Curve """
    if missingCheck and not data.has_key(name):
        if not hasattr(self, name):
            if IS_CLIENT:
                dbIntegrityError(data, 'field', name)
        else:
            return False
    if isinstance(default, Math.Vector3):
        value = data.readVector3(name, default)
        if condition(value):
            setattr(self, name, value)
    elif isinstance(default, Math.Vector2):
        value = data.readVector2(name, default)
        if condition(value):
            setattr(self, name, value)
    elif isinstance(default, str):
        value = data.readString(name, default)
        if condition(value):
            setattr(self, name, value)
    elif isinstance(default, Curve):
        value = findSection(data, name)
        if condition(value):
            readCurve(self, data, name, default)
    elif isinstance(default, float):
        value = data.readFloat(name, default)
        if condition(value):
            setattr(self, name, value)
    elif isinstance(default, int):
        value = data.readInt(name, default)
        if condition(value):
            setattr(self, name, value)
    else:
        LOG_ERROR('readValueOnRange: type error on read value of {_name_}'.format(_name_=name))
        return False
    return True


def readCurve2(self, data, name, default):
    if hasattr(self, name):
        parentAttr = getattr(self, name)
    else:
        parentAttr = None
    section = findSection(data, name)
    if section is not None:
        p = section.readVector2s('p')
        default.setPoints(p)
        if parentAttr is not None and len(default.getPoints()) == 0:
            default.setPoints(parentAttr.getPoints())
    elif IS_CLIENT:
        dbIntegrityError(data, 'field', name)
    setattr(self, name, default)
    return


def writeCurve2(self, data, name, value):
    section = findSection(data, name)
    if section is not None:
        for i in xrange(len(section.readVector2s('p'))):
            section.deleteSection('p')

        section.writeVector2s('p', value.getPoints())
    return