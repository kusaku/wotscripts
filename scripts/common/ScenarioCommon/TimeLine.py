# Embedded file name: scripts/common/ScenarioCommon/TimeLine.py
from random import random
import math

class TimeLine(object):
    """general class for controlling actions in timeline"""
    IS_PAST_TIME = 2.0

    def __init__(self, environmentData, timeLineData, actionsTable):
        """
        environmentData: container for actions runtime data (objects for changing in actions)
        timeLineData: static timeline data from XML
        actionsTable: {key: actionNameStr, value: actionFunction(actionData, environmentData)}
        """
        self.__environmentData = environmentData
        self.__nextActionId = 0
        self.__timeLineData = timeLineData
        self.__actionsTable = actionsTable
        self.__startTimeOffset = -1.0
        self.__innerTimeOffset = 0.0
        if hasattr(timeLineData, 'duration') and timeLineData.duration > 0.0:
            self.__duration = timeLineData.duration
        else:
            self.__duration = timeLineData.action[-1].startTimeRange if hasattr(timeLineData.action[-1], 'startTimeRange') else timeLineData.action[-1].startTime
        self.__calculatedStartTime = -1.0
        self.__actionIDCalculatedTime = None
        return

    @property
    def timeLineData(self):
        return self.__timeLineData

    @property
    def startTimeOffset(self):
        return self.__startTimeOffset

    @startTimeOffset.setter
    def startTimeOffset(self, value):
        self.__startTimeOffset = value
        self.__innerTimeOffset = self.__startTimeOffset + random() * self.__timeLineData.startRandomTime
        self.__nextActionId = 0
        self.__calculatedStartTime = -1.0
        self.__actionIDCalculatedTime = None
        return

    def __startAction(self, actionId):
        actionData = self.__timeLineData.action[actionId]
        for key, actionList in actionData.__dict__.iteritems():
            if key in self.__actionsTable:
                for action in actionList:
                    self.__actionsTable[key](action, self.__environmentData)

    def __calculateNextActionTime(self):
        """
        get randomized time value instead action[ActionId].startTime
        value calculated once for current ActionId
        """
        if self.__actionIDCalculatedTime != self.__nextActionId:
            action = self.__timeLineData.action[self.__nextActionId]
            self.__calculatedStartTime = action.startTime + random() * (action.startTimeRange - action.startTime if hasattr(action, 'startTimeRange') else 0)
            self.__actionIDCalculatedTime = self.__nextActionId
        return self.__calculatedStartTime

    def startActionsForTime(self, time):
        """
        process actions for global time
        time: global time
        return: time until the next action, -1 If there are no actions in the future
        """
        nextActionTime = -1.0
        currentTime = time - self.__innerTimeOffset
        if currentTime < 0.0:
            return -currentTime
        while self.__nextActionId < len(self.__timeLineData.action) and self.__calculateNextActionTime() <= currentTime:
            isPast = currentTime - self.__calculatedStartTime > TimeLine.IS_PAST_TIME
            if self.__timeLineData.continuously or not isPast:
                self.__startAction(self.__nextActionId)
            self.__nextActionId += 1
            if self.__nextActionId == len(self.__timeLineData.action) and self.__timeLineData.isLoop:
                duration = math.floor(currentTime / self.__duration)
                duration = (self.__duration if duration <= 1.0 else duration * self.__duration) + random() * self.__timeLineData.loopRandomTime
                self.__innerTimeOffset += duration
                self.__nextActionId = self.__nextActionId % len(self.__timeLineData.action)
                if currentTime >= duration:
                    currentTime = currentTime % duration
                else:
                    currentTime = -(currentTime - duration)
                    break

        if self.__nextActionId < len(self.__timeLineData.action):
            nextActionTime = self.__calculateNextActionTime() - currentTime
        return nextActionTime