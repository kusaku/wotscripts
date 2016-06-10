# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/header/SquadTypeSelectPopover.py
from debug_utils import LOG_ERROR
from gui.Scaleform.daapi.view.lobby.header import battle_selector_items
from gui.Scaleform.daapi.view.meta.BattleTypeSelectPopoverMeta import BattleTypeSelectPopoverMeta
from gui.prb_control.context import PrebattleAction
from gui.prb_control.prb_helpers import GlobalListener
from gui.prb_control.settings import PREBATTLE_ACTION_NAME
from gui.Scaleform.locale.TOOLTIPS import TOOLTIPS

class SquadTypeSelectPopover(BattleTypeSelectPopoverMeta, GlobalListener):

    def __init__(self, _ = None):
        super(SquadTypeSelectPopover, self).__init__()

    def selectFight(self, actionName):
        if self.prbDispatcher:
            self.prbDispatcher.doSelectAction(PrebattleAction(actionName))
        else:
            LOG_ERROR('Prebattle dispatcher is not defined')

    def getTooltipData(self, itemData):
        if itemData == PREBATTLE_ACTION_NAME.SQUAD:
            return TOOLTIPS.HEADER_SQUAD
        if itemData == PREBATTLE_ACTION_NAME.EVENT_SQUAD:
            return TOOLTIPS.HEADER_EVENTSQUAD_MEMBER
        return ''

    def demoClick(self):
        pass

    def update(self):
        if not self.isDisposed():
            self.as_updateS(*battle_selector_items.getSquadItems().getVOs())

    def _populate(self):
        super(SquadTypeSelectPopover, self)._populate()
        self.update()

    def _dispose(self):
        super(SquadTypeSelectPopover, self)._dispose()