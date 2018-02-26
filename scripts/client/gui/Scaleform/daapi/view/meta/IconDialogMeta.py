# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/IconDialogMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.dialogs.SimpleDialog import SimpleDialog

class IconDialogMeta(SimpleDialog):

    def as_setIconS(self, path):
        if self._isDAAPIInited():
            return self.flashObject.as_setIcon(path)