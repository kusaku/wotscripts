# Embedded file name: scripts/common/Lib/test/test_resource.py
import unittest
from test import test_support
import time
resource = test_support.import_module('resource')

class ResourceTest(unittest.TestCase):

    def test_args(self):
        self.assertRaises(TypeError, resource.getrlimit)
        self.assertRaises(TypeError, resource.getrlimit, 42, 42)
        self.assertRaises(TypeError, resource.setrlimit)
        self.assertRaises(TypeError, resource.setrlimit, 42, 42, 42)

    def test_fsize_ismax(self):
        try:
            cur, max = resource.getrlimit(resource.RLIMIT_FSIZE)
        except AttributeError:
            pass
        else:
            self.assertEqual(resource.RLIM_INFINITY, max)
            resource.setrlimit(resource.RLIMIT_FSIZE, (cur, max))

    def test_fsize_enforced(self):
        try:
            cur, max = resource.getrlimit(resource.RLIMIT_FSIZE)
        except AttributeError:
            pass
        else:
            try:
                try:
                    resource.setrlimit(resource.RLIMIT_FSIZE, (1024, max))
                    limit_set = True
                except ValueError:
                    limit_set = False

                f = open(test_support.TESTFN, 'wb')
                try:
                    f.write('X' * 1024)
                    try:
                        f.write('Y')
                        f.flush()
                        for i in range(5):
                            time.sleep(0.1)
                            f.flush()

                    except IOError:
                        if not limit_set:
                            raise

                    if limit_set:
                        resource.setrlimit(resource.RLIMIT_FSIZE, (cur, max))
                finally:
                    f.close()

            finally:
                if limit_set:
                    resource.setrlimit(resource.RLIMIT_FSIZE, (cur, max))
                test_support.unlink(test_support.TESTFN)

    def test_fsize_toobig(self):
        too_big = 100000000000000000000000000000000000000000000000000L
        try:
            cur, max = resource.getrlimit(resource.RLIMIT_FSIZE)
        except AttributeError:
            pass
        else:
            try:
                resource.setrlimit(resource.RLIMIT_FSIZE, (too_big, max))
            except (OverflowError, ValueError):
                pass

            try:
                resource.setrlimit(resource.RLIMIT_FSIZE, (max, too_big))
            except (OverflowError, ValueError):
                pass

    def test_getrusage(self):
        self.assertRaises(TypeError, resource.getrusage)
        self.assertRaises(TypeError, resource.getrusage, 42, 42)
        usageself = resource.getrusage(resource.RUSAGE_SELF)
        usagechildren = resource.getrusage(resource.RUSAGE_CHILDREN)
        try:
            usageboth = resource.getrusage(resource.RUSAGE_BOTH)
        except (ValueError, AttributeError):
            pass


def test_main(verbose = None):
    test_support.run_unittest(ResourceTest)


if __name__ == '__main__':
    test_main()