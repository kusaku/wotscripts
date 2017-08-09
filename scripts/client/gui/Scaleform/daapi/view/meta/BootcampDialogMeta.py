# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BootcampDialogMeta.py
from gui.Scaleform.daapi.view.dialogs.SimpleDialog import SimpleDialog

class BootcampDialogMeta(SimpleDialog):

    def as_setDataS(self, path, label, showAward, awardText):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(path, label, showAward, awardText)