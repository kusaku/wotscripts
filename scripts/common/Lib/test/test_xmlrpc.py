# Embedded file name: scripts/common/Lib/test/test_xmlrpc.py
import base64
import datetime
import sys
import time
import unittest
import xmlrpclib
import SimpleXMLRPCServer
import mimetools
import httplib
import socket
import StringIO
import os
import re
from test import test_support
try:
    import threading
except ImportError:
    threading = None

try:
    unicode
except NameError:
    have_unicode = False
else:
    have_unicode = True

alist = [{'astring': 'foo@bar.baz.spam',
  'afloat': 7283.43,
  'anint': 1048576,
  'ashortlong': 2L,
  'anotherlist': ['.zyx.41'],
  'abase64': xmlrpclib.Binary('my dog has fleas'),
  'boolean': xmlrpclib.False,
  'unicode': u'\u4000\u6000\u8000',
  u'ukey\u4000': 'regular value',
  'datetime1': xmlrpclib.DateTime('20050210T11:41:23'),
  'datetime2': xmlrpclib.DateTime((2005, 2, 10, 11, 41, 23, 0, 1, -1)),
  'datetime3': xmlrpclib.DateTime(datetime.datetime(2005, 2, 10, 11, 41, 23))}]

class XMLRPCTestCase(unittest.TestCase):

    def test_dump_load(self):
        self.assertEqual(alist, xmlrpclib.loads(xmlrpclib.dumps((alist,)))[0][0])

    def test_dump_bare_datetime(self):
        dt = datetime.datetime(2005, 2, 10, 11, 41, 23)
        s = xmlrpclib.dumps((dt,))
        (newdt,), m = xmlrpclib.loads(s, use_datetime=1)
        self.assertEqual(newdt, dt)
        self.assertEqual(m, None)
        (newdt,), m = xmlrpclib.loads(s, use_datetime=0)
        self.assertEqual(newdt, xmlrpclib.DateTime('20050210T11:41:23'))
        return

    def test_datetime_before_1900(self):
        dt = datetime.datetime(1, 2, 10, 11, 41, 23)
        s = xmlrpclib.dumps((dt,))
        (newdt,), m = xmlrpclib.loads(s, use_datetime=1)
        self.assertEqual(newdt, dt)
        self.assertEqual(m, None)
        (newdt,), m = xmlrpclib.loads(s, use_datetime=0)
        self.assertEqual(newdt, xmlrpclib.DateTime('00010210T11:41:23'))
        return

    def test_cmp_datetime_DateTime(self):
        now = datetime.datetime.now()
        dt = xmlrpclib.DateTime(now.timetuple())
        self.assertTrue(dt == now)
        self.assertTrue(now == dt)
        then = now + datetime.timedelta(seconds=4)
        self.assertTrue(then >= dt)
        self.assertTrue(dt < then)

    def test_bug_1164912(self):
        d = xmlrpclib.DateTime()
        (new_d,), dummy = xmlrpclib.loads(xmlrpclib.dumps((d,), methodresponse=True))
        self.assertIsInstance(new_d.value, str)
        s = xmlrpclib.dumps((new_d,), methodresponse=True)
        self.assertIsInstance(s, str)

    def test_newstyle_class(self):

        class T(object):
            pass

        t = T()
        t.x = 100
        t.y = 'Hello'
        (t2,), dummy = xmlrpclib.loads(xmlrpclib.dumps((t,)))
        self.assertEqual(t2, t.__dict__)

    def test_dump_big_long(self):
        self.assertRaises(OverflowError, xmlrpclib.dumps, (633825300114114700748351602688L,))

    def test_dump_bad_dict(self):
        self.assertRaises(TypeError, xmlrpclib.dumps, ({(1, 2, 3): 1},))

    def test_dump_recursive_seq(self):
        l = [1, 2, 3]
        t = [3,
         4,
         5,
         l]
        l.append(t)
        self.assertRaises(TypeError, xmlrpclib.dumps, (l,))

    def test_dump_recursive_dict(self):
        d = {'1': 1,
         '2': 1}
        t = {'3': 3,
         'd': d}
        d['t'] = t
        self.assertRaises(TypeError, xmlrpclib.dumps, (d,))

    def test_dump_big_int(self):
        if sys.maxint > 2147483647L:
            self.assertRaises(OverflowError, xmlrpclib.dumps, (int(17179869184L),))
        xmlrpclib.dumps((xmlrpclib.MAXINT, xmlrpclib.MININT))
        self.assertRaises(OverflowError, xmlrpclib.dumps, (xmlrpclib.MAXINT + 1,))
        self.assertRaises(OverflowError, xmlrpclib.dumps, (xmlrpclib.MININT - 1,))

        def dummy_write(s):
            pass

        m = xmlrpclib.Marshaller()
        m.dump_int(xmlrpclib.MAXINT, dummy_write)
        m.dump_int(xmlrpclib.MININT, dummy_write)
        self.assertRaises(OverflowError, m.dump_int, xmlrpclib.MAXINT + 1, dummy_write)
        self.assertRaises(OverflowError, m.dump_int, xmlrpclib.MININT - 1, dummy_write)

    def test_dump_none(self):
        value = alist + [None]
        arg1 = (alist + [None],)
        strg = xmlrpclib.dumps(arg1, allow_none=True)
        self.assertEqual(value, xmlrpclib.loads(strg)[0][0])
        self.assertRaises(TypeError, xmlrpclib.dumps, (arg1,))
        return

    def test_default_encoding_issues(self):
        utf8 = "<?xml version='1.0' encoding='iso-8859-1'?>\n                  <params>\n                    <param><value>\n                      <string>abc \x95</string>\n                      </value></param>\n                    <param><value>\n                      <struct>\n                        <member>\n                          <name>def \x96</name>\n                          <value><string>ghi \x97</string></value>\n                          </member>\n                        </struct>\n                      </value></param>\n                  </params>\n                  "
        old_encoding = sys.getdefaultencoding()
        with test_support.CleanImport('sys'):
            import sys as temp_sys
            temp_sys.setdefaultencoding('iso-8859-1')
            try:
                (s, d), m = xmlrpclib.loads(utf8)
            finally:
                temp_sys.setdefaultencoding(old_encoding)

        items = d.items()
        if have_unicode:
            self.assertEqual(s, u'abc \x95')
            self.assertIsInstance(s, unicode)
            self.assertEqual(items, [(u'def \x96', u'ghi \x97')])
            self.assertIsInstance(items[0][0], unicode)
            self.assertIsInstance(items[0][1], unicode)
        else:
            self.assertEqual(s, 'abc \xc2\x95')
            self.assertEqual(items, [('def \xc2\x96', 'ghi \xc2\x97')])


class HelperTestCase(unittest.TestCase):

    def test_escape(self):
        self.assertEqual(xmlrpclib.escape('a&b'), 'a&amp;b')
        self.assertEqual(xmlrpclib.escape('a<b'), 'a&lt;b')
        self.assertEqual(xmlrpclib.escape('a>b'), 'a&gt;b')


class FaultTestCase(unittest.TestCase):

    def test_repr(self):
        f = xmlrpclib.Fault(42, 'Test Fault')
        self.assertEqual(repr(f), "<Fault 42: 'Test Fault'>")
        self.assertEqual(repr(f), str(f))

    def test_dump_fault(self):
        f = xmlrpclib.Fault(42, 'Test Fault')
        s = xmlrpclib.dumps((f,))
        (newf,), m = xmlrpclib.loads(s)
        self.assertEqual(newf, {'faultCode': 42,
         'faultString': 'Test Fault'})
        self.assertEqual(m, None)
        s = xmlrpclib.Marshaller().dumps(f)
        self.assertRaises(xmlrpclib.Fault, xmlrpclib.loads, s)
        return


class DateTimeTestCase(unittest.TestCase):

    def test_default(self):
        t = xmlrpclib.DateTime()

    def test_time(self):
        d = 1181399930.036952
        t = xmlrpclib.DateTime(d)
        self.assertEqual(str(t), time.strftime('%Y%m%dT%H:%M:%S', time.localtime(d)))

    def test_time_tuple(self):
        d = (2007, 6, 9, 10, 38, 50, 5, 160, 0)
        t = xmlrpclib.DateTime(d)
        self.assertEqual(str(t), '20070609T10:38:50')

    def test_time_struct(self):
        d = time.localtime(1181399930.036952)
        t = xmlrpclib.DateTime(d)
        self.assertEqual(str(t), time.strftime('%Y%m%dT%H:%M:%S', d))

    def test_datetime_datetime(self):
        d = datetime.datetime(2007, 1, 2, 3, 4, 5)
        t = xmlrpclib.DateTime(d)
        self.assertEqual(str(t), '20070102T03:04:05')

    def test_repr(self):
        d = datetime.datetime(2007, 1, 2, 3, 4, 5)
        t = xmlrpclib.DateTime(d)
        val = "<DateTime '20070102T03:04:05' at %x>" % id(t)
        self.assertEqual(repr(t), val)

    def test_decode(self):
        d = ' 20070908T07:11:13  '
        t1 = xmlrpclib.DateTime()
        t1.decode(d)
        tref = xmlrpclib.DateTime(datetime.datetime(2007, 9, 8, 7, 11, 13))
        self.assertEqual(t1, tref)
        t2 = xmlrpclib._datetime(d)
        self.assertEqual(t1, tref)


class BinaryTestCase(unittest.TestCase):

    def test_default(self):
        t = xmlrpclib.Binary()
        self.assertEqual(str(t), '')

    def test_string(self):
        d = '\x01\x02\x03abc123\xff\xfe'
        t = xmlrpclib.Binary(d)
        self.assertEqual(str(t), d)

    def test_decode(self):
        d = '\x01\x02\x03abc123\xff\xfe'
        de = base64.encodestring(d)
        t1 = xmlrpclib.Binary()
        t1.decode(de)
        self.assertEqual(str(t1), d)
        t2 = xmlrpclib._binary(de)
        self.assertEqual(str(t2), d)


ADDR = PORT = URL = None

def http_server(evt, numrequests, requestHandler = None):
    global ADDR
    global URL
    global PORT

    class TestInstanceClass:

        def div(self, x, y):
            return x // y

        def _methodHelp(self, name):
            if name == 'div':
                return 'This is the div function'

    def my_function():
        """This is my function"""
        return True

    class MyXMLRPCServer(SimpleXMLRPCServer.SimpleXMLRPCServer):

        def get_request(self):
            s, port = self.socket.accept()
            s.setblocking(True)
            return (s, port)

    if not requestHandler:
        requestHandler = SimpleXMLRPCServer.SimpleXMLRPCRequestHandler
    serv = MyXMLRPCServer(('localhost', 0), requestHandler, logRequests=False, bind_and_activate=False)
    try:
        serv.socket.settimeout(3)
        serv.server_bind()
        ADDR, PORT = serv.socket.getsockname()
        URL = 'http://%s:%d' % (ADDR, PORT)
        serv.server_activate()
        serv.register_introspection_functions()
        serv.register_multicall_functions()
        serv.register_function(pow)
        serv.register_function(lambda x, y: x + y, 'add')
        serv.register_function(my_function)
        serv.register_instance(TestInstanceClass())
        evt.set()
        while numrequests > 0:
            serv.handle_request()
            numrequests -= 1

    except socket.timeout:
        pass
    finally:
        serv.socket.close()
        PORT = None
        evt.set()

    return


def http_multi_server(evt, numrequests, requestHandler = None):
    global URL
    global ADDR
    global PORT

    class TestInstanceClass:

        def div(self, x, y):
            return x // y

        def _methodHelp(self, name):
            if name == 'div':
                return 'This is the div function'

    def my_function():
        """This is my function"""
        return True

    class MyXMLRPCServer(SimpleXMLRPCServer.MultiPathXMLRPCServer):

        def get_request(self):
            s, port = self.socket.accept()
            s.setblocking(True)
            return (s, port)

    if not requestHandler:
        requestHandler = SimpleXMLRPCServer.SimpleXMLRPCRequestHandler

    class MyRequestHandler(requestHandler):
        rpc_paths = []

    serv = MyXMLRPCServer(('localhost', 0), MyRequestHandler, logRequests=False, bind_and_activate=False)
    serv.socket.settimeout(3)
    serv.server_bind()
    try:
        ADDR, PORT = serv.socket.getsockname()
        URL = 'http://%s:%d' % (ADDR, PORT)
        serv.server_activate()
        paths = ['/foo', '/foo/bar']
        for path in paths:
            d = serv.add_dispatcher(path, SimpleXMLRPCServer.SimpleXMLRPCDispatcher())
            d.register_introspection_functions()
            d.register_multicall_functions()

        serv.get_dispatcher(paths[0]).register_function(pow)
        serv.get_dispatcher(paths[1]).register_function(lambda x, y: x + y, 'add')
        evt.set()
        while numrequests > 0:
            serv.handle_request()
            numrequests -= 1

    except socket.timeout:
        pass
    finally:
        serv.socket.close()
        PORT = None
        evt.set()

    return


def is_unavailable_exception(e):
    """Returns True if the given ProtocolError is the product of a server-side
    exception caused by the 'temporarily unavailable' response sometimes
    given by operations on non-blocking sockets."""
    try:
        if e.errcode == -1 or e.headers is None:
            return True
        exc_mess = e.headers.get('X-exception')
    except AttributeError:
        exc_mess = str(e)

    if exc_mess and 'temporarily unavailable' in exc_mess.lower():
        return True
    else:
        return False


@unittest.skipUnless(threading, 'Threading required for this test.')

class BaseServerTestCase(unittest.TestCase):
    requestHandler = None
    request_count = 1
    threadFunc = staticmethod(http_server)

    def setUp(self):
        SimpleXMLRPCServer.SimpleXMLRPCServer._send_traceback_header = True
        self.evt = threading.Event()
        serv_args = (self.evt, self.request_count, self.requestHandler)
        threading.Thread(target=self.threadFunc, args=serv_args).start()
        self.evt.wait(10)
        self.evt.clear()

    def tearDown(self):
        self.evt.wait(10)
        SimpleXMLRPCServer.SimpleXMLRPCServer._send_traceback_header = False


class SimpleServerTestCase(BaseServerTestCase):

    def test_simple1(self):
        try:
            p = xmlrpclib.ServerProxy(URL)
            self.assertEqual(p.pow(6, 8), 1679616)
        except (xmlrpclib.ProtocolError, socket.error) as e:
            if not is_unavailable_exception(e):
                self.fail('%s\n%s' % (e, getattr(e, 'headers', '')))

    def test_nonascii(self):
        start_string = 'P\\N{LATIN SMALL LETTER Y WITH CIRCUMFLEX}t'
        end_string = 'h\\N{LATIN SMALL LETTER O WITH HORN}n'
        try:
            p = xmlrpclib.ServerProxy(URL)
            self.assertEqual(p.add(start_string, end_string), start_string + end_string)
        except (xmlrpclib.ProtocolError, socket.error) as e:
            if not is_unavailable_exception(e):
                self.fail('%s\n%s' % (e, getattr(e, 'headers', '')))

    def test_unicode_host(self):
        server = xmlrpclib.ServerProxy(u'http://%s:%d/RPC2' % (ADDR, PORT))
        self.assertEqual(server.add('a', u'\xe9'), u'a\xe9')

    def XXXtest_404(self):
        conn = httplib.HTTPConnection(ADDR, PORT)
        conn.request('POST', '/this-is-not-valid')
        response = conn.getresponse()
        conn.close()
        self.assertEqual(response.status, 404)
        self.assertEqual(response.reason, 'Not Found')

    def test_introspection1(self):
        try:
            p = xmlrpclib.ServerProxy(URL)
            meth = p.system.listMethods()
            expected_methods = set(['pow',
             'div',
             'my_function',
             'add',
             'system.listMethods',
             'system.methodHelp',
             'system.methodSignature',
             'system.multicall'])
            self.assertEqual(set(meth), expected_methods)
        except (xmlrpclib.ProtocolError, socket.error) as e:
            if not is_unavailable_exception(e):
                self.fail('%s\n%s' % (e, getattr(e, 'headers', '')))

    def test_introspection2(self):
        try:
            p = xmlrpclib.ServerProxy(URL)
            divhelp = p.system.methodHelp('div')
            self.assertEqual(divhelp, 'This is the div function')
        except (xmlrpclib.ProtocolError, socket.error) as e:
            if not is_unavailable_exception(e):
                self.fail('%s\n%s' % (e, getattr(e, 'headers', '')))

    @unittest.skipIf(sys.flags.optimize >= 2, 'Docstrings are omitted with -O2 and above')
    def test_introspection3(self):
        try:
            p = xmlrpclib.ServerProxy(URL)
            myfunction = p.system.methodHelp('my_function')
            self.assertEqual(myfunction, 'This is my function')
        except (xmlrpclib.ProtocolError, socket.error) as e:
            if not is_unavailable_exception(e):
                self.fail('%s\n%s' % (e, getattr(e, 'headers', '')))

    def test_introspection4(self):
        try:
            p = xmlrpclib.ServerProxy(URL)
            divsig = p.system.methodSignature('div')
            self.assertEqual(divsig, 'signatures not supported')
        except (xmlrpclib.ProtocolError, socket.error) as e:
            if not is_unavailable_exception(e):
                self.fail('%s\n%s' % (e, getattr(e, 'headers', '')))

    def test_multicall(self):
        try:
            p = xmlrpclib.ServerProxy(URL)
            multicall = xmlrpclib.MultiCall(p)
            multicall.add(2, 3)
            multicall.pow(6, 8)
            multicall.div(127, 42)
            add_result, pow_result, div_result = multicall()
            self.assertEqual(add_result, 5)
            self.assertEqual(pow_result, 1679616)
            self.assertEqual(div_result, 3)
        except (xmlrpclib.ProtocolError, socket.error) as e:
            if not is_unavailable_exception(e):
                self.fail('%s\n%s' % (e, getattr(e, 'headers', '')))

    def test_non_existing_multicall(self):
        try:
            p = xmlrpclib.ServerProxy(URL)
            multicall = xmlrpclib.MultiCall(p)
            multicall.this_is_not_exists()
            result = multicall()
            self.assertEqual(result.results[0]['faultCode'], 1)
            self.assertEqual(result.results[0]['faultString'], '<type \'exceptions.Exception\'>:method "this_is_not_exists" is not supported')
        except (xmlrpclib.ProtocolError, socket.error) as e:
            if not is_unavailable_exception(e):
                self.fail('%s\n%s' % (e, getattr(e, 'headers', '')))

    def test_dotted_attribute(self):
        self.assertRaises(AttributeError, SimpleXMLRPCServer.resolve_dotted_attribute, str, '__add')
        self.assertTrue(SimpleXMLRPCServer.resolve_dotted_attribute(str, 'title'))
        self.test_simple1()

    def test_partial_post(self):
        conn = httplib.HTTPConnection(ADDR, PORT)
        conn.request('POST', '/RPC2 HTTP/1.0\r\nContent-Length: 100\r\n\r\nbye')
        conn.close()


class MultiPathServerTestCase(BaseServerTestCase):
    threadFunc = staticmethod(http_multi_server)
    request_count = 2

    def test_path1(self):
        p = xmlrpclib.ServerProxy(URL + '/foo')
        self.assertEqual(p.pow(6, 8), 1679616)
        self.assertRaises(xmlrpclib.Fault, p.add, 6, 8)

    def test_path2(self):
        p = xmlrpclib.ServerProxy(URL + '/foo/bar')
        self.assertEqual(p.add(6, 8), 14)
        self.assertRaises(xmlrpclib.Fault, p.pow, 6, 8)


class BaseKeepaliveServerTestCase(BaseServerTestCase):

    class RequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
        parentClass = SimpleXMLRPCServer.SimpleXMLRPCRequestHandler
        protocol_version = 'HTTP/1.1'
        myRequests = []

        def handle(self):
            self.myRequests.append([])
            self.reqidx = len(self.myRequests) - 1
            return self.parentClass.handle(self)

        def handle_one_request(self):
            result = self.parentClass.handle_one_request(self)
            self.myRequests[self.reqidx].append(self.raw_requestline)
            return result

    requestHandler = RequestHandler

    def setUp(self):
        self.RequestHandler.myRequests = []
        return BaseServerTestCase.setUp(self)


class KeepaliveServerTestCase1(BaseKeepaliveServerTestCase):

    def test_two(self):
        p = xmlrpclib.ServerProxy(URL)
        self.assertEqual(p.pow(6, 8), 1679616)
        self.assertEqual(p.pow(6, 8), 1679616)
        self.assertEqual(p.pow(6, 8), 1679616)
        self.assertEqual(len(self.RequestHandler.myRequests), 1)
        self.assertGreaterEqual(len(self.RequestHandler.myRequests[-1]), 2)


class KeepaliveServerTestCase2(BaseKeepaliveServerTestCase):
    request_count = 2

    def test_close(self):
        p = xmlrpclib.ServerProxy(URL)
        self.assertEqual(p.pow(6, 8), 1679616)
        self.assertEqual(p.pow(6, 8), 1679616)
        self.assertEqual(p.pow(6, 8), 1679616)
        p('close')()
        self.assertEqual(p.pow(6, 8), 1679616)
        self.assertEqual(p.pow(6, 8), 1679616)
        self.assertEqual(p.pow(6, 8), 1679616)
        self.assertEqual(len(self.RequestHandler.myRequests), 2)
        self.assertGreaterEqual(len(self.RequestHandler.myRequests[-1]), 2)
        self.assertGreaterEqual(len(self.RequestHandler.myRequests[-2]), 2)

    def test_transport(self):
        p = xmlrpclib.ServerProxy(URL)
        self.assertEqual(p.pow(6, 8), 1679616)
        p('transport').close()
        self.assertEqual(p.pow(6, 8), 1679616)
        self.assertEqual(len(self.RequestHandler.myRequests), 2)


class GzipServerTestCase(BaseServerTestCase):

    class RequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
        parentClass = SimpleXMLRPCServer.SimpleXMLRPCRequestHandler
        protocol_version = 'HTTP/1.1'

        def do_POST(self):
            self.__class__.content_length = int(self.headers['content-length'])
            return self.parentClass.do_POST(self)

    requestHandler = RequestHandler

    class Transport(xmlrpclib.Transport):
        fake_gzip = False

        def parse_response(self, response):
            self.response_length = int(response.getheader('content-length', 0))
            return xmlrpclib.Transport.parse_response(self, response)

        def send_content(self, connection, body):
            if self.fake_gzip:
                connection.putheader('Content-Encoding', 'gzip')
            return xmlrpclib.Transport.send_content(self, connection, body)

    def setUp(self):
        BaseServerTestCase.setUp(self)

    def test_gzip_request(self):
        t = self.Transport()
        t.encode_threshold = None
        p = xmlrpclib.ServerProxy(URL, transport=t)
        self.assertEqual(p.pow(6, 8), 1679616)
        a = self.RequestHandler.content_length
        t.encode_threshold = 0
        self.assertEqual(p.pow(6, 8), 1679616)
        b = self.RequestHandler.content_length
        self.assertTrue(a > b)
        return

    def test_bad_gzip_request(self):
        t = self.Transport()
        t.encode_threshold = None
        t.fake_gzip = True
        p = xmlrpclib.ServerProxy(URL, transport=t)
        cm = self.assertRaisesRegexp(xmlrpclib.ProtocolError, re.compile('\\b400\\b'))
        with cm:
            p.pow(6, 8)
        return

    def test_gsip_response(self):
        t = self.Transport()
        p = xmlrpclib.ServerProxy(URL, transport=t)
        old = self.requestHandler.encode_threshold
        self.requestHandler.encode_threshold = None
        self.assertEqual(p.pow(6, 8), 1679616)
        a = t.response_length
        self.requestHandler.encode_threshold = 0
        self.assertEqual(p.pow(6, 8), 1679616)
        b = t.response_length
        self.requestHandler.encode_threshold = old
        self.assertTrue(a > b)
        return


class ServerProxyTestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        if threading:
            self.url = URL
        else:
            self.url = 'http://'

    def test_close(self):
        p = xmlrpclib.ServerProxy(self.url)
        self.assertEqual(p('close')(), None)
        return

    def test_transport(self):
        t = xmlrpclib.Transport()
        p = xmlrpclib.ServerProxy(self.url, transport=t)
        self.assertEqual(p('transport'), t)


class FailingMessageClass(mimetools.Message):

    def __getitem__(self, key):
        key = key.lower()
        if key == 'content-length':
            return 'I am broken'
        return mimetools.Message.__getitem__(self, key)


@unittest.skipUnless(threading, 'Threading required for this test.')

class FailingServerTestCase(unittest.TestCase):

    def setUp(self):
        self.evt = threading.Event()
        serv_args = (self.evt, 1)
        threading.Thread(target=http_server, args=serv_args).start()
        self.evt.wait()
        self.evt.clear()

    def tearDown(self):
        self.evt.wait()
        SimpleXMLRPCServer.SimpleXMLRPCServer._send_traceback_header = False
        SimpleXMLRPCServer.SimpleXMLRPCRequestHandler.MessageClass = mimetools.Message

    def test_basic(self):
        flagval = SimpleXMLRPCServer.SimpleXMLRPCServer._send_traceback_header
        self.assertEqual(flagval, False)
        SimpleXMLRPCServer.SimpleXMLRPCServer._send_traceback_header = True
        try:
            p = xmlrpclib.ServerProxy(URL)
            self.assertEqual(p.pow(6, 8), 1679616)
        except (xmlrpclib.ProtocolError, socket.error) as e:
            if not is_unavailable_exception(e):
                self.fail('%s\n%s' % (e, getattr(e, 'headers', '')))

    def test_fail_no_info(self):
        SimpleXMLRPCServer.SimpleXMLRPCRequestHandler.MessageClass = FailingMessageClass
        try:
            p = xmlrpclib.ServerProxy(URL)
            p.pow(6, 8)
        except (xmlrpclib.ProtocolError, socket.error) as e:
            if not is_unavailable_exception(e) and hasattr(e, 'headers'):
                self.assertTrue(e.headers.get('X-exception') is None)
                self.assertTrue(e.headers.get('X-traceback') is None)
        else:
            self.fail('ProtocolError not raised')

        return

    def test_fail_with_info(self):
        SimpleXMLRPCServer.SimpleXMLRPCRequestHandler.MessageClass = FailingMessageClass
        SimpleXMLRPCServer.SimpleXMLRPCServer._send_traceback_header = True
        try:
            p = xmlrpclib.ServerProxy(URL)
            p.pow(6, 8)
        except (xmlrpclib.ProtocolError, socket.error) as e:
            if not is_unavailable_exception(e) and hasattr(e, 'headers'):
                expected_err = "invalid literal for int() with base 10: 'I am broken'"
                self.assertEqual(e.headers.get('x-exception'), expected_err)
                self.assertTrue(e.headers.get('x-traceback') is not None)
        else:
            self.fail('ProtocolError not raised')

        return


class CGIHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.cgi = SimpleXMLRPCServer.CGIXMLRPCRequestHandler()

    def tearDown(self):
        self.cgi = None
        return

    def test_cgi_get(self):
        with test_support.EnvironmentVarGuard() as env:
            env['REQUEST_METHOD'] = 'GET'
            with test_support.captured_stdout() as data_out:
                self.cgi.handle_request()
            data_out.seek(0)
            handle = data_out.read()
            status = handle.split()[1]
            message = ' '.join(handle.split()[2:4])
            self.assertEqual(status, '400')
            self.assertEqual(message, 'Bad Request')

    def test_cgi_xmlrpc_response(self):
        data = "<?xml version='1.0'?>\n        <methodCall>\n            <methodName>test_method</methodName>\n            <params>\n                <param>\n                    <value><string>foo</string></value>\n                </param>\n                <param>\n                    <value><string>bar</string></value>\n                </param>\n            </params>\n        </methodCall>\n        "
        with test_support.EnvironmentVarGuard() as env:
            with test_support.captured_stdout() as data_out:
                with test_support.captured_stdin() as data_in:
                    data_in.write(data)
                    data_in.seek(0)
                    env['CONTENT_LENGTH'] = str(len(data))
                    self.cgi.handle_request()
        data_out.seek(0)
        handle = data_out.read()
        self.assertRaises(xmlrpclib.Fault, xmlrpclib.loads, handle[44:])
        content = handle[handle.find('<?xml'):]
        self.assertEqual(int(re.search('Content-Length: (\\d+)', handle).group(1)), len(content))


class FakeSocket:

    def __init__(self):
        self.data = StringIO.StringIO()

    def send(self, buf):
        self.data.write(buf)
        return len(buf)

    def sendall(self, buf):
        self.data.write(buf)

    def getvalue(self):
        return self.data.getvalue()

    def makefile(self, x = 'r', y = -1):
        raise RuntimeError

    def close(self):
        pass


class FakeTransport(xmlrpclib.Transport):
    """A Transport instance that records instead of sending a request.
    
    This class replaces the actual socket used by httplib with a
    FakeSocket object that records the request.  It doesn't provide a
    response.
    """

    def make_connection(self, host):
        conn = xmlrpclib.Transport.make_connection(self, host)
        conn.sock = self.fake_socket = FakeSocket()
        return conn


class TransportSubclassTestCase(unittest.TestCase):

    def issue_request(self, transport_class):
        """Return an HTTP request made via transport_class."""
        transport = transport_class()
        proxy = xmlrpclib.ServerProxy('http://example.com/', transport=transport)
        try:
            proxy.pow(6, 8)
        except RuntimeError:
            return transport.fake_socket.getvalue()

        return None

    def test_custom_user_agent(self):

        class TestTransport(FakeTransport):

            def send_user_agent(self, conn):
                xmlrpclib.Transport.send_user_agent(self, conn)
                conn.putheader('X-Test', 'test_custom_user_agent')

        req = self.issue_request(TestTransport)
        self.assertIn('X-Test: test_custom_user_agent\r\n', req)

    def test_send_host(self):

        class TestTransport(FakeTransport):

            def send_host(self, conn, host):
                xmlrpclib.Transport.send_host(self, conn, host)
                conn.putheader('X-Test', 'test_send_host')

        req = self.issue_request(TestTransport)
        self.assertIn('X-Test: test_send_host\r\n', req)

    def test_send_request(self):

        class TestTransport(FakeTransport):

            def send_request(self, conn, url, body):
                xmlrpclib.Transport.send_request(self, conn, url, body)
                conn.putheader('X-Test', 'test_send_request')

        req = self.issue_request(TestTransport)
        self.assertIn('X-Test: test_send_request\r\n', req)

    def test_send_content(self):

        class TestTransport(FakeTransport):

            def send_content(self, conn, body):
                conn.putheader('X-Test', 'test_send_content')
                xmlrpclib.Transport.send_content(self, conn, body)

        req = self.issue_request(TestTransport)
        self.assertIn('X-Test: test_send_content\r\n', req)


@test_support.reap_threads
def test_main():
    xmlrpc_tests = [XMLRPCTestCase,
     HelperTestCase,
     DateTimeTestCase,
     BinaryTestCase,
     FaultTestCase,
     TransportSubclassTestCase]
    xmlrpc_tests.append(SimpleServerTestCase)
    xmlrpc_tests.append(KeepaliveServerTestCase1)
    xmlrpc_tests.append(KeepaliveServerTestCase2)
    try:
        import gzip
        xmlrpc_tests.append(GzipServerTestCase)
    except ImportError:
        pass

    xmlrpc_tests.append(MultiPathServerTestCase)
    xmlrpc_tests.append(ServerProxyTestCase)
    xmlrpc_tests.append(FailingServerTestCase)
    xmlrpc_tests.append(CGIHandlerTestCase)
    test_support.run_unittest(*xmlrpc_tests)


if __name__ == '__main__':
    test_main()