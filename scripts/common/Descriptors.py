# Embedded file name: scripts/common/Descriptors.py
from consts import INVALID_POSITION
import struct
from debug_utils import *
import Math
__teamObjectMask = '=LH?Hhhh'

def createTeamObjectCompactDescriptor(entityID, arenaObjID, isAlive, maxHealth, position):
    return struct.pack(__teamObjectMask, entityID, arenaObjID, isAlive, maxHealth, int(position.x + 0.5), int(position.y + 0.5), int(position.z + 0.5))


def getTeamObjectDescriptorFromCompactDescriptor(compactDescriptor):
    data = struct.unpack(__teamObjectMask, compactDescriptor)
    return {'id': data[0],
     'arenaObjID': data[1],
     'isAlive': data[2],
     'maxHealth': data[3],
     'pos': Math.Vector3(data[4], data[5], data[6])}


def packVariablesToInt(descriptions, *variables):
    """
        @param descriptions: [(strVarName, maxVarSizeInBits)]. 
        If you want to pack signed values maxVarSizeInBits must be negative value for each one!!!
        @param variables: variables to pack. You'll got error if len(variables) != len(descriptions)!!!
        @return: all variables data packed into Int
    """
    dLen = len(descriptions)
    vLen = len(variables)
    if dLen != vLen:
        LOG_ERROR('different len for descriptions', descriptions, 'and variables', variables)
        return
    minLen = min(dLen, vLen)
    shift = 0
    v = 0
    for i in xrange(minLen):
        size = abs(descriptions[i][1])
        vv = abs(variables[i])
        if descriptions[i][1] > 0:
            if variables[i] > (1 << size) - 1:
                LOG_ERROR('data lost for', i, 'variable in', variables, variables[i], 'incorrect descriptions', descriptions[i])
        else:
            if abs(variables[i]) > (1 << size - 1) - 1:
                LOG_ERROR('data lost for', i, 'variable in', variables, variables[i], 'incorrect descriptions', descriptions[i])
            if variables[i] < 0:
                vv |= 1 << size - 1
        v |= vv << shift
        shift += size

    return v


def unpackIntToDict(descriptions, v):
    shift = 0
    d = {}
    for desc in descriptions:
        size = abs(desc[1])
        vv = v >> shift & (1 << size) - 1
        if desc[1] < 0 and vv >> size - 1 == 1:
            vv = -(vv & (1 << size - 1) - 1)
        d[desc[0]] = vv
        shift += size

    return d