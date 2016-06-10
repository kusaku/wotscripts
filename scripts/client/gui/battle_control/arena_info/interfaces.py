# Embedded file name: scripts/client/gui/battle_control/arena_info/interfaces.py
from gui.battle_control.arena_info.settings import ARENA_LISTENER_SCOPE as _SCOPE

class IArenaController(object):
    """
    Interface of GUI controller to displays information of vehicles in
    each team on arena.
    """
    __slots__ = ('__weakref__',)

    def getCtrlScope(self):
        raise NotImplementedError('Routine "getCtrlScope" must be implemented')

    def clear(self):
        pass

    def setBattleCtx(self, battleCtx):
        """
        Sets battle context.
        :param battleCtx: instance of BattleContext or None
        """
        pass


class IArenaLoadController(IArenaController):
    __slots__ = ()

    def getCtrlScope(self):
        return _SCOPE.LOAD

    def spaceLoadStarted(self):
        """
        Arena space loading started
        """
        pass

    def spaceLoadCompleted(self):
        """
        Arena space loading completed
        """
        pass

    def updateSpaceLoadProgress(self, progress):
        """
        Arena space loading progress has been changed
        @param progress: [float] progress value
        :param progress:
        """
        pass

    def arenaLoadCompleted(self):
        """
        Arena space loading completed and influx draw enabled. This event
        means arena is ready to be shown.
        """
        pass


class IArenaVehiclesController(IArenaLoadController):
    __slots__ = ()

    def getCtrlScope(self):
        return _SCOPE.VEHICLES | _SCOPE.LOAD

    def invalidateArenaInfo(self):
        """
        Starts to invalidate information of arena.
        :return:
        """
        pass

    def invalidateVehiclesInfo(self, arenaDP):
        """
        New list of vehicles has been received.
        :param arenaDP: instance of ArenaDataProvider.
        """
        pass

    def invalidateStats(self, arenaDP):
        """
        New statistics (frags) has been received.
        :param arenaDP: instance of ArenaDataProvider.
        """
        pass

    def addVehicleInfo(self, vo, arenaDP):
        """
        New vehicle added to arena.
        :param vo: instance of VehicleArenaInfoVO that has been added.
        :param arenaDP: instance of ArenaDataProvider.
        :return:
        """
        pass

    def invalidateVehicleInfo(self, flags, vo, arenaDP):
        """
        Vehicle has been updated on arena.
        :param flags: bitmask containing values from INVALIDATE_OP.
        :param vo: instance of VehicleArenaInfoVO that has been updated.
        :param arenaDP:
        :return: instance of ArenaDataProvider.
        """
        pass

    def invalidateVehicleStatus(self, flags, vo, arenaDP):
        """
        Status of vehicle (isReady, isAlive, ...) has been updated on arena.
        :param flags: bitmask containing values from INVALIDATE_OP.
        :param vo: instance of VehicleArenaInfoVO for that status updated.
        :param arenaDP: instance of ArenaDataProvider.
        """
        pass

    def invalidateVehicleStats(self, flags, vo, arenaDP):
        """
        Statistics of vehicle has been updated on arena.
        Updates required player's panel, frags panel.
        :param flags: bitmask containing values from INVALIDATE_OP.
        :param vo: instance of VehicleArenaStatsVO.
        :param arenaDP: instance of ArenaDataProvider.
        """
        pass

    def invalidatePlayerStatus(self, flags, vo, arenaDP):
        """
        Status of player (isTeamKiller, ...) has been updated on arena.
        :param flags: bitmask containing values from INVALIDATE_OP.
        :param vo: instance of VehicleArenaInfoVO for that status updated.
        :param arenaDP: instance of ArenaDataProvider.
        """
        pass

    def invalidateUsersTags(self):
        """
        New list of chat rosters has been received.
        """
        pass

    def invalidateUserTags(self, user):
        """
        Chat rosters has been changed.
        :param user: instance of UserEntity.
        """
        pass

    def invalidateVehicleInteractiveStats(self):
        """
        Statistics of interactives has been updated on arena.
        Updates required flags pannel.
        """
        pass

    def invalidateFootballPenaltyPoints(self, data):
        """
        :param data: dict, contains information of ball possession {'ballPossession': [team0, team1, team2]}
        In overtime period data extends by information: 'penaltyPoints': [team0, team1, team2]
        """
        pass


class ITeamsBasesController(IArenaController):
    __slots__ = ()

    def getCtrlScope(self):
        return _SCOPE.TEAMS_BASES

    def invalidateTeamBasePoints(self, baseTeam, baseID, points, timeLeft, invadersCnt, capturingStopped):
        """
        Adds/Updates indicator for base that is capturing in UI.
        :param baseTeam: number of base's team.
        :param baseID: integer containing unique ID of base.
        :param points: integer containing value of points (0 ... 100).
        :param timeLeft: time left until base will be captured
        :param invadersCnt: count of invaders
        :param capturingStopped: is capture stopped.
        :return:
        """
        pass

    def invalidateTeamBaseCaptured(self, baseTeam, baseID):
        """
        Team base has been captured.
        :param baseTeam: number of base's team.
        :param baseID: integer containing unique ID of base.
        """
        pass

    def removeTeamsBases(self):
        """
        Removes all teams bases.
        """
        pass


class IArenaPeriodController(IArenaController):
    __slots__ = ()

    def getCtrlScope(self):
        return _SCOPE.PERIOD

    def setPeriodInfo(self, period, endTime, length, additionalInfo, soundID):
        """
        Sets current time metrics that takes from the ClientArena.
        :param period: integer containing one of the ARENA_PERIOD.* values.
        :param endTime: float containing server time of the period end.
        :param length: float containing period length.
        :param additionalInfo: arena additional info, @see ClientArena.
        :param soundID: string containing path to the sound of countdown timer.
        """
        pass

    def invalidatePeriodInfo(self, period, endTime, length, additionalInfo):
        """
        Time metrics has been updated by server.
        :param period: integer containing one of the ARENA_PERIOD.* values.
        :param endTime: float containing server time of the period end.
        :param length: float containing period length.
        :param additionalInfo: PeriodAdditionalInfo
        """
        pass


class IArenaRespawnController(IArenaController):
    __slots__ = ()

    def getCtrlScope(self):
        return _SCOPE.RESPAWN

    def updateSpaceLoadProgress(self, progress):
        """
        Arena space loading progress has been changed.
        :param progress: [float] progress value.
        :return:
        """
        pass

    def arenaLoadCompleted(self):
        """
        Arena space loading completed and influx draw enabled. This event
        means arena is ready to be shown.
        """
        pass

    def updateRespawnVehicles(self, vehsList):
        """
        Arena received list of vehicles, available for respawns.
        :param vehsList: list of vehicles.
        """
        pass

    def updateRespawnCooldowns(self, cooldowns):
        """
        Arena received list of cooldowns for respawns.
        :param cooldowns: list of cooldowns
        """
        pass

    def updateRespawnInfo(self, respawnInfo):
        """
        Arena received respawn info.
        :param respawnInfo:
        """
        pass

    def updateRespawnRessurectedInfo(self, respawnInfo):
        """
        Arena received respawn ressurected info.
        :param respawnInfo:
        """
        pass


class IPersonalInvitationsController(IArenaVehiclesController):
    __slots__ = ()

    def getCtrlScope(self):
        return _SCOPE.VEHICLES | _SCOPE.INVITATIONS

    def invalidateInvitationsStatuses(self, vos, arenaDP):
        pass


class IVehiclesAndPositionsController(IArenaVehiclesController):
    __slots__ = ()

    def getCtrlScope(self):
        return _SCOPE.VEHICLES | _SCOPE.POSITIONS

    def updatePositions(self, iterator):
        pass