# Embedded file name: scripts/common/qualifier_condition_updaters.py
import time
RADIUS_NEARBY = 50

def __now(**kwargs):
    return int(time.time())


def __mapKind(mapKind, **kwargs):
    return mapKind


def __playerTankHealthPercent(vehicleRef, **kwargs):
    vehicle = vehicleRef()
    return vehicle.health / float(vehicle.typeDescriptor.maxHealth)


def __aliveSquadMembersCount(vehicleRef, spatialData, **kwargs):
    vehicle = vehicleRef()
    selfSquadID = vehicle.publicInfo.prebattleID
    if not selfSquadID:
        return None
    else:
        aliveSquadMembersCount = 0
        for vehSpatialInfo in spatialData:
            vehID = vehSpatialInfo['vehicleID']
            if vehID != vehicle.id:
                prebattleID = vehSpatialInfo['prebattleID']
                isAlive = vehSpatialInfo['isAlive']
                if isAlive and prebattleID and prebattleID == selfSquadID:
                    aliveSquadMembersCount += 1

        return aliveSquadMembersCount


def __aliveAlliesCount(vehicleRef, spatialData, **kwargs):
    vehicle = vehicleRef()
    selfTeam = vehicle.publicInfo.team
    aliveAlliesCount = 0
    for vehSpatialInfo in spatialData:
        team = vehSpatialInfo['team']
        isAlive = vehSpatialInfo['isAlive']
        if isAlive and team == selfTeam:
            aliveAlliesCount += 1

    return aliveAlliesCount


def __enemiesCountNearby(vehicleRef, spatialData, **kwargs):
    vehicle = vehicleRef()
    selfPosition = vehicle.position
    selfTeam = vehicle.publicInfo.team
    enemiesCountNearby = 0
    for vehSpatialInfo in spatialData:
        team = vehSpatialInfo['team']
        position = vehSpatialInfo['position']
        isAlive = vehSpatialInfo['isAlive']
        if selfTeam != team and isAlive and selfPosition.distTo(position) <= RADIUS_NEARBY:
            enemiesCountNearby += 1

    return enemiesCountNearby


def __lightTankEnemiesCountNearby(vehicleRef, spatialData, **kwargs):
    vehicle = vehicleRef()
    selfPosition = vehicle.position
    selfTeam = vehicle.publicInfo.team
    lightTankEnemiesCountNearby = 0
    for vehSpatialInfo in spatialData:
        team = vehSpatialInfo['team']
        vehClass = vehSpatialInfo['vehClass']
        position = vehSpatialInfo['position']
        isAlive = vehSpatialInfo['isAlive']
        if selfTeam != team and vehClass == 'lightTank' and isAlive and selfPosition.distTo(position) <= RADIUS_NEARBY:
            lightTankEnemiesCountNearby += 1

    return lightTankEnemiesCountNearby


def __anyEnemyTankDetectionTime(vehicleRef, **kwargs):
    witness = vehicleRef().p['witness']
    timestamps = []
    for id in witness.getTemporarilyWitnessedVehicles():
        timestamp = witness.getTimestamp(id)
        if timestamp is None:
            continue
        timestamps.append(timestamps)

    res = max(timestamps) if timestamps else 0
    return res


CONDITION_UPDATERS = {'now': __now,
 'mapKind': __mapKind,
 'playerTankHealthPercent': __playerTankHealthPercent,
 'aliveSquadMembersCount': __aliveSquadMembersCount,
 'aliveAlliesCount': __aliveAlliesCount,
 'enemiesCountNearby': __enemiesCountNearby,
 'lightTankEnemiesCountNearby': __lightTankEnemiesCountNearby,
 'enemyTankDetectionTime': __anyEnemyTankDetectionTime}
REGISTERED_CONDITION_PARAMS = frozenset(CONDITION_UPDATERS.keys()).union({'playerTankUnproductiveHitTime', 'enemyTankDestructionTime', 'enemyTankCriticalHitTime'})