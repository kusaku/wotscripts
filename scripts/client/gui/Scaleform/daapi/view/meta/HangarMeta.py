# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/HangarMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class HangarMeta(View):

    def onEscape(self):
        self._printOverrideError('onEscape')

    def showHelpLayout(self):
        self._printOverrideError('showHelpLayout')

    def closeHelpLayout(self):
        self._printOverrideError('closeHelpLayout')

    def as_setCrewEnabledS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setCrewEnabled(value)

    def as_setCarouselEnabledS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setCarouselEnabled(value)

    def as_setupAmmunitionPanelS(self, maintenanceEnabled, maintenanceTooltip, customizationEnabled, customizationTooltip):
        if self._isDAAPIInited():
            return self.flashObject.as_setupAmmunitionPanel(maintenanceEnabled, maintenanceTooltip, customizationEnabled, customizationTooltip)

    def as_setControlsVisibleS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setControlsVisible(value)

    def as_setVisibleS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setVisible(value)

    def as_showHelpLayoutS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_showHelpLayout()

    def as_closeHelpLayoutS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_closeHelpLayout()

    def as_showMiniClientInfoS(self, description, hyperlink):
        if self._isDAAPIInited():
            return self.flashObject.as_showMiniClientInfo(description, hyperlink)

    def as_show3DSceneTooltipS(self, id, args):
        """
        :param args: Represented by Array (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_show3DSceneTooltip(id, args)

    def as_hide3DSceneTooltipS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hide3DSceneTooltip()

    def as_setCarouselS(self, linkage, alias):
        if self._isDAAPIInited():
            return self.flashObject.as_setCarousel(linkage, alias)

    def as_setDefaultHeaderS(self, isDefault):
        if self._isDAAPIInited():
            return self.flashObject.as_setDefaultHeader(isDefault)

    def as_setAlertMessageBlockVisibleS(self, isVisible):
        if self._isDAAPIInited():
            return self.flashObject.as_setAlertMessageBlockVisible(isVisible)

    def as_initNYS(self, isEnabled, isAvailable, counter):
        if self._isDAAPIInited():
            return self.flashObject.as_initNY(isEnabled, isAvailable, counter)

    def as_updateNYBoxCounterS(self, counter):
        if self._isDAAPIInited():
            return self.flashObject.as_updateNYBoxCounter(counter)

    def as_updateNYEnabledS(self, isEnabled):
        if self._isDAAPIInited():
            return self.flashObject.as_updateNYEnabled(isEnabled)

    def as_updateNYAvailableS(self, isAvailable):
        if self._isDAAPIInited():
            return self.flashObject.as_updateNYAvailable(isAvailable)