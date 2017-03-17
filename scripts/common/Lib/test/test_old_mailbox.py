# Embedded file name: scripts/common/Lib/test/test_old_mailbox.py
import mailbox
import os
import time
import unittest
from test import test_support
try:
    os.unlink(test_support.TESTFN)
except os.error:
    pass

FROM_ = 'From some.body@dummy.domain  Sat Jul 24 13:43:35 2004\n'
DUMMY_MESSAGE = 'From: some.body@dummy.domain\nTo: me@my.domain\nSubject: Simple Test\n\nThis is a dummy message.\n'

class MaildirTestCase(unittest.TestCase):

    def setUp(self):
        self._dir = test_support.TESTFN
        os.mkdir(self._dir)
        os.mkdir(os.path.join(self._dir, 'cur'))
        os.mkdir(os.path.join(self._dir, 'tmp'))
        os.mkdir(os.path.join(self._dir, 'new'))
        self._counter = 1
        self._msgfiles = []

    def tearDown(self):
        map(os.unlink, self._msgfiles)
        os.rmdir(os.path.join(self._dir, 'cur'))
        os.rmdir(os.path.join(self._dir, 'tmp'))
        os.rmdir(os.path.join(self._dir, 'new'))
        os.rmdir(self._dir)

    def createMessage(self, dir, mbox = False):
        t = int(time.time() % 1000000)
        pid = self._counter
        self._counter += 1
        filename = os.extsep.join((str(t),
         str(pid),
         'myhostname',
         'mydomain'))
        tmpname = os.path.join(self._dir, 'tmp', filename)
        newname = os.path.join(self._dir, dir, filename)
        with open(tmpname, 'w') as fp:
            self._msgfiles.append(tmpname)
            if mbox:
                fp.write(FROM_)
            fp.write(DUMMY_MESSAGE)
        if hasattr(os, 'link'):
            os.link(tmpname, newname)
        else:
            with open(newname, 'w') as fp:
                fp.write(DUMMY_MESSAGE)
        self._msgfiles.append(newname)
        return tmpname

    def test_empty_maildir(self):
        """Test an empty maildir mailbox"""
        self.mbox = mailbox.Maildir(test_support.TESTFN)
        self.assertTrue(len(self.mbox) == 0)
        self.assertTrue(self.mbox.next() is None)
        self.assertTrue(self.mbox.next() is None)
        return

    def test_nonempty_maildir_cur(self):
        self.createMessage('cur')
        self.mbox = mailbox.Maildir(test_support.TESTFN)
        self.assertTrue(len(self.mbox) == 1)
        self.assertTrue(self.mbox.next() is not None)
        self.assertTrue(self.mbox.next() is None)
        self.assertTrue(self.mbox.next() is None)
        return

    def test_nonempty_maildir_new(self):
        self.createMessage('new')
        self.mbox = mailbox.Maildir(test_support.TESTFN)
        self.assertTrue(len(self.mbox) == 1)
        self.assertTrue(self.mbox.next() is not None)
        self.assertTrue(self.mbox.next() is None)
        self.assertTrue(self.mbox.next() is None)
        return

    def test_nonempty_maildir_both(self):
        self.createMessage('cur')
        self.createMessage('new')
        self.mbox = mailbox.Maildir(test_support.TESTFN)
        self.assertTrue(len(self.mbox) == 2)
        self.assertTrue(self.mbox.next() is not None)
        self.assertTrue(self.mbox.next() is not None)
        self.assertTrue(self.mbox.next() is None)
        self.assertTrue(self.mbox.next() is None)
        return

    def test_unix_mbox(self):
        import email.parser
        fname = self.createMessage('cur', True)
        n = 0
        with open(fname) as f:
            for msg in mailbox.PortableUnixMailbox(f, email.parser.Parser().parse):
                n += 1
                self.assertEqual(msg['subject'], 'Simple Test')
                self.assertEqual(len(str(msg)), len(FROM_) + len(DUMMY_MESSAGE))

        self.assertEqual(n, 1)


class MboxTestCase(unittest.TestCase):

    def setUp(self):
        self._path = test_support.TESTFN

    def tearDown(self):
        os.unlink(self._path)

    def test_from_regex(self):
        with open(self._path, 'w') as f:
            f.write('From fred@example.com Mon May 31 13:24:50 2004 +0200\nSubject: message 1\n\nbody1\nFrom fred@example.com Mon May 31 13:24:50 2004 -0200\nSubject: message 2\n\nbody2\nFrom fred@example.com Mon May 31 13:24:50 2004\nSubject: message 3\n\nbody3\nFrom fred@example.com Mon May 31 13:24:50 2004\nSubject: message 4\n\nbody4\n')
        with open(self._path, 'r') as f:
            box = mailbox.UnixMailbox(f)
            self.assertTrue(len(list(iter(box))) == 4)


def test_main():
    test_support.run_unittest(MaildirTestCase, MboxTestCase)


if __name__ == '__main__':
    test_main()