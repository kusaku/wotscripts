# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/SimpleDialogMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class SimpleDialogMeta(AbstractWindowView):

    def onButtonClick(self, buttonId):
        self._printOverrideError('onButtonClick')

    def as_setTextS(self, text):
        if self._isDAAPIInited():
            return self.flashObject.as_setText(text)

    def as_setTitleS(self, title):
        if self._isDAAPIInited():
            return self.flashObject.as_setTitle(title)

    def as_setButtonsS(self, buttonNames):
        """
        :param buttonNames: Represented by Array (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setButtons(buttonNames)

    def as_setButtonEnablingS(self, id, isEnabled):
        if self._isDAAPIInited():
            return self.flashObject.as_setButtonEnabling(id, isEnabled)

    def as_setButtonFocusS(self, id):
        if self._isDAAPIInited():
            return self.flashObject.as_setButtonFocus(id)