# Embedded file name: scripts/client/gui/prb_control/functional/fallout.py
from CurrentVehicle import g_currentVehicle
from constants import FALLOUT_BATTLE_TYPE, QUEUE_TYPE
from gui.prb_control.context import pre_queue_ctx
from gui.prb_control.events_dispatcher import g_eventDispatcher
from gui.prb_control.functional import unit
from gui.prb_control.functional import event_battles
from gui.prb_control.functional import prequeue
from gui.prb_control.functional.decorators import falloutQueueAmmoCheck
from gui.prb_control.items import SelectResult
from gui.prb_control.settings import FUNCTIONAL_FLAG, PREBATTLE_ACTION_NAME
from gui.prb_control.settings import PREBATTLE_RESTRICTION

class FalloutEntry(prequeue.PreQueueEntry):

    def __init__(self):
        super(FalloutEntry, self).__init__(QUEUE_TYPE.EVENT_BATTLES, FUNCTIONAL_FLAG.UNDEFINED)

    def _goToFunctional(self):
        super(FalloutEntry, self)._goToFunctional()
        g_eventDispatcher.showFalloutWindow()


class FalloutQueueFunctional(event_battles.EventBattlesQueueFunctional):

    def init(self, ctx = None):
        self.storage.release()
        g_eventDispatcher.loadFallout()
        return super(FalloutQueueFunctional, self).init(ctx)

    def fini(self, woEvents = False):
        if not woEvents and self._flags & FUNCTIONAL_FLAG.SWITCH == 0:
            self.storage.suspend()
            g_eventDispatcher.unloadFallout()
        return super(FalloutQueueFunctional, self).fini(woEvents)

    @falloutQueueAmmoCheck()
    def queue(self, ctx, callback = None):
        super(FalloutQueueFunctional, self).queue(ctx, callback=callback)

    def leave(self, ctx, callback = None):
        self.storage.suspend()
        super(FalloutQueueFunctional, self).leave(ctx, callback=callback)

    def doSelectAction(self, action):
        isProcessed = False
        newEntry = None
        name = action.actionName
        if name == PREBATTLE_ACTION_NAME.SQUAD:
            newEntry = unit.EventSquadEntry(self.storage.getBattleType())
            isProcessed = True
        elif name == PREBATTLE_ACTION_NAME.EVENT_BATTLES_QUEUE:
            isProcessed = True
        return SelectResult(isProcessed, newEntry)

    def canPlayerDoAction(self):
        canDo = not self.isInQueue()
        restriction = ''
        if canDo and self.storage.isEnabled():
            if self.storage.getBattleType() == FALLOUT_BATTLE_TYPE.UNDEFINED:
                canDo = False
                restriction = PREBATTLE_RESTRICTION.FALLOUT_NOT_SELECTED
            elif not g_currentVehicle.isGroupReady():
                canDo = False
                restriction = PREBATTLE_RESTRICTION.VEHICLE_GROUP_IS_NOT_READY
        return (canDo, restriction)

    def _makeQueueCtxByAction(self, action = None):
        storage = self.storage
        return pre_queue_ctx.EventBattlesQueueCtx(storage.getVehiclesInvIDs(excludeEmpty=True), storage.getBattleType(), storage.isAutomatch(), waitingID='prebattle/join')