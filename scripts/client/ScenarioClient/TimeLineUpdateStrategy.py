# Embedded file name: scripts/client/ScenarioClient/TimeLineUpdateStrategy.py
import BigWorld
from ScenarioCommon.ITimelineUpdateStrategy import ITimelineUpdateStrategy
import GameEnvironment
from functools import partial

class TimelineUpdateStrategyClient(ITimelineUpdateStrategy):
    """
    class for controlling timeLines update on client side. Uses BigWorld.callback for this
    """

    def __init__(self):
        self.__callbacks = {}

    def destroy(self):
        map(BigWorld.cancelCallback, self.__callbacks.values())
        self.__callbacks.clear()

    def time(self):
        return BigWorld.serverTime()

    def __onTimeLineCallback(self, timeLine):
        if timeLine.startTimeOffset >= 0.0:
            nextTime = timeLine.startActionsForTime(self.time())
            if nextTime > -1.0:
                self.__addCallback(timeLine, nextTime)
            else:
                del self.__callbacks[timeLine]

    def __addCallback(self, timeLine, time):
        self.__callbacks[timeLine] = BigWorld.callback(time, partial(self.__onTimeLineCallback, timeLine))

    def activateTimeLine(self, timeLine, nextTime):
        self.__addCallback(timeLine, nextTime)

    def deactivateTimeLine(self, timeLine):
        if timeLine in self.__callbacks:
            BigWorld.cancelCallback(self.__callbacks[timeLine])
            del self.__callbacks[timeLine]