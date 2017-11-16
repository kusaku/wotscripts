# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/EvilEyeMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class EvilEyeMeta(BaseDAAPIComponent):

    def as_showMainS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_showMain()

    def as_showSecondaryS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_showSecondary()

    def as_showNotificationS(self, msg):
        if self._isDAAPIInited():
            return self.flashObject.as_showNotification(msg)

    def as_setEyeLabelsS(self, data):
        """
        :param data: Represented by EvilEyeMessageVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setEyeLabels(data)

    def as_hideAllNowS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideAllNow()

    def as_hideMainS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideMain()

    def as_hideSecondaryS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideSecondary()

    def as_hideNotificationS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideNotification()