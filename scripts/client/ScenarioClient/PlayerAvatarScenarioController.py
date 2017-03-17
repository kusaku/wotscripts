# Embedded file name: scripts/client/ScenarioClient/PlayerAvatarScenarioController.py
from ScenarioCommon.ScenarioControllerBase import ScenarioControllerMaster
from TimeLineUpdateStrategy import TimelineUpdateStrategyClient
from AvatarControllerBase import AvatarControllerBase
from ClientScenarioActions import PLAYER_CAMERA_ACTION_TABLE

class PlayerAvatarScenarioController(ScenarioControllerMaster, AvatarControllerBase):
    """scenario logic for player avatar on client"""

    def __init__(self, owner, scenarioData):
        AvatarControllerBase.__init__(self, owner)
        ScenarioControllerMaster.__init__(self, scenarioData, None, PLAYER_CAMERA_ACTION_TABLE, TimelineUpdateStrategyClient())
        return

    def destroy(self):
        ScenarioControllerMaster.destroy(self)
        AvatarControllerBase.destroy(self)

    def onEvent(self, eventName, eventTime):
        self._updateStrategy.destroy()
        ScenarioControllerMaster.onEvent(self, eventName, eventTime)