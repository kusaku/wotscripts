# Embedded file name: scripts/client/VOIP/__init__.py
import BigWorld
from debug_utils import LOG_WARNING, LOG_ERROR

class _Stub:

    def __init__(self, name):
        self.__name = name

    class _Attr:

        def __init__(self, name):
            self.__name = name

        def __nonzero__(self):
            LOG_WARNING('{0}: not initialized; property will return False'.format(self.__name))
            return False

        def __call__(self, *args, **kwargs):
            LOG_WARNING('{0}: not initialized; call ignored'.format(self.__name))

        def __iadd__(self, delegate):
            LOG_WARNING('{0}: not initialized; operator + ignored'.format(self.__name))
            return self

        def __isub__(self, delegate):
            LOG_WARNING('{0}: not initialized; operator - ignored'.format(self.__name))
            return self

    def __nonzero__(self):
        return False

    def __getattr__(self, name):
        if name.startswith('_'):
            return self.__dict__[name]
        return _Stub._Attr(self.__name + '.' + name)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            self.__dict__[name] = value
        else:
            LOG_WARNING('{0}.{1}: not initialized; property will not be set'.format(self.__name, name))

    def __repr__(self):
        return '<Null>'


_api = _Stub('VOIP.api()')
_initCallbacks = []

def initialize(playerID):
    global _api
    global _initCallbacks
    if not _api:
        from API import API
        _api = API(playerID)
        import Settings
        settings = Settings.g_instance.getVoipSettings()
        _api.updateSettings(voiceActivationLevel=settings['micVolume'], voiceVolume=settings['masterVolume'], muffledMasterVolume=settings['fadeVolume'], autoConnectArenaChannel=settings['autoConnectArenaChannel'], captureDevice=settings['captureDevice'])
        _api.enabled = settings['isVoipEnabled']
        for func in _initCallbacks:
            func()

        _initCallbacks = []
    elif playerID != _api.playerID:
        LOG_ERROR('VOIP.initialize failed: attempt to change player ID from {0} to {1}'.format(_api.playerID, playerID))
    else:
        _api._initialize()


def shutdown():
    global _api
    global _initCallbacks
    if _api:
        _api._shutdown()
        _api = _Stub('VOIP.api()')
    _initCallbacks = []


def callWhenInitialized(func):
    """ Calls func immediately if API is already initialized.
        Otherwise, call is deferred until call to VOIP.initialize().
        Any call to VOIP.shutdown() always clears list of previously deferred calls.
    """
    if _api:
        func()
    else:
        _initCallbacks.append(func)


def api():
    return _api