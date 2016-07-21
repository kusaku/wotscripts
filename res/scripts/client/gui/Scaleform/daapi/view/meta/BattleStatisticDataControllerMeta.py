# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BattleStatisticDataControllerMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIModule import BaseDAAPIModule

class BattleStatisticDataControllerMeta(BaseDAAPIModule):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseDAAPIModule
    null
    """

    def onRefreshComplete(self):
        """
        :return :
        """
        self._printOverrideError('onRefreshComplete')

    def as_refreshS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_refresh()

    def as_setVehiclesDataS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setVehiclesData(data)

    def as_addVehiclesInfoS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_addVehiclesInfo(data)

    def as_updateVehiclesInfoS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateVehiclesInfo(data)

    def as_updateVehicleStatusS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateVehicleStatus(data)

    def as_setVehiclesStatsS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setVehiclesStats(data)

    def as_updateVehiclesStatsS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateVehiclesStats(data)

    def as_updatePlayerStatusS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updatePlayerStatus(data)

    def as_setArenaInfoS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setArenaInfo(data)

    def as_setUserTagsS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setUserTags(data)

    def as_updateUserTagsS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateUserTags(data)

    def as_updateInvitationsStatusesS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateInvitationsStatuses(data)

    def as_setPersonalStatusS(self, bitmask):
        """
        :param bitmask:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setPersonalStatus(bitmask)

    def as_updatePersonalStatusS(self, added, removed):
        """
        :param added:
        :param removed:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updatePersonalStatus(added, removed)