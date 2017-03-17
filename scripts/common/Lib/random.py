# Embedded file name: scripts/common/Lib/random.py
"""Random variable generators.

    integers
    --------
           uniform within range

    sequences
    ---------
           pick random element
           pick random sample
           generate random permutation

    distributions on the real line:
    ------------------------------
           uniform
           triangular
           normal (Gaussian)
           lognormal
           negative exponential
           gamma
           beta
           pareto
           Weibull

    distributions on the circle (angles 0 to 2pi)
    ---------------------------------------------
           circular uniform
           von Mises

General notes on the underlying Mersenne Twister core generator:

* The period is 2**19937-1.
* It is one of the most extensively tested generators in existence.
* Without a direct way to compute N steps forward, the semantics of
  jumpahead(n) are weakened to simply jump to another distant state and rely
  on the large period to avoid overlapping sequences.
* The random() method is implemented in C, executes in a single Python step,
  and is, therefore, threadsafe.

"""
from __future__ import division
from warnings import warn as _warn
from types import MethodType as _MethodType, BuiltinMethodType as _BuiltinMethodType
from math import log as _log, exp as _exp, pi as _pi, e as _e, ceil as _ceil
from math import sqrt as _sqrt, acos as _acos, cos as _cos, sin as _sin
from os import urandom as _urandom
from binascii import hexlify as _hexlify
import hashlib as _hashlib
__all__ = ['Random',
 'seed',
 'random',
 'uniform',
 'randint',
 'choice',
 'sample',
 'randrange',
 'shuffle',
 'normalvariate',
 'lognormvariate',
 'expovariate',
 'vonmisesvariate',
 'gammavariate',
 'triangular',
 'gauss',
 'betavariate',
 'paretovariate',
 'weibullvariate',
 'getstate',
 'setstate',
 'jumpahead',
 'WichmannHill',
 'getrandbits',
 'SystemRandom']
NV_MAGICCONST = 4 * _exp(-0.5) / _sqrt(2.0)
TWOPI = 2.0 * _pi
LOG4 = _log(4.0)
SG_MAGICCONST = 1.0 + _log(4.5)
BPF = 53
RECIP_BPF = 2 ** (-BPF)
import _random

class Random(_random.Random):
    """Random number generator base class used by bound module functions.
    
    Used to instantiate instances of Random to get generators that don't
    share state.  Especially useful for multi-threaded programs, creating
    a different instance of Random for each thread, and using the jumpahead()
    method to ensure that the generated sequences seen by each thread don't
    overlap.
    
    Class Random can also be subclassed if you want to use a different basic
    generator of your own devising: in that case, override the following
    methods: random(), seed(), getstate(), setstate() and jumpahead().
    Optionally, implement a getrandbits() method so that randrange() can cover
    arbitrarily large ranges.
    
    """
    VERSION = 3

    def __init__(self, x = None):
        """Initialize an instance.
        
        Optional argument x controls seeding, as for Random.seed().
        """
        self.seed(x)
        self.gauss_next = None
        return

    def seed(self, a = None):
        """Initialize internal state from hashable object.
        
        None or no argument seeds from current time or from an operating
        system specific randomness source if available.
        
        If a is not None or an int or long, hash(a) is used instead.
        """
        if a is None:
            try:
                a = long(_hexlify(_urandom(16)), 16)
            except NotImplementedError:
                import time
                a = long(time.time() * 256)

        super(Random, self).seed(a)
        self.gauss_next = None
        return

    def getstate(self):
        """Return internal state; can be passed to setstate() later."""
        return (self.VERSION, super(Random, self).getstate(), self.gauss_next)

    def setstate(self, state):
        """Restore internal state from object returned by getstate()."""
        version = state[0]
        if version == 3:
            version, internalstate, self.gauss_next = state
            super(Random, self).setstate(internalstate)
        elif version == 2:
            version, internalstate, self.gauss_next = state
            try:
                internalstate = tuple((long(x) % 4294967296L for x in internalstate))
            except ValueError as e:
                raise TypeError, e

            super(Random, self).setstate(internalstate)
        else:
            raise ValueError('state with version %s passed to Random.setstate() of version %s' % (version, self.VERSION))

    def jumpahead(self, n):
        """Change the internal state to one that is likely far away
        from the current state.  This method will not be in Py3.x,
        so it is better to simply reseed.
        """
        s = repr(n) + repr(self.getstate())
        n = int(_hashlib.new('sha512', s).hexdigest(), 16)
        super(Random, self).jumpahead(n)

    def __getstate__(self):
        return self.getstate()

    def __setstate__(self, state):
        self.setstate(state)

    def __reduce__(self):
        return (self.__class__, (), self.getstate())

    def randrange(self, start, stop = None, step = 1, int = int, default = None, maxwidth = 1L << BPF):
        """Choose a random item from range(start, stop[, step]).
        
        This fixes the problem with randint() which includes the
        endpoint; in Python this is usually not what you want.
        Do not supply the 'int', 'default', and 'maxwidth' arguments.
        """
        istart = int(start)
        if istart != start:
            raise ValueError, 'non-integer arg 1 for randrange()'
        if stop is default:
            if istart > 0:
                if istart >= maxwidth:
                    return self._randbelow(istart)
                return int(self.random() * istart)
            raise ValueError, 'empty range for randrange()'
        istop = int(stop)
        if istop != stop:
            raise ValueError, 'non-integer stop for randrange()'
        width = istop - istart
        if step == 1 and width > 0:
            if width >= maxwidth:
                return int(istart + self._randbelow(width))
            return int(istart + int(self.random() * width))
        if step == 1:
            raise ValueError, 'empty range for randrange() (%d,%d, %d)' % (istart, istop, width)
        istep = int(step)
        if istep != step:
            raise ValueError, 'non-integer step for randrange()'
        if istep > 0:
            n = (width + istep - 1) // istep
        elif istep < 0:
            n = (width + istep + 1) // istep
        else:
            raise ValueError, 'zero step for randrange()'
        if n <= 0:
            raise ValueError, 'empty range for randrange()'
        if n >= maxwidth:
            return istart + istep * self._randbelow(n)
        return istart + istep * int(self.random() * n)

    def randint(self, a, b):
        """Return random integer in range [a, b], including both end points.
        """
        return self.randrange(a, b + 1)

    def _randbelow(self, n, _log = _log, int = int, _maxwidth = 1L << BPF, _Method = _MethodType, _BuiltinMethod = _BuiltinMethodType):
        """Return a random int in the range [0,n)
        
        Handles the case where n has more bits than returned
        by a single call to the underlying generator.
        """
        try:
            getrandbits = self.getrandbits
        except AttributeError:
            pass
        else:
            if type(self.random) is _BuiltinMethod or type(getrandbits) is _Method:
                k = int(1.00001 + _log(n - 1, 2.0))
                r = getrandbits(k)
                while r >= n:
                    r = getrandbits(k)

                return r

        if n >= _maxwidth:
            _warn('Underlying random() generator does not supply \nenough bits to choose from a population range this large')
        return int(self.random() * n)

    def choice(self, seq):
        """Choose a random element from a non-empty sequence."""
        return seq[int(self.random() * len(seq))]

    def shuffle(self, x, random = None, int = int):
        """x, random=random.random -> shuffle list x in place; return None.
        
        Optional arg random is a 0-argument function returning a random
        float in [0.0, 1.0); by default, the standard random.random.
        """
        if random is None:
            random = self.random
        for i in reversed(xrange(1, len(x))):
            j = int(random() * (i + 1))
            x[i], x[j] = x[j], x[i]

        return

    def sample(self, population, k):
        """Chooses k unique random elements from a population sequence.
        
        Returns a new list containing elements from the population while
        leaving the original population unchanged.  The resulting list is
        in selection order so that all sub-slices will also be valid random
        samples.  This allows raffle winners (the sample) to be partitioned
        into grand prize and second place winners (the subslices).
        
        Members of the population need not be hashable or unique.  If the
        population contains repeats, then each occurrence is a possible
        selection in the sample.
        
        To choose a sample in a range of integers, use xrange as an argument.
        This is especially fast and space efficient for sampling from a
        large population:   sample(xrange(10000000), 60)
        """
        n = len(population)
        if not 0 <= k <= n:
            raise ValueError('sample larger than population')
        random = self.random
        _int = int
        result = [None] * k
        setsize = 21
        if k > 5:
            setsize += 4 ** _ceil(_log(k * 3, 4))
        if n <= setsize or hasattr(population, 'keys'):
            pool = list(population)
            for i in xrange(k):
                j = _int(random() * (n - i))
                result[i] = pool[j]
                pool[j] = pool[n - i - 1]

        else:
            try:
                selected = set()
                selected_add = selected.add
                for i in xrange(k):
                    j = _int(random() * n)
                    while j in selected:
                        j = _int(random() * n)

                    selected_add(j)
                    result[i] = population[j]

            except (TypeError, KeyError):
                if isinstance(population, list):
                    raise
                return self.sample(tuple(population), k)

        return result

    def uniform(self, a, b):
        """Get a random number in the range [a, b) or [a, b] depending on rounding."""
        return a + (b - a) * self.random()

    def triangular(self, low = 0.0, high = 1.0, mode = None):
        """Triangular distribution.
        
        Continuous distribution bounded by given lower and upper limits,
        and having a given mode value in-between.
        
        http://en.wikipedia.org/wiki/Triangular_distribution
        
        """
        u = self.random()
        c = 0.5 if mode is None else (mode - low) / (high - low)
        if u > c:
            u = 1.0 - u
            c = 1.0 - c
            low, high = high, low
        return low + (high - low) * (u * c) ** 0.5

    def normalvariate--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'random'
6	STORE_FAST        'random'

9	SETUP_LOOP        '93'

12	LOAD_FAST         'random'
15	CALL_FUNCTION_0   None
18	STORE_FAST        'u1'

21	LOAD_CONST        1.0
24	LOAD_FAST         'random'
27	CALL_FUNCTION_0   None
30	BINARY_SUBTRACT   None
31	STORE_FAST        'u2'

34	LOAD_GLOBAL       'NV_MAGICCONST'
37	LOAD_FAST         'u1'
40	LOAD_CONST        0.5
43	BINARY_SUBTRACT   None
44	BINARY_MULTIPLY   None
45	LOAD_FAST         'u2'
48	BINARY_TRUE_DIVIDE None
49	STORE_FAST        'z'

52	LOAD_FAST         'z'
55	LOAD_FAST         'z'
58	BINARY_MULTIPLY   None
59	LOAD_CONST        4.0
62	BINARY_TRUE_DIVIDE None
63	STORE_FAST        'zz'

66	LOAD_FAST         'zz'
69	LOAD_GLOBAL       '_log'
72	LOAD_FAST         'u2'
75	CALL_FUNCTION_1   None
78	UNARY_NEGATIVE    None
79	COMPARE_OP        '<='
82	POP_JUMP_IF_FALSE '12'

85	BREAK_LOOP        None
86	JUMP_BACK         '12'
89	JUMP_BACK         '12'
92	POP_BLOCK         None
93_0	COME_FROM         '9'

93	LOAD_FAST         'mu'
96	LOAD_FAST         'z'
99	LOAD_FAST         'sigma'
102	BINARY_MULTIPLY   None
103	BINARY_ADD        None
104	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 92

    def lognormvariate(self, mu, sigma):
        """Log normal distribution.
        
        If you take the natural logarithm of this distribution, you'll get a
        normal distribution with mean mu and standard deviation sigma.
        mu can have any value, and sigma must be greater than zero.
        
        """
        return _exp(self.normalvariate(mu, sigma))

    def expovariate(self, lambd):
        """Exponential distribution.
        
        lambd is 1.0 divided by the desired mean.  It should be
        nonzero.  (The parameter would be called "lambda", but that is
        a reserved word in Python.)  Returned values range from 0 to
        positive infinity if lambd is positive, and from negative
        infinity to 0 if lambd is negative.
        
        """
        return -_log(1.0 - self.random()) / lambd

    def vonmisesvariate--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'random'
6	STORE_FAST        'random'

9	LOAD_FAST         'kappa'
12	LOAD_CONST        1e-06
15	COMPARE_OP        '<='
18	POP_JUMP_IF_FALSE '32'

21	LOAD_GLOBAL       'TWOPI'
24	LOAD_FAST         'random'
27	CALL_FUNCTION_0   None
30	BINARY_MULTIPLY   None
31	RETURN_END_IF     None

32	LOAD_CONST        1.0
35	LOAD_GLOBAL       '_sqrt'
38	LOAD_CONST        1.0
41	LOAD_CONST        4.0
44	LOAD_FAST         'kappa'
47	BINARY_MULTIPLY   None
48	LOAD_FAST         'kappa'
51	BINARY_MULTIPLY   None
52	BINARY_ADD        None
53	CALL_FUNCTION_1   None
56	BINARY_ADD        None
57	STORE_FAST        'a'

60	LOAD_FAST         'a'
63	LOAD_GLOBAL       '_sqrt'
66	LOAD_CONST        2.0
69	LOAD_FAST         'a'
72	BINARY_MULTIPLY   None
73	CALL_FUNCTION_1   None
76	BINARY_SUBTRACT   None
77	LOAD_CONST        2.0
80	LOAD_FAST         'kappa'
83	BINARY_MULTIPLY   None
84	BINARY_TRUE_DIVIDE None
85	STORE_FAST        'b'

88	LOAD_CONST        1.0
91	LOAD_FAST         'b'
94	LOAD_FAST         'b'
97	BINARY_MULTIPLY   None
98	BINARY_ADD        None
99	LOAD_CONST        2.0
102	LOAD_FAST         'b'
105	BINARY_MULTIPLY   None
106	BINARY_TRUE_DIVIDE None
107	STORE_FAST        'r'

110	SETUP_LOOP        '237'

113	LOAD_FAST         'random'
116	CALL_FUNCTION_0   None
119	STORE_FAST        'u1'

122	LOAD_GLOBAL       '_cos'
125	LOAD_GLOBAL       '_pi'
128	LOAD_FAST         'u1'
131	BINARY_MULTIPLY   None
132	CALL_FUNCTION_1   None
135	STORE_FAST        'z'

138	LOAD_CONST        1.0
141	LOAD_FAST         'r'
144	LOAD_FAST         'z'
147	BINARY_MULTIPLY   None
148	BINARY_ADD        None
149	LOAD_FAST         'r'
152	LOAD_FAST         'z'
155	BINARY_ADD        None
156	BINARY_TRUE_DIVIDE None
157	STORE_FAST        'f'

160	LOAD_FAST         'kappa'
163	LOAD_FAST         'r'
166	LOAD_FAST         'f'
169	BINARY_SUBTRACT   None
170	BINARY_MULTIPLY   None
171	STORE_FAST        'c'

174	LOAD_FAST         'random'
177	CALL_FUNCTION_0   None
180	STORE_FAST        'u2'

183	LOAD_FAST         'u2'
186	LOAD_FAST         'c'
189	LOAD_CONST        2.0
192	LOAD_FAST         'c'
195	BINARY_SUBTRACT   None
196	BINARY_MULTIPLY   None
197	COMPARE_OP        '<'
200	POP_JUMP_IF_TRUE  '229'
203	LOAD_FAST         'u2'
206	LOAD_FAST         'c'
209	LOAD_GLOBAL       '_exp'
212	LOAD_CONST        1.0
215	LOAD_FAST         'c'
218	BINARY_SUBTRACT   None
219	CALL_FUNCTION_1   None
222	BINARY_MULTIPLY   None
223	COMPARE_OP        '<='
226_0	COME_FROM         '200'
226	POP_JUMP_IF_FALSE '113'

229	BREAK_LOOP        None
230	JUMP_BACK         '113'
233	JUMP_BACK         '113'
236	POP_BLOCK         None
237_0	COME_FROM         '110'

237	LOAD_FAST         'random'
240	CALL_FUNCTION_0   None
243	STORE_FAST        'u3'

246	LOAD_FAST         'u3'
249	LOAD_CONST        0.5
252	COMPARE_OP        '>'
255	POP_JUMP_IF_FALSE '281'

258	LOAD_FAST         'mu'
261	LOAD_GLOBAL       'TWOPI'
264	BINARY_MODULO     None
265	LOAD_GLOBAL       '_acos'
268	LOAD_FAST         'f'
271	CALL_FUNCTION_1   None
274	BINARY_ADD        None
275	STORE_FAST        'theta'
278	JUMP_FORWARD      '301'

281	LOAD_FAST         'mu'
284	LOAD_GLOBAL       'TWOPI'
287	BINARY_MODULO     None
288	LOAD_GLOBAL       '_acos'
291	LOAD_FAST         'f'
294	CALL_FUNCTION_1   None
297	BINARY_SUBTRACT   None
298	STORE_FAST        'theta'
301_0	COME_FROM         '278'

301	LOAD_FAST         'theta'
304	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 236

    def gammavariate--- This code section failed: ---

0	LOAD_FAST         'alpha'
3	LOAD_CONST        0.0
6	COMPARE_OP        '<='
9	POP_JUMP_IF_TRUE  '24'
12	LOAD_FAST         'beta'
15	LOAD_CONST        0.0
18	COMPARE_OP        '<='
21_0	COME_FROM         '9'
21	POP_JUMP_IF_FALSE '36'

24	LOAD_GLOBAL       'ValueError'
27	LOAD_CONST        'gammavariate: alpha and beta must be > 0.0'
30	RAISE_VARARGS_2   None
33	JUMP_FORWARD      '36'
36_0	COME_FROM         '33'

36	LOAD_FAST         'self'
39	LOAD_ATTR         'random'
42	STORE_FAST        'random'

45	LOAD_FAST         'alpha'
48	LOAD_CONST        1.0
51	COMPARE_OP        '>'
54	POP_JUMP_IF_FALSE '285'

57	LOAD_GLOBAL       '_sqrt'
60	LOAD_CONST        2.0
63	LOAD_FAST         'alpha'
66	BINARY_MULTIPLY   None
67	LOAD_CONST        1.0
70	BINARY_SUBTRACT   None
71	CALL_FUNCTION_1   None
74	STORE_FAST        'ainv'

77	LOAD_FAST         'alpha'
80	LOAD_GLOBAL       'LOG4'
83	BINARY_SUBTRACT   None
84	STORE_FAST        'bbb'

87	LOAD_FAST         'alpha'
90	LOAD_FAST         'ainv'
93	BINARY_ADD        None
94	STORE_FAST        'ccc'

97	SETUP_LOOP        '518'

100	LOAD_FAST         'random'
103	CALL_FUNCTION_0   None
106	STORE_FAST        'u1'

109	LOAD_CONST        1e-07
112	LOAD_FAST         'u1'
115	DUP_TOP           None
116	ROT_THREE         None
117	COMPARE_OP        '<'
120	JUMP_IF_FALSE_OR_POP '132'
123	LOAD_CONST        0.9999999
126	COMPARE_OP        '<'
129	JUMP_FORWARD      '134'
132_0	COME_FROM         '120'
132	ROT_TWO           None
133	POP_TOP           None
134_0	COME_FROM         '129'
134	POP_JUMP_IF_TRUE  '143'

137	CONTINUE          '100'
140	JUMP_FORWARD      '143'
143_0	COME_FROM         '140'

143	LOAD_CONST        1.0
146	LOAD_FAST         'random'
149	CALL_FUNCTION_0   None
152	BINARY_SUBTRACT   None
153	STORE_FAST        'u2'

156	LOAD_GLOBAL       '_log'
159	LOAD_FAST         'u1'
162	LOAD_CONST        1.0
165	LOAD_FAST         'u1'
168	BINARY_SUBTRACT   None
169	BINARY_TRUE_DIVIDE None
170	CALL_FUNCTION_1   None
173	LOAD_FAST         'ainv'
176	BINARY_TRUE_DIVIDE None
177	STORE_FAST        'v'

180	LOAD_FAST         'alpha'
183	LOAD_GLOBAL       '_exp'
186	LOAD_FAST         'v'
189	CALL_FUNCTION_1   None
192	BINARY_MULTIPLY   None
193	STORE_FAST        'x'

196	LOAD_FAST         'u1'
199	LOAD_FAST         'u1'
202	BINARY_MULTIPLY   None
203	LOAD_FAST         'u2'
206	BINARY_MULTIPLY   None
207	STORE_FAST        'z'

210	LOAD_FAST         'bbb'
213	LOAD_FAST         'ccc'
216	LOAD_FAST         'v'
219	BINARY_MULTIPLY   None
220	BINARY_ADD        None
221	LOAD_FAST         'x'
224	BINARY_SUBTRACT   None
225	STORE_FAST        'r'

228	LOAD_FAST         'r'
231	LOAD_GLOBAL       'SG_MAGICCONST'
234	BINARY_ADD        None
235	LOAD_CONST        4.5
238	LOAD_FAST         'z'
241	BINARY_MULTIPLY   None
242	BINARY_SUBTRACT   None
243	LOAD_CONST        0.0
246	COMPARE_OP        '>='
249	POP_JUMP_IF_TRUE  '270'
252	LOAD_FAST         'r'
255	LOAD_GLOBAL       '_log'
258	LOAD_FAST         'z'
261	CALL_FUNCTION_1   None
264	COMPARE_OP        '>='
267_0	COME_FROM         '249'
267	POP_JUMP_IF_FALSE '100'

270	LOAD_FAST         'x'
273	LOAD_FAST         'beta'
276	BINARY_MULTIPLY   None
277	RETURN_END_IF     None
278	JUMP_BACK         '100'
281	POP_BLOCK         None
282_0	COME_FROM         '97'
282	JUMP_FORWARD      '518'

285	LOAD_FAST         'alpha'
288	LOAD_CONST        1.0
291	COMPARE_OP        '=='
294	POP_JUMP_IF_FALSE '349'

297	LOAD_FAST         'random'
300	CALL_FUNCTION_0   None
303	STORE_FAST        'u'

306	SETUP_LOOP        '334'
309	LOAD_FAST         'u'
312	LOAD_CONST        1e-07
315	COMPARE_OP        '<='
318	POP_JUMP_IF_FALSE '333'

321	LOAD_FAST         'random'
324	CALL_FUNCTION_0   None
327	STORE_FAST        'u'
330	JUMP_BACK         '309'
333	POP_BLOCK         None
334_0	COME_FROM         '306'

334	LOAD_GLOBAL       '_log'
337	LOAD_FAST         'u'
340	CALL_FUNCTION_1   None
343	UNARY_NEGATIVE    None
344	LOAD_FAST         'beta'
347	BINARY_MULTIPLY   None
348	RETURN_END_IF     None

349	SETUP_LOOP        '510'

352	LOAD_FAST         'random'
355	CALL_FUNCTION_0   None
358	STORE_FAST        'u'

361	LOAD_GLOBAL       '_e'
364	LOAD_FAST         'alpha'
367	BINARY_ADD        None
368	LOAD_GLOBAL       '_e'
371	BINARY_TRUE_DIVIDE None
372	STORE_FAST        'b'

375	LOAD_FAST         'b'
378	LOAD_FAST         'u'
381	BINARY_MULTIPLY   None
382	STORE_FAST        'p'

385	LOAD_FAST         'p'
388	LOAD_CONST        1.0
391	COMPARE_OP        '<='
394	POP_JUMP_IF_FALSE '414'

397	LOAD_FAST         'p'
400	LOAD_CONST        1.0
403	LOAD_FAST         'alpha'
406	BINARY_TRUE_DIVIDE None
407	BINARY_POWER      None
408	STORE_FAST        'x'
411	JUMP_FORWARD      '435'

414	LOAD_GLOBAL       '_log'
417	LOAD_FAST         'b'
420	LOAD_FAST         'p'
423	BINARY_SUBTRACT   None
424	LOAD_FAST         'alpha'
427	BINARY_TRUE_DIVIDE None
428	CALL_FUNCTION_1   None
431	UNARY_NEGATIVE    None
432	STORE_FAST        'x'
435_0	COME_FROM         '411'

435	LOAD_FAST         'random'
438	CALL_FUNCTION_0   None
441	STORE_FAST        'u1'

444	LOAD_FAST         'p'
447	LOAD_CONST        1.0
450	COMPARE_OP        '>'
453	POP_JUMP_IF_FALSE '483'

456	LOAD_FAST         'u1'
459	LOAD_FAST         'x'
462	LOAD_FAST         'alpha'
465	LOAD_CONST        1.0
468	BINARY_SUBTRACT   None
469	BINARY_POWER      None
470	COMPARE_OP        '<='
473	POP_JUMP_IF_FALSE '506'

476	BREAK_LOOP        None
477	JUMP_ABSOLUTE     '506'
480	JUMP_BACK         '352'

483	LOAD_FAST         'u1'
486	LOAD_GLOBAL       '_exp'
489	LOAD_FAST         'x'
492	UNARY_NEGATIVE    None
493	CALL_FUNCTION_1   None
496	COMPARE_OP        '<='
499	POP_JUMP_IF_FALSE '352'

502	BREAK_LOOP        None
503	JUMP_BACK         '352'
506	JUMP_BACK         '352'
509	POP_BLOCK         None
510_0	COME_FROM         '349'

510	LOAD_FAST         'x'
513	LOAD_FAST         'beta'
516	BINARY_MULTIPLY   None
517	RETURN_VALUE      None
518_0	COME_FROM         '282'

Syntax error at or near `POP_BLOCK' token at offset 281

    def gauss(self, mu, sigma):
        """Gaussian distribution.
        
        mu is the mean, and sigma is the standard deviation.  This is
        slightly faster than the normalvariate() function.
        
        Not thread-safe without a lock around calls.
        
        """
        random = self.random
        z = self.gauss_next
        self.gauss_next = None
        if z is None:
            x2pi = random() * TWOPI
            g2rad = _sqrt(-2.0 * _log(1.0 - random()))
            z = _cos(x2pi) * g2rad
            self.gauss_next = _sin(x2pi) * g2rad
        return mu + z * sigma

    def betavariate(self, alpha, beta):
        """Beta distribution.
        
        Conditions on the parameters are alpha > 0 and beta > 0.
        Returned values range between 0 and 1.
        
        """
        y = self.gammavariate(alpha, 1.0)
        if y == 0:
            return 0.0
        else:
            return y / (y + self.gammavariate(beta, 1.0))

    def paretovariate(self, alpha):
        """Pareto distribution.  alpha is the shape parameter."""
        u = 1.0 - self.random()
        return 1.0 / pow(u, 1.0 / alpha)

    def weibullvariate(self, alpha, beta):
        """Weibull distribution.
        
        alpha is the scale parameter and beta is the shape parameter.
        
        """
        u = 1.0 - self.random()
        return alpha * pow(-_log(u), 1.0 / beta)


class WichmannHill(Random):
    VERSION = 1

    def seed(self, a = None):
        """Initialize internal state from hashable object.
        
        None or no argument seeds from current time or from an operating
        system specific randomness source if available.
        
        If a is not None or an int or long, hash(a) is used instead.
        
        If a is an int or long, a is used directly.  Distinct values between
        0 and 27814431486575L inclusive are guaranteed to yield distinct
        internal states (this guarantee is specific to the default
        Wichmann-Hill generator).
        """
        if a is None:
            try:
                a = long(_hexlify(_urandom(16)), 16)
            except NotImplementedError:
                import time
                a = long(time.time() * 256)

        if not isinstance(a, (int, long)):
            a = hash(a)
        a, x = divmod(a, 30268)
        a, y = divmod(a, 30306)
        a, z = divmod(a, 30322)
        self._seed = (int(x) + 1, int(y) + 1, int(z) + 1)
        self.gauss_next = None
        return

    def random(self):
        """Get the next random number in the range [0.0, 1.0)."""
        x, y, z = self._seed
        x = 171 * x % 30269
        y = 172 * y % 30307
        z = 170 * z % 30323
        self._seed = (x, y, z)
        return (x / 30269.0 + y / 30307.0 + z / 30323.0) % 1.0

    def getstate(self):
        """Return internal state; can be passed to setstate() later."""
        return (self.VERSION, self._seed, self.gauss_next)

    def setstate(self, state):
        """Restore internal state from object returned by getstate()."""
        version = state[0]
        if version == 1:
            version, self._seed, self.gauss_next = state
        else:
            raise ValueError('state with version %s passed to Random.setstate() of version %s' % (version, self.VERSION))

    def jumpahead(self, n):
        """Act as if n calls to random() were made, but quickly.
        
        n is an int, greater than or equal to 0.
        
        Example use:  If you have 2 threads and know that each will
        consume no more than a million random numbers, create two Random
        objects r1 and r2, then do
            r2.setstate(r1.getstate())
            r2.jumpahead(1000000)
        Then r1 and r2 will use guaranteed-disjoint segments of the full
        period.
        """
        if not n >= 0:
            raise ValueError('n must be >= 0')
        x, y, z = self._seed
        x = int(x * pow(171, n, 30269)) % 30269
        y = int(y * pow(172, n, 30307)) % 30307
        z = int(z * pow(170, n, 30323)) % 30323
        self._seed = (x, y, z)

    def __whseed(self, x = 0, y = 0, z = 0):
        """Set the Wichmann-Hill seed from (x, y, z).
        
        These must be integers in the range [0, 256).
        """
        if not type(x) == type(y) == type(z) == int:
            raise TypeError('seeds must be integers')
        if not (0 <= x < 256 and 0 <= y < 256 and 0 <= z < 256):
            raise ValueError('seeds must be in range(0, 256)')
        if 0 == x == y == z:
            import time
            t = long(time.time() * 256)
            t = int(t & 16777215 ^ t >> 24)
            t, x = divmod(t, 256)
            t, y = divmod(t, 256)
            t, z = divmod(t, 256)
        self._seed = (x or 1, y or 1, z or 1)
        self.gauss_next = None
        return

    def whseed(self, a = None):
        """Seed from hashable object's hash code.
        
        None or no argument seeds from current time.  It is not guaranteed
        that objects with distinct hash codes lead to distinct internal
        states.
        
        This is obsolete, provided for compatibility with the seed routine
        used prior to Python 2.1.  Use the .seed() method instead.
        """
        if a is None:
            self.__whseed()
            return
        else:
            a = hash(a)
            a, x = divmod(a, 256)
            a, y = divmod(a, 256)
            a, z = divmod(a, 256)
            x = (x + a) % 256 or 1
            y = (y + a) % 256 or 1
            z = (z + a) % 256 or 1
            self.__whseed(x, y, z)
            return


class SystemRandom(Random):
    """Alternate random number generator using sources provided
    by the operating system (such as /dev/urandom on Unix or
    CryptGenRandom on Windows).
    
     Not available on all systems (see os.urandom() for details).
    """

    def random(self):
        """Get the next random number in the range [0.0, 1.0)."""
        return (long(_hexlify(_urandom(7)), 16) >> 3) * RECIP_BPF

    def getrandbits(self, k):
        """getrandbits(k) -> x.  Generates a long int with k random bits."""
        if k <= 0:
            raise ValueError('number of bits must be greater than zero')
        if k != int(k):
            raise TypeError('number of bits should be an integer')
        bytes = (k + 7) // 8
        x = long(_hexlify(_urandom(bytes)), 16)
        return x >> bytes * 8 - k

    def _stub(self, *args, **kwds):
        """Stub method.  Not used for a system random number generator."""
        return None

    seed = jumpahead = _stub

    def _notimplemented(self, *args, **kwds):
        """Method should not be called for a system random number generator."""
        raise NotImplementedError('System entropy source does not have state.')

    getstate = setstate = _notimplemented


def _test_generator(n, func, args):
    import time
    print n, 'times', func.__name__
    total = 0.0
    sqsum = 0.0
    smallest = 10000000000.0
    largest = -10000000000.0
    t0 = time.time()
    for i in range(n):
        x = func(*args)
        total += x
        sqsum = sqsum + x * x
        smallest = min(x, smallest)
        largest = max(x, largest)

    t1 = time.time()
    print round(t1 - t0, 3), 'sec,',
    avg = total / n
    stddev = _sqrt(sqsum / n - avg * avg)
    print 'avg %g, stddev %g, min %g, max %g' % (avg,
     stddev,
     smallest,
     largest)


def _test(N = 2000):
    _test_generator(N, random, ())
    _test_generator(N, normalvariate, (0.0, 1.0))
    _test_generator(N, lognormvariate, (0.0, 1.0))
    _test_generator(N, vonmisesvariate, (0.0, 1.0))
    _test_generator(N, gammavariate, (0.01, 1.0))
    _test_generator(N, gammavariate, (0.1, 1.0))
    _test_generator(N, gammavariate, (0.1, 2.0))
    _test_generator(N, gammavariate, (0.5, 1.0))
    _test_generator(N, gammavariate, (0.9, 1.0))
    _test_generator(N, gammavariate, (1.0, 1.0))
    _test_generator(N, gammavariate, (2.0, 1.0))
    _test_generator(N, gammavariate, (20.0, 1.0))
    _test_generator(N, gammavariate, (200.0, 1.0))
    _test_generator(N, gauss, (0.0, 1.0))
    _test_generator(N, betavariate, (3.0, 3.0))
    _test_generator(N, triangular, (0.0, 1.0, 0.3333333333333333))


_inst = Random()
seed = _inst.seed
random = _inst.random
uniform = _inst.uniform
triangular = _inst.triangular
randint = _inst.randint
choice = _inst.choice
randrange = _inst.randrange
sample = _inst.sample
shuffle = _inst.shuffle
normalvariate = _inst.normalvariate
lognormvariate = _inst.lognormvariate
expovariate = _inst.expovariate
vonmisesvariate = _inst.vonmisesvariate
gammavariate = _inst.gammavariate
gauss = _inst.gauss
betavariate = _inst.betavariate
paretovariate = _inst.paretovariate
weibullvariate = _inst.weibullvariate
getstate = _inst.getstate
setstate = _inst.setstate
jumpahead = _inst.jumpahead
getrandbits = _inst.getrandbits
if __name__ == '__main__':
    _test()