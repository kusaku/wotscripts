# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCAppearManagerMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class BCAppearManagerMeta(BaseDAAPIComponent):

    def onComponentTweenComplete(self, componentId):
        self._printOverrideError('onComponentTweenComplete')

    def onComponentPrepareAppear(self, componentId):
        self._printOverrideError('onComponentPrepareAppear')

    def as_showAnimatedS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_showAnimated(data)

    def as_setAppearConfigS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setAppearConfig(data)