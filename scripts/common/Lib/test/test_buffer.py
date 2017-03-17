# Embedded file name: scripts/common/Lib/test/test_buffer.py
"""Unit tests for buffer objects.

For now, tests just new or changed functionality.

"""
import unittest
from test import test_support

class BufferTests(unittest.TestCase):

    def test_extended_getslice(self):
        s = ''.join((chr(c) for c in list(range(255, -1, -1))))
        b = buffer(s)
        indices = (0, None, 1, 3, 19, 300, -1, -2, -31, -300)
        for start in indices:
            for stop in indices:
                for step in indices[1:]:
                    self.assertEqual(b[start:stop:step], s[start:stop:step])

        return None


def test_main():
    with test_support.check_py3k_warnings(('buffer.. not supported', DeprecationWarning)):
        test_support.run_unittest(BufferTests)


if __name__ == '__main__':
    test_main()