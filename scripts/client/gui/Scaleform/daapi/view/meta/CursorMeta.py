# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/CursorMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class CursorMeta(View):

    def as_setCursorS(self, cursor):
        if self._isDAAPIInited():
            return self.flashObject.as_setCursor(cursor)

    def as_showCursorS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_showCursor()

    def as_hideCursorS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideCursor()