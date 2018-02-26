# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/NYChestsViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class NYChestsViewMeta(View):

    def onOpenBtnClick(self):
        self._printOverrideError('onOpenBtnClick')

    def onCloseWindow(self):
        self._printOverrideError('onCloseWindow')

    def onPlaySound(self, soundType):
        self._printOverrideError('onPlaySound')

    def as_setInitDataS(self, data):
        """
        :param data: Represented by NYChestsViewVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_setRewardDataS(self, awardData):
        """
        :param awardData: Represented by RibbonAwardsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setRewardData(awardData)

    def as_setOpenBtnLabelS(self, label):
        if self._isDAAPIInited():
            return self.flashObject.as_setOpenBtnLabel(label)

    def as_setOpenBtnEnabledS(self, enabled):
        if self._isDAAPIInited():
            return self.flashObject.as_setOpenBtnEnabled(enabled)

    def as_setControlsEnabledS(self, enabled):
        if self._isDAAPIInited():
            return self.flashObject.as_setControlsEnabled(enabled)

    def as_showRewardRibbonS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_showRewardRibbon()

    def as_hideRewardRibbonS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideRewardRibbon()