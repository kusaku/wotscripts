# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/EpicRandomScorePanelMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class EpicRandomScorePanelMeta(BaseDAAPIComponent):

    def as_setTeamHealthPercentagesS(self, team1, team2):
        if self._isDAAPIInited():
            return self.flashObject.as_setTeamHealthPercentages(team1, team2)