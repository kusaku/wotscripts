# Embedded file name: scripts/common/db/DBCameraMisc.py
from DBHelpers import *
from debug_utils import DBLOG_ERROR
from consts import WORLD_SCALING
import Math

class Preset:

    def __init__(self, data = None):
        self.readData(data)

    def readData(self, data):
        if data != None:
            readValue(self, data, 'moveSpeed', 0.0)
            readValue(self, data, 'rotationSpeed', 0.0)
            readValue(self, data, 'distance', 0.0)
            readValue(self, data, 'targetOffset', Math.Vector3(0, 0, 0))
            readValue(self, data, 'targetMoveSpeed', 0.0)
            readValue(self, data, 'distanceChangeSpeed', 0.0)
            readValue(self, data, 'fovStepFactor', 0.0005)
            readValue(self, data, 'aircraftRotationSpeed', 1.0)
            self.__postLoadTransform()
        return

    def __postLoadTransform(self):
        self.distance *= WORLD_SCALING
        self.targetOffset *= WORLD_SCALING


class CameraDebug:

    def __init__(self, data = None):
        self.__presets = []
        self.readData(data)

    def readData(self, data):
        if data != None:
            presets = findSection(data, 'presets')
            if presets != None:
                for presetData in presets.values():
                    self.__presets.append(Preset(presetData))

        return

    def getPreset(self, id):
        if id < len(self.__presets):
            return self.__presets[id]
        if len(self.__presets) == 0:
            DBLOG_ERROR("Can't get debug camera preset because preset array is empty!")
        else:
            DBLOG_ERROR("Can't find debug camera preset with ID: " + str(id))


class CameraMisc:

    def __init__(self, data = None):
        self.debugCamera = None
        self.readData(data)
        return

    def readData(self, data):
        if data != None:
            debugCamera = findSection(data, 'debugCamera')
            if debugCamera != None:
                self.debugCamera = CameraDebug(debugCamera)
        return