# Embedded file name: scripts/client/gui/Scaleform/WebBrowser.py
import base64
import BigWorld
import Settings
import GlobalEvents
from debug_utils import LOG_TRACE
from debug_utils import LOG_ERROR
from ConnectionManager import connectionManager

class WebBrowser(object):
    URL_KONG = 'urlKong'
    BATTLE_COUNT = 11
    BattleCount = 0
    BattleFinished = False
    ProceedLogin = False

    def __init__(self, lobby):
        self.kongUrl = None
        self.shadow = None
        self.lobby = lobby
        self.frames = {}
        self.areaID = None
        self.userEncoded = None
        self.databaseID = None
        return

    def show(self):
        if self.shadow is None:
            self.lobby.call_1('hangar.showBrowser')
        return

    def showIfNecessary(self):
        condition_FromLobby = WebBrowser.ProceedLogin
        condition_FromNthBattle = WebBrowser.BattleFinished and WebBrowser.BattleCount % WebBrowser.BATTLE_COUNT == 0
        if condition_FromLobby or condition_FromNthBattle:
            self.show()

    def release(self):
        self.lobby = None
        WebBrowser.BattleFinished = False
        WebBrowser.ProceedLogin = False
        return

    def onOpen(self):
        if self.shadow is None:
            self.performInitialization()
        else:
            self.shadow.updateSurface()
        return

    def onRefresh(self):
        if self.shadow is not None:
            self.shadow.awesomium.loadURL(self.kongUrl)
        return

    def onClose(self):
        if self.shadow is not None:
            self.performUninitialization()
        return

    def handleKeyEvent(self, event):
        if self.shadow is None:
            return False
        else:
            return self.shadow.handleKeyEvent(event)

    def handleMouseWheelEvent(self, event):
        if self.shadow is None:
            return False
        else:
            return self.shadow.handleMouseWheelEvent(event)

    def handleMouseMoveEvent(self, xpos, ypos):
        if self.shadow is None:
            return False
        else:
            return self.shadow.handleMouseMoveEvent(float(xpos), float(ypos))

    def onChangeTitle(self, title):
        pass

    def onChangeAddressBar(self, addressBar):
        pass

    def onChangeTooltip(self, tooltip):
        pass

    def onChangeTargetURL(self, targetURL):
        pass

    def onChangeCursor(self, cursor):
        pass

    def onBeginLoadingFrame(self, frame, isMainFrame, spec):
        self.frames[frame] = True
        if len(self.frames) == 1:
            self.lobby.call_1('browser.beginloadingframe')

    def onFailLoadingFrame(self, frame, isMainFrame, errorCode, spec):
        if frame in self.frames:
            del self.frames[frame]
        if len(self.frames) == 0:
            self.lobby.call_1('browser.finishloadingframe')

    def onFinishLoadingFrame(self, frame, isMainFrame, spec):
        if frame in self.frames:
            del self.frames[frame]
        if len(self.frames) == 0:
            self.lobby.call_1('browser.finishloadingframe')

    def onDocumentReady(self, spec):
        pass

    def performInitialization(self):
        LOG_TRACE('WebBrowser: initializing...')
        areaID = connectionManager.areaID
        loginName = connectionManager.loginName
        if areaID is None or loginName is None:
            LOG_ERROR('WebBrowser: Unable to open browser: bad areaID or loginName in script_config.xml', areaID, loginName)
            return
        else:
            try:
                self.kongUrl = Settings.g_instance.scriptConfig.urls[WebBrowser.URL_KONG]
                self.areaID = areaID
                self.userEncoded = base64.b64encode(loginName)
                self.shadow = BigWorld.WebBrowser()
                self.shadow.awesomium.script = self
                GlobalEvents.onKeyEvent += self.handleKeyEvent
                GlobalEvents.onMouseEvent.insert(0, self.handleMouseWheelEvent)
                BigWorld.player().tokenManager.requestToken(self.receiveDatabaseIDAndContinueInitialization)
            except:
                LOG_ERROR('WebBrowser: initialization failed')

            return

    def performUninitialization(self):
        self.kongUrl = None
        self.shadow = None
        self.areaID = None
        self.userEncoded = None
        self.databaseID = None
        GlobalEvents.onKeyEvent -= self.handleKeyEvent
        GlobalEvents.onMouseEvent.remove(self.handleMouseWheelEvent)
        LOG_TRACE('WebBrowser: uninitialized')
        return

    def receiveDatabaseIDAndContinueInitialization(self, databaseID, token):
        self.databaseID = databaseID
        self.kongUrl = self.kongUrl % {'userEncoded': self.userEncoded,
         'areaID': self.areaID,
         'databaseID': self.databaseID}
        self.shadow.awesomium.loadURL(self.kongUrl)
        LOG_TRACE('WebBrowser: initialized.')

    @staticmethod
    def ReportBecomePlayer():
        if WebBrowser.ProceedLogin:
            return
        WebBrowser.BattleCount += 1
        WebBrowser.BattleFinished = True

    @staticmethod
    def ReportLoginProceed():
        WebBrowser.ProceedLogin = True