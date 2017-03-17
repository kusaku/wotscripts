# Embedded file name: scripts/common/Lib/test/test_nis.py
from test import test_support
import unittest
nis = test_support.import_module('nis')

class NisTests(unittest.TestCase):

    def test_maps(self):
        try:
            maps = nis.maps()
        except nis.error as msg:
            if test_support.verbose:
                print 'Test Skipped:', msg
            return

        try:
            maps.remove('passwd.adjunct.byname')
        except ValueError:
            pass

        done = 0
        for nismap in maps:
            mapping = nis.cat(nismap)
            for k, v in mapping.items():
                if not k:
                    continue
                if nis.match(k, nismap) != v:
                    self.fail("NIS match failed for key `%s' in map `%s'" % (k, nismap))
                else:
                    done = 1
                    break

            if done:
                break


def test_main():
    test_support.run_unittest(NisTests)


if __name__ == '__main__':
    test_main()