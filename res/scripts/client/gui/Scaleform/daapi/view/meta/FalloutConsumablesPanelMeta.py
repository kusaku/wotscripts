# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/FalloutConsumablesPanelMeta.py
from gui.Scaleform.daapi.view.battle.shared.consumables_panel import ConsumablesPanel

class FalloutConsumablesPanelMeta(ConsumablesPanel):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends ConsumablesPanel
    null
    """

    def as_initializeRageProgressS(self, show, barProps):
        """
        :param show:
        :param barProps:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_initializeRageProgress(show, barProps)

    def as_updateProgressBarValueByDeltaS(self, delta):
        """
        :param delta:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateProgressBarValueByDelta(delta)

    def as_updateProgressBarValueS(self, value):
        """
        :param value:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateProgressBarValue(value)