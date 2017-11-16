# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/EventBoardsBattleOverlayMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class EventBoardsBattleOverlayMeta(BaseDAAPIComponent):

    def as_setDataS(self, data):
        """
        :param data: Represented by EventBoardsBattleOverlayVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_setExperienceDataS(self, data):
        """
        :param data: Represented by BattleExperienceBlockVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setExperienceData(data)

    def as_setStatisticsDataS(self, data):
        """
        :param data: Represented by BattleStatisticsBlockVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setStatisticsData(data)

    def as_setTableHeaderDataS(self, data):
        """
        :param data: Represented by EventBoardTableHeaderVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setTableHeaderData(data)

    def as_setTableDataS(self, data):
        """
        :param data: Represented by EventBoardTableRendererContainerVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setTableData(data)