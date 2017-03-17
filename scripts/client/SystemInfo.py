# Embedded file name: scripts/client/SystemInfo.py
__author__ = 'r_dolgarev'
import BigWorld
import ResMgr
import debug_utils
import Settings
import math
from functools import partial
AUTO_CONFIG_SETTINGS = 'system/data/auto_config_settings.xml'

class SystemInfo:

    def __init__(self):
        self.__si = BigWorld.SystemInfo()
        self.__benchChain = []
        self.__chainCB = None
        self.__bounds = []
        self.__results = {}
        self.__readData()
        self.__endCB = None
        return

    def __readData(self):
        root = ResMgr.openSection(AUTO_CONFIG_SETTINGS)
        for tag, presetReq in root.items():
            presetName = presetReq.asString
            bounds = dict()
            for key, value in presetReq.items():
                bounds[key] = value.asInt

            level = [ index for index, name in Settings.GRAPHICS_QUALITY_NAMES.iteritems() if name == presetName ][0]
            self.__bounds.insert(level, bounds)

        ResMgr.purge(AUTO_CONFIG_SETTINGS)

    def detect(self, cb = None):
        debug_utils.LOG_INFO('Benchmark test started')
        self.__endCB = cb
        self.__benchChain.append(partial(self.__resultCB, 'VirtualMemory', self.__si.memoryVirtual))
        self.__benchChain.append(partial(self.__resultCB, 'RAM', self.__si.memoryPhysical))
        self.__benchChain.append(partial(self.__resultCB, 'GPUMemory', self.__si.memoryGPU))
        self.__benchChain.append(partial(self.__si.runCPUBench, partial(self.__resultCB, 'CPURating'), 32))
        self.__benchChain.append(partial(self.__si.runGPUBench, partial(self.__resultGPU, 'GPURating')))
        self.__chainStep()

    def __resultGPU(self, name, result):
        cur = BigWorld.screenWidth() * BigWorld.screenHeight()
        hd = 2073600.0
        k = math.sqrt(hd / cur)
        rating = int(result * k)
        debug_utils.LOG_INFO('GPU benchmark result:{0}, k:{1}, rating:{2}'.format(result, k, rating))
        return self.__resultCB(name, rating)

    def __resultCB(self, name, result):
        self.__results[name] = result
        self.__chainStep()
        return True

    def __chainStep(self):
        if self.__benchChain:
            step = self.__benchChain.pop()
            if not step():
                self.__benchChain.append(step)
                self.__chainCB = BigWorld.callback(1.0, self.__chainStep)
        else:
            self.__finalize()

    def __finalize(self):
        endLevel = len(Settings.GRAPHICS_QUALITY_NAMES)
        totalLevel = 0
        debug_utils.LOG_INFO('Benchmark test finished')
        for name, result in self.__results.iteritems():
            level = endLevel
            for idx, requirement in enumerate(self.__bounds):
                minimal = requirement.get(name)
                if minimal is not None:
                    if result >= minimal:
                        level = idx
                        break

            if level > totalLevel:
                totalLevel = level
            debug_utils.LOG_INFO(name, result, Settings.GRAPHICS_QUALITY_NAMES.get(level, 'Lower than the minimal requirements'))

        if self.__endCB:
            self.__endCB(totalLevel)
            self.__endCB = None
        return

    @property
    def rating(self):
        return ('CPURating:' + str(self.__results.get('CPURating', 0)), 'GPURating:' + str(self.__results.get('GPURating', 0)))

    @property
    def hardwareInfo(self):
        hardwares = ('RAM:' + str(self.__si.memoryPhysical),
         'VRAM: ' + str(self.__si.memoryGPU),
         'VMEM: ' + str(self.__si.memoryVirtual),
         self.__si.infoCPU,
         self.__si.infoGPU)
        return hardwares