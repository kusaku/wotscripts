# Embedded file name: scripts/client/gui/prb_control/entities/company/legacy/limits.py
from gui.prb_control.entities.base.limits import LimitsCollection, VehicleIsValid, VehiclesLevelLimit, TeamIsValid

class CompanyLimits(LimitsCollection):
    """
    Company limits class
    """

    def __init__(self, entity):
        super(CompanyLimits, self).__init__(entity, (VehicleIsValid(),), (VehiclesLevelLimit(), TeamIsValid()))