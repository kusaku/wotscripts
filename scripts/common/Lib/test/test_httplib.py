# Embedded file name: scripts/common/Lib/test/test_httplib.py
import httplib
import array
import httplib
import StringIO
import socket
import errno
import unittest
TestCase = unittest.TestCase
from test import test_support
HOST = test_support.HOST

class FakeSocket:

    def __init__(self, text, fileclass = StringIO.StringIO):
        self.text = text
        self.fileclass = fileclass
        self.data = ''

    def sendall(self, data):
        self.data += ''.join(data)

    def makefile(self, mode, bufsize = None):
        if mode != 'r' and mode != 'rb':
            raise httplib.UnimplementedFileMode()
        return self.fileclass(self.text)


class EPipeSocket(FakeSocket):

    def __init__(self, text, pipe_trigger):
        FakeSocket.__init__(self, text)
        self.pipe_trigger = pipe_trigger

    def sendall(self, data):
        if self.pipe_trigger in data:
            raise socket.error(errno.EPIPE, 'gotcha')
        self.data += data

    def close(self):
        pass


class NoEOFStringIO(StringIO.StringIO):
    """Like StringIO, but raises AssertionError on EOF.
    
    This is used below to test that httplib doesn't try to read
    more from the underlying file than it should.
    """

    def read(self, n = -1):
        data = StringIO.StringIO.read(self, n)
        if data == '':
            raise AssertionError('caller tried to read past EOF')
        return data

    def readline(self, length = None):
        data = StringIO.StringIO.readline(self, length)
        if data == '':
            raise AssertionError('caller tried to read past EOF')
        return data


class HeaderTests(TestCase):

    def test_auto_headers(self):

        class HeaderCountingBuffer(list):

            def __init__(self):
                self.count = {}

            def append(self, item):
                kv = item.split(':')
                if len(kv) > 1:
                    lcKey = kv[0].lower()
                    self.count.setdefault(lcKey, 0)
                    self.count[lcKey] += 1
                list.append(self, item)

        for explicit_header in (True, False):
            for header in ('Content-length', 'Host', 'Accept-encoding'):
                conn = httplib.HTTPConnection('example.com')
                conn.sock = FakeSocket('blahblahblah')
                conn._buffer = HeaderCountingBuffer()
                body = 'spamspamspam'
                headers = {}
                if explicit_header:
                    headers[header] = str(len(body))
                conn.request('POST', '/', body, headers)
                self.assertEqual(conn._buffer.count[header.lower()], 1)

    def test_putheader(self):
        conn = httplib.HTTPConnection('example.com')
        conn.sock = FakeSocket(None)
        conn.putrequest('GET', '/')
        conn.putheader('Content-length', 42)
        self.assertTrue('Content-length: 42' in conn._buffer)
        return

    def test_ipv6host_header(self):
        expected = 'GET /foo HTTP/1.1\r\nHost: [2001::]:81\r\nAccept-Encoding: identity\r\n\r\n'
        conn = httplib.HTTPConnection('[2001::]:81')
        sock = FakeSocket('')
        conn.sock = sock
        conn.request('GET', '/foo')
        self.assertTrue(sock.data.startswith(expected))
        expected = 'GET /foo HTTP/1.1\r\nHost: [2001:102A::]\r\nAccept-Encoding: identity\r\n\r\n'
        conn = httplib.HTTPConnection('[2001:102A::]')
        sock = FakeSocket('')
        conn.sock = sock
        conn.request('GET', '/foo')
        self.assertTrue(sock.data.startswith(expected))


class BasicTest(TestCase):

    def test_status_lines(self):
        body = 'HTTP/1.1 200 Ok\r\n\r\nText'
        sock = FakeSocket(body)
        resp = httplib.HTTPResponse(sock)
        resp.begin()
        self.assertEqual(resp.read(), 'Text')
        self.assertTrue(resp.isclosed())
        body = 'HTTP/1.1 400.100 Not Ok\r\n\r\nText'
        sock = FakeSocket(body)
        resp = httplib.HTTPResponse(sock)
        self.assertRaises(httplib.BadStatusLine, resp.begin)

    def test_bad_status_repr(self):
        exc = httplib.BadStatusLine('')
        self.assertEqual(repr(exc), 'BadStatusLine("\'\'",)')

    def test_partial_reads(self):
        body = 'HTTP/1.1 200 Ok\r\nContent-Length: 4\r\n\r\nText'
        sock = FakeSocket(body)
        resp = httplib.HTTPResponse(sock)
        resp.begin()
        self.assertEqual(resp.read(2), 'Te')
        self.assertFalse(resp.isclosed())
        self.assertEqual(resp.read(2), 'xt')
        self.assertTrue(resp.isclosed())

    def test_host_port(self):
        for hp in ('www.python.org:abc', 'user:password@www.python.org'):
            self.assertRaises(httplib.InvalidURL, httplib.HTTP, hp)

        for hp, h, p in (('[fe80::207:e9ff:fe9b]:8000', 'fe80::207:e9ff:fe9b', 8000),
         ('www.python.org:80', 'www.python.org', 80),
         ('www.python.org', 'www.python.org', 80),
         ('www.python.org:', 'www.python.org', 80),
         ('[fe80::207:e9ff:fe9b]', 'fe80::207:e9ff:fe9b', 80)):
            http = httplib.HTTP(hp)
            c = http._conn
            if h != c.host:
                self.fail('Host incorrectly parsed: %s != %s' % (h, c.host))
            if p != c.port:
                self.fail('Port incorrectly parsed: %s != %s' % (p, c.host))

    def test_response_headers(self):
        text = 'HTTP/1.1 200 OK\r\nSet-Cookie: Customer="WILE_E_COYOTE"; Version="1"; Path="/acme"\r\nSet-Cookie: Part_Number="Rocket_Launcher_0001"; Version="1"; Path="/acme"\r\n\r\nNo body\r\n'
        hdr = 'Customer="WILE_E_COYOTE"; Version="1"; Path="/acme", Part_Number="Rocket_Launcher_0001"; Version="1"; Path="/acme"'
        s = FakeSocket(text)
        r = httplib.HTTPResponse(s)
        r.begin()
        cookies = r.getheader('Set-Cookie')
        if cookies != hdr:
            self.fail('multiple headers not combined properly')

    def test_read_head(self):
        sock = FakeSocket('HTTP/1.1 200 OK\r\nContent-Length: 14432\r\n\r\n', NoEOFStringIO)
        resp = httplib.HTTPResponse(sock, method='HEAD')
        resp.begin()
        if resp.read() != '':
            self.fail('Did not expect response from HEAD request')

    def test_send_file(self):
        expected = 'GET /foo HTTP/1.1\r\nHost: example.com\r\nAccept-Encoding: identity\r\nContent-Length:'
        body = open(__file__, 'rb')
        conn = httplib.HTTPConnection('example.com')
        sock = FakeSocket(body)
        conn.sock = sock
        conn.request('GET', '/foo', body)
        self.assertTrue(sock.data.startswith(expected))

    def test_send(self):
        expected = 'this is a test this is only a test'
        conn = httplib.HTTPConnection('example.com')
        sock = FakeSocket(None)
        conn.sock = sock
        conn.send(expected)
        self.assertEqual(expected, sock.data)
        sock.data = ''
        conn.send(array.array('c', expected))
        self.assertEqual(expected, sock.data)
        sock.data = ''
        conn.send(StringIO.StringIO(expected))
        self.assertEqual(expected, sock.data)
        return

    def test_chunked(self):
        chunked_start = 'HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\na\r\nhello worl\r\n1\r\nd\r\n'
        sock = FakeSocket(chunked_start + '0\r\n')
        resp = httplib.HTTPResponse(sock, method='GET')
        resp.begin()
        self.assertEqual(resp.read(), 'hello world')
        resp.close()
        for x in ('', 'foo\r\n'):
            sock = FakeSocket(chunked_start + x)
            resp = httplib.HTTPResponse(sock, method='GET')
            resp.begin()
            try:
                resp.read()
            except httplib.IncompleteRead as i:
                self.assertEqual(i.partial, 'hello world')
                self.assertEqual(repr(i), 'IncompleteRead(11 bytes read)')
                self.assertEqual(str(i), 'IncompleteRead(11 bytes read)')
            else:
                self.fail('IncompleteRead expected')
            finally:
                resp.close()

    def test_chunked_head(self):
        chunked_start = 'HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\na\r\nhello world\r\n1\r\nd\r\n'
        sock = FakeSocket(chunked_start + '0\r\n')
        resp = httplib.HTTPResponse(sock, method='HEAD')
        resp.begin()
        self.assertEqual(resp.read(), '')
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.reason, 'OK')
        self.assertTrue(resp.isclosed())

    def test_negative_content_length(self):
        sock = FakeSocket('HTTP/1.1 200 OK\r\nContent-Length: -1\r\n\r\nHello\r\n')
        resp = httplib.HTTPResponse(sock, method='GET')
        resp.begin()
        self.assertEqual(resp.read(), 'Hello\r\n')
        resp.close()

    def test_incomplete_read(self):
        sock = FakeSocket('HTTP/1.1 200 OK\r\nContent-Length: 10\r\n\r\nHello\r\n')
        resp = httplib.HTTPResponse(sock, method='GET')
        resp.begin()
        try:
            resp.read()
        except httplib.IncompleteRead as i:
            self.assertEqual(i.partial, 'Hello\r\n')
            self.assertEqual(repr(i), 'IncompleteRead(7 bytes read, 3 more expected)')
            self.assertEqual(str(i), 'IncompleteRead(7 bytes read, 3 more expected)')
        else:
            self.fail('IncompleteRead expected')
        finally:
            resp.close()

    def test_epipe(self):
        sock = EPipeSocket('HTTP/1.0 401 Authorization Required\r\nContent-type: text/html\r\nWWW-Authenticate: Basic realm="example"\r\n', 'Content-Length')
        conn = httplib.HTTPConnection('example.com')
        conn.sock = sock
        self.assertRaises(socket.error, lambda : conn.request('PUT', '/url', 'body'))
        resp = conn.getresponse()
        self.assertEqual(401, resp.status)
        self.assertEqual('Basic realm="example"', resp.getheader('www-authenticate'))

    def test_filenoattr(self):
        body = 'HTTP/1.1 200 Ok\r\n\r\nText'
        sock = FakeSocket(body)
        resp = httplib.HTTPResponse(sock)
        self.assertTrue(hasattr(resp, 'fileno'), 'HTTPResponse should expose a fileno attribute')

    def test_overflowing_status_line(self):
        self.skipTest('disabled for HTTP 0.9 support')
        body = 'HTTP/1.1 200 Ok' + 'k' * 65536 + '\r\n'
        resp = httplib.HTTPResponse(FakeSocket(body))
        self.assertRaises((httplib.LineTooLong, httplib.BadStatusLine), resp.begin)

    def test_overflowing_header_line(self):
        body = 'HTTP/1.1 200 OK\r\nX-Foo: bar' + 'r' * 65536 + '\r\n\r\n'
        resp = httplib.HTTPResponse(FakeSocket(body))
        self.assertRaises(httplib.LineTooLong, resp.begin)

    def test_overflowing_chunked_line(self):
        body = 'HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n' + '0' * 65536 + 'a\r\nhello world\r\n0\r\n'
        resp = httplib.HTTPResponse(FakeSocket(body))
        resp.begin()
        self.assertRaises(httplib.LineTooLong, resp.read)


class OfflineTest(TestCase):

    def test_responses(self):
        self.assertEqual(httplib.responses[httplib.NOT_FOUND], 'Not Found')


class SourceAddressTest(TestCase):

    def setUp(self):
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = test_support.bind_port(self.serv)
        self.source_port = test_support.find_unused_port()
        self.serv.listen(5)
        self.conn = None
        return

    def tearDown(self):
        if self.conn:
            self.conn.close()
            self.conn = None
        self.serv.close()
        self.serv = None
        return

    def testHTTPConnectionSourceAddress(self):
        self.conn = httplib.HTTPConnection(HOST, self.port, source_address=('', self.source_port))
        self.conn.connect()
        self.assertEqual(self.conn.sock.getsockname()[1], self.source_port)

    @unittest.skipIf(not hasattr(httplib, 'HTTPSConnection'), 'httplib.HTTPSConnection not defined')
    def testHTTPSConnectionSourceAddress(self):
        self.conn = httplib.HTTPSConnection(HOST, self.port, source_address=('', self.source_port))


class TimeoutTest(TestCase):
    PORT = None

    def setUp(self):
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TimeoutTest.PORT = test_support.bind_port(self.serv)
        self.serv.listen(5)

    def tearDown(self):
        self.serv.close()
        self.serv = None
        return

    def testTimeoutAttribute(self):
        """This will prove that the timeout gets through
        HTTPConnection and into the socket.
        """
        self.assertTrue(socket.getdefaulttimeout() is None)
        socket.setdefaulttimeout(30)
        try:
            httpConn = httplib.HTTPConnection(HOST, TimeoutTest.PORT)
            httpConn.connect()
        finally:
            socket.setdefaulttimeout(None)

        self.assertEqual(httpConn.sock.gettimeout(), 30)
        httpConn.close()
        self.assertTrue(socket.getdefaulttimeout() is None)
        socket.setdefaulttimeout(30)
        try:
            httpConn = httplib.HTTPConnection(HOST, TimeoutTest.PORT, timeout=None)
            httpConn.connect()
        finally:
            socket.setdefaulttimeout(None)

        self.assertEqual(httpConn.sock.gettimeout(), None)
        httpConn.close()
        httpConn = httplib.HTTPConnection(HOST, TimeoutTest.PORT, timeout=30)
        httpConn.connect()
        self.assertEqual(httpConn.sock.gettimeout(), 30)
        httpConn.close()
        return


class HTTPSTimeoutTest(TestCase):

    def test_attributes(self):
        if hasattr(httplib, 'HTTPSConnection'):
            h = httplib.HTTPSConnection(HOST, TimeoutTest.PORT, timeout=30)
            self.assertEqual(h.timeout, 30)

    @unittest.skipIf(not hasattr(httplib, 'HTTPS'), 'httplib.HTTPS not available')
    def test_host_port(self):
        for hp in ('www.python.org:abc', 'user:password@www.python.org'):
            self.assertRaises(httplib.InvalidURL, httplib.HTTP, hp)

        for hp, h, p in (('[fe80::207:e9ff:fe9b]:8000', 'fe80::207:e9ff:fe9b', 8000),
         ('pypi.python.org:443', 'pypi.python.org', 443),
         ('pypi.python.org', 'pypi.python.org', 443),
         ('pypi.python.org:', 'pypi.python.org', 443),
         ('[fe80::207:e9ff:fe9b]', 'fe80::207:e9ff:fe9b', 443)):
            http = httplib.HTTPS(hp)
            c = http._conn
            if h != c.host:
                self.fail('Host incorrectly parsed: %s != %s' % (h, c.host))
            if p != c.port:
                self.fail('Port incorrectly parsed: %s != %s' % (p, c.host))


def test_main(verbose = None):
    test_support.run_unittest(HeaderTests, OfflineTest, BasicTest, TimeoutTest, HTTPSTimeoutTest, SourceAddressTest)


if __name__ == '__main__':
    test_main()