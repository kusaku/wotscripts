# Embedded file name: scripts/common/Lib/test/test_netrc.py
import netrc, os, unittest, sys, textwrap
from test import test_support
temp_filename = test_support.TESTFN

class NetrcTestCase(unittest.TestCase):

    def tearDown(self):
        os.unlink(temp_filename)

    def make_nrc(self, test_data):
        test_data = textwrap.dedent(test_data)
        mode = 'w'
        if sys.platform != 'cygwin':
            mode += 't'
        with open(temp_filename, mode) as fp:
            fp.write(test_data)
        return netrc.netrc(temp_filename)

    def test_default(self):
        nrc = self.make_nrc('            machine host1.domain.com login log1 password pass1 account acct1\n            default login log2 password pass2\n            ')
        self.assertEqual(nrc.hosts['host1.domain.com'], ('log1', 'acct1', 'pass1'))
        self.assertEqual(nrc.hosts['default'], ('log2', None, 'pass2'))
        return None

    def test_macros(self):
        nrc = self.make_nrc('            macdef macro1\n            line1\n            line2\n\n            macdef macro2\n            line3\n            line4\n            ')
        self.assertEqual(nrc.macros, {'macro1': ['line1\n', 'line2\n'],
         'macro2': ['line3\n', 'line4\n']})

    def _test_passwords(self, nrc, passwd):
        nrc = self.make_nrc(nrc)
        self.assertEqual(nrc.hosts['host.domain.com'], ('log', 'acct', passwd))

    def test_password_with_leading_hash(self):
        self._test_passwords('            machine host.domain.com login log password #pass account acct\n            ', '#pass')

    def test_password_with_trailing_hash(self):
        self._test_passwords('            machine host.domain.com login log password pass# account acct\n            ', 'pass#')

    def test_password_with_internal_hash(self):
        self._test_passwords('            machine host.domain.com login log password pa#ss account acct\n            ', 'pa#ss')

    def _test_comment(self, nrc, passwd = 'pass'):
        nrc = self.make_nrc(nrc)
        self.assertEqual(nrc.hosts['foo.domain.com'], ('bar', None, passwd))
        self.assertEqual(nrc.hosts['bar.domain.com'], ('foo', None, 'pass'))
        return

    def test_comment_before_machine_line(self):
        self._test_comment('            # comment\n            machine foo.domain.com login bar password pass\n            machine bar.domain.com login foo password pass\n            ')

    def test_comment_before_machine_line_no_space(self):
        self._test_comment('            #comment\n            machine foo.domain.com login bar password pass\n            machine bar.domain.com login foo password pass\n            ')

    def test_comment_before_machine_line_hash_only(self):
        self._test_comment('            #\n            machine foo.domain.com login bar password pass\n            machine bar.domain.com login foo password pass\n            ')

    def test_comment_at_end_of_machine_line(self):
        self._test_comment('            machine foo.domain.com login bar password pass # comment\n            machine bar.domain.com login foo password pass\n            ')

    def test_comment_at_end_of_machine_line_no_space(self):
        self._test_comment('            machine foo.domain.com login bar password pass #comment\n            machine bar.domain.com login foo password pass\n            ')

    def test_comment_at_end_of_machine_line_pass_has_hash(self):
        self._test_comment('            machine foo.domain.com login bar password #pass #comment\n            machine bar.domain.com login foo password pass\n            ', '#pass')


def test_main():
    test_support.run_unittest(NetrcTestCase)


if __name__ == '__main__':
    test_main()