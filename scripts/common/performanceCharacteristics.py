# Embedded file name: scripts/common/performanceCharacteristics.py
import db.DBLogic
from _airplanesConfigurations_db import airplanesConfigurations
import _performanceCharacteristics_db
from consts import LOGICAL_PART
performanceParamList = ['hp',
 'dps',
 'speedFactor',
 'maneuverability',
 'speedAtTheGround',
 'maxSpeed',
 'optimalHeight',
 'averageTurnTime',
 'mass',
 'shellMass',
 'rateOfClimbing',
 'optimalManeuverSpeed',
 'rollManeuverability',
 'controllability',
 'diveSpeed',
 'stallSpeed']

def hp(globalID, modifiers, bombCount, rocketCount):
    return _performanceCharacteristics_db.airplanes[globalID].hp


def dps(globalID, modifiers, bombCount, rocketCount):
    return _performanceCharacteristics_db.airplanes[globalID].dps


def speedFactor(globalID, modifiers, bombCount, rocketCount):
    return _performanceCharacteristics_db.airplanes[globalID].speedFactor


def maneuverability(globalID, modifiers, bombCount, rocketCount):
    return _performanceCharacteristics_db.airplanes[globalID].maneuverability


def speedAtTheGround(globalID, modifiers, bombCount, rocketCount):
    return _performanceCharacteristics_db.airplanes[globalID].speedAtTheGround


def maxSpeed(globalID, modifiers, bombCount, rocketCount):
    return _performanceCharacteristics_db.airplanes[globalID].maxSpeed


def optimalHeight(globalID, modifiers, bombCount, rocketCount):
    return _performanceCharacteristics_db.airplanes[globalID].optimalHeight


def averageTurnTime(globalID, modifiers, bombCount, rocketCount):
    return _performanceCharacteristics_db.airplanes[globalID].averageTurnTime


def mass(globalID, modifiers, bombCount, rocketCount):
    return _performanceCharacteristics_db.airplanes[globalID].mass


def shellMass(globalID, modifiers, bombCount, rocketCount):
    return _performanceCharacteristics_db.airplanes[globalID].shellMass


def rateOfClimbing(globalID, modifiers, bombCount, rocketCount):
    return _performanceCharacteristics_db.airplanes[globalID].rateOfClimbing


def optimalManeuverSpeed(globalID, modifiers, bombCount, rocketCount):
    return _performanceCharacteristics_db.airplanes[globalID].optimalManeuverSpeed


def rollManeuverability(globalID, modifiers, bombCount, rocketCount):
    return _performanceCharacteristics_db.airplanes[globalID].rollManeuverability


def controllability(globalID, modifiers, bombCount, rocketCount):
    return _performanceCharacteristics_db.airplanes[globalID].controllability