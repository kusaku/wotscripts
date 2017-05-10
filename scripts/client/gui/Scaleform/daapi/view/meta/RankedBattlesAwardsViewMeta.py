# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RankedBattlesAwardsViewMeta.py
from gui.Scaleform.framework.entities.View import View

class RankedBattlesAwardsViewMeta(View):

    def closeView(self):
        self._printOverrideError('closeView')

    def onSoundTrigger(self, triggerName):
        self._printOverrideError('onSoundTrigger')

    def as_setDataS(self, data):
        """
        :param data: Represented by RankedBattleAwardViewVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)