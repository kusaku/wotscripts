# Embedded file name: scripts/common/Lib/test/test_urllib2net.py
import unittest
from test import test_support
from test.test_urllib2 import sanepathname2url
import socket
import urllib2
import os
import sys
TIMEOUT = 60

def _retry_thrice(func, exc, *args, **kwargs):
    for i in range(3):
        try:
            return func(*args, **kwargs)
        except exc as last_exc:
            continue
        except:
            raise

    raise last_exc


def _wrap_with_retry_thrice(func, exc):

    def wrapped(*args, **kwargs):
        return _retry_thrice(func, exc, *args, **kwargs)

    return wrapped


_urlopen_with_retry = _wrap_with_retry_thrice(urllib2.urlopen, urllib2.URLError)

class AuthTests(unittest.TestCase):
    """Tests urllib2 authentication features."""
    pass


class CloseSocketTest(unittest.TestCase):

    def test_close(self):
        import httplib
        response = _urlopen_with_retry('http://www.python.org/')
        abused_fileobject = response.fp
        self.assertTrue(abused_fileobject.__class__ is socket._fileobject)
        httpresponse = abused_fileobject._sock
        self.assertTrue(httpresponse.__class__ is httplib.HTTPResponse)
        fileobject = httpresponse.fp
        self.assertTrue(fileobject.__class__ is socket._fileobject)
        self.assertTrue(not fileobject.closed)
        response.close()
        self.assertTrue(fileobject.closed)


class OtherNetworkTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_ftp(self):
        urls = ['ftp://ftp.kernel.org/pub/linux/kernel/README', 'ftp://ftp.kernel.org/pub/linux/kernel/non-existent-file', 'ftp://gatekeeper.research.compaq.com/pub/DEC/SRC/research-reports/00README-Legal-Rules-Regs']
        self._test_urls(urls, self._extra_handlers())

    def test_file(self):
        TESTFN = test_support.TESTFN
        f = open(TESTFN, 'w')
        try:
            f.write('hi there\n')
            f.close()
            urls = ['file:' + sanepathname2url(os.path.abspath(TESTFN)), ('file:///nonsensename/etc/passwd', None, urllib2.URLError)]
            self._test_urls(urls, self._extra_handlers(), retry=True)
        finally:
            os.remove(TESTFN)

        self.assertRaises(ValueError, urllib2.urlopen, './relative_path/to/file')
        return

    def test_urlwithfrag(self):
        urlwith_frag = 'http://docs.python.org/glossary.html#glossary'
        with test_support.transient_internet(urlwith_frag):
            req = urllib2.Request(urlwith_frag)
            res = urllib2.urlopen(req)
            self.assertEqual(res.geturl(), 'http://docs.python.org/glossary.html#glossary')

    def test_fileno(self):
        req = urllib2.Request('http://www.python.org')
        opener = urllib2.build_opener()
        res = opener.open(req)
        try:
            res.fileno()
        except AttributeError:
            self.fail('HTTPResponse object should return a valid fileno')
        finally:
            res.close()

    def test_custom_headers(self):
        url = 'http://www.example.com'
        with test_support.transient_internet(url):
            opener = urllib2.build_opener()
            request = urllib2.Request(url)
            self.assertFalse(request.header_items())
            opener.open(request)
            self.assertTrue(request.header_items())
            self.assertTrue(request.has_header('User-agent'))
            request.add_header('User-Agent', 'Test-Agent')
            opener.open(request)
            self.assertEqual(request.get_header('User-agent'), 'Test-Agent')

    def test_sites_no_connection_close(self):
        URL = 'http://www.imdb.com'
        with test_support.transient_internet(URL):
            req = urllib2.urlopen(URL)
            res = req.read()
            self.assertTrue(res)

    def _test_urls(self, urls, handlers, retry = True):
        import time
        import logging
        debug = logging.getLogger('test_urllib2').debug
        urlopen = urllib2.build_opener(*handlers).open
        if retry:
            urlopen = _wrap_with_retry_thrice(urlopen, urllib2.URLError)
        for url in urls:
            if isinstance(url, tuple):
                url, req, expected_err = url
            else:
                req = expected_err = None
            with test_support.transient_internet(url):
                debug(url)
                try:
                    f = urlopen(url, req, TIMEOUT)
                except EnvironmentError as err:
                    debug(err)
                    if expected_err:
                        msg = "Didn't get expected error(s) %s for %s %s, got %s: %s" % (expected_err,
                         url,
                         req,
                         type(err),
                         err)
                        self.assertIsInstance(err, expected_err, msg)
                except urllib2.URLError as err:
                    if isinstance(err[0], socket.timeout):
                        print >> sys.stderr, '<timeout: %s>' % url
                        continue
                    else:
                        raise
                else:
                    try:
                        with test_support.transient_internet(url):
                            buf = f.read()
                            debug('read %d bytes' % len(buf))
                    except socket.timeout:
                        print >> sys.stderr, '<timeout: %s>' % url

                    f.close()

            debug('******** next url coming up...')
            time.sleep(0.1)

        return

    def _extra_handlers(self):
        handlers = []
        cfh = urllib2.CacheFTPHandler()
        self.addCleanup(cfh.clear_cache)
        cfh.setTimeout(1)
        handlers.append(cfh)
        return handlers


class TimeoutTest(unittest.TestCase):

    def test_http_basic(self):
        self.assertTrue(socket.getdefaulttimeout() is None)
        url = 'http://www.python.org'
        with test_support.transient_internet(url, timeout=None):
            u = _urlopen_with_retry(url)
            self.assertTrue(u.fp._sock.fp._sock.gettimeout() is None)
        return

    def test_http_default_timeout(self):
        self.assertTrue(socket.getdefaulttimeout() is None)
        url = 'http://www.python.org'
        with test_support.transient_internet(url):
            socket.setdefaulttimeout(60)
            try:
                u = _urlopen_with_retry(url)
            finally:
                socket.setdefaulttimeout(None)

            self.assertEqual(u.fp._sock.fp._sock.gettimeout(), 60)
        return

    def test_http_no_timeout(self):
        self.assertTrue(socket.getdefaulttimeout() is None)
        url = 'http://www.python.org'
        with test_support.transient_internet(url):
            socket.setdefaulttimeout(60)
            try:
                u = _urlopen_with_retry(url, timeout=None)
            finally:
                socket.setdefaulttimeout(None)

            self.assertTrue(u.fp._sock.fp._sock.gettimeout() is None)
        return

    def test_http_timeout(self):
        url = 'http://www.python.org'
        with test_support.transient_internet(url):
            u = _urlopen_with_retry(url, timeout=120)
            self.assertEqual(u.fp._sock.fp._sock.gettimeout(), 120)

    FTP_HOST = 'ftp://ftp.mirror.nl/pub/gnu/'

    def test_ftp_basic(self):
        self.assertTrue(socket.getdefaulttimeout() is None)
        with test_support.transient_internet(self.FTP_HOST, timeout=None):
            u = _urlopen_with_retry(self.FTP_HOST)
            self.assertTrue(u.fp.fp._sock.gettimeout() is None)
        return

    def test_ftp_default_timeout(self):
        self.assertTrue(socket.getdefaulttimeout() is None)
        with test_support.transient_internet(self.FTP_HOST):
            socket.setdefaulttimeout(60)
            try:
                u = _urlopen_with_retry(self.FTP_HOST)
            finally:
                socket.setdefaulttimeout(None)

            self.assertEqual(u.fp.fp._sock.gettimeout(), 60)
        return

    def test_ftp_no_timeout(self):
        self.assertTrue(socket.getdefaulttimeout() is None)
        with test_support.transient_internet(self.FTP_HOST):
            socket.setdefaulttimeout(60)
            try:
                u = _urlopen_with_retry(self.FTP_HOST, timeout=None)
            finally:
                socket.setdefaulttimeout(None)

            self.assertTrue(u.fp.fp._sock.gettimeout() is None)
        return

    def test_ftp_timeout(self):
        with test_support.transient_internet(self.FTP_HOST):
            u = _urlopen_with_retry(self.FTP_HOST, timeout=60)
            self.assertEqual(u.fp.fp._sock.gettimeout(), 60)


def test_main():
    test_support.requires('network')
    test_support.run_unittest(AuthTests, OtherNetworkTests, CloseSocketTest, TimeoutTest)


if __name__ == '__main__':
    test_main()