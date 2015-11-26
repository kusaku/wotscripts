# Embedded file name: scripts/client/gui/Scaleform/daapi/view/battle/gas_attack.py
import weakref
from debug_utils import LOG_ERROR
from gui.Scaleform.locale.FALLOUT import FALLOUT
from gui.battle_control import g_sessionProvider
from gui.shared.utils.plugins import IPlugin
from gui import makeHtmlString
from helpers import i18n
_PANEL_CALLBACK_NAME = 'battle.onLoadGasAttackPanel'
_TIMER_CALLBACK_NAME = 'battle.onLoadSafeZoneTimer'

class _GasAttackPanel(object):

    def __init__(self, battleUI):
        self.__flashObject = weakref.proxy(battleUI.movie.gasAttackPanel.instance)

    def destroy(self):
        self.__flashObject = None
        return

    @property
    def flashObject(self):
        return self.__flashObject

    def showStart(self):
        if self.__flashObject is not None:
            self.__flashObject.as_showStart(FALLOUT.GASATTACKPANEL_START_TITLE, FALLOUT.GASATTACKPANEL_START_MESSAGE)
        return

    def showGasAttackNear(self):
        if self.__flashObject is not None:
            self.__flashObject.as_showGasAttack(FALLOUT.GASATTACKPANEL_GASATTACK_TITLE, FALLOUT.GASATTACKPANEL_GASATTACK_MESSAGE)
        return

    def showGasAttack(self):
        if self.__flashObject is not None:
            self.__flashObject.as_showGasAttack(FALLOUT.GASATTACKPANEL_INSIDE_TITLE, FALLOUT.GASATTACKPANEL_INSIDE_MESSAGE)
        return

    def showSafeZone(self):
        if self.__flashObject is not None:
            infoStr = i18n.makeString(FALLOUT.GASATTACKPANEL_SAFEZONE_MESSAGE)
            self.__flashObject.as_showSafeZone(FALLOUT.GASATTACKPANEL_SAFEZONE_TITLE, makeHtmlString('html_templates:battle/gasAtackPanel', 'safeZone', infoStr))
        return

    def hide(self):
        if self.__flashObject is not None:
            self.__flashObject.as_hide()
        return


class _SafeZoneTimer(object):

    def __init__(self, battleUI):
        self.__flashObject = weakref.proxy(battleUI.movie.safeZoneTimer.instance)
        self.__flashObject.as_setMessage(FALLOUT.SAFEZONE_MESSAGE)

    def destroy(self):
        self.__flashObject = None
        return

    @property
    def flashObject(self):
        return self.__flashObject

    def showTimer(self, timeStr):
        if self.__flashObject is not None:
            self.__flashObject.as_showTime(timeStr)
        return

    def hideTimer(self):
        if self.__flashObject is not None:
            self.__flashObject.as_hide()
        return


class GasAttackPlugin(IPlugin):

    def __init__(self, parentObj):
        super(GasAttackPlugin, self).__init__(parentObj)
        self.__gasAttackPanel = None
        self.__safeZoneTimer = None
        return

    def init(self):
        super(GasAttackPlugin, self).init()
        self._parentObj.addExternalCallback(_PANEL_CALLBACK_NAME, self.__onLoadPanel)
        self._parentObj.addExternalCallback(_TIMER_CALLBACK_NAME, self.__onLoadSafeZone)

    def fini(self):
        self._parentObj.removeExternalCallback(_PANEL_CALLBACK_NAME)
        self._parentObj.removeExternalCallback(_TIMER_CALLBACK_NAME)
        super(GasAttackPlugin, self).fini()

    def start(self):
        super(GasAttackPlugin, self).start()
        self._parentObj.movie.falloutItems.as_loadGasAttackPanel()
        self._parentObj.movie.falloutItems.as_loadSafeZoneTimer()
        g_sessionProvider.getGasAttackCtrl().start(self._parentObj)

    def stop(self):
        g_sessionProvider.getGasAttackCtrl().stop()
        if self.__gasAttackPanel is not None:
            self.__gasAttackPanel.destroy()
            self.__gasAttackPanel = None
        if self.__safeZoneTimer is not None:
            self.__safeZoneTimer.destroy()
            self.__safeZoneTimer = None
        super(GasAttackPlugin, self).stop()
        return

    def __onLoadPanel(self, _):
        self.__gasAttackPanel = _GasAttackPanel(self._parentObj)
        g_sessionProvider.getGasAttackCtrl().setPanel(self.__gasAttackPanel)

    def __onLoadSafeZone(self, _):
        self.__safeZoneTimer = _SafeZoneTimer(self._parentObj)
        g_sessionProvider.getGasAttackCtrl().setSafeZoneTimer(self.__safeZoneTimer)