# Embedded file name: scripts/client/gui/HudElements/CollisionWarningSystem.py
import GUI
import BigWorld
import Math
from consts import WORLD_SCALING

class CollisionWarningSystem:
    MAX_OBSTACLE_TIME = 5.0
    CRITICAL_OBSTACLE_TIME = 0.5
    SIGN_SIZE = Math.Vector2(22.0, 8.0) * WORLD_SCALING

    def __init__(self, collisionWarningCallBack):
        self.__collisionMp = GUI.CollisionMp()
        self.__collisionMp.enabled = False
        self.__collisionMp.maxObstacleTime = CollisionWarningSystem.MAX_OBSTACLE_TIME
        self.__collisionMp.criticalObstacleTime = CollisionWarningSystem.CRITICAL_OBSTACLE_TIME
        self.__collisionMp.entityMP = BigWorld.player().realMatrix
        self.__collisionMp.signSize = CollisionWarningSystem.SIGN_SIZE
        currentMatrix = Math.Matrix(self.__collisionMp.entityMP)
        self.__collisionMp.lastParentPosition = currentMatrix.applyToOrigin()
        self.__collisionMp.py_callback = self.__isCollisionWarning
        self.__collisionWarningCallBack = collisionWarningCallBack

    def destroy(self):
        self.__collisionWarningCallBack = None
        self.__collisionMp.enabled = False
        self.__collisionMp.py_callback = None
        self.__collisionMp = None
        return

    def enabled(self, flag):
        if self.__collisionMp.enabled != flag:
            self.__collisionMp.enabled = flag

    def __isCollisionWarning(self, flag):
        if self.__collisionWarningCallBack is not None:
            self.__collisionWarningCallBack(flag)
        return