# Embedded file name: scripts/client/ScenarioClient/TeamObjectScenarioController.py
from ScenarioCommon.ScenarioControllerBase import ScenarioControllerSlave
from TimeLineUpdateStrategy import TimelineUpdateStrategyClient
from ClientScenarioActions import ACTION_TABLE

class TeamObjectScenarioEnvironment:

    def __init__(self, destructableObject):
        self.destructableObject = destructableObject


class TeamObjectScenarioController(ScenarioControllerSlave):
    """scenario logic for team objects on client"""

    def __init__(self, destructableObject, scenarioData):
        ScenarioControllerSlave.__init__(self, scenarioData, TeamObjectScenarioEnvironment(destructableObject), ACTION_TABLE, TimelineUpdateStrategyClient())
        ScenarioControllerSlave.refreshTimelines(self, destructableObject.timelinesTime)