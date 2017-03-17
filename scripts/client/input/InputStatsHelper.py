# Embedded file name: scripts/client/input/InputStatsHelper.py
__author__ = 'm_antipov'
import BigWorld
from debug_utils import LOG_TRACE, LOG_DEBUG

class InputStatsHelper:

    class CommandStats:

        def __init__(self, idCommand):
            self.idCommand = idCommand
            self.started = False
            self.timeStart = 0
            self.commandDuration = 0
            self.measurementDuration = 0
            self.commandUsageValue = 0

    def __init__(self):
        self.__commandFilter = ['CMD_BOMBING_SIGHT',
         'CMD_BACK_VIEW',
         'CMD_TARGET_CAMERA',
         'CMD_CURSOR_CAMERA',
         'CMD_SNIPER_CAMERA',
         'CMD_BOMBING_SIGHT',
         'CMD_BATTLE_MODE']
        self.__commandTimings = dict()
        self.__startTime = None
        self.__measuredTime = 0
        self.__commandUsageStats = dict()
        self.__prevGatherInterval = 0
        self.__startGatheringStats = False
        self.__isContinuousGathering = True
        return

    def __getCommandStats(self, idCommand):
        commandStats = self.__commandTimings.get(idCommand)
        if commandStats is None:
            commandStats = InputStatsHelper.CommandStats(idCommand)
            self.__commandTimings[idCommand] = commandStats
        return commandStats

    def __isLogged(self, idCommand):
        if self.__commandFilter:
            return idCommand in self.__commandFilter
        else:
            return True

    def setCommandFilter(self, filter):
        self.__commandFilter = filter

    def startGatheringStats(self):
        self.__startTime = BigWorld.time()
        self.__startGatheringStats = True

    def stopGatheringStats(self):
        self.__startGatheringStats = False
        self.gatherStats()
        if not self.__isContinuousGathering:
            self.reset()

    def reset(self):
        self.__commandTimings.clear()

    def gatherStats(self):
        if self.__startTime is None:
            return dict()
        else:
            measuredTime = BigWorld.time() - self.__startTime
            for key, value in self.__commandTimings.iteritems():
                value.commandUsageValue = (value.commandUsageValue * value.measurementDuration + value.commandDuration) / (value.measurementDuration + measuredTime)
                value.commandDuration = 0
                value.measurementDuration = value.measurementDuration + measuredTime
                self.__commandUsageStats[key] = value.commandUsageValue

            self.__startTime = BigWorld.time()
            return self.__commandUsageStats

    @property
    def isGatheringStats(self):
        return self.__startGatheringStats

    def logCommandStart(self, idCommand):
        if not self.__startGatheringStats:
            return
        if not self.__isLogged(idCommand):
            return
        commandStats = self.__getCommandStats(idCommand)
        if commandStats.started:
            LOG_TRACE('event %s already started' % idCommand)
        else:
            commandStats.started = True
            commandStats.timeStart = BigWorld.time()

    def logCommandEnd(self, idCommand):
        if not self.__startGatheringStats:
            return
        if not self.__isLogged(idCommand):
            return
        commandStats = self.__getCommandStats(idCommand)
        if not commandStats.started:
            LOG_DEBUG('event %s ended without beginning' % idCommand)
            commandStats.started = False
            if self.__startTime:
                commandStats.commandDuration += BigWorld.time() - self.__startTime
        else:
            commandStats.started = False
            commandStats.commandDuration += BigWorld.time() - commandStats.timeStart