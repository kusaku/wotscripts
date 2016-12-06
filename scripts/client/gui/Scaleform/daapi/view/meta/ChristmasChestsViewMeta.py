# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ChristmasChestsViewMeta.py
from gui.Scaleform.framework.entities.View import View

class ChristmasChestsViewMeta(View):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends View
    """

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

    def as_showAwardRibbonS(self, showRibbon):
        if self._isDAAPIInited():
            return self.flashObject.as_showAwardRibbon(showRibbon)

    def as_setAwardDataS(self, awardData):
        """
        :param awardData: Represented by Vector.<AwardCarouselItemRendererVO> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setAwardData(awardData)

    def as_setBottomTextsS(self, chestsNum, openBtnLabel):
        if self._isDAAPIInited():
            return self.flashObject.as_setBottomTexts(chestsNum, openBtnLabel)

    def as_setControlsEnabledS(self, enabled):
        if self._isDAAPIInited():
            return self.flashObject.as_setControlsEnabled(enabled)