# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/HalloweenBattleSelectorMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class HalloweenBattleSelectorMeta(BaseDAAPIComponent):

    def playerSelectionMade(self, isPvE):
        self._printOverrideError('playerSelectionMade')

    def as_showS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_show()

    def as_hideS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hide()

    def as_enableButtonsS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_enableButtons()

    def as_disableButtonsS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_disableButtons()

    def as_startWithPvES(self, val):
        if self._isDAAPIInited():
            return self.flashObject.as_startWithPvE(val)

    def as_currentStateIsPvES(self):
        if self._isDAAPIInited():
            return self.flashObject.as_currentStateIsPvE()

    def as_initBattleSelectorS(self, data):
        """
        :param data: Represented by SelectorWindowStaticDataVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_initBattleSelector(data)