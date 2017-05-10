# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/AcademyViewMeta.py
from gui.Scaleform.framework.entities.View import View

class AcademyViewMeta(View):

    def closeView(self):
        self._printOverrideError('closeView')