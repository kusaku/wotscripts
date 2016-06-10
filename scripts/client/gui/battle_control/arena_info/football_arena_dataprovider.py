# Embedded file name: scripts/client/gui/battle_control/arena_info/football_arena_dataprovider.py
from constants import ARENA_GUI_TYPE, ARENA_BONUS_TYPE
from gui.battle_control import avatar_getter
from gui.battle_control.arena_info import arena_vos
from gui.battle_control.arena_info.ArenaDataProvider import ArenaDataProvider

class _FootballEventVehicleInteractiveStatsVO(arena_vos.VehicleArenaInteractiveStatsVO):
    __slots__ = ('goalsTimeLine', 'autoGoalsTimeLine')

    def __init__(self, vehicleID, xp = 0, damageDealt = 0, capturePts = 0, flagActions = None, winPoints = 0, deathCount = 0, resourceAbsorbed = 0, stopRespawn = False, equipmentDamage = 0, equipmentKills = 0, *args):
        super(_FootballEventVehicleInteractiveStatsVO, self).__init__(vehicleID, xp, damageDealt, capturePts, flagActions, winPoints, deathCount, resourceAbsorbed, stopRespawn, equipmentDamage, equipmentKills, *args)
        self.goalsTimeLine = []
        self.autoGoalsTimeLine = []

    def update(self, xp = 0, damageDealt = 0, capturePts = 0, flagActions = None, winPoints = 0, deathCount = 0, resourceAbsorbed = 0, stopRespawn = False, equipmentDamage = 0, equipmentKills = 0, *args):
        self.goalsTimeLine, self.autoGoalsTimeLine, assistTimeLine = args
        return super(_FootballEventVehicleInteractiveStatsVO, self).update(xp, damageDealt, capturePts, flagActions, winPoints, deathCount, resourceAbsorbed, stopRespawn, equipmentDamage, equipmentKills, *args)


class _FootballVehicleArenaInteractiveStatsDict(arena_vos.VehicleArenaInteractiveStatsDict):

    def __missing__(self, key):
        self[key] = value = _FootballEventVehicleInteractiveStatsVO(key)
        return value


class FootballArenaDataProvider(ArenaDataProvider):

    def __init__(self, avatar = None):
        super(FootballArenaDataProvider, self).__init__(avatar)
        self._viStatsVOs = _FootballVehicleArenaInteractiveStatsDict()
        self.__scoresByTeamId = {}
        self.__scores = (0, 0)
        self.__ballPossession = None
        self.__penaltyPoints = None
        self.__lastGoal = None
        self.__autoGoals = (0, 0)
        self.__goals = (0, 0)
        return

    def buildStatsData(self, stats):
        super(FootballArenaDataProvider, self).buildStatsData(stats)
        self.__calcScore()

    def updateVehicleStats(self, vID, vStats):
        stats = super(FootballArenaDataProvider, self).updateVehicleStats(vID, vStats)
        self.__calcScore()
        return stats

    def getScores(self):
        return self.__scores

    def getScoresByTeamId(self):
        return self.__scoresByTeamId

    def getBallPossession(self):
        return self.__ballPossession

    def getPenaltyPoints(self):
        return self.__penaltyPoints

    def getLastGoal(self):
        return self.__lastGoal

    def updateFootballPenaltyPoints(self, data):
        """
        Data possession points handler for Football Event
        :param data: dict -{
            'ballPossession': ball possessions in main time,
            'penaltyPoints': penalty points in overtime period (there was no winner in match)
        }
        """
        self.__ballPossession = self.__calcPoints(data.get('ballPossession'))
        self.__penaltyPoints = self.__calcPoints(data.get('penaltyPoints'))

    def _findSquads(self, arenaGuiType, exclude = None):
        if arenaGuiType == ARENA_GUI_TYPE.EVENT_BATTLES and avatar_getter.getArena().bonusType == ARENA_BONUS_TYPE.TOURNAMENT_EVENT:
            return []
        return super(FootballArenaDataProvider, self)._findSquads(arenaGuiType, exclude)

    def __calcScore(self):
        if self.isRequiredDataExists() or self.getAllyTeams()[0]:
            allyScore, enemyScore = (0, 0)
            allyGoals, enemyGoals = (0, 0)
            allyAutoGoals, enemyAutoGoals = (0, 0)
            for vInfoVO, vStatsVO, viStatsVO in self.getAllVehiclesIterator():
                score = vStatsVO.frags
                goals = score & 3
                autogoals = score >> 2
                if self.isEnemyTeam(vInfoVO.team):
                    enemyScore += goals
                    allyScore += autogoals
                    enemyAutoGoals += autogoals
                    enemyGoals += goals
                else:
                    allyScore += goals
                    enemyScore += autogoals
                    allyAutoGoals += autogoals
                    allyGoals += goals

            myTeamId = self.getAllyTeams()[0]
            enemyTeamId = self.getEnemyTeams()[0]
            if allyGoals - self.__goals[0] > 0:
                self.__lastGoal = (myTeamId, enemyTeamId)
            elif enemyGoals - self.__goals[1] > 0:
                self.__lastGoal = (enemyTeamId, myTeamId)
            elif allyAutoGoals - self.__autoGoals[0] > 0:
                self.__lastGoal = (myTeamId, myTeamId)
            elif enemyAutoGoals - self.__autoGoals[1] > 0:
                self.__lastGoal = (enemyTeamId, enemyTeamId)
            self.__autoGoals = (allyAutoGoals, enemyAutoGoals)
            self.__goals = (allyGoals, enemyGoals)
            self.__scores = (allyScore, enemyScore)
            for arenaTeamId in self.getTeamsOnArena():
                self.__scoresByTeamId[arenaTeamId] = enemyScore if self.isEnemyTeam(arenaTeamId) else allyScore

    def __calcPoints(self, points):
        if not points:
            return None
        else:
            arena_teams = self.getTeamsOnArena()
            raise len(arena_teams) == 2 or AssertionError('Invalid teams count: %s. Only 2 teams must be on Football Arena!' % len(arena_teams))
            ally = 0
            enemy = 0
            for team in arena_teams:
                value = points[team]
                if self.isEnemyTeam(team):
                    enemy += value
                else:
                    ally += value

            return (ally, enemy)