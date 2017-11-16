# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BossLocationMarkerMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class BossLocationMarkerMeta(BaseDAAPIComponent):

    def as_hideS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hide()

    def as_showS(self, onLeft):
        if self._isDAAPIInited():
            return self.flashObject.as_show(onLeft)

    def as_updateDistanceS(self, val):
        if self._isDAAPIInited():
            return self.flashObject.as_updateDistance(val)