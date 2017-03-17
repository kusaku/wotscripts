# Embedded file name: scripts/client/gui/HudElements/ForestallingPoint.py
import BigWorld
import GUI
import db.DBLogic
from consts import *
from gui.HUDconsts import *
import gui.GUIHelper
from EntityHelpers import isAvatar, isTeamObject
from clientConsts import FP_VISIBILITY_DISTANCE, FP_EFFECTIVE_FIRING_DISTANCE_K, FP_SMALL_CIRCLE_K, FP_EFFECTIVE_FIRING_DISTANCE_TO_AIM
from debug_utils import LOG_DEBUG
import sys
import Event
import Settings

class FP_STATES:
    VECTOR = 3
    SMALL_CIRCLE = 2
    BIG_CIRCLE = 1
    AIM = 0


FP_STATES_SCALE_SIZE = {FP_STATES.SMALL_CIRCLE: dict(min=15.0, max=29.0)}

class ForestallingPoint:
    POINT_FADE_DISTANCE_RANGE = 100.0 * WORLD_SCALING
    POINT_FADE_RADIUS_MIN = 0.0 * WORLD_SCALING
    POINT_FADE_RADIUS_MAX = 0.0 * WORLD_SCALING
    LINE_START_COLOR = 0
    LINE_END_COLOR = 1711276032
    LINE_ACTIVE_STATE_TIME = 2.0

    def __init__(self, state, offsetMtx):
        self.__lineComponent = None
        self.__subState = FP_STATES.VECTOR
        self.__offsetMtx = offsetMtx
        self.__inited = False
        self.__visible = False
        self.__matrixProvider = None
        self.eChangeDistState = Event.Event()
        return

    @property
    def matrixProvider(self):
        return self.__matrixProvider

    def setTarget(self, entity):
        if not self.__inited:
            self.__createTarget()
        self.__lineComponent.clearDistanceState()
        if entity is not None and isAvatar(entity):
            self.__matrixProvider.target = entity.matrix
            self.__deflectionTarget(entity)
            self.__offsetMtx.target = self.__matrixProvider
            if COLLISION_RECORDER:
                self.__matrixProvider.targetEntity = entity
        else:
            self.__matrixProvider.target = None
            self.__deflectionTarget(None)
            if entity is not None and TEAM_OBJECT_PARALLAX_ENABLED and isTeamObject(entity):
                self.__offsetMtx.target = entity.matrix
            else:
                self.__offsetMtx.target = None
            if COLLISION_RECORDER:
                self.__matrixProvider.targetEntity = None
        self.__lineComponent.sourceMatrix = self.__matrixProvider.target
        self.__pCallbackDist(FP_STATES.VECTOR)
        return

    def __deflectionTarget(self, entity):
        BigWorld.player().deflectionTargetsInProgress += 1
        BigWorld.player().cell.setDeflectionTarget(entity.id if entity is not None else 0)
        return

    def __createTarget(self):
        self.__matrixProvider = GUI.ForestallingMp()
        self.__matrixProvider.source = BigWorld.player().realMatrix
        self.__matrixProvider.target = None
        self.__matrixProvider.offset = self.__offsetMtx
        if COLLISION_RECORDER:
            self.__matrixProvider.sourceEntity = BigWorld.player()
            self.__matrixProvider.targetEntity = None
        self.__inited = True
        self.__lineComponent = GUI.SmartArrow()
        self.__lineComponent.targetMatrix = self.__matrixProvider
        self.__lineComponent.minAlphaSize = ForestallingPoint.POINT_FADE_RADIUS_MIN
        self.__lineComponent.maxAlphaSize = ForestallingPoint.POINT_FADE_RADIUS_MAX
        self.__lineComponent.sourceColor = ForestallingPoint.LINE_START_COLOR
        self.__lineComponent.targetColor = ForestallingPoint.LINE_END_COLOR
        self.__lineComponent.activeStateTime = ForestallingPoint.LINE_ACTIVE_STATE_TIME
        return

    def addScaleformComponent(self, pMovie, mcRoot, mcScale):
        self.__setScaleStatesScaleformComponent()
        self.__lineComponent.addScaleformComponent(pMovie, mcRoot, mcScale)

    def setBulletRange(self, bulletRange, bulletRangeDps, planeLevel, targetMatrixDefaultLength, cursorMatrix):
        if not self.__inited:
            self.__createTarget()
        self.__lineComponent.ownerMatrix = BigWorld.player().realMatrix
        self.__lineComponent.cursorMatrix = cursorMatrix
        self.__lineComponent.targetMatrixDefaultLength = targetMatrixDefaultLength
        self.__lineComponent.minAlphaDistance = bulletRange
        self.__lineComponent.maxAlphaDistance = bulletRange
        distStates = list()
        distStates.insert(FP_STATES.AIM, sys.float_info.min)
        distStates.insert(FP_STATES.BIG_CIRCLE, bulletRangeDps * FP_EFFECTIVE_FIRING_DISTANCE_K)
        distStates.insert(FP_STATES.SMALL_CIRCLE, bulletRange * FP_SMALL_CIRCLE_K)
        distStates.insert(FP_STATES.VECTOR, FP_VISIBILITY_DISTANCE.get(planeLevel) * WORLD_SCALING)
        self.__lineComponent.setDistanceStates(tuple(distStates))
        self.__lineComponent.pCallbackDist = self.__pCallbackDist
        self.__lineComponent.effectiveDistanceToAim = FP_EFFECTIVE_FIRING_DISTANCE_TO_AIM

    def __pCallbackDist(self, subState):
        lastState = self.__subState
        self.__subState = subState
        self.__updateVisibility()
        if not Settings.g_instance.isBestTimeFP and subState == FP_STATES.AIM:
            return
        if not Settings.g_instance.isSizeFP and subState == FP_STATES.SMALL_CIRCLE:
            subState = FP_STATES.BIG_CIRCLE
        self.eChangeDistState(lastState, subState)

    @property
    def state(self):
        return self.__subState

    def setBulletSpeed(self, bulletSpeed):
        if not self.__inited:
            self.__createTarget()
        self.__matrixProvider.bulletSpeed = bulletSpeed

    def destroy(self):
        self.setVisible(False)
        if self.__lineComponent is not None:
            self.__lineComponent.pCallbackDist = None
            self.__lineComponent.removeAll()
            self.__lineComponent = None
        self.__inited = False
        self.__visible = False
        self.__matrixProvider = None
        self.__offsetMtx.target = None
        self.__offsetMtx = None
        self.eChangeDistState.clear()
        return

    @staticmethod
    def getPreloadedResources():
        return list()

    def __setScaleStatesScaleformComponent(self):
        if Settings.g_instance.isSizeFP:
            self.__lineComponent.setScaleStatesScaleformComponent([ [scaleState, 100.0 * (scaleStateData['min'] / scaleStateData['max'])] for scaleState, scaleStateData in FP_STATES_SCALE_SIZE.iteritems() ])
        else:
            self.__lineComponent.setScaleStatesScaleformComponent([])

    def __updateVisibility(self):
        if not self.__inited:
            self.__createTarget()
        if self.isVisible():
            GUI.addRoot(self.__lineComponent)
        else:
            GUI.delRoot(self.__lineComponent)
        self.__setScaleStatesScaleformComponent()
        visible = self.isVisible() and self.__matrixProvider is not None and self.__matrixProvider.target is not None and not (not Settings.g_instance.isToBoundaryFP and self.__subState == FP_STATES.VECTOR)
        self.__lineComponent.visible = visible
        self.__lineComponent.activateScaleformComponent(visible)
        return

    def setVisible(self, visible):
        if visible != self.__visible:
            self.__visible = visible
            self.__updateVisibility()

    def getFadeDistance(self):
        return self.__lineComponent.maxAlphaDistance

    def isVisible(self):
        return bool(self.__visible and self.__matrixProvider.target)

    def disableUpdate(self, value):
        if self.__matrixProvider is not None:
            self.__matrixProvider.updateDisabled = value
        return