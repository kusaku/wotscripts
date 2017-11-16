# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/AwardWindowsBaseMeta.py
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class AwardWindowsBaseMeta(AbstractWindowView):

    def as_setDataS(self, data):
        """
        :param data: Represented by AwardWindowVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)