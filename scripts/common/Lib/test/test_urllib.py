# Embedded file name: scripts/common/Lib/test/test_urllib.py
"""Regresssion tests for urllib"""
import urllib
import httplib
import unittest
import os
import sys
import mimetools
import tempfile
import StringIO
from test import test_support
from base64 import b64encode

def hexescape(char):
    """Escape char as RFC 2396 specifies"""
    hex_repr = hex(ord(char))[2:].upper()
    if len(hex_repr) == 1:
        hex_repr = '0%s' % hex_repr
    return '%' + hex_repr


class FakeHTTPMixin(object):

    def fakehttp(self, fakedata):

        class FakeSocket(StringIO.StringIO):

            def sendall(self, data):
                FakeHTTPConnection.buf = data

            def makefile(self, *args, **kwds):
                return self

            def read(self, amt = None):
                if self.closed:
                    return ''
                return StringIO.StringIO.read(self, amt)

            def readline(self, length = None):
                if self.closed:
                    return ''
                return StringIO.StringIO.readline(self, length)

        class FakeHTTPConnection(httplib.HTTPConnection):
            buf = ''

            def connect(self):
                self.sock = FakeSocket(fakedata)

        raise httplib.HTTP._connection_class == httplib.HTTPConnection or AssertionError
        httplib.HTTP._connection_class = FakeHTTPConnection

    def unfakehttp(self):
        httplib.HTTP._connection_class = httplib.HTTPConnection


class urlopen_FileTests(unittest.TestCase):
    """Test urlopen() opening a temporary file.
    
    Try to test as much functionality as possible so as to cut down on reliance
    on connecting to the Net for testing.
    
    """

    def setUp(self):
        """Setup of a temp file to use for testing"""
        self.text = 'test_urllib: %s\n' % self.__class__.__name__
        FILE = file(test_support.TESTFN, 'wb')
        try:
            FILE.write(self.text)
        finally:
            FILE.close()

        self.pathname = test_support.TESTFN
        self.returned_obj = urllib.urlopen('file:%s' % self.pathname)

    def tearDown(self):
        """Shut down the open object"""
        self.returned_obj.close()
        os.remove(test_support.TESTFN)

    def test_interface(self):
        for attr in ('read', 'readline', 'readlines', 'fileno', 'close', 'info', 'geturl', 'getcode', '__iter__'):
            self.assertTrue(hasattr(self.returned_obj, attr), 'object returned by urlopen() lacks %s attribute' % attr)

    def test_read(self):
        self.assertEqual(self.text, self.returned_obj.read())

    def test_readline(self):
        self.assertEqual(self.text, self.returned_obj.readline())
        self.assertEqual('', self.returned_obj.readline(), 'calling readline() after exhausting the file did not return an empty string')

    def test_readlines(self):
        lines_list = self.returned_obj.readlines()
        self.assertEqual(len(lines_list), 1, 'readlines() returned the wrong number of lines')
        self.assertEqual(lines_list[0], self.text, 'readlines() returned improper text')

    def test_fileno(self):
        file_num = self.returned_obj.fileno()
        self.assertIsInstance(file_num, int, 'fileno() did not return an int')
        self.assertEqual(os.read(file_num, len(self.text)), self.text, 'Reading on the file descriptor returned by fileno() did not return the expected text')

    def test_close(self):
        self.returned_obj.close()

    def test_info(self):
        self.assertIsInstance(self.returned_obj.info(), mimetools.Message)

    def test_geturl(self):
        self.assertEqual(self.returned_obj.geturl(), self.pathname)

    def test_getcode(self):
        self.assertEqual(self.returned_obj.getcode(), None)
        return

    def test_iter(self):
        for line in self.returned_obj.__iter__():
            self.assertEqual(line, self.text)

    def test_relativelocalfile(self):
        self.assertRaises(ValueError, urllib.urlopen, './' + self.pathname)


class ProxyTests(unittest.TestCase):

    def setUp(self):
        self.env = test_support.EnvironmentVarGuard()
        for k in os.environ.keys():
            if 'proxy' in k.lower():
                self.env.unset(k)

    def tearDown(self):
        self.env.__exit__()
        del self.env

    def test_getproxies_environment_keep_no_proxies(self):
        self.env.set('NO_PROXY', 'localhost')
        proxies = urllib.getproxies_environment()
        self.assertEqual('localhost', proxies['no'])
        self.env.set('NO_PROXY', 'localhost, anotherdomain.com, newdomain.com')
        self.assertTrue(urllib.proxy_bypass_environment('anotherdomain.com'))


class urlopen_HttpTests(unittest.TestCase, FakeHTTPMixin):
    """Test urlopen() opening a fake http connection."""

    def test_read(self):
        self.fakehttp('Hello!')
        try:
            fp = urllib.urlopen('http://python.org/')
            self.assertEqual(fp.readline(), 'Hello!')
            self.assertEqual(fp.readline(), '')
            self.assertEqual(fp.geturl(), 'http://python.org/')
            self.assertEqual(fp.getcode(), 200)
        finally:
            self.unfakehttp()

    def test_url_fragment(self):
        url = 'http://docs.python.org/library/urllib.html#OK'
        self.fakehttp('Hello!')
        try:
            fp = urllib.urlopen(url)
            self.assertEqual(fp.geturl(), url)
        finally:
            self.unfakehttp()

    def test_read_bogus(self):
        self.fakehttp('HTTP/1.1 401 Authentication Required\nDate: Wed, 02 Jan 2008 03:03:54 GMT\nServer: Apache/1.3.33 (Debian GNU/Linux) mod_ssl/2.8.22 OpenSSL/0.9.7e\nConnection: close\nContent-Type: text/html; charset=iso-8859-1\n')
        try:
            self.assertRaises(IOError, urllib.urlopen, 'http://python.org/')
        finally:
            self.unfakehttp()

    def test_invalid_redirect(self):
        self.fakehttp('HTTP/1.1 302 Found\nDate: Wed, 02 Jan 2008 03:03:54 GMT\nServer: Apache/1.3.33 (Debian GNU/Linux) mod_ssl/2.8.22 OpenSSL/0.9.7e\nLocation: file:README\nConnection: close\nContent-Type: text/html; charset=iso-8859-1\n')
        try:
            self.assertRaises(IOError, urllib.urlopen, 'http://python.org/')
        finally:
            self.unfakehttp()

    def test_empty_socket(self):
        self.fakehttp('')
        try:
            self.assertRaises(IOError, urllib.urlopen, 'http://something')
        finally:
            self.unfakehttp()

    def test_userpass_inurl(self):
        self.fakehttp('Hello!')
        try:
            fakehttp_wrapper = httplib.HTTP._connection_class
            fp = urllib.urlopen('http://user:pass@python.org/')
            authorization = 'Authorization: Basic %s\r\n' % b64encode('user:pass')
            self.assertIn(authorization, fakehttp_wrapper.buf)
            self.assertEqual(fp.readline(), 'Hello!')
            self.assertEqual(fp.readline(), '')
            self.assertEqual(fp.geturl(), 'http://user:pass@python.org/')
            self.assertEqual(fp.getcode(), 200)
        finally:
            self.unfakehttp()

    def test_userpass_with_spaces_inurl(self):
        self.fakehttp('Hello!')
        try:
            url = 'http://a b:c d@python.org/'
            fakehttp_wrapper = httplib.HTTP._connection_class
            authorization = 'Authorization: Basic %s\r\n' % b64encode('a b:c d')
            fp = urllib.urlopen(url)
            self.assertIn(authorization, fakehttp_wrapper.buf)
            self.assertEqual(fp.readline(), 'Hello!')
            self.assertEqual(fp.readline(), '')
            self.assertNotEqual(fp.geturl(), url)
            self.assertEqual(fp.getcode(), 200)
        finally:
            self.unfakehttp()


class urlretrieve_FileTests(unittest.TestCase):
    """Test urllib.urlretrieve() on local files"""

    def setUp(self):
        self.tempFiles = []
        self.registerFileForCleanUp(test_support.TESTFN)
        self.text = 'testing urllib.urlretrieve'
        try:
            FILE = file(test_support.TESTFN, 'wb')
            FILE.write(self.text)
            FILE.close()
        finally:
            try:
                FILE.close()
            except:
                pass

    def tearDown(self):
        for each in self.tempFiles:
            try:
                os.remove(each)
            except:
                pass

    def constructLocalFileUrl(self, filePath):
        return 'file://%s' % urllib.pathname2url(os.path.abspath(filePath))

    def createNewTempFile(self, data = ''):
        """Creates a new temporary file containing the specified data,
        registers the file for deletion during the test fixture tear down, and
        returns the absolute path of the file."""
        newFd, newFilePath = tempfile.mkstemp()
        try:
            self.registerFileForCleanUp(newFilePath)
            newFile = os.fdopen(newFd, 'wb')
            newFile.write(data)
            newFile.close()
        finally:
            try:
                newFile.close()
            except:
                pass

        return newFilePath

    def registerFileForCleanUp(self, fileName):
        self.tempFiles.append(fileName)

    def test_basic(self):
        result = urllib.urlretrieve('file:%s' % test_support.TESTFN)
        self.assertEqual(result[0], test_support.TESTFN)
        self.assertIsInstance(result[1], mimetools.Message, 'did not get a mimetools.Message instance as second returned value')

    def test_copy(self):
        second_temp = '%s.2' % test_support.TESTFN
        self.registerFileForCleanUp(second_temp)
        result = urllib.urlretrieve(self.constructLocalFileUrl(test_support.TESTFN), second_temp)
        self.assertEqual(second_temp, result[0])
        self.assertTrue(os.path.exists(second_temp), 'copy of the file was not made')
        FILE = file(second_temp, 'rb')
        try:
            text = FILE.read()
            FILE.close()
        finally:
            try:
                FILE.close()
            except:
                pass

        self.assertEqual(self.text, text)

    def test_reporthook(self):

        def hooktester(count, block_size, total_size, count_holder = [0]):
            self.assertIsInstance(count, int)
            self.assertIsInstance(block_size, int)
            self.assertIsInstance(total_size, int)
            self.assertEqual(count, count_holder[0])
            count_holder[0] = count_holder[0] + 1

        second_temp = '%s.2' % test_support.TESTFN
        self.registerFileForCleanUp(second_temp)
        urllib.urlretrieve(self.constructLocalFileUrl(test_support.TESTFN), second_temp, hooktester)

    def test_reporthook_0_bytes(self):
        report = []

        def hooktester(count, block_size, total_size, _report = report):
            _report.append((count, block_size, total_size))

        srcFileName = self.createNewTempFile()
        urllib.urlretrieve(self.constructLocalFileUrl(srcFileName), test_support.TESTFN, hooktester)
        self.assertEqual(len(report), 1)
        self.assertEqual(report[0][2], 0)

    def test_reporthook_5_bytes(self):
        report = []

        def hooktester(count, block_size, total_size, _report = report):
            _report.append((count, block_size, total_size))

        srcFileName = self.createNewTempFile('xxxxx')
        urllib.urlretrieve(self.constructLocalFileUrl(srcFileName), test_support.TESTFN, hooktester)
        self.assertEqual(len(report), 2)
        self.assertEqual(report[0][1], 8192)
        self.assertEqual(report[0][2], 5)

    def test_reporthook_8193_bytes(self):
        report = []

        def hooktester(count, block_size, total_size, _report = report):
            _report.append((count, block_size, total_size))

        srcFileName = self.createNewTempFile('x' * 8193)
        urllib.urlretrieve(self.constructLocalFileUrl(srcFileName), test_support.TESTFN, hooktester)
        self.assertEqual(len(report), 3)
        self.assertEqual(report[0][1], 8192)
        self.assertEqual(report[0][2], 8193)


class urlretrieve_HttpTests(unittest.TestCase, FakeHTTPMixin):
    """Test urllib.urlretrieve() using fake http connections"""

    def test_short_content_raises_ContentTooShortError(self):
        self.fakehttp('HTTP/1.1 200 OK\nDate: Wed, 02 Jan 2008 03:03:54 GMT\nServer: Apache/1.3.33 (Debian GNU/Linux) mod_ssl/2.8.22 OpenSSL/0.9.7e\nConnection: close\nContent-Length: 100\nContent-Type: text/html; charset=iso-8859-1\n\nFF\n')

        def _reporthook(par1, par2, par3):
            pass

        try:
            self.assertRaises(urllib.ContentTooShortError, urllib.urlretrieve, 'http://example.com', reporthook=_reporthook)
        finally:
            self.unfakehttp()

    def test_short_content_raises_ContentTooShortError_without_reporthook(self):
        self.fakehttp('HTTP/1.1 200 OK\nDate: Wed, 02 Jan 2008 03:03:54 GMT\nServer: Apache/1.3.33 (Debian GNU/Linux) mod_ssl/2.8.22 OpenSSL/0.9.7e\nConnection: close\nContent-Length: 100\nContent-Type: text/html; charset=iso-8859-1\n\nFF\n')
        try:
            self.assertRaises(urllib.ContentTooShortError, urllib.urlretrieve, 'http://example.com/')
        finally:
            self.unfakehttp()


class QuotingTests(unittest.TestCase):
    r"""Tests for urllib.quote() and urllib.quote_plus()
    
    According to RFC 2396 ("Uniform Resource Identifiers), to escape a
    character you write it as '%' + <2 character US-ASCII hex value>.  The Python
    code of ``'%' + hex(ord(<character>))[2:]`` escapes a character properly.
    Case does not matter on the hex letters.
    
    The various character sets specified are:
    
    Reserved characters : ";/?:@&=+$,"
        Have special meaning in URIs and must be escaped if not being used for
        their special meaning
    Data characters : letters, digits, and "-_.!~*'()"
        Unreserved and do not need to be escaped; can be, though, if desired
    Control characters : 0x00 - 0x1F, 0x7F
        Have no use in URIs so must be escaped
    space : 0x20
        Must be escaped
    Delimiters : '<>#%"'
        Must be escaped
    Unwise : "{}|\^[]`"
        Must be escaped
    
    """

    def test_never_quote(self):
        do_not_quote = ''.join(['ABCDEFGHIJKLMNOPQRSTUVWXYZ',
         'abcdefghijklmnopqrstuvwxyz',
         '0123456789',
         '_.-'])
        result = urllib.quote(do_not_quote)
        self.assertEqual(do_not_quote, result, 'using quote(): %s != %s' % (do_not_quote, result))
        result = urllib.quote_plus(do_not_quote)
        self.assertEqual(do_not_quote, result, 'using quote_plus(): %s != %s' % (do_not_quote, result))

    def test_default_safe(self):
        self.assertEqual(urllib.quote.func_defaults[0], '/')

    def test_safe(self):
        quote_by_default = '<>'
        result = urllib.quote(quote_by_default, safe=quote_by_default)
        self.assertEqual(quote_by_default, result, 'using quote(): %s != %s' % (quote_by_default, result))
        result = urllib.quote_plus(quote_by_default, safe=quote_by_default)
        self.assertEqual(quote_by_default, result, 'using quote_plus(): %s != %s' % (quote_by_default, result))

    def test_default_quoting(self):
        should_quote = [ chr(num) for num in range(32) ]
        should_quote.append('<>#%"{}|\\^[]`')
        should_quote.append(chr(127))
        should_quote = ''.join(should_quote)
        for char in should_quote:
            result = urllib.quote(char)
            self.assertEqual(hexescape(char), result, 'using quote(): %s should be escaped to %s, not %s' % (char, hexescape(char), result))
            result = urllib.quote_plus(char)
            self.assertEqual(hexescape(char), result, 'using quote_plus(): %s should be escapes to %s, not %s' % (char, hexescape(char), result))

        del should_quote
        partial_quote = 'ab[]cd'
        expected = 'ab%5B%5Dcd'
        result = urllib.quote(partial_quote)
        self.assertEqual(expected, result, 'using quote(): %s != %s' % (expected, result))
        result = urllib.quote_plus(partial_quote)
        self.assertEqual(expected, result, 'using quote_plus(): %s != %s' % (expected, result))
        self.assertRaises(TypeError, urllib.quote, None)
        return

    def test_quoting_space(self):
        result = urllib.quote(' ')
        self.assertEqual(result, hexescape(' '), 'using quote(): %s != %s' % (result, hexescape(' ')))
        result = urllib.quote_plus(' ')
        self.assertEqual(result, '+', 'using quote_plus(): %s != +' % result)
        given = 'a b cd e f'
        expect = given.replace(' ', hexescape(' '))
        result = urllib.quote(given)
        self.assertEqual(expect, result, 'using quote(): %s != %s' % (expect, result))
        expect = given.replace(' ', '+')
        result = urllib.quote_plus(given)
        self.assertEqual(expect, result, 'using quote_plus(): %s != %s' % (expect, result))

    def test_quoting_plus(self):
        self.assertEqual(urllib.quote_plus('alpha+beta gamma'), 'alpha%2Bbeta+gamma')
        self.assertEqual(urllib.quote_plus('alpha+beta gamma', '+'), 'alpha+beta+gamma')


class UnquotingTests(unittest.TestCase):
    """Tests for unquote() and unquote_plus()
    
    See the doc string for quoting_Tests for details on quoting and such.
    
    """

    def test_unquoting(self):
        escape_list = []
        for num in range(128):
            given = hexescape(chr(num))
            expect = chr(num)
            result = urllib.unquote(given)
            self.assertEqual(expect, result, 'using unquote(): %s != %s' % (expect, result))
            result = urllib.unquote_plus(given)
            self.assertEqual(expect, result, 'using unquote_plus(): %s != %s' % (expect, result))
            escape_list.append(given)

        escape_string = ''.join(escape_list)
        del escape_list
        result = urllib.unquote(escape_string)
        self.assertEqual(result.count('%'), 1, 'using quote(): not all characters escaped; %s' % result)
        result = urllib.unquote(escape_string)
        self.assertEqual(result.count('%'), 1, 'using unquote(): not all characters escaped: %s' % result)

    def test_unquoting_badpercent(self):
        given = '%xab'
        expect = given
        result = urllib.unquote(given)
        self.assertEqual(expect, result, 'using unquote(): %r != %r' % (expect, result))
        given = '%x'
        expect = given
        result = urllib.unquote(given)
        self.assertEqual(expect, result, 'using unquote(): %r != %r' % (expect, result))
        given = '%'
        expect = given
        result = urllib.unquote(given)
        self.assertEqual(expect, result, 'using unquote(): %r != %r' % (expect, result))

    def test_unquoting_mixed_case(self):
        given = '%Ab%eA'
        expect = '\xab\xea'
        result = urllib.unquote(given)
        self.assertEqual(expect, result, 'using unquote(): %r != %r' % (expect, result))

    def test_unquoting_parts(self):
        given = 'ab%sd' % hexescape('c')
        expect = 'abcd'
        result = urllib.unquote(given)
        self.assertEqual(expect, result, 'using quote(): %s != %s' % (expect, result))
        result = urllib.unquote_plus(given)
        self.assertEqual(expect, result, 'using unquote_plus(): %s != %s' % (expect, result))

    def test_unquoting_plus(self):
        given = 'are+there+spaces...'
        expect = given
        result = urllib.unquote(given)
        self.assertEqual(expect, result, 'using unquote(): %s != %s' % (expect, result))
        expect = given.replace('+', ' ')
        result = urllib.unquote_plus(given)
        self.assertEqual(expect, result, 'using unquote_plus(): %s != %s' % (expect, result))

    def test_unquote_with_unicode(self):
        r = urllib.unquote(u'br%C3%BCckner_sapporo_20050930.doc')
        self.assertEqual(r, u'br\xc3\xbcckner_sapporo_20050930.doc')


class urlencode_Tests(unittest.TestCase):
    """Tests for urlencode()"""

    def help_inputtype(self, given, test_type):
        """Helper method for testing different input types.
        
        'given' must lead to only the pairs:
            * 1st, 1
            * 2nd, 2
            * 3rd, 3
        
        Test cannot assume anything about order.  Docs make no guarantee and
        have possible dictionary input.
        
        """
        expect_somewhere = ['1st=1', '2nd=2', '3rd=3']
        result = urllib.urlencode(given)
        for expected in expect_somewhere:
            self.assertIn(expected, result, 'testing %s: %s not found in %s' % (test_type, expected, result))

        self.assertEqual(result.count('&'), 2, "testing %s: expected 2 '&'s; got %s" % (test_type, result.count('&')))
        amp_location = result.index('&')
        on_amp_left = result[amp_location - 1]
        on_amp_right = result[amp_location + 1]
        self.assertTrue(on_amp_left.isdigit() and on_amp_right.isdigit(), "testing %s: '&' not located in proper place in %s" % (test_type, result))
        self.assertEqual(len(result), 17, 'testing %s: unexpected number of characters: %s != %s' % (test_type, len(result), 17))

    def test_using_mapping(self):
        self.help_inputtype({'1st': '1',
         '2nd': '2',
         '3rd': '3'}, 'using dict as input type')

    def test_using_sequence(self):
        self.help_inputtype([('1st', '1'), ('2nd', '2'), ('3rd', '3')], 'using sequence of two-item tuples as input')

    def test_quoting(self):
        given = {'&': '='}
        expect = '%s=%s' % (hexescape('&'), hexescape('='))
        result = urllib.urlencode(given)
        self.assertEqual(expect, result)
        given = {'key name': 'A bunch of pluses'}
        expect = 'key+name=A+bunch+of+pluses'
        result = urllib.urlencode(given)
        self.assertEqual(expect, result)

    def test_doseq(self):
        given = {'sequence': ['1', '2', '3']}
        expect = 'sequence=%s' % urllib.quote_plus(str(['1', '2', '3']))
        result = urllib.urlencode(given)
        self.assertEqual(expect, result)
        result = urllib.urlencode(given, True)
        for value in given['sequence']:
            expect = 'sequence=%s' % value
            self.assertIn(expect, result)

        self.assertEqual(result.count('&'), 2, "Expected 2 '&'s, got %s" % result.count('&'))


class Pathname_Tests(unittest.TestCase):
    """Test pathname2url() and url2pathname()"""

    def test_basic(self):
        expected_path = os.path.join('parts', 'of', 'a', 'path')
        expected_url = 'parts/of/a/path'
        result = urllib.pathname2url(expected_path)
        self.assertEqual(expected_url, result, 'pathname2url() failed; %s != %s' % (result, expected_url))
        result = urllib.url2pathname(expected_url)
        self.assertEqual(expected_path, result, 'url2pathame() failed; %s != %s' % (result, expected_path))

    def test_quoting(self):
        given = os.path.join('needs', 'quot=ing', 'here')
        expect = 'needs/%s/here' % urllib.quote('quot=ing')
        result = urllib.pathname2url(given)
        self.assertEqual(expect, result, 'pathname2url() failed; %s != %s' % (expect, result))
        expect = given
        result = urllib.url2pathname(result)
        self.assertEqual(expect, result, 'url2pathname() failed; %s != %s' % (expect, result))
        given = os.path.join('make sure', 'using_quote')
        expect = '%s/using_quote' % urllib.quote('make sure')
        result = urllib.pathname2url(given)
        self.assertEqual(expect, result, 'pathname2url() failed; %s != %s' % (expect, result))
        given = 'make+sure/using_unquote'
        expect = os.path.join('make+sure', 'using_unquote')
        result = urllib.url2pathname(given)
        self.assertEqual(expect, result, 'url2pathname() failed; %s != %s' % (expect, result))

    @unittest.skipUnless(sys.platform == 'win32', 'test specific to the nturl2path library')
    def test_ntpath(self):
        given = ('/C:/', '///C:/', '/C|//')
        expect = 'C:\\'
        for url in given:
            result = urllib.url2pathname(url)
            self.assertEqual(expect, result, 'nturl2path.url2pathname() failed; %s != %s' % (expect, result))

        given = '///C|/path'
        expect = 'C:\\path'
        result = urllib.url2pathname(given)
        self.assertEqual(expect, result, 'nturl2path.url2pathname() failed; %s != %s' % (expect, result))


class Utility_Tests(unittest.TestCase):
    """Testcase to test the various utility functions in the urllib."""

    def test_splitpasswd(self):
        """Some of the password examples are not sensible, but it is added to
        confirming to RFC2617 and addressing issue4675.
        """
        self.assertEqual(('user', 'ab'), urllib.splitpasswd('user:ab'))
        self.assertEqual(('user', 'a\nb'), urllib.splitpasswd('user:a\nb'))
        self.assertEqual(('user', 'a\tb'), urllib.splitpasswd('user:a\tb'))
        self.assertEqual(('user', 'a\rb'), urllib.splitpasswd('user:a\rb'))
        self.assertEqual(('user', 'a\x0cb'), urllib.splitpasswd('user:a\x0cb'))
        self.assertEqual(('user', 'a\x0bb'), urllib.splitpasswd('user:a\x0bb'))
        self.assertEqual(('user', 'a:b'), urllib.splitpasswd('user:a:b'))
        self.assertEqual(('user', 'a b'), urllib.splitpasswd('user:a b'))
        self.assertEqual(('user 2', 'ab'), urllib.splitpasswd('user 2:ab'))
        self.assertEqual(('user+1', 'a+b'), urllib.splitpasswd('user+1:a+b'))


class URLopener_Tests(unittest.TestCase):
    """Testcase to test the open method of URLopener class."""

    def test_quoted_open(self):

        class DummyURLopener(urllib.URLopener):

            def open_spam(self, url):
                return url

        self.assertEqual(DummyURLopener().open('spam://example/ /'), '//example/%20/')
        self.assertEqual(DummyURLopener().open("spam://c:|windows%/:=&?~#+!$,;'@()*[]|/path/"), "//c:|windows%/:=&?~#+!$,;'@()*[]|/path/")


def test_main():
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', '.*urllib\\.urlopen.*Python 3.0', DeprecationWarning)
        test_support.run_unittest(urlopen_FileTests, urlopen_HttpTests, urlretrieve_FileTests, urlretrieve_HttpTests, ProxyTests, QuotingTests, UnquotingTests, urlencode_Tests, Pathname_Tests, Utility_Tests, URLopener_Tests)


if __name__ == '__main__':
    test_main()