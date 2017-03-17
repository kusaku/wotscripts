# Embedded file name: scripts/common/Lib/test/test_quopri.py
from test import test_support
import unittest
import sys, cStringIO, subprocess
import quopri
ENCSAMPLE = "Here's a bunch of special=20\n\n=A1=A2=A3=A4=A5=A6=A7=A8=A9\n=AA=AB=AC=AD=AE=AF=B0=B1=B2=B3\n=B4=B5=B6=B7=B8=B9=BA=BB=BC=BD=BE\n=BF=C0=C1=C2=C3=C4=C5=C6\n=C7=C8=C9=CA=CB=CC=CD=CE=CF\n=D0=D1=D2=D3=D4=D5=D6=D7\n=D8=D9=DA=DB=DC=DD=DE=DF\n=E0=E1=E2=E3=E4=E5=E6=E7\n=E8=E9=EA=EB=EC=ED=EE=EF\n=F0=F1=F2=F3=F4=F5=F6=F7\n=F8=F9=FA=FB=FC=FD=FE=FF\n\ncharacters... have fun!\n"
DECSAMPLE = "Here's a bunch of special \n" + '\n\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\n\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\n\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\n\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\n\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\n\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\n\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\n\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\n\xe8\xe9\xea\xeb\xec\xed\xee\xef\n\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\n\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff\n\ncharacters... have fun!\n'

def withpythonimplementation(testfunc):

    def newtest(self):
        testfunc(self)
        if quopri.b2a_qp is not None or quopri.a2b_qp is not None:
            oldencode = quopri.b2a_qp
            olddecode = quopri.a2b_qp
            try:
                quopri.b2a_qp = None
                quopri.a2b_qp = None
                testfunc(self)
            finally:
                quopri.b2a_qp = oldencode
                quopri.a2b_qp = olddecode

        return

    newtest.__name__ = testfunc.__name__
    return newtest


class QuopriTestCase(unittest.TestCase):
    STRINGS = (('hello', 'hello'),
     ('hello\n        there\n        world', 'hello\n        there\n        world'),
     ('hello\n        there\n        world\n', 'hello\n        there\n        world\n'),
     ('\x81\x82\x83', '=81=82=83'),
     ('hello ', 'hello=20'),
     ('hello\t', 'hello=09'),
     ('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\xd8\xd9\xda\xdb\xdc\xdd\xde\xdfxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=D8=D9=DA=DB=DC=DD=DE=DFx=\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'),
     ('yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy', 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'),
     ('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz', 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz=\nzz'),
     ('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz', 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz=\nzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'),
     ('yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy\nzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz', 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=\nyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy\nzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'),
     (DECSAMPLE, ENCSAMPLE))
    ESTRINGS = (('hello world', 'hello=20world'), ('hello\tworld', 'hello=09world'))
    HSTRINGS = (('hello world', 'hello_world'), ('hello_world', 'hello=5Fworld'))

    @withpythonimplementation
    def test_encodestring(self):
        for p, e in self.STRINGS:
            self.assertTrue(quopri.encodestring(p) == e)

    @withpythonimplementation
    def test_decodestring(self):
        for p, e in self.STRINGS:
            self.assertTrue(quopri.decodestring(e) == p)

    @withpythonimplementation
    def test_idempotent_string(self):
        for p, e in self.STRINGS:
            self.assertTrue(quopri.decodestring(quopri.encodestring(e)) == e)

    @withpythonimplementation
    def test_encode(self):
        for p, e in self.STRINGS:
            infp = cStringIO.StringIO(p)
            outfp = cStringIO.StringIO()
            quopri.encode(infp, outfp, quotetabs=False)
            self.assertTrue(outfp.getvalue() == e)

    @withpythonimplementation
    def test_decode(self):
        for p, e in self.STRINGS:
            infp = cStringIO.StringIO(e)
            outfp = cStringIO.StringIO()
            quopri.decode(infp, outfp)
            self.assertTrue(outfp.getvalue() == p)

    @withpythonimplementation
    def test_embedded_ws(self):
        for p, e in self.ESTRINGS:
            self.assertTrue(quopri.encodestring(p, quotetabs=True) == e)
            self.assertTrue(quopri.decodestring(e) == p)

    @withpythonimplementation
    def test_encode_header(self):
        for p, e in self.HSTRINGS:
            self.assertTrue(quopri.encodestring(p, header=True) == e)

    @withpythonimplementation
    def test_decode_header(self):
        for p, e in self.HSTRINGS:
            self.assertTrue(quopri.decodestring(e, header=True) == p)

    def test_scriptencode(self):
        p, e = self.STRINGS[-1]
        process = subprocess.Popen([sys.executable, '-mquopri'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.addCleanup(process.stdout.close)
        cout, cerr = process.communicate(p)
        self.assertEqual(cout.splitlines(), e.splitlines())

    def test_scriptdecode(self):
        p, e = self.STRINGS[-1]
        process = subprocess.Popen([sys.executable, '-mquopri', '-d'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.addCleanup(process.stdout.close)
        cout, cerr = process.communicate(e)
        self.assertEqual(cout.splitlines(), p.splitlines())


def test_main():
    test_support.run_unittest(QuopriTestCase)


if __name__ == '__main__':
    test_main()