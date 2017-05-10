# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RankedBattlesStageCompleteViewMeta.py
from gui.Scaleform.framework.entities.View import View

class RankedBattlesStageCompleteViewMeta(View):

    def closeView(self):
        self._printOverrideError('closeView')

    def onSoundTrigger(self, trigerName):
        self._printOverrideError('onSoundTrigger')

    def as_setDataS(self, data):
        """
        :param data: Represented by RankedBattlesStageCompleteVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)