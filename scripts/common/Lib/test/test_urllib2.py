# Embedded file name: scripts/common/Lib/test/test_urllib2.py
import unittest
from test import test_support
import os
import socket
import StringIO
import urllib2
from urllib2 import Request, OpenerDirector

class TrivialTests(unittest.TestCase):

    def test_trivial(self):
        self.assertRaises(ValueError, urllib2.urlopen, 'bogus url')
        fname = os.path.abspath(urllib2.__file__).replace('\\', '/')
        if os.name == 'riscos':
            import string
            fname = os.expand(fname)
            fname = fname.translate(string.maketrans('/.', './'))
        if os.name == 'nt':
            file_url = 'file:///%s' % fname
        else:
            file_url = 'file://%s' % fname
        f = urllib2.urlopen(file_url)
        buf = f.read()
        f.close()

    def test_parse_http_list(self):
        tests = [('a,b,c', ['a', 'b', 'c']),
         ('path"o,l"og"i"cal, example', ['path"o,l"og"i"cal', 'example']),
         ('a, b, "c", "d", "e,f", g, h', ['a',
           'b',
           '"c"',
           '"d"',
           '"e,f"',
           'g',
           'h']),
         ('a="b\\"c", d="e\\,f", g="h\\\\i"', ['a="b"c"', 'd="e,f"', 'g="h\\i"'])]
        for string, list in tests:
            self.assertEqual(urllib2.parse_http_list(string), list)


def test_request_headers_dict():
    """
    The Request.headers dictionary is not a documented interface.  It should
    stay that way, because the complete set of headers are only accessible
    through the .get_header(), .has_header(), .header_items() interface.
    However, .headers pre-dates those methods, and so real code will be using
    the dictionary.
    
    The introduction in 2.4 of those methods was a mistake for the same reason:
    code that previously saw all (urllib2 user)-provided headers in .headers
    now sees only a subset (and the function interface is ugly and incomplete).
    A better change would have been to replace .headers dict with a dict
    subclass (or UserDict.DictMixin instance?)  that preserved the .headers
    interface and also provided access to the "unredirected" headers.  It's
    probably too late to fix that, though.
    
    
    Check .capitalize() case normalization:
    
    >>> url = "http://example.com"
    >>> Request(url, headers={"Spam-eggs": "blah"}).headers["Spam-eggs"]
    'blah'
    >>> Request(url, headers={"spam-EggS": "blah"}).headers["Spam-eggs"]
    'blah'
    
    Currently, Request(url, "Spam-eggs").headers["Spam-Eggs"] raises KeyError,
    but that could be changed in future.
    
    """
    pass


def test_request_headers_methods():
    """
    Note the case normalization of header names here, to .capitalize()-case.
    This should be preserved for backwards-compatibility.  (In the HTTP case,
    normalization to .title()-case is done by urllib2 before sending headers to
    httplib).
    
    >>> url = "http://example.com"
    >>> r = Request(url, headers={"Spam-eggs": "blah"})
    >>> r.has_header("Spam-eggs")
    True
    >>> r.header_items()
    [('Spam-eggs', 'blah')]
    >>> r.add_header("Foo-Bar", "baz")
    >>> items = r.header_items()
    >>> items.sort()
    >>> items
    [('Foo-bar', 'baz'), ('Spam-eggs', 'blah')]
    
    Note that e.g. r.has_header("spam-EggS") is currently False, and
    r.get_header("spam-EggS") returns None, but that could be changed in
    future.
    
    >>> r.has_header("Not-there")
    False
    >>> print r.get_header("Not-there")
    None
    >>> r.get_header("Not-there", "default")
    'default'
    
    """
    pass


def test_password_manager(self):
    """
        >>> mgr = urllib2.HTTPPasswordMgr()
        >>> add = mgr.add_password
        >>> add("Some Realm", "http://example.com/", "joe", "password")
        >>> add("Some Realm", "http://example.com/ni", "ni", "ni")
        >>> add("c", "http://example.com/foo", "foo", "ni")
        >>> add("c", "http://example.com/bar", "bar", "nini")
        >>> add("b", "http://example.com/", "first", "blah")
        >>> add("b", "http://example.com/", "second", "spam")
        >>> add("a", "http://example.com", "1", "a")
        >>> add("Some Realm", "http://c.example.com:3128", "3", "c")
        >>> add("Some Realm", "d.example.com", "4", "d")
        >>> add("Some Realm", "e.example.com:3128", "5", "e")
    
        >>> mgr.find_user_password("Some Realm", "example.com")
        ('joe', 'password')
        >>> mgr.find_user_password("Some Realm", "http://example.com")
        ('joe', 'password')
        >>> mgr.find_user_password("Some Realm", "http://example.com/")
        ('joe', 'password')
        >>> mgr.find_user_password("Some Realm", "http://example.com/spam")
        ('joe', 'password')
        >>> mgr.find_user_password("Some Realm", "http://example.com/spam/spam")
        ('joe', 'password')
        >>> mgr.find_user_password("c", "http://example.com/foo")
        ('foo', 'ni')
        >>> mgr.find_user_password("c", "http://example.com/bar")
        ('bar', 'nini')
    
        Actually, this is really undefined ATM
    ##     Currently, we use the highest-level path where more than one match:
    
    ##     >>> mgr.find_user_password("Some Realm", "http://example.com/ni")
    ##     ('joe', 'password')
    
        Use latest add_password() in case of conflict:
    
        >>> mgr.find_user_password("b", "http://example.com/")
        ('second', 'spam')
    
        No special relationship between a.example.com and example.com:
    
        >>> mgr.find_user_password("a", "http://example.com/")
        ('1', 'a')
        >>> mgr.find_user_password("a", "http://a.example.com/")
        (None, None)
    
        Ports:
    
        >>> mgr.find_user_password("Some Realm", "c.example.com")
        (None, None)
        >>> mgr.find_user_password("Some Realm", "c.example.com:3128")
        ('3', 'c')
        >>> mgr.find_user_password("Some Realm", "http://c.example.com:3128")
        ('3', 'c')
        >>> mgr.find_user_password("Some Realm", "d.example.com")
        ('4', 'd')
        >>> mgr.find_user_password("Some Realm", "e.example.com:3128")
        ('5', 'e')
    
        """
    pass


def test_password_manager_default_port(self):
    """
    >>> mgr = urllib2.HTTPPasswordMgr()
    >>> add = mgr.add_password
    
    The point to note here is that we can't guess the default port if there's
    no scheme.  This applies to both add_password and find_user_password.
    
    >>> add("f", "http://g.example.com:80", "10", "j")
    >>> add("g", "http://h.example.com", "11", "k")
    >>> add("h", "i.example.com:80", "12", "l")
    >>> add("i", "j.example.com", "13", "m")
    >>> mgr.find_user_password("f", "g.example.com:100")
    (None, None)
    >>> mgr.find_user_password("f", "g.example.com:80")
    ('10', 'j')
    >>> mgr.find_user_password("f", "g.example.com")
    (None, None)
    >>> mgr.find_user_password("f", "http://g.example.com:100")
    (None, None)
    >>> mgr.find_user_password("f", "http://g.example.com:80")
    ('10', 'j')
    >>> mgr.find_user_password("f", "http://g.example.com")
    ('10', 'j')
    >>> mgr.find_user_password("g", "h.example.com")
    ('11', 'k')
    >>> mgr.find_user_password("g", "h.example.com:80")
    ('11', 'k')
    >>> mgr.find_user_password("g", "http://h.example.com:80")
    ('11', 'k')
    >>> mgr.find_user_password("h", "i.example.com")
    (None, None)
    >>> mgr.find_user_password("h", "i.example.com:80")
    ('12', 'l')
    >>> mgr.find_user_password("h", "http://i.example.com:80")
    ('12', 'l')
    >>> mgr.find_user_password("i", "j.example.com")
    ('13', 'm')
    >>> mgr.find_user_password("i", "j.example.com:80")
    (None, None)
    >>> mgr.find_user_password("i", "http://j.example.com")
    ('13', 'm')
    >>> mgr.find_user_password("i", "http://j.example.com:80")
    (None, None)
    
    """
    pass


class MockOpener():
    addheaders = []

    def open(self, req, data = None, timeout = socket._GLOBAL_DEFAULT_TIMEOUT):
        self.req, self.data, self.timeout = req, data, timeout

    def error(self, proto, *args):
        self.proto, self.args = proto, args


class MockFile():

    def read(self, count = None):
        pass

    def readline(self, count = None):
        pass

    def close(self):
        pass


class MockHeaders(dict):

    def getheaders(self, name):
        return self.values()


class MockResponse(StringIO.StringIO):

    def __init__(self, code, msg, headers, data, url = None):
        StringIO.StringIO.__init__(self, data)
        self.code, self.msg, self.headers, self.url = (code,
         msg,
         headers,
         url)

    def info(self):
        return self.headers

    def geturl(self):
        return self.url


class MockCookieJar():

    def add_cookie_header(self, request):
        self.ach_req = request

    def extract_cookies(self, response, request):
        self.ec_req, self.ec_r = request, response


class FakeMethod():

    def __init__(self, meth_name, action, handle):
        self.meth_name = meth_name
        self.handle = handle
        self.action = action

    def __call__(self, *args):
        return self.handle(self.meth_name, self.action, *args)


class MockHTTPResponse():

    def __init__(self, fp, msg, status, reason):
        self.fp = fp
        self.msg = msg
        self.status = status
        self.reason = reason

    def read(self):
        return ''


class MockHTTPClass():

    def __init__(self):
        self.req_headers = []
        self.data = None
        self.raise_on_endheaders = False
        self._tunnel_headers = {}
        return

    def __call__(self, host, timeout = socket._GLOBAL_DEFAULT_TIMEOUT):
        self.host = host
        self.timeout = timeout
        return self

    def set_debuglevel(self, level):
        self.level = level

    def set_tunnel(self, host, port = None, headers = None):
        self._tunnel_host = host
        self._tunnel_port = port
        if headers:
            self._tunnel_headers = headers
        else:
            self._tunnel_headers.clear()

    def request(self, method, url, body = None, headers = None):
        self.method = method
        self.selector = url
        if headers is not None:
            self.req_headers += headers.items()
        self.req_headers.sort()
        if body:
            self.data = body
        if self.raise_on_endheaders:
            import socket
            raise socket.error()
        return

    def getresponse(self):
        return MockHTTPResponse(MockFile(), {}, 200, 'OK')

    def close(self):
        pass


class MockHandler():
    handler_order = 500

    def __init__(self, methods):
        self._define_methods(methods)

    def _define_methods(self, methods):
        for spec in methods:
            if len(spec) == 2:
                name, action = spec
            else:
                name, action = spec, None
            meth = FakeMethod(name, action, self.handle)
            setattr(self.__class__, name, meth)

        return

    def handle(self, fn_name, action, *args, **kwds):
        self.parent.calls.append((self,
         fn_name,
         args,
         kwds))
        if action is None:
            return
        elif action == 'return self':
            return self
        elif action == 'return response':
            res = MockResponse(200, 'OK', {}, '')
            return res
        elif action == 'return request':
            return Request('http://blah/')
        elif action.startswith('error'):
            code = action[action.rfind(' ') + 1:]
            try:
                code = int(code)
            except ValueError:
                pass

            res = MockResponse(200, 'OK', {}, '')
            return self.parent.error('http', args[0], res, code, '', {})
        else:
            if action == 'raise':
                raise urllib2.URLError('blah')
            raise False or AssertionError
            return

    def close(self):
        pass

    def add_parent(self, parent):
        self.parent = parent
        self.parent.calls = []

    def __lt__(self, other):
        if not hasattr(other, 'handler_order'):
            return True
        return self.handler_order < other.handler_order


def add_ordered_mock_handlers(opener, meth_spec):
    """Create MockHandlers and add them to an OpenerDirector.
    
    meth_spec: list of lists of tuples and strings defining methods to define
    on handlers.  eg:
    
    [["http_error", "ftp_open"], ["http_open"]]
    
    defines methods .http_error() and .ftp_open() on one handler, and
    .http_open() on another.  These methods just record their arguments and
    return None.  Using a tuple instead of a string causes the method to
    perform some action (see MockHandler.handle()), eg:
    
    [["http_error"], [("http_open", "return request")]]
    
    defines .http_error() on one handler (which simply returns None), and
    .http_open() on another handler, which returns a Request object.
    
    """
    handlers = []
    count = 0
    for meths in meth_spec:

        class MockHandlerSubclass(MockHandler):
            pass

        h = MockHandlerSubclass(meths)
        h.handler_order += count
        h.add_parent(opener)
        count = count + 1
        handlers.append(h)
        opener.add_handler(h)

    return handlers


def build_test_opener(*handler_instances):
    opener = OpenerDirector()
    for h in handler_instances:
        opener.add_handler(h)

    return opener


class MockHTTPHandler(urllib2.BaseHandler):

    def __init__(self, code, headers):
        self.code = code
        self.headers = headers
        self.reset()

    def reset(self):
        self._count = 0
        self.requests = []

    def http_open(self, req):
        import mimetools, httplib, copy
        from StringIO import StringIO
        self.requests.append(copy.deepcopy(req))
        if self._count == 0:
            self._count = self._count + 1
            name = httplib.responses[self.code]
            msg = mimetools.Message(StringIO(self.headers))
            return self.parent.error('http', req, MockFile(), self.code, name, msg)
        else:
            self.req = req
            msg = mimetools.Message(StringIO('\r\n\r\n'))
            return MockResponse(200, 'OK', msg, '', req.get_full_url())


class MockHTTPSHandler(urllib2.AbstractHTTPHandler):

    def __init__(self):
        urllib2.AbstractHTTPHandler.__init__(self)
        self.httpconn = MockHTTPClass()

    def https_open(self, req):
        return self.do_open(self.httpconn, req)


class MockPasswordManager():

    def add_password(self, realm, uri, user, password):
        self.realm = realm
        self.url = uri
        self.user = user
        self.password = password

    def find_user_password(self, realm, authuri):
        self.target_realm = realm
        self.target_url = authuri
        return (self.user, self.password)


class OpenerDirectorTests(unittest.TestCase):

    def test_add_non_handler(self):

        class NonHandler(object):
            pass

        self.assertRaises(TypeError, OpenerDirector().add_handler, NonHandler())

    def test_badly_named_methods(self):
        from urllib2 import URLError
        o = OpenerDirector()
        meth_spec = [[('do_open', 'return self'), ('proxy_open', 'return self')], [('redirect_request', 'return self')]]
        handlers = add_ordered_mock_handlers(o, meth_spec)
        o.add_handler(urllib2.UnknownHandler())
        for scheme in ('do', 'proxy', 'redirect'):
            self.assertRaises(URLError, o.open, scheme + '://example.com/')

    def test_handled(self):
        o = OpenerDirector()
        meth_spec = [['http_open', 'ftp_open', 'http_error_302'],
         ['ftp_open'],
         [('http_open', 'return self')],
         [('http_open', 'return self')]]
        handlers = add_ordered_mock_handlers(o, meth_spec)
        req = Request('http://example.com/')
        r = o.open(req)
        self.assertEqual(r, handlers[2])
        calls = [(handlers[0], 'http_open'), (handlers[2], 'http_open')]
        for expected, got in zip(calls, o.calls):
            handler, name, args, kwds = got
            self.assertEqual((handler, name), expected)
            self.assertEqual(args, (req,))

    def test_handler_order(self):
        o = OpenerDirector()
        handlers = []
        for meths, handler_order in [([('http_open', 'return self')], 500), (['http_open'], 0)]:

            class MockHandlerSubclass(MockHandler):
                pass

            h = MockHandlerSubclass(meths)
            h.handler_order = handler_order
            handlers.append(h)
            o.add_handler(h)

        r = o.open('http://example.com/')
        self.assertEqual(o.calls[0][0], handlers[1])
        self.assertEqual(o.calls[1][0], handlers[0])

    def test_raise(self):
        o = OpenerDirector()
        meth_spec = [[('http_open', 'raise')], [('http_open', 'return self')]]
        handlers = add_ordered_mock_handlers(o, meth_spec)
        req = Request('http://example.com/')
        self.assertRaises(urllib2.URLError, o.open, req)
        self.assertEqual(o.calls, [(handlers[0],
          'http_open',
          (req,),
          {})])

    def test_http_error(self):
        o = OpenerDirector()
        meth_spec = [[('http_open', 'error 302')],
         [('http_error_400', 'raise'), 'http_open'],
         [('http_error_302', 'return response'), 'http_error_303', 'http_error'],
         ['http_error_302']]
        handlers = add_ordered_mock_handlers(o, meth_spec)

        class Unknown:

            def __eq__(self, other):
                return True

        req = Request('http://example.com/')
        r = o.open(req)
        raise len(o.calls) == 2 or AssertionError
        calls = [(handlers[0], 'http_open', (req,)), (handlers[2], 'http_error_302', (req,
           Unknown(),
           302,
           '',
           {}))]
        for expected, got in zip(calls, o.calls):
            handler, method_name, args = expected
            self.assertEqual((handler, method_name), got[:2])
            self.assertEqual(args, got[2])

    def test_processors(self):
        o = OpenerDirector()
        meth_spec = [[('http_request', 'return request'), ('http_response', 'return response')], [('http_request', 'return request'), ('http_response', 'return response')]]
        handlers = add_ordered_mock_handlers(o, meth_spec)
        req = Request('http://example.com/')
        r = o.open(req)
        calls = [(handlers[0], 'http_request'),
         (handlers[1], 'http_request'),
         (handlers[0], 'http_response'),
         (handlers[1], 'http_response')]
        for i, (handler, name, args, kwds) in enumerate(o.calls):
            if i < 2:
                self.assertEqual((handler, name), calls[i])
                self.assertEqual(len(args), 1)
                self.assertIsInstance(args[0], Request)
            else:
                self.assertEqual((handler, name), calls[i])
                self.assertEqual(len(args), 2)
                self.assertIsInstance(args[0], Request)
                self.assertTrue(args[1] is None or isinstance(args[1], MockResponse))

        return


def sanepathname2url(path):
    import urllib
    urlpath = urllib.pathname2url(path)
    if os.name == 'nt' and urlpath.startswith('///'):
        urlpath = urlpath[2:]
    return urlpath


class HandlerTests(unittest.TestCase):

    def test_ftp(self):

        class MockFTPWrapper:

            def __init__(self, data):
                self.data = data

            def retrfile(self, filename, filetype):
                self.filename, self.filetype = filename, filetype
                return (StringIO.StringIO(self.data), len(self.data))

            def close(self):
                pass

        class NullFTPHandler(urllib2.FTPHandler):

            def __init__(self, data):
                self.data = data

            def connect_ftp(self, user, passwd, host, port, dirs, timeout = socket._GLOBAL_DEFAULT_TIMEOUT):
                self.user, self.passwd = user, passwd
                self.host, self.port = host, port
                self.dirs = dirs
                self.ftpwrapper = MockFTPWrapper(self.data)
                return self.ftpwrapper

        import ftplib
        data = 'rheum rhaponicum'
        h = NullFTPHandler(data)
        o = h.parent = MockOpener()
        for url, host, port, user, passwd, type_, dirs, filename, mimetype in [('ftp://localhost/foo/bar/baz.html',
          'localhost',
          ftplib.FTP_PORT,
          '',
          '',
          'I',
          ['foo', 'bar'],
          'baz.html',
          'text/html'),
         ('ftp://parrot@localhost/foo/bar/baz.html',
          'localhost',
          ftplib.FTP_PORT,
          'parrot',
          '',
          'I',
          ['foo', 'bar'],
          'baz.html',
          'text/html'),
         ('ftp://%25parrot@localhost/foo/bar/baz.html',
          'localhost',
          ftplib.FTP_PORT,
          '%parrot',
          '',
          'I',
          ['foo', 'bar'],
          'baz.html',
          'text/html'),
         ('ftp://%2542parrot@localhost/foo/bar/baz.html',
          'localhost',
          ftplib.FTP_PORT,
          '%42parrot',
          '',
          'I',
          ['foo', 'bar'],
          'baz.html',
          'text/html'),
         ('ftp://localhost:80/foo/bar/',
          'localhost',
          80,
          '',
          '',
          'D',
          ['foo', 'bar'],
          '',
          None),
         ('ftp://localhost/baz.gif;type=a',
          'localhost',
          ftplib.FTP_PORT,
          '',
          '',
          'A',
          [],
          'baz.gif',
          None)]:
            req = Request(url)
            req.timeout = None
            r = h.ftp_open(req)
            self.assertEqual(h.user, user)
            self.assertEqual(h.passwd, passwd)
            self.assertEqual(h.host, socket.gethostbyname(host))
            self.assertEqual(h.port, port)
            self.assertEqual(h.dirs, dirs)
            self.assertEqual(h.ftpwrapper.filename, filename)
            self.assertEqual(h.ftpwrapper.filetype, type_)
            headers = r.info()
            self.assertEqual(headers.get('Content-type'), mimetype)
            self.assertEqual(int(headers['Content-length']), len(data))

        return

    def test_file(self):
        import rfc822, socket
        h = urllib2.FileHandler()
        o = h.parent = MockOpener()
        TESTFN = test_support.TESTFN
        urlpath = sanepathname2url(os.path.abspath(TESTFN))
        towrite = 'hello, world\n'
        urls = ['file://localhost%s' % urlpath, 'file://%s' % urlpath, 'file://%s%s' % (socket.gethostbyname('localhost'), urlpath)]
        try:
            localaddr = socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            localaddr = ''

        if localaddr:
            urls.append('file://%s%s' % (localaddr, urlpath))
        for url in urls:
            f = open(TESTFN, 'wb')
            try:
                try:
                    f.write(towrite)
                finally:
                    f.close()

                r = h.file_open(Request(url))
                try:
                    data = r.read()
                    headers = r.info()
                    respurl = r.geturl()
                finally:
                    r.close()

                stats = os.stat(TESTFN)
                modified = rfc822.formatdate(stats.st_mtime)
            finally:
                os.remove(TESTFN)

            self.assertEqual(data, towrite)
            self.assertEqual(headers['Content-type'], 'text/plain')
            self.assertEqual(headers['Content-length'], '13')
            self.assertEqual(headers['Last-modified'], modified)
            self.assertEqual(respurl, url)

        for url in ['file://localhost:80%s' % urlpath,
         'file:///file_does_not_exist.txt',
         'file://%s:80%s/%s' % (socket.gethostbyname('localhost'), os.getcwd(), TESTFN),
         'file://somerandomhost.ontheinternet.com%s/%s' % (os.getcwd(), TESTFN)]:
            try:
                f = open(TESTFN, 'wb')
                try:
                    f.write(towrite)
                finally:
                    f.close()

                self.assertRaises(urllib2.URLError, h.file_open, Request(url))
            finally:
                os.remove(TESTFN)

        h = urllib2.FileHandler()
        o = h.parent = MockOpener()
        for url, ftp in [('file://ftp.example.com//foo.txt', True),
         ('file://ftp.example.com///foo.txt', False),
         ('file://ftp.example.com/foo.txt', False),
         ('file://somehost//foo/something.txt', True),
         ('file://localhost//foo/something.txt', False)]:
            req = Request(url)
            try:
                h.file_open(req)
            except (urllib2.URLError, OSError):
                self.assertTrue(not ftp)
            else:
                self.assertTrue(o.req is req)
                self.assertEqual(req.type, 'ftp')

            self.assertEqual(req.type == 'ftp', ftp)

    def test_http(self):
        h = urllib2.AbstractHTTPHandler()
        o = h.parent = MockOpener()
        url = 'http://example.com/'
        for method, data in [('GET', None), ('POST', 'blah')]:
            req = Request(url, data, {'Foo': 'bar'})
            req.timeout = None
            req.add_unredirected_header('Spam', 'eggs')
            http = MockHTTPClass()
            r = h.do_open(http, req)
            r.read
            r.readline
            r.info
            r.geturl
            (r.code, r.msg == 200, 'OK')
            hdrs = r.info()
            hdrs.get
            hdrs.has_key
            self.assertEqual(r.geturl(), url)
            self.assertEqual(http.host, 'example.com')
            self.assertEqual(http.level, 0)
            self.assertEqual(http.method, method)
            self.assertEqual(http.selector, '/')
            self.assertEqual(http.req_headers, [('Connection', 'close'), ('Foo', 'bar'), ('Spam', 'eggs')])
            self.assertEqual(http.data, data)

        http.raise_on_endheaders = True
        self.assertRaises(urllib2.URLError, h.do_open, http, req)
        o.addheaders = [('Spam', 'eggs')]
        for data in ('', None):
            req = Request('http://example.com/', data)
            r = MockResponse(200, 'OK', {}, '')
            newreq = h.do_request_(req)
            if data is None:
                self.assertNotIn('Content-length', req.unredirected_hdrs)
                self.assertNotIn('Content-type', req.unredirected_hdrs)
            else:
                self.assertEqual(req.unredirected_hdrs['Content-length'], '0')
                self.assertEqual(req.unredirected_hdrs['Content-type'], 'application/x-www-form-urlencoded')
            self.assertEqual(req.unredirected_hdrs['Host'], 'example.com')
            self.assertEqual(req.unredirected_hdrs['Spam'], 'eggs')
            req.add_unredirected_header('Content-length', 'foo')
            req.add_unredirected_header('Content-type', 'bar')
            req.add_unredirected_header('Host', 'baz')
            req.add_unredirected_header('Spam', 'foo')
            newreq = h.do_request_(req)
            self.assertEqual(req.unredirected_hdrs['Content-length'], 'foo')
            self.assertEqual(req.unredirected_hdrs['Content-type'], 'bar')
            self.assertEqual(req.unredirected_hdrs['Host'], 'baz')
            self.assertEqual(req.unredirected_hdrs['Spam'], 'foo')

        return

    def test_http_doubleslash(self):
        h = urllib2.AbstractHTTPHandler()
        o = h.parent = MockOpener()
        data = ''
        ds_urls = ['http://example.com/foo/bar/baz.html',
         'http://example.com//foo/bar/baz.html',
         'http://example.com/foo//bar/baz.html',
         'http://example.com/foo/bar//baz.html']
        for ds_url in ds_urls:
            ds_req = Request(ds_url, data)
            np_ds_req = h.do_request_(ds_req)
            self.assertEqual(np_ds_req.unredirected_hdrs['Host'], 'example.com')
            ds_req.set_proxy('someproxy:3128', None)
            p_ds_req = h.do_request_(ds_req)
            self.assertEqual(p_ds_req.unredirected_hdrs['Host'], 'example.com')

        return

    def test_fixpath_in_weirdurls(self):
        h = urllib2.AbstractHTTPHandler()
        o = h.parent = MockOpener()
        weird_url = 'http://www.python.org?getspam'
        req = Request(weird_url)
        newreq = h.do_request_(req)
        self.assertEqual(newreq.get_host(), 'www.python.org')
        self.assertEqual(newreq.get_selector(), '/?getspam')
        url_without_path = 'http://www.python.org'
        req = Request(url_without_path)
        newreq = h.do_request_(req)
        self.assertEqual(newreq.get_host(), 'www.python.org')
        self.assertEqual(newreq.get_selector(), '')

    def test_errors(self):
        h = urllib2.HTTPErrorProcessor()
        o = h.parent = MockOpener()
        url = 'http://example.com/'
        req = Request(url)
        r = MockResponse(200, 'OK', {}, '', url)
        newr = h.http_response(req, r)
        self.assertTrue(r is newr)
        self.assertTrue(not hasattr(o, 'proto'))
        r = MockResponse(202, 'Accepted', {}, '', url)
        newr = h.http_response(req, r)
        self.assertTrue(r is newr)
        self.assertTrue(not hasattr(o, 'proto'))
        r = MockResponse(206, 'Partial content', {}, '', url)
        newr = h.http_response(req, r)
        self.assertTrue(r is newr)
        self.assertTrue(not hasattr(o, 'proto'))
        r = MockResponse(502, 'Bad gateway', {}, '', url)
        self.assertTrue(h.http_response(req, r) is None)
        self.assertEqual(o.proto, 'http')
        self.assertEqual(o.args, (req,
         r,
         502,
         'Bad gateway',
         {}))
        return

    def test_cookies(self):
        cj = MockCookieJar()
        h = urllib2.HTTPCookieProcessor(cj)
        o = h.parent = MockOpener()
        req = Request('http://example.com/')
        r = MockResponse(200, 'OK', {}, '')
        newreq = h.http_request(req)
        self.assertTrue(cj.ach_req is req is newreq)
        self.assertEqual(req.get_origin_req_host(), 'example.com')
        self.assertTrue(not req.is_unverifiable())
        newr = h.http_response(req, r)
        self.assertTrue(cj.ec_req is req)
        self.assertTrue(cj.ec_r is r is newr)

    def test_redirect--- This code section failed: ---

0	LOAD_CONST        'http://example.com/a.html'
3	STORE_FAST        'from_url'

6	LOAD_CONST        'http://example.com/b.html'
9	STORE_FAST        'to_url'

12	LOAD_GLOBAL       'urllib2'
15	LOAD_ATTR         'HTTPRedirectHandler'
18	CALL_FUNCTION_0   None
21	STORE_FAST        'h'

24	LOAD_GLOBAL       'MockOpener'
27	CALL_FUNCTION_0   None
30	DUP_TOP           None
31	STORE_FAST        'o'
34	LOAD_FAST         'h'
37	STORE_ATTR        'parent'

40	SETUP_LOOP        '527'
43	LOAD_CONST        (301, 302, 303, 307)
46	GET_ITER          None
47	FOR_ITER          '526'
50	STORE_FAST        'code'

53	SETUP_LOOP        '523'
56	LOAD_CONST        (None, 'blah\nblah\n')
59	GET_ITER          None
60	FOR_ITER          '522'
63	STORE_FAST        'data'

66	LOAD_GLOBAL       'getattr'
69	LOAD_FAST         'h'
72	LOAD_CONST        'http_error_%s'
75	LOAD_FAST         'code'
78	BINARY_MODULO     None
79	CALL_FUNCTION_2   None
82	STORE_FAST        'method'

85	LOAD_GLOBAL       'Request'
88	LOAD_FAST         'from_url'
91	LOAD_FAST         'data'
94	CALL_FUNCTION_2   None
97	STORE_FAST        'req'

100	LOAD_FAST         'req'
103	LOAD_ATTR         'add_header'
106	LOAD_CONST        'Nonsense'
109	LOAD_CONST        'viking=withhold'
112	CALL_FUNCTION_2   None
115	POP_TOP           None

116	LOAD_GLOBAL       'socket'
119	LOAD_ATTR         '_GLOBAL_DEFAULT_TIMEOUT'
122	LOAD_FAST         'req'
125	STORE_ATTR        'timeout'

128	LOAD_FAST         'data'
131	LOAD_CONST        None
134	COMPARE_OP        'is not'
137	POP_JUMP_IF_FALSE '171'

140	LOAD_FAST         'req'
143	LOAD_ATTR         'add_header'
146	LOAD_CONST        'Content-Length'
149	LOAD_GLOBAL       'str'
152	LOAD_GLOBAL       'len'
155	LOAD_FAST         'data'
158	CALL_FUNCTION_1   None
161	CALL_FUNCTION_1   None
164	CALL_FUNCTION_2   None
167	POP_TOP           None
168	JUMP_FORWARD      '171'
171_0	COME_FROM         '168'

171	LOAD_FAST         'req'
174	LOAD_ATTR         'add_unredirected_header'
177	LOAD_CONST        'Spam'
180	LOAD_CONST        'spam'
183	CALL_FUNCTION_2   None
186	POP_TOP           None

187	SETUP_EXCEPT      '232'

190	LOAD_FAST         'method'
193	LOAD_FAST         'req'
196	LOAD_GLOBAL       'MockFile'
199	CALL_FUNCTION_0   None
202	LOAD_FAST         'code'
205	LOAD_CONST        'Blah'

208	LOAD_GLOBAL       'MockHeaders'
211	BUILD_MAP         None
214	LOAD_FAST         'to_url'
217	LOAD_CONST        'location'
220	STORE_MAP         None
221	CALL_FUNCTION_1   None
224	CALL_FUNCTION_5   None
227	POP_TOP           None
228	POP_BLOCK         None
229	JUMP_FORWARD      '283'
232_0	COME_FROM         '187'

232	DUP_TOP           None
233	LOAD_GLOBAL       'urllib2'
236	LOAD_ATTR         'HTTPError'
239	COMPARE_OP        'exception match'
242	POP_JUMP_IF_FALSE '282'
245	POP_TOP           None
246	POP_TOP           None
247	POP_TOP           None

248	LOAD_FAST         'self'
251	LOAD_ATTR         'assertTrue'
254	LOAD_FAST         'code'
257	LOAD_CONST        307
260	COMPARE_OP        '=='
263	JUMP_IF_FALSE_OR_POP '275'
266	LOAD_FAST         'data'
269	LOAD_CONST        None
272	COMPARE_OP        'is not'
275_0	COME_FROM         '263'
275	CALL_FUNCTION_1   None
278	POP_TOP           None
279	JUMP_FORWARD      '283'
282	END_FINALLY       None
283_0	COME_FROM         '229'
283_1	COME_FROM         '282'

283	LOAD_FAST         'self'
286	LOAD_ATTR         'assertEqual'
289	LOAD_FAST         'o'
292	LOAD_ATTR         'req'
295	LOAD_ATTR         'get_full_url'
298	CALL_FUNCTION_0   None
301	LOAD_FAST         'to_url'
304	CALL_FUNCTION_2   None
307	POP_TOP           None

308	SETUP_EXCEPT      '340'

311	LOAD_FAST         'self'
314	LOAD_ATTR         'assertEqual'
317	LOAD_FAST         'o'
320	LOAD_ATTR         'req'
323	LOAD_ATTR         'get_method'
326	CALL_FUNCTION_0   None
329	LOAD_CONST        'GET'
332	CALL_FUNCTION_2   None
335	POP_TOP           None
336	POP_BLOCK         None
337	JUMP_FORWARD      '380'
340_0	COME_FROM         '308'

340	DUP_TOP           None
341	LOAD_GLOBAL       'AttributeError'
344	COMPARE_OP        'exception match'
347	POP_JUMP_IF_FALSE '379'
350	POP_TOP           None
351	POP_TOP           None
352	POP_TOP           None

353	LOAD_FAST         'self'
356	LOAD_ATTR         'assertTrue'
359	LOAD_FAST         'o'
362	LOAD_ATTR         'req'
365	LOAD_ATTR         'has_data'
368	CALL_FUNCTION_0   None
371	UNARY_NOT         None
372	CALL_FUNCTION_1   None
375	POP_TOP           None
376	JUMP_FORWARD      '380'
379	END_FINALLY       None
380_0	COME_FROM         '337'
380_1	COME_FROM         '379'

380	BUILD_LIST_0      None
383	LOAD_FAST         'o'
386	LOAD_ATTR         'req'
389	LOAD_ATTR         'headers'
392	GET_ITER          None
393	FOR_ITER          '414'
396	STORE_FAST        'x'
399	LOAD_FAST         'x'
402	LOAD_ATTR         'lower'
405	CALL_FUNCTION_0   None
408	LIST_APPEND       None
411	JUMP_BACK         '393'
414	STORE_FAST        'headers'

417	LOAD_FAST         'self'
420	LOAD_ATTR         'assertNotIn'
423	LOAD_CONST        'content-length'
426	LOAD_FAST         'headers'
429	CALL_FUNCTION_2   None
432	POP_TOP           None

433	LOAD_FAST         'self'
436	LOAD_ATTR         'assertNotIn'
439	LOAD_CONST        'content-type'
442	LOAD_FAST         'headers'
445	CALL_FUNCTION_2   None
448	POP_TOP           None

449	LOAD_FAST         'self'
452	LOAD_ATTR         'assertEqual'
455	LOAD_FAST         'o'
458	LOAD_ATTR         'req'
461	LOAD_ATTR         'headers'
464	LOAD_CONST        'Nonsense'
467	BINARY_SUBSCR     None

468	LOAD_CONST        'viking=withhold'
471	CALL_FUNCTION_2   None
474	POP_TOP           None

475	LOAD_FAST         'self'
478	LOAD_ATTR         'assertNotIn'
481	LOAD_CONST        'Spam'
484	LOAD_FAST         'o'
487	LOAD_ATTR         'req'
490	LOAD_ATTR         'headers'
493	CALL_FUNCTION_2   None
496	POP_TOP           None

497	LOAD_FAST         'self'
500	LOAD_ATTR         'assertNotIn'
503	LOAD_CONST        'Spam'
506	LOAD_FAST         'o'
509	LOAD_ATTR         'req'
512	LOAD_ATTR         'unredirected_hdrs'
515	CALL_FUNCTION_2   None
518	POP_TOP           None
519	JUMP_BACK         '60'
522	POP_BLOCK         None
523_0	COME_FROM         '53'
523	JUMP_BACK         '47'
526	POP_BLOCK         None
527_0	COME_FROM         '40'

527	LOAD_GLOBAL       'Request'
530	LOAD_FAST         'from_url'
533	CALL_FUNCTION_1   None
536	STORE_FAST        'req'

539	LOAD_GLOBAL       'socket'
542	LOAD_ATTR         '_GLOBAL_DEFAULT_TIMEOUT'
545	LOAD_FAST         'req'
548	STORE_ATTR        'timeout'

551	LOAD_FAST         'to_url'
554	LOAD_CONST        '<code_object redirect>'
557	MAKE_FUNCTION_1   None
560	STORE_FAST        'redirect'

563	LOAD_GLOBAL       'Request'
566	LOAD_FAST         'from_url'
569	LOAD_CONST        'origin_req_host'
572	LOAD_CONST        'example.com'
575	CALL_FUNCTION_257 None
578	STORE_FAST        'req'

581	LOAD_CONST        0
584	STORE_FAST        'count'

587	LOAD_GLOBAL       'socket'
590	LOAD_ATTR         '_GLOBAL_DEFAULT_TIMEOUT'
593	LOAD_FAST         'req'
596	STORE_ATTR        'timeout'

599	SETUP_EXCEPT      '639'

602	SETUP_LOOP        '635'

605	LOAD_FAST         'redirect'
608	LOAD_FAST         'h'
611	LOAD_FAST         'req'
614	LOAD_CONST        'http://example.com/'
617	CALL_FUNCTION_3   None
620	POP_TOP           None

621	LOAD_FAST         'count'
624	LOAD_CONST        1
627	BINARY_ADD        None
628	STORE_FAST        'count'
631	JUMP_BACK         '605'
634	POP_BLOCK         None
635_0	COME_FROM         '602'
635	POP_BLOCK         None
636	JUMP_FORWARD      '681'
639_0	COME_FROM         '599'

639	DUP_TOP           None
640	LOAD_GLOBAL       'urllib2'
643	LOAD_ATTR         'HTTPError'
646	COMPARE_OP        'exception match'
649	POP_JUMP_IF_FALSE '680'
652	POP_TOP           None
653	POP_TOP           None
654	POP_TOP           None

655	LOAD_FAST         'self'
658	LOAD_ATTR         'assertEqual'
661	LOAD_FAST         'count'
664	LOAD_GLOBAL       'urllib2'
667	LOAD_ATTR         'HTTPRedirectHandler'
670	LOAD_ATTR         'max_repeats'
673	CALL_FUNCTION_2   None
676	POP_TOP           None
677	JUMP_FORWARD      '681'
680	END_FINALLY       None
681_0	COME_FROM         '636'
681_1	COME_FROM         '680'

681	LOAD_GLOBAL       'Request'
684	LOAD_FAST         'from_url'
687	LOAD_CONST        'origin_req_host'
690	LOAD_CONST        'example.com'
693	CALL_FUNCTION_257 None
696	STORE_FAST        'req'

699	LOAD_CONST        0
702	STORE_FAST        'count'

705	LOAD_GLOBAL       'socket'
708	LOAD_ATTR         '_GLOBAL_DEFAULT_TIMEOUT'
711	LOAD_FAST         'req'
714	STORE_ATTR        'timeout'

717	SETUP_EXCEPT      '761'

720	SETUP_LOOP        '757'

723	LOAD_FAST         'redirect'
726	LOAD_FAST         'h'
729	LOAD_FAST         'req'
732	LOAD_CONST        'http://example.com/%d'
735	LOAD_FAST         'count'
738	BINARY_MODULO     None
739	CALL_FUNCTION_3   None
742	POP_TOP           None

743	LOAD_FAST         'count'
746	LOAD_CONST        1
749	BINARY_ADD        None
750	STORE_FAST        'count'
753	JUMP_BACK         '723'
756	POP_BLOCK         None
757_0	COME_FROM         '720'
757	POP_BLOCK         None
758	JUMP_FORWARD      '803'
761_0	COME_FROM         '717'

761	DUP_TOP           None
762	LOAD_GLOBAL       'urllib2'
765	LOAD_ATTR         'HTTPError'
768	COMPARE_OP        'exception match'
771	POP_JUMP_IF_FALSE '802'
774	POP_TOP           None
775	POP_TOP           None
776	POP_TOP           None

777	LOAD_FAST         'self'
780	LOAD_ATTR         'assertEqual'
783	LOAD_FAST         'count'

786	LOAD_GLOBAL       'urllib2'
789	LOAD_ATTR         'HTTPRedirectHandler'
792	LOAD_ATTR         'max_redirections'
795	CALL_FUNCTION_2   None
798	POP_TOP           None
799	JUMP_FORWARD      '803'
802	END_FINALLY       None
803_0	COME_FROM         '758'
803_1	COME_FROM         '802'
803	LOAD_CONST        None
806	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 634

    def test_invalid_redirect(self):
        from_url = 'http://example.com/a.html'
        valid_schemes = ['http', 'https', 'ftp']
        invalid_schemes = ['file', 'imap', 'ldap']
        schemeless_url = 'example.com/b.html'
        h = urllib2.HTTPRedirectHandler()
        o = h.parent = MockOpener()
        req = Request(from_url)
        req.timeout = socket._GLOBAL_DEFAULT_TIMEOUT
        for scheme in invalid_schemes:
            invalid_url = scheme + '://' + schemeless_url
            self.assertRaises(urllib2.HTTPError, h.http_error_302, req, MockFile(), 302, 'Security Loophole', MockHeaders({'location': invalid_url}))

        for scheme in valid_schemes:
            valid_url = scheme + '://' + schemeless_url
            h.http_error_302(req, MockFile(), 302, "That's fine", MockHeaders({'location': valid_url}))
            self.assertEqual(o.req.get_full_url(), valid_url)

    def test_cookie_redirect(self):
        from cookielib import CookieJar
        from test.test_cookielib import interact_netscape
        cj = CookieJar()
        interact_netscape(cj, 'http://www.example.com/', 'spam=eggs')
        hh = MockHTTPHandler(302, 'Location: http://www.cracker.com/\r\n\r\n')
        hdeh = urllib2.HTTPDefaultErrorHandler()
        hrh = urllib2.HTTPRedirectHandler()
        cp = urllib2.HTTPCookieProcessor(cj)
        o = build_test_opener(hh, hdeh, hrh, cp)
        o.open('http://www.example.com/')
        self.assertTrue(not hh.req.has_header('Cookie'))

    def test_redirect_fragment(self):
        redirected_url = 'http://www.example.com/index.html#OK\r\n\r\n'
        hh = MockHTTPHandler(302, 'Location: ' + redirected_url)
        hdeh = urllib2.HTTPDefaultErrorHandler()
        hrh = urllib2.HTTPRedirectHandler()
        o = build_test_opener(hh, hdeh, hrh)
        fp = o.open('http://www.example.com')
        self.assertEqual(fp.geturl(), redirected_url.strip())

    def test_proxy(self):
        o = OpenerDirector()
        ph = urllib2.ProxyHandler(dict(http='proxy.example.com:3128'))
        o.add_handler(ph)
        meth_spec = [[('http_open', 'return response')]]
        handlers = add_ordered_mock_handlers(o, meth_spec)
        req = Request('http://acme.example.com/')
        self.assertEqual(req.get_host(), 'acme.example.com')
        r = o.open(req)
        self.assertEqual(req.get_host(), 'proxy.example.com:3128')
        self.assertEqual([(handlers[0], 'http_open')], [ tup[0:2] for tup in o.calls ])

    def test_proxy_no_proxy(self):
        os.environ['no_proxy'] = 'python.org'
        o = OpenerDirector()
        ph = urllib2.ProxyHandler(dict(http='proxy.example.com'))
        o.add_handler(ph)
        req = Request('http://www.perl.org/')
        self.assertEqual(req.get_host(), 'www.perl.org')
        r = o.open(req)
        self.assertEqual(req.get_host(), 'proxy.example.com')
        req = Request('http://www.python.org')
        self.assertEqual(req.get_host(), 'www.python.org')
        r = o.open(req)
        self.assertEqual(req.get_host(), 'www.python.org')
        del os.environ['no_proxy']

    def test_proxy_https(self):
        o = OpenerDirector()
        ph = urllib2.ProxyHandler(dict(https='proxy.example.com:3128'))
        o.add_handler(ph)
        meth_spec = [[('https_open', 'return response')]]
        handlers = add_ordered_mock_handlers(o, meth_spec)
        req = Request('https://www.example.com/')
        self.assertEqual(req.get_host(), 'www.example.com')
        r = o.open(req)
        self.assertEqual(req.get_host(), 'proxy.example.com:3128')
        self.assertEqual([(handlers[0], 'https_open')], [ tup[0:2] for tup in o.calls ])

    def test_proxy_https_proxy_authorization(self):
        o = OpenerDirector()
        ph = urllib2.ProxyHandler(dict(https='proxy.example.com:3128'))
        o.add_handler(ph)
        https_handler = MockHTTPSHandler()
        o.add_handler(https_handler)
        req = Request('https://www.example.com/')
        req.add_header('Proxy-Authorization', 'FooBar')
        req.add_header('User-Agent', 'Grail')
        self.assertEqual(req.get_host(), 'www.example.com')
        self.assertIsNone(req._tunnel_host)
        r = o.open(req)
        self.assertNotIn(('Proxy-Authorization', 'FooBar'), https_handler.httpconn.req_headers)
        self.assertIn(('User-Agent', 'Grail'), https_handler.httpconn.req_headers)
        self.assertIsNotNone(req._tunnel_host)
        self.assertEqual(req.get_host(), 'proxy.example.com:3128')
        self.assertEqual(req.get_header('Proxy-authorization'), 'FooBar')

    def test_basic_auth(self, quote_char = '"'):
        opener = OpenerDirector()
        password_manager = MockPasswordManager()
        auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
        realm = 'ACME Widget Store'
        http_handler = MockHTTPHandler(401, 'WWW-Authenticate: Basic realm=%s%s%s\r\n\r\n' % (quote_char, realm, quote_char))
        opener.add_handler(auth_handler)
        opener.add_handler(http_handler)
        self._test_basic_auth(opener, auth_handler, 'Authorization', realm, http_handler, password_manager, 'http://acme.example.com/protected', 'http://acme.example.com/protected')

    def test_basic_auth_with_single_quoted_realm(self):
        self.test_basic_auth(quote_char="'")

    def test_proxy_basic_auth(self):
        opener = OpenerDirector()
        ph = urllib2.ProxyHandler(dict(http='proxy.example.com:3128'))
        opener.add_handler(ph)
        password_manager = MockPasswordManager()
        auth_handler = urllib2.ProxyBasicAuthHandler(password_manager)
        realm = 'ACME Networks'
        http_handler = MockHTTPHandler(407, 'Proxy-Authenticate: Basic realm="%s"\r\n\r\n' % realm)
        opener.add_handler(auth_handler)
        opener.add_handler(http_handler)
        self._test_basic_auth(opener, auth_handler, 'Proxy-authorization', realm, http_handler, password_manager, 'http://acme.example.com:3128/protected', 'proxy.example.com:3128')

    def test_basic_and_digest_auth_handlers(self):

        class RecordingOpenerDirector(OpenerDirector):

            def __init__(self):
                OpenerDirector.__init__(self)
                self.recorded = []

            def record(self, info):
                self.recorded.append(info)

        class TestDigestAuthHandler(urllib2.HTTPDigestAuthHandler):

            def http_error_401(self, *args, **kwds):
                self.parent.record('digest')
                urllib2.HTTPDigestAuthHandler.http_error_401(self, *args, **kwds)

        class TestBasicAuthHandler(urllib2.HTTPBasicAuthHandler):

            def http_error_401(self, *args, **kwds):
                self.parent.record('basic')
                urllib2.HTTPBasicAuthHandler.http_error_401(self, *args, **kwds)

        opener = RecordingOpenerDirector()
        password_manager = MockPasswordManager()
        digest_handler = TestDigestAuthHandler(password_manager)
        basic_handler = TestBasicAuthHandler(password_manager)
        realm = 'ACME Networks'
        http_handler = MockHTTPHandler(401, 'WWW-Authenticate: Basic realm="%s"\r\n\r\n' % realm)
        opener.add_handler(basic_handler)
        opener.add_handler(digest_handler)
        opener.add_handler(http_handler)
        self._test_basic_auth(opener, basic_handler, 'Authorization', realm, http_handler, password_manager, 'http://acme.example.com/protected', 'http://acme.example.com/protected')
        self.assertEqual(opener.recorded, ['digest', 'basic'] * 2)

    def _test_basic_auth(self, opener, auth_handler, auth_header, realm, http_handler, password_manager, request_url, protected_url):
        import base64
        user, password = ('wile', 'coyote')
        auth_handler.add_password(realm, request_url, user, password)
        self.assertEqual(realm, password_manager.realm)
        self.assertEqual(request_url, password_manager.url)
        self.assertEqual(user, password_manager.user)
        self.assertEqual(password, password_manager.password)
        r = opener.open(request_url)
        self.assertEqual(password_manager.target_realm, realm)
        self.assertEqual(password_manager.target_url, protected_url)
        self.assertEqual(len(http_handler.requests), 2)
        self.assertFalse(http_handler.requests[0].has_header(auth_header))
        userpass = '%s:%s' % (user, password)
        auth_hdr_value = 'Basic ' + base64.encodestring(userpass).strip()
        self.assertEqual(http_handler.requests[1].get_header(auth_header), auth_hdr_value)
        self.assertEqual(http_handler.requests[1].unredirected_hdrs[auth_header], auth_hdr_value)
        password_manager.user = password_manager.password = None
        http_handler.reset()
        r = opener.open(request_url)
        self.assertEqual(len(http_handler.requests), 1)
        self.assertFalse(http_handler.requests[0].has_header(auth_header))
        return


class MiscTests(unittest.TestCase):

    def test_build_opener(self):

        class MyHTTPHandler(urllib2.HTTPHandler):
            pass

        class FooHandler(urllib2.BaseHandler):

            def foo_open(self):
                pass

        class BarHandler(urllib2.BaseHandler):

            def bar_open(self):
                pass

        build_opener = urllib2.build_opener
        o = build_opener(FooHandler, BarHandler)
        self.opener_has_handler(o, FooHandler)
        self.opener_has_handler(o, BarHandler)
        o = build_opener(FooHandler, BarHandler())
        self.opener_has_handler(o, FooHandler)
        self.opener_has_handler(o, BarHandler)
        o = build_opener(MyHTTPHandler)
        self.opener_has_handler(o, MyHTTPHandler)
        o = build_opener()
        self.opener_has_handler(o, urllib2.HTTPHandler)
        o = build_opener(urllib2.HTTPHandler)
        self.opener_has_handler(o, urllib2.HTTPHandler)
        o = build_opener(urllib2.HTTPHandler())
        self.opener_has_handler(o, urllib2.HTTPHandler)

        class MyOtherHTTPHandler(urllib2.HTTPHandler):
            pass

        o = build_opener(MyHTTPHandler, MyOtherHTTPHandler)
        self.opener_has_handler(o, MyHTTPHandler)
        self.opener_has_handler(o, MyOtherHTTPHandler)

    def opener_has_handler(self, opener, handler_class):
        for h in opener.handlers:
            if h.__class__ == handler_class:
                break
        else:
            self.assertTrue(False)


class RequestTests(unittest.TestCase):

    def setUp(self):
        self.get = urllib2.Request('http://www.python.org/~jeremy/')
        self.post = urllib2.Request('http://www.python.org/~jeremy/', 'data', headers={'X-Test': 'test'})

    def test_method(self):
        self.assertEqual('POST', self.post.get_method())
        self.assertEqual('GET', self.get.get_method())

    def test_add_data(self):
        self.assertTrue(not self.get.has_data())
        self.assertEqual('GET', self.get.get_method())
        self.get.add_data('spam')
        self.assertTrue(self.get.has_data())
        self.assertEqual('POST', self.get.get_method())

    def test_get_full_url(self):
        self.assertEqual('http://www.python.org/~jeremy/', self.get.get_full_url())

    def test_selector(self):
        self.assertEqual('/~jeremy/', self.get.get_selector())
        req = urllib2.Request('http://www.python.org/')
        self.assertEqual('/', req.get_selector())

    def test_get_type(self):
        self.assertEqual('http', self.get.get_type())

    def test_get_host(self):
        self.assertEqual('www.python.org', self.get.get_host())

    def test_get_host_unquote(self):
        req = urllib2.Request('http://www.%70ython.org/')
        self.assertEqual('www.python.org', req.get_host())

    def test_proxy(self):
        self.assertTrue(not self.get.has_proxy())
        self.get.set_proxy('www.perl.org', 'http')
        self.assertTrue(self.get.has_proxy())
        self.assertEqual('www.python.org', self.get.get_origin_req_host())
        self.assertEqual('www.perl.org', self.get.get_host())

    def test_wrapped_url(self):
        req = Request('<URL:http://www.python.org>')
        self.assertEqual('www.python.org', req.get_host())

    def test_url_fragment(self):
        req = Request('http://www.python.org/?qs=query#fragment=true')
        self.assertEqual('/?qs=query', req.get_selector())
        req = Request('http://www.python.org/#fun=true')
        self.assertEqual('/', req.get_selector())
        url = 'http://docs.python.org/library/urllib2.html#OK'
        req = Request(url)
        self.assertEqual(req.get_full_url(), url)


def test_HTTPError_interface():
    """
    Issue 13211 reveals that HTTPError didn't implement the URLError
    interface even though HTTPError is a subclass of URLError.
    
    >>> err = urllib2.HTTPError(msg='something bad happened', url=None, code=None, hdrs=None, fp=None)
    >>> assert hasattr(err, 'reason')
    >>> err.reason
    'something bad happened'
    """
    pass


def test_main(verbose = None):
    from test import test_urllib2
    test_support.run_doctest(test_urllib2, verbose)
    test_support.run_doctest(urllib2, verbose)
    tests = (TrivialTests,
     OpenerDirectorTests,
     HandlerTests,
     MiscTests,
     RequestTests)
    test_support.run_unittest(*tests)


if __name__ == '__main__':
    test_main(verbose=True)