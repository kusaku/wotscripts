# Embedded file name: scripts/common/Lib/test/test_epoll.py
"""
Tests for epoll wrapper.
"""
import socket
import errno
import time
import select
import unittest
from test import test_support
if not hasattr(select, 'epoll'):
    raise unittest.SkipTest('test works only on Linux 2.6')
try:
    select.epoll()
except IOError as e:
    if e.errno == errno.ENOSYS:
        raise unittest.SkipTest("kernel doesn't support epoll()")
    raise

class TestEPoll(unittest.TestCase):

    def setUp(self):
        self.serverSocket = socket.socket()
        self.serverSocket.bind(('127.0.0.1', 0))
        self.serverSocket.listen(1)
        self.connections = [self.serverSocket]

    def tearDown(self):
        for skt in self.connections:
            skt.close()

    def _connected_pair(self):
        client = socket.socket()
        client.setblocking(False)
        try:
            client.connect(('127.0.0.1', self.serverSocket.getsockname()[1]))
        except socket.error as e:
            self.assertEqual(e.args[0], errno.EINPROGRESS)
        else:
            raise AssertionError('Connect should have raised EINPROGRESS')

        server, addr = self.serverSocket.accept()
        self.connections.extend((client, server))
        return (client, server)

    def test_create(self):
        try:
            ep = select.epoll(16)
        except OSError as e:
            raise AssertionError(str(e))

        self.assertTrue(ep.fileno() > 0, ep.fileno())
        self.assertTrue(not ep.closed)
        ep.close()
        self.assertTrue(ep.closed)
        self.assertRaises(ValueError, ep.fileno)

    def test_badcreate(self):
        self.assertRaises(TypeError, select.epoll, 1, 2, 3)
        self.assertRaises(TypeError, select.epoll, 'foo')
        self.assertRaises(TypeError, select.epoll, None)
        self.assertRaises(TypeError, select.epoll, ())
        self.assertRaises(TypeError, select.epoll, ['foo'])
        self.assertRaises(TypeError, select.epoll, {})
        return

    def test_add(self):
        server, client = self._connected_pair()
        ep = select.epoll(2)
        try:
            ep.register(server.fileno(), select.EPOLLIN | select.EPOLLOUT)
            ep.register(client.fileno(), select.EPOLLIN | select.EPOLLOUT)
        finally:
            ep.close()

        ep = select.epoll(2)
        try:
            ep.register(server, select.EPOLLIN | select.EPOLLOUT)
            ep.register(client, select.EPOLLIN | select.EPOLLOUT)
        finally:
            ep.close()

        ep = select.epoll(2)
        try:
            self.assertRaises(TypeError, ep.register, object(), select.EPOLLIN | select.EPOLLOUT)
            self.assertRaises(TypeError, ep.register, None, select.EPOLLIN | select.EPOLLOUT)
            self.assertRaises(ValueError, ep.register, -1, select.EPOLLIN | select.EPOLLOUT)
            self.assertRaises(IOError, ep.register, 10000, select.EPOLLIN | select.EPOLLOUT)
            ep.register(server, select.EPOLLIN | select.EPOLLOUT)
            self.assertRaises(IOError, ep.register, server, select.EPOLLIN | select.EPOLLOUT)
        finally:
            ep.close()

        return

    def test_fromfd(self):
        server, client = self._connected_pair()
        ep = select.epoll(2)
        ep2 = select.epoll.fromfd(ep.fileno())
        ep2.register(server.fileno(), select.EPOLLIN | select.EPOLLOUT)
        ep2.register(client.fileno(), select.EPOLLIN | select.EPOLLOUT)
        events = ep.poll(1, 4)
        events2 = ep2.poll(0.9, 4)
        self.assertEqual(len(events), 2)
        self.assertEqual(len(events2), 2)
        ep.close()
        try:
            ep2.poll(1, 4)
        except IOError as e:
            self.assertEqual(e.args[0], errno.EBADF, e)
        else:
            self.fail("epoll on closed fd didn't raise EBADF")

    def test_control_and_wait(self):
        client, server = self._connected_pair()
        ep = select.epoll(16)
        ep.register(server.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLET)
        ep.register(client.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLET)
        now = time.time()
        events = ep.poll(1, 4)
        then = time.time()
        self.assertFalse(then - now > 0.1, then - now)
        events.sort()
        expected = [(client.fileno(), select.EPOLLOUT), (server.fileno(), select.EPOLLOUT)]
        expected.sort()
        self.assertEqual(events, expected)
        self.assertFalse(then - now > 0.01, then - now)
        now = time.time()
        events = ep.poll(timeout=2.1, maxevents=4)
        then = time.time()
        self.assertFalse(events)
        client.send('Hello!')
        server.send('world!!!')
        now = time.time()
        events = ep.poll(1, 4)
        then = time.time()
        self.assertFalse(then - now > 0.01)
        events.sort()
        expected = [(client.fileno(), select.EPOLLIN | select.EPOLLOUT), (server.fileno(), select.EPOLLIN | select.EPOLLOUT)]
        expected.sort()
        self.assertEqual(events, expected)
        ep.unregister(client.fileno())
        ep.modify(server.fileno(), select.EPOLLOUT)
        now = time.time()
        events = ep.poll(1, 4)
        then = time.time()
        self.assertFalse(then - now > 0.01)
        expected = [(server.fileno(), select.EPOLLOUT)]
        self.assertEqual(events, expected)

    def test_errors(self):
        self.assertRaises(ValueError, select.epoll, -2)
        self.assertRaises(ValueError, select.epoll().register, -1, select.EPOLLIN)

    def test_unregister_closed(self):
        server, client = self._connected_pair()
        fd = server.fileno()
        ep = select.epoll(16)
        ep.register(server)
        now = time.time()
        events = ep.poll(1, 4)
        then = time.time()
        self.assertFalse(then - now > 0.01)
        server.close()
        ep.unregister(fd)


def test_main():
    test_support.run_unittest(TestEPoll)


if __name__ == '__main__':
    test_main()