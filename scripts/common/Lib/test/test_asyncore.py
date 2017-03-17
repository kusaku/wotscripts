# Embedded file name: scripts/common/Lib/test/test_asyncore.py
import asyncore
import unittest
import select
import os
import socket
import sys
import time
import warnings
import errno
from test import test_support
from test.test_support import TESTFN, run_unittest, unlink
from StringIO import StringIO
try:
    import threading
except ImportError:
    threading = None

HOST = test_support.HOST

class dummysocket:

    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True

    def fileno(self):
        return 42


class dummychannel:

    def __init__(self):
        self.socket = dummysocket()

    def close(self):
        self.socket.close()


class exitingdummy:

    def __init__(self):
        pass

    def handle_read_event(self):
        raise asyncore.ExitNow()

    handle_write_event = handle_read_event
    handle_close = handle_read_event
    handle_expt_event = handle_read_event


class crashingdummy:

    def __init__(self):
        self.error_handled = False

    def handle_read_event(self):
        raise Exception()

    handle_write_event = handle_read_event
    handle_close = handle_read_event
    handle_expt_event = handle_read_event

    def handle_error(self):
        self.error_handled = True


def capture_server(evt, buf, serv):
    try:
        serv.listen(5)
        conn, addr = serv.accept()
    except socket.timeout:
        pass
    else:
        n = 200
        while n > 0:
            r, w, e = select.select([conn], [], [])
            if r:
                data = conn.recv(10)
                buf.write(data.replace('\n', ''))
                if '\n' in data:
                    break
            n -= 1
            time.sleep(0.01)

        conn.close()
    finally:
        serv.close()
        evt.set()


class HelperFunctionTests(unittest.TestCase):

    def test_readwriteexc(self):
        tr1 = exitingdummy()
        self.assertRaises(asyncore.ExitNow, asyncore.read, tr1)
        self.assertRaises(asyncore.ExitNow, asyncore.write, tr1)
        self.assertRaises(asyncore.ExitNow, asyncore._exception, tr1)
        tr2 = crashingdummy()
        asyncore.read(tr2)
        self.assertEqual(tr2.error_handled, True)
        tr2 = crashingdummy()
        asyncore.write(tr2)
        self.assertEqual(tr2.error_handled, True)
        tr2 = crashingdummy()
        asyncore._exception(tr2)
        self.assertEqual(tr2.error_handled, True)

    @unittest.skipUnless(hasattr(select, 'poll'), 'select.poll required')
    def test_readwrite(self):
        attributes = ('read', 'expt', 'write', 'closed', 'error_handled')
        expected = ((select.POLLIN, 'read'),
         (select.POLLPRI, 'expt'),
         (select.POLLOUT, 'write'),
         (select.POLLERR, 'closed'),
         (select.POLLHUP, 'closed'),
         (select.POLLNVAL, 'closed'))

        class testobj:

            def __init__(self):
                self.read = False
                self.write = False
                self.closed = False
                self.expt = False
                self.error_handled = False

            def handle_read_event(self):
                self.read = True

            def handle_write_event(self):
                self.write = True

            def handle_close(self):
                self.closed = True

            def handle_expt_event(self):
                self.expt = True

            def handle_error(self):
                self.error_handled = True

        for flag, expectedattr in expected:
            tobj = testobj()
            self.assertEqual(getattr(tobj, expectedattr), False)
            asyncore.readwrite(tobj, flag)
            for attr in attributes:
                self.assertEqual(getattr(tobj, attr), attr == expectedattr)

            tr1 = exitingdummy()
            self.assertRaises(asyncore.ExitNow, asyncore.readwrite, tr1, flag)
            tr2 = crashingdummy()
            self.assertEqual(tr2.error_handled, False)
            asyncore.readwrite(tr2, flag)
            self.assertEqual(tr2.error_handled, True)

    def test_closeall(self):
        self.closeall_check(False)

    def test_closeall_default(self):
        self.closeall_check(True)

    def closeall_check(self, usedefault):
        l = []
        testmap = {}
        for i in range(10):
            c = dummychannel()
            l.append(c)
            self.assertEqual(c.socket.closed, False)
            testmap[i] = c

        if usedefault:
            socketmap = asyncore.socket_map
            try:
                asyncore.socket_map = testmap
                asyncore.close_all()
            finally:
                testmap, asyncore.socket_map = asyncore.socket_map, socketmap

        else:
            asyncore.close_all(testmap)
        self.assertEqual(len(testmap), 0)
        for c in l:
            self.assertEqual(c.socket.closed, True)

    def test_compact_traceback(self):
        try:
            raise Exception("I don't like spam!")
        except:
            real_t, real_v, real_tb = sys.exc_info()
            r = asyncore.compact_traceback()
        else:
            self.fail('Expected exception')

        (f, function, line), t, v, info = r
        self.assertEqual(os.path.split(f)[-1], 'test_asyncore.py')
        self.assertEqual(function, 'test_compact_traceback')
        self.assertEqual(t, real_t)
        self.assertEqual(v, real_v)
        self.assertEqual(info, '[%s|%s|%s]' % (f, function, line))


class DispatcherTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        asyncore.close_all()

    def test_basic(self):
        d = asyncore.dispatcher()
        self.assertEqual(d.readable(), True)
        self.assertEqual(d.writable(), True)

    def test_repr(self):
        d = asyncore.dispatcher()
        self.assertEqual(repr(d), '<asyncore.dispatcher at %#x>' % id(d))

    def test_log(self):
        d = asyncore.dispatcher()
        fp = StringIO()
        stderr = sys.stderr
        l1 = 'Lovely spam! Wonderful spam!'
        l2 = "I don't like spam!"
        try:
            sys.stderr = fp
            d.log(l1)
            d.log(l2)
        finally:
            sys.stderr = stderr

        lines = fp.getvalue().splitlines()
        self.assertEqual(lines, ['log: %s' % l1, 'log: %s' % l2])

    def test_log_info(self):
        d = asyncore.dispatcher()
        fp = StringIO()
        stdout = sys.stdout
        l1 = 'Have you got anything without spam?'
        l2 = "Why can't she have egg bacon spam and sausage?"
        l3 = "THAT'S got spam in it!"
        try:
            sys.stdout = fp
            d.log_info(l1, 'EGGS')
            d.log_info(l2)
            d.log_info(l3, 'SPAM')
        finally:
            sys.stdout = stdout

        lines = fp.getvalue().splitlines()
        expected = ['EGGS: %s' % l1, 'info: %s' % l2, 'SPAM: %s' % l3]
        self.assertEqual(lines, expected)

    def test_unhandled(self):
        d = asyncore.dispatcher()
        d.ignore_log_types = ()
        fp = StringIO()
        stdout = sys.stdout
        try:
            sys.stdout = fp
            d.handle_expt()
            d.handle_read()
            d.handle_write()
            d.handle_connect()
            d.handle_accept()
        finally:
            sys.stdout = stdout

        lines = fp.getvalue().splitlines()
        expected = ['warning: unhandled incoming priority event',
         'warning: unhandled read event',
         'warning: unhandled write event',
         'warning: unhandled connect event',
         'warning: unhandled accept event']
        self.assertEqual(lines, expected)

    def test_issue_8594(self):
        d = asyncore.dispatcher(socket.socket())
        self.assertRaisesRegexp(AttributeError, 'dispatcher instance', getattr, d, 'foo')
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            family = d.family
            self.assertEqual(family, socket.AF_INET)
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))

    def test_strerror(self):
        err = asyncore._strerror(errno.EPERM)
        if hasattr(os, 'strerror'):
            self.assertEqual(err, os.strerror(errno.EPERM))
        err = asyncore._strerror(-1)
        self.assertTrue(err != '')


class dispatcherwithsend_noread(asyncore.dispatcher_with_send):

    def readable(self):
        return False

    def handle_connect(self):
        pass


class DispatcherWithSendTests(unittest.TestCase):
    usepoll = False

    def setUp(self):
        pass

    def tearDown(self):
        asyncore.close_all()

    @unittest.skipUnless(threading, 'Threading required for this test.')
    @test_support.reap_threads
    def test_send(self):
        evt = threading.Event()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        port = test_support.bind_port(sock)
        cap = StringIO()
        args = (evt, cap, sock)
        t = threading.Thread(target=capture_server, args=args)
        t.start()
        try:
            time.sleep(0.2)
            data = "Suppose there isn't a 16-ton weight?"
            d = dispatcherwithsend_noread()
            d.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            d.connect((HOST, port))
            time.sleep(0.1)
            d.send(data)
            d.send(data)
            d.send('\n')
            n = 1000
            while d.out_buffer and n > 0:
                asyncore.poll()
                n -= 1

            evt.wait()
            self.assertEqual(cap.getvalue(), data * 2)
        finally:
            t.join()


class DispatcherWithSendTests_UsePoll(DispatcherWithSendTests):
    usepoll = True


@unittest.skipUnless(hasattr(asyncore, 'file_wrapper'), 'asyncore.file_wrapper required')

class FileWrapperTest(unittest.TestCase):

    def setUp(self):
        self.d = "It's not dead, it's sleeping!"
        with file(TESTFN, 'w') as h:
            h.write(self.d)

    def tearDown(self):
        unlink(TESTFN)

    def test_recv(self):
        fd = os.open(TESTFN, os.O_RDONLY)
        w = asyncore.file_wrapper(fd)
        os.close(fd)
        self.assertNotEqual(w.fd, fd)
        self.assertNotEqual(w.fileno(), fd)
        self.assertEqual(w.recv(13), "It's not dead")
        self.assertEqual(w.read(6), ", it's")
        w.close()
        self.assertRaises(OSError, w.read, 1)

    def test_send(self):
        d1 = 'Come again?'
        d2 = 'I want to buy some cheese.'
        fd = os.open(TESTFN, os.O_WRONLY | os.O_APPEND)
        w = asyncore.file_wrapper(fd)
        os.close(fd)
        w.write(d1)
        w.send(d2)
        w.close()
        self.assertEqual(file(TESTFN).read(), self.d + d1 + d2)

    @unittest.skipUnless(hasattr(asyncore, 'file_dispatcher'), 'asyncore.file_dispatcher required')
    def test_dispatcher(self):
        fd = os.open(TESTFN, os.O_RDONLY)
        data = []

        class FileDispatcher(asyncore.file_dispatcher):

            def handle_read(self):
                data.append(self.recv(29))

        s = FileDispatcher(fd)
        os.close(fd)
        asyncore.loop(timeout=0.01, use_poll=True, count=2)
        self.assertEqual(''.join(data), self.d)


class BaseTestHandler(asyncore.dispatcher):

    def __init__(self, sock = None):
        asyncore.dispatcher.__init__(self, sock)
        self.flag = False

    def handle_accept(self):
        raise Exception('handle_accept not supposed to be called')

    def handle_connect(self):
        raise Exception('handle_connect not supposed to be called')

    def handle_expt(self):
        raise Exception('handle_expt not supposed to be called')

    def handle_close(self):
        raise Exception('handle_close not supposed to be called')

    def handle_error(self):
        raise


class TCPServer(asyncore.dispatcher):
    """A server which listens on an address and dispatches the
    connection to a handler.
    """

    def __init__(self, handler = BaseTestHandler, host = HOST, port = 0):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.handler = handler

    @property
    def address(self):
        return self.socket.getsockname()[:2]

    def handle_accept(self):
        sock, addr = self.accept()
        self.handler(sock)

    def handle_error(self):
        raise


class BaseClient(BaseTestHandler):

    def __init__(self, address):
        BaseTestHandler.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(address)

    def handle_connect(self):
        pass


class BaseTestAPI(unittest.TestCase):

    def tearDown(self):
        asyncore.close_all()

    def loop_waiting_for_flag(self, instance, timeout = 5):
        timeout = float(timeout) / 100
        count = 100
        while asyncore.socket_map and count > 0:
            asyncore.loop(timeout=0.01, count=1, use_poll=self.use_poll)
            if instance.flag:
                return
            count -= 1
            time.sleep(timeout)

        self.fail('flag not set')

    def test_handle_connect(self):

        class TestClient(BaseClient):

            def handle_connect(self):
                self.flag = True

        server = TCPServer()
        client = TestClient(server.address)
        self.loop_waiting_for_flag(client)

    def test_handle_accept(self):

        class TestListener(BaseTestHandler):

            def __init__(self):
                BaseTestHandler.__init__(self)
                self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
                self.bind((HOST, 0))
                self.listen(5)
                self.address = self.socket.getsockname()[:2]

            def handle_accept(self):
                self.flag = True

        server = TestListener()
        client = BaseClient(server.address)
        self.loop_waiting_for_flag(server)

    def test_handle_read(self):

        class TestClient(BaseClient):

            def handle_read(self):
                self.flag = True

        class TestHandler(BaseTestHandler):

            def __init__(self, conn):
                BaseTestHandler.__init__(self, conn)
                self.send('x' * 1024)

        server = TCPServer(TestHandler)
        client = TestClient(server.address)
        self.loop_waiting_for_flag(client)

    def test_handle_write(self):

        class TestClient(BaseClient):

            def handle_write(self):
                self.flag = True

        server = TCPServer()
        client = TestClient(server.address)
        self.loop_waiting_for_flag(client)

    def test_handle_close(self):

        class TestClient(BaseClient):

            def handle_read(self):
                self.recv(1024)

            def handle_close(self):
                self.flag = True
                self.close()

        class TestHandler(BaseTestHandler):

            def __init__(self, conn):
                BaseTestHandler.__init__(self, conn)
                self.close()

        server = TCPServer(TestHandler)
        client = TestClient(server.address)
        self.loop_waiting_for_flag(client)

    @unittest.skipIf(sys.platform.startswith('sunos'), 'OOB support is broken on Solaris')
    def test_handle_expt(self):

        class TestClient(BaseClient):

            def handle_expt(self):
                self.flag = True

        class TestHandler(BaseTestHandler):

            def __init__(self, conn):
                BaseTestHandler.__init__(self, conn)
                self.socket.send(chr(244), socket.MSG_OOB)

        server = TCPServer(TestHandler)
        client = TestClient(server.address)
        self.loop_waiting_for_flag(client)

    def test_handle_error(self):

        class TestClient(BaseClient):

            def handle_write(self):
                1.0 / 0

            def handle_error(self):
                self.flag = True
                try:
                    raise
                except ZeroDivisionError:
                    pass
                else:
                    raise Exception('exception not raised')

        server = TCPServer()
        client = TestClient(server.address)
        self.loop_waiting_for_flag(client)

    def test_connection_attributes(self):
        server = TCPServer()
        client = BaseClient(server.address)
        self.assertFalse(server.connected)
        self.assertTrue(server.accepting)
        self.assertFalse(client.accepting)
        asyncore.loop(timeout=0.01, use_poll=self.use_poll, count=100)
        self.assertFalse(server.connected)
        self.assertTrue(server.accepting)
        self.assertTrue(client.connected)
        self.assertFalse(client.accepting)
        client.close()
        self.assertFalse(server.connected)
        self.assertTrue(server.accepting)
        self.assertFalse(client.connected)
        self.assertFalse(client.accepting)
        server.close()
        self.assertFalse(server.connected)
        self.assertFalse(server.accepting)

    def test_create_socket(self):
        s = asyncore.dispatcher()
        s.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.assertEqual(s.socket.family, socket.AF_INET)
        self.assertEqual(s.socket.type, socket.SOCK_STREAM)

    def test_bind(self):
        s1 = asyncore.dispatcher()
        s1.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.bind((HOST, 0))
        s1.listen(5)
        port = s1.socket.getsockname()[1]
        s2 = asyncore.dispatcher()
        s2.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.assertRaises(socket.error, s2.bind, (HOST, port))

    def test_set_reuse_addr(self):
        sock = socket.socket()
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error:
            unittest.skip('SO_REUSEADDR not supported on this platform')
        else:
            s = asyncore.dispatcher(socket.socket())
            self.assertFalse(s.socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR))
            s.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            s.set_reuse_addr()
            self.assertTrue(s.socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR))
        finally:
            sock.close()


class TestAPI_UseSelect(BaseTestAPI):
    use_poll = False


@unittest.skipUnless(hasattr(select, 'poll'), 'select.poll required')

class TestAPI_UsePoll(BaseTestAPI):
    use_poll = True


def test_main():
    tests = [HelperFunctionTests,
     DispatcherTests,
     DispatcherWithSendTests,
     DispatcherWithSendTests_UsePoll,
     TestAPI_UseSelect,
     TestAPI_UsePoll,
     FileWrapperTest]
    run_unittest(*tests)


if __name__ == '__main__':
    test_main()