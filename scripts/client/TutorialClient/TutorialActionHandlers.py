# Embedded file name: scripts/client/TutorialClient/TutorialActionHandlers.py
import GameEnvironment
import Keys
import BigWorld
from Helpers.i18n import localizeTutorial
import InputMapping
import Math
from MathExt import clamp
from TutorialClient.TutorialUIWrapper import TutorialUIWrapper, MouseLimitArea
from TutorialCommon.TutorialManagerBase import TutorialManagerBase
from TutorialObjects import TutorialObjects
from consts import AXIS_NAME_TO_INT_MAP, INPUT_SYSTEM_STATE, TutorialHintsInputEnum, WORLD_SCALING
import consts
from debug_utils import LOG_ERROR, LOG_DEBUG
from gui.Scaleform.UI import TutorialCaptionParams
from _performanceCharacteristics_db import airplanes
import math
import copy
from clientConsts import INPUT_SYSTEM_PROFILES
import gui.hud
import db.DBLogic
from gui.Scaleform.utils.MeasurementSystem import MeasurementSystem

class RaceHandler:

    def __init__(self, splineName, caption, radius, ui):
        self.__radius = radius
        self.__splineData = db.DBLogic.g_instance.getSpline(splineName).getBasePoints()
        self.__step = 1.0 / (len(self.__splineData) - 1)
        self.__splineIndex = 1
        self.__ui = ui
        self.__ratio = 0
        self.__caption = localizeTutorial(caption)

    def update(self):
        pos = BigWorld.player().position
        if pos.distSqrTo(self.__splineData[self.__splineIndex]) < self.__radius * self.__radius:
            if self.__splineIndex < len(self.__splineData) - 1:
                self.__splineIndex += 1
        passedK = self.__splineIndex - 1
        targetPoint = self.__splineData[self.__splineIndex]
        prevPoint = self.__splineData[self.__splineIndex - 1]
        curDist = math.sqrt((targetPoint.x - pos.x) * (targetPoint.x - pos.x) + (targetPoint.z - pos.z) * (targetPoint.z - pos.z))
        fullDist = math.sqrt((targetPoint.x - prevPoint.x) * (targetPoint.x - prevPoint.x) + (targetPoint.z - prevPoint.z) * (targetPoint.z - prevPoint.z))
        curK = (fullDist - curDist) / (fullDist - self.__radius)
        curK = clamp(0.0, curK, 1.0)
        ratio = (passedK + curK) * self.__step * 100.0
        if self.__ratio < ratio:
            self.__ratio = ratio
            self.__ui.setProgressBarValue(self.__ratio, self.__caption)

    def onDestroy(self):
        self.__ui = None
        return


class SpeedController:

    def __init__(self, entity):
        self.__entity = entity
        self.__criticalSpeed = 0.6 * airplanes[self.__entity.globalID].maxSpeed / 3.6
        self.__forbid = False

    def update(self):
        speed = self.__entity.getSpeed()
        if speed < self.__criticalSpeed and not self.__forbid:
            GameEnvironment.getInput().commandProcessor.setFilter([InputMapping.CMD_ENGINE_OFF], False)
            if 'tutorialManager' in self.__entity.controllers and GameEnvironment.getInput().isFired(InputMapping.CMD_ENGINE_OFF):
                self.__entity.controllers['tutorialManager'].tutorialUI.ui.showLowSpeedWarning(True)
            self.__forbid = True
        elif speed > 1.1 * self.__criticalSpeed and self.__forbid:
            GameEnvironment.getInput().commandProcessor.setFilter(None, False)
            if 'tutorialManager' in self.__entity.controllers:
                self.__entity.controllers['tutorialManager'].tutorialUI.ui.showLowSpeedWarning(False)
            self.__forbid = False
        return

    def onDestroy(self):
        self.__entity = None
        if self.__forbid:
            GameEnvironment.getInput().commandProcessor.setFilter(None, False)
            self.__forbid = False
        return


class MarkerHandler:

    def __init__(self, ui):
        self.__ui = ui
        self.__markerVisible = False
        self.__arrowVisible = False

    def showTutorialMarkerPointer(self, value):
        if self.__markerVisible == value:
            return
        self.__markerVisible = value
        self.__ui.showTutorialMarkerPointer(value)

    def showTutorialArrowPointer(self, value):
        if self.__arrowVisible == value:
            return
        self.__arrowVisible = value
        self.__ui.showTutorialArrowPointer(value)

    def update(self, markerPos, showMarker, showArrow, showDistance):
        if markerPos is None:
            self.showTutorialMarkerPointer(False)
            self.showTutorialArrowPointer(False)
            return (False, False)
        else:
            vec = markerPos
            ms = MeasurementSystem()
            distance = ms.getMeters((vec - BigWorld.player().position).length / WORLD_SCALING)
            distStr = ms.localizeHUD('ui_meter')
            screenPointPos = BigWorld.worldToScreen(vec)
            screenPointMarker = BigWorld.worldToScreen(vec)
            self.__ui.showTutorialMarkerPointerMinimap(vec.x, vec.z)
            halfWidth = BigWorld.screenWidth() / 2
            halfHeight = BigWorld.screenHeight() / 2
            screenPointPos -= Math.Vector3(halfWidth, halfHeight, 0)
            screenPointMarker -= Math.Vector3(halfWidth, halfHeight, 0)
            screenDist = math.sqrt(screenPointMarker.x * screenPointMarker.x + screenPointMarker.y * screenPointMarker.y)
            if screenPointMarker.z >= 0 and abs(screenPointMarker.x) < halfWidth and abs(screenPointMarker.y) < halfHeight and showMarker:
                if not self.__markerVisible:
                    self.showTutorialMarkerPointer(True)
                self.__ui.setTutorialMarkerPointer(screenPointMarker.x, screenPointMarker.y, '%.0f%s' % (distance, distStr) if showDistance else '')
            else:
                if self.__markerVisible:
                    self.showTutorialMarkerPointer(False)
                if screenPointMarker.z >= 0:
                    self.__ui.setTutorialMarkerPointer(screenPointMarker.x, screenPointMarker.y, '')
                else:
                    self.__ui.setTutorialMarkerPointer(10000, 10000, '')
            screenDist = math.sqrt(screenPointPos.x * screenPointPos.x + screenPointPos.y * screenPointPos.y)
            if (screenDist >= 0.5 * halfHeight or screenPointPos.z < 0) and showArrow:
                angle = 0
                if screenPointPos.z >= 0:
                    angle = math.degrees(math.atan2(screenPointPos.y, screenPointPos.x))
                else:
                    angle = math.degrees(math.atan2(-screenPointPos.y, -screenPointPos.x))
                if not self.__arrowVisible:
                    self.showTutorialArrowPointer(True)
                self.__ui.setTutorialArrowPointer(angle, '%.0f%s' % (distance, distStr) if showDistance else '')
            elif self.__arrowVisible:
                self.showTutorialArrowPointer(False)
            return (self.__markerVisible, self.__arrowVisible)

    def onDestroy(self):
        if self.__arrowVisible:
            self.__ui.showTutorialArrowPointer(False)
            self.__arrowVisible = False
        if self.__markerVisible:
            self.__ui.showTutorialMarkerPointer(False)
            self.__markerVisible = False
        self.__ui = None
        return


class CountdownHandler:

    def __init__(self, time, ui):
        self.__time = time
        self.__ui = ui
        self.__timeBegin = BigWorld.time()
        self.__timePrev = BigWorld.time()

    def update(self):
        if self.__time < 0:
            return True
        if int(self.__timePrev - self.__timeBegin) != int(BigWorld.time() - self.__timeBegin):
            self.__timePrev = BigWorld.time()
            self.__time -= 1
            if self.__time >= 0:
                self.__ui.updateBigTime(self.__time)
        return False

    def onDestroy(self):
        self.__ui.hideBigTime()
        self.__ui = None
        return


class VOHighlightedElemTP2:

    def __init__(self, enable = True):
        self.targetPoint2 = enable


class FPHighlightHandler:

    def __init__(self, ui):
        self._ui = ui
        self._enabled = False

    def update(self, val):
        screenPoint = GameEnvironment.getHUD().getForestallingPointScreenPos()
        enable = True
        if screenPoint is None or not val:
            enable = False
        if enable != self._enabled:
            self._enabled = enable
            self._ui.showTutorialHighlightControls(VOHighlightedElemTP2(enable), 'red')
        if self._enabled:
            pass
        return

    def onDestroy(self):
        if self._enabled:
            self._ui.showTutorialHighlightControls(VOHighlightedElemTP2(False), '')
        self._ui = None
        return