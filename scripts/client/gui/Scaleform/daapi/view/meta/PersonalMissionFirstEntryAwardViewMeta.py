# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/PersonalMissionFirstEntryAwardViewMeta.py
from gui.Scaleform.daapi.view.meta.PersonalMissionsAbstractInfoViewMeta import PersonalMissionsAbstractInfoViewMeta

class PersonalMissionFirstEntryAwardViewMeta(PersonalMissionsAbstractInfoViewMeta):

    def onEscapePress(self):
        self._printOverrideError('onEscapePress')