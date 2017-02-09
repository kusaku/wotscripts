# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ProfileTechniqueMeta.py
from gui.Scaleform.daapi.view.lobby.profile.ProfileSection import ProfileSection

class ProfileTechniqueMeta(ProfileSection):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends ProfileSection
    """

    def setSelectedTableColumn(self, index, sortDirection):
        self._printOverrideError('setSelectedTableColumn')

    def as_responseVehicleDossierS(self, data):
        """
        :param data: Represented by ProfileVehicleDossierVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_responseVehicleDossier(data)