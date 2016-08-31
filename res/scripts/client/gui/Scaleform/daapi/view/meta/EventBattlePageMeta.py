# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/EventBattlePageMeta.py
from gui.Scaleform.daapi.view.battle.event_mark1.page import EventMark1Page

class EventBattlePageMeta(EventMark1Page):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends EventMark1Page
    null
    """

    def as_setPostmortemGasAtackInfoS(self, infoStr, respawnStr, showDeadIcon):
        """
        :param infoStr:
        :param respawnStr:
        :param showDeadIcon:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setPostmortemGasAtackInfo(infoStr, respawnStr, showDeadIcon)

    def as_hidePostmortemGasAtackInfoS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_hidePostmortemGasAtackInfo()