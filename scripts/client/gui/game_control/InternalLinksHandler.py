# Embedded file name: scripts/client/gui/game_control/InternalLinksHandler.py
from adisp import async, process
from debug_utils import LOG_ERROR
from gui import GUI_SETTINGS
from gui.game_control import gc_constants
from gui.game_control.links import URLMarcos
from gui.shared import g_eventBus
from gui.shared.events import OpenLinkEvent
from helpers import dependency
from skeletons.gui.game_control import IInternalLinksController, IBrowserController
_LISTENERS = {OpenLinkEvent.CLUB_HELP: '_handleClubHelp',
 OpenLinkEvent.MEDKIT_HELP: '_handleVideoHelp',
 OpenLinkEvent.REPAIRKITHELP_HELP: '_handleVideoHelp',
 OpenLinkEvent.FIRE_EXTINGUISHERHELP_HELP: '_handleVideoHelp'}

class InternalLinksHandler(IInternalLinksController):
    browserCtrl = dependency.descriptor(IBrowserController)

    def __init__(self):
        super(InternalLinksHandler, self).__init__()
        self.__urlMarcos = None
        self._browserID = None
        return

    def init(self):
        self.__urlMarcos = URLMarcos()
        addListener = g_eventBus.addListener
        for eventType, handlerName in _LISTENERS.iteritems():
            handler = getattr(self, handlerName, None)
            if not handler:
                LOG_ERROR('Handler is not found', eventType, handlerName)
                continue
            if not callable(handler):
                LOG_ERROR('Handler is invalid', eventType, handlerName, handler)
                continue
            addListener(eventType, handler)

        return

    def fini(self):
        if self.__urlMarcos is not None:
            self.__urlMarcos.clear()
            self.__urlMarcos = None
        self._browserID = None
        removeListener = g_eventBus.removeListener
        for eventType, handlerName in _LISTENERS.iteritems():
            handler = getattr(self, handlerName, None)
            if handler:
                removeListener(eventType, handler)

        super(InternalLinksHandler, self).fini()
        return

    @async
    @process
    def getURL(self, name, callback):
        urlSettings = GUI_SETTINGS.lookup(name)
        if urlSettings:
            url = yield self.__urlMarcos.parse(str(urlSettings))
        else:
            url = yield lambda callback: callback('')
        callback(url)

    @process
    def __openInternalBrowse(self, urlName, title = '', browserSize = None, showActionBtn = True, showCloseBtn = False):
        parsedUrl = yield self.getURL(urlName)
        if parsedUrl:
            self._browserID = yield self.browserCtrl.load(parsedUrl, browserID=self._browserID, title=title, browserSize=browserSize, showActionBtn=showActionBtn, showCloseBtn=showCloseBtn)

    def _handleClubHelp(self, event):
        self.__openInternalBrowse(event.eventType, event.title, browserSize=gc_constants.BROWSER.CLUB_SIZE)

    def _handleVideoHelp(self, event):
        self.__openInternalBrowse(event.eventType, event.title, browserSize=gc_constants.BROWSER.VIDEO_SIZE, showActionBtn=False, showCloseBtn=True)