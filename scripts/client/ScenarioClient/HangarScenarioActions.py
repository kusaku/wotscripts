# Embedded file name: scripts/client/ScenarioClient/HangarScenarioActions.py
__author__ = 'm_antipov'
import BigWorld
import EffectManager
from db.DBEffects import Effects
import Math
import math
from debug_utils import LOG_ERROR, LOG_DEBUG
from functools import partial
from clientConsts import BULLET_PARAM, TEAMOBJECT_SIMPLIFICATION_DISTANCE, TEAMOBJECT_SIMPLIFICATION_FILTER, TURRET_TRACKER_AXIS
from consts import UPDATABLE_TYPE
import db.DBLogic
from random import random, uniform
import GameEnvironment
from EntityHelpers import isClientReadyToPlay
import gui.Scaleform.utils.HangarSpace
from WWISE_ import SoundObject
from CameraStates import CameraState

class Dummy:
    pass


class HangarScenarioActions:
    """
    Class stores client actions logic for scenarios
    """
    delayedActions = []
    sounds = {}

    def __init__(self):
        self.__sounds = {}

    def stopActions(self):
        for soundName in self.__sounds:
            HangarScenarioActions.sounds[soundName].destroy()
            HangarScenarioActions.sounds[soundName] = None
            HangarScenarioActions.sounds = {}

        return

    def refreshDelayedActions(self):
        LOG_DEBUG('HangarScenarioActions::refreshDelayedActions', len(HangarScenarioActions.delayedActions))
        for fn, args, kw in HangarScenarioActions.delayedActions:
            fn(*args, **kw)

        HangarScenarioActions.delayedActions = []

    @staticmethod
    def soundEvent(actionData, environmentData):
        so = HangarScenarioActions.sounds.get(actionData.name, None)
        if so is None:
            so = SoundObject(actionData.name, 0, 0)
            HangarScenarioActions.sounds[actionData.name] = so
        so.postEvent(actionData.event)
        return

    @staticmethod
    def cinematic(actionData, environmentData):
        from gui.Scaleform.utils.HangarSpace import g_hangarSpace
        if g_hangarSpace.space is not None:
            camera = g_hangarSpace.space.hangarCamera
            if camera.getState() == CameraState.SpectatorSide:
                camera.getStateObject().updateParams(actionData)
            else:
                camera.setState(CameraState.SpectatorSide, actionData)
        return

    def destroy(self):
        self.stopActions()


HANGAR_SCENARIO_ACTION_TABLE = {'cinematic': HangarScenarioActions.cinematic,
 'soundEvent': HangarScenarioActions.soundEvent}