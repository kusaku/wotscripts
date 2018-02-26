# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/NYMissionRewardScreen.py
from gui.Scaleform.framework.entities.View import View

class NYMissionRewardScreen(View):

    def onOpenBtnClick(self):
        self._printOverrideError('onOpenBtnClick')

    def onCloseWindow(self):
        self._printOverrideError('onCloseWindow')

    def onPlaySound(self, soundType):
        self._printOverrideError('onPlaySound')

    def as_setInitDataS(self, data):
        """
        :param data: Represented by ChestsViewVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_setOpenBtnEnabledS(self, enabled):
        if self._isDAAPIInited():
            return self.flashObject.as_setOpenBtnEnabled(enabled)

    def as_showRewardRibbonS(self, showRibbon):
        if self._isDAAPIInited():
            return self.flashObject.as_showRewardRibbon(showRibbon)

    def as_setRewardDataS(self, awardData):
        """
        :param awardData: Represented by Vector.<RewardCarouselItemRendererVO> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setRewardData(awardData)

    def as_setBottomTextsS(self, chestsNum, openBtnLabel):
        if self._isDAAPIInited():
            return self.flashObject.as_setBottomTexts(chestsNum, openBtnLabel)

    def as_setControlsEnabledS(self, enabled):
        if self._isDAAPIInited():
            return self.flashObject.as_setControlsEnabled(enabled)