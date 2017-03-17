# Embedded file name: scripts/client/gui/Scaleform/UIHelper.py
import BigWorld
import GameEnvironment
from clientConsts import LOC_HINT_PLANE_TASK, BATTLE_NAME_BY_TYPE_HUD_LOC_ID, FIREPOWER_K, MANEUVERABILITY_K, SPEED_K, COMPARING_VEHICLE_STATES, HEIGHT_K, HP_K
from Helpers.i18n import localizeTutorial, localizeLobby, localizeMap
from _tutorial_data import TutorialData
import db.DBLogic
from debug_utils import LOG_ERROR, LOG_DEBUG
import InputMapping
from Helpers.PerformanceSpecsHelper import getPerformanceSpecsTable, ProjectileInfo
from consts import UPDATABLE_TYPE, UPGRADE_TYPE, TYPE_TEAM_OBJECT
from _airplanesConfigurations_db import getAirplaneConfiguration
from math import ceil

def getTeamObjectType(clientArena, id):
    if clientArena.isTeamObjectContainsTurret(id):
        return TYPE_TEAM_OBJECT.TURRET
    else:
        targetType = clientArena.getTeamObjectType(id)
        if targetType == TYPE_TEAM_OBJECT.VEHICLE:
            targetType = TYPE_TEAM_OBJECT.SMALL
        return targetType


def getPlayerNameWithClan(playerName, clanName):
    if clanName:
        if playerName.find('[') < 0 or playerName[-1] != ']':
            return '{0}[{1}]'.format(playerName, clanName)
    return playerName


class BattleInfo:

    def __init__(self):
        pass

    def getBattleInfo(self, battleType = None, tutorialIndex = None):
        owner = BigWorld.player()
        if battleType is None:
            battleType = owner.battleType
        try:
            battleName = localizeLobby(BATTLE_NAME_BY_TYPE_HUD_LOC_ID[battleType]) if battleType else None
        except KeyError:
            battleName = 'No battle name provided for battleType id {}'.format(battleType)

        arenaData = db.DBLogic.g_instance.getArenaData(owner.arenaType)
        mapName = localizeMap(arenaData.typeName) if arenaData else None
        teamTask, playerTask = ('teamTask', 'playerTask')
        if tutorialIndex is None:
            tutorialIndex = owner.tutorialIndex
        if tutorialIndex != -1:
            teamTask = localizeTutorial(TutorialData.lesson[tutorialIndex].battleLoadingTitle)
            playerTask = localizeTutorial(TutorialData.lesson[tutorialIndex].battleLoadingDescription)
        else:
            ownerInfo = GameEnvironment.getClientArena().getAvatarInfo(owner.id)
            if ownerInfo is not None:
                teamTask = localizeTutorial(LOC_HINT_PLANE_TASK.get(ownerInfo['settings'].airplane.planeType, teamTask))
                playerTask = localizeTutorial('hint_superiority_1')
        return (battleType,
         battleName,
         mapName,
         teamTask,
         playerTask)


class SQUAD_TYPES:
    WITHOUT_SQUAD = 0
    OTHER = 1
    OWN = 2

    @staticmethod
    def getSquadType(squadNumber, avatarID):
        if not squadNumber:
            return SQUAD_TYPES.WITHOUT_SQUAD
        owner = BigWorld.player()
        if avatarID == owner.id:
            return SQUAD_TYPES.OWN
        clientArena = GameEnvironment.getClientArena()
        ownerInfo = clientArena.getAvatarInfo(owner.id)
        avatarInfo = clientArena.getAvatarInfo(avatarID)
        if ownerInfo is not None and avatarInfo is not None:
            if owner.teamIndex == avatarInfo['teamIndex'] and ownerInfo['squadID'] == squadNumber:
                return SQUAD_TYPES.OWN
            return SQUAD_TYPES.OTHER
        else:
            return

    @staticmethod
    def playerSquadID():
        return SQUAD_TYPES.getSquadIDbyAvatarID(BigWorld.player().id)

    @staticmethod
    def getSquadIDbyAvatarID(avatarID):
        avatarInfo = GameEnvironment.getClientArena().getAvatarInfo(avatarID)
        if avatarInfo is not None and 'squadID' in avatarInfo:
            return avatarInfo['squadID']
        else:
            return 0


def getTargetHealth(target):
    if target.health <= 0:
        return 0
    h = ceil(target.health)
    if 1 >= h:
        return 1
    return h


def getTargetHealthPrc(target):
    hPrc = 100.0 * getTargetHealth(target) / target.maxHealth
    if 1 >= hPrc > 0:
        return 1
    return int(round(hPrc))


class EQUIPMENT_STATES:
    EMPTY = 0
    READY = 1
    DISABLED = 2
    USE = 3


def getKeyLocalization(cmdID, keyIndex = 0):
    keyName = ''
    keysControls = InputMapping.g_instance.getKeyControlsHelp([cmdID])
    keysData = keysControls.get(cmdID, None)
    if keysData is not None and keysData['keys']:
        keyName = InputMapping.getKeyLocalization(keysData['keys'][keyIndex])
        if keysData['isFireAxis'][keyIndex]:
            if keysData['axisSign'][keyIndex] == 1:
                keyName += '+'
            else:
                keyName += '-'
    return keyName


def getProjectiles(globalID, shellsCount):
    if shellsCount is not None:
        planeConfig = getAirplaneConfiguration(globalID)
        projectiles = []
        shellsCount = dict([ (x['key'], x['value']) for x in shellsCount ])
        for slotID, configID in planeConfig.weaponSlots:
            weaponInfo = db.DBLogic.g_instance.getWeaponInfo(planeConfig.planeID, slotID, configID)
            if weaponInfo and slotID in shellsCount:
                projectiles.append(ProjectileInfo(slotID, configID, weaponInfo[2], shellsCount[slotID]))

    else:
        projectiles = None
    return projectiles


BALANCE_CHARACTERISTIC = {'dps': FIREPOWER_K,
 'maneuverability': MANEUVERABILITY_K,
 'speedFactor': SPEED_K,
 'optimalHeight': HEIGHT_K,
 'hp': HP_K}

def getCalculatedBalanceCharacteristic(ID1, ID2 = None):
    owner = BigWorld.player()
    if ID2 is None:
        ID2 = owner.id
    globalID1 = getGlobalID(ID1)
    globalID2 = getGlobalID(ID2)
    avatarsInfo = GameEnvironment.getClientArena().avatarInfos
    otherInfo = avatarsInfo.get(ID1, None)
    ownerInfo = avatarsInfo.get(ID2, None)
    otherProjectiles = getProjectiles(globalID1, otherInfo.get('shellsCount', None))
    ownerProjectiles = getProjectiles(globalID2, ownerInfo.get('shellsCount', None))
    specs1 = getPerformanceSpecsTable(globalID1, True, otherProjectiles, otherInfo.get('equipment', None), maxHealth=otherInfo.get('maxHealth', None))
    specs2 = getPerformanceSpecsTable(globalID2, True, ownerProjectiles, ownerInfo.get('equipment', None), maxHealth=ownerInfo.get('maxHealth', None))
    if specs1 is None:
        LOG_ERROR('Performance specs not found for globalID {0}'.format(globalID1))
    if specs2 is None:
        LOG_ERROR('Performance specs not found for globalID {0}'.format(globalID2))
    first = dict([ (ch, getattr(specs1, ch) if specs1 is not None else 0.0) for ch in BALANCE_CHARACTERISTIC.iterkeys() ])
    second = dict([ (ch, getattr(specs2, ch) if specs2 is not None else 0.0) for ch in BALANCE_CHARACTERISTIC.iterkeys() ])
    diff = dict([ (ch, round(second[ch]) - round(first[ch])) for ch in BALANCE_CHARACTERISTIC.iterkeys() ])
    try:
        ratio = dict([ (ch, second[ch] / first[ch] if first[ch] else second[ch]) for ch in BALANCE_CHARACTERISTIC.iterkeys() ])
        percentDiff = dict([ (ch, round(diff[ch] * 100.0 / second[ch])) for ch in BALANCE_CHARACTERISTIC.iterkeys() ])
    except ZeroDivisionError:
        LOG_ERROR('One of comparable performance specs is zero for global ids: {0} {1}'.format(globalID1, globalID2))
        raise

    def getState(ch, ratio, diff):
        K = BALANCE_CHARACTERISTIC[ch]
        if K == 1.0:
            if diff > 0.0:
                return COMPARING_VEHICLE_STATES.UP
            if diff < 0.0:
                return COMPARING_VEHICLE_STATES.DOWN
        else:
            if not diff:
                return COMPARING_VEHICLE_STATES.NORMAL
            if ratio > K:
                return COMPARING_VEHICLE_STATES.UP
            if 1 / K > ratio:
                return COMPARING_VEHICLE_STATES.DOWN
        return COMPARING_VEHICLE_STATES.NORMAL

    state = dict([ (ch, getState(ch, ratio[ch], diff[ch])) for ch in BALANCE_CHARACTERISTIC.iterkeys() ])
    return (diff, state, percentDiff)


def getGlobalID(ID):
    clientArena = GameEnvironment.getClientArena()
    if clientArena is not None:
        avatarInfo = clientArena.getAvatarInfo(ID)
        if avatarInfo:
            airplaneInfo = avatarInfo.get('airplaneInfo', None)
            if airplaneInfo:
                return airplaneInfo['globalID']
    return 0


def onDenunciation(DBId, denunciationID, violatorKind):
    """
    @param <int> DBId:
    @param denunciationID:  see class consts.DENUNCIATION
    @param <int> violatorKind:    1 - enemy, 2 - ally
    """
    LOG_DEBUG('__onDenunciation', DBId, denunciationID, violatorKind)
    BigWorld.player().base.makeDenunciation(DBId, denunciationID, violatorKind)
    import BWPersonality
    BWPersonality.g_initPlayerInfo.denunciationsLeft -= 1 if BWPersonality.g_initPlayerInfo.denunciationsLeft > 0 else 0