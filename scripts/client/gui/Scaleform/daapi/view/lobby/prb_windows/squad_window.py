# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/prb_windows/squad_window.py
from constants import PREBATTLE_TYPE
from gui.Scaleform.locale.MENU import MENU
from gui.prb_control.settings import FUNCTIONAL_FLAG
from gui.Scaleform.daapi.view.meta.SquadWindowMeta import SquadWindowMeta
from gui.Scaleform.managers.windows_stored_data import DATA_TYPE, TARGET_ID
from gui.Scaleform.managers.windows_stored_data import stored_window
from gui.Scaleform.genConsts.PREBATTLE_ALIASES import PREBATTLE_ALIASES
from gui.prb_control.context import unit_ctx
from gui.prb_control.formatters import messages
from gui.shared import events, EVENT_BUS_SCOPE
from gui.prb_control import settings
from helpers import i18n

@stored_window(DATA_TYPE.UNIQUE_WINDOW, TARGET_ID.CHANNEL_CAROUSEL)

class SquadWindow(SquadWindowMeta):

    def getPrbType(self):
        return PREBATTLE_TYPE.SQUAD

    def onWindowClose(self):
        self.prbDispatcher.doLeaveAction(unit_ctx.LeaveUnitCtx(waitingID='prebattle/leave', flags=FUNCTIONAL_FLAG.UNDEFINED))

    def onWindowMinimize(self):
        self.destroy()

    @property
    def squadViewComponent(self):
        return self.components.get(self._getSquadViewAlias())

    def _getSquadViewAlias(self):
        return PREBATTLE_ALIASES.SQUAD_VIEW_PY

    def onUnitFlagsChanged(self, flags, timeLeft):
        self.as_enableWndCloseBtnS(not self.unitFunctional.getFlags().isInQueue())

    def onUnitPlayerOnlineStatusChanged(self, pInfo):
        if pInfo.isOffline():
            key = settings.UNIT_NOTIFICATION_KEY.PLAYER_OFFLINE
        else:
            key = settings.UNIT_NOTIFICATION_KEY.PLAYER_ONLINE
        self.__addPlayerNotification(key, pInfo)

    def onUnitPlayerAdded(self, pInfo):
        if not pInfo.isInvite():
            self.__addPlayerNotification(settings.UNIT_NOTIFICATION_KEY.PLAYER_ADDED, pInfo)

    def onUnitPlayerRemoved(self, pInfo):
        if not pInfo.isInvite():
            self.__addPlayerNotification(settings.UNIT_NOTIFICATION_KEY.PLAYER_REMOVED, pInfo)

    def onUnitPlayerBecomeCreator(self, pInfo):
        if pInfo.isCurrentPlayer():
            self._showLeadershipNotification()
        chat = self.chat
        if chat:
            chat.as_addMessageS(messages.getUnitPlayerNotification(settings.UNIT_NOTIFICATION_KEY.GIVE_LEADERSHIP, pInfo))

    def _populate(self):
        self.as_setComponentIdS(self._getSquadViewAlias())
        self._setWindowTitle()
        super(SquadWindow, self)._populate()
        self.addListener(events.HideWindowEvent.HIDE_UNIT_WINDOW, self.__handleSquadWindowHide, scope=EVENT_BUS_SCOPE.LOBBY)

    def _dispose(self):
        self.removeListener(events.HideWindowEvent.HIDE_UNIT_WINDOW, self.__handleSquadWindowHide, scope=EVENT_BUS_SCOPE.LOBBY)
        super(SquadWindow, self)._dispose()

    def _showLeadershipNotification(self):
        pass

    def _setWindowTitle(self):
        title = ''.join((i18n.makeString(MENU.HEADERBUTTONS_BATTLE_TYPES_SQUAD), i18n.makeString(MENU.HEADERBUTTONS_BATTLE_TYPES_SQUAD_RANDOMBATTLE)))
        self.as_setWindowTitleS(title)

    def __handleSquadWindowHide(self, _):
        self.destroy()

    def __addPlayerNotification(self, key, pInfo):
        chat = self.chat
        if chat and not pInfo.isCurrentPlayer():
            chat.as_addMessageS(messages.getUnitPlayerNotification(key, pInfo))


class FalloutSquadWindow(SquadWindow):

    def getPrbType(self):
        return PREBATTLE_TYPE.FALLOUT

    def _getSquadViewAlias(self):
        return PREBATTLE_ALIASES.FALLOUT_SQUAD_VIEW_PY


class EventSquadWindow(SquadWindow):

    def getPrbType(self):
        return PREBATTLE_TYPE.EVENT

    def _getSquadViewAlias(self):
        return PREBATTLE_ALIASES.EVENT_SQUAD_VIEW_PY

    def _setWindowTitle(self):
        title = i18n.makeString(MENU.HEADERBUTTONS_BATTLE_TYPES_EVENTSQUAD)
        self.as_setWindowTitleS(title)