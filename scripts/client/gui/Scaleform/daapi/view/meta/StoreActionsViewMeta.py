# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/StoreActionsViewMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class StoreActionsViewMeta(BaseDAAPIComponent):

    def actionSelect(self, triggerChainID):
        self._printOverrideError('actionSelect')

    def onBattleTaskSelect(self, actionId):
        self._printOverrideError('onBattleTaskSelect')

    def onActionSeen(self, actionId):
        self._printOverrideError('onActionSeen')

    def as_setDataS(self, storeActionsData):
        """
        :param storeActionsData: Represented by StoreActionsViewVo (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(storeActionsData)

    def as_actionTimeUpdateS(self, actionsTime):
        """
        :param actionsTime: Represented by Vector.<StoreActionTimeVo> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_actionTimeUpdate(actionsTime)