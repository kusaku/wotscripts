# Embedded file name: scripts/client/TutorialClient/UICaptionInputTrigger.py
from TutorialCommon.TriggerBase import TriggerBase
from gui.Scaleform.UI import TutorialCaptionParams

class UICaptionInputTrigger(TriggerBase):
    """
    Tutorial UI input trigger
    """

    def __init__(self, manager, data, operation):
        """
        @param manager: tutorial manager
        @type manager: TutorialClient.TutorialManager.TutorialManager
        @param data: trigger data
        @param operation: operation
        """
        TriggerBase.__init__(self, data, operation)
        self.__manager = manager

    def update(self, dt):
        pass

    def __onBtnPressed(self):
        self.__manager.tutorialUI.clearScreen()
        self._setState(True)

    def initialize(self):
        """
        Initializes trigger
        """
        TriggerBase.initialize(self)
        params = TutorialCaptionParams()
        params.message = self.data.message
        params.title = self.data.title
        params.isBonus = self.data.isBonus
        if hasattr(self.data, 'nameReward'):
            params.nameReward = self.data.nameReward
        if hasattr(self.data, 'countCredits'):
            params.countCredits = self.data.countCredits
        if hasattr(self.data, 'nameCredits'):
            params.nameCredits = self.data.nameCredits
        if hasattr(self.data, 'countExperience'):
            params.countExperience = self.data.countExperience
        if hasattr(self.data, 'nameExperience'):
            params.nameExperience = self.data.nameExperience
        if hasattr(self.data, 'isActionBtn'):
            params.isAction1 = self.data.isActionBtn
        if hasattr(self.data, 'actionBtnText'):
            params.nameAction1 = self.data.actionBtnText
        self.__manager.tutorialUI.showCaption(params, params.isAction1 and self.__onBtnPressed or None)
        return