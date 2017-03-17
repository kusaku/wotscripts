# Embedded file name: scripts/client/gui/WindowsManager.py
from BattleReplay import BattleReplay
import BigWorld, GUI
from gui.Scaleform import main_interfaces
from gui.Scaleform.windows import GUIWindow, GUIWindowAccount
from gui.Scaleform.ScreenManager import ScreenManager
from gui.Scaleform.Login import Login
from gui.Scaleform.Lobby import Lobby
from gui.Scaleform.Disconnect import Disconnect
from gui.Scaleform.Waiting import Waiting
import Event
from debug_utils import *
from gui.ModalWindowsManager import ModalWindowsManager
import GlobalEvents
import InputMapping
import consts

class FuncHolder:

    def __init__(self, func, *a):
        self.function = func
        self.args = a


class WindowsManager(object):

    def __init__(self):
        self.__screenManager = ScreenManager()
        self.__delayedCallback = None
        self.__delayedCallbackList = []
        self.__battleUI = None
        self.__inited = True
        self.__savedObjects = {}
        self.__savedSessionObjects = {}
        return

    def __processDelayedCallbacks(self):
        for o in self.__delayedCallbackList:
            o.function(*o.args)

        self.__delayedCallbackList = []
        if self.__delayedCallback != None:
            BigWorld.cancelCallback(self.__delayedCallback)
            self.__delayedCallback = None
        return

    def destroy(self):
        self.__savedObjects = {}
        self.__savedSessionObjects = {}
        self.__screenManager.destroy()
        self.__battleUI = None
        self.__inited = False
        GlobalEvents.onKeyEvent -= self.handleKeyEvent
        GlobalEvents.onMouseEvent -= self.handleMouseEvent
        GlobalEvents.onAxisEvent -= self.handleAxisEvent
        InputMapping.g_instance.onProfileLoaded -= self.tryStartReplay
        ModalWindowsManager().destroy()
        return

    def readSessionObject(self, name):
        LOG_DEBUG('reading session object', name)
        return self.__savedSessionObjects.get(name, None)

    def writeSessionObject(self, name, obj):
        LOG_DEBUG('writing session object', name, obj)
        self.__savedSessionObjects[name] = obj

    def clearSessionObject(self):
        LOG_DEBUG('clear session object')
        self.__savedSessionObjects.clear()

    def readObject(self, name):
        LOG_DEBUG('reading object', name)
        if self.__savedObjects.has_key(name):
            return self.__savedObjects[name]
        else:
            return None

    def writeObject(self, name, obj):
        LOG_DEBUG('writing object', name, obj)
        self.__savedObjects[name] = obj

    def onMovieLoaded(self, movieName, movieInstance):
        LOG_INFO('onMovieLoaded ' + movieName)
        GlobalEvents.onMovieLoaded(movieName, movieInstance)

    def onHideModalScreen(self, movieName):
        LOG_INFO('onMovieHide', movieName)
        GlobalEvents.onHideModalScreen(movieName)

    def start(self):
        GlobalEvents.onKeyEvent += self.handleKeyEvent
        GlobalEvents.onMouseEvent += self.handleMouseEvent
        GlobalEvents.onAxisEvent += self.handleAxisEvent
        if InputMapping.g_instance.profileLoadInProgress():
            InputMapping.g_instance.onProfileLoaded += self.tryStartReplay
        else:
            self.tryStartReplay()

    def tryStartReplay(self):
        InputMapping.g_instance.onProfileLoaded -= self.tryStartReplay
        if not BattleReplay.autoStartBattleReplay() and not consts.IS_OFFLINE_MODE_ENABLED:
            self.showLogin()

    def handleMouseEvent(self, event):
        if GUI.mcursor().visible:
            GUI.handleMouseEvent(event)
            ModalWindowsManager().handleMouseEvent(event)
            return True
        else:
            return False

    @property
    def initialized(self):
        return self.__screenManager.initialized

    @property
    def activeMovie(self):
        return self.__screenManager.activeMovie

    def handleAxisEvent(self, event):
        modalWindowResult = ModalWindowsManager().handleAxisEvent(event)
        if modalWindowResult:
            return modalWindowResult
        if self.__screenManager.activeMovie:
            return self.__screenManager.activeMovie.handleAxisEvent(event)
        return False

    def __isGUIBlocked(self, event):
        player = BigWorld.player()
        return player != None and player.isGUIBlocked(event)

    def handleKeyEvent(self, event):
        if not self.__isGUIBlocked(event):
            GUI.handleKeyEvent(event)
        modalWindowResult = ModalWindowsManager().handleKeyEvent(event)
        if modalWindowResult:
            return modalWindowResult
        if self.__screenManager.activeMovie:
            return self.__screenManager.activeMovie.handleKeyEvent(event)
        return False

    def showStartGameVideo(self):
        GUI.mcursor().shape = 'cursor_no'

    def updateLocalizationTable(self):
        self.__screenManager.updateLocalizationTable()

    def showLogin(self):
        GUI.mcursor().shape = 'arrow'
        self.__currentLanguage = None
        self.__screenManager.loadMovie(main_interfaces.GUI_SCREEN_LOGIN)
        return

    def showLobby(self):
        if self.__inited:
            import BWPersonality, time
            BWPersonality.g_loadLobbyTime = time.time()
            self.__screenManager.loadMovie(main_interfaces.GUI_SCREEN_LOBBY)

    def showPrebattle(self):
        if self.__inited:
            self.__screenManager.loadMovie(main_interfaces.GUI_SCREEN_PREBATTLE)

    def showInterview(self):
        if self.__inited:
            self.__screenManager.loadMovie(main_interfaces.GUI_SCREEN_INTERVIEW)

    def showOptions(self):
        if self.__inited:
            obj = FuncHolder(self.__screenManager.loadSubMovie, main_interfaces.GUI_SCREEN_OPTIONS)
        self.__delayedCallbackList.append(obj)
        self.__delayedCallback = BigWorld.callback(0.0, self.__processDelayedCallbacks)

    def hideOptions(self):
        if self.__inited:
            obj = FuncHolder(self.__screenManager.unloadSubMovie)
        self.__delayedCallbackList.append(obj)
        self.__delayedCallback = BigWorld.callback(0.0, self.__processDelayedCallbacks)

    def showHelpScreen(self):
        if self.__inited:
            pass

    def showBattleUI(self):
        if self.__inited:
            self.__screenManager.loadMovie(main_interfaces.GUI_SCREEN_UI)
        self.__battleUI = self.__screenManager.activeMovie

    def closeBattleUI(self):
        self.__battleUI = None
        if self.__inited:
            self.__screenManager.unloadActiveMovie()
        return

    def showLoadingBattle(self):
        if self.__inited:
            self.__screenManager.loadMovie(main_interfaces.GUI_SCREEN_BATTLELOADING)

    def getBattleUI(self):
        return self.__battleUI

    def getLobbyUI(self):
        return self.__getMovieForClass(main_interfaces.GUI_SCREEN_LOBBY)

    def getPrebatleUI(self):
        return self.__getMovieForClass(main_interfaces.GUI_SCREEN_PREBATTLE)

    def getAccountUI(self):
        if isinstance(self.__screenManager.activeMovie, GUIWindowAccount):
            return self.__screenManager.activeMovie
        else:
            return None

    @property
    def loginUI(self):
        return self.__getMovieForClass(main_interfaces.GUI_SCREEN_LOGIN)

    def getBattleLoading(self):
        return self.__getMovieForClass(main_interfaces.GUI_SCREEN_BATTLELOADING)

    def closeCurMovie(self):
        self.__screenManager.unloadActiveMovie()

    def hideAll(self):
        self.closeCurMovie()

    def __getMovieForClass(self, movieClass):
        if isinstance(self.__screenManager.activeMovie, main_interfaces.idict[movieClass]):
            return self.__screenManager.activeMovie
        else:
            return None

    def getPrevActiveMovieClassName(self):
        """
        @return: <str>  see: main_interfaces.GUI_SCREEN_LOGIN, main_interfaces.GUI_SCREEN_LOBBY, ... etc
        """
        return self.__screenManager.prevMovie

    def showBotsMenu(self):
        import exceptions
        try:
            from gui.Scaleform.development.BotsMenu import BotsMenu
            BotsMenu().active(True)
        except exceptions.ImportError:
            from debug_utils import LOG_ERROR
            LOG_ERROR('Package gui.Scaleform.development not found.')


g_windowsManager = WindowsManager()