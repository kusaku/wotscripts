# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/EventConsumablesPanelMeta.py
from gui.Scaleform.daapi.view.battle.shared.consumables_panel import ConsumablesPanel

class EventConsumablesPanelMeta(ConsumablesPanel):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends ConsumablesPanel
    null
    """

    def as_updateBonusNotificationS(self, isVisible, bonus, icon, tooltip):
        """
        :param isVisible:
        :param bonus:
        :param icon:
        :param tooltip:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateBonusNotification(isVisible, bonus, icon, tooltip)