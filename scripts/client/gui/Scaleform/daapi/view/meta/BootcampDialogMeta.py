# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BootcampDialogMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.dialogs.SimpleDialog import SimpleDialog

class BootcampDialogMeta(SimpleDialog):

    def as_setDataS(self, path, label, showAward, awardText):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(path, label, showAward, awardText)