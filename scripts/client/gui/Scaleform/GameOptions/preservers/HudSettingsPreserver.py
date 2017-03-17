# Embedded file name: scripts/client/gui/Scaleform/GameOptions/preservers/HudSettingsPreserver.py
__author__ = 's_karchavets'
from gui.Scaleform.GameOptions.utils import BasePreserver
import Settings
from gui.Scaleform.GameOptions.vo.MarkerSettings import AVAILABLE_MARKER_PROPERTIES

class SettingsAimsPreserver(BasePreserver):

    def __init__(self, key, profileName):
        self.__key = key
        self.__profileName = profileName

    def save(self, value):
        Settings.g_instance.setAimsDataByProfile(self.__key, value, self.__profileName)


class MarkersPreserver(BasePreserver):

    def save(self, value):
        for i, t in enumerate(value):
            for vehicleType in ('airMarker', 'groundMarker'):
                voVehicleType = getattr(t, vehicleType)
                for targetType in ('enemy', 'target', 'friendly', 'squads'):
                    voTargetType = getattr(voVehicleType, targetType)
                    for altState in ('basic', 'alt'):
                        voAltState = getattr(voTargetType, altState)
                        for key in AVAILABLE_MARKER_PROPERTIES:
                            Settings.g_instance.saveMarkers(vehicleType, targetType, altState, key, i, str(getattr(voAltState, key)))


class MarkerSelectPreserver(BasePreserver):

    def save(self, value):
        for i, t in enumerate(value):
            if t is not None:
                Settings.g_instance.setMarkerSelectID(i, t)

        return