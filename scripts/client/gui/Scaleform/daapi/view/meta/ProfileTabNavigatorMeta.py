# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ProfileTabNavigatorMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class ProfileTabNavigatorMeta(BaseDAAPIComponent):

    def onTabChange(self, tabId):
        self._printOverrideError('onTabChange')

    def as_setInitDataS(self, data):
        """
        :param data: Represented by ProfileMenuInfoVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_setBtnTabCountersS(self, counters):
        """
        :param counters: Represented by Vector.<CountersVo> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setBtnTabCounters(counters)