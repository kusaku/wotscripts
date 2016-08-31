# Embedded file name: scripts/client/gui/Scaleform/daapi/view/battle/event_mark1/battle_timers.py
from gui.shared.lock import Lock
from gui.battle_control.battle_constants import BATTLE_SYNC_LOCKS
from gui.Scaleform.daapi.view.battle.event_mark1.common import playMark1AtBaseWarningSound
from gui.Scaleform.daapi.view.battle.shared import battle_timers

class Mark1BattleTimer(battle_timers.BattleTimer):

    def __init__(self):
        super(Mark1BattleTimer, self).__init__()
        self.__soundLock = Lock(BATTLE_SYNC_LOCKS.BATTLE_MARK1_AT_BASE_SOUND_LOCK)

    def _dispose(self):
        self.__soundLock.dispose()
        super(Mark1BattleTimer, self)._dispose()

    def _callWWISE(self, wwiseEventName):
        if wwiseEventName == battle_timers._WWISE_EVENTS.BATTLE_ENDING_SOON:
            playMark1AtBaseWarningSound(self.__soundLock)
        super(Mark1BattleTimer, self)._callWWISE(wwiseEventName)