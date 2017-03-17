# Embedded file name: scripts/client/TutorialClient/KeyInputTrigger.py
import Keys
import InputMapping
import MathExt
from TutorialCommon.TriggerBase import TriggerBase
from consts import AXIS_NAME_TO_INT_MAP
from debug_utils import LOG_DEBUG
import GlobalEvents
import GameEnvironment

class KeyInputTrigger(TriggerBase):
    """
    Trigger that checks player input
    @param avatar:
    @param data:
    @param operation:
    """

    def __init__(self, manager, avatar, data, operation):
        """
        @type manager: TutorialClient.TutorialManager.TutorialManager
        """
        TriggerBase.__init__(self, data, operation)
        self.__avatar = avatar
        GlobalEvents.onKeyEvent += self.__onKeyEvent
        self.__tutorialManager = manager
        input = GameEnvironment.getInput()
        if self.data.keyCommand and input is not None and input.commandProcessor is not None:
            for keyCommand in self.data.keyCommand:
                input.commandProcessor.getCommand(InputMapping.g_descriptions.getCommandIntID(keyCommand)).startEvent += self.__onCommandEvent

        return

    def destroy(self):
        """
        Destructor
        """
        input = GameEnvironment.getInput()
        if self.data.keyCommand and input is not None and input.commandProcessor is not None:
            for keyCommand in self.data.keyCommand:
                input.commandProcessor.getCommand(InputMapping.g_descriptions.getCommandIntID(keyCommand)).startEvent -= self.__onCommandEvent

        GlobalEvents.onKeyEvent -= self.__onKeyEvent
        self.__avatar = None
        TriggerBase.destroy(self)
        return

    def update(self, dt):
        pass

    def __onCommandEvent(self):
        if not self.__tutorialManager.tutorialUI.isTutorialPaused():
            self._setState(True)

    def __onKeyEvent(self, event):
        """
        @type event: UserKeyEvent
        """
        if self.__tutorialManager.tutorialUI.isTutorialPaused() or event.key == Keys.KEY_ESCAPE or not event.isKeyDown():
            return
        if not self.data.keyCommand and not self.data.keyCode or self.data.keyCode and event.key in self.data.keyCode:
            self._setState(True)