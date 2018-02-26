# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ReportBugPanelMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class ReportBugPanelMeta(BaseDAAPIComponent):

    def reportBug(self):
        self._printOverrideError('reportBug')

    def as_setHyperLinkS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setHyperLink(value)