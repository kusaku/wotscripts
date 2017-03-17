# Embedded file name: scripts/common/Lib/plat-mac/aetools.py
"""Tools for use in AppleEvent clients and servers.

pack(x) converts a Python object to an AEDesc object
unpack(desc) does the reverse

packevent(event, parameters, attributes) sets params and attrs in an AEAppleEvent record
unpackevent(event) returns the parameters and attributes from an AEAppleEvent record

Plus...  Lots of classes and routines that help representing AE objects,
ranges, conditionals, logicals, etc., so you can write, e.g.:

    x = Character(1, Document("foobar"))

and pack(x) will create an AE object reference equivalent to AppleScript's

    character 1 of document "foobar"

Some of the stuff that appears to be exported from this module comes from other
files: the pack stuff from aepack, the objects from aetypes.

"""
from warnings import warnpy3k
warnpy3k('In 3.x, the aetools module is removed.', stacklevel=2)
from types import *
from Carbon import AE
from Carbon import Evt
from Carbon import AppleEvents
import MacOS
import sys
import time
from aetypes import *
from aepack import packkey, pack, unpack, coerce, AEDescType
Error = 'aetools.Error'
LAUNCH_MAX_WAIT_TIME = 10
aekeywords = ['tran',
 'rtid',
 'evcl',
 'evid',
 'addr',
 'optk',
 'timo',
 'inte',
 'esrc',
 'miss',
 'from']

def missed(ae):
    try:
        desc = ae.AEGetAttributeDesc('miss', 'keyw')
    except AE.Error as msg:
        return None

    return desc.data


def unpackevent--- This code section failed: ---

0	BUILD_MAP         None
3	STORE_FAST        'parameters'

6	SETUP_EXCEPT      '31'

9	LOAD_FAST         'ae'
12	LOAD_ATTR         'AEGetParamDesc'
15	LOAD_CONST        '----'
18	LOAD_CONST        '****'
21	CALL_FUNCTION_2   None
24	STORE_FAST        'dirobj'
27	POP_BLOCK         None
28	JUMP_FORWARD      '51'
31_0	COME_FROM         '6'

31	DUP_TOP           None
32	LOAD_GLOBAL       'AE'
35	LOAD_ATTR         'Error'
38	COMPARE_OP        'exception match'
41	POP_JUMP_IF_FALSE '50'
44	POP_TOP           None
45	POP_TOP           None
46	POP_TOP           None

47	JUMP_FORWARD      '73'
50	END_FINALLY       None
51_0	COME_FROM         '28'

51	LOAD_GLOBAL       'unpack'
54	LOAD_FAST         'dirobj'
57	LOAD_FAST         'formodulename'
60	CALL_FUNCTION_2   None
63	LOAD_FAST         'parameters'
66	LOAD_CONST        '----'
69	STORE_SUBSCR      None

70	DELETE_FAST       'dirobj'
73_0	COME_FROM         '50'

73	SETUP_EXCEPT      '98'

76	LOAD_FAST         'ae'
79	LOAD_ATTR         'AEGetParamDesc'
82	LOAD_CONST        'errn'
85	LOAD_CONST        '****'
88	CALL_FUNCTION_2   None
91	STORE_FAST        'dirobj'
94	POP_BLOCK         None
95	JUMP_FORWARD      '118'
98_0	COME_FROM         '73'

98	DUP_TOP           None
99	LOAD_GLOBAL       'AE'
102	LOAD_ATTR         'Error'
105	COMPARE_OP        'exception match'
108	POP_JUMP_IF_FALSE '117'
111	POP_TOP           None
112	POP_TOP           None
113	POP_TOP           None

114	JUMP_FORWARD      '140'
117	END_FINALLY       None
118_0	COME_FROM         '95'

118	LOAD_GLOBAL       'unpack'
121	LOAD_FAST         'dirobj'
124	LOAD_FAST         'formodulename'
127	CALL_FUNCTION_2   None
130	LOAD_FAST         'parameters'
133	LOAD_CONST        'errn'
136	STORE_SUBSCR      None

137	DELETE_FAST       'dirobj'
140_0	COME_FROM         '117'

140	SETUP_LOOP        '200'

143	LOAD_GLOBAL       'missed'
146	LOAD_FAST         'ae'
149	CALL_FUNCTION_1   None
152	STORE_FAST        'key'

155	LOAD_FAST         'key'
158	POP_JUMP_IF_TRUE  '165'
161	BREAK_LOOP        None
162	JUMP_FORWARD      '165'
165_0	COME_FROM         '162'

165	LOAD_GLOBAL       'unpack'
168	LOAD_FAST         'ae'
171	LOAD_ATTR         'AEGetParamDesc'
174	LOAD_FAST         'key'
177	LOAD_CONST        '****'
180	CALL_FUNCTION_2   None
183	LOAD_FAST         'formodulename'
186	CALL_FUNCTION_2   None
189	LOAD_FAST         'parameters'
192	LOAD_FAST         'key'
195	STORE_SUBSCR      None
196	JUMP_BACK         '143'
199	POP_BLOCK         None
200_0	COME_FROM         '140'

200	BUILD_MAP         None
203	STORE_FAST        'attributes'

206	SETUP_LOOP        '339'
209	LOAD_GLOBAL       'aekeywords'
212	GET_ITER          None
213	FOR_ITER          '338'
216	STORE_FAST        'key'

219	SETUP_EXCEPT      '244'

222	LOAD_FAST         'ae'
225	LOAD_ATTR         'AEGetAttributeDesc'
228	LOAD_FAST         'key'
231	LOAD_CONST        '****'
234	CALL_FUNCTION_2   None
237	STORE_FAST        'desc'
240	POP_BLOCK         None
241	JUMP_FORWARD      '316'
244_0	COME_FROM         '219'

244	DUP_TOP           None
245	LOAD_GLOBAL       'AE'
248	LOAD_ATTR         'Error'
251	LOAD_GLOBAL       'MacOS'
254	LOAD_ATTR         'Error'
257	BUILD_TUPLE_2     None
260	COMPARE_OP        'exception match'
263	POP_JUMP_IF_FALSE '315'
266	POP_TOP           None
267	STORE_FAST        'msg'
270	POP_TOP           None

271	LOAD_FAST         'msg'
274	LOAD_CONST        0
277	BINARY_SUBSCR     None
278	LOAD_CONST        -1701
281	COMPARE_OP        '!='
284	POP_JUMP_IF_FALSE '213'
287	LOAD_FAST         'msg'
290	LOAD_CONST        0
293	BINARY_SUBSCR     None
294	LOAD_CONST        -1704
297	COMPARE_OP        '!='
300_0	COME_FROM         '284'
300	POP_JUMP_IF_FALSE '213'

303	RAISE_VARARGS_0   None
306	JUMP_BACK         '213'

309	CONTINUE          '213'
312	JUMP_FORWARD      '316'
315	END_FINALLY       None
316_0	COME_FROM         '241'
316_1	COME_FROM         '315'

316	LOAD_GLOBAL       'unpack'
319	LOAD_FAST         'desc'
322	LOAD_FAST         'formodulename'
325	CALL_FUNCTION_2   None
328	LOAD_FAST         'attributes'
331	LOAD_FAST         'key'
334	STORE_SUBSCR      None
335	JUMP_BACK         '213'
338	POP_BLOCK         None
339_0	COME_FROM         '206'

339	LOAD_FAST         'parameters'
342	LOAD_FAST         'attributes'
345	BUILD_TUPLE_2     None
348	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 199


def packevent(ae, parameters = {}, attributes = {}):
    for key, value in parameters.items():
        packkey(ae, key, value)

    for key, value in attributes.items():
        ae.AEPutAttributeDesc(key, pack(value))


def keysubst(arguments, keydict):
    """Replace long name keys by their 4-char counterparts, and check"""
    ok = keydict.values()
    for k in arguments.keys():
        if k in keydict:
            v = arguments[k]
            del arguments[k]
            arguments[keydict[k]] = v
        elif k != '----' and k not in ok:
            raise TypeError, 'Unknown keyword argument: %s' % k


def enumsubst(arguments, key, edict):
    """Substitute a single enum keyword argument, if it occurs"""
    if key not in arguments or edict is None:
        return
    else:
        v = arguments[key]
        ok = edict.values()
        if v in edict:
            arguments[key] = Enum(edict[v])
        elif v not in ok:
            raise TypeError, 'Unknown enumerator: %s' % v
        return


def decodeerror(arguments):
    """Create the 'best' argument for a raise MacOS.Error"""
    errn = arguments['errn']
    err_a1 = errn
    if 'errs' in arguments:
        err_a2 = arguments['errs']
    else:
        err_a2 = MacOS.GetErrorString(errn)
    if 'erob' in arguments:
        err_a3 = arguments['erob']
    else:
        err_a3 = None
    return (err_a1, err_a2, err_a3)


class TalkTo:
    """An AE connection to an application"""
    _signature = None
    _moduleName = None
    _elemdict = {}
    _propdict = {}
    __eventloop_initialized = 0

    def __ensure_WMAvailable(klass):
        if klass.__eventloop_initialized:
            return 1
        if not MacOS.WMAvailable():
            return 0
        Evt.WaitNextEvent(0, 0)
        return 1

    __ensure_WMAvailable = classmethod(__ensure_WMAvailable)

    def __init__(self, signature = None, start = 0, timeout = 0):
        """Create a communication channel with a particular application.
        
        Addressing the application is done by specifying either a
        4-byte signature, an AEDesc or an object that will __aepack__
        to an AEDesc.
        """
        self.target_signature = None
        if signature is None:
            signature = self._signature
        if type(signature) == AEDescType:
            self.target = signature
        elif type(signature) == InstanceType and hasattr(signature, '__aepack__'):
            self.target = signature.__aepack__()
        elif type(signature) == StringType and len(signature) == 4:
            self.target = AE.AECreateDesc(AppleEvents.typeApplSignature, signature)
            self.target_signature = signature
        else:
            raise TypeError, 'signature should be 4-char string or AEDesc'
        self.send_flags = AppleEvents.kAEWaitReply
        self.send_priority = AppleEvents.kAENormalPriority
        if timeout:
            self.send_timeout = timeout
        else:
            self.send_timeout = AppleEvents.kAEDefaultTimeout
        if start:
            self._start()
        return

    def _start(self):
        """Start the application, if it is not running yet"""
        try:
            self.send('ascr', 'noop')
        except AE.Error:
            _launch(self.target_signature)
            for i in range(LAUNCH_MAX_WAIT_TIME):
                try:
                    self.send('ascr', 'noop')
                except AE.Error:
                    pass
                else:
                    break

                time.sleep(1)

    def start(self):
        """Deprecated, used _start()"""
        self._start()

    def newevent(self, code, subcode, parameters = {}, attributes = {}):
        """Create a complete structure for an apple event"""
        event = AE.AECreateAppleEvent(code, subcode, self.target, AppleEvents.kAutoGenerateReturnID, AppleEvents.kAnyTransactionID)
        packevent(event, parameters, attributes)
        return event

    def sendevent(self, event):
        """Send a pre-created appleevent, await the reply and unpack it"""
        if not self.__ensure_WMAvailable():
            raise RuntimeError, 'No window manager access, cannot send AppleEvent'
        reply = event.AESend(self.send_flags, self.send_priority, self.send_timeout)
        parameters, attributes = unpackevent(reply, self._moduleName)
        return (reply, parameters, attributes)

    def send(self, code, subcode, parameters = {}, attributes = {}):
        """Send an appleevent given code/subcode/pars/attrs and unpack the reply"""
        return self.sendevent(self.newevent(code, subcode, parameters, attributes))

    def activate(self):
        """Send 'activate' command"""
        self.send('misc', 'actv')

    def _get(self, _object, asfile = None, _attributes = {}):
        """_get: get data from an object
        Required argument: the object
        Keyword argument _attributes: AppleEvent attribute dictionary
        Returns: the data
        """
        _code = 'core'
        _subcode = 'getd'
        _arguments = {'----': _object}
        if asfile:
            _arguments['rtyp'] = mktype(asfile)
        _reply, _arguments, _attributes = self.send(_code, _subcode, _arguments, _attributes)
        if 'errn' in _arguments:
            raise Error, decodeerror(_arguments)
        if '----' in _arguments:
            return _arguments['----']
            if asfile:
                item.__class__ = asfile
            return item

    get = _get
    _argmap_set = {'to': 'data'}

    def _set(self, _object, _attributes = {}, **_arguments):
        """set: Set an object's data.
        Required argument: the object for the command
        Keyword argument to: The new value.
        Keyword argument _attributes: AppleEvent attribute dictionary
        """
        _code = 'core'
        _subcode = 'setd'
        keysubst(_arguments, self._argmap_set)
        _arguments['----'] = _object
        _reply, _arguments, _attributes = self.send(_code, _subcode, _arguments, _attributes)
        if _arguments.get('errn', 0):
            raise Error, decodeerror(_arguments)
        if '----' in _arguments:
            return _arguments['----']

    set = _set

    def __getattr__(self, name):
        if name in self._elemdict:
            cls = self._elemdict[name]
            return DelayedComponentItem(cls, None)
        elif name in self._propdict:
            cls = self._propdict[name]
            return cls()
        else:
            raise AttributeError, name
            return None


class _miniFinder(TalkTo):

    def open(self, _object, _attributes = {}, **_arguments):
        """open: Open the specified object(s)
        Required argument: list of objects to open
        Keyword argument _attributes: AppleEvent attribute dictionary
        """
        _code = 'aevt'
        _subcode = 'odoc'
        if _arguments:
            raise TypeError, 'No optional args expected'
        _arguments['----'] = _object
        _reply, _arguments, _attributes = self.send(_code, _subcode, _arguments, _attributes)
        if 'errn' in _arguments:
            raise Error, decodeerror(_arguments)
        if '----' in _arguments:
            return _arguments['----']


_finder = _miniFinder('MACS')

def _launch(appfile):
    """Open a file thru the finder. Specify file by name or fsspec"""
    _finder.open(_application_file(('ID  ', appfile)))


class _application_file(ComponentItem):
    """application file - An application's file on disk"""
    want = 'appf'


_application_file._propdict = {}
_application_file._elemdict = {}

def test():
    target = AE.AECreateDesc('sign', 'quil')
    ae = AE.AECreateAppleEvent('aevt', 'oapp', target, -1, 0)
    print unpackevent(ae)
    raw_input(':')
    ae = AE.AECreateAppleEvent('core', 'getd', target, -1, 0)
    obj = Character(2, Word(1, Document(1)))
    print obj
    print repr(obj)
    packevent(ae, {'----': obj})
    params, attrs = unpackevent(ae)
    print params['----']
    raw_input(':')


if __name__ == '__main__':
    test()
    sys.exit(1)