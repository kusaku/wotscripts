# Embedded file name: scripts/client/gui/Scaleform/managers/battle_input.py
import Keys
from avatar_helpers.aim_global_binding import CTRL_MODE_NAME
from gui.battle_control import avatar_getter
from gui.battle_control import event_dispatcher

class BattleGameInputMgr(object):
    __slots__ = ('__consumers',)

    def __init__(self):
        super(BattleGameInputMgr, self).__init__()
        self.__consumers = []

    def start(self):
        pass

    def stop(self):
        self.__consumers = []

    def enterGuiControlMode(self, consumerID, cursorVisible = True):
        if consumerID not in self.__consumers:
            if not self.__consumers:
                avatar_getter.setForcedGuiControlMode(True, cursorVisible=cursorVisible)
            self.__consumers.append(consumerID)

    def leaveGuiControlMode(self, consumerID):
        if consumerID in self.__consumers:
            self.__consumers.remove(consumerID)
            if not self.__consumers:
                avatar_getter.setForcedGuiControlMode(False)

    def handleKey(self, isDown, key, mods):
        if key == Keys.KEY_ESCAPE and isDown:
            handler = avatar_getter.getInputHandler()
            if handler is not None and handler.ctrlModeName != CTRL_MODE_NAME.MAP_CASE:
                event_dispatcher.showIngameMenu()
                event_dispatcher.toggleFullStats(False)
            return True
        elif key in (Keys.KEY_LCONTROL, Keys.KEY_RCONTROL):
            if not self.__consumers:
                avatar_getter.setForcedGuiControlMode(isDown)
            return True
        elif key == Keys.KEY_TAB and (mods != Keys.MODIFIER_CTRL or not isDown):
            event_dispatcher.toggleFullStats(isDown)
            return True
        elif key == Keys.KEY_TAB and mods == Keys.MODIFIER_CTRL and isDown:
            if not self.__consumers:
                event_dispatcher.setNextPlayerPanelMode()
            return True
        else:
            return False