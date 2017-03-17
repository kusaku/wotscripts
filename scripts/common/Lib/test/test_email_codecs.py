# Embedded file name: scripts/common/Lib/test/test_email_codecs.py
from email.test import test_email_codecs
from email.test import test_email_codecs_renamed
from test import test_support

def test_main():
    suite = test_email_codecs.suite()
    suite.addTest(test_email_codecs_renamed.suite())
    test_support.run_unittest(suite)


if __name__ == '__main__':
    test_main()