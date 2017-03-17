# Embedded file name: scripts/common/ScenarioCommon/ScenarioControllerBase.py
from TimeLine import TimeLine
from functools import partial

class ScenarioControllerBase(object):
    """base class for scenario logic"""

    def __init__(self, scenarioData, environmentData, actionTable, updateStrategy):
        self._timeLines = [ TimeLine(environmentData, timeLineData, actionTable) for timeLineData in scenarioData.timeline ]
        self._updateStrategy = updateStrategy

    def _activateTimeLine(self, activateTime, timeLineId):
        timeLine = self._timeLines[timeLineId]
        timeLine.startTimeOffset = activateTime
        nextTime = timeLine.startActionsForTime(self._updateStrategy.time())
        self._updateStrategy.activateTimeLine(timeLine, nextTime)
        return timeLine

    def _deactivateTimeLine(self, timeLineId):
        timeLine = self._timeLines[timeLineId]
        timeLine.startTimeOffset = -1.0
        self._updateStrategy.deactivateTimeLine(timeLine)
        return timeLine

    def destroy(self):
        self._updateStrategy.destroy()
        self._timeLines = None
        self._updateStrategy = None
        return


class ScenarioControllerMaster(ScenarioControllerBase):
    """Master scenario controller - to handle the gameplay event and manage timeline lifetime"""

    def __init__(self, scenarioData, environmentData, actionTable, updateStrategy):
        ScenarioControllerBase.__init__(self, scenarioData, environmentData, actionTable, updateStrategy)
        self.__startEventListeners = {}
        self.__stopEventListeners = {}
        for id in range(0, len(self._timeLines)):
            timeLineData = self._timeLines[id].timeLineData
            if timeLineData.startEvent != '':
                for eventName in timeLineData.startEvent.split(','):
                    self.__startEventListeners.setdefault(eventName.strip(), []).append(id)

            if timeLineData.stopEvent != '':
                for eventName in timeLineData.stopEvent.split(','):
                    self.__stopEventListeners.setdefault(eventName.strip(), []).append(id)

    def onPartDestroyed(self, partID):
        pass

    def onEvent(self, eventName, eventTime):
        if eventName in self.__startEventListeners:
            map(partial(self._activateTimeLine, eventTime), self.__startEventListeners[eventName])
        if eventName in self.__stopEventListeners:
            map(self._deactivateTimeLine, self.__stopEventListeners[eventName])

    def destroy(self):
        self.__startEventListeners.clear()
        self.__stopEventListeners.clear()
        ScenarioControllerBase.destroy(self)


class ScenarioControllerSlave(ScenarioControllerBase):
    r"""Slave scenario controller - only handle timelines activation\ deactivation from Master controller"""

    def refreshTimelines(self, timelinesTime):
        """
        timelinesTimes : [startTimeOffset,...] . startTimeOffset: time from timeline activation or -1 if timeline is not active
        """
        raise len(timelinesTime) == len(self._timeLines) or AssertionError('timelinesMap and self._timeLines have different sizes')
        for id in range(0, len(self._timeLines)):
            if self._timeLines[id].startTimeOffset != timelinesTime[id]:
                if self._timeLines[id].startTimeOffset > -1:
                    self._deactivateTimeLine(id)
                if timelinesTime[id] > -1:
                    self._activateTimeLine(timelinesTime[id], id)