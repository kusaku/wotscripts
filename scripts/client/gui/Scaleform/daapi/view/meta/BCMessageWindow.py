# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCMessageWindow.py
from gui.Scaleform.framework.entities.View import View

class BCMessageWindow(View):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends View
    """

    def onMessageRemoved(self):
        self._printOverrideError('onMessageRemoved')

    def as_setMessageDataS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setMessageData(value)