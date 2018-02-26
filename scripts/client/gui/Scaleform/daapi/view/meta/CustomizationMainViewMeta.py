# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/CustomizationMainViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class CustomizationMainViewMeta(View):

    def showBuyWindow(self):
        self._printOverrideError('showBuyWindow')

    def closeWindow(self):
        self._printOverrideError('closeWindow')

    def installCustomizationElement(self, itemIntCD, areaId, slotId, regionId, season):
        self._printOverrideError('installCustomizationElement')

    def switchToCustom(self):
        self._printOverrideError('switchToCustom')

    def switchToStyle(self):
        self._printOverrideError('switchToStyle')

    def showGroupFromTab(self, groupId):
        self._printOverrideError('showGroupFromTab')

    def fadeOutAnchors(self, value):
        self._printOverrideError('fadeOutAnchors')

    def getPropertySheetData(self, itemID):
        self._printOverrideError('getPropertySheetData')

    def clearFilter(self):
        self._printOverrideError('clearFilter')

    def refreshFilterData(self):
        self._printOverrideError('refreshFilterData')

    def clearCustomizationItem(self, areaId, slotId, regionId, season):
        self._printOverrideError('clearCustomizationItem')

    def changeSeason(self, season):
        self._printOverrideError('changeSeason')

    def itemContextMenuDisplayed(self):
        self._printOverrideError('itemContextMenuDisplayed')

    def onPropertySheetLoaded(self):
        self._printOverrideError('onPropertySheetLoaded')

    def getHistoricalPopoverData(self):
        self._printOverrideError('getHistoricalPopoverData')

    def updatePropertySheetButtons(self, areOaId, slotId, regionId):
        self._printOverrideError('updatePropertySheetButtons')

    def onLobbyClick(self):
        self._printOverrideError('onLobbyClick')

    def setEnableMultiselectRegions(self, value):
        self._printOverrideError('setEnableMultiselectRegions')

    def onSelectItem(self, index):
        self._printOverrideError('onSelectItem')

    def resetFilter(self):
        self._printOverrideError('resetFilter')

    def onChangeSize(self):
        self._printOverrideError('onChangeSize')

    def onSelectAnchor(self, areaID, regionID):
        self._printOverrideError('onSelectAnchor')

    def onPickItem(self):
        self._printOverrideError('onPickItem')

    def onReleaseItem(self):
        self._printOverrideError('onReleaseItem')

    def onSelectHotFilter(self, index, value):
        self._printOverrideError('onSelectHotFilter')

    def as_showBuyingPanelS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_showBuyingPanel()

    def as_hideBuyingPanelS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideBuyingPanel()

    def as_setHeaderDataS(self, data):
        """
        :param data: Represented by CustomizationHeaderVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setHeaderData(data)

    def as_setSeasonPanelDataS(self, data):
        """
        :param data: Represented by CustomizationSeasonPanelVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setSeasonPanelData(data)

    def as_setAnchorPositionsS(self, data):
        """
        :param data: Represented by CustomizationAnchorsSetVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setAnchorPositions(data)

    def as_setAnchorInitS(self, data):
        """
        :param data: Represented by CustomizationAnchorInitVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setAnchorInit(data)

    def as_updateAnchorDataS(self, data):
        """
        :param data: Represented by CustomizationAnchorInitVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateAnchorData(data)

    def as_setCarouselDataS(self, data):
        """
        :param data: Represented by CustomizationCarouselDataVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setCarouselData(data)

    def as_setCarouselFiltersInitDataS(self, data):
        """
        :param data: Represented by TankCarouselFilterInitVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setCarouselFiltersInitData(data)

    def as_setCarouselFiltersDataS(self, data):
        """
        :param data: Represented by TankCarouselFilterSelectedVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setCarouselFiltersData(data)

    def as_setFilterDataS(self, data):
        """
        :param data: Represented by CustomizationCarouselFilterVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setFilterData(data)

    def as_setBottomPanelHeaderS(self, data):
        """
        :param data: Represented by BottomPanelVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setBottomPanelHeader(data)

    def as_setBottomPanelInitDataS(self, data):
        """
        :param data: Represented by CustomizationBottomPanelInitVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setBottomPanelInitData(data)

    def as_setBottomPanelTabsDataS(self, data):
        """
        :param data: Represented by CustomizationTabNavigatorVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setBottomPanelTabsData(data)

    def as_getDataProviderS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getDataProvider()

    def as_onRegionHighlightedS(self, slotId):
        """
        :param slotId: Represented by CustomizationSlotIdVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_onRegionHighlighted(slotId)

    def as_refreshAnchorPropertySheetS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_refreshAnchorPropertySheet()

    def as_hideAnchorPropertySheetS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideAnchorPropertySheet()

    def as_updateHistoricStatusS(self, data):
        """
        :param data: Represented by HistoricIndicatorVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateHistoricStatus(data)

    def as_updateSelectedRegionsS(self, slotId):
        """
        :param slotId: Represented by CustomizationSlotIdVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateSelectedRegions(slotId)