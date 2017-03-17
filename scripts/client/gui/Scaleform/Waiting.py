# Embedded file name: scripts/client/gui/Scaleform/Waiting.py
from Event import Event
from config_consts import IS_DEVELOPMENT
from gui.Scaleform.windows import ModalWindow
from debug_utils import LOG_DEBUG, LOG_TRACE, LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_WARNING
from Helpers.i18n import localizeLobby
import BigWorld
import time

class WaitingFlags:
    NONE = 0
    WORLD_DRAW_DISABLE = 1
    LOADING_FPS_MODE = 2


WAITITNG_FLAGS = dict(((getattr(WaitingFlags, attrname), attrname) for attrname in dir(WaitingFlags) if not attrname.startswith('__') and not callable(getattr(WaitingFlags, attrname))))

class _Waiting(ModalWindow):

    def __init__(self):
        ModalWindow.__init__(self, 'waiting.swf')
        self.component.position.z = -0.1
        self.movie.backgroundAlpha = 0.0

    def setMessage(self, message):
        self.call_1('setWaitingMessage', localizeLobby(message))

    def __del__(self):
        pass


__waiting = None

class _MessageInfo(object):

    def __init__(self, message, flags):
        self.message = message
        self.flags = flags
        self.time = time.time()


class Waiting:
    CHECK_TIME = 30.0
    __checkCallbackID = None
    __window = None
    __isDisabled = False
    __freeIndex = 0
    __waitingDict = {}
    __flags = WaitingFlags.WORLD_DRAW_DISABLE
    __errorCB = []
    onHide = Event()
    onShow = Event()

    @staticmethod
    def globalDisable():
        if IS_DEVELOPMENT:
            Waiting.__isDisabled = True
            LOG_TRACE('Waiting screen is Disabled')

    @staticmethod
    def globalEnable():
        if IS_DEVELOPMENT:
            Waiting.__isDisabled = False
            LOG_TRACE('Waiting screen is Enabled')

    @classmethod
    def isVisible(cls):
        return cls.__window is not None

    @classmethod
    def isActive(cls, messageIndex):
        """
        Check if message with given index is active
        @param messageIndex: message index
        @type messageIndex: int
        @rtype: bool
        """
        return cls.__window is not None and cls.__waitingDict is not None and messageIndex in cls.__waitingDict

    @staticmethod
    def __setFlags(flags):
        if bool(flags & WaitingFlags.WORLD_DRAW_DISABLE) != bool(Waiting.__flags & WaitingFlags.WORLD_DRAW_DISABLE):
            BigWorld.worldDrawEnabled(not bool(flags & WaitingFlags.WORLD_DRAW_DISABLE))
        if bool(flags & WaitingFlags.LOADING_FPS_MODE) != bool(Waiting.__flags & WaitingFlags.LOADING_FPS_MODE):
            BigWorld.setLoadingFpsMode(bool(flags & WaitingFlags.LOADING_FPS_MODE))
        Waiting.__flags = flags

    @staticmethod
    def __refreshFlags():
        flags = WaitingFlags.NONE
        for messageinfo in Waiting.__waitingDict.itervalues():
            flags |= messageinfo.flags

        LOG_TRACE('Current waiting flags: {0}'.format(Waiting.__printableFlags(flags)))
        Waiting.__setFlags(flags)

    @staticmethod
    def __printableFlags(flags):
        return [ flname for flag, flname in WAITITNG_FLAGS.iteritems() if flags & flag ] or WAITITNG_FLAGS.get(flags, 'Unknown flags')

    @staticmethod
    def show(message, flags = WaitingFlags.NONE):
        if IS_DEVELOPMENT and Waiting.__isDisabled:
            return
        else:
            messageIndex = Waiting.__freeIndex
            Waiting.__freeIndex += 1
            LOG_TRACE('Waiting.show: {0} flags: {1}'.format(messageIndex, Waiting.__printableFlags(flags)))
            if not Waiting.__waitingDict:
                Waiting.__checkMessages()
            Waiting.__waitingDict[messageIndex] = _MessageInfo(message, flags)
            Waiting.__refreshFlags()
            if Waiting.__window is None:
                Waiting.__window = _Waiting()
                Waiting.__window.setMessage(message)
                Waiting.__window.active(True)
            else:
                Waiting.__window.setMessage(message)
            Waiting.onShow()
            return messageIndex

    @staticmethod
    def hide(messageIndex):
        if IS_DEVELOPMENT and Waiting.__isDisabled:
            return
        else:
            if Waiting.__waitingDict.pop(messageIndex, None) is None:
                LOG_WARNING('Message index {0} not in dict'.format(messageIndex))
            LOG_TRACE('Waiting.hide %d' % messageIndex)
            if not Waiting.__waitingDict:
                Waiting.__close()
            return

    @staticmethod
    def addErrorCB(callback):
        Waiting.__errorCB.append(callback)

    @staticmethod
    def removeErrorCB(callback):
        if callback in Waiting.__errorCB:
            Waiting.__errorCB.remove(callback)

    @staticmethod
    def hideAll():
        LOG_TRACE('Waiting.hideAll')
        Waiting.__close()

    @staticmethod
    def __close():
        LOG_TRACE('Waiting.close')
        if Waiting.__window is not None:
            Waiting.__window.close()
            Waiting.__window = None
            Waiting.__waitingDict.clear()
            Waiting.__refreshFlags()
            if Waiting.__checkCallbackID is not None:
                BigWorld.cancelCallback(Waiting.__checkCallbackID)
            Waiting.onHide()
        return

    @staticmethod
    def __checkMessages():
        if Waiting.__checkCallbackID is not None:
            BigWorld.cancelCallback(Waiting.__checkCallbackID)
        oldMessages = dict(((msgid, msgob) for msgid, msgob in Waiting.__waitingDict.iteritems() if time.time() - msgob.time > Waiting.CHECK_TIME))
        if oldMessages:
            LOG_ERROR('Waiting.__waitingDict', dict(((k, v.__dict__) for k, v in oldMessages.iteritems())))
            for entry in Waiting.__errorCB:
                entry()

            return
        else:
            Waiting.__checkCallbackID = BigWorld.callback(Waiting.CHECK_TIME, Waiting.__checkMessages)
            return