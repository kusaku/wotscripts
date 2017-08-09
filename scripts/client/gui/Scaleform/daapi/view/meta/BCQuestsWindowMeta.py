# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCQuestsWindowMeta.py
from gui.Scaleform.framework.entities.View import View

class BCQuestsWindowMeta(View):

    def onCloseClicked(self):
        self._printOverrideError('onCloseClicked')

    def as_setDataS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(value)