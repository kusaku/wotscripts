# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/TrainingFormMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class TrainingFormMeta(View):

    def joinTrainingRequest(self, id):
        self._printOverrideError('joinTrainingRequest')

    def createTrainingRequest(self):
        self._printOverrideError('createTrainingRequest')

    def onEscape(self):
        self._printOverrideError('onEscape')

    def onLeave(self):
        self._printOverrideError('onLeave')

    def as_setListS(self, data):
        """
        :param data: Represented by TrainingFormVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setList(data)