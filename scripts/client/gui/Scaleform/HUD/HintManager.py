# Embedded file name: scripts/client/gui/Scaleform/HUD/HintManager.py
__author__ = 's_karchavets'
import db.DBLogic
import BigWorld
import math
from EntityHelpers import isAvatar
from Helpers.i18n import localizeTutorial
import time
import Math
from consts import WORLD_SCALING
from gui.HUDconsts import DIST_FOR_SELECT_TARGETS
from clientConsts import POS_OFFSET_Y

def checkPointInSquare(x, y, w, h, x0, y0):
    if not w or not h:
        return False
    return x <= x0 <= x + w and y <= y0 <= y + h


def checkPointInCircle(x, y, x0, y0, R):
    return (x - x0) * (x - x0) + (y - y0) * (y - y0) <= R * R


class HINT_COLORS:
    GREEN = 1
    RED = 2
    YELLOW = 3


class VOHint:

    def __init__(self, timeForShow, text, color = HINT_COLORS.YELLOW):
        self.timeForShow = timeForShow
        self.text = text
        self.color = color


class BaseHint:
    _hudInfo = None

    def __init__(self, data, aimMtx, fpMtx, markerOwner):
        self._data = data
        self._hitTime = -1.0
        self._hitEntityHP = 0.0
        self._hitEntityID = -1
        self._markerOwner = markerOwner
        self._aimMtx, self._fpMtx = aimMtx, fpMtx
        self._owner = BigWorld.player()
        self._entity = None
        self._entityTarget = None
        self._FPdistState = -1
        self._minDist = data.mindist
        self._maxDist = data.maxdist
        self._countForUse = data.countForUse
        self._delayTime = data.delayTime + data.timeForShow
        self._time = 0.0
        self._isFinished = False
        self._isPaused = False
        return

    def _clearHitTime(self):
        self._hitEntityHP = 0.0
        self._hitTime = -1.0
        self._hitEntityID = -1

    def _initHitTime(self):
        if self._hitTime == -1.0:
            self._hitEntityHP = self._entityTarget.health
            self._hitTime = BigWorld.time()
            self._hitEntityID = self._entityTarget.id

    def _chekHitTime(self):
        result = False
        if BigWorld.time() - self._hitTime >= self._data.hitTime:
            target = BigWorld.entities.get(self._hitEntityID, None)
            if target is not None and not target.isDestroyed:
                result = not (self._hitEntityHP > target.health and self._owner.id == target.lastDamagerID)
            self._clearHitTime()
        return result

    def _checkDist(self, dist):
        if not dist:
            return False
        res = True
        if self._minDist:
            res = dist >= self._minDist
        if self._maxDist:
            res = res and dist <= self._maxDist
        return res

    @property
    def delayTime(self):
        return self._delayTime

    def update(self):
        if self._isFinished:
            return False
        self._checkDelay()
        if self._isPaused:
            return False
        return True

    def destroy(self):
        self._owner = None
        self._entity = None
        self._data = None
        self._markerOwner = None
        return

    def _checkCountUse(self):
        if self._countForUse != -1:
            if self._countForUse > 0:
                self._countForUse -= 1
            if self._countForUse == 0:
                self._isFinished = True

    def _initDelay(self):
        if not self._isFinished and self._delayTime:
            if not self._time:
                self._isPaused = True
                self._time = time.time()

    def _checkDelay(self):
        if not self._isFinished and self._time:
            if time.time() - self._time > self._delayTime:
                self._isPaused = False
                self._time = 0.0

    def _checkFPStateOutside(self):
        return self._FPdistState == -1 or self._FPdistState > self._data.distStateFP

    def onEntityChangeLastDamagerID(self, entity):
        pass

    def onChangeDistState(self, state):
        self._FPdistState = state

    def onSetTargetEntity(self, entity):
        self._entityTarget = entity

    @staticmethod
    def initialData(hudInfo):
        """
        @param hudInfo: dict
        """
        BaseHint._hudInfo = hudInfo.copy()

    def show(self):
        self._checkCountUse()
        self._initDelay()


class AltitudeHint(BaseHint):

    def update(self):
        if not BaseHint.update(self):
            return False
        elif BaseHint._hudInfo is None:
            return False
        isStallWarningVisible = BaseHint._hudInfo['stallSpeed'] > self._owner.getSpeed() > 0.0
        if isStallWarningVisible and self._owner.altitudeAboveObstacle > self._data.altitude:
            return True
        else:
            return False


class DamadgeAllyHint(BaseHint):

    def update(self):
        if not BaseHint.update(self):
            return False
        else:
            if self._owner.selectedGuns > 0 and self._entity is not None and not self._entity.isDestroyed and not self._owner.isDestroyed and self._entity.teamIndex == self._owner.teamIndex:
                if isAvatar(self._entity) and self._entity.lastDamagerID == self._owner.id:
                    return True
            return False

    def onEntityChangeLastDamagerID(self, entity):
        self._entity = entity


class CloserTargetHint(BaseHint):

    def update(self):
        if not BaseHint.update(self):
            return False
        else:
            if self._owner.selectedGuns > 0:
                if self._aimMtx is None:
                    return False
                if self._entityTarget is not None and isAvatar(self._entityTarget):
                    if self._checkFPStateOutside():
                        screenArea = self._entityTarget.getScreenArea()
                        if screenArea is not None:
                            tarScreenPos = BigWorld.worldToScreen(self._entityTarget.position)
                            w, h = screenArea
                            w *= self._data.areaK
                            h *= self._data.areaK
                            x, y = tarScreenPos.x - w / 2.0, tarScreenPos.y - h / 2.0
                            aimScreen = Math.Matrix(self._aimMtx)
                            aimScrrenPos = BigWorld.worldToScreen(aimScreen.translation)
                            return checkPointInSquare(x, y, w, h, aimScrrenPos.x, aimScrrenPos.y)
            return False


class TeamObjectHitHint(BaseHint):

    def update(self):
        if not BaseHint.update(self):
            return False
        elif self._hitTime != -1.0:
            return self._chekHitTime()
        else:
            if self._owner.selectedGuns > 0:
                if self._aimMtx is None or self._markerOwner is None:
                    return False
                if self._entityTarget is not None and not isAvatar(self._entityTarget):
                    distToTarget = (self._owner.position - self._entityTarget.position).length
                    if not self._checkDist(distToTarget / WORLD_SCALING):
                        return False
                    markerRect = self._markerOwner.getRectangle(self._entityTarget.id)
                    if markerRect is not None:
                        x, y, w, h = markerRect
                        aimScreen = Math.Matrix(self._aimMtx)
                        aimScreenPos = BigWorld.worldToScreen(aimScreen.translation)
                        x -= w / 2
                        y = y - h - POS_OFFSET_Y
                        if checkPointInSquare(x, y, w, h, aimScreenPos.x, aimScreenPos.y):
                            self._initHitTime()
            return False


class AvatarHitHint(BaseHint):

    def update(self):
        if not BaseHint.update(self):
            return False
        elif self._owner.isPvPUnlocked:
            return False
        elif self._hitTime != -1.0:
            return self._chekHitTime()
        elif self._checkFPStateOutside() or self._fpMtx is None or self._aimMtx is None:
            return False
        else:
            if self._owner.selectedGuns > 0:
                if self._entityTarget is not None and isAvatar(self._entityTarget):
                    screenArea = self._entityTarget.getScreenArea()
                    if screenArea is None:
                        return False
                    tarScreenPos = BigWorld.worldToScreen(self._entityTarget.position)
                    w, h = screenArea
                    x, y = tarScreenPos.x - w / 2.0, tarScreenPos.y - h / 2.0
                    aimScreen = Math.Matrix(self._aimMtx)
                    aimScrrenPos = BigWorld.worldToScreen(aimScreen.translation)
                    if checkPointInSquare(x, y, w, h, aimScrrenPos.x, aimScrrenPos.y):
                        fpScrren = Math.Matrix(self._fpMtx)
                        fpScrrenPos = BigWorld.worldToScreen(fpScrren.translation)
                        if not checkPointInSquare(x, y, w, h, fpScrrenPos.x, fpScrrenPos.y):
                            self._initHitTime()
            return False


_ALLOWED_HINTS_CLS = (CloserTargetHint,
 DamadgeAllyHint,
 AltitudeHint,
 TeamObjectHitHint,
 AvatarHitHint)
_UPDATE_TIME = 0.02
_INITIAL_TIME = 5.0

class HintManager:

    def __init__(self):
        self.__updateCallback = None
        self.__hints = dict()
        self.__uiOwner = None
        return

    def initialized(self, markerOwner, uiOwner, aimMtx, fpMtx):
        self.__uiOwner = uiOwner
        for hintCls in _ALLOWED_HINTS_CLS:
            hintData = db.DBLogic.g_instance.getHudHint(hintCls.__name__)
            if hintData is not None and hintData.enabled:
                self.__hints[hintCls.__name__] = hintCls(hintData, aimMtx, fpMtx, markerOwner)

        return

    def start(self):
        if self.__hints:
            self.__updateCallback = BigWorld.callback(_INITIAL_TIME, self.__update)

    def initialData(self, hudInfo):
        BaseHint.initialData(hudInfo)

    def onSetTargetEntity(self, entity):
        for hint in self.__hints.itervalues():
            hint.onSetTargetEntity(entity)

    def onEntityChangeLastDamagerID(self, entity):
        for hint in self.__hints.itervalues():
            hint.onEntityChangeLastDamagerID(entity)

    def onChangeDistState(self, state):
        for hint in self.__hints.itervalues():
            hint.onChangeDistState(state)

    def destroy(self):
        self.__uiOwner = None
        if self.__updateCallback is not None:
            BigWorld.cancelCallback(self.__updateCallback)
            self.__updateCallback = None
        for hint in self.__hints.itervalues():
            hint.destroy()

        self.__hints.clear()
        return

    def showCustomHint(self, timeForShow, text, color):
        self.__uiOwner.call_1('hud.hint', VOHint(timeForShow, text, color))

    def __update(self):
        hintReady = [ hintID for hintID, hint in self.__hints.iteritems() if hint.update() ]
        if hintReady:
            priority = 1000
            hintIDWithMaxPriority = -1
            for hintID in hintReady:
                hintData = db.DBLogic.g_instance.getHudHint(hintID)
                if hintData.priority < priority:
                    hintIDWithMaxPriority = hintID
                    priority = hintData.priority

            if hintIDWithMaxPriority != -1:
                hintData = db.DBLogic.g_instance.getHudHint(hintIDWithMaxPriority)
                self.__uiOwner.call_1('hud.hint', VOHint(hintData.timeForShow, localizeTutorial(hintData.textID)))
                self.__hints[hintIDWithMaxPriority].show()
                self.__updateCallback = BigWorld.callback(self.__hints[hintIDWithMaxPriority].delayTime, self.__update)
                return
        self.__updateCallback = BigWorld.callback(_UPDATE_TIME, self.__update)