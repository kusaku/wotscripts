# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RibbonsPanelMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class RibbonsPanelMeta(BaseDAAPIComponent):

    def onShow(self):
        self._printOverrideError('onShow')

    def onChange(self):
        self._printOverrideError('onChange')

    def onHide(self, ribbonId):
        self._printOverrideError('onHide')

    def as_setupS(self, items, isExtendedAnim, isVisible, isWithRibbonName, isWithVehName):
        """
        :param items: Represented by Array (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setup(items, isExtendedAnim, isVisible, isWithRibbonName, isWithVehName)

    def as_resetS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_reset()

    def as_addBattleEfficiencyEventS(self, ribbonType, ribbonId, leftFieldStr, vehName, vehType, rightFieldStr):
        if self._isDAAPIInited():
            return self.flashObject.as_addBattleEfficiencyEvent(ribbonType, ribbonId, leftFieldStr, vehName, vehType, rightFieldStr)

    def as_updateBattleEfficiencyEventS(self, ribbonType, ribbonId, leftFieldStr, vehName, vehType, rightFieldStr):
        if self._isDAAPIInited():
            return self.flashObject.as_updateBattleEfficiencyEvent(ribbonType, ribbonId, leftFieldStr, vehName, vehType, rightFieldStr)

    def as_setSettingsS(self, isVisible, isExtendedAnim, isWithRibbonName, isWithVehName):
        if self._isDAAPIInited():
            return self.flashObject.as_setSettings(isVisible, isExtendedAnim, isWithRibbonName, isWithVehName)