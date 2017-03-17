# Embedded file name: scripts/client/GameServiceBase.py
from debug_utils import LOG_TRACE

class GameServiceBase(object):

    def __init__(self):
        LOG_TRACE('%s::__init__' % self.__class__.__name__)
        self._gameEnvironment = None
        return

    def init(self, gameEnvr):
        LOG_TRACE('%s::init' % self.__class__.__name__)
        self._gameEnvironment = gameEnvr

    def destroy(self):
        LOG_TRACE('%s::destroy' % self.__class__.__name__)

    def doLeaveWorld(self):
        LOG_TRACE('%s::doLeaveWorld' % self.__class__.__name__)

    def afterLinking(self):
        LOG_TRACE('%s::afterLinking' % self.__class__.__name__)