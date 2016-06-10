# Embedded file name: scripts/client/FootballManager.py
import functools
import BigWorld
import Math
import WWISE
import SoundGroups
import ResMgr
import Event
from gui.battle_control.arena_info.interfaces import IArenaVehiclesController
from gui.battle_control import g_sessionProvider
from DetachedTurret import _TurretDetachmentEffects
from helpers.bound_effects import ModelBoundEffects
from debug_utils import LOG_ERROR
from vehicle_systems import assembly_utility
from helpers import newFakeModel
from helpers.EffectsList import SpecialKeyPointNames, SoundStartParam
from helpers.EffectsList import effectsFromSection, EffectsListPlayer
from helpers.CallbackDelayer import CallbackDelayer
from MapActivities import startActivity
from constants import ARENA_PERIOD
_DYNAMIC_OBJECTS_CONFIG_FILE = 'scripts/dynamic_objects.xml'
_gFootbalManager = None

def getFootbalManager():
    global _gFootbalManager
    if _gFootbalManager is None:
        _gFootbalManager = FootballManager()
    return _gFootbalManager


def addGlobalModel(model):
    BigWorld.player().addModel(model)


def delGlobalModel(model):
    BigWorld.player().delModel(model)


class _BallHitEffects(ModelBoundEffects, assembly_utility.Component):
    _BALL_HIT_EFFECT = 'ballHit'

    def showHit(self, attackerID, shotPoint, effectsIndex):
        effects = _gFootbalManager.effectsCache.get(_BallHitEffects._BALL_HIT_EFFECT, None)
        if effects is None:
            LOG_ERROR('Cannot find ball hit effect')
            return
        else:
            self.addNew(shotPoint.matrix, effects.effectsList, effects.keyPoints, showDecal=False, attackerID=attackerID)
            return


class _BallPullEffects(_TurretDetachmentEffects):

    def __init__(self, turretModel, detachmentEffectsDesc, onGround):
        super(_BallPullEffects, self).__init__(turretModel, detachmentEffectsDesc, onGround)
        self.ballSoundObject = SoundGroups.g_instance.WWgetSoundObject('ballObject', turretModel.matrix, (0.0, 0.0, 0.0))

    def destroy(self):
        self.ballSoundObject.stopAll()
        self.ballSoundObject = None
        return

    def notifyAboutCollision(self, energy, collisionPoint, effectMaterialIdx, groundEffect, underWater):
        if groundEffect:
            stages, effectsList, _ = self._TurretDetachmentEffects__detachmentEffectsDesc['collision'][effectMaterialIdx]
            dropEnergyParam = SoundStartParam('RTPC_ext_ev_football_drop_energy', energy)
            BigWorld.player().terrainEffects.addNew(collisionPoint, effectsList, stages, None, soundParams=(dropEnergyParam,), soundObject=self.ballSoundObject)
        super(_BallPullEffects, self).notifyAboutCollision(energy, collisionPoint, effectMaterialIdx, None, underWater)
        return


class BallToVehicleCollider(assembly_utility.Component):

    def __init__(self, ballSoundObject):
        self.__ballSoundObject = ballSoundObject

    def notifyAboutCollision(self, energy, point, normal):
        self.__ballSoundObject.setRTPC('RTPC_ext_ev_football_drop_energy', energy)
        self.__ballSoundObject.play('ev_collision_with_ball')


def _footballMgrSelfDestroy(finalizer, ball):
    global _gFootbalManager
    finalizer()
    g_sessionProvider.removeArenaCtrl(_gFootbalManager)
    _gFootbalManager.destroy()
    _gFootbalManager = None
    ball.onLeaveWorld = finalizer
    return


def assemblyBall(ball):
    ball.turretHitEffects = _BallHitEffects(ball.model)
    turretDescr = ball._DetachedTurret__vehDescr.turret
    ball.detachmentEffects = _BallPullEffects(ball.model, turretDescr['turretDetachmentEffects'], ball.isCollidingWithWorld == 1)
    ball.vehicleCollisionEffects = BallToVehicleCollider(ball.detachmentEffects.ballSoundObject)
    ball.onGoal = functools.partial(getFootbalManager().onGoal)
    g_sessionProvider.addArenaCtrl(_gFootbalManager)
    getFootbalManager().start(ball, g_sessionProvider.getArenaDP())
    ball.onLeaveWorld = functools.partial(_footballMgrSelfDestroy, ball.onLeaveWorld, ball)


class FootballManager(IArenaVehiclesController):
    effectsCache = property(lambda self: self.__effects)

    def __init__(self):
        self.__ballEntity = None
        self.__callbackID = None
        self.__footballCellPos = Math.Vector3(0, 0, 0)
        self.__gates = {}
        self.__effects = dict()
        self.__ballDestroyEffectDelay = None
        self.__configRead()
        self.__playerTeam = 0
        self.__arenaDP = None
        self.__prevArenaPeriod = ARENA_PERIOD.IDLE
        self.onDestroyBall = Event.Event()
        self.onRespwnBall = Event.Event()
        self.onBallInited = Event.Event()
        return

    def start(self, entity, arenaDP):
        self.__arenaDP = arenaDP
        self.__footballCellPos = Math.Vector3(0, 0, 0)
        self.__ballEntity = entity
        self.__playerTeam = BigWorld.player().team
        self.__initGatesPositions()
        self.__prevArenaPeriod = BigWorld.player().arena.period
        BigWorld.player().arena.onPeriodChange += self.__arenaPeriodChanged
        self.__ballEntity.ballDecal = _DefferredBallDecal(self.__ballEntity, self.__configSection) if not BigWorld.isForwardPipeline() else _ForwardBallDecal(self.__ballEntity, self.__configSection)
        self.__ballEntity.addComponent(self.__ballEntity.ballDecal)
        self.__tick()
        self.onBallInited()

    def destroy(self):
        BigWorld.player().arena.onPeriodChange -= self.__arenaPeriodChanged
        self.onDestroyBall.clear()
        self.onRespwnBall.clear()
        self.onBallInited.clear()
        self.__cancelTick()
        self.__ballEntity = None
        self.__arenaDP = None
        self.__gates = {}
        return

    def invalidateStats(self, arenaDP):
        self.__invalidateScore()

    _GOAL_ACTIVITIES = ['autogoalToRed',
     'goalToRed',
     'goalToBlue',
     'autogoalToBlue']

    def invalidateVehicleStats(self, flags, vo, arenaDP):
        self.__invalidateScore()
        teamFrom, teamTo = self.__arenaDP.getLastGoal()
        activityName = FootballManager._GOAL_ACTIVITIES[teamFrom - 1 + (teamTo - 1 << 1)]
        startActivity(activityName)

    def __invalidateScore(self):
        ally, enemy = self.__arenaDP.getScores()
        WWISE.WW_setRTCPGlobal('RTPC_ext_football_score_ally', ally)
        WWISE.WW_setRTCPGlobal('RTPC_ext_football_score_enemy', enemy)

    def __configRead(self):
        dynamicObjectsSection = ResMgr.openSection(_DYNAMIC_OBJECTS_CONFIG_FILE)
        raise 'footballBattle' in dynamicObjectsSection.keys() or AssertionError
        self.__configSection = dynamicObjectsSection['footballBattle']
        effectsSection = self.__configSection['footballEffects']
        if effectsSection is not None:
            for item in effectsSection.items():
                self.__effects[item[0]] = effectsFromSection(item[1])

        self.__ballDestroyEffectDelay = self.__configSection['ballDestroyEffectDelay'].asFloat
        return

    def __arenaPeriodChanged(self, period, periodEndTime, periodLength, periodAdditionalInfo):
        if self.__prevArenaPeriod == ARENA_PERIOD.PREBATTLE and period == ARENA_PERIOD.BATTLE:
            SoundGroups.g_instance.playSound2D('ev_football_whistle')
        self.__prevArenaPeriod = period

    @staticmethod
    def isFootballBattle():
        player = BigWorld.player()
        arena = getattr(player, 'arena', None)
        if arena is None:
            return False
        else:
            arenaType = getattr(arena, 'arenaType', None)
            if arenaType is None:
                return False
            footballCell = getattr(arenaType, 'footballCell', None)
            return footballCell is not None

    def __initGatesPositions(self):
        arenaType = BigWorld.player().arena.arenaType
        footballCell = arenaType.footballCell
        self.__footballCellPos = Math.Vector3(footballCell['position'])
        teamBasePositions = arenaType.teamBasePositions
        for team, teamBasePoints in enumerate(teamBasePositions, 1):
            for base, basePoint in teamBasePoints.items():
                pos = Math.Vector3(basePoint[0], self.__footballCellPos.y, basePoint[1])
                self.__gates[team] = pos

    def __tick(self):
        self.__callbackID = None
        self.__update()
        self.__callbackID = BigWorld.callback(0.1, self.__tick)
        return

    def __cancelTick(self):
        if self.__callbackID is not None:
            BigWorld.cancelCallback(self.__callbackID)
            self.__callbackID = None
        return

    def __update(self):
        self.__updateSoundParams()

    def __updateSoundParams(self):
        ourGatePos = self.__gates[self.__playerTeam]
        oppositeGatePos = self.__gates[3 - self.__playerTeam]
        playerVehicle = BigWorld.player().vehicle
        if playerVehicle is not None:
            vehiclePos = playerVehicle.position
            toOurGateDist = (ourGatePos - vehiclePos).lengthSquared
            toOppositeGateDist = (oppositeGatePos - vehiclePos).lengthSquared
            sidePlayerParam = 0 if toOurGateDist < toOppositeGateDist else 1
            WWISE.WW_setRTCPGlobal('RTPC_ext_ev_football_side_player', sidePlayerParam)
        ballPos = self.__ballEntity.position
        fromBallToOurGateDist = (ourGatePos - ballPos).length
        fromBallToOppositeGateDist = (oppositeGatePos - ballPos).length
        sideBallParam = 0 if fromBallToOurGateDist < fromBallToOppositeGateDist else 1
        WWISE.WW_setRTCPGlobal('RTPC_ext_ev_football_side_ball', sideBallParam)
        WWISE.WW_setRTCPGlobal('RTPC_ext_ev_football_distance_from_the_ball_gate_PC', fromBallToOurGateDist)
        WWISE.WW_setRTCPGlobal('RTPC_ext_ev_football_distance_from_the_ball_gate_NPC', fromBallToOppositeGateDist)
        return

    def onGoal(self, team):
        if team == self.__playerTeam:
            WWISE.WW_eventGlobal('ev_football_goal_in_enemy_gate')
        else:
            WWISE.WW_eventGlobal('ev_football_goal_in_our_gate')
        if self.__ballDestroyEffectDelay is not None:
            BigWorld.callback(self.__ballDestroyEffectDelay, self.__playBallDestroyEffect)
        else:
            self.__playBallDestroyEffect()
        return

    def onBallHit(self):
        effects = self.__effects.get('ballHit', None)
        if self.__ballEntity.model is not None and effects is not None:
            effectsPlayer = EffectsListPlayer(effects.effectsList, effects.keyPoints)
            effectsPlayer.play(self.__ballEntity.model, SpecialKeyPointNames.START)
        return

    def __playBallDestroyEffect(self):
        effects = self.__effects.get('ballDestruction', None)
        if self.__ballEntity.model is not None and effects is not None:
            self.__ballEntity.model.visible = False
            self.__ballEntity.ballDecal.show(False)
            BigWorld.player().terrainEffects.addNew(self.__ballEntity.model.position, effects.effectsList, effects.keyPoints, self.__respawnBall)
            self.onDestroyBall()
        return

    def __respawnBall(self):
        if self.__ballEntity is not None:
            self.__ballEntity.model.visible = True
            self.__ballEntity.ballDecal.show(True)
            self.__playRespawnBallEffect()
        return

    def __playRespawnBallEffect(self):
        if self.__ballEntity is None or self.__ballEntity.model is None:
            return
        else:
            effects = self.__effects.get('ballRespawn', None)
            if effects is None:
                return
            self.onRespwnBall()
            BigWorld.player().terrainEffects.addNew(self.__ballEntity.model.position, effects.effectsList, effects.keyPoints, None)
            return

    def __getLastGoalInfo(self):
        lastGoalTime = 0
        goalTeam = 0
        isAutoGoal = False
        for vInfoVO, vStatsVO, viStatsVO in self.__arenaDP.getAllVehiclesIterator():
            for goalTime in reversed(viStatsVO.goalsTimeLine):
                if goalTime > lastGoalTime:
                    lastGoalTime = goalTime
                    goalTeam = vInfoVO.team
                    isAutoGoal = False

            for goalTime in reversed(viStatsVO.autoGoalsTimeLine):
                if goalTime > lastGoalTime:
                    lastGoalTime = goalTime
                    goalTeam = vInfoVO.team
                    isAutoGoal = True

        return (goalTeam, isAutoGoal)


class IBallDecal(assembly_utility.Component):

    def show(self, doShow):
        raise NotImplementedError()


class _DefferredBallDecal(IBallDecal):

    def __init__(self, ballEntity, cfg):
        super(_DefferredBallDecal, self).__init__()
        self.__fakeModel = newFakeModel()
        addGlobalModel(self.__fakeModel)
        translationMProv = Math.WGTranslationOnlyMP()
        translationMProv.source = ballEntity.matrix
        self.__fakeModel.addMotor(BigWorld.Servo(translationMProv))
        raise 'footballDecalDeferred' in cfg.keys() or AssertionError
        decalTex = cfg['footballDecalDeferred'].asString
        self.__decal = self.__createDecal(self.__fakeModel.root, decalTex)

    def show(self, show):
        if show:
            if self.__decal is not None and not self.__decal.inWorld:
                self.__fakeModel.root.attach(self.__decal)
        elif self.__decal is not None and self.__decal.inWorld:
            self.__fakeModel.root.detach(self.__decal)
        return

    def destroy(self):
        self.__decal = None
        delGlobalModel(self.__fakeModel)
        return

    @staticmethod
    def __createDecal(parentNode, addTex, applyToAll = False):
        priority = 0
        materialType = 7
        influence = 18
        if applyToAll:
            influence = 62
        transform = Math.Matrix()
        transform.setScale(Math.Vector3(3, 3, 3))
        transform.translation = (0.0, -0.5, 0.0)
        decal = BigWorld.WGShadowForwardDecal()
        decal.setup(addTex, materialType, priority, influence)
        decal.setLocalTransform(transform)
        decal.collideWithScene(True)
        parentNode.attach(decal)
        return decal


class _ForwardBallDecal(IBallDecal, CallbackDelayer):

    def __init__(self, ballEntity, cfg):
        IBallDecal.__init__(self)
        CallbackDelayer.__init__(self)
        self.__ballEntity = ballEntity
        self.__fakeModel = None
        self.__matrix = None
        self.__terrainSelectedArea = None
        raise 'footballDecalForward' in cfg.keys() or AssertionError
        section = cfg['footballDecalForward']
        self.__decalModel = section['model'].asString
        self.__decalSize = section['size'].asFloat
        self.__overTerrainHeight = section['overTerrainHeight'].asFloat
        self.__maxTerrainHeight = section['maxTerrainHeight'].asFloat
        self.__createTerrainSelectedArea(self.__decalModel, self.__decalSize, self.__overTerrainHeight, self.__maxTerrainHeight)
        self.delayCallback(0.0, self.__update)
        return

    def destroy(self):
        CallbackDelayer.destroy(self)
        self.__destroyTerrainSelectedArea()
        self.__ballEntity = None
        return

    def show(self, doShow):
        if doShow:
            if self.__terrainSelectedArea is None:
                self.__createTerrainSelectedArea(self.__decalModel, self.__decalSize, self.__overTerrainHeight, self.__maxTerrainHeight)
        else:
            self.__destroyTerrainSelectedArea()
        return

    def __createTerrainSelectedArea(self, modelName, size, overTerrainHeight, maxTerrainHeight):
        color = 4294967295L
        terrainSelected = True
        self.__fakeModel = BigWorld.Model('objects/fake_model.model')
        self.__fakeModel.position = self.__ballEntity.position
        addGlobalModel(self.__fakeModel)
        self.__matrix = Math.Matrix(self.__fakeModel.matrix)
        self.__fakeModel.addMotor(BigWorld.Servo(self.__matrix))
        rootNode = self.__fakeModel.node('')
        self.__terrainSelectedArea = BigWorld.PyTerrainSelectedArea()
        self.__terrainSelectedArea.setup(modelName, Math.Vector2(size, size), overTerrainHeight, color, terrainSelected)
        self.__terrainSelectedArea.enableAccurateCollision(True)
        self.__terrainSelectedArea.setMaxTerrainHeight(maxTerrainHeight)
        rootNode.attach(self.__terrainSelectedArea)

    def __destroyTerrainSelectedArea(self):
        self.__matrix = None
        if self.__fakeModel is not None:
            delGlobalModel(self.__fakeModel)
            self.__fakeModel = None
        self.__terrainSelectedArea = None
        return

    def __update(self):
        if self.__matrix is None:
            return 0.0
        else:
            self.__matrix.setIdentity()
            self.__matrix.translation = self.__ballEntity.position
            if self.__terrainSelectedArea is not None:
                self.__terrainSelectedArea.updateHeights()
            return 0.0