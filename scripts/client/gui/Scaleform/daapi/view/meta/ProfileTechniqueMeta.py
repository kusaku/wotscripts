# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ProfileTechniqueMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.profile.ProfileSection import ProfileSection

class ProfileTechniqueMeta(ProfileSection):

    def setSelectedTableColumn(self, index, sortDirection):
        self._printOverrideError('setSelectedTableColumn')

    def showVehiclesRating(self):
        self._printOverrideError('showVehiclesRating')

    def as_responseVehicleDossierS(self, data):
        """
        :param data: Represented by ProfileVehicleDossierVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_responseVehicleDossier(data)

    def as_setRatingButtonS(self, data):
        """
        :param data: Represented by RatingButtonVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setRatingButton(data)

    def as_setBtnCountersS(self, counters):
        """
        :param counters: Represented by Vector.<CountersVo> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setBtnCounters(counters)