# Embedded file name: scripts/client/WeatherManager.py
import BigWorld
import db.DBLogic
from debug_utils import *

def InitWeather():
    arenaData = db.DBLogic.g_instance.getArenaData(BigWorld.player().arenaType)
    LOG_DEBUG("WeatherManager:InitWeather() '%s': %s, %s" % (arenaData.geometry, arenaData.weatherWindSpeed, arenaData.weatherWindGustiness))
    try:
        BigWorld.weather().windAverage(arenaData.weatherWindSpeed[0], arenaData.weatherWindSpeed[1])
        BigWorld.weather().windGustiness(arenaData.weatherWindGustiness)
    except ValueError:
        pass
    except EnvironmentError:
        pass