# Embedded file name: scripts/client/gui/battle_control/battle_period_ctrl.py
import weakref
import BattleReplay
import BigWorld
from ConnectionManager import connectionManager
from constants import ARENA_PERIOD as _PERIOD, ARENA_GUI_TYPE
from gui.battle_control import event_dispatcher, arena_info
from gui.battle_control.arena_info import isFalloutBattle, isEventBattle
from gui.battle_control.arena_info.interfaces import IArenaPeriodController
from gui.battle_control.battle_constants import COUNTDOWN_STATE
from gui.battle_control.view_components import IViewComponentsController
import SoundGroups
_CRITICAL_TIME_LEVEL = 60.0
_COUNTDOWN_HIDE_SPEED = 1.5
_START_NOTIFICATION_TIME = 5.0

def getTimeLevel(value):
    if value is None:
        return 1
    criticalTime = _CRITICAL_TIME_LEVEL
    if isFalloutBattle():
        criticalTime = 120.0
    if value <= criticalTime:
        return 1
    else:
        return 0


class ITimersBar(object):

    def setTotalTime(self, level, totalTime):
        raise NotImplementedError

    def hideTotalTime(self):
        raise NotImplementedError

    def setCountdown(self, state, level, timeLeft):
        raise NotImplementedError

    def hideCountdown(self, state, speed):
        raise NotImplementedError

    def populate(self):
        raise NotImplementedError

    def setWinConditionText(self, text):
        raise NotImplementedError


class IPlayersPanelsSwitcher(object):

    def setInitialMode(self):
        raise NotImplementedError

    def setLargeMode(self):
        raise NotImplementedError


class ArenaPeriodController(IArenaPeriodController, IViewComponentsController):
    __slots__ = ('_callbackID', '_period', '_endTime', '_length', '_sound', '_battleTimerUI', '_preBattleTimerUI', '_cdState', '_ttState', '_isNotified', '_totalTime', '_countdown', '_playingTime', '_switcherUI', '_switcherState', '_battleCtx', '_battleEndWarning')

    def __init__(self):
        super(ArenaPeriodController, self).__init__()
        self._callbackID = None
        self._period = _PERIOD.IDLE
        self._totalTime = -1
        self._endTime = 0
        self._countdown = -1
        self._length = 0
        self._sound = None
        self._battleTimerUI = None
        self._preBattleTimerUI = None
        self._switcherUI = None
        self._cdState = COUNTDOWN_STATE.UNDEFINED
        self._ttState = 0
        self._switcherState = 0
        self._isNotified = False
        self._playingTime = 0
        self._battleCtx = None
        self._battleEndWarning = None
        return

    def clear(self):
        self.__clearCallback()
        self._stopSound()
        self._setPlayingTimeOnArena()

    def setViewComponents(self, battleTimerUI, preBattleTimerUI, switcherUI = None, battleEndWarning = None):
        self._battleEndWarning = battleEndWarning
        self._battleTimerUI = battleTimerUI
        self._preBattleTimerUI = preBattleTimerUI
        self._switcherUI = switcherUI
        if self._period == _PERIOD.BATTLE:
            if switcherUI is not None:
                self._switcherUI.setInitialMode()
                self._switcherState = 1
        elif switcherUI is not None:
            self._switcherUI.setLargeMode()
            self._switcherState = 0
        if self._cdState in COUNTDOWN_STATE.VISIBLE:
            self._preBattleTimerUI.setCountdown(self._cdState, getTimeLevel(self._countdown), self._countdown)
            if self._battleCtx is not None:
                self._preBattleTimerUI.setWinConditionText(self._battleCtx.getArenaWinString())
        self._battleTimerUI.setTotalTime(getTimeLevel(self._totalTime), self._totalTime)
        return

    def clearViewComponents(self):
        self._battleTimerUI = None
        self._preBattleTimerUI = None
        self._switcherUI = None
        return

    def getEndTime(self):
        return self._endTime

    def getPeriod(self):
        return self._period

    def setPeriodInfo(self, period, endTime, length, additionalInfo, soundID = None):
        self._period = period
        self._endTime = endTime
        self._length = length
        if soundID:
            self._sound = SoundGroups.g_instance.getSound2D(soundID)
        self.__setCallback()

    def invalidatePeriodInfo(self, period, endTime, length, additionalInfo):
        self._period = period
        self._endTime = endTime
        self._length = length
        self.__clearCallback()
        self.__setCallback()
        self._setArenaWinStatus(additionalInfo)

    def setBattleCtx(self, battleCtx):
        self._battleCtx = battleCtx

    def _getTickInterval(self, floatLength):
        if floatLength > 1:
            return 1
        return 0

    def _getHideSpeed(self):
        return _COUNTDOWN_HIDE_SPEED

    def _calculate(self):
        return self._endTime - BigWorld.serverTime()

    def _setPlayingTimeOnArena(self):
        if self._playingTime:
            event_dispatcher.setPlayingTimeOnArena(self._playingTime)

    def _setTotalTime(self, totalTime):
        if self._totalTime == totalTime:
            return
        else:
            self._totalTime = totalTime
            if self._battleTimerUI is not None:
                self._battleTimerUI.setTotalTime(getTimeLevel(totalTime), totalTime)
            if self._battleEndWarning is not None and self._battleEndWarning.isLoaded():
                if not (isEventBattle() and self._battleCtx.getArenaDP().getPenaltyPoints() is not None):
                    self._battleEndWarning.setCurrentTimeLeft(totalTime)
            return

    def _hideTotalTime(self):
        if self._battleTimerUI is not None:
            self._battleTimerUI.hideTotalTime()
        return

    def _setCountdown(self, state, timeLeft = None):
        if timeLeft is not None and self._countdown == timeLeft:
            return
        else:
            self._countdown = timeLeft
            if self._preBattleTimerUI is not None:
                self._preBattleTimerUI.setCountdown(state, getTimeLevel(timeLeft), timeLeft)
            return

    def _hideCountdown(self, state, speed):
        self._countdown = None
        if self._preBattleTimerUI is not None:
            self._preBattleTimerUI.hideCountdown(state, speed)
        return

    def _playSound(self):
        if self._sound and not self._sound.isPlaying:
            self._sound.play()

    def _stopSound(self):
        if self._sound and self._sound.isPlaying:
            self._sound.stop()

    def _updateSound(self, timeLeft):
        if timeLeft:
            self._playSound()
        else:
            self._stopSound()

    def _doNotify(self):
        if not self._isNotified:
            BigWorld.WGWindowsNotifier.onBattleBeginning()
            self._isNotified = True

    def _updateCountdown(self, timeLeft):
        if self._period == _PERIOD.WAITING:
            if self._cdState != COUNTDOWN_STATE.WAIT:
                self._cdState = COUNTDOWN_STATE.WAIT
                self._setCountdown(COUNTDOWN_STATE.WAIT)
        elif self._period == _PERIOD.PREBATTLE:
            if timeLeft <= _START_NOTIFICATION_TIME:
                self._doNotify()
            self._cdState = COUNTDOWN_STATE.START
            self._setCountdown(COUNTDOWN_STATE.START, timeLeft)
            self._updateSound(timeLeft)
        elif self._period == _PERIOD.BATTLE and self._cdState in COUNTDOWN_STATE.VISIBLE:
            self._cdState = COUNTDOWN_STATE.STOP
            self._stopSound()
            self._hideCountdown(COUNTDOWN_STATE.STOP, self._getHideSpeed())

    def _setArenaWinStatus(self, additionalInfo):
        if additionalInfo is not None:
            self._battleCtx.setLastArenaWinStatus(additionalInfo.getWinStatus())
        return

    def __tick(self):
        floatLength = self._calculate()
        if floatLength is None:
            return 0
        else:
            intLength = max(int(floatLength), 0)
            if self._period != _PERIOD.AFTERBATTLE:
                self._ttState = 1
                self._setTotalTime(intLength)
                if self._period == _PERIOD.BATTLE:
                    self._playingTime = self._length - floatLength
                    if self._period == _PERIOD.BATTLE:
                        if self._switcherState != 1:
                            if self._switcherUI is not None:
                                self._switcherUI.setInitialMode()
                            self._switcherState = 1
                    elif self._switcherState != 0:
                        if self._switcherUI is not None:
                            self._switcherUI.setLargeMode()
                        self._switcherState = 0
            elif self._ttState:
                self._ttState = 0
                self._hideTotalTime()
            self._updateCountdown(intLength)
            return floatLength

    def __setCallback(self):
        self._callbackID = None
        length = self.__tick()
        self._callbackID = BigWorld.callback(self._getTickInterval(length), self.__setCallback)
        return

    def __clearCallback(self):
        if self._callbackID is not None:
            BigWorld.cancelCallback(self._callbackID)
            self._callbackID = None
        return


class ArenaPeriodRecorder(ArenaPeriodController):
    __slots__ = ('__recorder',)

    def __init__(self):
        super(ArenaPeriodRecorder, self).__init__()
        self.__recorder = None
        return

    def clear(self):
        connectionManager.onDisconnected -= self.__onDisconnected
        BattleReplay.g_replayCtrl.onStopped -= self.__onReplayStopped
        self.__recorder = None
        super(ArenaPeriodRecorder, self).clear()
        return

    def setPeriodInfo(self, period, endTime, length, additionalInfo, soundID = None):
        if arena_info.getArenaGuiType() != ARENA_GUI_TYPE.TUTORIAL:
            ctrl = BattleReplay.g_replayCtrl
            connectionManager.onDisconnected += self.__onDisconnected
            ctrl.onStopped += self.__onReplayStopped
            self.__recorder = ctrl.setArenaPeriod
        else:
            self.__recorder = None
        super(ArenaPeriodRecorder, self).setPeriodInfo(period, endTime, length, additionalInfo, soundID)
        return

    def _calculate(self):
        floatLength = super(ArenaPeriodRecorder, self)._calculate()
        if self.__recorder is not None and self._period != _PERIOD.AFTERBATTLE:
            self.__recorder(self._period, floatLength)
        return floatLength

    def __onReplayStopped(self):
        self.__recorder = None
        return

    def __onDisconnected(self):
        self.__recorder = None
        return


class ArenaPeriodPlayer(ArenaPeriodController):
    __slots__ = ('__replay',)

    def __init__(self):
        super(ArenaPeriodPlayer, self).__init__()
        self.__replay = None
        return

    def clear(self):
        self.__replay = None
        super(ArenaPeriodPlayer, self).clear()
        return

    def setPeriodInfo(self, period, endTime, length, additionalInfo, soundID = None):
        self.__replay = weakref.proxy(BattleReplay.g_replayCtrl)
        super(ArenaPeriodPlayer, self).setPeriodInfo(period, endTime, length, additionalInfo, soundID)

    def _getTickInterval(self, floatLength):
        if self._period == _PERIOD.IDLE:
            return 1
        return 0

    def _getHideSpeed(self):
        if self._playingTime > _COUNTDOWN_HIDE_SPEED:
            return 0
        else:
            return super(ArenaPeriodPlayer, self)._getHideSpeed()

    def _calculate(self):
        self._period = self.__replay.getArenaPeriod()
        if self._period == _PERIOD.IDLE:
            return None
        else:
            return self.__replay.getArenaLength()

    def _setPlayingTimeOnArena(self):
        pass

    def _setTotalTime(self, totalTime):
        if not self.__replay.isFinished():
            super(ArenaPeriodPlayer, self)._setTotalTime(totalTime)

    def _updateCountdown(self, timeLeft):
        if not self.__replay.isTimeWarpInProgress:
            super(ArenaPeriodPlayer, self)._updateCountdown(timeLeft)

    def _updateSound(self, timeLeft):
        if timeLeft and not self.__replay.playbackSpeed == 0:
            self._playSound()
        else:
            self._stopSound()

    def _doNotify(self):
        pass


def createPeriodCtrl(isReplayPlaying, isReplayRecording):
    if isReplayRecording:
        clazz = ArenaPeriodRecorder
    elif isReplayPlaying:
        clazz = ArenaPeriodPlayer
    else:
        clazz = ArenaPeriodController
    return clazz()