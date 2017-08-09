# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/SettingsWindowMeta.py
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class SettingsWindowMeta(AbstractWindowView):

    def applySettings(self, settings, isCloseWnd):
        self._printOverrideError('applySettings')

    def autodetectQuality(self):
        self._printOverrideError('autodetectQuality')

    def startVOIPTest(self, isVoiceTestStarted):
        self._printOverrideError('startVOIPTest')

    def updateCaptureDevices(self):
        self._printOverrideError('updateCaptureDevices')

    def onSettingsChange(self, controlID, controlVal):
        self._printOverrideError('onSettingsChange')

    def altVoicesPreview(self):
        self._printOverrideError('altVoicesPreview')

    def altBulbPreview(self, sampleID):
        self._printOverrideError('altBulbPreview')

    def isSoundModeValid(self):
        self._printOverrideError('isSoundModeValid')

    def showWarningDialog(self, dialogID, settings, isCloseWnd):
        self._printOverrideError('showWarningDialog')

    def onTabSelected(self, tabId):
        self._printOverrideError('onTabSelected')

    def onCounterTargetVisited(self, viewId, subViewId, controlId):
        self._printOverrideError('onCounterTargetVisited')

    def autodetectAcousticType(self):
        self._printOverrideError('autodetectAcousticType')

    def canSelectAcousticType(self, index):
        self._printOverrideError('canSelectAcousticType')

    def as_setDataS(self, settingsData):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(settingsData)

    def as_setCaptureDevicesS(self, captureDeviceIdx, devicesData):
        """
        :param devicesData: Represented by DataProvider (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setCaptureDevices(captureDeviceIdx, devicesData)

    def as_onVibroManagerConnectS(self, isConnect):
        if self._isDAAPIInited():
            return self.flashObject.as_onVibroManagerConnect(isConnect)

    def as_updateVideoSettingsS(self, videoSettings):
        if self._isDAAPIInited():
            return self.flashObject.as_updateVideoSettings(videoSettings)

    def as_confirmWarningDialogS(self, isOk, dialogID):
        if self._isDAAPIInited():
            return self.flashObject.as_confirmWarningDialog(isOk, dialogID)

    def as_ConfirmationOfApplicationS(self, isApplied):
        if self._isDAAPIInited():
            return self.flashObject.as_ConfirmationOfApplication(isApplied)

    def as_openTabS(self, tabIndex):
        if self._isDAAPIInited():
            return self.flashObject.as_openTab(tabIndex)

    def as_setGraphicsPresetS(self, presetNum):
        if self._isDAAPIInited():
            return self.flashObject.as_setGraphicsPreset(presetNum)

    def as_isPresetAppliedS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_isPresetApplied()

    def as_setCountersDataS(self, countersData):
        """
        :param countersData: Represented by Vector.<SettingsNewCountersVo> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setCountersData(countersData)

    def as_onSoundSpeakersPresetApplyS(self, isApply):
        if self._isDAAPIInited():
            return self.flashObject.as_onSoundSpeakersPresetApply(isApply)