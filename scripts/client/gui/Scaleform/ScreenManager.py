# Embedded file name: scripts/client/gui/Scaleform/ScreenManager.py
import BigWorld
from gui.Scaleform import main_interfaces
from gui.LocalizationHolder import LocalizationHolder
import weakref
from config_consts import IS_DEVELOPMENT
import debug_utils
from eventhandlers.responseEvents import onMovieInitialized

class ScreenManager(object):

    def __init__(self):
        self.__idict = main_interfaces.idict
        self.__activeMovie = None
        self._initializeCalled = False
        self.__prevActiveMovieClassName = None
        return

    @property
    def initialized(self):
        return self._initializeCalled

    def destroy(self):
        self.unloadActiveMovie()

    def __getWindow(self):
        return self.__activeMovie

    activeMovie = property(__getWindow)

    @property
    def prevMovie(self):
        """
        @return: <str>  see: main_interfaces.GUI_SCREEN_LOGIN, main_interfaces.GUI_SCREEN_LOBBY, ... etc
        """
        return self.__prevActiveMovieClassName

    def loadMovie(self, className):
        self.unloadActiveMovie()
        Class = self.__idict.get(className, None)
        if Class is not None and (self.__activeMovie is None or not isinstance(self.__activeMovie, Class)):
            self.__activeMovie = Class()
            self.__activeMovie.addExternalCallbacks({'initialized': self.__initialized})
            self.__activeMovie.className = className
            self.__activeMovie.active(True)
            debug_utils.LOG_DEBUG('loadMovie=%s, %s' % (className, self.__activeMovie))
        else:
            debug_utils.LOG_ERROR('Cannot load movie: ', className)
        return

    def __initialized(self):
        self.__activeMovie.initialized()
        self._initializeCalled = True
        onMovieInitialized()

    def loadSubMovie(self, className):
        Class = self.__idict.get(className, None)
        if Class is not None:
            if className == main_interfaces.GUI_SCREEN_OPTIONS:
                movie = Class()
                self.__activeMovie.proxifyMovie(movie)
        else:
            debug_utils.LOG_ERROR('Cannot attach to movie: ', className)
        return

    def unloadSubMovie(self):
        if self.__activeMovie:
            self.__activeMovie.deproxifyMovie()

    def unloadActiveMovie(self):
        self.unloadSubMovie()
        if self.__activeMovie is not None:
            activeMovieClassName = self.__activeMovie.className
            self.__prevActiveMovieClassName = activeMovieClassName
            debug_utils.LOG_DEBUG('unloadActiveMovie={0}'.format(activeMovieClassName), self.__activeMovie, self._initializeCalled)
            test = weakref.ref(self.__activeMovie)
            if self._initializeCalled:
                self._initializeCalled = False
                self.__activeMovie.call_1('dispose')
            self.__activeMovie.dispossessUI()
            self.__activeMovie.close()
            self.__activeMovie = None
            if test() is not None:
                import gc
                debug_utils.LOG_DEBUG('Screen referrers: ', gc.get_referrers(test()))
                if IS_DEVELOPMENT:
                    import pprint
                    pprint.pprint(gc.garbage)
                    debug_utils.CRITICAL_ERROR('unloadActiveMovie: Screen {0} has refs'.format(activeMovieClassName))
                else:
                    debug_utils.LOG_ERROR('unloadActiveMovie: Screen {0} has refs'.format(activeMovieClassName))
            if IS_DEVELOPMENT:
                callbacks = BigWorld.getCallbacks()
                if callbacks:
                    debug_utils.LOG_WARNING("don't canceled callbacks: {0}".format(callbacks))
        return

    def updateLocalizationTable(self):
        loc = LocalizationHolder().getLocalization(None, self.__activeMovie.className)
        self.__activeMovie.call_1('receiveLocalization', loc)
        return