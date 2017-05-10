# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/CrystalsPromoWindowMeta.py
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class CrystalsPromoWindowMeta(AbstractWindowView):

    def as_setDataS(self, data):
        """
        :param data: Represented by CrystalsPromoWindowVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)