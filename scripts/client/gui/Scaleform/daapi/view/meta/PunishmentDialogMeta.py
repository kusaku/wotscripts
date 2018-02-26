# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/PunishmentDialogMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.dialogs.SimpleDialog import SimpleDialog

class PunishmentDialogMeta(SimpleDialog):

    def as_setMsgTitleS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setMsgTitle(value)