# Embedded file name: scripts/common/Lib/test/test_robotparser.py
import unittest, StringIO, robotparser
from test import test_support
from urllib2 import urlopen, HTTPError

class RobotTestCase(unittest.TestCase):

    def __init__(self, index, parser, url, good, agent):
        unittest.TestCase.__init__(self)
        if good:
            self.str = 'RobotTest(%d, good, %s)' % (index, url)
        else:
            self.str = 'RobotTest(%d, bad, %s)' % (index, url)
        self.parser = parser
        self.url = url
        self.good = good
        self.agent = agent

    def runTest(self):
        if isinstance(self.url, tuple):
            agent, url = self.url
        else:
            url = self.url
            agent = self.agent
        if self.good:
            self.assertTrue(self.parser.can_fetch(agent, url))
        else:
            self.assertFalse(self.parser.can_fetch(agent, url))

    def __str__(self):
        return self.str


tests = unittest.TestSuite()

def RobotTest(index, robots_txt, good_urls, bad_urls, agent = 'test_robotparser'):
    lines = StringIO.StringIO(robots_txt).readlines()
    parser = robotparser.RobotFileParser()
    parser.parse(lines)
    for url in good_urls:
        tests.addTest(RobotTestCase(index, parser, url, 1, agent))

    for url in bad_urls:
        tests.addTest(RobotTestCase(index, parser, url, 0, agent))


doc = '\nUser-agent: *\nDisallow: /cyberworld/map/ # This is an infinite virtual URL space\nDisallow: /tmp/ # these will soon disappear\nDisallow: /foo.html\n'
good = ['/', '/test.html']
bad = ['/cyberworld/map/index.html', '/tmp/xxx', '/foo.html']
RobotTest(1, doc, good, bad)
doc = '\n# robots.txt for http://www.example.com/\n\nUser-agent: *\nDisallow: /cyberworld/map/ # This is an infinite virtual URL space\n\n# Cybermapper knows where to go.\nUser-agent: cybermapper\nDisallow:\n\n'
good = ['/', '/test.html', ('cybermapper', '/cyberworld/map/index.html')]
bad = ['/cyberworld/map/index.html']
RobotTest(2, doc, good, bad)
doc = '\n# go away\nUser-agent: *\nDisallow: /\n'
good = []
bad = ['/cyberworld/map/index.html', '/', '/tmp/']
RobotTest(3, doc, good, bad)
doc = '\nUser-agent: figtree\nDisallow: /tmp\nDisallow: /a%3cd.html\nDisallow: /a%2fb.html\nDisallow: /%7ejoe/index.html\n'
good = []
bad = ['/tmp',
 '/tmp.html',
 '/tmp/a.html',
 '/a%3cd.html',
 '/a%3Cd.html',
 '/a%2fb.html',
 '/~joe/index.html']
RobotTest(4, doc, good, bad, 'figtree')
RobotTest(5, doc, good, bad, 'FigTree Robot libwww-perl/5.04')
doc = '\nUser-agent: *\nDisallow: /tmp/\nDisallow: /a%3Cd.html\nDisallow: /a/b.html\nDisallow: /%7ejoe/index.html\n'
good = ['/tmp']
bad = ['/tmp/',
 '/tmp/a.html',
 '/a%3cd.html',
 '/a%3Cd.html',
 '/a/b.html',
 '/%7Ejoe/index.html']
RobotTest(6, doc, good, bad)
doc = '\nUser-Agent: *\nDisallow: /.\n'
good = ['/foo.html']
bad = []
RobotTest(7, doc, good, bad)
doc = '\nUser-agent: Googlebot\nAllow: /folder1/myfile.html\nDisallow: /folder1/\n'
good = ['/folder1/myfile.html']
bad = ['/folder1/anotherfile.html']
RobotTest(8, doc, good, bad, agent='Googlebot')
doc = '\nUser-agent: Googlebot\nDisallow: /\n\nUser-agent: Googlebot-Mobile\nAllow: /\n'
good = []
bad = ['/something.jpg']
RobotTest(9, doc, good, bad, agent='Googlebot')
good = []
bad = ['/something.jpg']
RobotTest(10, doc, good, bad, agent='Googlebot-Mobile')
doc = '\nUser-agent: Googlebot-Mobile\nAllow: /\n\nUser-agent: Googlebot\nDisallow: /\n'
good = []
bad = ['/something.jpg']
RobotTest(11, doc, good, bad, agent='Googlebot')
good = ['/something.jpg']
bad = []
RobotTest(12, doc, good, bad, agent='Googlebot-Mobile')
doc = '\nUser-agent: Googlebot\nAllow: /folder1/myfile.html\nDisallow: /folder1/\n'
good = ['/folder1/myfile.html']
bad = ['/folder1/anotherfile.html']
RobotTest(13, doc, good, bad, agent='googlebot')
doc = '\nUser-agent: *\nDisallow: /some/path?name=value\n'
good = ['/some/path']
bad = ['/some/path?name=value']
RobotTest(14, doc, good, bad)
doc = '\nUser-agent: *\nDisallow: /some/path\n\nUser-agent: *\nDisallow: /another/path\n'
good = ['/another/path']
bad = ['/some/path']
RobotTest(15, doc, good, bad)

class NetworkTestCase(unittest.TestCase):

    def testPasswordProtectedSite(self):
        test_support.requires('network')
        with test_support.transient_internet('mueblesmoraleda.com'):
            url = 'http://mueblesmoraleda.com'
            robots_url = url + '/robots.txt'
            try:
                urlopen(robots_url)
            except HTTPError as e:
                if e.code not in {401, 403}:
                    self.skipTest('%r should return a 401 or 403 HTTP error, not %r' % (robots_url, e.code))
            else:
                self.skipTest('%r should return a 401 or 403 HTTP error, not succeed' % robots_url)

            parser = robotparser.RobotFileParser()
            parser.set_url(url)
            try:
                parser.read()
            except IOError:
                self.skipTest('%s is unavailable' % url)

            self.assertEqual(parser.can_fetch('*', robots_url), False)

    def testPythonOrg(self):
        test_support.requires('network')
        with test_support.transient_internet('www.python.org'):
            parser = robotparser.RobotFileParser('http://www.python.org/robots.txt')
            parser.read()
            self.assertTrue(parser.can_fetch('*', 'http://www.python.org/robots.txt'))


def test_main():
    test_support.run_unittest(tests)
    test_support.run_unittest(NetworkTestCase)


if __name__ == '__main__':
    test_support.verbose = 1
    test_main()