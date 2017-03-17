# Embedded file name: scripts/client/ScenarioClient/HangarScenarioController.py
__author__ = 'm_antipov'
from ScenarioCommon.ScenarioControllerBase import ScenarioControllerMaster
from TimeLineUpdateStrategy import TimelineUpdateStrategyClient
from HangarScenarioActions import HangarScenarioActions, HANGAR_SCENARIO_ACTION_TABLE
from debug_utils import LOG_DEBUG
from CameraStates import CameraState

class HangarScenarioController(HangarScenarioActions, ScenarioControllerMaster):
    """scenario logic for player avatar on client"""

    def __init__(self, scenarioData):
        HangarScenarioActions.__init__(self)
        ScenarioControllerMaster.__init__(self, scenarioData, None, HANGAR_SCENARIO_ACTION_TABLE, TimelineUpdateStrategyClient())
        return

    def onEvent(self, eventName, eventTime):
        self._updateStrategy.destroy()
        ScenarioControllerMaster.onEvent(self, eventName, eventTime)

    def forceStop(self):
        from gui.Scaleform.utils.HangarSpace import g_hangarSpace
        if g_hangarSpace.space is not None:
            camera = g_hangarSpace.space.hangarCamera
            camera.leaveState(CameraState.SpectatorSide)
        self._updateStrategy.destroy()
        return

    def destroy(self):
        ScenarioControllerMaster.destroy(self)
        HangarScenarioActions.destroy(self)