# Embedded file name: scripts/common/BWLogging.py
import logging
import os
import sys
import BigWorld
logging._srcfile = os.path.normcase(logging.currentframe.__code__.co_filename)

class BWLogger(logging.Logger):
    """This class extends the logging.Logger class to provide BigWorld specific
    log level support."""
    TRACE = logging.DEBUG - 1
    NOTICE = logging.INFO + 1
    HACK = logging.CRITICAL + 1

    def __init__(self, name, level = logging.NOTSET):
        logging.Logger.__init__(self, name, level)

    def trace(self, msg, *args, **kw):
        """Trace messages are the lowest priority log level within the BigWorld
        Technology ecosystem"""
        if self.isEnabledFor(BWLogger.TRACE):
            self._log(BWLogger.TRACE, msg, args, **kw)

    def notice(self, msg, *args, **kw):
        """Notice messages are listed as a severity between an INFO and
        a WARNING."""
        if self.isEnabledFor(BWLogger.NOTICE):
            self._log(BWLogger.NOTICE, msg, args, **kw)

    def hack(self, msg, *args, **kw):
        """Hack messages are the highest priority log level within the BigWorld
        Technology ecosystem"""
        if self.isEnabledFor(BWLogger.HACK):
            self._log(BWLogger.HACK, msg, args, **kw)


class BWEntityLoggerAdapter(logging.LoggerAdapter):
    """
    Logger adapter for Entities
    @param entity:
    @type entity: BigWorld.Entity | BigWorld.Proxy | BigWorld.Base
    @type logger: BWLogger
    """

    def __init__(self, entity):
        super(BWEntityLoggerAdapter, self).__init__(None, {})
        self.logger = logging.getLogger(entity.__class__.__name__)
        if not self.logger.handlers:
            eh = BWLogRedirectionHandler()
            eh.setFormatter(logging.Formatter('[%(ent_id)s%(ent_db_id)s] (%(filename)s: %(lineno)d) %(message)s'))
            self.logger.addHandler(eh)
        self.logger.propagate = False
        self.extra['ent_id'] = 'id:%s' % getattr(entity, 'id')
        self.extra['ent_db_id'] = ' dbid:%s' % getattr(entity, 'databaseID', 0)
        return


logLevelToBigWorldFunction = {logging.NOTSET: BigWorld.logTrace,
 BWLogger.TRACE: BigWorld.logTrace,
 logging.DEBUG: BigWorld.logDebug,
 logging.INFO: BigWorld.logInfo,
 BWLogger.NOTICE: BigWorld.logNotice,
 logging.WARN: BigWorld.logWarning,
 logging.WARNING: BigWorld.logWarning,
 logging.ERROR: BigWorld.logError,
 logging.CRITICAL: BigWorld.logCritical,
 logging.FATAL: BigWorld.logCritical,
 BWLogger.HACK: BigWorld.logHack}

class BWLogRedirectionHandler(logging.Handler):
    """This class extends the logging Handler class to intercept a log message
    and redirect it to the BigWorld log message handlers for transport to
    MessageLogger."""

    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        """
        @type record: logging.LogRecord
        """
        logCategory = record.name.encode(sys.getdefaultencoding())
        msg = self.format(record)
        finalMessage = msg.encode(sys.getdefaultencoding())
        bwInternalLogFunction = logLevelToBigWorldFunction[record.levelno]
        bwInternalLogFunction(logCategory, finalMessage)


_bwRedirectionHandler = None

def init():
    """Initialise the BWLogging module."""
    global _bwRedirectionHandler
    if _bwRedirectionHandler is None:
        _bwRedirectionHandler = BWLogRedirectionHandler()
        _bwRedirectionHandler.setFormatter(logging.Formatter('(%(filename)s: %(lineno)d) %(message)s'))
    logging.setLoggerClass(BWLogger)
    logging.addLevelName(BWLogger.TRACE, 'TRACE')
    logging.addLevelName(BWLogger.NOTICE, 'NOTICE')
    logging.addLevelName(BWLogger.HACK, 'HACK')
    rootLogger = logging.getLogger()
    del rootLogger.handlers[:]
    rootLogger.addHandler(_bwRedirectionHandler)
    rootLogger.setLevel(BWLogger.TRACE)
    logging.captureWarnings(True)
    return


def getLogger(obj = None):
    """
    Return logger instance
    @type obj: None | str | BigWorld.Entity | BigWorld.Base | BigWorld.Proxy | BigWorld.Service
    @rtype: BWLogger
    """
    if obj is None:
        return logging.getLogger('Script')
    elif isinstance(obj, basestring):
        return logging.getLogger(obj)
    else:
        return BWEntityLoggerAdapter(obj)