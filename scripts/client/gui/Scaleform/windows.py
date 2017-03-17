# Embedded file name: scripts/client/gui/Scaleform/windows.py
import GUI
from debug_utils import LOG_DEBUG, LOG_WARNING, LOG_TRACE, LOG_ERROR
from gui import Cursor
from gui.Scaleform.Flash import Flash
import BigWorld
from gui.ModalWindowsManager import ModalWindowsManager
from exchangeapi.CommonUtils import convertIfaceDataFromUI, METHODTOINDEX
import consts
from config_consts import IS_DEVELOPMENT
from functools import partial
from exchangeapi.UICallbackUtils import sendDataToUICallbacks
import weakref
import Settings
from exchangeapi import ErrorCodes
from MovingText import MovingText
from clientConsts import NEWS_TICKER_SPEED, CLASTERS
from gui.WebPageHolder import WebPageHolder
from Helpers.i18n import getFormattedTime
import time
from audio import GameSound

class CustomObject:
    pass


class ModalWindow(Flash):

    def __init__(self, swf):
        Flash.__init__(self, swf)
        component = self.component
        component.size = (2, 2)
        self.component = GUI.Window('')
        self.component.addChild(component, 'flash')
        self.component.script = self
        self.component.crossFocus = True
        self.component.dragFocus = True
        self.component.dropFocus = True
        self.component.focus = True
        self.component.moveFocus = True
        self.component.mouseButtonFocus = True
        self.movie.backgroundAlpha = 0.75
        ModalWindowsManager().add(self)

    @property
    def movie(self):
        return self.component.flash.movie

    def close(self):
        ModalWindowsManager().remove(self)
        Flash.close(self)

    def handleAxisEvent(self, event):
        return True

    def handleDragEnterEvent(self, position, dragged):
        return True

    def handleDragLeaveEvent(self, position, dragged):
        return True

    def handleDragStartEvent(self, position):
        return True

    def handleDragStopEvent(self, position):
        return True

    def handleDropEvent(self, position, dropped):
        return True

    def handleKeyEvent(self, event):
        return self.movie.handleKeyEvent(event)

    def handleMouseClickEvent(self, position):
        return True

    def handleMouseEnterEvent(self, position):
        return True

    def handleMouseEvent(self, comp, event):
        return True

    def handleMouseLeaveEvent(self, position):
        return True

    def handleMouseButtonEvent(self, comp, event):
        return True


class BattleWindow(Flash):

    def __init__(self, swf):
        Flash.__init__(self, swf)
        self.addFsCallbacks({'WoTQuit': self.onQuit,
         'WoTLogoff': self.onLogoff})
        self.afterCreate()

    def __del__(self):
        LOG_DEBUG('Deleted: %s' % self)

    def close(self):
        Flash.close(self)

    def onQuit(self, arg):
        LOG_TRACE('BattleWindow Quit')
        BigWorld.quit()

    def onLogoff(self, arg):
        BigWorld.disconnect()
        BigWorld.clearEntitiesAndSpaces()
        from gui.WindowsManager import g_windowsManager
        g_windowsManager.showLogin()


class GUIWindow(BattleWindow):

    def __init__(self, swf):
        self.isModalMovie = True
        self.__initialized = False
        BattleWindow.__init__(self, swf)
        from BWPersonality import g_repeatKeyHandlers
        g_repeatKeyHandlers.add(self.component.handleKeyEvent)
        self._modalScreen = None
        self.__prefApi = self._createPreferencesAPI()
        self._mt = MovingText(self._getRssUrl())
        self._mt.onRssDownloadReceived += self._onRssDownloadReceived
        self._mt.onRssUrlOpen += self._onRssUrlOpen
        self.__externalCallbacks = {'system.getTimeFormated': self.__getTimeFormated,
         'system.getUTC': self.__getUtc,
         'UI.saveObject': self.writeObject,
         'UI.readObject': self.readObject,
         'system.setCursor': self.setCursor,
         'UI.playSFX': self.playSFX,
         'UI.setHoverButtonRadius': self.setHoverButtonRadius,
         'UI.togglePauseMenu': self.togglePauseMenu,
         'preferences.writeNode': self.__prefApi.writeNode,
         'preferences.readNode': self.__prefApi.readNode,
         'newsTicker.openNews': self._newsTickerOpenNews,
         'UI.saveSessionObject': self._writeSessionObject,
         'UI.readSessionObject': self._readSessionObject,
         'system.pasteTextToClipboard': self.pasteTextToClipboard,
         'system.installGameUpdate': self.installGameUpdate}
        self.addExternalCallbacks(self.__externalCallbacks)
        return

    def _writeSessionObject(self, name, obj):
        from gui.WindowsManager import g_windowsManager
        g_windowsManager.writeSessionObject(name, obj)

    def _readSessionObject(self, name):
        from gui.WindowsManager import g_windowsManager
        return g_windowsManager.readSessionObject(name)

    def _clearSessionObject(self):
        from gui.WindowsManager import g_windowsManager
        g_windowsManager.clearSessionObject()

    def __getUtc(self):
        return time.time()

    def __getTimeFormated(self, utc, pattern):
        """
        @param pattern: <str> see Settings.scriptConfig.timeFormated
        """
        timeFormated = Settings.g_instance.scriptConfig.timeFormated.get(pattern, None)
        if timeFormated is not None:
            return getFormattedTime(utc, timeFormated)
        else:
            return getFormattedTime(utc)

    def _onRssUrlOpen(self, link):
        WebPageHolder().openUrl(link)

    def _getRssUrl(self):
        import BWPersonality
        rssUrl = BWPersonality.g_initPlayerInfo.rssUrl
        if rssUrl:
            return rssUrl
        return Settings.g_instance.scriptConfig.urls['rssUrl']

    def _stopTickerNews(self):
        if self._mt is not None:
            self._mt.destroy()
            self._mt = None
        return

    def _startTickerNews(self):
        self.call_1('newsTicker.setSpeed', NEWS_TICKER_SPEED)
        self.call_1('setChinaFlag', Settings.g_instance.clusterID == CLASTERS.CN)
        self._mt.start()

    def _newsTickerOpenNews(self, id):
        self._mt.showBrowser(id)

    def _onRssDownloadReceived(self, result):
        self.call_1('newsTicker.setListNews', result)

    def _createPreferencesAPI(self):
        return Settings.PreferencesAPI(Settings.g_instance.userPrefs, 'uiPreferences')

    def initialized(self, initData = None):
        self.__initialized = True
        from gui.WindowsManager import g_windowsManager
        g_windowsManager.updateLocalizationTable()
        if initData == None:
            self.call_1('init')
        else:
            self.call_1('init', initData)
        g_windowsManager.onMovieLoaded(self.className, self)
        return

    def readObject(self, name):
        from gui.WindowsManager import g_windowsManager
        return g_windowsManager.readObject(name)

    def writeObject(self, name, obj):
        from gui.WindowsManager import g_windowsManager
        g_windowsManager.writeObject(name, obj)

    def isInitialized(self):
        return self.__initialized

    def active(self, state):
        if state != self.isActive:
            Cursor.showCursor(state, False)
            BattleWindow.active(self, state)
            if state:
                self.movie.setFocussed()

    def close(self):
        self._stopTickerNews()
        for command in self.__externalCallbacks.keys():
            self.removeExternalCallback(command)

        self.__externalCallbacks = None
        del self.__prefApi
        if self.component:
            from BWPersonality import g_repeatKeyHandlers
            g_repeatKeyHandlers.discard(self.component.handleKeyEvent)
        BattleWindow.close(self)
        return

    def handleKeyEvent(self, event):
        if self._modalScreen and self._modalScreen.isFlashReady:
            return self._modalScreen.handleKeyEvent(event)
        return False

    def handleAxisEvent(self, event):
        if self._modalScreen and self._modalScreen.isFlashReady:
            return self._modalScreen.handleAxisEvent(event)
        return False

    def proxifyMovie(self, movie):
        self._modalScreen = movie
        self._modalScreen.populateUI(self)

    def deproxifyMovie(self):
        if self._modalScreen:
            self._modalScreen.dispossessUI()
            self._modalScreen = None
        return

    def setCursor(self, shape):
        mc = GUI.mcursor()
        mc.shape = shape

    def playSFX(self, name):
        GameSound().ui.play(name)

    def setHoverButtonRadius(self, r):
        GameSound().ui.setHoverButtonRadius(r)

    def togglePauseMenu(self, visble):
        GameSound().ui.toggleInGameMenu(visble)

    def pasteTextToClipboard(self, text):
        BigWorld.putTextToClipboard(text)

    def installGameUpdate(self):
        BigWorld.installGameUpdate()


def addRequestToQueue(func):

    def run(self, *args, **kwargs):
        self.addRequestCallbackToQueue(partial(func, self, *args, **kwargs))

    return run


class CallbacksQueue(object):

    def __init__(self, name):
        super(CallbacksQueue, self).__init__()
        self.__name = name
        self.__queue = []
        self.__callbacksHandlerId = None
        return

    def add(self, function):
        self.__queue.append(function)
        if self.__callbacksHandlerId is None:
            self.__callbacksHandlerId = BigWorld.callback(0, partial(self.run))
        return

    def run(self):
        startTime = time.time()
        lastError = None
        while self.__queue and time.time() - startTime < 0.01:
            function = self.__queue.pop(0)
            try:
                function()
            except Exception as e:
                LOG_ERROR('CallbacksQueue:{0}.run()'.format(self.__name), e, function)
                lastError = e
                break

        if self.__queue:
            self.__callbacksHandlerId = BigWorld.callback(0, partial(self.run))
        else:
            self.__callbacksHandlerId = None
        if lastError and IS_DEVELOPMENT:
            raise
        return

    def flush(self):
        if self.__callbacksHandlerId:
            BigWorld.cancelCallback(self.__callbacksHandlerId)
        for func in self.__queue:
            if func and func.func.__name__ != 'call_1':
                func()

        self.__queue = []


SAVED = {}
MOCK_EDIT_KEY = '__DebugMockRequest'

def processMockRequest(requestob, method, obdataResponseHandler):
    global SAVED
    try:
        interfaceData = requestob[1][0][0].values()[0]
        interfaceName = requestob[1][0][0].keys()[0]
        objType = requestob[1][0][1][0][1]
        objID = requestob[1][0][1][0][0]
        breakFlag = False
    except IndexError:
        return

    if method == 'edit' and interfaceData.get(MOCK_EDIT_KEY, False):
        interfaceData.pop(MOCK_EDIT_KEY, None)
        SAVED.setdefault(interfaceName, {}).setdefault(objType, {})[objID] = interfaceData
        breakFlag = True
    value = SAVED.get(interfaceName, {}).get(objType, {}).get(objID, None)
    if method == 'view' and value:
        response = [[1, 1], [[{interfaceName: value}, [[objType, objID]]]], ErrorCodes.SUCCESS]
        obdataResponseHandler(response)
        breakFlag = True
    return breakFlag


class GUIWindowAccount(GUIWindow):
    """
    NOTE: BigWorld.player() should be loaded at this time. Should be account
    """
    REQUESTS_QUEUE = 'requests_queue'
    RESPONSES_QUEUE = 'responses_queue'

    def __init__(self, swf):
        GUIWindow.__init__(self, swf)
        self.__dbgIfacesOutput = None
        self.callbacksStorage = set()
        self.__requestsCallbacksQueue = CallbacksQueue(self.REQUESTS_QUEUE)
        self.__responsesCallbacksQueue = CallbacksQueue(self.RESPONSES_QUEUE)
        self.requestsQueue = []
        return

    def addRequestCallbackToQueue(self, function):
        self.__requestsCallbacksQueue.add(function)

    def addResponseCallbackToQueue(self, function):
        self.__responsesCallbacksQueue.add(function)

    def initialized(self, initData = None):
        self.addExternalCallbacks({'iface.view': self.viewIFace,
         'iface.edit': self.editIFace,
         'iface.add': self.addIFace,
         'iface.delete': self.deleteIFace,
         'iface.unsubscribe': self.unsubscribeIFace,
         'iface.unsubscribeAll': self.unsubscribeAllIFaces,
         'iface.subscribe': self.subscribeIFace})
        if consts.IS_DEBUG_IMPORTED:
            try:
                import debug.AccountDebug
                self.__accountDebug = debug.AccountDebug.AccountDebugService()
            except:
                pass

        GUIWindow.initialized(self, initData)
        BigWorld.player().ifaceHandler = self.handleIfaceData
        from exchangeapi.UICallbackUtils import sendSavedUICallbacks
        sendSavedUICallbacks(self)
        from Account import DATA_STORAGE
        import BWPersonality
        dataStorage = DATA_STORAGE['ifaces'].pop(BWPersonality.g_initPlayerInfo.databaseID, {})
        dataStorage.update(DATA_STORAGE['ifaces'].pop(None, {}))
        for ids, items in dataStorage.iteritems():
            for types, entryList in items.iteritems():
                for entry in entryList:
                    ifaces, headers = entry
                    from exchangeapi.CommonUtils import joinIDTypeList, listFromId
                    idTypeList = joinIDTypeList(listFromId(ids), listFromId(types))
                    respob = [[ifaces, idTypeList]]
                    self.handleIfaceData(headers, respob)

        return

    def dispossessUI(self):
        BigWorld.player().ifaceHandler = None
        self.__requestsCallbacksQueue.flush()
        self.__responsesCallbacksQueue.flush()
        self.unsubscribeAllIFaces()
        self.requestsQueue = []
        if consts.IS_DEBUG_IMPORTED:
            try:
                if self.__accountDebug:
                    self.__accountDebug.destroy()
                    self.__accountDebug = None
            except AttributeError as ex:
                LOG_WARNING(ex)

        return

    @addRequestToQueue
    def viewIFace(self, data, callback = None, dbgCallback = None, cacheResponse = True):
        self.__requestIface(data, callback, 'view', dbgCallback, cacheResponse=cacheResponse)

    @addRequestToQueue
    def editIFace(self, data, callback = None):
        self.__requestIface(data, callback, 'edit')

    @addRequestToQueue
    def addIFace(self, data, callback = None):
        self.__requestIface(data, callback, 'add')

    @addRequestToQueue
    def deleteIFace(self, data, callback = None):
        self.__requestIface(data, callback, 'delete')
        self.unsubscribeIFace(data, None)
        return

    def __checkAccount(self, data, callback):
        import BWPersonality
        if BWPersonality.g_connectedAccountID == None or BWPersonality.g_connectedAccountID != BigWorld.player().id:
            LOG_ERROR('Account id=%d is not connected' % BigWorld.player().id, data, callback)
            return False
        else:
            return True

    def subscribeIFace(self, data, callback, force = True):
        if not self.__checkAccount(data, callback):
            return
        from exchangeapi.UICallbackUtils import addUICallback
        if callback:
            addUICallback(convertIfaceDataFromUI(data), callback, self, force=force)

    def unsubscribeAllIFaces(self):
        if not self.__checkAccount(None, None):
            return
        else:
            from exchangeapi.UICallbackUtils import removeAllUICallbacks
            removeAllUICallbacks()
            return

    def unsubscribeIFace(self, data, callback):
        if not self.__checkAccount(data, callback):
            return
        from exchangeapi.UICallbackUtils import removeUICallback
        removeUICallback(convertIfaceDataFromUI(data), callback, self)

    def handleIfaceData(self, headers, respdata):
        sendDataToUICallbacks(headers, respdata, None, self, fromserver=True)
        return

    @staticmethod
    def obdataResponse(callback, dbgCallback, movieClipRef, responseob):
        headers, respdata, code = responseob
        try:
            if respdata:
                for ifaces, idTypeList in respdata:
                    if 'ISquad' in ifaces:
                        import VOIP
                        VOIP.api().updateSquad(idTypeList[0][0], ifaces['ISquad'])

        except:
            pass

        movieClip = movieClipRef()
        if movieClip:
            if dbgCallback:
                dbgCallback(respdata)
            if code == 0:
                movieClip.subscribeIFace(respdata, callback, False)
                sendDataToUICallbacks(headers, respdata, callback, movieClip, broadcast=headers[1] != METHODTOINDEX['view'] or callback is None)
            elif callback:
                movieClip.call_1(callback, respdata, code)
        else:
            LOG_WARNING('obdataRequest: Movie already unloaded')
        return

    def __requestIface(self, data, callback, method, dbgCallback = None, cacheResponse = False):
        if not self.__checkAccount(data, callback):
            return

        def doRequest(data, callback, method, dbgCallback, cacheResponse):
            lenData = len(data)
            if cacheResponse and lenData > 50:
                from Helpers import cache
                ids, cacheID, respdata = cache.getRespdataFromCache(data)
                if respdata:
                    return GUIWindowAccount.obdataResponse(callback, dbgCallback, weakref.ref(self), [[int(consts.IS_CLIENT), METHODTOINDEX['view']], respdata, ErrorCodes.SUCCESS])

                def setToCache(dbgCallback, cacheID, ids, lenData, respdata):
                    if isinstance(respdata, list) and len(respdata) == lenData:
                        cache.setRespdataToCache(respdata, ids, cacheID)
                    if dbgCallback:
                        dbgCallback(respdata)

                dbgCallback = partial(setToCache, dbgCallback, cacheID, ids, lenData)

            def obdataRequest(requestob, callback, dbgCallback):
                from Helpers.ExchangeObBuilder import ExchangeObBuilder
                from exchangeapi.EventUtils import generateEvent
                from consts import EMPTY_IDTYPELIST
                generateEvent(method, '%s_prediction' % method, 'IClientPrediction', EMPTY_IDTYPELIST, None, {'requestBody': requestob[1],
                 'window': weakref.ref(self),
                 'callback': callback})
                callback = partial(GUIWindowAccount.obdataResponse, callback, dbgCallback, weakref.ref(self))
                breakFlag = processMockRequest(requestob, method, callback)
                if not breakFlag:
                    builder = ExchangeObBuilder(requestob)
                    builder.setFinishCallback(callback)
                    builder.build()
                return

            obdataRequest([[int(consts.IS_CLIENT)], data, METHODTOINDEX[method]], callback, dbgCallback)

        data = convertIfaceDataFromUI(data)
        if not BigWorld.player().requestsAvailable:
            self.requestsQueue.append(partial(doRequest, data, callback, method, dbgCallback, cacheResponse))
        else:
            doRequest(data, callback, method, dbgCallback, cacheResponse)


class UIInterface(object):

    def __init__(self):
        self.uiHolder = None
        player = BigWorld.player()
        self._ownerID = player and player.id or -1
        self._isFlashReady = False
        return

    def populateUI(self, proxy):
        LOG_TRACE('UIInterface.populateUI', self)
        self._isFlashReady = True
        self.uiHolder = proxy

    def dispossessUI(self):
        LOG_TRACE('UIInterface.dispossessUI', self)
        self._isFlashReady = False
        self.uiHolder = None
        return

    @property
    def isFlashReady(self):
        return self._isFlashReady

    def closeFlash(self):
        """
        after calling this method, we should not send data to the flash
        """
        self._isFlashReady = False

    def call(self, methodName, args = None):
        if self.uiHolder:
            self.uiHolder.call(methodName, args)
        else:
            LOG_WARNING('Error to %s.call("%s", ...), check for possible memory leaks' % (self.__class__, methodName))

    def call_1(self, methodName, *methodArgs):
        if self.uiHolder:
            if self._isFlashReady:
                self.uiHolder.call_1(methodName, *methodArgs)
            else:
                LOG_WARNING('Error to %s.call_1("%s", ...), Flash is not ready' % (self.__class__, methodName))
        else:
            LOG_WARNING('Error to %s.call_1("%s", ...), check for possible memory leaks' % (self.__class__, methodName))

    def respond(self, args = None):
        if self.uiHolder:
            self.uiHolder.respond(args)
        else:
            LOG_WARNING('Error to %s.respond(), check for possible memory leaks' % self.__class__)

    def handleKeyEvent(self, event):
        return False

    def handleAxisEvent(self, event):
        return False

    def setMovieVariable(self, path, value):
        if self.uiHolder:
            self.uiHolder.setMovieVariable(path, value)
        else:
            LOG_WARNING('Error to %s.setMovieVariable("%s", ...), check for possible memory leaks' % (self.__class__, path))

    def close(self):
        from gui.WindowsManager import g_windowsManager
        g_windowsManager.onHideModalScreen(self.__class__.__name__)