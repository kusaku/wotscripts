# Embedded file name: scripts/client/gui/prb_control/entities/bootcamp/pre_queue/actions_validator.py
from gui.prb_control.entities.base.actions_validator import BaseActionsValidator
from gui.prb_control.items import ValidationResult

class BootcampActionsValidator(BaseActionsValidator):

    def _validate(self):
        from bootcamp.BootcampGarage import g_bootcampGarage
        if not g_bootcampGarage.isLessonFinished:
            return ValidationResult(False, 'bootcamp/lessonNotFinished')
        if not g_bootcampGarage.isSecondVehicleSelected():
            return ValidationResult(False, 'bootcamp/wrongVehicleSelected')
        return super(BootcampActionsValidator, self)._validate()