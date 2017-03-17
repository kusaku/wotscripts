# Embedded file name: scripts/client/TutorialClient/GunsOverheatedTrigger.py
from TutorialCommon.TriggerBase import TriggerBase

class GunsOverheatedTrigger(TriggerBase):

    def __init__(self, avatar, data, operation):
        TriggerBase.__init__(self, data, operation)
        self.__avatar = avatar
        self.__avatar.onGunOverheatedEvent += self.__onOverheated

    def __onOverheated(self):
        self._setState(True)

    def update(self, dt):
        pass

    def destroy(self):
        self.__avatar.onGunOverheatedEvent -= self.__onOverheated
        self.__avatar = None
        TriggerBase.destroy(self)
        return