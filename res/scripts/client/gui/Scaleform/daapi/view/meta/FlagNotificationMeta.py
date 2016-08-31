# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/FlagNotificationMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class FlagNotificationMeta(BaseDAAPIComponent):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseDAAPIComponent
    null
    """

    def as_setStateS(self, state):
        """
        :param state:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setState(state)

    def as_setActiveS(self, value):
        """
        :param value:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setActive(value)

    def as_setupS(self, states):
        """
        :param states:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setup(states)

    def as_hideS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_hide()

    def as_updateFieldsS(self, state, titleStr, body):
        """
        :param state:
        :param titleStr:
        :param body:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateFields(state, titleStr, body)