# Embedded file name: scripts/client/ClientLog.py
import debug_utils
import datetime
import Settings
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION
import atexit
import BigWorld
import sys
CLIENT_LOG_FILE = 'client.log'

class ClientLog:

    def __init__(self):
        pass

    def init(self, settings):
        self.pythonLog = 0
        self.clientLog = 0
        if settings is not None:
            self.pythonLog = settings.readInt('pythonLog', self.pythonLog)
            self.clientLog = settings.readInt('clientLog', self.clientLog)
        self.isEnabled = bool(self.pythonLog | self.clientLog)
        if self.isEnabled:
            try:
                self.logFile = open(BigWorld.getUserDataDirectory() + CLIENT_LOG_FILE, 'a')
                self.general('Init client logging : pythonLog=%s, clientLog=%s, localtime=%s' % (self.pythonLog, self.clientLog, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            except:
                LOG_CURRENT_EXCEPTION()
                self.isEnabled = False

        atexit.register(CleanLog)
        return

    def general(self, msg, *kargs):
        if self.isEnabled:
            self._doLog('GENERAL', msg, kargs)

    def gameplay(self, msg, *kargs):
        if self.isEnabled:
            self._doLog('GAMEPLAY', msg, kargs)

    def _doLog(self, s, msg, args):
        try:
            time = datetime.datetime.now()
            strTime = time.strftime('%Y-%m-%d %H:%M:%S ')
            header = '[%s] ' % s
            s = msg
            if args:
                s = s + args
            if self.pythonLog != 0:
                print header + s
            if self.clientLog != 0:
                self.logFile.write(strTime + header + s + '\n')
        except:
            LOG_ERROR('ERROR: ClientLog Write Exception', msg, args)
            LOG_CURRENT_EXCEPTION()

    def deinit(self):
        if self.isEnabled:
            self.general('Stop client logging')
            self.logFile.close()


def CleanLog():
    if g_instance:
        try:
            g_instance.deinit()
        except:
            LOG_CURRENT_EXCEPTION()

    else:
        LOG_ERROR('ERROR: deinit ClientLog has not been called')


g_instance = ClientLog()