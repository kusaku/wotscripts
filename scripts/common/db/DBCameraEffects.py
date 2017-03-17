# Embedded file name: scripts/common/db/DBCameraEffects.py
from DBHelpers import *
from consts import WORLD_SCALING
import math

class CameraPresetInfo(object):

    def __init__(self, ampFactor, normSpeedShift):
        self.amplitudeFactor = ampFactor
        self.normSpeedShift = normSpeedShift


class WakeEffectParams(object):

    def __init__(self):
        self.distance = 0.0
        self.angle = 0.0


class CameraEffects(object):

    def __init__(self, data = None):
        self.__camPresetInfo = {}
        self.__camPresetAmpFactorMin = 1.0
        self.__normSpeedAddRelNeigbourZone = 0.0
        self.__wakeParams = WakeEffectParams()
        self.__airwaveDistance = 0.0
        self.readData(data)

    @property
    def airwaveDistance(self):
        return self.__airwaveDistance

    @property
    def wakeParams(self):
        return self.__wakeParams

    @property
    def normSpeedAddRelNeigbourZone(self):
        return self.__normSpeedAddRelNeigbourZone

    @property
    def camPresetAmpFactorMin(self):
        return self.__camPresetAmpFactorMin

    @property
    def camPresetInfo(self):
        return self.__camPresetInfo

    @property
    def rammingEffectSplitter(self):
        return self.__rammingEffectSplitter

    def readData(self, data):
        if data != None:
            paramsSection = findSection(data, 'params')
            if paramsSection:
                camDepSettingsSection = findSection(paramsSection, 'cameraDependantSettings')
                if camDepSettingsSection:
                    for cameraGroupSection in camDepSettingsSection.values():
                        amplutudeFactor = cameraGroupSection.readFloat('factor')
                        normSpeedShift = cameraGroupSection.readFloat('normSpeedShift')
                        if amplutudeFactor < self.__camPresetAmpFactorMin:
                            self.__camPresetAmpFactorMin = amplutudeFactor
                        cameraPresetsSection = findSection(cameraGroupSection, 'cameraPresets')
                        if cameraPresetsSection:
                            for entry in cameraPresetsSection.values():
                                cameraID = entry.asString
                                self.__camPresetInfo[cameraID] = CameraPresetInfo(amplutudeFactor, normSpeedShift)

                commonParamsSection = findSection(paramsSection, 'common')
                if commonParamsSection:
                    self.__normSpeedAddRelNeigbourZone = commonParamsSection.readFloat('normSpeedAddRelNeigbourZone')
                    self.__airwaveDistance = commonParamsSection.readFloat('airwaveDistance') * WORLD_SCALING
                    self.__wakeParams.distance = commonParamsSection.readFloat('wakeDistance') * WORLD_SCALING
                    self.__wakeParams.angle = math.radians(commonParamsSection.readFloat('wakeAngle'))
                    self.__rammingEffectSplitter = commonParamsSection.readFloat('rammingEffectSplitter')
        return