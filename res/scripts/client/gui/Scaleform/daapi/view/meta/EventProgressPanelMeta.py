# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/EventProgressPanelMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class EventProgressPanelMeta(BaseDAAPIComponent):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseDAAPIComponent
    null
    """

    def as_initS(self, isAllyMark1, progress, currentHealth, maxHealth, state, vehName, isColorBlind):
        """
        :param isAllyMark1:
        :param progress:
        :param currentHealth:
        :param maxHealth:
        :param state:
        :param vehName:
        :param isColorBlind:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_init(isAllyMark1, progress, currentHealth, maxHealth, state, vehName, isColorBlind)

    def as_updateHealthS(self, health):
        """
        :param health:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateHealth(health)

    def as_updateProgressS(self, progress):
        """
        :param progress:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateProgress(progress)

    def as_updateStateS(self, state):
        """
        :param state:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateState(state)

    def as_updateSettingsS(self, isColorBlind):
        """
        :param isColorBlind:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateSettings(isColorBlind)