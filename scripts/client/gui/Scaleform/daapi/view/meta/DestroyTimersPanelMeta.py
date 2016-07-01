# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/DestroyTimersPanelMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class DestroyTimersPanelMeta(BaseDAAPIComponent):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseDAAPIComponent
    null
    """

    def as_showS(self, timerTypeID, timerViewTypeID):
        """
        :param timerTypeID:
        :param timerViewTypeID:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_show(timerTypeID, timerViewTypeID)

    def as_hideS(self, timerTypeID):
        """
        :param timerTypeID:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_hide(timerTypeID)

    def as_setTimeInSecondsS(self, timerTypeID, totalSeconds, currentTime):
        """
        :param timerTypeID:
        :param totalSeconds:
        :param currentTime:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setTimeInSeconds(timerTypeID, totalSeconds, currentTime)

    def as_setTimeSnapshotS(self, timerTypeID, totalSeconds, timeLeft):
        """
        :param timerTypeID:
        :param totalSeconds:
        :param timeLeft:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setTimeSnapshot(timerTypeID, totalSeconds, timeLeft)

    def as_setSpeedS(self, speed):
        """
        :param speed:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setSpeed(speed)