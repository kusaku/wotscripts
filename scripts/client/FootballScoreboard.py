# Embedded file name: scripts/client/FootballScoreboard.py
import BigWorld
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_ERROR
from gui.battle_control.arena_info.interfaces import IArenaVehiclesController
from gui.battle_control import g_sessionProvider

class FootballScoreboard(BigWorld.Entity, IArenaVehiclesController):
    BLUE_PANEL, RED_PANEL = (0, 1)

    def __init__(self):
        BigWorld.Entity.__init__(self)
        self.__scoreboardModel = None
        self.__numberPanels = []
        self.__arenaDP = None
        self.__score = {FootballScoreboard.BLUE_PANEL: 0,
         FootballScoreboard.RED_PANEL: 0}
        return

    def prerequisites(self):
        return [self.modelName, self.modelNameForDigitPanel, self.modelNameForDigitPanel]

    def onEnterWorld(self, prereqs):
        try:
            self.__loadModels(prereqs)
        except Exception:
            LOG_CURRENT_EXCEPTION()

        g_sessionProvider.addArenaCtrl(self)
        self.__arenaDP = g_sessionProvider.getArenaDP()
        self.__initGoalInfo()

    def onLeaveWorld(self):
        self.__arenaDP = None
        g_sessionProvider.removeArenaCtrl(self)
        del self.__numberPanels[:]
        self.__scoreboardModel = None
        return

    def collideSegment(self, startPoint, endPoint, skipGun = False):
        pass

    def invalidateStats(self, arenaDP):
        self.__invalidateScore()

    def invalidateVehicleStats(self, flags, vo, arenaDP):
        self.__invalidateScore()

    def __invalidateScore(self):
        goalInfo = self.__getGoalInfo()
        if goalInfo is None:
            return
        else:
            team1_goals, team2_goals = goalInfo
            if self.__score[FootballScoreboard.RED_PANEL] != team1_goals:
                self.__playDigitAnimation(FootballScoreboard.RED_PANEL, team1_goals)
                self.__score[FootballScoreboard.RED_PANEL] = team1_goals
            if self.__score[FootballScoreboard.BLUE_PANEL] != team2_goals:
                self.__playDigitAnimation(FootballScoreboard.BLUE_PANEL, team2_goals)
                self.__score[FootballScoreboard.BLUE_PANEL] = team2_goals
            return

    def __loadModels(self, prereqs):
        firstModel = True
        hpIndex = 0
        for modelName in prereqs.keys():
            if modelName in prereqs.failedIDs:
                LOG_ERROR('Failed to load football scoreboard model: %s' % modelName)
                continue
            model = prereqs[modelName]
            if firstModel:
                firstModel = False
                model.addMotor(BigWorld.Servo(self.matrix))
                model.castsShadow = False
                self.addModel(model)
                self.__scoreboardModel = model
            else:
                hardPoint = self.__scoreboardModel.node('HP_module_%d' % hpIndex)
                hardPoint.attach(model)
                hpIndex += 1
                self.__numberPanels.append(model)

    def __switchToStaticAnimation(self, panel, digit):
        try:
            animAction = self.__numberPanels[panel].action('scoreboard_table_static_%d_action' % digit)
            animAction()
        except Exception:
            LOG_CURRENT_EXCEPTION()

    def __playDigitAnimation(self, panel, digitToSwitch):
        try:
            animAction = self.__numberPanels[panel].action('scoreboard_table_change_%d_action' % digitToSwitch)
            animAction().action('scoreboard_table_static_%d_action' % digitToSwitch)()
        except Exception:
            LOG_CURRENT_EXCEPTION()

    def __getGoalsData(self):
        if self.__arenaDP is None:
            return
        else:
            return self.__arenaDP.getScoresByTeamId()

    def __getGoalInfo(self):
        data_vo = self.__getGoalsData()
        if data_vo is None:
            return
        else:
            team1_goals = data_vo[1]
            team2_goals = data_vo[2]
            return (team1_goals, team2_goals)

    def __initGoalInfo(self):
        goalInfo = self.__getGoalInfo()
        if goalInfo is None:
            return
        else:
            team1_goals, team2_goals = goalInfo
            self.__switchToStaticAnimation(FootballScoreboard.RED_PANEL, team1_goals)
            self.__switchToStaticAnimation(FootballScoreboard.BLUE_PANEL, team2_goals)
            self.__score[FootballScoreboard.RED_PANEL] = team1_goals
            self.__score[FootballScoreboard.BLUE_PANEL] = team2_goals
            return