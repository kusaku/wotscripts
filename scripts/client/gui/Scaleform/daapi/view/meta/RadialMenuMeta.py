# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RadialMenuMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class RadialMenuMeta(BaseDAAPIComponent):

    def onSelect(self):
        self._printOverrideError('onSelect')

    def onAction(self, action):
        self._printOverrideError('onAction')

    def as_buildDataS(self, data):
        """
        :param data: Represented by Array (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_buildData(data)

    def as_showS(self, radialState, offset, ratio):
        """
        :param offset: Represented by Array (AS)
        :param ratio: Represented by Array (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_show(radialState, offset, ratio)

    def as_hideS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hide()