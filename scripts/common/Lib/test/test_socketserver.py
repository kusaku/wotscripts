# Embedded file name: scripts/common/Lib/test/test_socketserver.py
"""
Test suite for SocketServer.py.
"""
import contextlib
import imp
import os
import select
import signal
import socket
import tempfile
import unittest
import SocketServer
import test.test_support
from test.test_support import reap_children, reap_threads, verbose
try:
    import threading
except ImportError:
    threading = None

test.test_support.requires('network')
TEST_STR = 'hello world\n'
HOST = test.test_support.HOST
HAVE_UNIX_SOCKETS = hasattr(socket, 'AF_UNIX')
HAVE_FORKING = hasattr(os, 'fork') and os.name != 'os2'

def signal_alarm(n):
    """Call signal.alarm when it exists (i.e. not on Windows)."""
    if hasattr(signal, 'alarm'):
        signal.alarm(n)


def receive(sock, n, timeout = 20):
    r, w, x = select.select([sock], [], [], timeout)
    if sock in r:
        return sock.recv(n)
    raise RuntimeError, 'timed out on %r' % (sock,)


if HAVE_UNIX_SOCKETS:

    class ForkingUnixStreamServer(SocketServer.ForkingMixIn, SocketServer.UnixStreamServer):
        pass


    class ForkingUnixDatagramServer(SocketServer.ForkingMixIn, SocketServer.UnixDatagramServer):
        pass


@contextlib.contextmanager
def simple_subprocess(testcase):
    pid = os.fork()
    if pid == 0:
        os._exit(72)
    yield
    pid2, status = os.waitpid(pid, 0)
    testcase.assertEqual(pid2, pid)
    testcase.assertEqual(18432, status)
    return


@unittest.skipUnless(threading, 'Threading required for this test.')

class SocketServerTest(unittest.TestCase):
    """Test all socket servers."""

    def setUp(self):
        signal_alarm(60)
        self.port_seed = 0
        self.test_files = []

    def tearDown(self):
        signal_alarm(0)
        reap_children()
        for fn in self.test_files:
            try:
                os.remove(fn)
            except os.error:
                pass

        self.test_files[:] = []

    def pickaddr(self, proto):
        if proto == socket.AF_INET:
            return (HOST, 0)
        else:
            dir = None
            if os.name == 'os2':
                dir = '\\socket'
            fn = tempfile.mktemp(prefix='unix_socket.', dir=dir)
            if os.name == 'os2':
                if fn[1] == ':':
                    fn = fn[2:]
                if fn[0] in (os.sep, os.altsep):
                    fn = fn[1:]
                if os.sep == '/':
                    fn = fn.replace(os.sep, os.altsep)
                else:
                    fn = fn.replace(os.altsep, os.sep)
            self.test_files.append(fn)
            return fn
            return

    def make_server(self, addr, svrcls, hdlrbase):

        class MyServer(svrcls):

            def handle_error(self, request, client_address):
                self.close_request(request)
                self.server_close()
                raise

        class MyHandler(hdlrbase):

            def handle(self):
                line = self.rfile.readline()
                self.wfile.write(line)

        if verbose:
            print 'creating server'
        server = MyServer(addr, MyHandler)
        self.assertEqual(server.server_address, server.socket.getsockname())
        return server

    @reap_threads
    def run_server(self, svrcls, hdlrbase, testfunc):
        server = self.make_server(self.pickaddr(svrcls.address_family), svrcls, hdlrbase)
        addr = server.server_address
        if verbose:
            print 'server created'
            print 'ADDR =', addr
            print 'CLASS =', svrcls
        t = threading.Thread(name='%s serving' % svrcls, target=server.serve_forever, kwargs={'poll_interval': 0.01})
        t.daemon = True
        t.start()
        if verbose:
            print 'server running'
        for i in range(3):
            if verbose:
                print 'test client', i
            testfunc(svrcls.address_family, addr)

        if verbose:
            print 'waiting for server'
        server.shutdown()
        t.join()
        if verbose:
            print 'done'

    def stream_examine(self, proto, addr):
        s = socket.socket(proto, socket.SOCK_STREAM)
        s.connect(addr)
        s.sendall(TEST_STR)
        buf = data = receive(s, 100)
        while data and '\n' not in buf:
            data = receive(s, 100)
            buf += data

        self.assertEqual(buf, TEST_STR)
        s.close()

    def dgram_examine(self, proto, addr):
        s = socket.socket(proto, socket.SOCK_DGRAM)
        s.sendto(TEST_STR, addr)
        buf = data = receive(s, 100)
        while data and '\n' not in buf:
            data = receive(s, 100)
            buf += data

        self.assertEqual(buf, TEST_STR)
        s.close()

    def test_TCPServer(self):
        self.run_server(SocketServer.TCPServer, SocketServer.StreamRequestHandler, self.stream_examine)

    def test_ThreadingTCPServer(self):
        self.run_server(SocketServer.ThreadingTCPServer, SocketServer.StreamRequestHandler, self.stream_examine)

    if HAVE_FORKING:

        def test_ForkingTCPServer(self):
            with simple_subprocess(self):
                self.run_server(SocketServer.ForkingTCPServer, SocketServer.StreamRequestHandler, self.stream_examine)

    if HAVE_UNIX_SOCKETS:

        def test_UnixStreamServer(self):
            self.run_server(SocketServer.UnixStreamServer, SocketServer.StreamRequestHandler, self.stream_examine)

        def test_ThreadingUnixStreamServer(self):
            self.run_server(SocketServer.ThreadingUnixStreamServer, SocketServer.StreamRequestHandler, self.stream_examine)

        if HAVE_FORKING:

            def test_ForkingUnixStreamServer(self):
                with simple_subprocess(self):
                    self.run_server(ForkingUnixStreamServer, SocketServer.StreamRequestHandler, self.stream_examine)

    def test_UDPServer(self):
        self.run_server(SocketServer.UDPServer, SocketServer.DatagramRequestHandler, self.dgram_examine)

    def test_ThreadingUDPServer(self):
        self.run_server(SocketServer.ThreadingUDPServer, SocketServer.DatagramRequestHandler, self.dgram_examine)

    if HAVE_FORKING:

        def test_ForkingUDPServer(self):
            with simple_subprocess(self):
                self.run_server(SocketServer.ForkingUDPServer, SocketServer.DatagramRequestHandler, self.dgram_examine)

    @reap_threads
    def test_shutdown(self):

        class MyServer(SocketServer.TCPServer):
            pass

        class MyHandler(SocketServer.StreamRequestHandler):
            pass

        threads = []
        for i in range(20):
            s = MyServer((HOST, 0), MyHandler)
            t = threading.Thread(name='MyServer serving', target=s.serve_forever, kwargs={'poll_interval': 0.01})
            t.daemon = True
            threads.append((t, s))

        for t, s in threads:
            t.start()
            s.shutdown()

        for t, s in threads:
            t.join()


def test_main():
    if imp.lock_held():
        raise unittest.SkipTest("can't run when import lock is held")
    test.test_support.run_unittest(SocketServerTest)


if __name__ == '__main__':
    test_main()