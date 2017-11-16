# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/PersonalMissionsPageMeta.py
from gui.Scaleform.framework.entities.View import View

class PersonalMissionsPageMeta(View):

    def onBarClick(self, vehIdx, operationIdx):
        self._printOverrideError('onBarClick')

    def onSkipTaskClick(self):
        self._printOverrideError('onSkipTaskClick')

    def onBackBtnClick(self):
        self._printOverrideError('onBackBtnClick')

    def closeView(self):
        self._printOverrideError('closeView')

    def onTutorialAcceptBtnClicked(self):
        self._printOverrideError('onTutorialAcceptBtnClicked')

    def as_setHeaderDataS(self, data):
        """
        :param data: Represented by OperationsHeaderVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setHeaderData(data)

    def as_updateBranchesDataS(self, data):
        """
        :param data: Represented by ChainsPanelVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateBranchesData(data)

    def as_setStatusDataS(self, data):
        """
        :param data: Represented by StatusFooterVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setStatusData(data)

    def as_setSelectedBranchIndexS(self, index):
        if self._isDAAPIInited():
            return self.flashObject.as_setSelectedBranchIndex(index)

    def as_showFirstAwardSheetObtainedPopupS(self, useAnim):
        if self._isDAAPIInited():
            return self.flashObject.as_showFirstAwardSheetObtainedPopup(useAnim)

    def as_showFourAwardSheetsObtainedPopupS(self, useAnim, data):
        if self._isDAAPIInited():
            return self.flashObject.as_showFourAwardSheetsObtainedPopup(useAnim, data)

    def as_hideAwardSheetObtainedPopupS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideAwardSheetObtainedPopup()

    def as_showAwardsPopoverForTutorS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_showAwardsPopoverForTutor()