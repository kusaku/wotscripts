# Embedded file name: scripts/client/BattleReplay.py
import base64
import datetime
from EntityHelpers import extractGameMode
from Event import Event, EventManager
import GlobalEvents
from gui.Version import Version
import json
import cPickle
import Math
from trace import pickle
import Settings
from debug_utils import *
from ConnectionManager import connectionManager
import db.DBLogic
import Keys
import InputMapping
from Helpers.i18n import localizeHUD
import os.path
from wofdecorators import noexcept
import GameEnvironment
from CameraStates import CameraState
import consts
from Helpers.cleaner import deleteOldFiles
from functools import partial
g_replay = None
TIME_FOR_SHOW_PANEL = 0.1
TIME_FOR_HIDE_PANEL = 20 + TIME_FOR_SHOW_PANEL
BATTLE_REPLAY_SCROLL_SCALE = 0.01
REPLAY_FILE_EXTENSION = '.wowpreplay'
REPLAYS_DIR_NAME = 'replays'
AUTO_RECORD_TEMP_FILENAME = 'temp'
FIXED_REPLAY_FILENAME = 'replay_last_battle'
REPLAY_TIME_MARK_CLIENT_READY = 2147483648L
REPLAY_TIME_MARK_REPLAY_FINISHED = 2147483649L
REPLAY_TIME_MARK_CURRENT_TIME = 2147483650L
REPLAY_TIME_MARK_ARENA_LOADED = 1
FAST_FORWARD_STEP = 20.0
ACTION_HOME = 0
ACTION_BACK = 1
ACTION_PLAY = 2
ACTION_PAUSE = 3
ACTION_FORWARD = 4
ACTION_END = 5
ACTION_SPEED_DEC = 6
ACTION_SPEED_INC = 7
ACTION_BACK_2 = 10
ACTION_FORWARD_2 = 11
ACTION_CAMERA_SWITCH = 12

class BattleReplay():
    isPlaying = property(lambda self: self.__replayCtrl.isPlaying)
    isRecording = property(lambda self: self.__replayCtrl.isRecording)
    isClientReady = property(lambda self: self.__replayCtrl.isClientReady)
    isControllingCamera = property(lambda self: self.__replayCtrl.isControllingCamera)
    isOffline = property(lambda self: self.__replayCtrl.isOfflinePlaybackMode)
    isTimeWarpInProgress = property(lambda self: self.__replayCtrl.isTimeWarpInProgress or self.__timeWarpCleanupCb is not None)
    playerVehicleID = property(lambda self: self.__replayCtrl.playerVehicleID)
    fps = property(lambda self: self.__replayCtrl.fps)
    ping = property(lambda self: self.__replayCtrl.ping)
    isLaggingNow = property(lambda self: self.__replayCtrl.isLaggingNow)
    playbackSpeed = property(lambda self: self.__replayCtrl.playbackSpeed)
    replayContainsGunReloads = property(lambda self: self.__replayCtrl.replayContainsGunReloads)
    scriptModalWindowsEnabled = property(lambda self: self.__replayCtrl.scriptModalWindowsEnabled)
    startServerTime = property(lambda self: self.__replayCtrl.arenaStartServerTime)

    def __init__(self):
        global g_replay
        userPrefs = Settings.g_instance.userPrefs
        if not userPrefs.has_key(Settings.KEY_REPLAY_PREFERENCES):
            userPrefs.write(Settings.KEY_REPLAY_PREFERENCES, '')
        self.__settings = userPrefs[Settings.KEY_REPLAY_PREFERENCES]
        self.__fileName = None
        self.__replayCtrl = BigWorld.WGReplayController(BigWorld.getMinCompatibleClientVersion())
        self.__replayCtrl.replayFinishedCallback = self.onReplayFinished
        self.__replayCtrl.controlModeChangedCallback = self.onControlModeChanged
        self.__replayCtrl.ammoButtonPressedCallback = self.onAmmoButtonPressed
        self.__replayCtrl.minimapCellClickedCallback = self.onMinimapCellClicked
        self.__replayCtrl.playerVehicleIDChangedCallback = self.onPlayerVehicleIDChanged
        self.__replayCtrl.clientVersionDiffersCallback = self.onClientVersionDiffers
        self.__replayCtrl.battleChatMessageCallback = self.onBattleChatMessage
        self.__replayCtrl.beforeBasePlayerCreateCallback = self.__startAutoRecord
        self.__replayCtrl.applyInputAxisCallback = self.__applyInputAxis
        self.__replayCtrl.applyTargetEntityCallback = self.__applyTargetEntity
        self.__replayCtrl.applyZoomChangeCallback = self.__applyZoomChange
        self.__replayCtrl.cameraStateChangedCallback = self.__applyCameraState
        self.__replayCtrl.setSniperModeTypeCallback = self.__applySniperModeType
        self.__replayCtrl.currentControlsChangedCallback = self.__applyCurrentControls
        self.__replayCtrl.flapsMessageCallback = self.onFlapsMessage
        self.__replayCtrl.applyTargetLockCallback = self.__applyTargetLock
        self.__replayCtrl.timeMarkerCallback = self.__timeMarkerCallback
        self.__isAutoRecordingEnabled = False
        self.__quitAfterStop = False
        self.__isPlayingPlayList = False
        self.__playList = []
        self.__playerDatabaseID = 0
        self.__playbackSpeedModifiers = (0.0, 0.125, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0)
        self.__playbackSpeedModifiersStr = ('0', '1/8', '1/4', '1/2', '1', '2', '4', '8', '16')
        self.__playbackSpeedIdx = self.__playbackSpeedModifiers.index(1.0)
        self.__replayDir = BigWorld.getReplaysDirectory()
        self.__replayCtrl.clientVersion = Version().getVersion()
        self.__timeWarpCleanupCb = None
        self.__enableTimeWarp = False
        self.__disableSidePanelContextMenuCb = None
        self.enableAutoRecordingBattles(Settings.g_instance.getReplaySettings()['saveBattleReplays'])
        em = self.__eventMgr = EventManager()
        self.eInitHUD = Event(em)
        self.eUpdateHUDProgress = Event(em)
        self.eUpdateHUDButtons = Event(em)
        self.eShowMessageHUD = Event(em)
        self.eShowFinish = Event(em)
        self.eMuteSound = Event(em)
        self.eShowPanel = Event(em)
        self.eHidePanel = Event(em)
        self.__playbackLength = 0
        self.__freeCameraMode = False
        self.__firstTimeHUDInit = True
        self.__callbackShowPanel = None
        self.__callbackHidePanel = None
        self.__curScroll = 0.0
        self.__arenaLoaded = False
        self.__dataForSyncCameraState = {'next': [],
         'applied': []}
        self.__setSniperModeTypeCbHandler = None
        g_replay = self
        return

    def startRecord(self):
        self.__startAutoRecord()

    def afterLinking(self):
        GlobalEvents.onKeyEvent += self.handleKeyEvent
        GlobalEvents.onMouseEvent += self.handleMouseEvent
        InputMapping.g_instance.onSaveControls += self.__onSaveControls
        self.__replayCtrl.onSyncPoint1()

    def doLeaveWorld(self):
        InputMapping.g_instance.onSaveControls -= self.__onSaveControls
        GlobalEvents.onMouseEvent -= self.handleMouseEvent
        GlobalEvents.onKeyEvent -= self.handleKeyEvent
        if self.isRecording:
            self.stop()
            self.setPlayerVehicleID(0)

    @property
    def guiWindowManager(self):
        from gui.WindowsManager import g_windowsManager
        return g_windowsManager

    def destroy(self):
        global g_replay
        self.stop()
        self.__eventMgr.clear()
        self.enableAutoRecordingBattles(False)
        self.__replayCtrl.replayFinishedCallback = None
        self.__replayCtrl.controlModeChangedCallback = None
        self.__replayCtrl.clientVersionDiffersCallback = None
        self.__replayCtrl.playerVehicleIDChangedCallback = None
        self.__replayCtrl.battleChatMessageCallback = None
        self.__replayCtrl.ammoButtonPressedCallback = None
        self.__replayCtrl.minimapCellClickedCallback = None
        self.__replayCtrl.beforeBasePlayerCreateCallback = None
        self.__replayCtrl = None
        if self.__timeWarpCleanupCb is not None:
            BigWorld.cancelCallback(self.__timeWarpCleanupCb)
            self.__timeWarpCleanupCb = None
        if self.__setSniperModeTypeCbHandler is not None:
            BigWorld.cancelCallback(self.__setSniperModeTypeCbHandler)
            self.__setSniperModeTypeCbHandler = None
        g_replay = None
        return

    def record(self, fileName = None):
        if self.isPlaying:
            LOG_WARNING('BattleReplay::startRecording isPlaying')
            return False
        elif self.isRecording:
            LOG_WARNING('BattleReplay::startRecording isRecording')
            return self.__fileName == fileName
        else:
            if fileName is None:
                fileName = os.path.join(self.__replayDir, AUTO_RECORD_TEMP_FILENAME + REPLAY_FILE_EXTENSION)
                try:
                    if not os.path.isdir(self.__replayDir):
                        os.makedirs(self.__replayDir)
                except:
                    LOG_ERROR('Failed to create directory for replay files')
                    return False

            try:
                f = open(fileName, 'wb')
                f.close()
                os.remove(fileName)
            except:
                LOG_ERROR('Failed to create replay file, replays folder may be write-protected')
                return False

            if self.__replayCtrl.startRecording(fileName):
                LOG_TRACE('BattleReplay::startRecording({0})'.format(fileName))
                self.__fileName = fileName
                self.__arenaLoaded = False
                return True
            return False
            return

    def play(self, fileName = None):
        if self.isRecording:
            self.stop()
        elif self.isPlaying:
            return self.__fileName == fileName
        BattleReplay.patchPickle()
        if fileName is not None and fileName.rfind('.wowpreplaylist') != -1:
            self.__playList = []
            self.__isPlayingPlayList = True
            try:
                f = open(fileName)
                s = f.read()
                f.close()
                self.__playList = s.replace('\r\n', '\n').replace('\r', '\n').split('\n')
                fileName = None
            except:
                pass

        if fileName is None:
            if len(self.__playList) == 0:
                return False
            fileName = self.__playList[0]
            self.__playList.pop(0)
            self.__quitAfterStop = len(self.__playList) == 0
        self.__fileName = fileName
        if self.__replayCtrl.startPlayback(fileName):
            self.__playbackSpeedIdx = self.__playbackSpeedModifiers.index(1.0)
            self.__savedPlaybackSpeedIdx = self.__playbackSpeedIdx
            self.__dataForSyncCameraState['next'] = []
            self.__dataForSyncCameraState['applied'] = []
            return True
        else:
            self.__fileName = None
            return False
            return

    def stop(self, rewindToTime = None, removeFile = False):
        LOG_TRACE('BattleReplay::stop')
        if not self.isPlaying and not self.isRecording:
            return False
        else:
            wasPlaying = self.isPlaying
            isOffline = self.__replayCtrl.isOfflinePlaybackMode
            self.__replayCtrl.stop(removeFile)
            self.__fileName = None
            if self.__disableSidePanelContextMenuCb is not None:
                BigWorld.cancelCallback(self.__disableSidePanelContextMenuCb)
                self.__disableSidePanelContextMenuCb = None
            if wasPlaying:
                if not isOffline:
                    connectionManager.onDisconnected += self.__showLoginPage
                BigWorld.clearEntitiesAndSpaces()
                BigWorld.disconnect()
                if self.__quitAfterStop:
                    BigWorld.quit()
                elif isOffline:
                    self.__showLoginPage()
            return

    @noexcept
    def __removeReplayFile(self):
        os.remove(self.__fileName)

    @staticmethod
    def patchPickle():
        import SafeUnpickler
        unpickler = SafeUnpickler.SafeUnpickler()
        cPickle.loads = unpickler.loads
        import wgPickle
        reload(wgPickle)
        LOG_TRACE('BattleReplay::patchPickle')

    @staticmethod
    def autoStartBattleReplay():
        fileName = BigWorld.getAutoStartReplayFileName()
        if fileName != '':
            if g_replay == None:
                BattleReplay()
            g_replay.__quitAfterStop = True
            return g_replay.play(fileName)
        else:
            return False

    def getReplayTime(self):
        return self.__replayCtrl.getTimeMark(REPLAY_TIME_MARK_CURRENT_TIME)

    def getReplayLength(self):
        return self.__replayCtrl.getTimeMark(REPLAY_TIME_MARK_REPLAY_FINISHED)

    def handleKeyEvent(self, event):
        if not (self.isPlaying and self.isClientReady):
            return False
        if event.key == Keys.KEY_HOME and event.isKeyDown() and not event.isCtrlDown():
            self.__action(ACTION_HOME)
            return True

    def handleMouseEvent(self, event):
        if not (self.isPlaying and self.isClientReady):
            return False
        if BigWorld.isKeyDown(Keys.KEY_LSHIFT, 0) or BigWorld.isKeyDown(Keys.KEY_RSHIFT, 0):
            if event.dz != 0:
                if event.dz > 0:
                    if self.__curScroll < 0:
                        self.__curScroll = 0
                elif event.dz < 0:
                    if self.__curScroll > len(self.__playbackSpeedModifiers):
                        self.__curScroll = len(self.__playbackSpeedModifiers)
                self.__curScroll += event.dz * BATTLE_REPLAY_SCROLL_SCALE
                if int(self.__curScroll) > self.__playbackSpeedIdx:
                    self.__action(ACTION_SPEED_INC)
                    return True
                if int(self.__curScroll) < self.__playbackSpeedIdx:
                    self.__action(ACTION_SPEED_DEC)
                    return True
        return False

    def addInputListeners(self, processor):
        ctrlBtn = lambda : BigWorld.isKeyDown(Keys.KEY_LCONTROL, 0) or BigWorld.isKeyDown(Keys.KEY_RCONTROL, 0)
        shiftBtn = lambda : BigWorld.isKeyDown(Keys.KEY_LSHIFT, 0) or BigWorld.isKeyDown(Keys.KEY_RSHIFT, 0)
        cmdList = [InputMapping.CMD_REPLAY_PLAYPAUSE,
         InputMapping.CMD_REPLAY_CAMERA_SWITCH,
         InputMapping.CMD_REPLAY_SPEED_DEC,
         InputMapping.CMD_REPLAY_SPEED_INC,
         InputMapping.CMD_REPLAY_FORWARD,
         InputMapping.CMD_REPLAY_BACK,
         InputMapping.CMD_REPLAY_END]
        for cmd in cmdList:
            processor.addPredicate(cmd, lambda : self.isPlaying and not ctrlBtn() and self.__arenaLoaded and not self.isTimeWarpInProgress)

        processor.addListeners(InputMapping.CMD_REPLAY_PLAYPAUSE, lambda : self.__action(ACTION_PLAY if self.__playbackSpeedIdx == 0 else ACTION_PAUSE))
        processor.addListeners(InputMapping.CMD_REPLAY_CAMERA_SWITCH, lambda : self.__action(ACTION_CAMERA_SWITCH))
        processor.addListeners(InputMapping.CMD_REPLAY_SPEED_DEC, lambda : self.__action(ACTION_SPEED_DEC))
        processor.addListeners(InputMapping.CMD_REPLAY_SPEED_INC, lambda : self.__action(ACTION_SPEED_INC))
        processor.addListeners(InputMapping.CMD_REPLAY_FORWARD, lambda : self.__action(ACTION_FORWARD_2 if shiftBtn() else ACTION_FORWARD))
        processor.addListeners(InputMapping.CMD_REPLAY_BACK, lambda : self.__action(ACTION_BACK_2 if shiftBtn() else ACTION_BACK))
        processor.addListeners(InputMapping.CMD_REPLAY_END, lambda : self.__action(ACTION_END))

    def setGunRotatorTargetPoint(self, value):
        self.__replayCtrl.gunRotatorTargetPoint = value

    def getGunRotatorTargetPoint(self):
        return self.__replayCtrl.gunRotatorTargetPoint

    def setGunMarkerParams(self, diameter, pos, dir):
        self.__replayCtrl.gunMarkerDiameter = diameter
        self.__replayCtrl.gunMarkerPosition = pos
        self.__replayCtrl.gunMarkerDirection = dir

    def getGunMarkerParams(self, defaultPos, defaultDir):
        diameter = self.__replayCtrl.gunMarkerDiameter
        dir = self.__replayCtrl.gunMarkerDirection
        pos = self.__replayCtrl.gunMarkerPosition
        if dir == Math.Vector3(0, 0, 0):
            pos = defaultPos
            dir = defaultDir
        return (diameter, pos, dir)

    def setArcadeGunMarkerSize(self, size):
        self.__replayCtrl.setArcadeGunMarkerSize(size)

    def getArcadeGunMarkerSize(self):
        return self.__replayCtrl.getArcadeGunMarkerSize()

    def setSPGGunMarkerParams(self, dispersionAngle, size):
        self.__replayCtrl.setSPGGunMarkerParams((dispersionAngle, size))

    def getSPGGunMarkerParams(self):
        return self.__replayCtrl.getSPGGunMarkerParams()

    def setTurretYaw(self, value):
        self.__replayCtrl.turretYaw = value

    def getTurretYaw(self):
        return self.__replayCtrl.turretYaw

    def setGunPitch(self, value):
        self.__replayCtrl.gunPitch = value

    def getGunPitch(self):
        return self.__replayCtrl.gunPitch

    def getGunReloadAmountLeft(self):
        return self.__replayCtrl.getGunReloadAmountLeft()

    def setGunReloadTime(self, startTime, duration):
        self.__replayCtrl.setGunReloadTime(startTime, duration)

    def getConsumableSlotCooldownAmount(self, idx):
        return self.__replayCtrl.getConsumableSlotCooldownAmount(idx)

    def setConsumableSlotCooldown(self, idx, cooldown, addToExistingCooldown):
        self.__replayCtrl.setConsumableSlotCooldown(idx, cooldown, addToExistingCooldown)

    def setArenaPeriod(self, value):
        self.__replayCtrl.arenaPeriod = value

    def getArenaPeriod(self):
        ret = self.__replayCtrl.arenaPeriod
        return ret

    def setPlayerVehicleID(self, vehicleID):
        self.__replayCtrl.playerVehicleID = vehicleID

    def setPlaybackSpeedIdx(self, value):
        self.__savedPlaybackSpeedIdx = self.__playbackSpeedIdx
        self.__playbackSpeedIdx = value
        oldSpeed = self.__playbackSpeedModifiers[self.__savedPlaybackSpeedIdx]
        oldQuiet = oldSpeed != 1
        newSpeed = self.__playbackSpeedModifiers[self.__playbackSpeedIdx]
        newQuiet = newSpeed != 1
        if oldQuiet != newQuiet:
            self.eMuteSound(newQuiet)
        self.__replayCtrl.playbackSpeed = newSpeed
        if newSpeed == 0:
            BigWorld.callback(0, self.__updateAim)
        self.__updateHUDButtons()

    def getPlaybackSpeedIdx(self):
        ret = self.__playbackSpeedModifiers.index(self.__replayCtrl.playbackSpeed)
        if ret == -1:
            return self.__playbackSpeedModifiers.index(1.0)
        return ret

    def setControlMode(self, value):
        self.__replayCtrl.controlMode = value

    def getControlMode(self):
        return self.__replayCtrl.controlMode

    def onClientReady(self):
        if not (self.isPlaying or self.isRecording):
            return
        player = BigWorld.player()
        if self.isRecording and 'tutorialManager' in BigWorld.player().controllers:
            self.stop(removeFile=True)
            return
        self.__replayCtrl.playerVehicleID = player.id
        self.__replayCtrl.onClientReady()
        if self.isRecording:
            arenaData = db.DBLogic.g_instance.getArenaData(player.arenaType)
            nowT = datetime.datetime.now()
            now = '%02d.%02d.%04d %02d:%02d:%02d' % (nowT.day,
             nowT.month,
             nowT.year,
             nowT.hour,
             nowT.minute,
             nowT.second)
            vehicle = db.DBLogic.g_instance.getAircraftData(player.planeID).airplane
            arenaInfo = {'dateTime': now,
             'playerName': player.objectName,
             'myID': player.id,
             'playerVehicle': vehicle.name,
             'mapName': arenaData.typeName,
             'mapDisplayName': arenaData.typeName,
             'gameplayID': extractGameMode(player.gameMode),
             'clientVersion': str(Version().getVersion()).strip()}
            self.__replayCtrl.recMapName = arenaData.typeName
            self.__replayCtrl.recPlayerVehicleName = vehicle.name
            self.__replayCtrl.setArenaInfoStr(json.dumps(arenaInfo))
            filename = '%s' % nowT.strftime('%y%m%d_%H%M%S')
            filename = '%s_%s' % (filename, vehicle.country)
            filename = '%s_%s' % (filename, 'X' if vehicle.level == 10 else str(vehicle.level))
            filename = '%s_%s' % (filename, vehicle.name)
            filename = '%s_%s' % (filename, arenaData.typeName)
            self.setResultingFileName(filename)
            self.__onSaveControls()
        else:
            self.__enableTimeWarp = True
            self.__initHUD()
            self.__syncCameraState()
            if self.__freeCameraMode:
                cam = GameEnvironment.getCamera()
                cam.setState(CameraState.ReplayFree)
                GlobalEvents.onMouseEvent += cam.processMouseEvent

    def __getArenaVehiclesInfo(self):
        vehicles = {}
        for k, v in db.DBLogic.g_instance.getAircraftsDict().iteritems():
            vehicles[k] = v.airplane.name

        return vehicles

    def onBattleSwfLoaded(self):
        if self.isPlaying:
            self.__replayCtrl.onBattleSwfLoaded()

    def onCommonSwfLoaded(self):
        self.__enableTimeWarp = False

    def onCommonSwfUnloaded(self):
        self.__enableTimeWarp = True

    def onReplayFinished(self):
        self.setPlaybackSpeedIdx(0)
        self.eShowFinish()
        return
        if not self.scriptModalWindowsEnabled:
            self.stop()
            return
        if self.__isPlayingPlayList:
            self.stop()
            BigWorld.callback(1.0, self.play)
            return

    def onControlModeChanged(self, forceControlMode = None):
        player = BigWorld.player()
        if not self.isPlaying or not isPlayerAvatar():
            return
        elif not self.isControllingCamera and forceControlMode is None:
            return
        else:
            controlMode = self.getControlMode() if forceControlMode is None else forceControlMode
            player.inputHandler.onControlModeChanged(controlMode, camMatrix=BigWorld.camera().matrix, preferredPos=self.getGunRotatorTargetPoint(), saveZoom=False, saveDist=False)
            return

    def onPlayerVehicleIDChanged(self):
        player = BigWorld.player()
        if self.isPlaying and hasattr(player, 'positionControl'):
            player.positionControl.bindToVehicle(True, self.__replayCtrl.playerVehicleID)
            self.onControlModeChanged()

    def onAmmoButtonPressed(self, idx):
        return
        player = BigWorld.player()
        if not isPlayerAvatar():
            return
        if self.isPlaying:
            player.onAmmoButtonPressed(idx)
        elif self.isRecording:
            self.__replayCtrl.onAmmoButtonPressed(idx)

    def onBattleChatMessage(self, messageText, isCurrentPlayer):
        return
        if self.isRecording:
            self.__replayCtrl.onBattleChatMessage(messageText, isCurrentPlayer)
        elif self.isPlaying and not self.isTimeWarpInProgress:
            MessengerEntry.g_instance.gui.addClientMessage(messageText, isCurrentPlayer)

    def onMinimapCellClicked(self, cellIdx):
        return
        player = BigWorld.player()
        if not isPlayerAvatar():
            return
        if self.isRecording:
            self.__replayCtrl.onMinimapCellClicked(cellIdx)
        elif self.isPlaying:
            self.guiWindowManager.battleWindow.minimap.markCell(cellIdx, 3.0)

    def setFpsPingLag(self, fps, ping, isLaggingNow):
        if self.isPlaying:
            return
        self.__replayCtrl.fps = fps
        self.__replayCtrl.ping = ping
        self.__replayCtrl.isLaggingNow = isLaggingNow

    def onClientVersionDiffers(self):
        LOG_TRACE('BattleReplay::onClientVersionDiffers')
        self.__replayCtrl.isWaitingForVersionConfirm = False
        self.stop()
        self.guiWindowManager.showLogin()

    def __loginOnLoadCallback(self):
        DialogsInterface.showI18nConfirmDialog('replayNotification', self.__onClientVersionConfirmDlgClosed)

    def __onClientVersionConfirmDlgClosed(self, result):
        if result:
            self.__replayCtrl.isWaitingForVersionConfirm = False
        else:
            self.stop()

    def enableAutoRecordingBattles(self, enable):
        if self.__isAutoRecordingEnabled == enable:
            return
        else:
            self.__isAutoRecordingEnabled = enable
            if enable:
                return
                if enable == 1:
                    self.setResultingFileName(FIXED_REPLAY_FILENAME)
                elif enable == 2:
                    self.setResultingFileName(None)
            elif self.isRecording:
                self.stop()
            return

    def setResultingFileName(self, fileName):
        self.__replayCtrl.setResultingFileName(fileName or '')

    def cancelSaveCurrMessage(self):
        self.__replayCtrl.cancelSaveCurrMessage()

    def __showInfoMessage(self, msg, args = None):
        if not self.isTimeWarpInProgress:
            self.guiWindowManager.battleWindow.vMsgsPanel.showMessage(msg, args)

    def __startAutoRecord(self):
        self.__isAutoRecordingEnabled = Settings.g_instance.getReplaySettings()['saveBattleReplays']
        if not self.__isAutoRecordingEnabled:
            return
        if self.isPlaying:
            return
        self.record()

    def __showLoginPage(self):
        self.guiWindowManager.showLogin()
        connectionManager.onDisconnected -= self.__showLoginPage

    def __updateAim(self):
        return
        if self.getPlaybackSpeedIdx() == 0:
            player = BigWorld.player()
            if isPlayerAvatar():
                if player.inputHandler.aim is not None:
                    player.inputHandler.aim._update()
                BigWorld.callback(0, self.__updateAim)
        return

    def onBattleResultsReceived(self, results):

        def set_default(obj):
            if isinstance(obj, set):
                return list(obj)
            raise TypeError

        self.__replayCtrl.setArenaStatisticsStr(json.dumps(results, default=set_default))

    def onExtendedBattleResultsReceived(self, results):
        self.__replayCtrl.setExtendedArenaStatisticsStr(cPickle.dumps(results))

    def __timeWarp(self, time):
        if not self.isPlaying or not self.__enableTimeWarp:
            return
        else:
            if time < self.getReplayTime():
                self.__arenaLoaded = False
                self.__cancelPanelCallbacks()
                self.__dataForSyncCameraState['next'] = []
                self.__dataForSyncCameraState['applied'] = []
                if self.__freeCameraMode:
                    cam = GameEnvironment.getCamera()
                    GlobalEvents.onMouseEvent -= cam.processMouseEvent
                    cam.leaveState(CameraState.ReplayFree)
            finishTime = self.getReplayLength()
            if time < finishTime and self.getReplayTime() >= finishTime and self.__playbackSpeedIdx == 0:
                self.setPlaybackSpeedIdx(self.__savedPlaybackSpeedIdx if self.__savedPlaybackSpeedIdx != 0 else self.__playbackSpeedModifiers.index(1.0))
            if not self.__replayCtrl.beginTimeWarp(time):
                return
            if self.__timeWarpCleanupCb is None:
                self.__timeWarpCleanupCb = BigWorld.callbackRealTime(0.5, self.__cleanupAfterTimeWarp)
            return

    def __cleanupAfterTimeWarp(self):
        self.__timeWarpCleanupCb = None
        BigWorld.clearDeferredImpacts()
        cam = GameEnvironment.getCamera()
        cam.getStateObject().refreshState()
        self.updateHUDProgress()
        return

    def __disableSidePanelContextMenu(self):
        self.__disableSidePanelContextMenuCb = None
        if hasattr(self.guiWindowManager.battleWindow.movie, 'leftPanel'):
            self.guiWindowManager.battleWindow.movie.leftPanel.onMouseDown = None
            self.guiWindowManager.battleWindow.movie.rightPanel.onMouseDown = None
        else:
            self.__disableSidePanelContextMenuCb = BigWorld.callback(0.1, self.__disableSidePanelContextMenu)
        return

    def getSetting(self, key, default = None):
        if self.__settings.has_key(key):
            return pickle.loads(base64.b64decode(self.__settings.readString(key)))
        return default

    def setSetting(self, key, value):
        self.__settings.write(key, base64.b64encode(pickle.dumps(value)))

    def isPlayingReplay(self):
        return self.__replayCtrl.isPlaying or self.__replayCtrl.isTimeWarpInProgress

    def __timeMarkerCallback(self, markType):
        if not self.__arenaLoaded and markType == REPLAY_TIME_MARK_ARENA_LOADED and not self.isTimeWarpInProgress:
            self.__action(ACTION_PAUSE)

    def onArenaLoaded(self):
        self.__replayCtrl.onTimeMarker(REPLAY_TIME_MARK_ARENA_LOADED)
        self.__arenaLoaded = True
        self.__syncCameraState()
        if not self.isTimeWarpInProgress:
            self.__action(ACTION_PLAY)

    def __action(self, idx):
        if not (self.isPlaying and self.isClientReady):
            return
        currReplayTime = self.getReplayTime()
        fastForwardStep = FAST_FORWARD_STEP
        if idx == ACTION_HOME:
            normalSpeedIdx = self.__playbackSpeedModifiers.index(1.0)
            self.setPlaybackSpeedIdx(normalSpeedIdx)
            self.__timeWarp(0.0)
        elif idx == ACTION_END:
            self.__timeWarp(self.getReplayLength())
        elif idx == ACTION_BACK or idx == ACTION_BACK_2:
            if idx == ACTION_BACK_2:
                fastForwardStep *= 2
            normalSpeedIdx = self.__playbackSpeedModifiers.index(1.0)
            if self.__playbackSpeedIdx > normalSpeedIdx:
                self.setPlaybackSpeedIdx(normalSpeedIdx)
            self.__timeWarp(currReplayTime - fastForwardStep)
        elif idx == ACTION_FORWARD or idx == ACTION_FORWARD_2:
            if idx == ACTION_FORWARD_2:
                fastForwardStep *= 2
            self.__timeWarp(currReplayTime + fastForwardStep)
        elif idx == ACTION_SPEED_INC:
            if self.__playbackSpeedIdx < len(self.__playbackSpeedModifiers) - 1 and self.__playbackSpeedIdx != 0:
                self.setPlaybackSpeedIdx(self.__playbackSpeedIdx + 1)
        elif idx == ACTION_SPEED_DEC:
            if self.__playbackSpeedIdx > 1:
                self.setPlaybackSpeedIdx(self.__playbackSpeedIdx - 1)
        elif idx == ACTION_PAUSE:
            if self.__playbackSpeedIdx != 0:
                self.setPlaybackSpeedIdx(0)
        elif idx == ACTION_PLAY:
            if self.__playbackSpeedIdx == 0 and currReplayTime < self.__playbackLength:
                self.setPlaybackSpeedIdx(self.__savedPlaybackSpeedIdx if self.__savedPlaybackSpeedIdx != 0 else self.__playbackSpeedModifiers.index(1.0))
        elif idx == ACTION_CAMERA_SWITCH:
            self.__freeCameraMode = not self.__freeCameraMode
            self.__replayCtrl.isControllingCamera = not self.__freeCameraMode
            cam = GameEnvironment.getCamera()
            if self.__freeCameraMode:
                cam.setState(CameraState.ReplayFree)
                GlobalEvents.onMouseEvent += cam.processMouseEvent
                self.eShowMessageHUD(localizeHUD('REPLAY_FREE_CAMERA_ON'))
            else:
                GlobalEvents.onMouseEvent -= cam.processMouseEvent
                cam.leaveState(CameraState.ReplayFree)
                self.eShowMessageHUD(localizeHUD('REPLAY_FREE_CAMERA_OFF'))

    def action(self, idx):
        BigWorld.callback(0, lambda : self.__action(idx))

    def __initHUD(self):
        keysMapping = {'up': InputMapping.getKeyLocalization(InputMapping.getKeyNameByCode(Keys.KEY_UPARROW)),
         'down': InputMapping.getKeyLocalization(InputMapping.getKeyNameByCode(Keys.KEY_DOWNARROW)),
         'left': InputMapping.getKeyLocalization(InputMapping.getKeyNameByCode(Keys.KEY_LEFTARROW)),
         'right': InputMapping.getKeyLocalization(InputMapping.getKeyNameByCode(Keys.KEY_RIGHTARROW)),
         'home': InputMapping.getKeyLocalization(InputMapping.getKeyNameByCode(Keys.KEY_HOME)),
         'end': InputMapping.getKeyLocalization(InputMapping.getKeyNameByCode(Keys.KEY_END)),
         'shift': InputMapping.getKeyLocalization('KEY_SHIFT'),
         'ctrl': 'CTRL',
         'space': InputMapping.getKeyLocalization(InputMapping.getKeyNameByCode(Keys.KEY_SPACE))}
        tips = [localizeHUD('REPLAY_MESSAGE_BEGIN').format(button=keysMapping['home']),
         localizeHUD('REPLAY_MESSAGE_BACKWARD').format(button=keysMapping['left'], combo='%s + %s' % (keysMapping['shift'], keysMapping['left'])),
         localizeHUD('REPLAY_MESSAGE_REPLAY').format(button=keysMapping['space']),
         localizeHUD('REPLAY_MESSAGE_PAUSE').format(button=keysMapping['space']),
         localizeHUD('REPLAY_MESSAGE_FORWARD').format(button=keysMapping['right'], combo='%s + %s' % (keysMapping['shift'], keysMapping['right'])),
         localizeHUD('REPLAY_MESSAGE_END').format(button=keysMapping['end']),
         localizeHUD('REPLAY_MESSAGE_SLOWER').format(btn1=keysMapping['down'], btn2=keysMapping['shift']),
         localizeHUD('REPLAY_MESSAGE_FASTER').format(btn1=keysMapping['up'], btn2=keysMapping['shift'])]
        self.__playbackLength = self.getReplayLength()
        self.eInitHUD('%02d:%02d' % (self.__playbackLength / 60, self.__playbackLength % 60), tips)
        self.__updateHUDButtons()

    def initPanelCallbacks(self):
        if self.isPlaying:
            if self.__firstTimeHUDInit:
                self.__callbackShowPanel = BigWorld.callback(TIME_FOR_SHOW_PANEL, self.__showPanelCallback)
                self.__callbackHidePanel = BigWorld.callback(TIME_FOR_HIDE_PANEL, self.__hidePanelCallback)
                self.__firstTimeHUDInit = False

    def __showPanelCallback(self):
        self.__callbackShowPanel = None
        self.eShowPanel()
        return

    def __hidePanelCallback(self):
        self.__callbackHidePanel = None
        self.eHidePanel()
        return

    def __cancelPanelCallbacks(self):
        if self.__callbackShowPanel is not None:
            BigWorld.cancelCallback(self.__callbackShowPanel)
            self.__callbackShowPanel = None
        if self.__callbackHidePanel is not None:
            BigWorld.cancelCallback(self.__callbackHidePanel)
            self.__callbackHidePanel = None
            self.__firstTimeHUDInit = True
        return

    def updateHUDProgress(self):
        curTime = self.getReplayTime()
        self.eUpdateHUDProgress('%02d:%02d' % (curTime / 60, curTime % 60), 0 if self.__playbackLength == 0 else int(curTime * 100 / self.__playbackLength))

    def __updateHUDButtons(self):
        isPaused = self.__playbackSpeedIdx == 0
        isEnd = self.getReplayTime() >= self.__playbackLength
        playSpeedStr = 'x%s' % self.__playbackSpeedModifiersStr[self.__playbackSpeedIdx]
        enableDec = self.__playbackSpeedIdx != 1
        enableInc = self.__playbackSpeedIdx != len(self.__playbackSpeedModifiers) - 1
        btns = [True,
         True,
         not isEnd,
         True,
         not isEnd,
         not isEnd,
         enableDec and not isPaused,
         enableInc and not isPaused]
        self.eUpdateHUDButtons(isPaused, playSpeedStr, btns)
        if self.getReplayTime() < self.__playbackLength:
            self.eShowMessageHUD(localizeHUD('REPLAY_OPTION_PAUSE') if isPaused else '%s %s' % (localizeHUD('REPLAY_MESSAGE_SPEED'), playSpeedStr))

    def deleteOldReplays(self):
        rem = Settings.g_instance.getReplaySettings()['removeBattleReplays']
        if not rem:
            return
        days = Settings.g_instance.getReplaySettings()['daysForRemoveBattleReplays']
        deleteOldFiles(self.__replayDir, days, REPLAY_FILE_EXTENSION)

    def notifyAxisValues(self, axis, value):
        if self.isRecording:
            self.__replayCtrl.onApplyInputAxis(axis, value)

    def __applyInputAxis(self, axis, value):
        if self.isPlaying and self.isClientReady and not self.isTimeWarpInProgress:
            BigWorld.player().applyInputAxis(axis, value, replayMode=True)

    def notifyTargetEntity(self, entityId):
        if self.isRecording:
            self.__replayCtrl.onTargetEntity(entityId)

    def __applyTargetEntity(self, entityId):
        if self.isPlaying and self.isClientReady:
            hud = GameEnvironment.getHUD()
            hud.onTargetEntity(hud.entityList[entityId] if entityId != 0 else None, replayMode=True)
        return

    def notifyTargetLock(self, isLocked):
        if self.isRecording:
            self.__replayCtrl.onTargetLock(isLocked)

    def __applyTargetLock(self, isLocked):
        if self.isPlaying and self.isClientReady:
            GameEnvironment.getHUD().setTargetLock(isLocked)

    def notifyZoomChange(self, zoomIdx, zoomPreset):
        if self.isRecording:
            self.__replayCtrl.onZoomChange(zoomIdx, '' if zoomPreset is None else zoomPreset)
        return

    def __applyZoomChange(self, zoomIdx, zoomPreset):
        if self.isPlaying:
            cam = GameEnvironment.getCamera()
            cam._Camera__setZoom(zoomIdx, zoomPreset if zoomPreset != '' else None)
        return

    def notifyCameraState(self, camState, isEnter):
        if self.isRecording:
            self.__replayCtrl.onCameraStateChanged(camState, isEnter)
        elif self.isPlaying:
            if not self.__arenaLoaded:
                if len(self.__dataForSyncCameraState['next']) > 0 and self.__dataForSyncCameraState['next'][0] == (camState, isEnter):
                    self.__dataForSyncCameraState['next'].pop(0)
                else:
                    self.__dataForSyncCameraState['applied'].append((camState, isEnter))

    def __applyCameraState(self, camState, isEnter):
        if self.isPlaying:
            cam = GameEnvironment.getCamera()
            if self.__arenaLoaded and cam:
                self.__syncCameraState()
                if isEnter:
                    reapplyFreeCamera = camState == CameraState.Spectator and not self.isControllingCamera
                    if reapplyFreeCamera:
                        self.__action(ACTION_CAMERA_SWITCH)
                    if self.isControllingCamera:
                        cam.setState(camState)
                    else:
                        cam.setPrevState(camState)
                    if reapplyFreeCamera:
                        self.__action(ACTION_CAMERA_SWITCH)
                else:
                    cam.leaveState(camState)
            elif len(self.__dataForSyncCameraState['applied']) > 0 and self.__dataForSyncCameraState['applied'][0] == (camState, isEnter):
                self.__dataForSyncCameraState['applied'].pop(0)
            else:
                self.__dataForSyncCameraState['next'].append((camState, isEnter))

    def __syncCameraState(self):
        cam = GameEnvironment.getCamera()
        if self.__arenaLoaded and cam:
            for cs in self.__dataForSyncCameraState['next']:
                camState = cs[0]
                if cs[1]:
                    cam.setState(camState) if self.isControllingCamera else cam.setPrevState(camState)
                else:
                    cam.leaveState(camState)

            self.__dataForSyncCameraState['next'] = []
            self.__dataForSyncCameraState['applied'] = []

    def notifySniperModeType(self, sniperModeType):
        if self.isRecording:
            self.__replayCtrl.onSetSniperModeType(sniperModeType)

    def __applySniperModeType(self, sniperModeType):
        if self.isPlaying:
            if self.__setSniperModeTypeCbHandler is not None:
                BigWorld.cancelCallback(self.__setSniperModeTypeCbHandler)
            self.__setSniperModeTypeCbHandler = BigWorld.callbackRealTime(0, partial(self.__setSniperModeTypeCB, sniperModeType))
        return

    def __setSniperModeTypeCB(self, sniperModeType):
        self.__setSniperModeTypeCbHandler = None
        cam = GameEnvironment.getCamera()
        if cam and cam.context and cam.context.cameraSettings:
            cam.setSniperModeType(sniperModeType)
        else:
            self.__setSniperModeTypeCbHandler = BigWorld.callbackRealTime(0.1, partial(self.__setSniperModeTypeCB, sniperModeType))
        return

    def notifyNewCPMatrix(self, m):
        if self.isRecording:
            self.__replayCtrl.setCenterPointMatrixProvider(m if m else Math.Matrix())

    def getCenterPointMatrixProvider(self):
        return self.__replayCtrl.getCenterPointMatrixProvider()

    def setAimDirection(self, direction):
        if self.isRecording:
            self.__replayCtrl.setAimDirection(direction)

    def getAimDirection(self):
        return self.__replayCtrl.getAimDirection()

    def __onSaveControls(self):
        if self.isRecording:
            profileType = InputMapping.g_instance.currentProfileType
            camType = 0
            if profileType == consts.INPUT_SYSTEM_STATE.MOUSE:
                camType = InputMapping.g_instance.mouseSettings.CAMERA_TYPE
            self.__replayCtrl.onCurrentControlsChanged(profileType, camType)

    def __applyCurrentControls(self, profileType, camType):
        if self.isPlaying:
            InputMapping.g_instance.setCurProfileName(consts.INPUT_SYSTEM_PROFILES_LIST_REVERT[profileType])
            GameEnvironment.g_instance.eAimsSettingsUpdate()

    def rewindToTime(self, percentage):
        newTime = percentage * self.__playbackLength / 100.0
        BigWorld.callback(0, lambda : self.__timeWarp(newTime))

    def onFlapsMessage(self, value):
        if self.isRecording:
            self.__replayCtrl.onFlapsMessage(value)
        elif self.isPlaying:
            GameEnvironment.getHUD().flapsMessage(value)

    def onFlyKeyBoardInputAllowed(self, flag, playerAvatar):
        if not self.isControllingCamera:
            cam = GameEnvironment.getCamera()
            if cam.getState() == CameraState.ReplayFree:
                cam.getStateStrategy().aroundLocalAxes = bool(Settings.g_instance.cinemaCamera)

    def setPlaneAimMatrix(self, m):
        if self.isRecording or self.isPlaying:
            self.__replayCtrl.setPlaneAimMatrix(m)


def isPlaying():
    if g_replay is None:
        return False
    else:
        return g_replay.isPlayingReplay()


def callback(delay, function):
    t = delay
    if isPlaying():
        if g_replay.isTimeWarpInProgress:
            function()
            return None
    return BigWorld.callback(t, function)