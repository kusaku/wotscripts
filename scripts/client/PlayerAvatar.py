# Embedded file name: scripts/client/PlayerAvatar.py
from functools import partial
import cPickle
import zlib
import os
import BigWorld
import CompoundSystem
import Keys
from Avatar import Avatar, isEntityInWorld, AvatarDummyPart
from Helpers.ActionMatcher import ActionMatcher, INTRO_LOFT_MIN_ROTATION_DEVIATION
from EntityHelpers import EntityStates, extractGameMode, isClientReadyToPlay
from Event import Event, EventOrdered, EventManager
from ExternalModifiers import ExternalModifiers
from Operations.OperationReceiver import OperationReceiver
from Operations.OperationSender import OperationSender
from OperationCodes import OPERATION_CODE
from TutorialClient.TutorialManager import TutorialManager
from HintsManager import HintsManager
from _preparedBattleData_db import preparedBattleData
from _performanceCharacteristics_db import airplanes as airplanes_PC
from clientConsts import NOT_CONTROLLED_MOD, CINEMATIC_CAMERA_SCENARIO_ID, OUTRO_FADEIN_DURATION, BULLET_HIT_INITIAL_FORCE, BULLET_HIT_FORCE_FACTOR, BULLET_HIT_LIMITED_EFFECT_REL_HP_LIMIT
from consts import *
from consts import COLLISION_TYPE_WATER, COLLISION_TYPE_GROUND
from debug_utils import *
from gui import Cursor
from gui.HUDconsts import *
import CameraEffect
import GameEnvironment
import VOIP
import db.DBLogic
import gui.hud
import updatable.UpdatableManager
import wgPickle
import GUI
import Math
import Settings
import EffectManager
import ClientLog
import StaticModels
import GameServerMessenger
import modelManipulator.ModelManipulator3
from messenger import XmppChat
import WeatherManager
from CollidableObject import CollidableObject
from AvatarControllerBase import AvatarControllerBase
from ScenarioClient.PlayerAvatarScenarioController import PlayerAvatarScenarioController
from ScenarioClient.TeamObjectScenarioController import TeamObjectScenarioController
from ScenarioClient.ClientScenarioActions import ClientScenarioActions
from db.DBEffects import Effects
from wofdecorators import timeLimit
import GlobalEvents
from config_consts import IS_DEVELOPMENT
from gui.hud import BattleQuest, SelectedComplexQuest
import GroundEffectsSettings
from audio.AKConsts import CAMERA_AIR_EFFECT
from audio import GameSound
from audio import HitSound
from audio import WwiseGameObject
if IS_CLIENT and IS_DEVELOPMENT and __debug__:
    import DebugManager
DISABLE_KEYS = (Keys.KEY_UPARROW,
 Keys.KEY_LEFTARROW,
 Keys.KEY_RIGHTARROW,
 Keys.KEY_DOWNARROW)

class EngineController(AvatarControllerBase):
    PART_NAME = 'Engine'

    def __init__(self, owner):
        AvatarControllerBase.__init__(self, owner)
        self.__overheat = False
        self.__inputValue = 0

    def __startOverheat(self):
        self.__overheat = True
        self._owner.eEngineOverheat()
        GameSound().voice.play('voice_engine_overheated')

    def __stopOverheat(self):
        self.__overheat = False

    def onParentSetState(self, stateID, data):
        pass

    def updateTemperature(self, tempr):
        if tempr >= WEP_DISABLE_TEMPERATURE and not self.__overheat:
            self.__startOverheat()
        if tempr < WEP_DISABLE_TEMPERATURE and self.__overheat:
            self.__stopOverheat()
        normT = (tempr - WEP_ENABLE_TEMPERATURE) / ENGINE_WORK_INTERVAL

    def applyInput(self, value):
        if value != self.__inputValue:
            if value >= 1:
                partsServerState = self.__getState()
                if partsServerState:
                    self._owner.eUpdateEngineState(partsServerState)
            self.__inputValue = value
        forceValue = self.__correctionForce(value)
        self._owner.eUpdateForce(forceValue)
        self._owner.controllers['modelManipulator'].updateForsageEffects(forceValue > 0 and not self.__overheat)
        if CameraEffect.g_instance:
            CameraEffect.g_instance.handleForsage(forceValue)

    def __getState(self):
        partsServerState = []
        for partID, partServerState in self._owner.partStates:
            partSettings = self._owner.settings.airplane.getPartByID(partID)
            if partSettings:
                partTypeData = partSettings.getActualPart(partID, self._owner.partTypes)
                partTypeStr = partTypeData.componentType
                if partTypeStr == EngineController.PART_NAME and partTypeStr in PART_TYPES_TO_ID:
                    partsServerState.append(partServerState)

        return partsServerState

    def __correctionForce(self, value):
        if self._owner.isWarEmergencyPower and not self._owner.autopilot:
            return 1.0
        if value > 0:
            return 0.0
        return value


class PlayerAvatar(Avatar):
    """
    Player avatar
    """

    def __init__(self):
        Avatar.__init__(self)
        self.__setAirplaneFilter(True)

    def sendInitialData(self, str):
        """
        Data for one-time initialization of fields avatar
        @param str: pickle string
        """
        data = wgPickle.loads(wgPickle.FromServerToClient, str)
        self.maxPitchRotationSpeed = data['maxPitchRotationSpeed']
        self.rollRudderNorma = data['rollRudderNorma']
        criticalSpeed = preparedBattleData[self.globalID].speedometer[-1]
        stallSpeed = airplanes_PC[self.globalID].stallSpeed / 3.6
        data_ = {'stallSpeed': stallSpeed,
         'criticalSpeed': criticalSpeed}
        self.eSendInitialData(data_)

    def receiveOperationTimeout(self, invocationId):
        """
        REceive operation timeout
        @param invocationId:
        """
        self.__operationReceiver.receiveOperationTimeout(invocationId)

    def clientReceiveResponse(self, responseType, sequenceID, invocationId, operationCode, argStr):
        """
        receive operation
        @param responseType
        @param sequenceId:
        @param operationCode:
        @param invocationId:
        @param argStr:
        """
        if responseType == RESPONSE_TYPE.RESPONSE_TYPE_OPERATION:
            self.__operationReceiver.receiveOperation(invocationId, operationCode, argStr)
        elif responseType == RESPONSE_TYPE.RESPONSE_TYPE_CMD:
            self.__operationSender.receiveOperationResponse(invocationId, operationCode, argStr)

    def onStreamComplete(self, id, data):
        try:
            id, streamData = cPickle.loads(zlib.decompress(data))
            if id == STREAM_CLIENT.STREAM_ID_UPDATE_ARENA:
                functionIndex, updateFunctionID, argStr = streamData
                self.onUpdateArena(functionIndex, updateFunctionID, argStr)
            elif id == STREAM_CLIENT.STREAM_ID_RESPONSE:
                responseType, operationCode, invocationId, operationData = streamData
                if responseType == RESPONSE_TYPE.RESPONSE_TYPE_OPERATION:
                    self.receiveOperation(invocationId, operationCode, operationData)
                elif responseType == RESPONSE_TYPE.RESPONSE_TYPE_CMD:
                    self.__operationSender.receiveOperationResponse(invocationId, operationCode, operationData)
        except:
            LOG_CURRENT_EXCEPTION()

    def _createControllers(self):
        super(PlayerAvatar, self)._createControllers()
        engineController = EngineController(self)
        self._registerController('engineController', engineController)
        self._registerController('externalModifiers', ExternalModifiers(self, self.consumables, self.equipment, self.crewSkills))
        self.controllers['weapons'].guns.eGunOverHeat += self.__onGunOverHeat
        self.weaponsSettings = self.settings.airplane.flightModel.weaponOptions
        if extractGameMode(self.gameMode) == GAME_MODE.GM_TUTORIAL:
            tutorialManager = TutorialManager(self, self.__operationReceiver)
            self._registerController('tutorialManager', tutorialManager)
        scenarioData = db.DBLogic.g_instance.getScenario(PLAYER_SCENARIO)
        if scenarioData:
            scenarioController = TeamObjectScenarioController(self, scenarioData)
            self._registerController('scenarioController', scenarioController)
        if CINEMATIC_CAMERA_SCENARIO_ID:
            scenarioData = db.DBLogic.g_instance.getScenario(CINEMATIC_CAMERA_SCENARIO_ID)
            if scenarioData:
                scenarioController = PlayerAvatarScenarioController(self, scenarioData)
                self._registerController('scenarioCameraController', scenarioController)
            else:
                LOG_ERROR("Can't find scenario: ", CINEMATIC_CAMERA_SCENARIO_ID)
        self._registerController('hintsManager', HintsManager(self))

    def _onControllersCreation(self):
        super(PlayerAvatar, self)._onControllersCreation()
        self.ePartStateChanged += self.controllers['externalModifiers'].onPartStateChanged

    def initTutorialUI(self):
        if 'tutorialManager' in self.controllers:
            self.controllers['tutorialManager'].initTutorialUI()

    def onHUDBattleLoadingClosed(self):
        if not self.clientIsReady and self.inWorld:
            GameSound().onLoadingScreenClosed()
            self.onHUDBattleLoadingClosedEvent()
            self.clientIsReady = True
            ClientScenarioActions.refreshDelayedActions()

    def onArenaLoaded(self):
        LOG_DEBUG('onArenaLoaded')
        self.cell.onArenaLoaded()
        if getattr(self, 'isBanned', False):
            return
        else:
            self.eArenaLoaded()
            if self.curVehicleID:
                self._checkStateSettings(EntityStates.GAME, self.state, False)
                currentTarget = BigWorld.entities.get(self.curVehicleID, None)
                if currentTarget and currentTarget.inWorld:
                    self.__updateSpectator()
            if not GameEnvironment.getHUD().isTutorial():
                BigWorld.worldDrawEnabled(True)
            BigWorld.setLoadingFpsMode(False)
            BigWorld.setReducedFpsMode(False)
            WeatherManager.InitWeather()
            return

    def _createEvents(self):
        if not super(PlayerAvatar, self)._createEvents():
            return False
        em = self._eventManager
        self.eArenaLoaded = Event(em)
        self.onAutopilotEvent = Event(em)
        self.onGunOverheatedEvent = Event(em)
        self.onStateChanged = Event(em)
        self.onUpdateArena = Event(em)
        self.eEnterWorldEvent = EventOrdered(em)
        self.onHUDBattleLoadingClosedEvent = Event(em)
        self.onUpdateDebugHUD = Event(em)
        self.onAvatarEnterWorldEvent = Event(em)
        self.onAvatarLeaveWorldEvent = Event(em)
        self.onReceiveServerData = Event(em)
        self.eUpdateHealth = Event(em)
        self.eUpdateConsumables = Event(em)
        self.eUpdateSpectator = Event(em)
        self.eLeaveWorldEvent = Event(em)
        self.eUpdateEngineTemperature = Event(em)
        self.ePartFlagSwitchedNotification = Event(em)
        self.ePartFlagSwitchedOn = Event(em)
        self.ePartCrit = Event(em)
        self.eSetBombTargetVisible = Event(em)
        self.eEngineOverheat = Event(em)
        self.eUpdateEngineState = Event(em)
        self.eUpdateForce = Event(em)
        self.eRestartInput = Event(em)
        self.eStartCollectClientStats = Event(em)
        self.eStopCollectClientStats = Event(em)
        self.eFlyKeyBoardInputAllowed = Event(em)
        self.eReportDestruction = Event(em)
        self.eRespawn = Event(em)
        self.eReportNoShell = Event(em)
        self.eUpdateHUDAmmo = Event(em)
        self.eSendInitialData = Event(em)
        self.eLaunchShell = Event(em)
        self.eOwnShellExplosion = Event(em)
        self.eSwitchedVehicle = Event(em)
        self.eAutoAlightFromDestroyedTransport = Event(em)
        self.eVictimInformAboutCrit = Event(em)
        self.eUniqueSkillStateChanged = Event(em)
        return True

    def onBecomePlayer(self):
        LOG_TRACE('PlayerAvatar: onBecomePlayer')
        self._createEvents()
        GameEnvironment.g_instance.start(self)
        self.__flyMouseInputAllowed = True
        self.__flyKeyBoardInputAllowed = True
        self.__operationReceiver = OperationReceiver(self.base, wgPickle.FromServerToClient, wgPickle.FromClientToServer)
        self.__operationSender = OperationSender(self.base, wgPickle.FromServerToClient, wgPickle.FromClientToServer)
        self.__forsageTime = 0.0
        self.pitchAngleBraking = 1.0
        self.maxPitchRotationSpeed = 1.0
        self.rollRudderNorma = 0.25 * math.pi
        self.altitudeAboveObstacle = 10000
        self.speed = 0.0
        self.__reportDestructionCallback = None
        self.__visibleAvatars = {}
        self.__waitVoipClientStatus = False
        self.__prevArmamamentStates = None
        self.deflectionTargetsInProgress = 0
        return

    def setFlyMouseInputAllowed(self, val):
        GameEnvironment.getInput().inputIsBlocked(val)
        self.__flyMouseInputAllowed = val

    def isFlyMouseInputAllowed(self):
        return self.__flyMouseInputAllowed

    def setFlyKeyBoardInputAllowed(self, flag):
        self.__flyKeyBoardInputAllowed = flag
        self.eFlyKeyBoardInputAllowed(flag, self)

    def isFlyKeyBoardInputAllowed(self):
        return self.__flyKeyBoardInputAllowed

    def _preStateChangeInit(self):
        Avatar._preStateChangeInit(self)
        GameEnvironment.getCamera().setMainEntity(self)
        CameraEffect.Init()

    def onEnterWorld(self, prereqs):
        try:
            LOG_TRACE('PlayerAvatar: onEnterWorld', self.id, self.pilotBodyType)
            LOG_INFO('ARENA TYPE enter:', self.arenaType)
            self.reportedDamagedPartsByEntity = {}
            self.reportedDamagedEntityID = None
            self.reportedDamagedAllyTime = 0
            self.reportedDestroyedObjectHQTime = 0
            self.__cameraAirEffectSound = {}
            self.airEffectName = None
            self.screenParticleName = None
            arenaData = db.DBLogic.g_instance.getArenaData(self.arenaType)
            import BWPersonality
            if arenaData:
                arenaTypeName = 'unknown arena type ({0})'.format(self.arenaType)
            else:
                import BWPersonality
                BWPersonality.g_lastMapID = -1
                arenaTypeName = arenaData.typeName
            ClientLog.g_instance.general('Enter World: %s' % arenaTypeName)
            Avatar.onEnterWorld(self, prereqs)
            self.__updateCameraForsageEffectParams()
            self.eEnterWorldEvent()
            self.cell.onClientCreated()
            from gui.WindowsManager import g_windowsManager
            g_windowsManager.showBattleUI()
            updatable.UpdatableManager.Init(self)
            CompoundSystem.setCompoundLODScale(AIRCRAFT_MODEL_SCALING)
            self.selectedGuns = 0
            damageEffects = self.settings.airplane.visualSettings.damageEffects
            self.__damageReasonToEffectID = {}
            self.__damageReasonToEffectID[DAMAGE_REASON.TREES] = damageEffects.receive_damage_tree
            self.__damageReasonToEffectID[DAMAGE_REASON.WATER] = damageEffects.receive_damage_water
            self.__damageReasonToEffectID[DAMAGE_REASON.TERRAIN] = damageEffects.receive_damage_terrain
            self.debugMode = False
            self.cell.setDebugMode(False)
            self.cell.setDeflectionMode(1 if Settings.g_instance.gameUI['deflectionTest1'] else 0)
            self.__updateCallBack = None
            self.__update()
            Settings.g_instance.blockSystemKeys(True)
            if 'tutorialManager' in self.controllers:
                self.controllers['tutorialManager'].onEnterWorld()
            detailTex = self.controllers['modelManipulator'].surface.getDetailTexture()
            if detailTex != None:
                BigWorld.setAircraftDetailTexture(detailTex)
            else:
                BigWorld.setAircraftDetailTexture('')
            BigWorld.setLoadingFpsMode(True)
            GameSound().loadArena()
        except:
            LOG_CURRENT_EXCEPTION()

        return

    def hasGunner(self):
        for partID, _ in self.partStates:
            partSettings = self.settings.airplane.getPartByID(partID)
            if partSettings:
                partTypeData = partSettings.getFirstPartType()
                if partTypeData.componentType == 'Gunner1':
                    return True

        return False

    def reportTeamObjectDestruction(self, killerID, victimID, objectType, objectTeamIndex, points, pointsMax):
        LOG_DEBUG('reportTeamObjectDestruction', killerID, victimID, objectType, objectTeamIndex, points, pointsMax)
        GameSound().music.playTeamObjectDestroyed(killerID, objectTeamIndex)

    def reportDestruction(self, killingInfo):
        self.__reportDestructionCallback = BigWorld.callback(0.2, partial(self.__reportDestruction, killingInfo))

    def __reportDestruction(self, killingInfo):
        """killingInfo = {killerID, victimID, lastDamageType}
        NOTE: lastDamageType is optional field. present only if this client destroyed airplane"""
        self.__reportDestructionCallback = None
        self.eReportDestruction(killingInfo)
        return

    def onEntitiesReset(self):
        BigWorld.worldDrawEnabled(False)

    def requestClientStats(self):
        clientStatsCollector = GameEnvironment.g_instance.service('ClientStatsCollector')
        if clientStatsCollector:
            clientStatsCollector.requestForData()

    def __disableNearPlaneAirwave(self):
        if CameraEffect.g_instance:
            CameraEffect.g_instance.stopNearPlaneEffects()
        self.__visibleAvatars.clear()

    def __destroyCameraEffectSystem(self):
        self.__disableNearPlaneAirwave()
        CameraEffect.Destroy()

    def onLeaveWorld(self):
        LOG_TRACE('PlayerAvatar: onLeaveWorld', self.id)
        if not BigWorld.isWindowVisible():
            BigWorld.flashGameWindow(0)
        Settings.g_instance.blockSystemKeys(False)
        ClientLog.g_instance.general('Leave World')
        BigWorld.worldDrawEnabled(False)
        BigWorld.setReducedFpsMode(True)
        self.eStopCollectClientStats()
        self.__setAirplaneFilter(False)
        self.__destroyCameraEffectSystem()
        BigWorld.clearAllGroup()
        BigWorld.clearBullets()
        BigWorld.cleanCombinedDiffuseTextures()
        StaticModels.destroyAll()
        EffectManager.Destroy()
        self.settings = None
        VOIP.api().onLeaveArenaChannel()
        VOIP.api().onLeaveArenaScreen()
        self.eLeaveWorldEvent()
        Avatar.onLeaveWorld(self)
        BigWorld.setAircraftDetailTexture('')
        try:
            self.arena.destroy()
            self.arena = None
        except Exception:
            pass

        Cursor.forceShowCursor(True)
        for x in GUI.roots():
            GUI.delRoot(x)

        if self.__updateCallBack != None:
            BigWorld.cancelCallback(self.__updateCallBack)
            self.__updateCallBack = None
        updatable.UpdatableManager.Destroy()
        if hasattr(self, 'avatarAPI') and self.avatarAPI is not None:
            self.avatarAPI.destroy()
        self.__operationReceiver.destroy()
        self.__operationReceiver = None
        self.__operationSender.destroy()
        self.__operationSender = None
        CompoundSystem.removeAllModels()
        BigWorld.removeAllShadowEntities()
        return

    def onBecomeNonPlayer(self):
        LOG_INFO('PlayerAvatar: onBecomeNonPlayer', self.id)
        from gui.WindowsManager import g_windowsManager
        if self.__reportDestructionCallback:
            BigWorld.cancelCallback(self.__reportDestructionCallback)
            self.__reportDestructionCallback = None
        GameEnvironment.g_instance.end()
        g_windowsManager.closeBattleUI()
        g_windowsManager.hideAll()
        return

    def set_isWarEmergencyPower(self, oldValue):
        if EntityStates.inState(self, EntityStates.GAME):
            input = GameEnvironment.getInput()
            if input:
                self.applyInputAxis(FORCE_AXIS, input.inputAxis.getCurrentForce(), True)
                self.eUpdateEngineTemperature(self.engineTemperature, self.wepWorkTime, self.isWarEmergencyPower)

    @isEntityInWorld
    def set_engineTemperature(self, oldValue):
        self.__updateEngineTemperature()

    def set_wepWorkTime(self, oldValue):
        self.__updateEngineTemperature()
        self.__updateCameraForsageEffectParams()

    def __updateEngineTemperature(self):
        self.eUpdateEngineTemperature(self.engineTemperature, self.wepWorkTime, self.isWarEmergencyPower)
        self.controllers['engineController'].updateTemperature(self.engineTemperature)

    def __updateCameraForsageEffectParams(self):
        cameraEffectInst = CameraEffect.g_instance
        if cameraEffectInst:
            effectParams = {}
            effectParams['wepWorkTime'] = self.wepWorkTime
            curEngineID = self.logicalParts[LOGICAL_PART.ENGINE]
            effectParams['defWepWorkTime'] = self.settings.airplane.flightModel.engine[curEngineID].wepWorkTime
            cameraEffectInst.setEffectParams('FORSAGE', effectParams)

    def applyInputAxis(self, axis, value, replayMode = False):
        """send axises for animations and sounds"""
        import BattleReplay
        BattleReplay.g_replay.notifyAxisValues(axis, value)
        if BattleReplay.isPlaying() and not replayMode:
            return
        elif not EntityStates.inState(self, EntityStates.GAME):
            return
        else:
            if FORCE_AXIS == axis:
                self.controllers['engineController'].applyInput(value)
            if FLAPS_AXIS == axis:
                if not preparedBattleData[self.globalID].flaps:
                    return
                sfx = GameSound().fixedSoundObject(BigWorld.player().id, 'sfx')
                if self.id == BigWorld.player().id and sfx is not None:
                    sfx.playFlaps(value)
            self.controllers['modelManipulator'].setAxisValue(axis, value)
            return

    def isGUIBlocked(self, event):
        return event.key in DISABLE_KEYS and self.isFlyKeyBoardInputAllowed() or event.key == Keys.KEY_LEFTMOUSE and event.isKeyDown() and self.isFlyMouseInputAllowed()

    def handleKeyEvent(self, event):
        """unused default BIgWorld callback"""
        pass

    def onReportBattleResult(self, clientBattleResult):
        LOG_TRACE('clientBattleResult =', clientBattleResult)
        self.controllers['modelManipulator'].setAxisValue(FORCE_AXIS, 0)
        self.__destroyCameraEffectSystem()

    def updateDebugHUD(self, strArgs):
        """SERVER MESSAGE: debug hud table resived"""
        self.onUpdateDebugHUD(self, strArgs)

    def _updateDamageEffects(self, effectPosition, effectForce):
        damageEffects = self.settings.airplane.visualSettings.damageEffects
        if self.lastDamageReason in self.__damageReasonToEffectID:
            externalEffectID = self.__damageReasonToEffectID[self.lastDamageReason]
            EffectManager.g_instance.createWorldEffect(Effects.getEffectId(externalEffectID), effectPosition, {'entity': self,
             'sfx': HitSound.AVATAR_EFFECT_HIT})
        else:
            if self.damagedByGunID:
                gunDescription = db.DBLogic.g_instance.getComponentByIndex(COMPONENT_TYPE.GUNS, self.damagedByGunID)
                gunProfile = db.DBLogic.g_instance.getGunProfileData(gunDescription.gunProfileName)
                damageEffects = gunProfile
            EffectManager.g_instance.createWorldEffect(Effects.getEffectId(damageEffects.receive_damage_own_1), effectPosition, {'entity': self,
             'force': effectForce,
             'sfx': HitSound.AVATAR_EFFECT_HIT})
            EffectManager.g_instance.createWorldEffect(Effects.getEffectId(damageEffects.receive_damage_own_2), effectPosition, {'entity': self,
             'sfx': HitSound.AVATAR_EFFECT_HIT})

    def __updateDamageCameraEffects(self, hpLostNorm):
        if CameraEffect.g_instance:
            isBulletDamage = self.lastDamageReason == DAMAGE_REASON.BULLET
            isGunnerAADamage = self.lastDamageReason == DAMAGE_REASON.AA_EXPLOSION
            if isBulletDamage or isGunnerAADamage:
                effectForce = BULLET_HIT_INITIAL_FORCE + hpLostNorm * BULLET_HIT_FORCE_FACTOR
                CameraEffect.g_instance.onCameraEffect('BULLET_HIT_STATIC_FORCE', force=1.0)
                CameraEffect.g_instance.onCameraEffect('BULLET_HIT_DYNAMIC_FORCE', force=effectForce)
                relHPRemainder = self.health / self.maxHealth
                if relHPRemainder <= BULLET_HIT_LIMITED_EFFECT_REL_HP_LIMIT:
                    CameraEffect.g_instance.onCameraEffect('BULLET_HIT_STATIC_FORCE_LIMITED_BY_HP', force=1.0)
                    CameraEffect.g_instance.onCameraEffect('BULLET_HIT_DYNAMIC_FORCE_LIMITED_BY_HP', force=effectForce)
            elif self.health > 0.0 and (self.lastDamageReason == DAMAGE_REASON.RAMMING or self.lastDamageReason == DAMAGE_REASON.OBSTACLE or self.lastDamageReason == DAMAGE_REASON.TREES):
                RAMMING_EFFECT_SPLITTER = db.DBLogic.g_instance.cameraEffects.rammingEffectSplitter
                effectID = 'LOW_RAMMING' if hpLostNorm < RAMMING_EFFECT_SPLITTER else 'HIGH_RAMMING'
                CameraEffect.g_instance.onCameraEffect(effectID, hpLostNorm)

    @isEntityInWorld
    def set_health(self, oldValue):
        """SERVER PROPERTY: health"""
        Avatar.set_health(self, oldValue)
        if oldValue > self.health:
            hpLostNorm = (oldValue - self.health) / self.maxHealth
            self.__updateDamageCameraEffects(hpLostNorm)
        self.eUpdateHealth(self.health, self.lastDamagerID, oldValue)

    def set_consumables(self, oldData):
        """SERVER PROPERTY: consumables"""
        Avatar.set_consumables(self, oldData)
        self.eUpdateConsumables(self.consumables)

    def set_armamentStates(self, oldValue):
        if self.armamentStates != self.__prevArmamamentStates and CameraEffect.g_instance:
            effectParams = {'caliber': self.__getActiveMaxCaliber()}
            effectID = self.settings.airplane.visualSettings.cameraEffects.shooting
            CameraEffect.g_instance.onCameraEffect(effectID, self.armamentStates != 0, additionalParams=effectParams)
            self.__prevArmamamentStates = self.armamentStates
        Avatar.set_armamentStates(self, oldValue)

    def __getActiveMaxCaliber(self):
        maxCaliber = 0
        if self.selectedGuns > 0:
            gunGroupsStates = self.controllers['weapons'].getGunGroupsStates()
            for groupID, reason in gunGroupsStates.items():
                groupMask = 1 << groupID - 1
                if self.selectedGuns & groupMask != 0 and reason == GUN_STATE.READY:
                    weaponGroups = self.getAmmoGroupsInitialInfo()
                    weaponData = weaponGroups[groupID]
                    description = weaponData['description']
                    if description and isinstance(description.caliber, (int,
                     long,
                     float,
                     complex)):
                        maxCaliber = max(maxCaliber, description.caliber)

        return maxCaliber

    def _checkStateSettings(self, oldState, state, transitionActions):
        """
        This function used for initialization the controllers at change of the state
        
        @param oldState: old entity state
        @param state: new entity state
        @param transitionActions: flag, is state change now or not
        @return:
        """
        Avatar._checkStateSettings(self, oldState, state, transitionActions)
        LOG_DEBUG(self.id, 'Avatar.STATE: ', EntityStates.getStateName(oldState), '->', EntityStates.getStateName(state))
        self.onStateChanged(oldState, state)
        if state & EntityStates.GAME:
            if self.actionMatcher:
                self.actionMatcher.destroy()
            if CameraEffect.g_instance:
                CameraEffect.g_instance.onCameraEffect('SPECTATOR', False)
                CameraEffect.g_instance.onCameraEffect('AIRCRAFT_IDLE_VIBRATION', True)
            self.actionMatcher = ActionMatcher(self, self.isPlayer())
            GameEnvironment.getInput().inputAxis.notControlledByUser(False, NOT_CONTROLLED_MOD.WAIT_START)
            GameEnvironment.getInput().inputAxis.notControlledByUser(False, NOT_CONTROLLED_MOD.AUTOPILOT)
            self.eStartCollectClientStats()
            if oldState & (EntityStates.WAIT_START | EntityStates.PRE_START_INTRO) and extractGameMode(self.gameMode) != GAME_MODE.GM_TUTORIAL:
                GameSound().onBattleStart()
            if CameraEffect.g_instance:
                CameraEffect.g_instance.startNearPlaneEffects()
        if state & EntityStates.PRE_START_INTRO:
            if CameraEffect.g_instance:
                CameraEffect.g_instance.onCameraEffect('SPECTATOR', True)
            GameEnvironment.getInput().inputAxis.notControlledByUser(True, NOT_CONTROLLED_MOD.AUTOPILOT)
            if not self.actionMatcher:
                self.actionMatcher = ActionMatcher(self, self.isPlayer(), INTRO_LOFT_MIN_ROTATION_DEVIATION)
            if transitionActions:
                self.eRestartInput()
                self.eRespawn()
        if state & EntityStates.WAIT_START:
            GameEnvironment.getInput().inputAxis.notControlledByUser(True, NOT_CONTROLLED_MOD.WAIT_START)
            if transitionActions:
                self.controllers['weapons'].restart()
                self.eRestartInput()
                self.updateAmmo()
                self.eRespawn()
            if CameraEffect.g_instance:
                CameraEffect.g_instance.onCameraEffect('SPECTATOR', False)
        elif not state & EntityStates.GAME:
            self.eSetBombTargetVisible(False)
        airplaneFilterEnabled = not EntityStates.inState(self, EntityStates.END_GAME)
        if not airplaneFilterEnabled:
            if self.actionMatcher:
                self.actionMatcher.destroy()
                self.actionMatcher = None
        self.__setAirplaneFilter(airplaneFilterEnabled)
        if EntityStates.inState(self, EntityStates.DEAD | EntityStates.OBSERVER | EntityStates.OUTRO):
            if CameraEffect.g_instance:
                CameraEffect.g_instance.onCameraEffect('AIRCRAFT_IDLE_VIBRATION', False)
                CameraEffect.g_instance.stopNearPlaneEffects()
            if EntityStates.inState(self, EntityStates.DEAD | EntityStates.OUTRO):
                if oldState & EntityStates.GAME and not state & EntityStates.OUTRO:
                    self.eRestartInput()
                if CameraEffect.g_instance:
                    if EntityStates.inState(self, EntityStates.DEAD):
                        CameraEffect.g_instance.stopAllEffects()
                        if CameraEffect.g_instance:
                            CameraEffect.g_instance.onCameraEffect('SPECTATOR', True)
                    else:
                        CameraEffect.g_instance.fadeOutAllEffects(OUTRO_FADEIN_DURATION)
            if state & EntityStates.DEAD and CameraEffect.g_instance and not self.curVehicleID and Settings.g_instance.cameraEffectsEnabled:
                CameraEffect.g_instance.onCameraEffect('DESTRUCTION')
        return

    def set_autopilot(self, oldValue):
        self.onAutopilotEvent(self.autopilot)
        GameEnvironment.getInput().inputAxis.notControlledByUser(self.autopilot, NOT_CONTROLLED_MOD.AUTOPILOT)
        if not self.autopilot:
            self.applyInputAxis(FORCE_AXIS, GameEnvironment.getInput().inputAxis.getCurrentForce())

    def OnReceiveDataFromServer(self, value):
        """SERVER PROPERTY: tick  - server sent data"""
        if self.movementFilter():
            if EntityStates.inState(BigWorld.player(), EntityStates.PRE_START_INTRO):
                self.speed = BigWorld.player().introFakeSpeed
            else:
                self.speed = self.getSpeed()
                maxSpeed = self.settings.airplane.flightModel.engine[0].maxSpeed if EntityStates.inState(self, EntityStates.GAME) else -1
                effectStartSpeed = self.settings.airplane.visualSettings.speedwiseEngineEffect
                self.controllers['modelManipulator'].updateSpeedwiseEngineEffects(self.speed, maxSpeed, effectStartSpeed)
            self.altitudeAboveObstacle = self.getAltitudeAboveObstacle()
            if CameraEffect.g_instance:
                CameraEffect.g_instance.handleSpeed(self.speed)
            self.onReceiveServerData()

    def syncGuns(self, data):
        weapons = self.controllers.get('weapons', None)
        if weapons:
            weapons.syncGuns(data)
            self.updateAmmo()
        return

    def deflectionTargetSet(self):
        BigWorld.player().deflectionTargetsInProgress -= 1

    def __onGunOverHeat(self):
        if 'tutorialManager' not in self.controllers:
            weapons = self.controllers.get('weapons', None)
            model = self.controllers.get('modelManipulator', None)
            if weapons and model:
                for group in weapons.getGunGroups():
                    if group.temperature >= GUN_OVERHEATING_TEMPERATURE:
                        sounds = weapons.getSounds(group.gunProfile.sounds.weaponSoundID)
                        if sounds is None:
                            continue
                        for s in sounds:
                            sfx = GameSound().fixedSoundObject(BigWorld.player().id, 'sfx')
                            if sfx:
                                sfx.play('NoAmmo')

                        GameSound().voice.play('voice_gun_overheated')

        return

    def onCollide(self, collidedContacts):
        tutorialManager = self.controllers.get('tutorialManager', None)
        if tutorialManager is None:
            return
        else:
            for cc in collidedContacts:
                if cc[0] == CollidableObject.DYNAMIC_COLLISION:
                    tutorialManager.onDynamicCollision()
                    return

            return

    def onResponseFromServer(self, cellRequest, cellResponse):
        """
        @param data: cellRequest, cellResponse
        """
        GameEnvironment.getInput().inputAxis.response(cellRequest, cellResponse)

    def set_shellsCount(self, oldValue):
        Avatar.set_shellsCount(self, oldValue)
        self.updateAmmo()

    def calcCorrectFireFlags(self, flags):
        return flags

    def onFireChange(self, newFireFlags):
        if self.selectedGuns != newFireFlags:
            self.selectedGuns = newFireFlags
            self.cell.onFire(self.calcCorrectFireFlags(newFireFlags))

    def getAmmoGroupsInitialInfo(self):
        ammoInitialInfo = self.controllers['weapons'].getGunGroupsInitialInfo()
        shellsInitialInfo = self.controllers['shellController'].getShellGroupsInitialInfo()
        ammoInitialInfo.update(shellsInitialInfo)
        return ammoInitialInfo

    def getAmmoCountByGroup(self):
        counters = self.controllers['weapons'].getGunGroupCounters()
        shellCounters = self.controllers['shellController'].getShellsCountByGroup()
        counters.update(shellCounters)
        return counters

    def launchShell(self, shellIndex):
        shellID = self.controllers['shellController'].getShellType(shellIndex)
        shellCount = self.controllers['shellController'].tryToLaunchShell(shellIndex)
        if shellCount == 0:
            self.eReportNoShell(shellID, LAUNCH_SHELL_RESULT_EMPTY)
        elif shellCount == -1:
            self.eReportNoShell(shellID, LAUNCH_SHELL_RESULT_DISABLED)
        elif shellCount == -2:
            self.eReportNoShell(shellID, LAUNCH_SHELL_RESULT_INCORRECT_ANGLE)
        elif shellCount != -3:
            self.eLaunchShell(shellIndex)
            if shellID == UPDATABLE_TYPE.BOMB and shellCount == 1:
                self.eSetBombTargetVisible(False)

    def updateAmmo(self):
        self.eUpdateHUDAmmo()

    def exitGame(self):
        self._leaveGame = True
        self.cell.leaveArena()

    def __setAirplaneFilter(self, enable):
        if enable:
            if not self.movementFilter():
                self.filter = self.createFilter()
            self.filter.airplaneFilter = False
            self.filter.speedCalculateEnable = True
            self.filter.inputCallback = self.OnReceiveDataFromServer
        elif self.movementFilter():
            self.filter.inputCallback = None
            self.filter = BigWorld.DumbFilter()
        return

    @property
    def tutorialIndex(self):
        if extractGameMode(self.gameMode) == GAME_MODE.GM_TUTORIAL:
            import BWPersonality
            return BWPersonality.g_tutorialIndex
        return -1

    def set_curVehicleID(self, lastValue):
        LOG_TRACE('PlayerAvatar: switchVehicle', self.curVehicleID, lastValue)
        self.__updateSpectator(lastValue)

    @timeLimit(0.6)
    def switchToVehicle(self, playerID):
        if EntityStates.inState(self, EntityStates.OBSERVER | EntityStates.DEAD | EntityStates.DESTROYED_FALL) and self.curVehicleID != playerID:
            self.cell.switchToVehicle(playerID)

    def __updateSpectator(self, prevVehicleID = None):
        currentTarget = BigWorld.entities.get(self.curVehicleID, None)
        isTargetPresent = currentTarget and currentTarget.inWorld
        if isTargetPresent:
            LOG_TRACE('PlayerAvatar: __updateSpectator switchVehicle', self.curVehicleID, prevVehicleID)
            detailTex = currentTarget.controllers['modelManipulator'].surface.getDetailTexture()
            if detailTex != None:
                BigWorld.setAircraftDetailTexture(detailTex)
            else:
                BigWorld.setAircraftDetailTexture('')
            if CameraEffect.g_instance:
                CameraEffect.g_instance.onCameraEffect('SPECTATOR', True)
            self.eSwitchedVehicle(self.id, self.curVehicleID, prevVehicleID)
            self.eUpdateSpectator(self.curVehicleID)
            BigWorld.setPlayersCompoundID(currentTarget.controllers['modelManipulator'].compoundID)
        return

    def onReceiveMarkerMessage(self, senderID, posX, posZ, messageStringID, fromQueue):
        GameSound().ui.postEvent('Play_hud_minimap_click')

    def __update(self):
        self.__updateCallBack = BigWorld.callback(0.001, self.__update)
        if updatable.UpdatableManager.g_instance:
            updatable.UpdatableManager.g_instance.update()
        if IS_DEVELOPMENT and __debug__:
            BigWorld.clearGroup('targetLine_' + str(self.id))
            BigWorld.clearGroup('movementLine_' + str(self.id))
            from AvatarBot import AvatarBot
            if not AvatarBot._DEBUG:
                return
            AvatarBot.renderDebugLines(self)

    def updateArena(self, functionIndex, updateFunctionID, argStr):
        self.onUpdateArena(functionIndex, updateFunctionID, argStr)

    def setDebugViewPosition(self, position, rotation):
        self.cell.setDebugViewPosition(position, rotation)

    def debugMoveAvatar(self, shift):
        self.cell.debugMoveAvatar(shift)

    def resetDebugMoveVector(self):
        self.cell.resetDebugMoveVector()

    def debugRotate(self, rotation):
        self.cell.debugRotate(rotation)

    def onUpdateTeamSuperiorityPoints(self, prevScore, ownScore, enemyScore):
        GameSound().music.playBattle(ownScore, enemyScore)

    def respondCommand(self, requestID, resultID, data):
        if hasattr(self, 'avatarAPI'):
            self.avatarAPI.onCmdResponse(requestID, resultID, data)

    def set_isArenaFreezed(self, oldValue):
        EffectManager.g_instance.setFreeze(self.isArenaFreezed)

    def onReceiveVOIPChannelCredentials(self, channel, teamMembers):
        if channel:
            VOIP.callWhenInitialized(lambda : VOIP.api().onEnterArenaChannel(channel, teamMembers.keys()))
        else:
            VOIP.api().onLeaveArenaChannel()

    def prerequisites(self):
        if hasattr(self, '_PlayerAvatar__prereqs'):
            return ()
        self.__prereqs = []
        self.__prereqs += EffectManager.g_instance.getPreloadingResources()
        self.__prereqs += [modelManipulator.ModelManipulator3.AIRCRAFT_FAKE_MODEL_NAME]
        self.__prereqs += gui.hud.HUD.getPreloadedResources()
        for s in self.__prereqs:
            LOG_DEBUG('prerequisites', s)

        return self.__prereqs

    def onPartFlagSwitchedOn(self, partId, flagID, authorID):
        LOG_DEBUG('onPartFlagSwitchedOn', partId, flagID, authorID)
        self.ePartFlagSwitchedOn(partId, flagID, authorID)

    def onPartStateChanging(self, partID, stateID, authorID, damageReason):
        if self._leaveGame:
            LOG_DEBUG('onPartStateChanging - player left the game', partID, stateID, authorID, damageReason)
            return
        LOG_DEBUG('onPartStateChanging', partID, stateID, authorID, damageReason)
        self.ePartCrit(AvatarDummyPart(self.settings.airplane, partID, stateID, authorID, damageReason))

    def onKickedFromServer(self, reason, isBan, expiryTime):
        LOG_MX('onKickedFromServer', reason, isBan, expiryTime)
        self.isBanned = True
        from gui.Scaleform.Disconnect import Disconnect
        Disconnect.show(reason, isBan, expiryTime)

    def onAvatarLeaveWorld(self, avatar):
        self.onAvatarLeaveWorldEvent(self, avatar.id)
        if avatar.id in self.__visibleAvatars:
            self.__visibleAvatars.pop(avatar.id)

    def onAvatarEnterWorld(self, avatar):
        LOG_DEBUG('onAvatarEnterWorld', avatar.id, self.curVehicleID)
        if self.inWorld and EntityStates.inState(self, EntityStates.DESTROYED | EntityStates.OBSERVER | EntityStates.DESTROYED_FALL) and self.curVehicleID == avatar.id:
            self.__updateSpectator()
            if isClientReadyToPlay():
                GameSound().initAvatar(avatar.id)
        elif self.inWorld and isClientReadyToPlay():
            GameSound().initAvatar(avatar.id)
        self.__visibleAvatars[avatar.id] = avatar
        self.onAvatarEnterWorldEvent(avatar.id)

    def messenger_onActionByServer(self, actionID, reqID, args):
        GameServerMessenger.g_instance.onActionByServer(XmppChat.MessengerActionProcessor(), actionID, reqID, args)

    def sendOperation(self, opCode, callback, *params):
        """ Needed for VOIP. """
        if self.__operationSender is not None:
            op = self.__operationSender.sendOperation(opCode, None, False, *params)
            if callback is not None:
                op.onResponse += callback
            return op
        else:
            return
            return

    def voipClientStatus(self, channelType, channelName, status):
        if hasattr(self.base, 'voipClientStatus'):
            if not self.__waitVoipClientStatus:
                self.__waitVoipClientStatus = True
                self.base.voipClientStatus(channelType, channelName, status)
        else:
            LOG_ERROR('PlayerAvatar.voipClientStatus: base not ready (?), will retry later')
            BigWorld.callback(3, lambda : self.voipClientStatus(channelType, channelName, status))

    def voipSquadStatus(self, squadID, status):
        self.base.voipSquadStatus(squadID, status)

    def voipMuteClient(self, dbid, mute):
        self.base.voipMuteClient(dbid, mute)

    def voipReceiveSquadChannel(self, channel, clients_list):
        LOG_TRACE('voipReceiveSquadChannel:', channel, clients_list)
        if channel != '':
            VOIP.callWhenInitialized(lambda : VOIP.api().onEnterSquadChannel(channel, clients_list))
        else:
            VOIP.api().onLeaveSquadChannel()

    def voipServerStatus(self, status, args):
        args = dict([ (pair['key'], pair['value']) for pair in args ])
        LOG_TRACE('voipServerStatus %d, args: %r' % (status, args))
        VOIP.api().onServerMessage(status, args)
        self.__waitVoipClientStatus = False

    def onTokenReceived(self, requestID, tokenType, data):
        pass

    def onQuestSelectConsist(self, res):
        try:
            res = cPickle.loads(zlib.decompress(res))
            LOG_DEBUG('Select quest Results: ', res)
            import BWPersonality
            BWPersonality.g_questSelected = SelectedComplexQuest(None)
            quests = BWPersonality.g_questSelected.quests
            from Helpers.i18n import localizeLobby, localizeAchievementsInQuest
            for r in res:
                questID, name, description, isComplete, isMainQuest = r
                if description and description.isupper():
                    description = localizeLobby(description)
                description = localizeAchievementsInQuest(description)
                quests[questID] = BattleQuest(questID, name, description, isMainQuest, isComplete)
                if isMainQuest:
                    BWPersonality.g_questSelected.mainQuestId = questID

            GlobalEvents.onQuestSelectUpdated()
        except:
            LOG_CURRENT_EXCEPTION()

        return

    def tutorialSetWPStrategySpline(self, botName, splineName):
        self.sendOperation(OPERATION_CODE.TUTORIAL_SET_WPS_SPLINE, None, botName, splineName)
        return

    def tutorialSetWPStrategyEvasion(self, botName, enable):
        self.sendOperation(OPERATION_CODE.TUTORIAL_SET_WPS_EVASION, None, botName, enable)
        return

    def tutorialSetBotStrategySimpleMode(self, botName, enable, distance, snapAlt):
        self.sendOperation(OPERATION_CODE.TUTORIAL_SET_BS_SIMPLE_MODE, None, botName, enable, distance, snapAlt)
        return

    def tutorialRestartPart(self):
        self.sendOperation(OPERATION_CODE.TUTORIAL_RESTART_PART, None)
        return

    def tutorialPause(self, value):
        self.sendOperation(OPERATION_CODE.TUTORIAL_PAUSE, None, value)
        return

    def tutorialReloadShells(self, reloadRockets = False, reloadBombs = False):
        self.sendOperation(OPERATION_CODE.TUTORIAL_RELOAD_SHELLS, None, reloadRockets, reloadBombs)
        return

    def onMapEntryCreated(self, mapEntry):
        if EntityStates.inState(self, EntityStates.PRE_START_INTRO):
            self.mapMatrix.a = mapEntry.mapMatrix
            GameEnvironment.getHUD().setRadarViewpoint(self.mapMatrix)

    def set_timelinesTime(self, oldValue):
        """transfer timeLines state from Cell ScenarioControllerMaster to Client ScenarioControllerSlave"""
        scenarioController = self.controllers.get('scenarioController', None)
        if scenarioController:
            scenarioController.refreshTimelines(self.timelinesTime)
        return

    @property
    def visibleAvatars(self):
        return self.__visibleAvatars

    def debugViewer_addNewKey(self, dvKey, str_data):
        import BattleReplay
        if BattleReplay.isPlaying():
            return
        print inspect.stack()
        from debug.layer0.DebugViewer.Debug_View_Manager import DebugViewManager
        DebugViewManager().addNewKey(dvKey, str_data)

    def debugViewer_pushToView(self, str_data):
        import BattleReplay
        if BattleReplay.isPlaying():
            return
        from debug.layer0.DebugViewer.Debug_View_Manager import DebugViewManager
        DebugViewManager().pushToView(str_data)

    def debugViewer_removeKey(self, dvKey):
        import BattleReplay
        if BattleReplay.isPlaying():
            return
        from debug.layer0.DebugViewer.Debug_View_Manager import DebugViewManager
        DebugViewManager().removeKey(dvKey)

    def battleStarted(self):
        import BWPersonality
        BWPersonality.g_lastMapID = self.arenaType

    def victimInformAboutCrit(self, partID, victimID, damageReason):
        self.eVictimInformAboutCrit(partID, victimID, HUD_MODULE_DESTROYED)

    def setNested_activeUniqueSkills(self, path, oldValue):
        if oldValue is 0:
            self.eUniqueSkillStateChanged(self.activeUniqueSkills[path[0]], True)
        else:
            self.eUniqueSkillStateChanged(oldValue, False)

    def setTargetEntity(self, target):
        self.cell.setLockTargetID(getattr(target, 'id', -1))

    def _doUpgradeGroundEffects(self, materialName, collisionPos, engine_index, deltaPos, effectData):
        super(PlayerAvatar, self)._doUpgradeGroundEffects(materialName, collisionPos, engine_index, deltaPos, effectData)
        isActive = effectData is not None
        isAirEffectActive = isActive and effectData.airEffect
        isScreenParticleActive = isActive and effectData.screenParticle
        if 'material' not in self.__cameraAirEffectSound:
            if isActive:
                self.__cameraAirEffectSound['soundObject'] = WwiseGameObject('Pillow', 0, 0, collisionPos)
                self.__cameraAirEffectSound['soundObject'].setSwitch(CAMERA_AIR_EFFECT.SWITCH_MATERIAL, materialName)
                self.__cameraAirEffectSound['soundObject'].postEvent(CAMERA_AIR_EFFECT.PLAY_EVENT_ID)
                self.__cameraAirEffectSound['material'] = materialName
        elif isActive:
            self.__cameraAirEffectSound['soundObject'].setPosition(collisionPos)
            if self.__cameraAirEffectSound['material'] != materialName:
                self.__cameraAirEffectSound['material'] = materialName
                self.__cameraAirEffectSound['soundObject'].setSwitch(CAMERA_AIR_EFFECT.SWITCH_MATERIAL, materialName)
        else:
            self.__cameraAirEffectSound['soundObject'].postEvent(CAMERA_AIR_EFFECT.STOP_EVENT_ID)
            del self.__cameraAirEffectSound['material']
        if not CameraEffect.g_instance:
            CameraEffect.Init()
        if self.airEffectName is None:
            if isAirEffectActive:
                self.airEffectName = effectData.airEffect
                CameraEffect.g_instance.onAirEffect(effectData.airEffect, True)
        elif not isAirEffectActive or self.airEffectName != effectData.airEffect:
            CameraEffect.g_instance.onAirEffect(self.airEffectName, False)
            self.airEffectName = None
        if self.screenParticleName is None:
            if isScreenParticleActive:
                self.screenParticleName = effectData.screenParticle
                EffectManager.g_instance.showScreenParticle(effectData.screenParticle)
        elif not isScreenParticleActive or self.screenParticleName != effectData.screenParticle:
            EffectManager.g_instance.hideScreenParticle(self.screenParticleName)
            self.screenParticleName = None
        return