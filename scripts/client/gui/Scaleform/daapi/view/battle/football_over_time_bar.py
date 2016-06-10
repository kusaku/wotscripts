# Embedded file name: scripts/client/gui/Scaleform/daapi/view/battle/football_over_time_bar.py
from constants import ARENA_PERIOD
from debug_utils import LOG_DEBUG
from gui.battle_control import g_sessionProvider
from gui.battle_control.arena_info.interfaces import IArenaPeriodController, IArenaVehiclesController
from SoundGroups import g_instance as _g_sound

class FootballOvertimeController(IArenaPeriodController, IArenaVehiclesController):

    def __init__(self, arena):
        super(FootballOvertimeController, self).__init__()
        self.__period = arena.period
        self._points = None
        self.__isOvertime = False
        return

    def getCtrlScope(self):
        return IArenaPeriodController.getCtrlScope(self) | IArenaVehiclesController.getCtrlScope(self)

    def start(self):
        self._update()
        g_sessionProvider.addArenaCtrl(self)

    def stop(self):
        g_sessionProvider.removeArenaCtrl(self)

    def isOvertime(self):
        return self.__isOvertime

    def invalidateFootballPenaltyPoints(self, data):
        self._points = g_sessionProvider.getArenaDP().getPenaltyPoints()
        self._update()

    def invalidatePeriodInfo(self, period, endTime, length, additionalInfo):
        self.__period = period
        self._update()

    def _update(self):
        self.__isOvertime = self.__period == ARENA_PERIOD.BATTLE and self._points is not None
        return


class FootballOverTimeBar(FootballOvertimeController):

    def __init__(self, arena, ui = None):
        super(FootballOverTimeBar, self).__init__(arena)
        self._ui = ui
        self.__flash = None
        self.__isFlashLoading = False
        self.__soundAlreadyPlayed = False
        self.start()
        return

    def __del__(self):
        LOG_DEBUG('FootballOverTimeBar is deleted')

    def populate(self):
        self.__isFlashLoading = False
        self.__flash = self._ui.movie._root.footballRageBar
        self._update()

    def destroy(self):
        self.stop()
        self.hide()
        self._ui = None
        return

    def hide(self):
        if self.__flash is not None:
            self.__flash.as_hide()
        return

    def _update(self):
        super(FootballOverTimeBar, self)._update()
        if self.isOvertime() and self._points == (0, 0) and not self.__soundAlreadyPlayed:
            LOG_DEBUG('Play sound: ev_football_overtime_start')
            self.__soundAlreadyPlayed = True
            _g_sound.playSound2D('ev_football_overtime_start')
        if self.__flash:
            self.__flash.as_setScore(*self._points)
        elif self.isOvertime() and not self.__isFlashLoading:
            self.__isFlashLoading = True
            self._ui.movie.loadFootballOverTimeBar('footballOverTimeBar.swf')