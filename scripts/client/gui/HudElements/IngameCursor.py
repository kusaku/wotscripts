# Embedded file name: scripts/client/gui/HudElements/IngameCursor.py
import BigWorld
import GUI
from Math import Vector2
import db.DBLogic
from consts import *
from gui.HUDconsts import *
import gui.GUIHelper
from MathExt import clamp

class IngameCursor(object):
    CURSOR_ARROW_BLEND_PERSCENT = 0.9
    CURSOR_ARROW_BLEND_DISTANCE = 50.0

    def __init__(self, sourceMatrix):
        self.__cursorPoint = gui.GUIHelper.createImage(db.DBLogic.g_instance.getGUITexture('TX_INGAME_CURSOR'), vAnchor='CENTER', color=(255, 255, 255, 255))
        self.__cursorPoint.filterType = 'LINEAR'
        self.__cursorPointArrow = gui.GUIHelper.createImage(db.DBLogic.g_instance.getGUITexture('TX_INGAME_CURSOR_ARROW'), vAnchor='CENTER', color=(255, 255, 255, 255))
        self.__cursorPointArrow.filterType = 'LINEAR'
        self.__cursor = GUI.SmartArrow()
        self.__cursor.sourceMatrix = sourceMatrix
        self.__cursor.targetMatrix = None
        self.__cursor.addComponent('endPoint', self.__cursorPoint, 1.0, False)
        self.__cursor.addComponent('endPointArrow', self.__cursorPointArrow, 1.0, True)
        self.__cursor.sourceColor = START_CURSOUR_COLOR
        self.__cursor.targetColor = END_CURSOUR_COLOR
        self.__cursor.targetLineOffset = 14
        self.__cursor.distFadeType = 'SCREEN'
        self.__cursor.maxAlphaSize = 128.0
        self.__cursor.minAlphaSize = -32.0
        self.setState(0.0)
        GUI.addRoot(self.__cursor)
        self.__visible = False
        self.__enable = False
        self.__cursor.visible = False
        return

    def setState(self, value):
        alpha = (value - IngameCursor.CURSOR_ARROW_BLEND_PERSCENT) / (1.0 - IngameCursor.CURSOR_ARROW_BLEND_PERSCENT) * 255
        self.__cursorPointArrow.colour.w = clamp(0, alpha, 255)
        self.__cursorPoint.colour.w = 255 - clamp(0, alpha, 255)

    def setCursorPosition(self, value):
        self.__cursor.screenPosTarget = value

    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, isVisible):
        self.__visible = isVisible
        self.__cursor.visible = self.__visible and self.__enable

    @property
    def enable(self):
        return self.__enable

    @visible.setter
    def enable(self, isEnable):
        self.__enable = isEnable
        self.__cursor.visible = self.__visible and self.__enable

    def getVisible(self):
        return self.__cursor.visible

    def getCursorScreenPosition(self):
        """
        
        @rtype: Math.Vector2
        """
        return Vector2(self.__cursor.screenPosTarget.x, self.__cursor.screenPosTarget.y)

    def getCursorScreenPositionSource(self):
        return Vector2(self.__cursor.screenPosSource.x, self.__cursor.screenPosSource.y)

    def setCursorDefaultLength(self, value):
        self.__cursor.sourceMatrix.defaultLength = value