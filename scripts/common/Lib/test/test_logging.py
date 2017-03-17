# Embedded file name: scripts/common/Lib/test/test_logging.py
"""Test harness for the logging module. Run all tests.

Copyright (C) 2001-2010 Vinay Sajip. All Rights Reserved.
"""
import logging
import logging.handlers
import logging.config
import codecs
import cPickle
import cStringIO
import gc
import json
import os
import re
import select
import socket
from SocketServer import ThreadingTCPServer, StreamRequestHandler
import struct
import sys
import tempfile
from test.test_support import captured_stdout, run_with_locale, run_unittest
import textwrap
import unittest
import warnings
import weakref
try:
    import threading
except ImportError:
    threading = None

class BaseTest(unittest.TestCase):
    """Base class for logging tests."""
    log_format = '%(name)s -> %(levelname)s: %(message)s'
    expected_log_pat = '^([\\w.]+) -> ([\\w]+): ([\\d]+)$'
    message_num = 0

    def setUp(self):
        """Setup the default logging stream to an internal StringIO instance,
        so that we can examine log output as we want."""
        logger_dict = logging.getLogger().manager.loggerDict
        logging._acquireLock()
        try:
            self.saved_handlers = logging._handlers.copy()
            self.saved_handler_list = logging._handlerList[:]
            self.saved_loggers = logger_dict.copy()
            self.saved_level_names = logging._levelNames.copy()
        finally:
            logging._releaseLock()

        logging.getLogger('\xab\xd7\xbb')
        logging.getLogger(u'\u013f\xd6G')
        self.root_logger = logging.getLogger('')
        self.original_logging_level = self.root_logger.getEffectiveLevel()
        self.stream = cStringIO.StringIO()
        self.root_logger.setLevel(logging.DEBUG)
        self.root_hdlr = logging.StreamHandler(self.stream)
        self.root_formatter = logging.Formatter(self.log_format)
        self.root_hdlr.setFormatter(self.root_formatter)
        self.root_logger.addHandler(self.root_hdlr)

    def tearDown(self):
        """Remove our logging stream, and restore the original logging
        level."""
        self.stream.close()
        self.root_logger.removeHandler(self.root_hdlr)
        while self.root_logger.handlers:
            h = self.root_logger.handlers[0]
            self.root_logger.removeHandler(h)
            h.close()

        self.root_logger.setLevel(self.original_logging_level)
        logging._acquireLock()
        try:
            logging._levelNames.clear()
            logging._levelNames.update(self.saved_level_names)
            logging._handlers.clear()
            logging._handlers.update(self.saved_handlers)
            logging._handlerList[:] = self.saved_handler_list
            loggerDict = logging.getLogger().manager.loggerDict
            loggerDict.clear()
            loggerDict.update(self.saved_loggers)
        finally:
            logging._releaseLock()

    def assert_log_lines(self, expected_values, stream = None):
        """Match the collected log lines against the regular expression
        self.expected_log_pat, and compare the extracted group values to
        the expected_values list of tuples."""
        stream = stream or self.stream
        pat = re.compile(self.expected_log_pat)
        try:
            stream.reset()
            actual_lines = stream.readlines()
        except AttributeError:
            actual_lines = stream.getvalue().splitlines()

        self.assertEqual(len(actual_lines), len(expected_values))
        for actual, expected in zip(actual_lines, expected_values):
            match = pat.search(actual)
            if not match:
                self.fail('Log line does not match expected pattern:\n' + actual)
            self.assertEqual(tuple(match.groups()), expected)

        s = stream.read()
        if s:
            self.fail('Remaining output at end of log stream:\n' + s)

    def next_message(self):
        """Generate a message consisting solely of an auto-incrementing
        integer."""
        self.message_num += 1
        return '%d' % self.message_num


class BuiltinLevelsTest(BaseTest):
    """Test builtin levels and their inheritance."""

    def test_flat(self):
        m = self.next_message
        ERR = logging.getLogger('ERR')
        ERR.setLevel(logging.ERROR)
        INF = logging.getLogger('INF')
        INF.setLevel(logging.INFO)
        DEB = logging.getLogger('DEB')
        DEB.setLevel(logging.DEBUG)
        ERR.log(logging.CRITICAL, m())
        ERR.error(m())
        INF.log(logging.CRITICAL, m())
        INF.error(m())
        INF.warn(m())
        INF.info(m())
        DEB.log(logging.CRITICAL, m())
        DEB.error(m())
        DEB.warn(m())
        DEB.info(m())
        DEB.debug(m())
        ERR.warn(m())
        ERR.info(m())
        ERR.debug(m())
        INF.debug(m())
        self.assert_log_lines([('ERR', 'CRITICAL', '1'),
         ('ERR', 'ERROR', '2'),
         ('INF', 'CRITICAL', '3'),
         ('INF', 'ERROR', '4'),
         ('INF', 'WARNING', '5'),
         ('INF', 'INFO', '6'),
         ('DEB', 'CRITICAL', '7'),
         ('DEB', 'ERROR', '8'),
         ('DEB', 'WARNING', '9'),
         ('DEB', 'INFO', '10'),
         ('DEB', 'DEBUG', '11')])

    def test_nested_explicit(self):
        m = self.next_message
        INF = logging.getLogger('INF')
        INF.setLevel(logging.INFO)
        INF_ERR = logging.getLogger('INF.ERR')
        INF_ERR.setLevel(logging.ERROR)
        INF_ERR.log(logging.CRITICAL, m())
        INF_ERR.error(m())
        INF_ERR.warn(m())
        INF_ERR.info(m())
        INF_ERR.debug(m())
        self.assert_log_lines([('INF.ERR', 'CRITICAL', '1'), ('INF.ERR', 'ERROR', '2')])

    def test_nested_inherited(self):
        m = self.next_message
        INF = logging.getLogger('INF')
        INF.setLevel(logging.INFO)
        INF_ERR = logging.getLogger('INF.ERR')
        INF_ERR.setLevel(logging.ERROR)
        INF_UNDEF = logging.getLogger('INF.UNDEF')
        INF_ERR_UNDEF = logging.getLogger('INF.ERR.UNDEF')
        UNDEF = logging.getLogger('UNDEF')
        INF_UNDEF.log(logging.CRITICAL, m())
        INF_UNDEF.error(m())
        INF_UNDEF.warn(m())
        INF_UNDEF.info(m())
        INF_ERR_UNDEF.log(logging.CRITICAL, m())
        INF_ERR_UNDEF.error(m())
        INF_UNDEF.debug(m())
        INF_ERR_UNDEF.warn(m())
        INF_ERR_UNDEF.info(m())
        INF_ERR_UNDEF.debug(m())
        self.assert_log_lines([('INF.UNDEF', 'CRITICAL', '1'),
         ('INF.UNDEF', 'ERROR', '2'),
         ('INF.UNDEF', 'WARNING', '3'),
         ('INF.UNDEF', 'INFO', '4'),
         ('INF.ERR.UNDEF', 'CRITICAL', '5'),
         ('INF.ERR.UNDEF', 'ERROR', '6')])

    def test_nested_with_virtual_parent(self):
        m = self.next_message
        INF = logging.getLogger('INF')
        GRANDCHILD = logging.getLogger('INF.BADPARENT.UNDEF')
        CHILD = logging.getLogger('INF.BADPARENT')
        INF.setLevel(logging.INFO)
        GRANDCHILD.log(logging.FATAL, m())
        GRANDCHILD.info(m())
        CHILD.log(logging.FATAL, m())
        CHILD.info(m())
        GRANDCHILD.debug(m())
        CHILD.debug(m())
        self.assert_log_lines([('INF.BADPARENT.UNDEF', 'CRITICAL', '1'),
         ('INF.BADPARENT.UNDEF', 'INFO', '2'),
         ('INF.BADPARENT', 'CRITICAL', '3'),
         ('INF.BADPARENT', 'INFO', '4')])

    def test_invalid_name(self):
        self.assertRaises(TypeError, logging.getLogger, any)


class BasicFilterTest(BaseTest):
    """Test the bundled Filter class."""

    def test_filter(self):
        filter_ = logging.Filter('spam.eggs')
        handler = self.root_logger.handlers[0]
        try:
            handler.addFilter(filter_)
            spam = logging.getLogger('spam')
            spam_eggs = logging.getLogger('spam.eggs')
            spam_eggs_fish = logging.getLogger('spam.eggs.fish')
            spam_bakedbeans = logging.getLogger('spam.bakedbeans')
            spam.info(self.next_message())
            spam_eggs.info(self.next_message())
            spam_eggs_fish.info(self.next_message())
            spam_bakedbeans.info(self.next_message())
            self.assert_log_lines([('spam.eggs', 'INFO', '2'), ('spam.eggs.fish', 'INFO', '3')])
        finally:
            handler.removeFilter(filter_)


SILENT = 120
TACITURN = 119
TERSE = 118
EFFUSIVE = 117
SOCIABLE = 116
VERBOSE = 115
TALKATIVE = 114
GARRULOUS = 113
CHATTERBOX = 112
BORING = 111
LEVEL_RANGE = range(BORING, SILENT + 1)
my_logging_levels = {SILENT: 'Silent',
 TACITURN: 'Taciturn',
 TERSE: 'Terse',
 EFFUSIVE: 'Effusive',
 SOCIABLE: 'Sociable',
 VERBOSE: 'Verbose',
 TALKATIVE: 'Talkative',
 GARRULOUS: 'Garrulous',
 CHATTERBOX: 'Chatterbox',
 BORING: 'Boring'}

class GarrulousFilter(logging.Filter):
    """A filter which blocks garrulous messages."""

    def filter(self, record):
        return record.levelno != GARRULOUS


class VerySpecificFilter(logging.Filter):
    """A filter which blocks sociable and taciturn messages."""

    def filter(self, record):
        return record.levelno not in [SOCIABLE, TACITURN]


class CustomLevelsAndFiltersTest(BaseTest):
    """Test various filtering possibilities with custom logging levels."""
    expected_log_pat = '^[\\w.]+ -> ([\\w]+): ([\\d]+)$'

    def setUp(self):
        BaseTest.setUp(self)
        for k, v in my_logging_levels.items():
            logging.addLevelName(k, v)

    def log_at_all_levels(self, logger):
        for lvl in LEVEL_RANGE:
            logger.log(lvl, self.next_message())

    def test_logger_filter(self):
        self.root_logger.setLevel(VERBOSE)
        self.log_at_all_levels(self.root_logger)
        self.assert_log_lines([('Verbose', '5'),
         ('Sociable', '6'),
         ('Effusive', '7'),
         ('Terse', '8'),
         ('Taciturn', '9'),
         ('Silent', '10')])

    def test_handler_filter(self):
        self.root_logger.handlers[0].setLevel(SOCIABLE)
        try:
            self.log_at_all_levels(self.root_logger)
            self.assert_log_lines([('Sociable', '6'),
             ('Effusive', '7'),
             ('Terse', '8'),
             ('Taciturn', '9'),
             ('Silent', '10')])
        finally:
            self.root_logger.handlers[0].setLevel(logging.NOTSET)

    def test_specific_filters(self):
        handler = self.root_logger.handlers[0]
        specific_filter = None
        garr = GarrulousFilter()
        handler.addFilter(garr)
        try:
            self.log_at_all_levels(self.root_logger)
            first_lines = [('Boring', '1'),
             ('Chatterbox', '2'),
             ('Talkative', '4'),
             ('Verbose', '5'),
             ('Sociable', '6'),
             ('Effusive', '7'),
             ('Terse', '8'),
             ('Taciturn', '9'),
             ('Silent', '10')]
            self.assert_log_lines(first_lines)
            specific_filter = VerySpecificFilter()
            self.root_logger.addFilter(specific_filter)
            self.log_at_all_levels(self.root_logger)
            self.assert_log_lines(first_lines + [('Boring', '11'),
             ('Chatterbox', '12'),
             ('Talkative', '14'),
             ('Verbose', '15'),
             ('Effusive', '17'),
             ('Terse', '18'),
             ('Silent', '20')])
        finally:
            if specific_filter:
                self.root_logger.removeFilter(specific_filter)
            handler.removeFilter(garr)

        return


class MemoryHandlerTest(BaseTest):
    """Tests for the MemoryHandler."""
    expected_log_pat = '^[\\w.]+ -> ([\\w]+): ([\\d]+)$'

    def setUp(self):
        BaseTest.setUp(self)
        self.mem_hdlr = logging.handlers.MemoryHandler(10, logging.WARNING, self.root_hdlr)
        self.mem_logger = logging.getLogger('mem')
        self.mem_logger.propagate = 0
        self.mem_logger.addHandler(self.mem_hdlr)

    def tearDown(self):
        self.mem_hdlr.close()
        BaseTest.tearDown(self)

    def test_flush(self):
        self.mem_logger.debug(self.next_message())
        self.assert_log_lines([])
        self.mem_logger.info(self.next_message())
        self.assert_log_lines([])
        self.mem_logger.warn(self.next_message())
        lines = [('DEBUG', '1'), ('INFO', '2'), ('WARNING', '3')]
        self.assert_log_lines(lines)
        for n in (4, 14):
            for i in range(9):
                self.mem_logger.debug(self.next_message())

            self.assert_log_lines(lines)
            self.mem_logger.debug(self.next_message())
            lines = lines + [ ('DEBUG', str(i)) for i in range(n, n + 10) ]
            self.assert_log_lines(lines)

        self.mem_logger.debug(self.next_message())
        self.assert_log_lines(lines)


class ExceptionFormatter(logging.Formatter):
    """A special exception formatter."""

    def formatException(self, ei):
        return 'Got a [%s]' % ei[0].__name__


class ConfigFileTest(BaseTest):
    """Reading logging config from a .ini-style config file."""
    expected_log_pat = '^([\\w]+) \\+\\+ ([\\w]+)$'
    config0 = '\n    [loggers]\n    keys=root\n\n    [handlers]\n    keys=hand1\n\n    [formatters]\n    keys=form1\n\n    [logger_root]\n    level=WARNING\n    handlers=hand1\n\n    [handler_hand1]\n    class=StreamHandler\n    level=NOTSET\n    formatter=form1\n    args=(sys.stdout,)\n\n    [formatter_form1]\n    format=%(levelname)s ++ %(message)s\n    datefmt=\n    '
    config1 = '\n    [loggers]\n    keys=root,parser\n\n    [handlers]\n    keys=hand1\n\n    [formatters]\n    keys=form1\n\n    [logger_root]\n    level=WARNING\n    handlers=\n\n    [logger_parser]\n    level=DEBUG\n    handlers=hand1\n    propagate=1\n    qualname=compiler.parser\n\n    [handler_hand1]\n    class=StreamHandler\n    level=NOTSET\n    formatter=form1\n    args=(sys.stdout,)\n\n    [formatter_form1]\n    format=%(levelname)s ++ %(message)s\n    datefmt=\n    '
    config1a = '\n    [loggers]\n    keys=root,parser\n\n    [handlers]\n    keys=hand1\n\n    [formatters]\n    keys=form1\n\n    [logger_root]\n    level=WARNING\n    handlers=hand1\n\n    [logger_parser]\n    level=DEBUG\n    handlers=\n    propagate=1\n    qualname=compiler.parser\n\n    [handler_hand1]\n    class=StreamHandler\n    level=NOTSET\n    formatter=form1\n    args=(sys.stdout,)\n\n    [formatter_form1]\n    format=%(levelname)s ++ %(message)s\n    datefmt=\n    '
    config2 = config1.replace('sys.stdout', 'sys.stbout')
    config3 = config1.replace('formatter=form1', 'formatter=misspelled_name')
    config4 = '\n    [loggers]\n    keys=root\n\n    [handlers]\n    keys=hand1\n\n    [formatters]\n    keys=form1\n\n    [logger_root]\n    level=NOTSET\n    handlers=hand1\n\n    [handler_hand1]\n    class=StreamHandler\n    level=NOTSET\n    formatter=form1\n    args=(sys.stdout,)\n\n    [formatter_form1]\n    class=' + __name__ + '.ExceptionFormatter\n    format=%(levelname)s:%(name)s:%(message)s\n    datefmt=\n    '
    config5 = config1.replace('class=StreamHandler', 'class=logging.StreamHandler')
    config6 = '\n    [loggers]\n    keys=root,parser\n\n    [handlers]\n    keys=hand1, hand2\n\n    [formatters]\n    keys=form1, form2\n\n    [logger_root]\n    level=WARNING\n    handlers=\n\n    [logger_parser]\n    level=DEBUG\n    handlers=hand1\n    propagate=1\n    qualname=compiler.parser\n\n    [handler_hand1]\n    class=StreamHandler\n    level=NOTSET\n    formatter=form1\n    args=(sys.stdout,)\n\n    [handler_hand2]\n    class=StreamHandler\n    level=NOTSET\n    formatter=form1\n    args=(sys.stderr,)\n\n    [formatter_form1]\n    format=%(levelname)s ++ %(message)s\n    datefmt=\n\n    [formatter_form2]\n    format=%(message)s\n    datefmt=\n    '
    config7 = '\n    [loggers]\n    keys=root,parser,compiler\n\n    [handlers]\n    keys=hand1\n\n    [formatters]\n    keys=form1\n\n    [logger_root]\n    level=WARNING\n    handlers=hand1\n\n    [logger_compiler]\n    level=DEBUG\n    handlers=\n    propagate=1\n    qualname=compiler\n\n    [logger_parser]\n    level=DEBUG\n    handlers=\n    propagate=1\n    qualname=compiler.parser\n\n    [handler_hand1]\n    class=StreamHandler\n    level=NOTSET\n    formatter=form1\n    args=(sys.stdout,)\n\n    [formatter_form1]\n    format=%(levelname)s ++ %(message)s\n    datefmt=\n    '

    def apply_config(self, conf):
        file = cStringIO.StringIO(textwrap.dedent(conf))
        logging.config.fileConfig(file)

    def test_config0_ok(self):
        with captured_stdout() as output:
            self.apply_config(self.config0)
            logger = logging.getLogger()
            logger.info(self.next_message())
            logger.error(self.next_message())
            self.assert_log_lines([('ERROR', '2')], stream=output)
            self.assert_log_lines([])

    def test_config1_ok(self, config = config1):
        with captured_stdout() as output:
            self.apply_config(config)
            logger = logging.getLogger('compiler.parser')
            logger.info(self.next_message())
            logger.error(self.next_message())
            self.assert_log_lines([('INFO', '1'), ('ERROR', '2')], stream=output)
            self.assert_log_lines([])

    def test_config2_failure(self):
        self.assertRaises(StandardError, self.apply_config, self.config2)

    def test_config3_failure(self):
        self.assertRaises(StandardError, self.apply_config, self.config3)

    def test_config4_ok(self):
        with captured_stdout() as output:
            self.apply_config(self.config4)
            logger = logging.getLogger()
            try:
                raise RuntimeError()
            except RuntimeError:
                logging.exception('just testing')

            sys.stdout.seek(0)
            self.assertEqual(output.getvalue(), 'ERROR:root:just testing\nGot a [RuntimeError]\n')
            self.assert_log_lines([])

    def test_config5_ok(self):
        self.test_config1_ok(config=self.config5)

    def test_config6_ok(self):
        self.test_config1_ok(config=self.config6)

    def test_config7_ok(self):
        with captured_stdout() as output:
            self.apply_config(self.config1a)
            logger = logging.getLogger('compiler.parser')
            hyphenated = logging.getLogger('compiler-hyphenated')
            logger.info(self.next_message())
            logger.error(self.next_message())
            hyphenated.critical(self.next_message())
            self.assert_log_lines([('INFO', '1'), ('ERROR', '2'), ('CRITICAL', '3')], stream=output)
            self.assert_log_lines([])
        with captured_stdout() as output:
            self.apply_config(self.config7)
            logger = logging.getLogger('compiler.parser')
            self.assertFalse(logger.disabled)
            logger.info(self.next_message())
            logger.error(self.next_message())
            logger = logging.getLogger('compiler.lexer')
            logger.info(self.next_message())
            logger.error(self.next_message())
            hyphenated.critical(self.next_message())
            self.assert_log_lines([('INFO', '4'),
             ('ERROR', '5'),
             ('INFO', '6'),
             ('ERROR', '7')], stream=output)
            self.assert_log_lines([])


class LogRecordStreamHandler(StreamRequestHandler):
    """Handler for a streaming logging request. It saves the log message in the
    TCP server's 'log_output' attribute."""
    TCP_LOG_END = '!!!END!!!'

    def handle(self):
        """Handle multiple requests - each expected to be of 4-byte length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally."""
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))

            obj = self.unpickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handle_log_record(record)

    def unpickle(self, data):
        return cPickle.loads(data)

    def handle_log_record(self, record):
        if self.TCP_LOG_END in record.msg:
            self.server.abort = 1
            return
        self.server.log_output += record.msg + '\n'


class LogRecordSocketReceiver(ThreadingTCPServer):
    """A simple-minded TCP socket-based logging receiver suitable for test
    purposes."""
    allow_reuse_address = 1
    log_output = ''

    def __init__(self, host = 'localhost', port = logging.handlers.DEFAULT_TCP_LOGGING_PORT, handler = LogRecordStreamHandler):
        ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = False
        self.timeout = 0.1
        self.finished = threading.Event()

    def serve_until_stopped(self):
        while not self.abort:
            rd, wr, ex = select.select([self.socket.fileno()], [], [], self.timeout)
            if rd:
                self.handle_request()

        self.finished.set()
        self.server_close()


@unittest.skipUnless(threading, 'Threading required for this test.')

class SocketHandlerTest(BaseTest):
    """Test for SocketHandler objects."""

    def setUp(self):
        """Set up a TCP server to receive log messages, and a SocketHandler
        pointing to that server's address and port."""
        BaseTest.setUp(self)
        self.tcpserver = LogRecordSocketReceiver(port=0)
        self.port = self.tcpserver.socket.getsockname()[1]
        self.threads = [threading.Thread(target=self.tcpserver.serve_until_stopped)]
        for thread in self.threads:
            thread.start()

        self.sock_hdlr = logging.handlers.SocketHandler('localhost', self.port)
        self.sock_hdlr.setFormatter(self.root_formatter)
        self.root_logger.removeHandler(self.root_logger.handlers[0])
        self.root_logger.addHandler(self.sock_hdlr)

    def tearDown(self):
        """Shutdown the TCP server."""
        try:
            self.tcpserver.abort = True
            del self.tcpserver
            self.root_logger.removeHandler(self.sock_hdlr)
            self.sock_hdlr.close()
            for thread in self.threads:
                thread.join(2.0)

        finally:
            BaseTest.tearDown(self)

    def get_output(self):
        """Get the log output as received by the TCP server."""
        self.root_logger.critical(LogRecordStreamHandler.TCP_LOG_END)
        self.tcpserver.finished.wait(2.0)
        return self.tcpserver.log_output

    def test_output(self):
        logger = logging.getLogger('tcp')
        logger.error('spam')
        logger.debug('eggs')
        self.assertEqual(self.get_output(), 'spam\neggs\n')


class MemoryTest(BaseTest):
    """Test memory persistence of logger objects."""

    def setUp(self):
        """Create a dict to remember potentially destroyed objects."""
        BaseTest.setUp(self)
        self._survivors = {}

    def _watch_for_survival(self, *args):
        """Watch the given objects for survival, by creating weakrefs to
        them."""
        for obj in args:
            key = (id(obj), repr(obj))
            self._survivors[key] = weakref.ref(obj)

    def _assertTruesurvival(self):
        """Assert that all objects watched for survival have survived."""
        gc.collect()
        dead = []
        for (id_, repr_), ref in self._survivors.items():
            if ref() is None:
                dead.append(repr_)

        if dead:
            self.fail('%d objects should have survived but have been destroyed: %s' % (len(dead), ', '.join(dead)))
        return

    def test_persistent_loggers(self):
        self.root_logger.setLevel(logging.INFO)
        foo = logging.getLogger('foo')
        self._watch_for_survival(foo)
        foo.setLevel(logging.DEBUG)
        self.root_logger.debug(self.next_message())
        foo.debug(self.next_message())
        self.assert_log_lines([('foo', 'DEBUG', '2')])
        del foo
        self._assertTruesurvival()
        bar = logging.getLogger('foo')
        bar.debug(self.next_message())
        self.assert_log_lines([('foo', 'DEBUG', '2'), ('foo', 'DEBUG', '3')])


class EncodingTest(BaseTest):

    def test_encoding_plain_file(self):
        log = logging.getLogger('test')
        fn = tempfile.mktemp('.log')
        data = 'foo\x80'
        try:
            handler = logging.FileHandler(fn)
            log.addHandler(handler)
            try:
                log.warning(data)
            finally:
                log.removeHandler(handler)
                handler.close()

            f = open(fn)
            try:
                self.assertEqual(f.read().rstrip(), data)
            finally:
                f.close()

        finally:
            if os.path.isfile(fn):
                os.remove(fn)

    def test_encoding_cyrillic_unicode(self):
        log = logging.getLogger('test')
        message = u'\u0434\u043e \u0441\u0432\u0438\u0434\u0430\u043d\u0438\u044f'
        writer_class = codecs.getwriter('cp1251')
        writer_class.encoding = 'cp1251'
        stream = cStringIO.StringIO()
        writer = writer_class(stream, 'strict')
        handler = logging.StreamHandler(writer)
        log.addHandler(handler)
        try:
            log.warning(message)
        finally:
            log.removeHandler(handler)
            handler.close()

        s = stream.getvalue()
        self.assertEqual(s, '\xe4\xee \xf1\xe2\xe8\xe4\xe0\xed\xe8\xff\n')


class WarningsTest(BaseTest):

    def test_warnings(self):
        with warnings.catch_warnings():
            logging.captureWarnings(True)
            try:
                warnings.filterwarnings('always', category=UserWarning)
                file = cStringIO.StringIO()
                h = logging.StreamHandler(file)
                logger = logging.getLogger('py.warnings')
                logger.addHandler(h)
                warnings.warn("I'm warning you...")
                logger.removeHandler(h)
                s = file.getvalue()
                h.close()
                self.assertTrue(s.find("UserWarning: I'm warning you...\n") > 0)
                file = cStringIO.StringIO()
                warnings.showwarning('Explicit', UserWarning, 'dummy.py', 42, file, 'Dummy line')
                s = file.getvalue()
                file.close()
                self.assertEqual(s, 'dummy.py:42: UserWarning: Explicit\n  Dummy line\n')
            finally:
                logging.captureWarnings(False)


def formatFunc(format, datefmt = None):
    return logging.Formatter(format, datefmt)


def handlerFunc():
    return logging.StreamHandler()


class CustomHandler(logging.StreamHandler):
    pass


class ConfigDictTest(BaseTest):
    """Reading logging config from a dictionary."""
    expected_log_pat = '^([\\w]+) \\+\\+ ([\\w]+)$'
    config0 = {'version': 1,
     'formatters': {'form1': {'format': '%(levelname)s ++ %(message)s'}},
     'handlers': {'hand1': {'class': 'logging.StreamHandler',
                            'formatter': 'form1',
                            'level': 'NOTSET',
                            'stream': 'ext://sys.stdout'}},
     'root': {'level': 'WARNING',
              'handlers': ['hand1']}}
    config1 = {'version': 1,
     'formatters': {'form1': {'format': '%(levelname)s ++ %(message)s'}},
     'handlers': {'hand1': {'class': 'logging.StreamHandler',
                            'formatter': 'form1',
                            'level': 'NOTSET',
                            'stream': 'ext://sys.stdout'}},
     'loggers': {'compiler.parser': {'level': 'DEBUG',
                                     'handlers': ['hand1']}},
     'root': {'level': 'WARNING'}}
    config2 = {'version': 1,
     'formatters': {'form1': {'format': '%(levelname)s ++ %(message)s'}},
     'handlers': {'hand1': {'class': 'logging.StreamHandler',
                            'formatter': 'form1',
                            'level': 'NOTSET',
                            'stream': 'ext://sys.stdbout'}},
     'loggers': {'compiler.parser': {'level': 'DEBUG',
                                     'handlers': ['hand1']}},
     'root': {'level': 'WARNING'}}
    config2a = {'version': 1,
     'formatters': {'form1': {'format': '%(levelname)s ++ %(message)s'}},
     'handlers': {'hand1': {'class': 'logging.StreamHandler',
                            'formatter': 'form1',
                            'level': 'NTOSET',
                            'stream': 'ext://sys.stdout'}},
     'loggers': {'compiler.parser': {'level': 'DEBUG',
                                     'handlers': ['hand1']}},
     'root': {'level': 'WARNING'}}
    config2b = {'version': 1,
     'formatters': {'form1': {'format': '%(levelname)s ++ %(message)s'}},
     'handlers': {'hand1': {'class': 'logging.StreamHandler',
                            'formatter': 'form1',
                            'level': 'NOTSET',
                            'stream': 'ext://sys.stdout'}},
     'loggers': {'compiler.parser': {'level': 'DEBUG',
                                     'handlers': ['hand1']}},
     'root': {'level': 'WRANING'}}
    config3 = {'version': 1,
     'formatters': {'form1': {'format': '%(levelname)s ++ %(message)s'}},
     'handlers': {'hand1': {'class': 'logging.StreamHandler',
                            'formatter': 'misspelled_name',
                            'level': 'NOTSET',
                            'stream': 'ext://sys.stdout'}},
     'loggers': {'compiler.parser': {'level': 'DEBUG',
                                     'handlers': ['hand1']}},
     'root': {'level': 'WARNING'}}
    config4 = {'version': 1,
     'formatters': {'form1': {'()': __name__ + '.ExceptionFormatter',
                              'format': '%(levelname)s:%(name)s:%(message)s'}},
     'handlers': {'hand1': {'class': 'logging.StreamHandler',
                            'formatter': 'form1',
                            'level': 'NOTSET',
                            'stream': 'ext://sys.stdout'}},
     'root': {'level': 'NOTSET',
              'handlers': ['hand1']}}
    config4a = {'version': 1,
     'formatters': {'form1': {'()': ExceptionFormatter,
                              'format': '%(levelname)s:%(name)s:%(message)s'},
                    'form2': {'()': __name__ + '.formatFunc',
                              'format': '%(levelname)s:%(name)s:%(message)s'},
                    'form3': {'()': formatFunc,
                              'format': '%(levelname)s:%(name)s:%(message)s'}},
     'handlers': {'hand1': {'class': 'logging.StreamHandler',
                            'formatter': 'form1',
                            'level': 'NOTSET',
                            'stream': 'ext://sys.stdout'},
                  'hand2': {'()': handlerFunc}},
     'root': {'level': 'NOTSET',
              'handlers': ['hand1']}}
    config5 = {'version': 1,
     'formatters': {'form1': {'format': '%(levelname)s ++ %(message)s'}},
     'handlers': {'hand1': {'class': __name__ + '.CustomHandler',
                            'formatter': 'form1',
                            'level': 'NOTSET',
                            'stream': 'ext://sys.stdout'}},
     'loggers': {'compiler.parser': {'level': 'DEBUG',
                                     'handlers': ['hand1']}},
     'root': {'level': 'WARNING'}}
    config6 = {'version': 1,
     'formatters': {'form1': {'format': '%(levelname)s ++ %(message)s'}},
     'handlers': {'hand1': {'class': __name__ + '.CustomHandler',
                            'formatter': 'form1',
                            'level': 'NOTSET',
                            'stream': 'ext://sys.stdout',
                            '9': 'invalid parameter name'}},
     'loggers': {'compiler.parser': {'level': 'DEBUG',
                                     'handlers': ['hand1']}},
     'root': {'level': 'WARNING'}}
    config7 = {'version': 1,
     'formatters': {'form1': {'format': '%(levelname)s ++ %(message)s'}},
     'handlers': {'hand1': {'class': 'logging.StreamHandler',
                            'formatter': 'form1',
                            'level': 'NOTSET',
                            'stream': 'ext://sys.stdout'}},
     'loggers': {'compiler.lexer': {'level': 'DEBUG',
                                    'handlers': ['hand1']}},
     'root': {'level': 'WARNING'}}
    config8 = {'version': 1,
     'disable_existing_loggers': False,
     'formatters': {'form1': {'format': '%(levelname)s ++ %(message)s'}},
     'handlers': {'hand1': {'class': 'logging.StreamHandler',
                            'formatter': 'form1',
                            'level': 'NOTSET',
                            'stream': 'ext://sys.stdout'}},
     'loggers': {'compiler': {'level': 'DEBUG',
                              'handlers': ['hand1']},
                 'compiler.lexer': {}},
     'root': {'level': 'WARNING'}}
    config9 = {'version': 1,
     'formatters': {'form1': {'format': '%(levelname)s ++ %(message)s'}},
     'handlers': {'hand1': {'class': 'logging.StreamHandler',
                            'formatter': 'form1',
                            'level': 'WARNING',
                            'stream': 'ext://sys.stdout'}},
     'loggers': {'compiler.parser': {'level': 'WARNING',
                                     'handlers': ['hand1']}},
     'root': {'level': 'NOTSET'}}
    config9a = {'version': 1,
     'incremental': True,
     'handlers': {'hand1': {'level': 'WARNING'}},
     'loggers': {'compiler.parser': {'level': 'INFO'}}}
    config9b = {'version': 1,
     'incremental': True,
     'handlers': {'hand1': {'level': 'INFO'}},
     'loggers': {'compiler.parser': {'level': 'INFO'}}}
    config10 = {'version': 1,
     'formatters': {'form1': {'format': '%(levelname)s ++ %(message)s'}},
     'filters': {'filt1': {'name': 'compiler.parser'}},
     'handlers': {'hand1': {'class': 'logging.StreamHandler',
                            'formatter': 'form1',
                            'level': 'NOTSET',
                            'stream': 'ext://sys.stdout',
                            'filters': ['filt1']}},
     'loggers': {'compiler.parser': {'level': 'DEBUG',
                                     'filters': ['filt1']}},
     'root': {'level': 'WARNING',
              'handlers': ['hand1']}}
    config11 = {'version': 1,
     'true_formatters': {'form1': {'format': '%(levelname)s ++ %(message)s'}},
     'handler_configs': {'hand1': {'class': 'logging.StreamHandler',
                                   'formatter': 'form1',
                                   'level': 'NOTSET',
                                   'stream': 'ext://sys.stdout'}},
     'formatters': 'cfg://true_formatters',
     'handlers': {'hand1': 'cfg://handler_configs[hand1]'},
     'loggers': {'compiler.parser': {'level': 'DEBUG',
                                     'handlers': ['hand1']}},
     'root': {'level': 'WARNING'}}
    config12 = {'true_formatters': {'form1': {'format': '%(levelname)s ++ %(message)s'}},
     'handler_configs': {'hand1': {'class': 'logging.StreamHandler',
                                   'formatter': 'form1',
                                   'level': 'NOTSET',
                                   'stream': 'ext://sys.stdout'}},
     'formatters': 'cfg://true_formatters',
     'handlers': {'hand1': 'cfg://handler_configs[hand1]'},
     'loggers': {'compiler.parser': {'level': 'DEBUG',
                                     'handlers': ['hand1']}},
     'root': {'level': 'WARNING'}}
    config13 = {'version': 2,
     'true_formatters': {'form1': {'format': '%(levelname)s ++ %(message)s'}},
     'handler_configs': {'hand1': {'class': 'logging.StreamHandler',
                                   'formatter': 'form1',
                                   'level': 'NOTSET',
                                   'stream': 'ext://sys.stdout'}},
     'formatters': 'cfg://true_formatters',
     'handlers': {'hand1': 'cfg://handler_configs[hand1]'},
     'loggers': {'compiler.parser': {'level': 'DEBUG',
                                     'handlers': ['hand1']}},
     'root': {'level': 'WARNING'}}

    def apply_config(self, conf):
        logging.config.dictConfig(conf)

    def test_config0_ok(self):
        with captured_stdout() as output:
            self.apply_config(self.config0)
            logger = logging.getLogger()
            logger.info(self.next_message())
            logger.error(self.next_message())
            self.assert_log_lines([('ERROR', '2')], stream=output)
            self.assert_log_lines([])

    def test_config1_ok(self, config = config1):
        with captured_stdout() as output:
            self.apply_config(config)
            logger = logging.getLogger('compiler.parser')
            logger.info(self.next_message())
            logger.error(self.next_message())
            self.assert_log_lines([('INFO', '1'), ('ERROR', '2')], stream=output)
            self.assert_log_lines([])

    def test_config2_failure(self):
        self.assertRaises(StandardError, self.apply_config, self.config2)

    def test_config2a_failure(self):
        self.assertRaises(StandardError, self.apply_config, self.config2a)

    def test_config2b_failure(self):
        self.assertRaises(StandardError, self.apply_config, self.config2b)

    def test_config3_failure(self):
        self.assertRaises(StandardError, self.apply_config, self.config3)

    def test_config4_ok(self):
        with captured_stdout() as output:
            self.apply_config(self.config4)
            try:
                raise RuntimeError()
            except RuntimeError:
                logging.exception('just testing')

            sys.stdout.seek(0)
            self.assertEqual(output.getvalue(), 'ERROR:root:just testing\nGot a [RuntimeError]\n')
            self.assert_log_lines([])

    def test_config4a_ok(self):
        with captured_stdout() as output:
            self.apply_config(self.config4a)
            try:
                raise RuntimeError()
            except RuntimeError:
                logging.exception('just testing')

            sys.stdout.seek(0)
            self.assertEqual(output.getvalue(), 'ERROR:root:just testing\nGot a [RuntimeError]\n')
            self.assert_log_lines([])

    def test_config5_ok(self):
        self.test_config1_ok(config=self.config5)

    def test_config6_failure(self):
        self.assertRaises(StandardError, self.apply_config, self.config6)

    def test_config7_ok(self):
        with captured_stdout() as output:
            self.apply_config(self.config1)
            logger = logging.getLogger('compiler.parser')
            logger.info(self.next_message())
            logger.error(self.next_message())
            self.assert_log_lines([('INFO', '1'), ('ERROR', '2')], stream=output)
            self.assert_log_lines([])
        with captured_stdout() as output:
            self.apply_config(self.config7)
            logger = logging.getLogger('compiler.parser')
            self.assertTrue(logger.disabled)
            logger = logging.getLogger('compiler.lexer')
            logger.info(self.next_message())
            logger.error(self.next_message())
            self.assert_log_lines([('INFO', '3'), ('ERROR', '4')], stream=output)
            self.assert_log_lines([])

    def test_config_8_ok(self):
        with captured_stdout() as output:
            self.apply_config(self.config1)
            logger = logging.getLogger('compiler.parser')
            logger.info(self.next_message())
            logger.error(self.next_message())
            self.assert_log_lines([('INFO', '1'), ('ERROR', '2')], stream=output)
            self.assert_log_lines([])
        with captured_stdout() as output:
            self.apply_config(self.config8)
            logger = logging.getLogger('compiler.parser')
            self.assertFalse(logger.disabled)
            logger.info(self.next_message())
            logger.error(self.next_message())
            logger = logging.getLogger('compiler.lexer')
            logger.info(self.next_message())
            logger.error(self.next_message())
            self.assert_log_lines([('INFO', '3'),
             ('ERROR', '4'),
             ('INFO', '5'),
             ('ERROR', '6')], stream=output)
            self.assert_log_lines([])

    def test_config_9_ok(self):
        with captured_stdout() as output:
            self.apply_config(self.config9)
            logger = logging.getLogger('compiler.parser')
            logger.info(self.next_message())
            self.assert_log_lines([], stream=output)
            self.apply_config(self.config9a)
            logger.info(self.next_message())
            self.assert_log_lines([], stream=output)
            self.apply_config(self.config9b)
            logger.info(self.next_message())
            self.assert_log_lines([('INFO', '3')], stream=output)

    def test_config_10_ok(self):
        with captured_stdout() as output:
            self.apply_config(self.config10)
            logger = logging.getLogger('compiler.parser')
            logger.warning(self.next_message())
            logger = logging.getLogger('compiler')
            logger.warning(self.next_message())
            logger = logging.getLogger('compiler.lexer')
            logger.warning(self.next_message())
            logger = logging.getLogger('compiler.parser.codegen')
            logger.error(self.next_message())
            self.assert_log_lines([('WARNING', '1'), ('ERROR', '4')], stream=output)

    def test_config11_ok(self):
        self.test_config1_ok(self.config11)

    def test_config12_failure(self):
        self.assertRaises(StandardError, self.apply_config, self.config12)

    def test_config13_failure(self):
        self.assertRaises(StandardError, self.apply_config, self.config13)

    @unittest.skipUnless(threading, 'listen() needs threading to work')
    def setup_via_listener(self, text):
        t = logging.config.listen(0)
        t.start()
        t.ready.wait()
        port = t.port
        t.ready.clear()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            sock.connect(('localhost', port))
            slen = struct.pack('>L', len(text))
            s = slen + text
            sentsofar = 0
            left = len(s)
            while left > 0:
                sent = sock.send(s[sentsofar:])
                sentsofar += sent
                left -= sent

            sock.close()
        finally:
            t.ready.wait(2.0)
            logging.config.stopListening()
            t.join(2.0)

    def test_listen_config_10_ok(self):
        with captured_stdout() as output:
            self.setup_via_listener(json.dumps(self.config10))
            logger = logging.getLogger('compiler.parser')
            logger.warning(self.next_message())
            logger = logging.getLogger('compiler')
            logger.warning(self.next_message())
            logger = logging.getLogger('compiler.lexer')
            logger.warning(self.next_message())
            logger = logging.getLogger('compiler.parser.codegen')
            logger.error(self.next_message())
            self.assert_log_lines([('WARNING', '1'), ('ERROR', '4')], stream=output)

    def test_listen_config_1_ok(self):
        with captured_stdout() as output:
            self.setup_via_listener(textwrap.dedent(ConfigFileTest.config1))
            logger = logging.getLogger('compiler.parser')
            logger.info(self.next_message())
            logger.error(self.next_message())
            self.assert_log_lines([('INFO', '1'), ('ERROR', '2')], stream=output)
            self.assert_log_lines([])


class ManagerTest(BaseTest):

    def test_manager_loggerclass(self):
        logged = []

        class MyLogger(logging.Logger):

            def _log(self, level, msg, args, exc_info = None, extra = None):
                logged.append(msg)

        man = logging.Manager(None)
        self.assertRaises(TypeError, man.setLoggerClass, int)
        man.setLoggerClass(MyLogger)
        logger = man.getLogger('test')
        logger.warning('should appear in logged')
        logging.warning('should not appear in logged')
        self.assertEqual(logged, ['should appear in logged'])
        return


class ChildLoggerTest(BaseTest):

    def test_child_loggers(self):
        r = logging.getLogger()
        l1 = logging.getLogger('abc')
        l2 = logging.getLogger('def.ghi')
        c1 = r.getChild('xyz')
        c2 = r.getChild('uvw.xyz')
        self.assertTrue(c1 is logging.getLogger('xyz'))
        self.assertTrue(c2 is logging.getLogger('uvw.xyz'))
        c1 = l1.getChild('def')
        c2 = c1.getChild('ghi')
        c3 = l1.getChild('def.ghi')
        self.assertTrue(c1 is logging.getLogger('abc.def'))
        self.assertTrue(c2 is logging.getLogger('abc.def.ghi'))
        self.assertTrue(c2 is c3)


@run_with_locale('LC_ALL', '')
def test_main():
    run_unittest(BuiltinLevelsTest, BasicFilterTest, CustomLevelsAndFiltersTest, MemoryHandlerTest, ConfigFileTest, SocketHandlerTest, MemoryTest, EncodingTest, WarningsTest, ConfigDictTest, ManagerTest, ChildLoggerTest)


if __name__ == '__main__':
    test_main()