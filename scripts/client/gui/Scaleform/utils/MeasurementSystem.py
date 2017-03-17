# Embedded file name: scripts/client/gui/Scaleform/utils/MeasurementSystem.py
import Settings
from Helpers.i18n import localizeHUD, localizeLobby
from clientConsts import SI_TO_SI_KMH, SI_TO_IMPERIAL_KMH, SI_TO_SEA_KMH, SI_TO_SI_METER, SI_TO_IMPERIAL_METER, SI_TO_SEA_METER, SI_TO_SI_KGS, SI_TO_IMPERIAL_KGS, SI_TO_SEA_KGS

class MeasurementSystem(object):
    __LOC_HUD_TABLE = {'ui_vario': ['ui_vario_meters', 'UI_VARIO_FT', 'UI_VARIO_FT'],
     'ui_speed': ['ui_speedo_kmh', 'ui_speedo_mph', 'ui_speedo_knt'],
     'ui_meter': ['ui_vario_m', 'ui_vario_ft', 'ui_vario_ft']}
    groundSpeed = ('MARKET_AIRPLANE_GROUND_MAX_SPEED_KMH', 'MARKET_AIRPLANE_GROUND_MAX_SPEED_MPH', 'MARKET_AIRPLANE_GROUND_MAX_SPEED_KNT')
    distance = ('MARKET_AIRPLANE_TURN_RADIUS_M', 'MARKET_AIRPLANE_TURN_RADIUS_FT', 'MARKET_AIRPLANE_TURN_RADIUS_FT')
    __LOC_MARKET_TABLE = {'MARKET_AIRPLANE_ENGINE_CAPACITY_KGS': ['MARKET_AIRPLANE_ENGINE_CAPACITY_KGS', 'MARKET_AIRPLANE_ENGINE_CAPACITY_LBF', 'MARKET_AIRPLANE_ENGINE_CAPACITY_LBF'],
     'MARKET_AIRPLANE_GROUND_MAX_SPEED': groundSpeed,
     'MARKET_AIRPLANE_HEIGHT_MAX_SPEED': ['MARKET_AIRPLANE_HEIGHT_MAX_SPEED_KMH', 'MARKET_AIRPLANE_HEIGHT_MAX_SPEED_MPH', 'MARKET_AIRPLANE_HEIGHT_MAX_SPEED_KNT'],
     'MARKET_AIRPLANE_RATE_OF_CLIMB': ['MARKET_AIRPLANE_RATE_OF_CLIMB_MS', 'MARKET_AIRPLANE_RATE_OF_CLIMB_FPS', 'MARKET_AIRPLANE_RATE_OF_CLIMB_FPS'],
     'MARKET_AIRPLANE_TURN_RADIUS': distance,
     'MARKET_AIRPLANE_MASS': ['MARKET_AIRPLANE_MASS_KG', 'MARKET_AIRPLANE_MASS_POUNDS', 'MARKET_AIRPLANE_MASS_KG'],
     'LABEL_OPTIMAL_MANEUVERING_SPEED': groundSpeed,
     'LABEL_DIVING_SPEED': groundSpeed,
     'LABEL_STALL_SPEED': groundSpeed,
     'LOBBY_AIRCRAFT_COMPARISON_LABEL_ALTITUDE': distance,
     'LABEL_OPTIMAL_HEIGHT': distance,
     'LOBBY_CHARACTERISTICS_ROLL_SPD': ['MARKET_AIRPLANE_DEG_PER_SEC', 'MARKET_AIRPLANE_DEG_PER_SEC', 'MARKET_AIRPLANE_DEG_PER_SEC']}
    __CONVERSION = {'khm': [SI_TO_SI_KMH, SI_TO_IMPERIAL_KMH, SI_TO_SEA_KMH],
     'meters': [SI_TO_SI_METER, SI_TO_IMPERIAL_METER, SI_TO_SEA_METER],
     'kgs': [SI_TO_SI_KGS, SI_TO_IMPERIAL_KGS, SI_TO_SEA_KGS]}

    def __init__(self, measurementSystem = None):
        if measurementSystem is None:
            self.__measurementSystem = Settings.g_instance.gameUI['measurementSystem']
        else:
            self.__measurementSystem = measurementSystem
        if self.__measurementSystem > 2:
            raise ValueError('Measurement system value is outbound: {0}'.format(self.__measurementSystem))
        return

    def __onMeasurementSystemChanged(self):
        self.__measurementSystem = Settings.g_instance.gameUI['measurementSystem']

    def localizeHUD(self, id):
        return localizeHUD(self.__LOC_HUD_TABLE[id][self.__measurementSystem])

    def localizeMarket(self, id):
        return localizeLobby(self.__LOC_MARKET_TABLE[id][self.__measurementSystem])

    def getKmh(self, kmh):
        return kmh / self.__CONVERSION['khm'][self.__measurementSystem]

    def getMeters(self, meters):
        return meters / self.__CONVERSION['meters'][self.__measurementSystem]

    def getKgs(self, kgs):
        return kgs / self.__CONVERSION['kgs'][self.__measurementSystem]