# Embedded file name: scripts/client/gui/Scaleform/BattleResult.py
import BigWorld
import GameEnvironment
from _awards_data import AwardsDB
from debug_utils import LOG_DEBUG, LOG_TRACE
from consts import *
from Helpers.i18n import localizeHUD, localizeAirplane, localizeBattleResults, localizeLobby, localizeAchievements
import ClientLog
from Singleton import singleton
from EntityHelpers import AvatarFlags
from clientConsts import PLANE_TYPE_BATTLE_RESULT_ICO_PATH, OBJECTS_INFO
from UIHelper import SQUAD_TYPES, getPlayerNameWithClan
from consts import DAMAGE_REASON

def getStrValueWithFactor(val, xp_factor):
    if val > 0:
        val = ''.join(['+', str(val)])
        if xp_factor > 1:
            val = ''.join([str(val),
             '(x',
             str(xp_factor),
             ')'])
    return val


class _AwardVO:

    def __init__(self, name, iconPath, count = 1):
        self.name = name
        self.icon = iconPath
        self.count = count


class _BattleResultVO:

    def __init__(self):
        self.package_ = 'wowp.battleResult.vo.'
        self.battleResult = ''
        self.shots = ''
        self.hits = ''
        self.hitsTaken = ''
        self.credits = ''
        self.experience = ''
        self.infoPlayer = ''
        self.killedBy = ''
        self.killedByTitle = ''
        self.killedPlayers = []
        self.damagedPlayers = []
        self.spottedPlayers = []
        self.teamPlayers = []
        self.winState = -1
        self.txtPenaltyCredits = 0
        self.txtPenaltyExperience = 0
        self.txtCompensationCredits = 0
        self.awards = []


@singleton

class BattleResult(object):

    def __init__(self):
        self.__battleResData = None
        return

    def setResults(self, clientBattleResult):
        LOG_DEBUG('setBattleResult:', clientBattleResult)
        self.__battleResData = _BattleResultVO()
        self.__lastClientBattleResult = clientBattleResult
        self.__makeResult()

    def __makeResult(self):
        player = BigWorld.player()
        lastDamageReason = player.lastDamageReason
        clientArena = GameEnvironment.getClientArena()
        avatarInfos = clientArena.avatarInfos
        result = self.__lastClientBattleResult
        ownPlayerData = avatarInfos[player.id]
        planeShots = result['shots']
        planeHits = result['hitted']
        ownHit = result['received']
        winState = result['winState']
        gameResult = result['gameResult']
        playerTeamID = ownPlayerData['teamIndex']
        playerCredits = result['credits']
        playerExperience = result['xp']
        playerXPCoeff = result['xpFactor']
        playerCreditsCoeff = result['crFactor']
        creditsPenalty = result['creditsPenalty']
        xpPenalty = result['xpPenalty']
        creditsFromTK = result['creditsFromTK']
        hitStructure = 0
        killerID = result['killerID']
        damagedObjects = {TYPE_TEAM_OBJECT.TURRET: result['damagedTurrets'],
         TYPE_TEAM_OBJECT.BIG: result['damagedBaseObjects'],
         TYPE_TEAM_OBJECT.SMALL: result['damagedGroundObjects']}
        damagedPlanes = result['damagedPlanes']
        damagedGroundObjectsWithTurrets = {TYPE_TEAM_OBJECT.TURRET: result['damagedGroundObjectsWithTurrets']}
        killedObjects = {TYPE_TEAM_OBJECT.TURRET: result['killedTurrets'],
         TYPE_TEAM_OBJECT.BIG: result['killedBaseObjects'],
         TYPE_TEAM_OBJECT.SMALL: result['killedGroundObjects']}
        killedPlanes = result['killedPlanes']
        killedGroundObjectsWithTurrets = {TYPE_TEAM_OBJECT.TURRET: result['killedGroundObjectsWithTurrets']}
        generalSpottedList = []
        generalDamagedList = []
        for objectType, objectsCount in damagedObjects.items():
            self.__gatheringData(player, generalDamagedList, objectsCount, OBJECTS_INFO[objectType]['ICO_PATH'], OBJECTS_INFO[objectType]['LOC_ID'])

        for objectType, objectsCount in damagedGroundObjectsWithTurrets.iteritems():
            self.__gatheringData(player, generalDamagedList, objectsCount, OBJECTS_INFO[objectType]['ICO_PATH'], OBJECTS_INFO[TYPE_TEAM_OBJECT.SMALL]['LOC_ID'])

        for damagedPlaneID in damagedPlanes:
            generalDamagedList.extend(self.__getObjectInfo(player, avatarInfos, damagedPlaneID))

        generalKilledList = []
        for objectType, objectsCount in killedObjects.items():
            self.__gatheringData(player, generalKilledList, objectsCount, OBJECTS_INFO[objectType]['ICO_PATH'], OBJECTS_INFO[objectType]['LOC_ID'])

        for objectType, objectsCount in killedGroundObjectsWithTurrets.iteritems():
            self.__gatheringData(player, generalKilledList, objectsCount, OBJECTS_INFO[objectType]['ICO_PATH'], OBJECTS_INFO[TYPE_TEAM_OBJECT.SMALL]['LOC_ID'])

        for killedPlaneID in killedPlanes:
            generalKilledList.extend(self.__getObjectInfo(player, avatarInfos, killedPlaneID))

        if len(generalDamagedList) > 0:
            LOG_DEBUG('battleResult.addDamagedList', generalDamagedList)
        if len(generalKilledList) > 0:
            LOG_DEBUG('battleResult.generalKilledList', generalKilledList)
        if len(generalSpottedList) > 0:
            LOG_DEBUG('battleResult.generalSpottedList', generalSpottedList)
        generalHits = int(hitStructure + planeHits)
        generalReceived = int(ownHit)
        playerDataList = []
        assists = {}
        assistsGround = {}
        playersData = result['playersData']
        for playerData in playersData:
            assists[playerData['avatarID']] = playerData['assists']
            assistsGround[playerData['avatarID']] = playerData['assistsGround']

        for avatarID, avatarInfo in avatarInfos.items():
            settings = avatarInfo['settings']
            stats = avatarInfo.get('stats', None)
            if stats:
                playerDataMap = {'playerName': avatarInfo['playerName'],
                 'clanAbbrev': avatarInfo['clanAbbrev'],
                 'frags': stats['frags'],
                 'fragsTeamObjects': stats['fragsTeamObjects'],
                 'dead': stats['flags'] & AvatarFlags.DEAD != 0,
                 'lost': stats['flags'] & AvatarFlags.LOST != 0,
                 'aircraftName': localizeAirplane(settings.airplane.name),
                 'aircraftLevel': settings.airplane.level,
                 'aircraftType': settings.airplane.planeType,
                 'hudIcoPath': settings.airplane.hudIcoPath,
                 'screentPosition': int(avatarInfo['teamIndex'] != playerTeamID),
                 'amI': avatarID == player.id,
                 'squadID': avatarInfo['squadID'],
                 'squadType': SQUAD_TYPES.getSquadType(avatarInfo['squadID'], avatarID),
                 'assistsNum': str(assists[avatarID]),
                 'assistsGroundNum': str(assistsGround[avatarID])}
                playerDataList.append(playerDataMap)
                s = ''
                for key, value in playerDataMap.items():
                    if key == 'aircraftName':
                        value = settings.airplane.name
                    s = ''.join([s,
                     "'",
                     key,
                     "':",
                     str(value),
                     ' '])

                ClientLog.g_instance.gameplay(s)

        from HelperFunctions import multiKeySorting
        playerDataList = self.__marketAirplanesList = multiKeySorting(playerDataList, ['dead',
         '-aircraftLevel',
         'aircraftType',
         'aircraftName'])
        stat = 'missed'
        res = 'missed'
        if winState == 2:
            stat = localizeHUD('HUD_DRAW_STR')
            if gameResult == GAME_RESULT.DRAW_ELIMINATION:
                res = localizeHUD('HUD_DRAW_PLAYERS')
            elif gameResult == GAME_RESULT.DRAW_TIME_IS_RUNNING_OUT:
                res = localizeHUD('HUD_DRAW_TIME')
        else:
            isWinner = winState == 1
            stat = localizeHUD('HUD_WINNERS_STR') if isWinner else localizeHUD('HUD_LOOSERS_STR')
            res = str(gameResult)
            if gameResult == GAME_RESULT.ELIMINATION:
                res = localizeHUD('HUD_ENEMIES_ELIMINATION_STR') if isWinner else localizeHUD('HUD_OWN_ELIMINATION_STR')
            elif gameResult == GAME_RESULT.SUPERIORITY_SUCCESS:
                res = localizeHUD('HUD_WIN_SUPERIORITY_STR') if isWinner else localizeHUD('HUD_LOOSE_SUPERIORITY_STR')
        ownPlayerName = getPlayerNameWithClan(ownPlayerData['playerName'], ownPlayerData['clanAbbrev'])
        ownPlayerAirplaneName = localizeAirplane(ownPlayerData['settings'].airplane.name)
        ownPlayerDataStr = localizeBattleResults('BATTLERESULT_OWN_DATA').format(player=ownPlayerName.decode('utf-8'), vehicle=ownPlayerAirplaneName)
        killerPlayerDataResult = list()
        if killerID > 0:
            killerPlayerData = avatarInfos.get(killerID, None)
            if killerPlayerData:
                if lastDamageReason == DAMAGE_REASON.TERRAIN:
                    self.__battleResData.killedByTitle = localizeHUD('HUD_PLAYER_DEAD_FROM_GROUND')
                elif lastDamageReason == DAMAGE_REASON.WATER:
                    self.__battleResData.killedByTitle = localizeHUD('HUD_PLAYER_DEAD_FROM_WATER')
                elif lastDamageReason == DAMAGE_REASON.RAMMING:
                    self.__battleResData.killedByTitle = localizeHUD('UI_MESSAGE_YOU_FALL_ON_GROUND_TARGET')
                else:
                    self.__battleResData.killedByTitle = localizeHUD('HUD_PLAYER_DEAD_FROM_GROUND')
                if killerID != player.id:
                    self.__battleResData.killedByTitle = localizeBattleResults('BATTLERESULT_KILLER_NAME')
                    killerPlayerDataResult.extend(self.__getObjectInfo(player, avatarInfos, killerID))
            else:
                self.__battleResData.killedByTitle = localizeBattleResults('BATTLERESULT_KILLED_BY_TURRET')
                killerPlayerDataResult.extend((localizeHUD(OBJECTS_INFO[TYPE_TEAM_OBJECT.TURRET]['LOC_ID']), '', OBJECTS_INFO[TYPE_TEAM_OBJECT.TURRET]['ICO_PATH']))
        creditsStr = getStrValueWithFactor(int(playerCredits), int(playerCreditsCoeff))
        experienceStr = getStrValueWithFactor(int(playerExperience), int(playerXPCoeff))
        setattr(self.__battleResData, 'txtTitleAward', localizeLobby('MESSAGE_AWARD_NAME'))
        status = localizeHUD('HUD_GAME_RESULT_STR').format(s=stat, r=res)
        self.__battleResData.battleResult = status
        self.__battleResData.shots = str(planeShots)
        self.__battleResData.hits = str(generalHits)
        self.__battleResData.hitsTaken = str(generalReceived)
        self.__battleResData.credits = creditsStr
        self.__battleResData.experience = experienceStr
        self.__battleResData.infoPlayer = ownPlayerDataStr
        self.__battleResData.killedBy = killerPlayerDataResult
        self.__battleResData.killedPlayers = generalKilledList
        self.__battleResData.damagedPlayers = generalDamagedList
        self.__battleResData.spottedPlayers = generalSpottedList
        self.__battleResData.winState = winState
        if creditsPenalty or xpPenalty:
            self.__battleResData.txtPenaltyCredits = int(round(creditsPenalty, 1))
            self.__battleResData.txtPenaltyExperience = int(round(xpPenalty, 1))
        if creditsFromTK:
            self.__battleResData.txtCompensationCredits = int(round(creditsFromTK, 1))
        self.__battleResData.awards.extend((_AwardVO(localizeAchievements(AwardsDB[id].ui.name), AwardsDB[id].ui.icoPath) for id in result['gainedMedals']))
        LOG_DEBUG('battleResult.setResult: awards: {0}'.format([ i.name for i in self.__battleResData.awards ]), [status,
         creditsStr,
         experienceStr,
         ownPlayerDataStr,
         playerExperience,
         killerPlayerDataResult])
        ClientLog.g_instance.gameplay('Plane shots: %s, Plane hits: %s, Received hits: %s' % (planeShots, generalHits, generalReceived))
        LOG_TRACE('Preparation of results battle over.')
        return

    def __gatheringData(self, player, whereList, whatList, icoPath, objectType = False):
        whatSize = len(whatList)
        if whatSize > 0:
            whereList.extend((localizeHUD(objectType) if objectType else 'Unknown object', ''.join([' (x', str(whatSize), ')']), icoPath))

    def __getObjectInfo(self, player, avatarInfos, objectID):
        airplaneName = 'ERROR airplaneName'
        icoPath = 'ERROR icoPath'
        name = GameEnvironment.getClientArena().getObjectName(objectID)
        avatarInfo = avatarInfos.get(objectID, None)
        if avatarInfo:
            name = getPlayerNameWithClan(name, avatarInfo['clanAbbrev'] if 'clanAbbrev' in avatarInfo else '')
            settings = avatarInfo['settings']
            if settings:
                airplaneName = localizeAirplane(settings.airplane.name)
                icoPath = PLANE_TYPE_BATTLE_RESULT_ICO_PATH.icon(settings.airplane.planeType)
        return (name, ''.join(['(', airplaneName, ')']), icoPath)