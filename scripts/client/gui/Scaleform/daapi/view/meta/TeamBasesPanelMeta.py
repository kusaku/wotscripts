# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/TeamBasesPanelMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class TeamBasesPanelMeta(BaseDAAPIComponent):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseDAAPIComponent
    null
    """

    def as_addS(self, barId, sortWeight, colorType, title, points, captureTime, vehiclesCount):
        """
        :param barId:
        :param sortWeight:
        :param colorType:
        :param title:
        :param points:
        :param captureTime:
        :param vehiclesCount:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_add(barId, sortWeight, colorType, title, points, captureTime, vehiclesCount)

    def as_removeS(self, id):
        """
        :param id:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_remove(id)

    def as_stopCaptureS(self, id, points):
        """
        :param id:
        :param points:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_stopCapture(id, points)

    def as_updateCaptureDataS(self, id, points, rate, captureTime, vehiclesCount):
        """
        :param id:
        :param points:
        :param rate:
        :param captureTime:
        :param vehiclesCount:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateCaptureData(id, points, rate, captureTime, vehiclesCount)

    def as_setCapturedS(self, id, title):
        """
        :param id:
        :param title:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setCaptured(id, title)

    def as_setOffsetForEnemyPointsS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setOffsetForEnemyPoints()

    def as_clearS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_clear()