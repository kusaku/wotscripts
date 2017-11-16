# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/EventBoardsResultFilterPopoverViewMeta.py
from gui.Scaleform.daapi.view.lobby.popover.SmartPopOverView import SmartPopOverView

class EventBoardsResultFilterPopoverViewMeta(SmartPopOverView):

    def changeFilter(self, id):
        self._printOverrideError('changeFilter')

    def as_setInitDataS(self, data):
        """
        :param data: Represented by EventBoardTableFilterVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)