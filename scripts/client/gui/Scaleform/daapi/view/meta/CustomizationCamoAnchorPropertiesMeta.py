# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/CustomizationCamoAnchorPropertiesMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.customization.anchor_properties import AnchorProperties

class CustomizationCamoAnchorPropertiesMeta(AnchorProperties):

    def setCamoColor(self, swatchID):
        self._printOverrideError('setCamoColor')

    def setCamoScale(self, scale, index):
        self._printOverrideError('setCamoScale')

    def as_setPopoverDataS(self, data):
        """
        :param data: Represented by CustomizationCamoAnchorVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setPopoverData(data)