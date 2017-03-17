# Embedded file name: scripts/common/Lib/test/test_cprofile.py
"""Test suite for the cProfile module."""
import sys
from test.test_support import run_unittest, TESTFN, unlink
import cProfile
from test.test_profile import ProfileTest, regenerate_expected_output

class CProfileTest(ProfileTest):
    profilerclass = cProfile.Profile
    expected_list_sort_output = "{method 'sort' of 'list' objects}"

    def test_bad_counter_during_dealloc(self):
        import _lsprof
        sys.stderr = open(TESTFN, 'w')
        try:
            obj = _lsprof.Profiler(lambda : int)
            obj.enable()
            obj = _lsprof.Profiler(1)
            obj.disable()
        finally:
            sys.stderr = sys.__stderr__
            unlink(TESTFN)


def test_main():
    run_unittest(CProfileTest)


def main():
    if '-r' not in sys.argv:
        test_main()
    else:
        regenerate_expected_output(__file__, CProfileTest)


CProfileTest.expected_output['print_stats'] = "         126 function calls (106 primitive calls) in 1.000 seconds\n\n   Ordered by: standard name\n\n   ncalls  tottime  percall  cumtime  percall filename:lineno(function)\n        1    0.000    0.000    1.000    1.000 <string>:1(<module>)\n       28    0.028    0.001    0.028    0.001 profilee.py:110(__getattr__)\n        1    0.270    0.270    1.000    1.000 profilee.py:25(testfunc)\n     23/3    0.150    0.007    0.170    0.057 profilee.py:35(factorial)\n       20    0.020    0.001    0.020    0.001 profilee.py:48(mul)\n        2    0.040    0.020    0.600    0.300 profilee.py:55(helper)\n        4    0.116    0.029    0.120    0.030 profilee.py:73(helper1)\n        2    0.000    0.000    0.140    0.070 profilee.py:84(helper2_indirect)\n        8    0.312    0.039    0.400    0.050 profilee.py:88(helper2)\n        8    0.064    0.008    0.080    0.010 profilee.py:98(subhelper)\n       12    0.000    0.000    0.012    0.001 {hasattr}\n        4    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}\n        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}\n        8    0.000    0.000    0.000    0.000 {range}\n        4    0.000    0.000    0.000    0.000 {sys.exc_info}\n\n\n"
CProfileTest.expected_output['print_callers'] = "   Ordered by: standard name\n\nFunction                                          was called by...\n                                                      ncalls  tottime  cumtime\n<string>:1(<module>)                              <-\nprofilee.py:110(__getattr__)                      <-      16    0.016    0.016  profilee.py:98(subhelper)\n                                                          12    0.012    0.012  {hasattr}\nprofilee.py:25(testfunc)                          <-       1    0.270    1.000  <string>:1(<module>)\nprofilee.py:35(factorial)                         <-       1    0.014    0.130  profilee.py:25(testfunc)\n                                                        20/3    0.130    0.147  profilee.py:35(factorial)\n                                                           2    0.006    0.040  profilee.py:84(helper2_indirect)\nprofilee.py:48(mul)                               <-      20    0.020    0.020  profilee.py:35(factorial)\nprofilee.py:55(helper)                            <-       2    0.040    0.600  profilee.py:25(testfunc)\nprofilee.py:73(helper1)                           <-       4    0.116    0.120  profilee.py:55(helper)\nprofilee.py:84(helper2_indirect)                  <-       2    0.000    0.140  profilee.py:55(helper)\nprofilee.py:88(helper2)                           <-       6    0.234    0.300  profilee.py:55(helper)\n                                                           2    0.078    0.100  profilee.py:84(helper2_indirect)\nprofilee.py:98(subhelper)                         <-       8    0.064    0.080  profilee.py:88(helper2)\n{hasattr}                                         <-       4    0.000    0.004  profilee.py:73(helper1)\n                                                           8    0.000    0.008  profilee.py:88(helper2)\n{method 'append' of 'list' objects}               <-       4    0.000    0.000  profilee.py:73(helper1)\n{method 'disable' of '_lsprof.Profiler' objects}  <-\n{range}                                           <-       8    0.000    0.000  profilee.py:98(subhelper)\n{sys.exc_info}                                    <-       4    0.000    0.000  profilee.py:73(helper1)\n\n\n"
CProfileTest.expected_output['print_callees'] = "   Ordered by: standard name\n\nFunction                                          called...\n                                                      ncalls  tottime  cumtime\n<string>:1(<module>)                              ->       1    0.270    1.000  profilee.py:25(testfunc)\nprofilee.py:110(__getattr__)                      ->\nprofilee.py:25(testfunc)                          ->       1    0.014    0.130  profilee.py:35(factorial)\n                                                           2    0.040    0.600  profilee.py:55(helper)\nprofilee.py:35(factorial)                         ->    20/3    0.130    0.147  profilee.py:35(factorial)\n                                                          20    0.020    0.020  profilee.py:48(mul)\nprofilee.py:48(mul)                               ->\nprofilee.py:55(helper)                            ->       4    0.116    0.120  profilee.py:73(helper1)\n                                                           2    0.000    0.140  profilee.py:84(helper2_indirect)\n                                                           6    0.234    0.300  profilee.py:88(helper2)\nprofilee.py:73(helper1)                           ->       4    0.000    0.004  {hasattr}\n                                                           4    0.000    0.000  {method 'append' of 'list' objects}\n                                                           4    0.000    0.000  {sys.exc_info}\nprofilee.py:84(helper2_indirect)                  ->       2    0.006    0.040  profilee.py:35(factorial)\n                                                           2    0.078    0.100  profilee.py:88(helper2)\nprofilee.py:88(helper2)                           ->       8    0.064    0.080  profilee.py:98(subhelper)\n                                                           8    0.000    0.008  {hasattr}\nprofilee.py:98(subhelper)                         ->      16    0.016    0.016  profilee.py:110(__getattr__)\n                                                           8    0.000    0.000  {range}\n{hasattr}                                         ->      12    0.012    0.012  profilee.py:110(__getattr__)\n{method 'append' of 'list' objects}               ->\n{method 'disable' of '_lsprof.Profiler' objects}  ->\n{range}                                           ->\n{sys.exc_info}                                    ->\n\n\n"
if __name__ == '__main__':
    main()