# Embedded file name: scripts/client/gui/HudElements/LandingPlace.py
import BigWorld
import GUI
import db.DBLogic
import Math
from consts import *
from gui.HUDconsts import *
from clientConsts import BOMB_SIGN_DISABLED_MATERIAL

class LandingPlace:
    LANDING_POINT_VISUAL = 'objects/landing_point.visual'
    MAX_OBSTACLE_TIME = 5.0
    CRITICAL_OBSTACLE_TIME = 3.0
    HIDE_TIME = 0.2
    MAX_ALPHA = 0.5
    SIGN_SIZE = Math.Vector2(22.0, 8.0) * WORLD_SCALING

    def __init__(self):
        self.__inited = False
        self.__visible = False

    def __createTarget(self):
        self.__hud = GUI.LandingPlaceHud()
        self.__hud.signModelName = LandingPlace.LANDING_POINT_VISUAL
        self.__hud.maxObstacleTime = LandingPlace.MAX_OBSTACLE_TIME
        self.__hud.criticalObstacleTime = LandingPlace.CRITICAL_OBSTACLE_TIME
        self.__hud.hideTime = LandingPlace.HIDE_TIME
        self.__hud.maxAlpha = LandingPlace.MAX_ALPHA
        self.__hud.signSize = LandingPlace.SIGN_SIZE
        self.__hud.entityMP = BigWorld.player().realMatrix
        self.__hud.init()
        self.__signEnabled = True
        self.__inited = True
        self.__hud.visible = True
        GUI.addRoot(self.__hud)

    def destroy(self):
        self.setVisible(False)
        if self.__inited:
            GUI.delRoot(self.__hud)
            self.__hud.entityMP = None
        self.__inited = False
        self.__visible = False
        self.__hud = None
        self.__cachedTexture = None
        return

    def setBombTargetEnable(self, signEnabled):
        if self.__signEnabled != signEnabled:
            if signEnabled:
                self.__hud.disabled = False
            else:
                self.__hud.disabled = True
            self.__signEnabled = signEnabled

    def setVisible(self, visible):
        if visible != self.__visible:
            self.__visible = visible
            if visible and not self.__inited:
                self.__createTarget()
            if self.__inited:
                self.__hud.visible = visible

    def isVisible(self):
        return self.__visible