# Embedded file name: scripts/client/audio/GameSoundImpl.py
import BigWorld
from SoundObjects import Music, UI, Voiceover, TurretSoundObjectsFactories, AircraftSoundObjectsFactories
from WWISE_ import setVolumeAmp, setReplayMute, setCurrentLanguage
from audio.SoundBanksManager import SoundBanksManager
from Event import Event, EventManager
from consts import GAME_MODE, GAME_RESULT, ARENA_TYPE
import db.DBLogic
from _preparedBattleData_db import preparedBattleData
import modelManipulator.ModelManipulator3
import modelManipulator.CompoundBuilder
import GameEnvironment
from EntityHelpers import EntityStates
from EntityHelpers import extractGameMode, isAvatar
import BattleReplay
from AKTunes import Arena_Banks, RTPC_Altitude_Update_Freq
from AKConsts import SPEEDOMETER_MAX_SPEED_IDX, SPEEDOMETER_DATA_SIZE, INIT_BANK_NAME, WEAPONS_BANK_NAME, SOUND_CASES
from debug_utils import LOG_INFO, LOG_WARNING
from DopplerEffect import DopplerEffect
from InteractiveMix import InteractiveMixHandler

class GameSoundImpl():

    def __init__(self):
        self.__soundBanksManager = SoundBanksManager.instance()
        self.__initPackages()
        self.__soundBanksManager.loadInitBank(INIT_BANK_NAME)
        self.__voice = None
        self.__music = Music()
        self.__ui = UI()
        self.__interactiveMix = InteractiveMixHandler()
        self.__prevTarget = None
        self.__burning = {}
        self.__disconnected = True
        self.__isReplayMute = False
        self.__winner = False
        self.__draw = False
        self.__em = EventManager()
        self.eOnBattleStart = Event(self.__em)
        self.eOnBattleEnd = Event(self.__em)
        self.eOnStallDanger = Event(self.__em)
        self.eLoadingScreenClosed = Event(self.__em)
        return

    def __initPackages(self):
        self.__soundBanksManager.loadFilePackage('ambient')
        self.__soundBanksManager.loadFilePackage('common')
        self.__soundBanksManager.loadFilePackage('engines')
        self.__soundBanksManager.loadFilePackage('music')
        self.__soundBanksManager.loadFilePackage('ui')
        self.__soundBanksManager.loadFilePackage('weapons')
        self.__soundBanksManager.loadFilePackage('hangar_pearl')
        self.__soundBanksManager.loadFilePackage('hangars')

    def cache(self, objDBData, objectBuilder, context, isPlayer, soundObjects, weaponSoundID, turretSoundID):
        if weaponSoundID is None:
            weaponSoundID = []
        info = db.DBLogic.g_instance.getAircraftSound(objDBData.name)
        if info is None and turretSoundID is None:
            return
        else:
            partByNames = {}
            modelParts = objDBData.partsSettings.getPartsOnlyList()
            for partDb in modelParts:
                partByNames[partDb.name] = partDb

            data = {'modelManipulator': modelManipulator,
             'objectBuilder': objectBuilder,
             'info': info,
             'partByNames': partByNames,
             'isPlayer': isPlayer,
             'weaponSoundID': weaponSoundID,
             'turretSoundID': turretSoundID,
             'soundObjects': soundObjects,
             'context': context}
            for soundObjectFactory in TurretSoundObjectsFactories:
                soundObjectFactory.getSoundObjectSettings(data)

            if not info:
                return
            for soundObjectFactory in AircraftSoundObjectsFactories:
                soundObjectFactory.getSoundObjectSettings(data)

            return

    def initPlayer(self):
        model = BigWorld.player().controllers.get('modelManipulator', None)
        if hasattr(model, 'soundObjects'):
            for so in model.soundObjects:
                so.factory.createPlayer(so)

        woosh = db.DBLogic.g_instance.getWoosh()
        BigWorld.initBulletPassbySound(woosh['WooshSphereMain'], int(woosh['MaxHits']), float(woosh['Radius']))
        return

    def initAvatar(self, avatarID):
        avatar = BigWorld.entities.get(avatarID)
        if avatar:
            model = avatar.controllers['modelManipulator']
            if hasattr(model, 'soundObjects'):
                for so in model.soundObjects:
                    so.factory.createAvatar(avatar, so)

        else:
            LOG_INFO('[Audio] unable to find an avatar by id: ', avatarID)

    def createTurret(self):
        arena = GameEnvironment.getClientArena()
        for obj in arena.allObjectsData.items():
            val = obj[1]
            if 'turretsLogic' not in val or 'modelManipulator' not in val:
                continue
            if not hasattr(val['modelManipulator'], 'soundObjects'):
                continue
            for so in val['modelManipulator'].soundObjects:
                so.factory.createTurret(obj[0], so, val)

    def stopHangar(self):
        self.music.stopHangar()
        self.ui.setHoverButtonRadius(100.0)

    def loadArena(self):
        self.__soundBanksManager.loadBank(WEAPONS_BANK_NAME)
        self.__soundBanksManager.attachWwiseObjectToCase(WEAPONS_BANK_NAME, SOUND_CASES.ARENA)
        self.__voice = Voiceover()
        self.music.playArena()
        self.voice.load()
        self.__prevTarget = None
        self.__winner = False
        self.__draw = False
        self.__prevTarget = None
        self.__burning = {}
        self.__soundBanksManager.unloadSoundCase(SOUND_CASES.HANGAR)
        for bankName in Arena_Banks:
            self.__soundBanksManager.loadBank(bankName)
            self.__soundBanksManager.attachWwiseObjectToCase(bankName, SOUND_CASES.ARENA)

        GameEnvironment.getClientArena().onGameResultChanged += self.__onGameResultChanged
        player = BigWorld.player()
        player.eArenaLoaded += self.__onArenaLoaded
        player.eLeaveWorldEvent += self.__onLeaveWorld
        return

    def unloadArena(self):
        self.__voice = None
        self.__soundBanksManager.unloadSoundCase(SOUND_CASES.ARENA)
        BigWorld.finiBulletPassbySound()
        self.__em.clear()
        return

    def getSoundObjects(self, entityId):
        arena = GameEnvironment.getClientArena()
        avatarInfo = arena.avatarInfos.get(entityId, {})
        model = avatarInfo.get('modelManipulator', None)
        if model and model.soundObjects:
            return [avatarInfo, model.soundObjects]
        else:
            return [avatarInfo, None]

    def enumSoundObjects(self, entityId, cls):
        arena = GameEnvironment.getClientArena()
        avatarInfo = arena.avatarInfos.get(entityId, {})
        model = avatarInfo.get('modelManipulator', None)
        if not model or not model.soundObjects:
            return
        else:
            result = []
            for s in model.soundObjects:
                if s.factory.__class__.__name__ == 'AircraftEngineSoundFactory':
                    result.append(s)

            return result

    def fixedSoundObject(self, entityId, name):
        soundObjects = self.getSoundObjects(entityId)[1]
        if not soundObjects:
            return None
        else:
            for so in soundObjects:
                if so.factory.__class__.__name__ == 'AircraftSFXFactory' and so.wwiseGameObject:
                    return so.wwiseGameObject

            return None

    def findLoadSet(self, eventSet, isPlayer, isAA = False, isTL = False, justCopyList = None):
        loadSet = {}
        for i in eventSet:
            if str(i).find('Player') != -1 and isPlayer or str(i).find('NPC') != -1 or str(i).find('AA') != -1 and isAA or str(i).find('TL') != -1 and isTL or justCopyList and i in justCopyList:
                loadSet[i] = eventSet[i]

        return loadSet

    def updateSpeedAndAltitude(self, entity, isPlayer, soundObject):
        altitude = entity.altitudeAboveObstacle if isPlayer else entity.getAltitudeAboveWaterLevel()
        soundObject.setRTPC('RTPC_Aircraft_Height' if isPlayer else 'RTPC_NPC_Height', altitude, 1000 / RTPC_Altitude_Update_Freq)
        entityGID = entity.globalID
        battleData = preparedBattleData.get(entityGID, None)
        if battleData:
            speedometer = battleData.speedometer
            if speedometer:
                if len(speedometer) == SPEEDOMETER_DATA_SIZE:
                    maxSpeedPercentRatio = 100.0 / speedometer[SPEEDOMETER_MAX_SPEED_IDX]
                    soundObject.setRTPC('RTPC_Aircraft_Body_Speed' if isPlayer else 'RTPC_NPC_Body_Speed', maxSpeedPercentRatio * entity.getSpeed(), 1000 / RTPC_Altitude_Update_Freq)
                else:
                    LOG_WARNING('Speedometer wrong data length. Expected: {0}, Actual: {1}'.format(SPEEDOMETER_DATA_SIZE, len(speedometer)))
            else:
                LOG_WARNING("Can't get an speedometer data from the prepared battle data")
        else:
            LOG_WARNING("Can't get a battle data for global ID: ", entityGID)
        return

    def replayMute(self, mute):
        self.__isReplayMute = mute
        setReplayMute(mute)

    def setVolumeAmplifier(self, p):
        setVolumeAmp(p)

    def onBattleStart(self):
        self.ui.onBattleStart()
        self.eOnBattleStart()

    def onBattleEnd(self, inGame = True):
        if inGame:
            self.ui.playGameResults()
        self.eOnBattleEnd()

    def onStateChanged(self, entity, old, new):
        model = entity.controllers.get('modelManipulator', None)
        isPlayer = entity.id == BigWorld.player().id
        if not model or not model.soundObjects:
            return
        else:
            for so in model.soundObjects:
                if not so.wwiseGameObject:
                    continue
                so.wwiseGameObject.onStateChanged(entity, old, new)

            return

    def onBurning(self, entityID, isPlayer, burning):
        self.__burning[entityID] = 0 if burning else BigWorld.time()
        self.__playFireSpeech(entityID, isPlayer, burning)
        if isPlayer:
            sfx = self.fixedSoundObject(BigWorld.player().id, 'sfx')
            if not sfx:
                return
            if burning:
                sfx.play('Fire', 'State')
            else:
                sfx.stop('Fire', 'State')

    def onConnected(self):
        self.__disconnected = False

    def onDisconnect(self):
        self.__disconnected = True

    def onStallingDanger(self, visible):
        self.eOnStallDanger(visible)

    def onLoadingScreenClosed(self):
        curVehicleID = BigWorld.player().curVehicleID
        DopplerEffect.instance().setListener(BigWorld.player())
        DopplerEffect.instance().activate()
        for k in BigWorld.player().visibleAvatars.keys():
            if not BigWorld.player().visibleAvatars[k].inWorld:
                continue
            self.initAvatar(k)

        if not curVehicleID:
            BigWorld.player().eUpdateSpectator += self.__onSpectator
        self.eLoadingScreenClosed()

    def __onArenaLoaded(self):
        self.createTurret()
        gm = extractGameMode(BigWorld.player().gameMode)

    def __onSpectator(self, target):
        DopplerEffect.instance().setListener(BigWorld.entities.get(target))

    def __onLeaveWorld(self):
        gm = extractGameMode(BigWorld.player().gameMode)
        BigWorld.player().eUpdateSpectator -= self.__onSpectator

    def __onGameResultChanged(self, gameResult, winState):
        winResults = [GAME_RESULT.SUPERIORITY_SUCCESS, GAME_RESULT.ELIMINATION]
        self.__winner = gameResult in winResults and BigWorld.player().teamIndex == winState
        self.__draw = gameResult in [GAME_RESULT.DRAW_ELIMINATION,
         GAME_RESULT.DRAW_ELIMINATION_NO_PLAYERS,
         GAME_RESULT.DRAW_SUPERIORITY,
         GAME_RESULT.DRAW_TIME_IS_RUNNING_OUT]
        battleType = GameEnvironment.getClientArena().battleType
        if battleType == ARENA_TYPE.TRAINING or battleType == ARENA_TYPE.TUTORIAL:
            self.onBattleEnd(False)

    def __playFireSpeech(self, entityID, isPlayer, isFire):
        if isPlayer:
            if isFire:
                self.voice.play('voice_fire_started')
            else:
                self.voice.skipDynSeqItems(['voice_fire_started'])
                self.voice.play('voice_fire_stopped')
        elif isFire:
            entity = BigWorld.entities.get(entityID)
            player = BigWorld.player()
            if entity and hasattr(entity, 'lastDamagerID') and entity.lastDamagerID == player.id and entity.teamIndex != player.teamIndex and EntityStates.inState(player, EntityStates.GAME):
                self.voice.play('voice_fire_enemy' if isAvatar(entity) else 'voice_ground_target_fire')

    def isBurning(self, id, fireAttenuationDelta = 0):
        value = self.__burning.get(id, -1)
        if value < 0:
            return False
        if value > 0:
            return BigWorld.time() < value + fireAttenuationDelta
        return True

    @property
    def isWinner(self):
        return self.__winner

    @property
    def isDraw(self):
        return self.__draw

    @property
    def isDisconnected(self):
        return self.__disconnected

    @property
    def isReplayMute(self):
        return self.__isReplayMute or BattleReplay.g_replay and BattleReplay.g_replay.isTimeWarpInProgress

    @property
    def voice(self):
        if not self.__voice:
            self.__voice = Voiceover()
        return self.__voice

    @property
    def music(self):
        return self.__music

    @property
    def ui(self):
        return self.__ui


g_sound_impl = None

def GameSound():
    global g_sound_impl
    if g_sound_impl is None:
        g_sound_impl = GameSoundImpl()
    return g_sound_impl


def GS():
    return GameSound()