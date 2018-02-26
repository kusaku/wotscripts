# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ProfileSectionMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class ProfileSectionMeta(BaseDAAPIComponent):

    def setActive(self, value):
        self._printOverrideError('setActive')

    def requestData(self, vehicleId):
        self._printOverrideError('requestData')

    def requestDossier(self, type):
        self._printOverrideError('requestDossier')

    def as_updateS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_update(data)

    def as_setInitDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_responseDossierS(self, battlesType, data, frameLabel, emptyScreenLabel):
        if self._isDAAPIInited():
            return self.flashObject.as_responseDossier(battlesType, data, frameLabel, emptyScreenLabel)