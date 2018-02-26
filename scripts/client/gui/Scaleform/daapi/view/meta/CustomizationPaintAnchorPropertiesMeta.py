# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/CustomizationPaintAnchorPropertiesMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.customization.anchor_properties import AnchorProperties

class CustomizationPaintAnchorPropertiesMeta(AnchorProperties):

    def as_setPopoverDataS(self, data):
        """
        :param data: Represented by CustomizationPaintAnchorVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setPopoverData(data)