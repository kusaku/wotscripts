# Embedded file name: scripts/common/Lib/test/test_email_renamed.py
from email.test.test_email_renamed import suite
from test import test_support

def test_main():
    test_support.run_unittest(suite())


if __name__ == '__main__':
    test_main()