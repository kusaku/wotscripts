# Embedded file name: scripts/client/TutorialClient/HealthTrigger.py
from TutorialCommon.TriggerBase import TriggerBase
import BigWorld
import GameEnvironment

class HealthTrigger(TriggerBase):

    def __init__(self, data, operation):
        TriggerBase.__init__(self, data, operation)
        self.__entityName = data.entityName
        self.__healthPercent = data.healthPercent

    def update(self, dt):
        if self._isConditionsComplete or self.__entityName == '':
            return
        else:
            ids = GameEnvironment.getClientArena().findIDsByPlayerName(self.__entityName)
            if len(ids) > 0:
                entity = BigWorld.entities.get(ids[0], None)
                if entity is not None and entity.health < self.__healthPercent * entity.maxHealth / 100.0:
                    self._setState(True)
            return