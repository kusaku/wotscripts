# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/PersonalMissionsAbstractInfoViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class PersonalMissionsAbstractInfoViewMeta(View):

    def bigBtnClicked(self):
        self._printOverrideError('bigBtnClicked')

    def as_setInitDataS(self, data):
        """
        :param data: Represented by PersonalMissionsAbstractInfoViewVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_updateS(self, data):
        """
        :param data: Represented by OperationAwardsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_update(data)