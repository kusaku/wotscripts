# Embedded file name: scripts/client/gui/prb_control/entities/base/unit/cooldown.py
from gui.prb_control.entities.base.cooldown import PrbCooldownManager

class UnitCooldownManager(PrbCooldownManager):
    """
    Unit cooldown manager class
    """

    def getDefaultCoolDown(self):
        return 0.0