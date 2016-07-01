# Embedded file name: scripts/client/gui/Scaleform/daapi/view/battle/shared/ingame_menu.py
import constants
from ConnectionManager import connectionManager
from adisp import process
from gui import DialogsInterface, GUI_SETTINGS
from gui import game_control, makeHtmlString
from gui.Scaleform.daapi.view.dialogs import DIALOG_BUTTON_ID
from gui.Scaleform.daapi.view.dialogs import I18nConfirmDialogMeta
from gui.Scaleform.daapi.view.dialogs.deserter_meta import IngameDeserterDialogMeta
from gui.Scaleform.daapi.view.meta.IngameMenuMeta import IngameMenuMeta
from gui.Scaleform.genConsts.GLOBAL_VARS_MGR_CONSTS import GLOBAL_VARS_MGR_CONSTS
from gui.Scaleform.genConsts.INTERFACE_STATES import INTERFACE_STATES
from gui.Scaleform.locale.TOOLTIPS import TOOLTIPS
from gui.battle_control import g_sessionProvider
from gui.battle_control import event_dispatcher as battle_event_dispatcher
from gui.shared import event_dispatcher as shared_event_dispatcher
from gui.shared import events
from gui.shared.utils.functions import makeTooltip
from helpers import i18n

class IngameMenu(IngameMenuMeta):

    def onWindowClose(self):
        self.destroy()

    def quitBattleClick(self):
        if self.app.varsManager.isTutorialRunning(GLOBAL_VARS_MGR_CONSTS.BATTLE):
            self.__doLeaveTutorial()
        else:
            self.__doLeaveArena()

    def settingsClick(self):
        shared_event_dispatcher.showSettingsWindow(redefinedKeyMode=True)

    def helpClick(self):
        self.destroy()
        battle_event_dispatcher.toggleHelp()

    def cancelClick(self):
        self.destroy()

    def _populate(self):
        super(IngameMenu, self)._populate()
        self.__setServerSettings()
        self.__setServerStats()

    def __setServerSettings(self):
        tooltipBody = i18n.makeString(TOOLTIPS.HEADER_INFO_PLAYERS_ONLINE_FULL_BODY)
        tooltipFullData = makeTooltip(TOOLTIPS.HEADER_INFO_PLAYERS_ONLINE_FULL_HEADER, tooltipBody % {'servername': connectionManager.serverUserName})
        serverName = makeHtmlString('html_templates:lobby/serverStats', 'serverName', {'name': connectionManager.serverUserName})
        self.as_setServerSettingS(serverName, tooltipFullData, INTERFACE_STATES.SHOW_ALL)

    def __setServerStats(self):
        if constants.IS_SHOW_SERVER_STATS:
            self.as_setServerStatsS(*game_control.g_instance.serverStats.getFormattedStats())

    @process
    def __doLeaveTutorial(self):
        result = yield DialogsInterface.showDialog(I18nConfirmDialogMeta('refuseTraining', focusedID=DIALOG_BUTTON_ID.CLOSE))
        if result:
            self.fireEvent(events.TutorialEvent(events.TutorialEvent.STOP_TRAINING))
            self.destroy()

    @process
    def __doLeaveArena(self):
        exitResult = g_sessionProvider.getExitResult()
        if exitResult.playerInfo is not None:
            igrType = exitResult.playerInfo.igrType
        else:
            igrType = constants.IGR_TYPE.NONE
        if constants.IS_KOREA and GUI_SETTINGS.igrEnabled and igrType != constants.IGR_TYPE.NONE:
            i18nKey = 'quitBattleIGR'
        else:
            i18nKey = 'quitBattle'
        if exitResult.isDeserter:
            result = yield DialogsInterface.showDialog(IngameDeserterDialogMeta(i18nKey + '/deserter', focusedID=DIALOG_BUTTON_ID.CLOSE))
        else:
            result = yield DialogsInterface.showDialog(I18nConfirmDialogMeta('quitBattle', focusedID=DIALOG_BUTTON_ID.CLOSE))
        if result:
            g_sessionProvider.exit()
            self.destroy()
        return