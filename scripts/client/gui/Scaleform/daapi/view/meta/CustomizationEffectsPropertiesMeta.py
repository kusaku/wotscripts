# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/CustomizationEffectsPropertiesMeta.py
from gui.Scaleform.daapi.view.lobby.customization.anchor_properties import AnchorProperties

class CustomizationEffectsPropertiesMeta(AnchorProperties):

    def as_setPopoverDataS(self, data):
        """
        :param data: Represented by CustomizationEffectsSlotVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setPopoverData(data)