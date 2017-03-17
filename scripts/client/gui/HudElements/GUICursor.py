# Embedded file name: scripts/client/gui/HudElements/GUICursor.py
import GUI
from consts import GUICursorStates

class GUICursor(object):
    SHAPES = {GUICursorStates.NORMAL_ON: 'arrow',
     GUICursorStates.NORMAL_OFF: 'arrow',
     GUICursorStates.ENEMY: 'arrow',
     GUICursorStates.FRIENDLY: 'arrow'}

    def __init__(self, state):
        self.__state = state

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, newState):
        self.__state = newState
        self.__updateShape()

    @property
    def switchStyle(self):
        return self.__switchStyle

    @switchStyle.setter
    def switchStyle(self, newSwitchStyle):
        self.__switchStyle = newSwitchStyle

    def __updateShape(self):
        if self.__state in self.SHAPES and GUI.mcursor().shape != self.SHAPES[self.__state]:
            GUI.mcursor().shape = self.SHAPES[self.__state]