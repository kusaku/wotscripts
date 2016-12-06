# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ChristmasMainViewMeta.py
from gui.Scaleform.framework.entities.View import View

class ChristmasMainViewMeta(View):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends View
    """

    def installItem(self, itemId, slotId):
        self._printOverrideError('installItem')

    def moveItem(self, srcSlotId, targetSlotId):
        self._printOverrideError('moveItem')

    def uninstallItem(self, slotId):
        self._printOverrideError('uninstallItem')

    def showConversion(self):
        self._printOverrideError('showConversion')

    def switchOffNewItem(self, itemId):
        self._printOverrideError('switchOffNewItem')

    def applyRankFilter(self, filterId):
        self._printOverrideError('applyRankFilter')

    def applyTypeFilter(self, filterId):
        self._printOverrideError('applyTypeFilter')

    def onChangeTab(self, tabId):
        self._printOverrideError('onChangeTab')

    def onEmptyListBtnClick(self):
        self._printOverrideError('onEmptyListBtnClick')

    def closeWindow(self):
        self._printOverrideError('closeWindow')

    def showRules(self):
        self._printOverrideError('showRules')

    def switchCamera(self):
        self._printOverrideError('switchCamera')

    def convertItems(self):
        self._printOverrideError('convertItems')

    def cancelConversion(self):
        self._printOverrideError('cancelConversion')

    def onConversionAnimationComplete(self):
        self._printOverrideError('onConversionAnimationComplete')

    def as_setStaticDataS(self, data):
        """
        :param data: Represented by MainViewStaticDataVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setStaticData(data)

    def as_setFiltersS(self, ranks, types):
        """
        :param ranks: Represented by ChristmasFiltersVO (AS)
        :param types: Represented by ChristmasFiltersVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setFilters(ranks, types)

    def as_setProgressS(self, data):
        """
        :param data: Represented by ProgressBarVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setProgress(data)

    def as_selectSlotsTabS(self, index):
        if self._isDAAPIInited():
            return self.flashObject.as_selectSlotsTab(index)

    def as_showSlotsViewS(self, linkage):
        if self._isDAAPIInited():
            return self.flashObject.as_showSlotsView(linkage)

    def as_setSlotsDataS(self, data):
        """
        :param data: Represented by SlotsDataClassVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setSlotsData(data)

    def as_updateSlotS(self, data):
        """
        :param data: Represented by SlotVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateSlot(data)

    def as_scrollToItemS(self, index):
        if self._isDAAPIInited():
            return self.flashObject.as_scrollToItem(index)

    def as_getDecorationsDPS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getDecorationsDP()

    def as_setEmptyListDataS(self, visible, data):
        """
        :param data: Represented by InfoMessageVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setEmptyListData(visible, data)

    def as_updateConversionBtnS(self, enabled, icon):
        if self._isDAAPIInited():
            return self.flashObject.as_updateConversionBtn(enabled, icon)