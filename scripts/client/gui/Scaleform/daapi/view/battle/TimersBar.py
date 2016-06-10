# Embedded file name: scripts/client/gui/Scaleform/daapi/view/battle/TimersBar.py
from SoundGroups import g_instance as _g_sound
from debug_utils import LOG_DEBUG
from gui.Scaleform.locale.INGAME_GUI import INGAME_GUI
from gui.battle_control import arena_info, g_sessionProvider
from gui.battle_control.arena_info.interfaces import IArenaVehiclesController
from gui.battle_control.battle_constants import COUNTDOWN_STATE
from gui.battle_control.battle_period_ctrl import ITimersBar
from helpers.i18n import makeString as _ms

class _SOUNDS:
    BATTLE_ENDING_SOON = 'time_buzzer_02'
    COUNTDOWN_TICKING = 'time_countdown'
    BATTLE_END = 'time_over'
    STOP_TICKING = 'time_countdown_stop'


_BATTLE_END_SOUND_TIME = 2
_STATE_TO_MESSAGE = {COUNTDOWN_STATE.WAIT: _ms('#ingame_gui:timer/waiting'),
 COUNTDOWN_STATE.START: _ms('#ingame_gui:timer/starting'),
 COUNTDOWN_STATE.STOP: _ms('#ingame_gui:timer/started')}
_EVENT_STATE_TO_MESSAGE = {COUNTDOWN_STATE.WAIT: _ms(INGAME_GUI.TIMER_WAITING),
 COUNTDOWN_STATE.START: _ms(INGAME_GUI.TIMER_FOOTBALL_STARTING),
 COUNTDOWN_STATE.STOP: _ms(INGAME_GUI.TIMER_FOOTBALL_STARTED)}

class BaseTimersBar(ITimersBar):

    def __init__(self, ui = None, isEvent = False):
        super(BaseTimersBar, self).__init__()
        self._ui = ui
        self.__isTicking = False
        arenaType = arena_info.getArenaType()
        self._state = COUNTDOWN_STATE.STOP
        self.__roundLength = arenaType.roundLength
        self.__endingSoonTime = arenaType.battleEndingSoonTime
        self.__endWarningIsEnabled = self.__checkEndWarningStatus()
        self.__isTicking = False
        if isEvent or self.__endWarningIsEnabled:
            timerPath = 'eventBattleTimer.swf'
            _g_sound.playSound2D(_SOUNDS.STOP_TICKING)
        else:
            timerPath = 'BattleTimer.swf'
        self._ui.movie.loadTimer(timerPath)

    def __del__(self):
        LOG_DEBUG('TimersBar is deleted')

    def setTotalTime(self, level, totalTime):
        minutes, seconds = divmod(int(totalTime), 60)
        if self.__endWarningIsEnabled and self._state == COUNTDOWN_STATE.STOP:
            if _BATTLE_END_SOUND_TIME < totalTime <= self.__endingSoonTime:
                if not self.__isTicking:
                    _g_sound.playSound2D(_SOUNDS.COUNTDOWN_TICKING)
                    self.__isTicking = True
                if totalTime == self.__endingSoonTime:
                    _g_sound.playSound2D(_SOUNDS.BATTLE_ENDING_SOON)
            elif self.__isTicking:
                _g_sound.playSound2D(_SOUNDS.STOP_TICKING)
            if totalTime == _BATTLE_END_SOUND_TIME and self.__isTicking:
                _g_sound.playSound2D(_SOUNDS.BATTLE_END)
                self.__isTicking = False
        self._call('timerBar.setTotalTime', [level, '{:02d}'.format(minutes), '{:02d}'.format(seconds)])

    def hideTotalTime(self):
        self._call('showBattleTimer', [False])

    def destroy(self):
        self._ui = None
        return

    def populate(self):
        pass

    def setWinConditionText(self, text):
        pass

    def _call(self, funcName, args = None):
        if self._ui:
            self._ui.call('battle.{0}'.format(funcName), args)

    def __validateEndingSoonTime(self):
        return self.__endingSoonTime > 0 and self.__endingSoonTime < self.__roundLength

    def __checkEndWarningStatus(self):
        endingSoonTimeIsValid = self.__validateEndingSoonTime()
        return arena_info.battleEndWarningEnabled() and endingSoonTimeIsValid


class TimersBar(BaseTimersBar):

    def setCountdown(self, state, _, timeLeft):
        self._state = state
        self._call('timerBig.setTimer', [_STATE_TO_MESSAGE[state], timeLeft])

    def hideCountdown(self, state, speed):
        self._state = state
        self._call('timerBig.setTimer', [_STATE_TO_MESSAGE[state]])
        self._call('timerBig.hide', [speed])


class FootballOverTimeTimersBar(TimersBar, IArenaVehiclesController):

    def __init__(self, ui = None):
        super(FootballOverTimeTimersBar, self).__init__(ui, True)
        self.__timeLeft = 0
        self.__isShowing = False
        self.__overtimeTimer = None
        self.__overtimeSwfLoading = False
        self.__soundAlreadyPlayed = False
        g_sessionProvider.addArenaCtrl(self)
        return

    def populate(self):
        self.__overtimeSwfLoading = False
        self.__overtimeTimer = self._ui.movie._root.timersBar
        if self.__isShowing:
            self.__startCountDown(self.__timeLeft)

    def destroy(self):
        g_sessionProvider.removeArenaCtrl(self)
        super(FootballOverTimeTimersBar, self).destroy()
        self.__overtimeTimer = None
        self.__isShowing = False
        return

    def setCountdown(self, state, _, timeLeft):
        self.__timeLeft = timeLeft
        self._state = state
        self.__isShowing = True
        if self.__overtimeTimer:
            self.__startCountDown(timeLeft)
        elif self.__hasPenaltyPoints():
            self.__loadOvertimeTimer()
        else:
            self._call('timerBig.setTimer', [_EVENT_STATE_TO_MESSAGE[state], timeLeft])

    def hideCountdown(self, state, speed):
        self._state = state
        self.__isShowing = False
        if self.__overtimeTimer is not None:
            self.__overtimeTimer.as_hide()
        else:
            self._call('timerBig.setTimer', [_EVENT_STATE_TO_MESSAGE[state]])
            self._call('timerBig.hide', [speed])
        return

    def invalidateFootballPenaltyPoints(self, data):
        if self.__hasPenaltyPoints() and self.__isShowing and not self.__overtimeTimer and not self.__overtimeSwfLoading:
            super(FootballOverTimeTimersBar, self).hideCountdown(self._state, 0.1)
            self.__loadOvertimeTimer()

    def __loadOvertimeTimer(self):
        self.__overtimeSwfLoading = True
        self._ui.movie.loadTimersBar('footballOverTimeTimer.swf')

    def __hasPenaltyPoints(self):
        ballPossession = g_sessionProvider.getArenaDP().getBallPossession()
        return ballPossession and ballPossession != (0, 0) or g_sessionProvider.getArenaDP().getPenaltyPoints() is not None

    def __startCountDown(self, timeLeft):
        if not self.__soundAlreadyPlayed:
            self.__soundAlreadyPlayed = True
            _g_sound.playSound2D('ev_football_overtime_countdown')
        self.__overtimeTimer.as_setTimer(timeLeft)


def timersBarFactory(ui = None, isEvent = False):
    if isEvent:
        return FootballOverTimeTimersBar(ui)
    else:
        return TimersBar(ui, isEvent)