# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RepairPointTimerMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class RepairPointTimerMeta(BaseDAAPIComponent):
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

    def as_setTimeInSecondsS(self, seconds):
        """
        :param seconds:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setTimeInSeconds(seconds)

    def as_setTimeStringS(self, timeStr):
        """
        :param timeStr:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setTimeString(timeStr)

    def as_useActionScriptTimerS(self, isASTimer):
        """
        :param isASTimer:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_useActionScriptTimer(isASTimer)

    def as_hideS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_hide()