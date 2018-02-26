# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/NYMissionRewardScreenMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class NYMissionRewardScreenMeta(View):

    def onOpenBtnClick(self):
        self._printOverrideError('onOpenBtnClick')

    def onCloseWindow(self):
        self._printOverrideError('onCloseWindow')

    def onPlaySound(self, soundType):
        self._printOverrideError('onPlaySound')

    def onToyObtained(self, level):
        self._printOverrideError('onToyObtained')

    def as_setInitDataS(self, data):
        """
        :param data: Represented by NYMissionRewardScreenVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_setRewardDataS(self, awardData):
        """
        :param awardData: Represented by RibbonAwardsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setRewardData(awardData)

    def as_setVehicleDataS(self, data):
        """
        :param data: Represented by NYVehicleRewardVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setVehicleData(data)

    def as_startAnimationS(self, boxAnimSource):
        if self._isDAAPIInited():
            return self.flashObject.as_startAnimation(boxAnimSource)

    def as_restartAnimationS(self, boxAnimSource):
        if self._isDAAPIInited():
            return self.flashObject.as_restartAnimation(boxAnimSource)

    def as_setOpenBtnLabelS(self, label):
        if self._isDAAPIInited():
            return self.flashObject.as_setOpenBtnLabel(label)

    def as_setOpenBtnEnabledS(self, enabled):
        if self._isDAAPIInited():
            return self.flashObject.as_setOpenBtnEnabled(enabled)

    def as_setCloseBtnEnabledS(self, enabled):
        if self._isDAAPIInited():
            return self.flashObject.as_setCloseBtnEnabled(enabled)