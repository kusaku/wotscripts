# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BattleStatisticDataControllerMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class BattleStatisticDataControllerMeta(BaseDAAPIComponent):

    def onRefreshComplete(self):
        self._printOverrideError('onRefreshComplete')

    def as_refreshS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_refresh()

    def as_setVehiclesDataS(self, vehData):
        """
        :param vehData: Represented by DAAPIVehiclesDataVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setVehiclesData(vehData)

    def as_addVehiclesInfoS(self, vehInfo):
        """
        :param vehInfo: Represented by DAAPIVehiclesDataVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_addVehiclesInfo(vehInfo)

    def as_updateVehiclesInfoS(self, upVehInfo):
        """
        :param upVehInfo: Represented by DAAPIVehiclesDataVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateVehiclesInfo(upVehInfo)

    def as_updateVehicleStatusS(self, data):
        """
        :param data: Represented by DAAPIVehicleStatusVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateVehicleStatus(data)

    def as_setFragsS(self, data):
        """
        :param data: Represented by DAAPIVehiclesStatsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setFrags(data)

    def as_updateVehiclesStatsS(self, data):
        """
        :param data: Represented by DAAPIVehiclesStatsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateVehiclesStats(data)

    def as_updatePlayerStatusS(self, data):
        """
        :param data: Represented by DAAPIPlayerStatusVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updatePlayerStatus(data)

    def as_setArenaInfoS(self, data):
        """
        :param data: Represented by DAAPIArenaInfoVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setArenaInfo(data)

    def as_setUserTagsS(self, data):
        """
        :param data: Represented by DAAPIVehiclesUserTagsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setUserTags(data)

    def as_updateUserTagsS(self, data):
        """
        :param data: Represented by DAAPIVehicleUserTagsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateUserTags(data)

    def as_updateInvitationsStatusesS(self, data):
        """
        :param data: Represented by DAAPIVehiclesInvitationStatusVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateInvitationsStatuses(data)

    def as_setPersonalStatusS(self, bitmask):
        if self._isDAAPIInited():
            return self.flashObject.as_setPersonalStatus(bitmask)

    def as_updatePersonalStatusS(self, added = 0, removed = 0):
        if self._isDAAPIInited():
            return self.flashObject.as_updatePersonalStatus(added, removed)