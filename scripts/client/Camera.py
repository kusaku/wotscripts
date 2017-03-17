# Embedded file name: scripts/client/Camera.py
import BigWorld
from EntityHelpers import EntityStates, getReductionPointVector, isAvatar
import GameEnvironment
from GameServiceBase import GameServiceBase
import Math
import math
from functools import partial
from MathExt import *
from consts import *
from StateMachine import *
import Settings
from debug_utils import *
from Event import Event, EventManager
from gui.HUDconsts import HUD_REDUCTION_POINT_SCALE
from clientConsts import CAMERA_MOVING_SPEED, CAMERA_SCROLL_SCALE, CAMERA_SCROLL_STEP, CAMERA_DEFAULT_BOMBING_IDX, CAMERA_ALT_MODE_SHIFT_VECTOR, CAMERA_MAX_TARGET_SPEED, CAMERA_ZOOM_PRESET, SWITCH_STYLES_BUTTONS, OUTRO_FADEIN_DURATION, CAMERA_START_ALIGN_TIME, CAMERA_STOP_ALIGN_TIME, CAMERA_ALIGN_FLEXIBILITY
from Spectator import SpectatorStateMachine, SpectatorStateDynamic, SpectatorStateObserver, SpectatorStateFilm
import CameraZoomStatsCollector
import Settings
import InputMapping
import db.DBLogic
from CameraStates import *
inputToCamState = {INPUT_SYSTEM_STATE.MOUSE: {BATTLE_MODE.COMBAT_MODE: CameraState.MouseCombat,
                            BATTLE_MODE.ASSAULT_MODE: CameraState.MouseAssault},
 INPUT_SYSTEM_STATE.KEYBOARD: {BATTLE_MODE.COMBAT_MODE: CameraState.NormalCombat,
                               BATTLE_MODE.ASSAULT_MODE: CameraState.NormalAssault},
 INPUT_SYSTEM_STATE.JOYSTICK: {BATTLE_MODE.COMBAT_MODE: CameraState.JoystickCombat,
                               BATTLE_MODE.ASSAULT_MODE: CameraState.JoystickAssault},
 INPUT_SYSTEM_STATE.GAMEPAD_DIRECT_CONTROL: {BATTLE_MODE.COMBAT_MODE: CameraState.MouseCombat,
                                             BATTLE_MODE.ASSAULT_MODE: CameraState.MouseAssault}}
cameraStatesWithZoom = [CameraState.MouseCombat,
 CameraState.MouseAssault,
 CameraState.NormalCombat,
 CameraState.NormalAssault,
 CameraState.JoystickCombat,
 CameraState.JoystickAssault,
 CameraState.MouseCombat,
 CameraState.MouseAssault]

class CameraContext:

    def __init__(self, entity):
        self.entity = entity
        self.entityMatrix = entity.realMatrix
        self.targetMatrix = entity.realMatrix
        self.cameraSettings = db.DBLogic.g_instance.getAirplaneCameraPreset(entity.settings.airplane.visualSettings.camera)
        self.cameraOffset = entity.settings.airplane.visualSettings.cameraOffset
        self.reductionPoint = getReductionPointVector(entity.settings.airplane.flightModel.weaponOptions)
        self.normalFov = math.radians(self.cameraSettings.defaultFov)


class Camera(GameServiceBase):
    PRE_INTRO_ZOOM_IDX = 1
    PRE_INTRO_ZOOM_START_TIME = 7
    PRE_INTRO_CINEMATIC_START_TIME = 30

    def __init__(self):
        LOG_DEBUG('Camera constructor')
        super(Camera, self).__init__()
        self.__createEvents()
        self.__createMatrices()
        self.__cameraStateMachine = BattleCameraStateMachine()
        self.__zoomDataPosition = Math.Vector3(0, 0, 0)
        self.__inputState = None
        self.__inputBattleMode = BATTLE_MODE.COMBAT_MODE
        self.__updateZoomCallback = None
        self.__modelVisible = True
        self.__backToCurrentZoomDataIdx = None
        self.__isZoomEnable = True
        self.__isSniperModeEnable = True
        self.isSniperMode = False
        self.__bombingPrevZoomDataIdx = CAMERA_DEFAULT_BOMBING_IDX + 1
        self.__altMode = False
        self.__effectFOV = 1.0
        self.__effectOffset = Math.Vector4(0.0, 0.0, 0.0, 0.0)
        self.__context = None
        self.__targetEntity = None
        self.__curZoomData = None
        self.setEffectsEnabled(Settings.g_instance.cameraEffectsEnabled)
        self.__sniperOnZoomDataIdx = None
        self.__preIntroZoomIdxBackup = None
        self.__zoomDataIdx = Settings.g_instance.camZoomIndex
        self.__lastZoomDataIdx = Settings.g_instance.camZoomIndex
        self.__curZoomPreset = CAMERA_ZOOM_PRESET.DEFAULT
        self.__spectatorStateMachine = SpectatorStateMachine(self)
        self.setMaxMouseCombatFov(Settings.g_instance.maxMouseCombatFov)
        self.__FOVDistanceCorrection = 1.0
        self.__cbOutro = None
        self.__cinematicStarted = False
        self.__cursorLocked = False
        self.__preintroStopped = False
        self.__preintroFinished = False
        self.__cinematicPlayed = False
        self.__sniperModeTransferFinished = True
        return

    def setMaxMouseCombatFov(self, value):
        self.__maxDistanceFOV = value
        if self.__context and self.__context.cameraSettings:
            self.__applyZoomStateFov(self.zoomInterpolationTime)

    def getMaxMouseCombatFov(self):
        return self.__maxDistanceFOV

    @property
    def context(self):
        return self.__context

    @property
    def spectator(self):
        return self.__spectatorStateMachine

    @property
    def zoomInterpolationTime(self):
        return self.__compositeOffset.duration

    @zoomInterpolationTime.setter
    def zoomInterpolationTime(self, value):
        if self.__compositeOffset:
            self.__compositeOffset.duration = value

    def __unlockCursor(self, flexibility = -1):
        if self.__defaultStrategies['CameraStrategyMouse']:
            if flexibility > 0.0:
                self.__defaultStrategies['CameraStrategyMouse'].flexibility = flexibility
            self.__defaultStrategies['CameraStrategyMouse'].unlockCursor()
            self.__defaultStrategies['CameraStrategyMouse'].rotateCursor(0, 0)

    def __checkBattleCount(self):
        arenaStartTime = BigWorld.player().arenaStartTime
        serverTime = BigWorld.serverTime()
        curTime = int(round(arenaStartTime - serverTime))
        if arenaStartTime > 0:
            if curTime > CAMERA_STOP_ALIGN_TIME and curTime <= CAMERA_START_ALIGN_TIME:
                GameEnvironment.getHUD().eUpdateTimer -= self.__checkBattleCount
                if self.__defaultStrategies['CameraStrategyMouse']:
                    flexibility = self.__defaultStrategies['CameraStrategyMouse'].flexibility
                    self.__defaultStrategies['CameraStrategyMouse'].flexibility = CAMERA_ALIGN_FLEXIBILITY
                    self.__defaultStrategies['CameraStrategyMouse'].lockCursor()
                    self.__defaultStrategies['CameraStrategyMouse'].rotateCursor(0, 0)
                    BigWorld.callback(CAMERA_STOP_ALIGN_TIME, partial(self.__unlockCursor, flexibility))

    def __updateHUDProgress(self):
        arenaStartTime = BigWorld.player().arenaStartTime
        serverTime = BigWorld.serverTime()
        curTime = int(round(arenaStartTime - serverTime))
        if arenaStartTime > 0:
            if curTime <= self.__class__.PRE_INTRO_CINEMATIC_START_TIME:
                if curTime > self.__class__.PRE_INTRO_ZOOM_START_TIME:
                    if not self.__cinematicStarted:
                        player = BigWorld.player()
                        if EntityStates.inState(player, EntityStates.PRE_START_INTRO):
                            if 'scenarioCameraController' in player.controllers:
                                import BWPersonality
                                player.controllers['scenarioCameraController'].onEvent(BWPersonality.getNextIntroTimeline(), BigWorld.serverTime())
                                cinematicStartTime = self.__class__.PRE_INTRO_CINEMATIC_START_TIME - curTime
                                if cinematicStartTime < self.__class__.PRE_INTRO_CINEMATIC_START_TIME:
                                    self.getStateObject().setCinematicTime(cinematicStartTime)
                            self.__cinematicStarted = True
                elif not self.__preintroFinished:
                    curTime = clamp(0.0, curTime, self.__class__.PRE_INTRO_ZOOM_START_TIME)
                    self.__finishPreIntro(curTime)

    def __startPreIntro(self):
        if not self.__cinematicPlayed:
            self.__preIntroZoomIdxBackup = Settings.g_instance.camZoomIndex
            self.__setZoom(self.__class__.PRE_INTRO_ZOOM_IDX)
            GameEnvironment.getHUD().eUpdateTimer += self.__updateHUDProgress
            self.setZoomEnable(False)
            self.__cinematicPlayed = True

    def __finishPreIntro(self, interpTime = 0.0):
        self.__preintroFinished = True
        zoomDataIdx = self.__zoomDataIdx
        if self.__preIntroZoomIdxBackup is not None:
            self.zoomInterpolationTime = interpTime
            zoomDataIdx = self.__preIntroZoomIdxBackup
            self.__preIntroZoomIdxBackup = None
            GameEnvironment.getHUD().eUpdateTimer -= self.__updateHUDProgress
        self.__setZoom(zoomDataIdx)
        return

    def __returnToNormalFov(self):
        if self.__context is not None and self.__context.cameraSettings:
            self.__applyZoomStateFov(CAMERA_MOVING_SPEED)
        return

    def stopPreIntro(self):
        self.__finishPreIntro()
        if self.getState() == CameraState.SpectatorSide:
            self.getStateObject().setReturnToNormalTime(0.0)
            self.leaveState(CameraState.SpectatorSide)
        self.zoomInterpolationTime = CAMERA_MOVING_SPEED
        self.__preintroStopped = True
        self.setZoomEnable(True)
        BigWorld.callback(0.01, self.__returnToNormalFov)

    def __startOutro(self):
        self.__cbOutro = None
        player = BigWorld.player()
        arenaData = db.DBLogic.g_instance.getArenaData(player.arenaType)
        timelineID = arenaData.outroTimeline
        if self.getState() == CameraState.ReplayFree:
            self.leaveState(CameraState.ReplayFree)
        player.controllers['scenarioCameraController'].onEvent(timelineID, BigWorld.serverTime())
        return

    def setSniperModeType(self, type):
        self.__isLastZoomModeAirplane = type
        self.__sniperOnZoomDataIdx = self.__getCurLastZoomDataIdx()
        self.__lastZoomDataIndecesShift = 1 if self.__isLastZoomModeAirplane else 2
        if self.isSniperMode:
            self.__setZoom(self.__sniperOnZoomDataIdx)

    def __createEvents(self):
        self.__eventManager = EventManager()
        em = self.__eventManager
        self.eSetCameraRingVisible = Event(em)
        self.eStateChanged = Event(em)
        self.eZoomStateChanged = Event(em)
        self.eDistanceChanged = Event(em)
        self.eSniperMode = Event(em)
        self.eSetViewpoint = Event(em)

    def addInputListeners(self, processor):
        processor.addListeners(InputMapping.CMD_CURSOR_CAMERA, lambda : self.setState(CameraState.Free), lambda : self.leaveState(CameraState.Free))
        processor.addPredicate(InputMapping.CMD_CURSOR_CAMERA, lambda : EntityStates.inState(BigWorld.player(), EntityStates.GAME | EntityStates.PRE_START_INTRO))
        processor.addListeners(InputMapping.CMD_TARGET_CAMERA, None, None, self.setTargetCamera)
        processor.addListeners(InputMapping.CMD_SIDE_CAMERA_ALT, None, None, self.__setAltMode)
        processor.addListeners(InputMapping.CMD_SNIPER_CAMERA, None, None, self.__onSniperModeKeyPressed)
        processor.addPredicate(InputMapping.CMD_SNIPER_CAMERA, lambda : self.__sniperModeTransferFinished)
        return

    def __createMatrices(self):
        self.__mainMatrixProvider = Math.MatrixProduct()
        self.__mainMatrixProvider.a = Math.Matrix()
        self.__mainMatrixProvider.a.setIdentity()
        self.__mainMatrixProvider.b = Math.MatrixProduct()
        self.__vibrationMatrix = BigWorld.VibroMatrixProvider()
        self.__mainMatrixProvider.b.a = self.__vibrationMatrix
        self.__mainMatrixProvider.b.a.isEnable = True
        self.__cam = BigWorld.AircraftCamera()
        self.__cam.parentMatrix = self.__mainMatrixProvider
        self.__compositeOffset = Math.Vector4Morph()
        self.__compositeOffset.duration = CAMERA_MOVING_SPEED
        self.__target = Math.Vector4Morph()
        self.__target.target = Math.Vector4(0.0, 0.0, 0.0, 0.0)
        self.__target.duration = CAMERA_MOVING_SPEED
        self.__fillDefaultStrategies()

    def __calcTargetSpeed(self, targetCamSpeed):
        sensitivity = (1 - Settings.g_instance.camTargetSensitivity) ** 4.0
        return targetCamSpeed * (1.0 - sensitivity) + CAMERA_MAX_TARGET_SPEED * sensitivity

    def __fillDefaultStrategies(self):
        self.__defaultStrategies = {}
        self.__defaultStrategies['CameraStrategyMouse'] = BigWorld.CameraStrategyMouse(self.__compositeOffset, self.__target, Math.Matrix())
        self.__defaultStrategies['CameraStrategyNormal'] = BigWorld.CameraStrategyNormal(self.__compositeOffset, self.__target, Math.Matrix(), 0.0, 0.0, 0.0)
        self.__defaultStrategies['CameraStrategyGamepad'] = BigWorld.CameraStrategyGamepad(self.__compositeOffset, self.__target, Math.Matrix(), 0.0, 0.0, 0.0)

    def __appendContextParams(self, context):
        context.mainMatrixProvider = self.__mainMatrixProvider
        context.defaultStrategies = self.__defaultStrategies
        context.cameraInstance = self.__cam
        context.cameraManager = self
        context.isAltMode = self.isAltMode
        context.calcTargetSpeed = self.__calcTargetSpeed
        context.applyZoomStateFov = self.__applyZoomStateFov
        context.getCurZoomlessOffset = self.__getCurZoomlessOffset
        context.setModelVisible = self.__setModelVisible
        context.setZoom = self.__setZoom
        context.getDestZoomDataIdx = lambda : self.__zoomDataIdx

    def setCameraOffset(self, cameraOffset):
        if not self.__context.entity.isDestroyed and self.__context.entity.inWorld:
            self.__mainMatrixProvider.a.setIdentity()
            self.__mainMatrixProvider.a.setTranslate(cameraOffset)
            self.__mainMatrixProvider.b.b = self.__context.entity.realMatrix
            self.__context.mainMatrixProvider = self.__mainMatrixProvider

    def __setContext(self, context):
        self.__context = context
        self.__appendContextParams(self.__context)
        self.setCameraOffset(Math.Vector3(0.0, 0.0, 0.0))
        self.__vibrationMatrix.offsetAmplitude = self.__context.cameraSettings.vibrationAmplitudes
        self.__vibrationMatrix.offsetFreqs = self.__context.cameraSettings.vibrationFrequencies
        self.__target.target = toVec4(self.__getReductionPoint())
        strategy = self.__defaultStrategies['CameraStrategyNormal']
        strategy.sourceMatrix = self.__context.entity.realMatrix
        strategy = self.__defaultStrategies['CameraStrategyGamepad']
        strategy.speedYawPitch = self.__context.cameraSettings.camSpeedYawPitch
        strategy.speedRoll = self.__context.cameraSettings.camSpeedRoll
        strategy.speedTarget = self.__calcTargetSpeed(self.__context.cameraSettings.targetCamSpeed)
        strategy.sourceMatrix = self.__context.entity.realMatrix
        strategy = self.__defaultStrategies['CameraStrategyMouse']
        strategy.sourceMatrix = self.__context.entity.realMatrix
        CameraState.setInitParams(self.__context)
        self.__cameraStateMachine._reEnterState()

    def __getReductionPoint(self, angle = 0.0):
        reductionPointVector = self.__context.reductionPoint
        redVec = reductionPointVector * HUD_REDUCTION_POINT_SCALE
        rotMatrix = Math.Matrix()
        rotMatrix.setRotateX(angle)
        resVec = rotMatrix.applyVector(redVec)
        return resVec

    def afterLinking(self):
        super(self.__class__, self).afterLinking()
        BigWorld.camera(self.__cam)
        import BattleReplay
        if not BattleReplay.isPlaying():
            self.setSniperModeType(Settings.g_instance.getGameUI()['isSniperMode'])
            BattleReplay.g_replay.notifySniperModeType(Settings.g_instance.getGameUI()['isSniperMode'])
        if BigWorld.player().state == EntityStates.PRE_START_INTRO:
            self.eSetViewpoint(BigWorld.player().mapMatrix)
        else:
            self.eSetViewpoint(BigWorld.camera().invViewMatrix)

    def doLeaveWorld(self):
        CameraZoomStatsCollector.g_cameraZoomStatsCollector.allowProfiling(False)
        self.__cancelZoomCallback()
        if self.__cameraStateMachine:
            self.__cameraStateMachine.destroy()
            self.__cameraStateMachine = None
        BigWorld.projection().fov = self.__context.normalFov
        self.__cam.parentMatrix = Math.Matrix()
        self.__cam = None
        self.__context = None
        self.__target = None
        self.__compositeOffset = None
        self.__mainMatrixProvider.b = None
        self.__mainMatrixProvider = None
        self.__vibrationMatrix = None
        self.__defaultStrategies['CameraStrategyNormal'].sourceMatrix = Math.Matrix()
        self.__defaultStrategies['CameraStrategyMouse'].sourceMatrix = Math.Matrix()
        self.__defaultStrategies['CameraStrategyGamepad'].sourceMatrix = Math.Matrix()
        CameraState.setInitParams(None)
        super(Camera, self).doLeaveWorld()
        if self.__cbOutro:
            BigWorld.cancelCallback(self.__cbOutro)
            self.__cbOutro = None
        return

    def destroy(self):
        self.__defaultStrategies['CameraStrategyNormal'].sourceMatrix = Math.Matrix()
        self.__defaultStrategies['CameraStrategyMouse'].sourceMatrix = Math.Matrix()
        self.__defaultStrategies['CameraStrategyGamepad'].sourceMatrix = Math.Matrix()
        self.__eventManager.clear()
        super(self.__class__, self).destroy()
        self.__destroySpectatorStateMachine()

    def __destroySpectatorStateMachine(self):
        if self.__spectatorStateMachine:
            self.__spectatorStateMachine.destroy()
            self.__spectatorStateMachine = None
        return

    def reset(self):
        self.setMainEntity(BigWorld.player())
        self.__cameraStateMachine.reset()
        self.__changeInputState()

    def __changeInputState(self):
        if EntityStates.inState(BigWorld.player(), EntityStates.OBSERVER | EntityStates.DESTROYED | EntityStates.DESTROYED_FALL | EntityStates.END_GAME):
            return
        self.setState(inputToCamState[self.__inputState][self.__inputBattleMode])

    def onInputProfileChange(self, inputState):
        if self.__inputState:
            self.leaveState(inputToCamState[self.__inputState][self.__inputBattleMode])
            if self.__inputState in (INPUT_SYSTEM_STATE.MOUSE, INPUT_SYSTEM_STATE.GAMEPAD_DIRECT_CONTROL):
                self.__cam.removeShadowStrategy(self.__defaultStrategies['CameraStrategyMouse'])
        if inputState in (INPUT_SYSTEM_STATE.MOUSE, INPUT_SYSTEM_STATE.GAMEPAD_DIRECT_CONTROL):
            self.__cam.addShadowStrategy(self.__defaultStrategies['CameraStrategyMouse'])
        self.__inputState = inputState
        self.__changeInputState()

    def onBattleModeChange(self, mode):
        if self.__inputState:
            self.leaveState(inputToCamState[self.__inputState][self.__inputBattleMode])
        self.__inputBattleMode = mode
        self.__changeInputState()

    def resetBattleState(self):
        self.__changeInputState()

    def setTargetCameraOnMe(self, isOn):
        if isOn:
            self.__context.targetMatrix = self.__context.entity.realMatrix
            self.setState(CameraState.TargetMe)
        else:
            self.leaveState(CameraState.TargetMe)

    def setTargetCamera(self, targetCamera):
        if targetCamera and self.__targetEntity is not None:
            self.__context.targetMatrix = self.__targetEntity.matrix
            self.__context.targetMatrix.notModel = True
            if self.__inputState != INPUT_SYSTEM_STATE.JOYSTICK:
                self.setState(CameraState.Target)
        else:
            self.leaveState(CameraState.Target)
        if self.__inputState == INPUT_SYSTEM_STATE.JOYSTICK:
            if targetCamera:
                self.resetToZoomMin()
            else:
                self.resetToBackZoom(ignoreZoomDataIdxList=[])
        return

    def setTargetEntity(self, entity):
        needRefreshTargetMatrix = entity is not None and entity != self.__targetEntity
        self.__targetEntity = entity
        if self.getState() == CameraState.Target:
            if needRefreshTargetMatrix:
                self.setTargetCamera(True)
            elif entity is None:
                cmd = InputMapping.CMD_TARGET_CAMERA
                if InputMapping.g_instance.getSwitchingStyle(cmd) == SWITCH_STYLES_BUTTONS.SWITCH:
                    GameEnvironment.getInput().commandProcessor.getCommand(cmd).isFired = False
                self.setTargetCamera(False)
        return

    def storeBombingData(self):
        self.__bombingPrevZoomDataIdx = self.__zoomDataIdx

    def setBombingData(self):
        self.__setZoom(CAMERA_DEFAULT_BOMBING_IDX)

    def restoreBombingData(self):
        if BATTLE_MODE.ASSAULT_MODE == self.__inputBattleMode and self.__bombingPrevZoomDataIdx == CAMERA_DEFAULT_BOMBING_IDX:
            self.__setZoom(CAMERA_DEFAULT_BOMBING_IDX + 1)
        else:
            self.__setZoom(self.__bombingPrevZoomDataIdx)
        self.__bombingPrevZoomDataIdx = CAMERA_DEFAULT_BOMBING_IDX + 1

    def updateSpectator(self, vehicleID):
        currentTarget = BigWorld.entities.get(vehicleID, None)
        if currentTarget:
            self.setMainEntity(currentTarget)
            if self.__spectatorStateMachine:
                self.__spectatorStateMachine.updateTarget()
            else:
                LOG_ERROR("Unable to update spectator target: spectator controller isn't exist")
        return

    def setMainEntity(self, entity):
        """set main matrix for all camera states from entity"""
        LOG_TRACE('Camera.setMainEntity', entity.id)
        self.__setContext(CameraContext(entity))
        self.__cancelZoomCallback()
        self.__sniperModeTransferFinished = True
        self.__setModelVisible(not (self.__curZoomData.hideModel if self.__curZoomData else False))

    def onPlayerAvatarStateChanged(self, oldState, state):
        if state == EntityStates.PRE_START_INTRO:
            GameEnvironment.getHUD().eUpdateTimer += self.__checkBattleCount
        if oldState == EntityStates.PRE_START_INTRO:
            self.eSetViewpoint(BigWorld.camera().invViewMatrix)
            self.__finishPreIntro()
            self.zoomInterpolationTime = CAMERA_MOVING_SPEED
        if state & EntityStates.GAME:
            CameraZoomStatsCollector.g_cameraZoomStatsCollector.allowProfiling(True)
            CameraZoomStatsCollector.g_cameraZoomStatsCollector.onChangeZoom(self.__zoomDataIdx)
        if state & (EntityStates.DEAD | EntityStates.OUTRO):
            CameraZoomStatsCollector.g_cameraZoomStatsCollector.allowProfiling(False)
        if state & EntityStates.DEAD:
            if self.__cameraStateMachine:
                self.__cameraStateMachine.reset()
        if state == EntityStates.DESTROYED_FALL:
            self.setState(CameraState.DestroyedFall)
        elif state == EntityStates.DESTROYED:
            self.setState(CameraState.DestroyedLanded)
        elif state == EntityStates.PRE_START_INTRO:
            import BattleReplay
            if Settings.g_instance.preIntroEnabled and not BattleReplay.isPlaying():
                self.__startPreIntro()
        elif state == EntityStates.OBSERVER:
            self.setEffectsEnabled(Settings.g_instance.cameraEffectsEnabled)
        elif state == EntityStates.OUTRO:
            self.__cbOutro = BigWorld.callback(OUTRO_FADEIN_DURATION, self.__startOutro)
            self.__destroySpectatorStateMachine()

    def doAvatarLeaveWorld(self, playerAvatar, avatarId):
        if EntityStates.inState(playerAvatar, EntityStates.DESTROYED | EntityStates.OBSERVER) and self.__context.entity.id == avatarId:
            self.setMainEntity(playerAvatar)
            if self.getState() == CameraState.DestroyedFall:
                self.getStateObject().stopCollisionCheck()

    def setEffectsEnabled(self, isEnabled):
        if self.__cam:
            self.__cam.effectController.setEnabled(isEnabled or EntityStates.inState(BigWorld.player(), EntityStates.OBSERVER))
        else:
            LOG_ERROR("Cannot change camera effects state, bacause AircraftCamera isn't created yet.")

    def setSniperModeEnabled(self, isEnabled):
        if not isEnabled and self.isSniperMode:
            self.__switchSniperMode()
        self.__isSniperModeEnable = isEnabled

    def __onSniperModeKeyPressed(self, keyState):
        if InputMapping.g_instance.getSwitchingStyle(InputMapping.CMD_SNIPER_CAMERA) == SWITCH_STYLES_BUTTONS.HOLD and self.isSniperMode and keyState:
            return
        if not self.isSniperMode and not keyState:
            return
        self.__switchSniperMode()

    def __switchSniperMode(self):
        prevStateObject = None
        prevState = self.__cameraStateMachine.getPrevState()
        if prevState and self.__isSniperModeEnable and self.isSniperMode:
            prevStateObject = self.__cameraStateMachine.getStateObject(prevState)
        if self.__isSniperModeEnable and (self.getStateObject().zoomPresent() or prevStateObject and prevStateObject.zoomPresent()):
            isSniper = not self.isSniperMode
            curZoomDataIdx = self.__sniperOnZoomDataIdx if isSniper else Settings.g_instance.camZoomIndex
            self.__setZoom(curZoomDataIdx)
        return

    def __turnOnSniperMode(self, isSniper):
        if self.isSniperMode != isSniper:
            self.isSniperMode = isSniper
            self.__cam.isSniperMode = self.isSniperMode
            self.eStateChanged()
            self.eSniperMode(isSniper)

    def __setModelVisible(self, isVisible):
        self.__modelVisible = isVisible
        self.__context.entity.updateVisibility()

    def isModelVisible(self):
        return self.__modelVisible

    def setZoomEnable(self, isEnable):
        """Tutorial/Pre-Intro"""
        self.__isZoomEnable = isEnable

    def isMouseHandled(self):
        state = self.getState()
        return state in (CameraState.Free,
         CameraState.Spectator,
         CameraState.DestroyedFall,
         CameraState.DestroyedLanded,
         CameraState.SuperFree,
         CameraState.ReplayFree)

    def processMouseEvent(self, event):
        if EntityStates.inState(BigWorld.player(), EntityStates.WAIT_START | EntityStates.CREATED):
            return
        ZoomTable = self.__context.cameraSettings.zoomTable[Settings.g_instance.cameraZoomType][self.__curZoomPreset]
        if len(ZoomTable) == 0:
            return
        if not self.__cameraStateMachine.updateStateAttr(self.getState(), 'onMouseScroll', event.dz):
            stateInstance = self.getStateObject()
            if stateInstance and stateInstance.zoomPresent() and self.__isZoomEnable:
                if event.dz > 0 and self.__zoomDataIdx < self.__sniperOnZoomDataIdx or event.dz < 0 and self.__zoomDataIdx > 0:
                    if event.dz < 0.0 and self.__zoomDataIdx > 1:
                        self.__curScroll = 0.0
                    self.__curScroll += event.dz * CAMERA_SCROLL_SCALE
                    defZoomDataIdx = self.__sniperOnZoomDataIdx - self.__lastZoomDataIndecesShift
                    changed = False
                    lastStateIsBombing = ZoomTable[0].angle != 0
                    idxStep = 0
                    if self.__zoomDataIdx > 1 and self.__curScroll <= -CAMERA_SCROLL_STEP or self.__zoomDataIdx <= 1 and (self.__curScroll <= -3 * CAMERA_SCROLL_STEP and lastStateIsBombing or self.__curScroll <= -CAMERA_SCROLL_STEP and not lastStateIsBombing):
                        idxStep = -(self.__lastZoomDataIndecesShift if self.__zoomDataIdx == self.__sniperOnZoomDataIdx else 1)
                        changed = True
                    elif self.__zoomDataIdx == defZoomDataIdx and self.__curScroll >= 3 * CAMERA_SCROLL_STEP or self.__zoomDataIdx < defZoomDataIdx and self.__curScroll >= CAMERA_SCROLL_STEP:
                        idxStep = self.__lastZoomDataIndecesShift if self.__zoomDataIdx == defZoomDataIdx else 1
                        changed = True
                    if changed:
                        self.__setZoom(self.__zoomDataIdx + idxStep)
                        cmd = InputMapping.CMD_SNIPER_CAMERA
                        if InputMapping.g_instance.getSwitchingStyle(cmd) == SWITCH_STYLES_BUTTONS.SWITCH:
                            if self.__lastZoomDataIdx == self.__sniperOnZoomDataIdx and self.__zoomDataIdx < self.__sniperOnZoomDataIdx:
                                GameEnvironment.getInput().commandProcessor.getCommand(cmd).isFired = False
                            if self.__lastZoomDataIdx < self.__sniperOnZoomDataIdx and self.__zoomDataIdx == self.__sniperOnZoomDataIdx:
                                GameEnvironment.getInput().commandProcessor.getCommand(cmd).isFired = True
                        if self.__zoomDataIdx < self.__sniperOnZoomDataIdx:
                            Settings.g_instance.camZoomIndex = self.__zoomDataIdx
        else:
            camStateStrategy = self.getStateStrategy()
            if hasattr(camStateStrategy, 'distance'):
                dist = self.getStateStrategy().distance
                self.eDistanceChanged(dist)

    def __getCurLastZoomDataIdx(self):
        ZoomTable = self.__context.cameraSettings.zoomTable[Settings.g_instance.cameraZoomType][self.__curZoomPreset]
        zoomTableLen = len(ZoomTable)
        if self.__isSniperModeEnable and not self.__isLastZoomModeAirplane:
            return zoomTableLen - 1
        return zoomTableLen - 2

    def __applyZoomState(self, fastSwitch = False):
        self.__curScroll = 0
        CameraZoomStatsCollector.g_cameraZoomStatsCollector.onChangeZoom(self.__zoomDataIdx)
        self.__turnOnSniperMode(self.__zoomDataIdx == self.__sniperOnZoomDataIdx)
        if not fastSwitch:
            self.__applyZoomStateFov(self.zoomInterpolationTime)
            self.__target.duration = self.zoomInterpolationTime
            if self.__lastZoomDataIdx == self.__sniperOnZoomDataIdx or self.__zoomDataIdx == self.__sniperOnZoomDataIdx:
                self.__sniperModeTransferFinished = False
            self.__context.entity.updateVisibility()
            self.__modelVisible = self.__context.entity.model and not self.__curZoomData.hideModel and self.__sniperModeTransferFinished
            if self.__curZoomData and self.__zoomDataIdx > 2:
                if self.getState() in [CameraState.MouseCombat,
                 CameraState.NormalCombat,
                 CameraState.JoystickCombat,
                 CameraState.GamepadCombat]:
                    zoomPosClose = self.__context.cameraSettings.zoomTable[Settings.g_instance.cameraZoomType][self.__curZoomPreset][2].position
                    offset = self.__compositeOffset.target
                    scale = min(1.0, abs(offset.z / zoomPosClose.z))
                    self.__updateZoomCallback = BigWorld.callback(self.zoomInterpolationTime * 0.5 * scale, self.__onUpdateZoomCallback)
                elif self.getState() in [CameraState.MouseAssault,
                 CameraState.NormalAssault,
                 CameraState.JoystickAssault,
                 CameraState.GamepadAssault]:
                    self.__updateZoomCallback = BigWorld.callback(self.zoomInterpolationTime * 0.5, self.__onUpdateZoomCallback)
            elif self.__lastZoomDataIdx == self.__sniperOnZoomDataIdx:
                self.__updateZoomCallback = BigWorld.callback(self.zoomInterpolationTime * 0.5, self.__onUpdateZoomCallback)
            self.__updateZoomDataPosition()
        else:
            self.__sniperModeTransferFinished = True
            self.__updateZoomDataPosition()
            self.__applyZoomStateFov(0.0)
            self.__target.duration = 0.0
            self.__compositeOffset.time = self.__compositeOffset.duration
            self.__setModelVisible(not self.__curZoomData.hideModel)
        self.__target.target = toVec4(self.__getReductionPoint(math.radians(self.__curZoomData.angle)))
        if self.__cameraStateMachine.getState() is not None:
            self.getStateObject().onZoomIndexChanged(self.__zoomDataIdx, self.__curZoomData)
        self.eZoomStateChanged(self.__zoomDataIdx)
        return

    def __onUpdateZoomCallback(self):
        self.__sniperModeTransferFinished = True
        if self.__curZoomData:
            self.__modelVisible = self.__context.entity.model and not self.__curZoomData.hideModel
        if not self.__context.entity.isDestroyed and self.__context.entity.inWorld:
            self.__context.entity.updateVisibility()

    def __cancelZoomCallback(self):
        if self.__updateZoomCallback is not None:
            BigWorld.cancelCallback(self.__updateZoomCallback)
            self.__updateZoomCallback = None
        return

    def __updateZoomDataPosition(self):
        if self.getState() is not None:
            stateObject = self.getStateObject()
            self.__zoomDataPosition = stateObject.getZoomDataPosition(self.__curZoomData)
            destOffset = None
            if self.getState() in [CameraState.MouseCombat,
             CameraState.NormalCombat,
             CameraState.JoystickCombat,
             CameraState.GamepadCombat] and self.__zoomDataIdx < 3:
                offset = toVec4(self.__zoomDataPosition) + self.__effectOffset
                offset.z = offset.z * self.__FOVDistanceCorrection
                destOffset = offset
            else:
                destOffset = toVec4(self.__zoomDataPosition) + self.__effectOffset
            if destOffset != self.__compositeOffset.target:
                self.__compositeOffset.target = destOffset
        return

    def __setZoom(self, zoomDataIdx, zoomPreset = None):
        if self.__context:
            import BattleReplay
            BattleReplay.g_replay.notifyZoomChange(zoomDataIdx, zoomPreset)
            self.__lastZoomDataIdx = self.__zoomDataIdx
            self.__zoomDataIdx = zoomDataIdx
            if zoomPreset is not None:
                self.__curZoomPreset = zoomPreset
            self.__curZoomData = self.__context.cameraSettings.zoomTable[Settings.g_instance.cameraZoomType][self.__curZoomPreset][self.__zoomDataIdx]
            if self.zoomPresent():
                self.__applyZoomState(zoomDataIdx == self.__sniperOnZoomDataIdx)
        return

    def __getCurZoomlessOffset(self):
        if self.isSniperMode:
            return self.__context.cameraSettings.zoomTable[Settings.g_instance.cameraZoomType][self.__curZoomPreset][Settings.g_instance.camZoomIndex].position
        else:
            return self.__zoomDataPosition

    def resetToMinZoom(self):
        """TO REMOVE"""
        self.__setZoom(0)

    def resetToZoomMin(self):
        zoomDataIdx = 0
        self.__backToCurrentZoomDataIdx = self.__zoomDataIdx
        self.__setZoom(zoomDataIdx)

    def resetToBackZoom(self, ignoreZoomDataIdxList = [3, 4]):
        if self.__backToCurrentZoomDataIdx is not None:
            if self.__backToCurrentZoomDataIdx not in ignoreZoomDataIdxList:
                self.__setZoom(self.__backToCurrentZoomDataIdx)
            cmd = InputMapping.CMD_SNIPER_CAMERA
            if InputMapping.g_instance.getSwitchingStyle(cmd) == SWITCH_STYLES_BUTTONS.SWITCH:
                if self.__backToCurrentZoomDataIdx == self.__sniperOnZoomDataIdx and self.__zoomDataIdx < self.__sniperOnZoomDataIdx:
                    GameEnvironment.getInput().commandProcessor.getCommand(cmd).isFired = False
            self.__backToCurrentZoomDataIdx = None
        return

    def zoomPresent(self):
        if self.__cameraStateMachine is not None:
            return self.getStateObject().zoomPresent()
        else:
            return False

    def update(self):
        if self.getState() is not None and self.__curZoomData is not None and EntityStates.inState(BigWorld.player(), EntityStates.GAME):
            self.__updateZoomDataPosition()
            self.getStateObject().onZoomIndexChanged(self.__zoomDataIdx, self.__curZoomData)
        return

    def __setAltMode(self, value):
        if value != self.__altMode:
            self.__altMode = value
            self.__cameraStateMachine._reEnterState()

    def isAltMode(self):
        return self.__altMode

    def updateStateAttr(self, stateName, attrName, attrValue):
        return self.__cameraStateMachine.updateStateAttr(stateName, attrName, attrValue)

    def onEnterSideView(self, stateData, cameraFreezed):
        if cameraFreezed:
            if self.getState() != CameraState.FreeFixable:
                self.setState(CameraState.FreeFixable)
            self.__cameraStateMachine.updateStateAttr(CameraState.FreeFixable, 'rotationPower', stateData[1])
        else:
            state = stateData[0]
            self.setState(state)

    def onLeaveSideView(self, stateData, cameraFreezed):
        if cameraFreezed:
            self.__cameraStateMachine.updateStateAttr(CameraState.FreeFixable, 'rotationPower', (0, 0))
        else:
            state = stateData[0]
            self.leaveState(state)

    def getFOV(self):
        return BigWorld.projection().fov

    def convertToVerticalFOV(self, horizontalFOV):
        return math.degrees(2.0 * math.atan(math.tan(math.radians(horizontalFOV) * 0.5) / BigWorld.projection().aspect))

    def __applyZoomStateFov(self, speed, forceCombatMode = False):
        defaultFov = math.radians(self.__context.cameraSettings.defaultFov) * self.__curZoomData.fovPercent
        state = self.getState()
        if (forceCombatMode or state in [CameraState.MouseCombat,
         CameraState.NormalCombat,
         CameraState.JoystickCombat,
         CameraState.GamepadCombat]) and self.__zoomDataIdx < 3:
            minDistanceFov = self.__context.cameraSettings.minMouseCombatFov
            delta = self.__maxDistanceFOV - minDistanceFov
            fovDeg = math.ceil(minDistanceFov + delta * (1.0 - float(self.__zoomDataIdx) * 0.5))
            fov = math.radians(self.convertToVerticalFOV(fovDeg))
            self.__FOVDistanceCorrection = math.tan(defaultFov * self.__effectFOV * 0.5) / math.tan(fov * self.__effectFOV * 0.5)
            if speed == 0:
                BigWorld.projection().fov = fov
            else:
                arenaStartTime = BigWorld.player().arenaStartTime
                serverTime = BigWorld.serverTime()
                curTime = int(round(arenaStartTime - serverTime))
                if not self.__preintroStopped and curTime > self.__class__.PRE_INTRO_ZOOM_START_TIME and curTime < self.__class__.PRE_INTRO_CINEMATIC_START_TIME:
                    speed = curTime * 0.5
                fov = fov * self.__effectFOV
        else:
            self.__FOVDistanceCorrection = 1.0
            if speed == 0:
                BigWorld.projection().fov = defaultFov
            fov = defaultFov * self.__effectFOV
        BigWorld.projection().rampFov(fov, speed, self.__context.cameraSettings.fovRampCurvature)

    def setState(self, newState, params = None):
        """
        @param newState: stateID
        """
        if newState not in cameraStatesWithZoom:
            CameraZoomStatsCollector.g_cameraZoomStatsCollector.onChangeZoom(None)
        import BattleReplay
        BattleReplay.g_replay.notifyCameraState(newState, True)
        prevState = self.getState()
        if prevState != CameraState.SuperFree and self.__cameraStateMachine:
            self.__cameraStateMachine.setState(newState, params)
            if newState in [CameraState.MouseCombat,
             CameraState.NormalCombat,
             CameraState.JoystickCombat,
             CameraState.GamepadCombat]:
                self.__applyZoomStateFov(self.zoomInterpolationTime)
            self.eStateChanged()
        return

    def setPrevState(self, newState):
        self.__cameraStateMachine.setPrevState(newState)

    def onHideBackendGraphics(self):
        """
        @return:
        """
        self.__checkSideCameraOnSwitchingInput()

    def leaveState(self, state = None):
        """
        @param state:
        @return:
        """
        if self.__cameraStateMachine:
            import BattleReplay
            BattleReplay.g_replay.notifyCameraState(state if state is not None else self.getState(), False)
            self.__cameraStateMachine.leaveState(state)
            if self.getState() in [CameraState.MouseCombat,
             CameraState.NormalCombat,
             CameraState.JoystickCombat,
             CameraState.GamepadCombat]:
                self.__applyZoomStateFov(self.zoomInterpolationTime)
            self.eStateChanged()
        return

    def stateObject(self, state):
        """
        @param state: camera state object with  stateID==state
        @return:
        """
        if self.__cameraStateMachine:
            return self.__cameraStateMachine.getStateObject(state)

    def getStateObject(self):
        """
        @return: current camera object
        """
        return self.__cameraStateMachine.getCurStateObject()

    def getState(self):
        """
        @return: current camera stateID
        """
        if self.__cameraStateMachine:
            return self.__cameraStateMachine.getState()

    def getStateStrategy(self):
        """
        @return: current camera state strategy
        """
        stateObj = self.getStateObject()
        if stateObj:
            return stateObj.strategy

    @property
    def getDefualtStrategies(self):
        return self.__defaultStrategies

    def __checkSideCameraOnSwitchingInput(self):
        if self.getState() not in [CameraState.DestroyedFall,
         CameraState.DestroyedLanded,
         CameraState.Spectator,
         CameraState.SuperFree,
         CameraState.NormalCombat,
         CameraState.NormalAssault,
         CameraState.GamepadCombat,
         CameraState.GamepadAssault]:
            self.reset()

    def onFlyKeyBoardInputAllowed(self, flag, playerAvatar):
        if not flag and EntityStates.inState(playerAvatar, EntityStates.GAME):
            if self.getState() not in [CameraState.DebugCamera,
             CameraState.Spectator,
             CameraState.DestroyedFall,
             CameraState.DestroyedLanded,
             CameraState.SuperFree,
             CameraState.ReplayFree]:
                self.reset()

    def getAircraftCam(self):
        return self.__cam

    def setEffectMove(self, offset):
        self.__effectOffset = offset

    @property
    def debugMode(self):
        return self.__cam.debugCamera != None

    @debugMode.setter
    def debugMode(self, value):
        """For camera debuging - visualization off camera source-target and up vectors"""
        if value:
            self.__cam.debugCamera = BigWorld.CursorCamera()
            self.__cam.debugCamera.target = BigWorld.player().realMatrix
            self.__cam.debugCamera.source = BigWorld.dcursor().matrix
            self.__cam.debugCamera.pivotPosition = Math.Vector3(0, 0, 0)
            self.__cam.debugCamera.pivotMaxDist = 50.0
        else:
            self.__cam.debugCamera.target = None
            self.__cam.debugCamera.source = None
            self.__cam.debugCamera = None
        return

    def getDistanceToSource(self):
        camera_pos = BigWorld.camera().position
        source_pos = Math.Matrix(self.__context.mainMatrixProvider).applyToOrigin()
        return (camera_pos - source_pos).length

    def getCurStateName(self):
        id = self.getState()
        for k, v in CameraState.__dict__.items():
            if v == id:
                return k

        return 'UNKNOWN_STATE'

    def setFov(self, newFov):
        curStateObj = self.getStateObject()
        if curStateObj.zoomPresent():
            self.__context.cameraSettings.defaultFov = newFov
        else:
            BigWorld.projection().rampFov(math.radians(newFov), 0.0)

    def setPos(self, newPos):
        curState = self.getState()
        curStateObj = self.__cameraStateMachine.getStateObject(self.__cameraStateMachine.getState())
        if curState == CameraState.Left:
            self.__context.cameraSettings.leftCamPos = newPos
            curStateObj._setTransformation(self.__context.cameraSettings.leftCamPos, self.__context.cameraSettings.leftCamDir, Math.Vector3(0.0, 1.0, 0.0))
            curStateObj.reEnter()
        elif curState == CameraState.Right:
            self.__context.cameraSettings.rightCamPos = newPos
            curStateObj._setTransformation(self.__context.cameraSettings.rightCamPos, self.__context.cameraSettings.rightCamDir, Math.Vector3(0.0, 1.0, 0.0))
            curStateObj.reEnter()
        elif curState == CameraState.Top:
            self.__context.cameraSettings.topCamPos = newPos
            curStateObj._setTransformation(self.__context.cameraSettings.topCamPos, self.__context.cameraSettings.topCamDir, Math.Vector3(0.0, 0.0, -1.0))
            curStateObj.reEnter()
        elif curState == CameraState.Bottom:
            self.__context.cameraSettings.bottomCamPos = newPos
            curStateObj._setTransformation(self.__context.cameraSettings.bottomCamPos, self.__context.cameraSettings.bottomCamDir, Math.Vector3(0.0, 0.0, 1.0))
            curStateObj.reEnter()
        elif curState in (CameraState.Free, CameraState.ReplayFree):
            pass
        elif curState == CameraState.SuperFree:
            pass
        else:
            self.__curZoomData.position = newPos

    def getPos(self):
        curState = self.getState()
        if curState == CameraState.Left:
            return self.__context.cameraSettings.leftCamPos
        if curState == CameraState.Right:
            return self.__context.cameraSettings.rightCamPos
        if curState == CameraState.Top:
            return self.__context.cameraSettings.topCamPos
        if curState == CameraState.Bottom:
            return self.__context.cameraSettings.bottomCamPos
        if curState in (CameraState.Free, CameraState.ReplayFree):
            return self.__getCurZoomlessOffset().length
        if curState == CameraState.SuperFree:
            return BigWorld.dcursor().matrix
        return self.__zoomDataPosition

    def setCameraPosQA(self, x, y, z):
        m = Math.Matrix(BigWorld.player().matrix)
        y = -y if z > 0 else y
        x = -x
        v = Math.Vector3(x, y, z)
        m1 = Math.Matrix()
        m1.setIdentity()
        m1.lookAt((0, 0, 0), v, (0, 1, 0))
        m.setRotateYPR(Math.Vector3(m.yaw + m1.yaw, m.pitch + m1.pitch, m.roll))
        self.__context.mainMatrixProvider = m
        self.setState(CameraState.SuperFree)
        strategy = self.getStateStrategy()
        strategy.distance = v.length

    def resetCameraPosQA(self):
        self.leaveState(CameraState.SuperFree)
        self.__context.mainMatrixProvider = self.__mainMatrixProvider