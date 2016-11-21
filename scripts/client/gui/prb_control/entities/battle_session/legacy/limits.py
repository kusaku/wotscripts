# Embedded file name: scripts/client/gui/prb_control/entities/battle_session/legacy/limits.py
from gui.prb_control.entities.base.limits import LimitsCollection, VehicleIsValid, VehiclesLevelLimit, TeamIsValid

class BattleSessionLimits(LimitsCollection):
    """
    Battle session limits class
    """

    def __init__(self, entity):
        super(BattleSessionLimits, self).__init__(entity, (VehicleIsValid(),), (VehiclesLevelLimit(), TeamIsValid()))