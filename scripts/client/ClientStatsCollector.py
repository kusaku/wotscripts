# Embedded file name: scripts/client/ClientStatsCollector.py
import BigWorld
import GameEnvironment
from GameServiceBase import GameServiceBase
import InputMapping
import Math
import MathExt
import Settings
from debug_utils import *
from consts import FPS_RANGES, SERVER_TICK_LENGTH
from wofdecorators import noexcept
from debug_utils import LOG_DEBUG
import time
STAT_MINIMAL_SEND_INTERVAL = 30

class ClientStatsCollector(GameServiceBase):

    def __init__(self):
        super(ClientStatsCollector, self).__init__()
        self.__stats = {}
        self.__stats['globalID'] = 0
        self.__stats['controllerProfileName'] = ''
        self.__stats['graphicsDetails'] = ''
        self.__stats['minFPS'] = 127
        self.__stats['medFPS'] = 0
        self.__stats['fpsRanges'] = [0] * (len(FPS_RANGES) + 1)
        self.__stats['keyboardUsagePercent'] = 0
        self.__stats['mouseUsagePercent'] = 0
        self.__stats['joystickUsagePercent'] = 0
        self.__stats['minPing'] = 1000
        self.__stats['medPing'] = 0
        self.__stats['lostRatio'] = 0
        self.__stats['skipIntro'] = -1
        self.__commandsUsageStats = []
        self.__fpsMeasurementsCount = 0
        self.__medFpsSum = 0
        self.__pingMeasurementsCount = 0
        self.__medPingSum = 0
        self.__lostRatioMeasurementsCount = 0
        self.__medLostRatioSum = 0
        self.__sendTime = 0
        self.__calculateStatsCallback = None
        return

    def setControllerProfileName(self, controllerProfileName):
        self.__stats['controllerProfileName'] = controllerProfileName

    def setGraphicsDetails(self, graphicsDetails):
        self.__stats['graphicsDetails'] = graphicsDetails

    def setFpsMin(self, fpsMin):
        fpsClamp = MathExt.clamp(0, fpsMin, 127)
        if fpsClamp < self.__stats['minFPS']:
            self.__stats['minFPS'] = fpsClamp

    def setFpsMed(self, fpsMed):
        fpsClamp = MathExt.clamp(0, fpsMed, 127)
        self.__medFpsSum += fpsClamp
        self.__fpsMeasurementsCount += 1
        self.__stats['medFPS'] = self.__medFpsSum / self.__fpsMeasurementsCount

    def updateFPSRanges(self, fps):
        value = 100000
        idx = 0
        for idx, value in enumerate(FPS_RANGES):
            if fps < value:
                break

        if value < fps:
            self.__stats['fpsRanges'][len(FPS_RANGES)] += 1
        else:
            self.__stats['fpsRanges'][idx] += 1

    def setPingMin(self, pingMin):
        if pingMin < self.__stats['minPing']:
            self.__stats['minPing'] = pingMin

    def setPingMed(self, pingMed):
        self.__medPingSum += pingMed
        self.__pingMeasurementsCount += 1
        self.__stats['medPing'] = self.__medPingSum / self.__pingMeasurementsCount

    def setLostRatioMed(self, lostRatioMed):
        self.__medLostRatioSum += lostRatioMed
        self.__lostRatioMeasurementsCount += 1
        self.__stats['lostRatio'] = float(self.__medLostRatioSum) / self.__lostRatioMeasurementsCount

    def setKeyboardUsagePercent(self, keyboardUsagePercent):
        self.__stats['keyboardUsagePercent'] = keyboardUsagePercent

    def setMouseUsagePercent(self, mouseUsagePercent):
        self.__stats['mouseUsagePercent'] = mouseUsagePercent

    def seJoystickUsagePercent(self, joystickUsagePercent):
        self.__stats['joystickUsagePercent'] = joystickUsagePercent

    def setZoomUsage(self, zoomUsage):
        self.__stats['zoomUsage'] = zoomUsage

    def setSkipIntro(self, skipIntro):
        self.__stats['skipIntro'] = skipIntro

    def __getStat(self, statName):
        if statName not in self.__stats:
            raise NameError, 'stats does not have field (%s)' % statName
        else:
            return self.__stats[statName]

    def getControllerProfileName(self):
        return self.__getStat('controllerProfileName')

    def getGraphicsDetails(self):
        return self.__getStat('graphicsDetails')

    def getMinFPS(self):
        return self.__getStat('minFPS')

    def getMedFPS(self):
        return self.__getStat('medFPS')

    def getFPSRanges(self):
        return self.__getStat('fpsRanges')

    def getMinPing(self):
        return self.__getStat('minPing')

    def getMedPing(self):
        return self.__getStat('medPing')

    def getMedLostRatio(self):
        return self.__getStat('lostRatio')

    def getKeyboardUsagePercent(self):
        return self.__getStat('keyboardUsagePercent')

    def getMouseUsagePercent(self):
        return self.__getStat('mouseUsagePercent')

    def getJoystickUsagePercent(self):
        return self.__getStat('joystickUsagePercent')

    def getZoomUsage(self):
        return self.__getStat('zoomUsage')

    def getSkipIntro(self):
        return self.__getStat('skipIntro')

    def getCommandsUsageStats(self, input):
        if input is None:
            return self.__commandsUsageStats
        else:
            self.__commandsUsageStats = [ {'key': id,
             'value': int(cmd.firedCount)} for id, cmd in input.commandProcessor.getCommandDescriptors().iteritems() if cmd.firedCount > 0 ]
            return self.__commandsUsageStats

    def startCollectClientStats(self):
        if self.__calculateStatsCallback is not None:
            return
        else:
            import CameraZoomStatsCollector
            CameraZoomStatsCollector.g_cameraZoomStatsCollector.resetStats()
            self.__calculateStats()
            self.__collectAndSendStats()
            return

    def stopCollectClientStats(self):
        if self.__calculateStatsCallback is not None:
            BigWorld.cancelCallback(self.__calculateStatsCallback)
            self.__calculateStatsCallback = None
        return

    def requestForData(self):
        self.__collectAndSendStats()

    def getLastInQueueWait(self):
        import BWPersonality
        return BWPersonality.g_lastTimeInQueue

    @noexcept
    def __collectAndSendStats(self):
        graphicsDetails = Settings.g_instance.graphicsDetails
        controllerProfileName = InputMapping.g_instance.getCurProfileName()
        width, height = self.getScreenDimensions()
        keyboardUsagePercent = -1
        mouseUsagePercent = -1
        joystickUsagePercent = -1
        zoomUsageStats = ''
        input = GameEnvironment.getInput()
        if input:
            keyboardUsagePercent = input.inputAxis.getControllersPercentageUsing()[0]
            mouseUsagePercent = input.inputAxis.getControllersPercentageUsing()[1]
            joystickUsagePercent = input.inputAxis.getControllersPercentageUsing()[2]
        import CameraZoomStatsCollector
        stats = CameraZoomStatsCollector.g_cameraZoomStatsCollector.getZoomStats()
        total = 0.0
        for key, value in stats.iteritems():
            total += float(value)

        if total > 1.0:
            for key, value in stats.iteritems():
                percentage = round(100.0 * (value / total))
                if percentage > 0:
                    zoomUsageStats += str(key) + ':' + str(percentage) + ';'

        self.setControllerProfileName(controllerProfileName)
        self.setGraphicsDetails(graphicsDetails)
        self.setKeyboardUsagePercent(keyboardUsagePercent)
        self.setMouseUsagePercent(mouseUsagePercent)
        self.seJoystickUsagePercent(joystickUsagePercent)
        self.setZoomUsage(zoomUsageStats)
        if self.__sendTime + STAT_MINIMAL_SEND_INTERVAL < time.time():
            LOG_DEBUG('zoomUsage = ', zoomUsageStats)
            stats = {'controllerProfileName': self.getControllerProfileName(),
             'graphicsDetails': self.getGraphicsDetails(),
             'minFPS': round(self.getMinFPS()),
             'medFPS': round(self.getMedFPS()),
             'fpsRanges': self.getFPSRanges(),
             'minPing': round(self.getMinPing()),
             'medPing': round(self.getMedPing()),
             'lostRatio': round(self.getMedLostRatio() * 10),
             'keyboardUsagePercent': self.getKeyboardUsagePercent(),
             'mouseUsagePercent': self.getMouseUsagePercent(),
             'joystickUsagePercent': self.getJoystickUsagePercent(),
             'zoomUsage': self.getZoomUsage(),
             'screenWidth': width,
             'screenHeight': height,
             'isFullScreen': Settings.g_instance.isFullScreen(),
             'inQueueWait': int(self.getLastInQueueWait()),
             'skipIntro': self.getSkipIntro()}
            player = BigWorld.player()
            player.cell.setClientStats(stats)
            self.__sendTime = time.time()

    def getScreenDimensions(self):
        resolution, index = Settings.g_instance.getVideoResolutions()
        dimensions = resolution[index].split('x')
        return (int(dimensions[0]), int(dimensions[1]))

    def __calculateStats(self):
        fps = BigWorld.getFPS()
        fpsMin = fps[2]
        fpsMed = fps[1]
        self.setFpsMin(fpsMin)
        self.setFpsMed(fpsMed)
        self.updateFPSRanges(fpsMed)
        ping = BigWorld.LatencyInfo().value[3] * 1000 - SERVER_TICK_LENGTH * 0.5 * 1000
        ping = max(1, ping)
        self.setPingMin(ping)
        self.setPingMed(ping)
        player = BigWorld.player()
        if player.movementFilter():
            self.setLostRatioMed(player.filter.dataLost)
        self.__calculateStatsCallback = BigWorld.callback(1.0, self.__calculateStats)