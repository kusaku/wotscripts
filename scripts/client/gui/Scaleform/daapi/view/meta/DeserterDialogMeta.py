# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/DeserterDialogMeta.py
from gui.Scaleform.daapi.view.dialogs.SimpleDialog import SimpleDialog

class DeserterDialogMeta(SimpleDialog):

    def as_setDataS(self, path, messageYOffset):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(path, messageYOffset)