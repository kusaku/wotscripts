# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/EventNotificationPanelMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class EventNotificationPanelMeta(BaseDAAPIComponent):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseDAAPIComponent
    null
    """

    def onHideAnimationComplete(self, state):
        """
        :param state:
        :return :
        """
        self._printOverrideError('onHideAnimationComplete')

    def as_initS(self, states):
        """
        :param states:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_init(states)

    def as_showS(self, state):
        """
        :param state:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_show(state)

    def as_hideS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_hide()