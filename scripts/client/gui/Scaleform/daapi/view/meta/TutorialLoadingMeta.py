# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/TutorialLoadingMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class TutorialLoadingMeta(BaseDAAPIComponent):

    def as_setTutorialArenaInfoS(self, data):
        """
        :param data: Represented by DAAPIArenaInfoVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setTutorialArenaInfo(data)