# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/QuestsSeasonsViewMeta.py
from gui.Scaleform.daapi.view.lobby.server_events.QuestsContentTabs import QuestsContentTabs

class QuestsSeasonsViewMeta(QuestsContentTabs):

    def onShowAwardsClick(self):
        self._printOverrideError('onShowAwardsClick')

    def onTileClick(self, tileID):
        self._printOverrideError('onTileClick')

    def onSlotClick(self, slotID):
        self._printOverrideError('onSlotClick')

    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_setSeasonsDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setSeasonsData(data)

    def as_setSlotsDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setSlotsData(data)