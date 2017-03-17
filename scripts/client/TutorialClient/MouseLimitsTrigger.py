# Embedded file name: scripts/client/TutorialClient/MouseLimitsTrigger.py
import GameEnvironment
from TutorialCommon.TriggerBase import TriggerBase
from debug_utils import LOG_DEBUG
import gui.hud

class MouseLimitsTrigger(TriggerBase):
    """
    Checks that mouse position is in the mouse limits on screen
    """

    def __init__(self, data, operation, ui):
        """
        
        @param data:
        @param operation:
        @type ui: gui.Scaleform.UI.UI
        @return:
        """
        TriggerBase.__init__(self, data, operation)
        self.__ui = ui
        self.__ui.onHitLimitAreaCircleEvent += self.__onHitArea
        self.__canRequest = True
        self.__isInAreaLast = False
        self.__isInArea = False
        self.__timer = 0

    def update(self, dt):
        if self.__canRequest:
            self.__canRequest = False
            position = GameEnvironment.getHUD().getCursorPosition()
            self.__ui.isHitLimitAreaCircle(position.x, position.y)
        if self.__isInArea:
            self.__timer += dt
            self._setState(self.__timer >= self.data.duration)
        else:
            if self.__isInAreaLast and self.data.failedOnMouseLeaveLimits:
                self._failed()
            self.__timer = 0
        self.__isInAreaLast = self.__isInArea

    def __onHitArea(self, isHit):
        self.__canRequest = True
        self.__isInArea = isHit

    def destroy(self):
        TriggerBase.destroy(self)
        self.__ui.onHitLimitAreaCircleEvent -= self.__onHitArea