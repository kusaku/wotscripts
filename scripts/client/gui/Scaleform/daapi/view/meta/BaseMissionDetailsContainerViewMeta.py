# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BaseMissionDetailsContainerViewMeta.py
from gui.Scaleform.framework.entities.View import View

class BaseMissionDetailsContainerViewMeta(View):

    def closeView(self):
        self._printOverrideError('closeView')

    def onChangePage(self, eventID):
        self._printOverrideError('onChangePage')

    def as_setInitDataS(self, data):
        """
        :param data: Represented by BaseMissionDetailsContainerVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)