# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/EpicRandomPlayersPanelMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.battle.classic.players_panel import PlayersPanel

class EpicRandomPlayersPanelMeta(PlayersPanel):

    def focusedColumnChanged(self, value):
        self._printOverrideError('focusedColumnChanged')

    def as_setPlayersSwitchingAllowedS(self, isAllowed):
        if self._isDAAPIInited():
            return self.flashObject.as_setPlayersSwitchingAllowed(isAllowed)