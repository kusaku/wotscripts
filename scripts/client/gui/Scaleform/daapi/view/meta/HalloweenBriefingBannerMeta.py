# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/HalloweenBriefingBannerMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class HalloweenBriefingBannerMeta(BaseDAAPIComponent):

    def as_hideS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hide()

    def as_showS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_show()