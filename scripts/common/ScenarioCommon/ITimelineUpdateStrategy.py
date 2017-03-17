# Embedded file name: scripts/common/ScenarioCommon/ITimelineUpdateStrategy.py
from exceptions import NotImplementedError

class ITimelineUpdateStrategy(object):

    def activateTimeLine(self, timeline, nextUpdateTime):
        raise NotImplementedError('Should have implemented this')

    def deactivateTimeLine(self, timeline):
        raise NotImplementedError('Should have implemented this')

    def destroy(self):
        raise NotImplementedError('Should have implemented this')

    def time(self):
        raise NotImplementedError('Should have implemented this')