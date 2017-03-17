# Embedded file name: scripts/common/Lib/plat-mac/EasyDialogs.py
"""Easy to use dialogs.

Message(msg) -- display a message and an OK button.
AskString(prompt, default) -- ask for a string, display OK and Cancel buttons.
AskPassword(prompt, default) -- like AskString(), but shows text as bullets.
AskYesNoCancel(question, default) -- display a question and Yes, No and Cancel buttons.
GetArgv(optionlist, commandlist) -- fill a sys.argv-like list using a dialog
AskFileForOpen(...) -- Ask the user for an existing file
AskFileForSave(...) -- Ask the user for an output file
AskFolder(...) -- Ask the user to select a folder
bar = Progress(label, maxvalue) -- Display a progress bar
bar.set(value) -- Set value
bar.inc( *amount ) -- increment value by amount (default=1)
bar.label( *newlabel ) -- get or set text label.

More documentation in each function.
This module uses DLOG resources 260 and on.
Based upon STDWIN dialogs with the same names and functions.
"""
from warnings import warnpy3k
warnpy3k('In 3.x, the EasyDialogs module is removed.', stacklevel=2)
from Carbon.Dlg import GetNewDialog, SetDialogItemText, GetDialogItemText, ModalDialog
from Carbon import Qd
from Carbon import QuickDraw
from Carbon import Dialogs
from Carbon import Windows
from Carbon import Dlg, Win, Evt, Events
from Carbon import Ctl
from Carbon import Controls
from Carbon import Menu
from Carbon import AE
import Nav
import MacOS
import string
from Carbon.ControlAccessor import *
import Carbon.File
import macresource
import os
import sys
__all__ = ['Message',
 'AskString',
 'AskPassword',
 'AskYesNoCancel',
 'GetArgv',
 'AskFileForOpen',
 'AskFileForSave',
 'AskFolder',
 'ProgressBar']
_initialized = 0

def _initialize():
    global _initialized
    if _initialized:
        return
    macresource.need('DLOG', 260, 'dialogs.rsrc', __name__)


def _interact():
    """Make sure the application is in the foreground"""
    AE.AEInteractWithUser(50000000)


def cr2lf(text):
    if '\r' in text:
        text = string.join(string.split(text, '\r'), '\n')
    return text


def lf2cr(text):
    if '\n' in text:
        text = string.join(string.split(text, '\n'), '\r')
    if len(text) > 253:
        text = text[:253] + '\xc9'
    return text


def Message--- This code section failed: ---

0	LOAD_GLOBAL       '_initialize'
3	CALL_FUNCTION_0   None
6	POP_TOP           None

7	LOAD_GLOBAL       '_interact'
10	CALL_FUNCTION_0   None
13	POP_TOP           None

14	LOAD_GLOBAL       'GetNewDialog'
17	LOAD_FAST         'id'
20	LOAD_CONST        -1
23	CALL_FUNCTION_2   None
26	STORE_FAST        'd'

29	LOAD_FAST         'd'
32	POP_JUMP_IF_TRUE  '52'

35	LOAD_CONST        "EasyDialogs: Can't get DLOG resource with id ="
38	PRINT_ITEM        None
39	LOAD_FAST         'id'
42	PRINT_ITEM_CONT   None
43	LOAD_CONST        ' (missing resource file?)'
46	PRINT_ITEM_CONT   None
47	PRINT_NEWLINE_CONT None

48	LOAD_CONST        None
51	RETURN_END_IF     None

52	LOAD_FAST         'd'
55	LOAD_ATTR         'GetDialogItemAsControl'
58	LOAD_CONST        2
61	CALL_FUNCTION_1   None
64	STORE_FAST        'h'

67	LOAD_GLOBAL       'SetDialogItemText'
70	LOAD_FAST         'h'
73	LOAD_GLOBAL       'lf2cr'
76	LOAD_FAST         'msg'
79	CALL_FUNCTION_1   None
82	CALL_FUNCTION_2   None
85	POP_TOP           None

86	LOAD_FAST         'ok'
89	LOAD_CONST        None
92	COMPARE_OP        'is not'
95	POP_JUMP_IF_FALSE '129'

98	LOAD_FAST         'd'
101	LOAD_ATTR         'GetDialogItemAsControl'
104	LOAD_CONST        1
107	CALL_FUNCTION_1   None
110	STORE_FAST        'h'

113	LOAD_FAST         'h'
116	LOAD_ATTR         'SetControlTitle'
119	LOAD_FAST         'ok'
122	CALL_FUNCTION_1   None
125	POP_TOP           None
126	JUMP_FORWARD      '129'
129_0	COME_FROM         '126'

129	LOAD_FAST         'd'
132	LOAD_ATTR         'SetDialogDefaultItem'
135	LOAD_CONST        1
138	CALL_FUNCTION_1   None
141	POP_TOP           None

142	LOAD_FAST         'd'
145	LOAD_ATTR         'AutoSizeDialog'
148	CALL_FUNCTION_0   None
151	POP_TOP           None

152	LOAD_FAST         'd'
155	LOAD_ATTR         'GetDialogWindow'
158	CALL_FUNCTION_0   None
161	LOAD_ATTR         'ShowWindow'
164	CALL_FUNCTION_0   None
167	POP_TOP           None

168	SETUP_LOOP        '203'

171	LOAD_GLOBAL       'ModalDialog'
174	LOAD_CONST        None
177	CALL_FUNCTION_1   None
180	STORE_FAST        'n'

183	LOAD_FAST         'n'
186	LOAD_CONST        1
189	COMPARE_OP        '=='
192	POP_JUMP_IF_FALSE '171'

195	LOAD_CONST        None
198	RETURN_END_IF     None
199	JUMP_BACK         '171'
202	POP_BLOCK         None
203_0	COME_FROM         '168'
203	LOAD_CONST        None
206	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 202


def AskString--- This code section failed: ---

0	LOAD_GLOBAL       '_initialize'
3	CALL_FUNCTION_0   None
6	POP_TOP           None

7	LOAD_GLOBAL       '_interact'
10	CALL_FUNCTION_0   None
13	POP_TOP           None

14	LOAD_GLOBAL       'GetNewDialog'
17	LOAD_FAST         'id'
20	LOAD_CONST        -1
23	CALL_FUNCTION_2   None
26	STORE_FAST        'd'

29	LOAD_FAST         'd'
32	POP_JUMP_IF_TRUE  '52'

35	LOAD_CONST        "EasyDialogs: Can't get DLOG resource with id ="
38	PRINT_ITEM        None
39	LOAD_FAST         'id'
42	PRINT_ITEM_CONT   None
43	LOAD_CONST        ' (missing resource file?)'
46	PRINT_ITEM_CONT   None
47	PRINT_NEWLINE_CONT None

48	LOAD_CONST        None
51	RETURN_END_IF     None

52	LOAD_FAST         'd'
55	LOAD_ATTR         'GetDialogItemAsControl'
58	LOAD_CONST        3
61	CALL_FUNCTION_1   None
64	STORE_FAST        'h'

67	LOAD_GLOBAL       'SetDialogItemText'
70	LOAD_FAST         'h'
73	LOAD_GLOBAL       'lf2cr'
76	LOAD_FAST         'prompt'
79	CALL_FUNCTION_1   None
82	CALL_FUNCTION_2   None
85	POP_TOP           None

86	LOAD_FAST         'd'
89	LOAD_ATTR         'GetDialogItemAsControl'
92	LOAD_CONST        4
95	CALL_FUNCTION_1   None
98	STORE_FAST        'h'

101	LOAD_GLOBAL       'SetDialogItemText'
104	LOAD_FAST         'h'
107	LOAD_GLOBAL       'lf2cr'
110	LOAD_FAST         'default'
113	CALL_FUNCTION_1   None
116	CALL_FUNCTION_2   None
119	POP_TOP           None

120	LOAD_FAST         'd'
123	LOAD_ATTR         'SelectDialogItemText'
126	LOAD_CONST        4
129	LOAD_CONST        0
132	LOAD_CONST        999
135	CALL_FUNCTION_3   None
138	POP_TOP           None

139	LOAD_FAST         'ok'
142	LOAD_CONST        None
145	COMPARE_OP        'is not'
148	POP_JUMP_IF_FALSE '182'

151	LOAD_FAST         'd'
154	LOAD_ATTR         'GetDialogItemAsControl'
157	LOAD_CONST        1
160	CALL_FUNCTION_1   None
163	STORE_FAST        'h'

166	LOAD_FAST         'h'
169	LOAD_ATTR         'SetControlTitle'
172	LOAD_FAST         'ok'
175	CALL_FUNCTION_1   None
178	POP_TOP           None
179	JUMP_FORWARD      '182'
182_0	COME_FROM         '179'

182	LOAD_FAST         'cancel'
185	LOAD_CONST        None
188	COMPARE_OP        'is not'
191	POP_JUMP_IF_FALSE '225'

194	LOAD_FAST         'd'
197	LOAD_ATTR         'GetDialogItemAsControl'
200	LOAD_CONST        2
203	CALL_FUNCTION_1   None
206	STORE_FAST        'h'

209	LOAD_FAST         'h'
212	LOAD_ATTR         'SetControlTitle'
215	LOAD_FAST         'cancel'
218	CALL_FUNCTION_1   None
221	POP_TOP           None
222	JUMP_FORWARD      '225'
225_0	COME_FROM         '222'

225	LOAD_FAST         'd'
228	LOAD_ATTR         'SetDialogDefaultItem'
231	LOAD_CONST        1
234	CALL_FUNCTION_1   None
237	POP_TOP           None

238	LOAD_FAST         'd'
241	LOAD_ATTR         'SetDialogCancelItem'
244	LOAD_CONST        2
247	CALL_FUNCTION_1   None
250	POP_TOP           None

251	LOAD_FAST         'd'
254	LOAD_ATTR         'AutoSizeDialog'
257	CALL_FUNCTION_0   None
260	POP_TOP           None

261	LOAD_FAST         'd'
264	LOAD_ATTR         'GetDialogWindow'
267	CALL_FUNCTION_0   None
270	LOAD_ATTR         'ShowWindow'
273	CALL_FUNCTION_0   None
276	POP_TOP           None

277	SETUP_LOOP        '355'

280	LOAD_GLOBAL       'ModalDialog'
283	LOAD_CONST        None
286	CALL_FUNCTION_1   None
289	STORE_FAST        'n'

292	LOAD_FAST         'n'
295	LOAD_CONST        1
298	COMPARE_OP        '=='
301	POP_JUMP_IF_FALSE '335'

304	LOAD_FAST         'd'
307	LOAD_ATTR         'GetDialogItemAsControl'
310	LOAD_CONST        4
313	CALL_FUNCTION_1   None
316	STORE_FAST        'h'

319	LOAD_GLOBAL       'cr2lf'
322	LOAD_GLOBAL       'GetDialogItemText'
325	LOAD_FAST         'h'
328	CALL_FUNCTION_1   None
331	CALL_FUNCTION_1   None
334	RETURN_END_IF     None

335	LOAD_FAST         'n'
338	LOAD_CONST        2
341	COMPARE_OP        '=='
344	POP_JUMP_IF_FALSE '280'
347	LOAD_CONST        None
350	RETURN_END_IF     None
351	JUMP_BACK         '280'
354	POP_BLOCK         None
355_0	COME_FROM         '277'
355	LOAD_CONST        None
358	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 354


def AskPassword--- This code section failed: ---

0	LOAD_GLOBAL       '_initialize'
3	CALL_FUNCTION_0   None
6	POP_TOP           None

7	LOAD_GLOBAL       '_interact'
10	CALL_FUNCTION_0   None
13	POP_TOP           None

14	LOAD_GLOBAL       'GetNewDialog'
17	LOAD_FAST         'id'
20	LOAD_CONST        -1
23	CALL_FUNCTION_2   None
26	STORE_FAST        'd'

29	LOAD_FAST         'd'
32	POP_JUMP_IF_TRUE  '52'

35	LOAD_CONST        "EasyDialogs: Can't get DLOG resource with id ="
38	PRINT_ITEM        None
39	LOAD_FAST         'id'
42	PRINT_ITEM_CONT   None
43	LOAD_CONST        ' (missing resource file?)'
46	PRINT_ITEM_CONT   None
47	PRINT_NEWLINE_CONT None

48	LOAD_CONST        None
51	RETURN_END_IF     None

52	LOAD_FAST         'd'
55	LOAD_ATTR         'GetDialogItemAsControl'
58	LOAD_CONST        3
61	CALL_FUNCTION_1   None
64	STORE_FAST        'h'

67	LOAD_GLOBAL       'SetDialogItemText'
70	LOAD_FAST         'h'
73	LOAD_GLOBAL       'lf2cr'
76	LOAD_FAST         'prompt'
79	CALL_FUNCTION_1   None
82	CALL_FUNCTION_2   None
85	POP_TOP           None

86	LOAD_FAST         'd'
89	LOAD_ATTR         'GetDialogItemAsControl'
92	LOAD_CONST        4
95	CALL_FUNCTION_1   None
98	STORE_FAST        'pwd'

101	LOAD_CONST        '\xa5'
104	LOAD_GLOBAL       'len'
107	LOAD_FAST         'default'
110	CALL_FUNCTION_1   None
113	BINARY_MULTIPLY   None
114	STORE_FAST        'bullets'

117	LOAD_GLOBAL       'SetControlData'
120	LOAD_FAST         'pwd'
123	LOAD_GLOBAL       'kControlEditTextPart'
126	LOAD_GLOBAL       'kControlEditTextPasswordTag'
129	LOAD_FAST         'default'
132	CALL_FUNCTION_4   None
135	POP_TOP           None

136	LOAD_FAST         'd'
139	LOAD_ATTR         'SelectDialogItemText'
142	LOAD_CONST        4
145	LOAD_CONST        0
148	LOAD_CONST        999
151	CALL_FUNCTION_3   None
154	POP_TOP           None

155	LOAD_GLOBAL       'Ctl'
158	LOAD_ATTR         'SetKeyboardFocus'
161	LOAD_FAST         'd'
164	LOAD_ATTR         'GetDialogWindow'
167	CALL_FUNCTION_0   None
170	LOAD_FAST         'pwd'
173	LOAD_GLOBAL       'kControlEditTextPart'
176	CALL_FUNCTION_3   None
179	POP_TOP           None

180	LOAD_FAST         'ok'
183	LOAD_CONST        None
186	COMPARE_OP        'is not'
189	POP_JUMP_IF_FALSE '223'

192	LOAD_FAST         'd'
195	LOAD_ATTR         'GetDialogItemAsControl'
198	LOAD_CONST        1
201	CALL_FUNCTION_1   None
204	STORE_FAST        'h'

207	LOAD_FAST         'h'
210	LOAD_ATTR         'SetControlTitle'
213	LOAD_FAST         'ok'
216	CALL_FUNCTION_1   None
219	POP_TOP           None
220	JUMP_FORWARD      '223'
223_0	COME_FROM         '220'

223	LOAD_FAST         'cancel'
226	LOAD_CONST        None
229	COMPARE_OP        'is not'
232	POP_JUMP_IF_FALSE '266'

235	LOAD_FAST         'd'
238	LOAD_ATTR         'GetDialogItemAsControl'
241	LOAD_CONST        2
244	CALL_FUNCTION_1   None
247	STORE_FAST        'h'

250	LOAD_FAST         'h'
253	LOAD_ATTR         'SetControlTitle'
256	LOAD_FAST         'cancel'
259	CALL_FUNCTION_1   None
262	POP_TOP           None
263	JUMP_FORWARD      '266'
266_0	COME_FROM         '263'

266	LOAD_FAST         'd'
269	LOAD_ATTR         'SetDialogDefaultItem'
272	LOAD_GLOBAL       'Dialogs'
275	LOAD_ATTR         'ok'
278	CALL_FUNCTION_1   None
281	POP_TOP           None

282	LOAD_FAST         'd'
285	LOAD_ATTR         'SetDialogCancelItem'
288	LOAD_GLOBAL       'Dialogs'
291	LOAD_ATTR         'cancel'
294	CALL_FUNCTION_1   None
297	POP_TOP           None

298	LOAD_FAST         'd'
301	LOAD_ATTR         'AutoSizeDialog'
304	CALL_FUNCTION_0   None
307	POP_TOP           None

308	LOAD_FAST         'd'
311	LOAD_ATTR         'GetDialogWindow'
314	CALL_FUNCTION_0   None
317	LOAD_ATTR         'ShowWindow'
320	CALL_FUNCTION_0   None
323	POP_TOP           None

324	SETUP_LOOP        '408'

327	LOAD_GLOBAL       'ModalDialog'
330	LOAD_CONST        None
333	CALL_FUNCTION_1   None
336	STORE_FAST        'n'

339	LOAD_FAST         'n'
342	LOAD_CONST        1
345	COMPARE_OP        '=='
348	POP_JUMP_IF_FALSE '388'

351	LOAD_FAST         'd'
354	LOAD_ATTR         'GetDialogItemAsControl'
357	LOAD_CONST        4
360	CALL_FUNCTION_1   None
363	STORE_FAST        'h'

366	LOAD_GLOBAL       'cr2lf'
369	LOAD_GLOBAL       'GetControlData'
372	LOAD_FAST         'pwd'
375	LOAD_GLOBAL       'kControlEditTextPart'
378	LOAD_GLOBAL       'kControlEditTextPasswordTag'
381	CALL_FUNCTION_3   None
384	CALL_FUNCTION_1   None
387	RETURN_END_IF     None

388	LOAD_FAST         'n'
391	LOAD_CONST        2
394	COMPARE_OP        '=='
397	POP_JUMP_IF_FALSE '327'
400	LOAD_CONST        None
403	RETURN_END_IF     None
404	JUMP_BACK         '327'
407	POP_BLOCK         None
408_0	COME_FROM         '324'
408	LOAD_CONST        None
411	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 407


def AskYesNoCancel--- This code section failed: ---

0	LOAD_GLOBAL       '_initialize'
3	CALL_FUNCTION_0   None
6	POP_TOP           None

7	LOAD_GLOBAL       '_interact'
10	CALL_FUNCTION_0   None
13	POP_TOP           None

14	LOAD_GLOBAL       'GetNewDialog'
17	LOAD_FAST         'id'
20	LOAD_CONST        -1
23	CALL_FUNCTION_2   None
26	STORE_FAST        'd'

29	LOAD_FAST         'd'
32	POP_JUMP_IF_TRUE  '52'

35	LOAD_CONST        "EasyDialogs: Can't get DLOG resource with id ="
38	PRINT_ITEM        None
39	LOAD_FAST         'id'
42	PRINT_ITEM_CONT   None
43	LOAD_CONST        ' (missing resource file?)'
46	PRINT_ITEM_CONT   None
47	PRINT_NEWLINE_CONT None

48	LOAD_CONST        None
51	RETURN_END_IF     None

52	LOAD_FAST         'd'
55	LOAD_ATTR         'GetDialogItemAsControl'
58	LOAD_CONST        5
61	CALL_FUNCTION_1   None
64	STORE_FAST        'h'

67	LOAD_GLOBAL       'SetDialogItemText'
70	LOAD_FAST         'h'
73	LOAD_GLOBAL       'lf2cr'
76	LOAD_FAST         'question'
79	CALL_FUNCTION_1   None
82	CALL_FUNCTION_2   None
85	POP_TOP           None

86	LOAD_FAST         'yes'
89	LOAD_CONST        None
92	COMPARE_OP        'is not'
95	POP_JUMP_IF_FALSE '157'

98	LOAD_FAST         'yes'
101	LOAD_CONST        ''
104	COMPARE_OP        '=='
107	POP_JUMP_IF_FALSE '126'

110	LOAD_FAST         'd'
113	LOAD_ATTR         'HideDialogItem'
116	LOAD_CONST        2
119	CALL_FUNCTION_1   None
122	POP_TOP           None
123	JUMP_ABSOLUTE     '157'

126	LOAD_FAST         'd'
129	LOAD_ATTR         'GetDialogItemAsControl'
132	LOAD_CONST        2
135	CALL_FUNCTION_1   None
138	STORE_FAST        'h'

141	LOAD_FAST         'h'
144	LOAD_ATTR         'SetControlTitle'
147	LOAD_FAST         'yes'
150	CALL_FUNCTION_1   None
153	POP_TOP           None
154	JUMP_FORWARD      '157'
157_0	COME_FROM         '154'

157	LOAD_FAST         'no'
160	LOAD_CONST        None
163	COMPARE_OP        'is not'
166	POP_JUMP_IF_FALSE '228'

169	LOAD_FAST         'no'
172	LOAD_CONST        ''
175	COMPARE_OP        '=='
178	POP_JUMP_IF_FALSE '197'

181	LOAD_FAST         'd'
184	LOAD_ATTR         'HideDialogItem'
187	LOAD_CONST        3
190	CALL_FUNCTION_1   None
193	POP_TOP           None
194	JUMP_ABSOLUTE     '228'

197	LOAD_FAST         'd'
200	LOAD_ATTR         'GetDialogItemAsControl'
203	LOAD_CONST        3
206	CALL_FUNCTION_1   None
209	STORE_FAST        'h'

212	LOAD_FAST         'h'
215	LOAD_ATTR         'SetControlTitle'
218	LOAD_FAST         'no'
221	CALL_FUNCTION_1   None
224	POP_TOP           None
225	JUMP_FORWARD      '228'
228_0	COME_FROM         '225'

228	LOAD_FAST         'cancel'
231	LOAD_CONST        None
234	COMPARE_OP        'is not'
237	POP_JUMP_IF_FALSE '299'

240	LOAD_FAST         'cancel'
243	LOAD_CONST        ''
246	COMPARE_OP        '=='
249	POP_JUMP_IF_FALSE '268'

252	LOAD_FAST         'd'
255	LOAD_ATTR         'HideDialogItem'
258	LOAD_CONST        4
261	CALL_FUNCTION_1   None
264	POP_TOP           None
265	JUMP_ABSOLUTE     '299'

268	LOAD_FAST         'd'
271	LOAD_ATTR         'GetDialogItemAsControl'
274	LOAD_CONST        4
277	CALL_FUNCTION_1   None
280	STORE_FAST        'h'

283	LOAD_FAST         'h'
286	LOAD_ATTR         'SetControlTitle'
289	LOAD_FAST         'cancel'
292	CALL_FUNCTION_1   None
295	POP_TOP           None
296	JUMP_FORWARD      '299'
299_0	COME_FROM         '296'

299	LOAD_FAST         'd'
302	LOAD_ATTR         'SetDialogCancelItem'
305	LOAD_CONST        4
308	CALL_FUNCTION_1   None
311	POP_TOP           None

312	LOAD_FAST         'default'
315	LOAD_CONST        1
318	COMPARE_OP        '=='
321	POP_JUMP_IF_FALSE '340'

324	LOAD_FAST         'd'
327	LOAD_ATTR         'SetDialogDefaultItem'
330	LOAD_CONST        2
333	CALL_FUNCTION_1   None
336	POP_TOP           None
337	JUMP_FORWARD      '396'

340	LOAD_FAST         'default'
343	LOAD_CONST        0
346	COMPARE_OP        '=='
349	POP_JUMP_IF_FALSE '368'

352	LOAD_FAST         'd'
355	LOAD_ATTR         'SetDialogDefaultItem'
358	LOAD_CONST        3
361	CALL_FUNCTION_1   None
364	POP_TOP           None
365	JUMP_FORWARD      '396'

368	LOAD_FAST         'default'
371	LOAD_CONST        -1
374	COMPARE_OP        '=='
377	POP_JUMP_IF_FALSE '396'

380	LOAD_FAST         'd'
383	LOAD_ATTR         'SetDialogDefaultItem'
386	LOAD_CONST        4
389	CALL_FUNCTION_1   None
392	POP_TOP           None
393	JUMP_FORWARD      '396'
396_0	COME_FROM         '337'
396_1	COME_FROM         '365'
396_2	COME_FROM         '393'

396	LOAD_FAST         'd'
399	LOAD_ATTR         'AutoSizeDialog'
402	CALL_FUNCTION_0   None
405	POP_TOP           None

406	LOAD_FAST         'd'
409	LOAD_ATTR         'GetDialogWindow'
412	CALL_FUNCTION_0   None
415	LOAD_ATTR         'ShowWindow'
418	CALL_FUNCTION_0   None
421	POP_TOP           None

422	SETUP_LOOP        '505'

425	LOAD_GLOBAL       'ModalDialog'
428	LOAD_CONST        None
431	CALL_FUNCTION_1   None
434	STORE_FAST        'n'

437	LOAD_FAST         'n'
440	LOAD_CONST        1
443	COMPARE_OP        '=='
446	POP_JUMP_IF_FALSE '453'
449	LOAD_FAST         'default'
452	RETURN_END_IF     None

453	LOAD_FAST         'n'
456	LOAD_CONST        2
459	COMPARE_OP        '=='
462	POP_JUMP_IF_FALSE '469'
465	LOAD_CONST        1
468	RETURN_END_IF     None

469	LOAD_FAST         'n'
472	LOAD_CONST        3
475	COMPARE_OP        '=='
478	POP_JUMP_IF_FALSE '485'
481	LOAD_CONST        0
484	RETURN_END_IF     None

485	LOAD_FAST         'n'
488	LOAD_CONST        4
491	COMPARE_OP        '=='
494	POP_JUMP_IF_FALSE '425'
497	LOAD_CONST        -1
500	RETURN_END_IF     None
501	JUMP_BACK         '425'
504	POP_BLOCK         None
505_0	COME_FROM         '422'
505	LOAD_CONST        None
508	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 504


screenbounds = Qd.GetQDGlobalsScreenBits().bounds
screenbounds = (screenbounds[0] + 4,
 screenbounds[1] + 4,
 screenbounds[2] - 4,
 screenbounds[3] - 4)
kControlProgressBarIndeterminateTag = 'inde'

class ProgressBar:

    def __init__(self, title = 'Working...', maxval = 0, label = '', id = 263):
        self.w = None
        self.d = None
        _initialize()
        self.d = GetNewDialog(id, -1)
        self.w = self.d.GetDialogWindow()
        self.label(label)
        self.title(title)
        self.set(0, maxval)
        self.d.AutoSizeDialog()
        self.w.ShowWindow()
        self.d.DrawDialog()
        return

    def __del__(self):
        if self.w:
            self.w.BringToFront()
            self.w.HideWindow()
        del self.w
        del self.d

    def title(self, newstr = ''):
        """title(text) - Set title of progress window"""
        self.w.BringToFront()
        self.w.SetWTitle(newstr)

    def label(self, *newstr):
        """label(text) - Set text in progress box"""
        self.w.BringToFront()
        if newstr:
            self._label = lf2cr(newstr[0])
        text_h = self.d.GetDialogItemAsControl(2)
        SetDialogItemText(text_h, self._label)

    def _update(self, value):
        maxval = self.maxval
        if maxval == 0:
            Ctl.IdleControls(self.w)
        else:
            if maxval > 32767:
                value = int(value / (maxval / 32767.0))
                maxval = 32767
            maxval = int(maxval)
            value = int(value)
            progbar = self.d.GetDialogItemAsControl(3)
            progbar.SetControlMaximum(maxval)
            progbar.SetControlValue(value)
        ready, ev = Evt.WaitNextEvent(Events.mDownMask, 1)
        if ready:
            what, msg, when, where, mod = ev
            part = Win.FindWindow(where)[0]
            if Dlg.IsDialogEvent(ev):
                ds = Dlg.DialogSelect(ev)
                if ds[0] and ds[1] == self.d and ds[-1] == 1:
                    self.w.HideWindow()
                    self.w = None
                    self.d = None
                    raise KeyboardInterrupt, ev
            elif part == 4:
                self.w.DragWindow(where, screenbounds)
            else:
                MacOS.HandleEvent(ev)
        return

    def set(self, value, max = None):
        """set(value) - Set progress bar position"""
        if max is not None:
            self.maxval = max
            bar = self.d.GetDialogItemAsControl(3)
            if max <= 0:
                bar.SetControlData(0, kControlProgressBarIndeterminateTag, '\x01')
            else:
                bar.SetControlData(0, kControlProgressBarIndeterminateTag, '\x00')
        if value < 0:
            value = 0
        elif value > self.maxval:
            value = self.maxval
        self.curval = value
        self._update(value)
        return

    def inc(self, n = 1):
        """inc(amt) - Increment progress bar position"""
        self.set(self.curval + n)


ARGV_ID = 265
ARGV_ITEM_OK = 1
ARGV_ITEM_CANCEL = 2
ARGV_OPTION_GROUP = 3
ARGV_OPTION_EXPLAIN = 4
ARGV_OPTION_VALUE = 5
ARGV_OPTION_ADD = 6
ARGV_COMMAND_GROUP = 7
ARGV_COMMAND_EXPLAIN = 8
ARGV_COMMAND_ADD = 9
ARGV_ADD_OLDFILE = 10
ARGV_ADD_NEWFILE = 11
ARGV_ADD_FOLDER = 12
ARGV_CMDLINE_GROUP = 13
ARGV_CMDLINE_DATA = 14

def _setmenu(control, items):
    mhandle = control.GetControlData_Handle(Controls.kControlMenuPart, Controls.kControlPopupButtonMenuHandleTag)
    menu = Menu.as_Menu(mhandle)
    for item in items:
        if type(item) == type(()):
            label = item[0]
        else:
            label = item
        if label[-1] == '=' or label[-1] == ':':
            label = label[:-1]
        menu.AppendMenu(label)

    control.SetControlMinimum(1)
    control.SetControlMaximum(len(items) + 1)


def _selectoption(d, optionlist, idx):
    if idx < 0 or idx >= len(optionlist):
        MacOS.SysBeep()
        return
    option = optionlist[idx]
    if type(option) == type(()):
        if len(option) == 4:
            help = option[2]
        elif len(option) > 1:
            help = option[-1]
        else:
            help = ''
    else:
        help = ''
    h = d.GetDialogItemAsControl(ARGV_OPTION_EXPLAIN)
    if help and len(help) > 250:
        help = help[:250] + '...'
    Dlg.SetDialogItemText(h, help)
    hasvalue = 0
    if type(option) == type(()):
        label = option[0]
    else:
        label = option
    if label[-1] == '=' or label[-1] == ':':
        hasvalue = 1
    h = d.GetDialogItemAsControl(ARGV_OPTION_VALUE)
    Dlg.SetDialogItemText(h, '')
    if hasvalue:
        d.ShowDialogItem(ARGV_OPTION_VALUE)
        d.SelectDialogItemText(ARGV_OPTION_VALUE, 0, 0)
    else:
        d.HideDialogItem(ARGV_OPTION_VALUE)


def GetArgv--- This code section failed: ---

0	LOAD_GLOBAL       '_initialize'
3	CALL_FUNCTION_0   None
6	POP_TOP           None

7	LOAD_GLOBAL       '_interact'
10	CALL_FUNCTION_0   None
13	POP_TOP           None

14	LOAD_GLOBAL       'GetNewDialog'
17	LOAD_FAST         'id'
20	LOAD_CONST        -1
23	CALL_FUNCTION_2   None
26	STORE_FAST        'd'

29	LOAD_FAST         'd'
32	POP_JUMP_IF_TRUE  '52'

35	LOAD_CONST        "EasyDialogs: Can't get DLOG resource with id ="
38	PRINT_ITEM        None
39	LOAD_FAST         'id'
42	PRINT_ITEM_CONT   None
43	LOAD_CONST        ' (missing resource file?)'
46	PRINT_ITEM_CONT   None
47	PRINT_NEWLINE_CONT None

48	LOAD_CONST        None
51	RETURN_END_IF     None

52	LOAD_FAST         'optionlist'
55	POP_JUMP_IF_FALSE '99'

58	LOAD_GLOBAL       '_setmenu'
61	LOAD_FAST         'd'
64	LOAD_ATTR         'GetDialogItemAsControl'
67	LOAD_GLOBAL       'ARGV_OPTION_GROUP'
70	CALL_FUNCTION_1   None
73	LOAD_FAST         'optionlist'
76	CALL_FUNCTION_2   None
79	POP_TOP           None

80	LOAD_GLOBAL       '_selectoption'
83	LOAD_FAST         'd'
86	LOAD_FAST         'optionlist'
89	LOAD_CONST        0
92	CALL_FUNCTION_3   None
95	POP_TOP           None
96	JUMP_FORWARD      '118'

99	LOAD_FAST         'd'
102	LOAD_ATTR         'GetDialogItemAsControl'
105	LOAD_GLOBAL       'ARGV_OPTION_GROUP'
108	CALL_FUNCTION_1   None
111	LOAD_ATTR         'DeactivateControl'
114	CALL_FUNCTION_0   None
117	POP_TOP           None
118_0	COME_FROM         '96'

118	LOAD_FAST         'commandlist'
121	POP_JUMP_IF_FALSE '247'

124	LOAD_GLOBAL       '_setmenu'
127	LOAD_FAST         'd'
130	LOAD_ATTR         'GetDialogItemAsControl'
133	LOAD_GLOBAL       'ARGV_COMMAND_GROUP'
136	CALL_FUNCTION_1   None
139	LOAD_FAST         'commandlist'
142	CALL_FUNCTION_2   None
145	POP_TOP           None

146	LOAD_GLOBAL       'type'
149	LOAD_FAST         'commandlist'
152	LOAD_CONST        0
155	BINARY_SUBSCR     None
156	CALL_FUNCTION_1   None
159	LOAD_GLOBAL       'type'
162	LOAD_CONST        ()
165	CALL_FUNCTION_1   None
168	COMPARE_OP        '=='
171	POP_JUMP_IF_FALSE '266'
174	LOAD_GLOBAL       'len'
177	LOAD_FAST         'commandlist'
180	LOAD_CONST        0
183	BINARY_SUBSCR     None
184	CALL_FUNCTION_1   None
187	LOAD_CONST        1
190	COMPARE_OP        '>'
193_0	COME_FROM         '171'
193	POP_JUMP_IF_FALSE '266'

196	LOAD_FAST         'commandlist'
199	LOAD_CONST        0
202	BINARY_SUBSCR     None
203	LOAD_CONST        -1
206	BINARY_SUBSCR     None
207	STORE_FAST        'help'

210	LOAD_FAST         'd'
213	LOAD_ATTR         'GetDialogItemAsControl'
216	LOAD_GLOBAL       'ARGV_COMMAND_EXPLAIN'
219	CALL_FUNCTION_1   None
222	STORE_FAST        'h'

225	LOAD_GLOBAL       'Dlg'
228	LOAD_ATTR         'SetDialogItemText'
231	LOAD_FAST         'h'
234	LOAD_FAST         'help'
237	CALL_FUNCTION_2   None
240	POP_TOP           None
241	JUMP_ABSOLUTE     '266'
244	JUMP_FORWARD      '266'

247	LOAD_FAST         'd'
250	LOAD_ATTR         'GetDialogItemAsControl'
253	LOAD_GLOBAL       'ARGV_COMMAND_GROUP'
256	CALL_FUNCTION_1   None
259	LOAD_ATTR         'DeactivateControl'
262	CALL_FUNCTION_0   None
265	POP_TOP           None
266_0	COME_FROM         '244'

266	LOAD_FAST         'addoldfile'
269	POP_JUMP_IF_TRUE  '294'

272	LOAD_FAST         'd'
275	LOAD_ATTR         'GetDialogItemAsControl'
278	LOAD_GLOBAL       'ARGV_ADD_OLDFILE'
281	CALL_FUNCTION_1   None
284	LOAD_ATTR         'DeactivateControl'
287	CALL_FUNCTION_0   None
290	POP_TOP           None
291	JUMP_FORWARD      '294'
294_0	COME_FROM         '291'

294	LOAD_FAST         'addnewfile'
297	POP_JUMP_IF_TRUE  '322'

300	LOAD_FAST         'd'
303	LOAD_ATTR         'GetDialogItemAsControl'
306	LOAD_GLOBAL       'ARGV_ADD_NEWFILE'
309	CALL_FUNCTION_1   None
312	LOAD_ATTR         'DeactivateControl'
315	CALL_FUNCTION_0   None
318	POP_TOP           None
319	JUMP_FORWARD      '322'
322_0	COME_FROM         '319'

322	LOAD_FAST         'addfolder'
325	POP_JUMP_IF_TRUE  '350'

328	LOAD_FAST         'd'
331	LOAD_ATTR         'GetDialogItemAsControl'
334	LOAD_GLOBAL       'ARGV_ADD_FOLDER'
337	CALL_FUNCTION_1   None
340	LOAD_ATTR         'DeactivateControl'
343	CALL_FUNCTION_0   None
346	POP_TOP           None
347	JUMP_FORWARD      '350'
350_0	COME_FROM         '347'

350	LOAD_FAST         'd'
353	LOAD_ATTR         'SetDialogDefaultItem'
356	LOAD_GLOBAL       'ARGV_ITEM_OK'
359	CALL_FUNCTION_1   None
362	POP_TOP           None

363	LOAD_FAST         'd'
366	LOAD_ATTR         'SetDialogCancelItem'
369	LOAD_GLOBAL       'ARGV_ITEM_CANCEL'
372	CALL_FUNCTION_1   None
375	POP_TOP           None

376	LOAD_FAST         'd'
379	LOAD_ATTR         'GetDialogWindow'
382	CALL_FUNCTION_0   None
385	LOAD_ATTR         'ShowWindow'
388	CALL_FUNCTION_0   None
391	POP_TOP           None

392	LOAD_FAST         'd'
395	LOAD_ATTR         'DrawDialog'
398	CALL_FUNCTION_0   None
401	POP_TOP           None

402	LOAD_GLOBAL       'hasattr'
405	LOAD_GLOBAL       'MacOS'
408	LOAD_CONST        'SchedParams'
411	CALL_FUNCTION_2   None
414	POP_JUMP_IF_FALSE '438'

417	LOAD_GLOBAL       'MacOS'
420	LOAD_ATTR         'SchedParams'
423	LOAD_CONST        1
426	LOAD_CONST        0
429	CALL_FUNCTION_2   None
432	STORE_FAST        'appsw'
435	JUMP_FORWARD      '438'
438_0	COME_FROM         '435'

438	SETUP_FINALLY     '1826'

441	SETUP_LOOP        '1531'

444	BUILD_LIST_0      None
447	STORE_FAST        'stringstoadd'

450	LOAD_GLOBAL       'ModalDialog'
453	LOAD_CONST        None
456	CALL_FUNCTION_1   None
459	STORE_FAST        'n'

462	LOAD_FAST         'n'
465	LOAD_GLOBAL       'ARGV_ITEM_OK'
468	COMPARE_OP        '=='
471	POP_JUMP_IF_FALSE '478'

474	BREAK_LOOP        None
475	JUMP_FORWARD      '1326'

478	LOAD_FAST         'n'
481	LOAD_GLOBAL       'ARGV_ITEM_CANCEL'
484	COMPARE_OP        '=='
487	POP_JUMP_IF_FALSE '499'

490	LOAD_GLOBAL       'SystemExit'
493	RAISE_VARARGS_1   None
496	JUMP_FORWARD      '1326'

499	LOAD_FAST         'n'
502	LOAD_GLOBAL       'ARGV_OPTION_GROUP'
505	COMPARE_OP        '=='
508	POP_JUMP_IF_FALSE '555'

511	LOAD_FAST         'd'
514	LOAD_ATTR         'GetDialogItemAsControl'
517	LOAD_GLOBAL       'ARGV_OPTION_GROUP'
520	CALL_FUNCTION_1   None
523	LOAD_ATTR         'GetControlValue'
526	CALL_FUNCTION_0   None
529	LOAD_CONST        1
532	BINARY_SUBTRACT   None
533	STORE_FAST        'idx'

536	LOAD_GLOBAL       '_selectoption'
539	LOAD_FAST         'd'
542	LOAD_FAST         'optionlist'
545	LOAD_FAST         'idx'
548	CALL_FUNCTION_3   None
551	POP_TOP           None
552	JUMP_FORWARD      '1326'

555	LOAD_FAST         'n'
558	LOAD_GLOBAL       'ARGV_OPTION_VALUE'
561	COMPARE_OP        '=='
564	POP_JUMP_IF_FALSE '570'

567	JUMP_FORWARD      '1326'

570	LOAD_FAST         'n'
573	LOAD_GLOBAL       'ARGV_OPTION_ADD'
576	COMPARE_OP        '=='
579	POP_JUMP_IF_FALSE '857'

582	LOAD_FAST         'd'
585	LOAD_ATTR         'GetDialogItemAsControl'
588	LOAD_GLOBAL       'ARGV_OPTION_GROUP'
591	CALL_FUNCTION_1   None
594	LOAD_ATTR         'GetControlValue'
597	CALL_FUNCTION_0   None
600	LOAD_CONST        1
603	BINARY_SUBTRACT   None
604	STORE_FAST        'idx'

607	LOAD_CONST        0
610	LOAD_FAST         'idx'
613	DUP_TOP           None
614	ROT_THREE         None
615	COMPARE_OP        '<='
618	JUMP_IF_FALSE_OR_POP '636'
621	LOAD_GLOBAL       'len'
624	LOAD_FAST         'optionlist'
627	CALL_FUNCTION_1   None
630	COMPARE_OP        '<'
633	JUMP_FORWARD      '638'
636_0	COME_FROM         '618'
636	ROT_TWO           None
637	POP_TOP           None
638_0	COME_FROM         '633'
638	POP_JUMP_IF_FALSE '844'

641	LOAD_FAST         'optionlist'
644	LOAD_FAST         'idx'
647	BINARY_SUBSCR     None
648	STORE_FAST        'option'

651	LOAD_GLOBAL       'type'
654	LOAD_FAST         'option'
657	CALL_FUNCTION_1   None
660	LOAD_GLOBAL       'type'
663	LOAD_CONST        ()
666	CALL_FUNCTION_1   None
669	COMPARE_OP        '=='
672	POP_JUMP_IF_FALSE '688'

675	LOAD_FAST         'option'
678	LOAD_CONST        0
681	BINARY_SUBSCR     None
682	STORE_FAST        'option'
685	JUMP_FORWARD      '688'
688_0	COME_FROM         '685'

688	LOAD_FAST         'option'
691	LOAD_CONST        -1
694	BINARY_SUBSCR     None
695	LOAD_CONST        '='
698	COMPARE_OP        '=='
701	POP_JUMP_IF_TRUE  '720'
704	LOAD_FAST         'option'
707	LOAD_CONST        -1
710	BINARY_SUBSCR     None
711	LOAD_CONST        ':'
714	COMPARE_OP        '=='
717_0	COME_FROM         '701'
717	POP_JUMP_IF_FALSE '763'

720	LOAD_FAST         'option'
723	LOAD_CONST        -1
726	SLICE+2           None
727	STORE_FAST        'option'

730	LOAD_FAST         'd'
733	LOAD_ATTR         'GetDialogItemAsControl'
736	LOAD_GLOBAL       'ARGV_OPTION_VALUE'
739	CALL_FUNCTION_1   None
742	STORE_FAST        'h'

745	LOAD_GLOBAL       'Dlg'
748	LOAD_ATTR         'GetDialogItemText'
751	LOAD_FAST         'h'
754	CALL_FUNCTION_1   None
757	STORE_FAST        'value'
760	JUMP_FORWARD      '769'

763	LOAD_CONST        ''
766	STORE_FAST        'value'
769_0	COME_FROM         '760'

769	LOAD_GLOBAL       'len'
772	LOAD_FAST         'option'
775	CALL_FUNCTION_1   None
778	LOAD_CONST        1
781	COMPARE_OP        '=='
784	POP_JUMP_IF_FALSE '800'

787	LOAD_CONST        '-'
790	LOAD_FAST         'option'
793	BINARY_ADD        None
794	STORE_FAST        'stringtoadd'
797	JUMP_FORWARD      '810'

800	LOAD_CONST        '--'
803	LOAD_FAST         'option'
806	BINARY_ADD        None
807	STORE_FAST        'stringtoadd'
810_0	COME_FROM         '797'

810	LOAD_FAST         'stringtoadd'
813	BUILD_LIST_1      None
816	STORE_FAST        'stringstoadd'

819	LOAD_FAST         'value'
822	POP_JUMP_IF_FALSE '854'

825	LOAD_FAST         'stringstoadd'
828	LOAD_ATTR         'append'
831	LOAD_FAST         'value'
834	CALL_FUNCTION_1   None
837	POP_TOP           None
838	JUMP_ABSOLUTE     '854'
841	JUMP_ABSOLUTE     '1326'

844	LOAD_GLOBAL       'MacOS'
847	LOAD_ATTR         'SysBeep'
850	CALL_FUNCTION_0   None
853	POP_TOP           None
854	JUMP_FORWARD      '1326'

857	LOAD_FAST         'n'
860	LOAD_GLOBAL       'ARGV_COMMAND_GROUP'
863	COMPARE_OP        '=='
866	POP_JUMP_IF_FALSE '1029'

869	LOAD_FAST         'd'
872	LOAD_ATTR         'GetDialogItemAsControl'
875	LOAD_GLOBAL       'ARGV_COMMAND_GROUP'
878	CALL_FUNCTION_1   None
881	LOAD_ATTR         'GetControlValue'
884	CALL_FUNCTION_0   None
887	LOAD_CONST        1
890	BINARY_SUBTRACT   None
891	STORE_FAST        'idx'

894	LOAD_CONST        0
897	LOAD_FAST         'idx'
900	DUP_TOP           None
901	ROT_THREE         None
902	COMPARE_OP        '<='
905	JUMP_IF_FALSE_OR_POP '923'
908	LOAD_GLOBAL       'len'
911	LOAD_FAST         'commandlist'
914	CALL_FUNCTION_1   None
917	COMPARE_OP        '<'
920	JUMP_FORWARD      '925'
923_0	COME_FROM         '905'
923	ROT_TWO           None
924	POP_TOP           None
925_0	COME_FROM         '920'
925	POP_JUMP_IF_FALSE '1326'
928	LOAD_GLOBAL       'type'
931	LOAD_FAST         'commandlist'
934	LOAD_FAST         'idx'
937	BINARY_SUBSCR     None
938	CALL_FUNCTION_1   None
941	LOAD_GLOBAL       'type'
944	LOAD_CONST        ()
947	CALL_FUNCTION_1   None
950	COMPARE_OP        '=='
953_0	COME_FROM         '925'
953	POP_JUMP_IF_FALSE '1326'

956	LOAD_GLOBAL       'len'
959	LOAD_FAST         'commandlist'
962	LOAD_FAST         'idx'
965	BINARY_SUBSCR     None
966	CALL_FUNCTION_1   None
969	LOAD_CONST        1
972	COMPARE_OP        '>'
975_0	COME_FROM         '953'
975	POP_JUMP_IF_FALSE '1326'

978	LOAD_FAST         'commandlist'
981	LOAD_FAST         'idx'
984	BINARY_SUBSCR     None
985	LOAD_CONST        -1
988	BINARY_SUBSCR     None
989	STORE_FAST        'help'

992	LOAD_FAST         'd'
995	LOAD_ATTR         'GetDialogItemAsControl'
998	LOAD_GLOBAL       'ARGV_COMMAND_EXPLAIN'
1001	CALL_FUNCTION_1   None
1004	STORE_FAST        'h'

1007	LOAD_GLOBAL       'Dlg'
1010	LOAD_ATTR         'SetDialogItemText'
1013	LOAD_FAST         'h'
1016	LOAD_FAST         'help'
1019	CALL_FUNCTION_2   None
1022	POP_TOP           None
1023	JUMP_ABSOLUTE     '1326'
1026	JUMP_FORWARD      '1326'

1029	LOAD_FAST         'n'
1032	LOAD_GLOBAL       'ARGV_COMMAND_ADD'
1035	COMPARE_OP        '=='
1038	POP_JUMP_IF_FALSE '1172'

1041	LOAD_FAST         'd'
1044	LOAD_ATTR         'GetDialogItemAsControl'
1047	LOAD_GLOBAL       'ARGV_COMMAND_GROUP'
1050	CALL_FUNCTION_1   None
1053	LOAD_ATTR         'GetControlValue'
1056	CALL_FUNCTION_0   None
1059	LOAD_CONST        1
1062	BINARY_SUBTRACT   None
1063	STORE_FAST        'idx'

1066	LOAD_CONST        0
1069	LOAD_FAST         'idx'
1072	DUP_TOP           None
1073	ROT_THREE         None
1074	COMPARE_OP        '<='
1077	JUMP_IF_FALSE_OR_POP '1095'
1080	LOAD_GLOBAL       'len'
1083	LOAD_FAST         'commandlist'
1086	CALL_FUNCTION_1   None
1089	COMPARE_OP        '<'
1092	JUMP_FORWARD      '1097'
1095_0	COME_FROM         '1077'
1095	ROT_TWO           None
1096	POP_TOP           None
1097_0	COME_FROM         '1092'
1097	POP_JUMP_IF_FALSE '1159'

1100	LOAD_FAST         'commandlist'
1103	LOAD_FAST         'idx'
1106	BINARY_SUBSCR     None
1107	STORE_FAST        'command'

1110	LOAD_GLOBAL       'type'
1113	LOAD_FAST         'command'
1116	CALL_FUNCTION_1   None
1119	LOAD_GLOBAL       'type'
1122	LOAD_CONST        ()
1125	CALL_FUNCTION_1   None
1128	COMPARE_OP        '=='
1131	POP_JUMP_IF_FALSE '1147'

1134	LOAD_FAST         'command'
1137	LOAD_CONST        0
1140	BINARY_SUBSCR     None
1141	STORE_FAST        'command'
1144	JUMP_FORWARD      '1147'
1147_0	COME_FROM         '1144'

1147	LOAD_FAST         'command'
1150	BUILD_LIST_1      None
1153	STORE_FAST        'stringstoadd'
1156	JUMP_ABSOLUTE     '1326'

1159	LOAD_GLOBAL       'MacOS'
1162	LOAD_ATTR         'SysBeep'
1165	CALL_FUNCTION_0   None
1168	POP_TOP           None
1169	JUMP_FORWARD      '1326'

1172	LOAD_FAST         'n'
1175	LOAD_GLOBAL       'ARGV_ADD_OLDFILE'
1178	COMPARE_OP        '=='
1181	POP_JUMP_IF_FALSE '1214'

1184	LOAD_GLOBAL       'AskFileForOpen'
1187	CALL_FUNCTION_0   None
1190	STORE_FAST        'pathname'

1193	LOAD_FAST         'pathname'
1196	POP_JUMP_IF_FALSE '1326'

1199	LOAD_FAST         'pathname'
1202	BUILD_LIST_1      None
1205	STORE_FAST        'stringstoadd'
1208	JUMP_ABSOLUTE     '1326'
1211	JUMP_FORWARD      '1326'

1214	LOAD_FAST         'n'
1217	LOAD_GLOBAL       'ARGV_ADD_NEWFILE'
1220	COMPARE_OP        '=='
1223	POP_JUMP_IF_FALSE '1256'

1226	LOAD_GLOBAL       'AskFileForSave'
1229	CALL_FUNCTION_0   None
1232	STORE_FAST        'pathname'

1235	LOAD_FAST         'pathname'
1238	POP_JUMP_IF_FALSE '1326'

1241	LOAD_FAST         'pathname'
1244	BUILD_LIST_1      None
1247	STORE_FAST        'stringstoadd'
1250	JUMP_ABSOLUTE     '1326'
1253	JUMP_FORWARD      '1326'

1256	LOAD_FAST         'n'
1259	LOAD_GLOBAL       'ARGV_ADD_FOLDER'
1262	COMPARE_OP        '=='
1265	POP_JUMP_IF_FALSE '1298'

1268	LOAD_GLOBAL       'AskFolder'
1271	CALL_FUNCTION_0   None
1274	STORE_FAST        'pathname'

1277	LOAD_FAST         'pathname'
1280	POP_JUMP_IF_FALSE '1326'

1283	LOAD_FAST         'pathname'
1286	BUILD_LIST_1      None
1289	STORE_FAST        'stringstoadd'
1292	JUMP_ABSOLUTE     '1326'
1295	JUMP_FORWARD      '1326'

1298	LOAD_FAST         'n'
1301	LOAD_GLOBAL       'ARGV_CMDLINE_DATA'
1304	COMPARE_OP        '=='
1307	POP_JUMP_IF_FALSE '1313'

1310	JUMP_FORWARD      '1326'

1313	LOAD_GLOBAL       'RuntimeError'
1316	LOAD_CONST        'Unknown dialog item %d'
1319	LOAD_FAST         'n'
1322	BINARY_MODULO     None
1323	RAISE_VARARGS_2   None
1326_0	COME_FROM         '475'
1326_1	COME_FROM         '496'
1326_2	COME_FROM         '552'
1326_3	COME_FROM         '567'
1326_4	COME_FROM         '854'
1326_5	COME_FROM         '1026'
1326_6	COME_FROM         '1169'
1326_7	COME_FROM         '1211'
1326_8	COME_FROM         '1253'
1326_9	COME_FROM         '1295'
1326_10	COME_FROM         '1310'

1326	SETUP_LOOP        '1527'
1329	LOAD_FAST         'stringstoadd'
1332	GET_ITER          None
1333	FOR_ITER          '1526'
1336	STORE_FAST        'stringtoadd'

1339	LOAD_CONST        '"'
1342	LOAD_FAST         'stringtoadd'
1345	COMPARE_OP        'in'
1348	POP_JUMP_IF_TRUE  '1375'
1351	LOAD_CONST        "'"
1354	LOAD_FAST         'stringtoadd'
1357	COMPARE_OP        'in'
1360	POP_JUMP_IF_TRUE  '1375'
1363	LOAD_CONST        ' '
1366	LOAD_FAST         'stringtoadd'
1369	COMPARE_OP        'in'
1372_0	COME_FROM         '1348'
1372_1	COME_FROM         '1360'
1372	POP_JUMP_IF_FALSE '1390'

1375	LOAD_GLOBAL       'repr'
1378	LOAD_FAST         'stringtoadd'
1381	CALL_FUNCTION_1   None
1384	STORE_FAST        'stringtoadd'
1387	JUMP_FORWARD      '1390'
1390_0	COME_FROM         '1387'

1390	LOAD_FAST         'd'
1393	LOAD_ATTR         'GetDialogItemAsControl'
1396	LOAD_GLOBAL       'ARGV_CMDLINE_DATA'
1399	CALL_FUNCTION_1   None
1402	STORE_FAST        'h'

1405	LOAD_GLOBAL       'GetDialogItemText'
1408	LOAD_FAST         'h'
1411	CALL_FUNCTION_1   None
1414	STORE_FAST        'oldstr'

1417	LOAD_FAST         'oldstr'
1420	POP_JUMP_IF_FALSE '1452'
1423	LOAD_FAST         'oldstr'
1426	LOAD_CONST        -1
1429	BINARY_SUBSCR     None
1430	LOAD_CONST        ' '
1433	COMPARE_OP        '!='
1436_0	COME_FROM         '1420'
1436	POP_JUMP_IF_FALSE '1452'

1439	LOAD_FAST         'oldstr'
1442	LOAD_CONST        ' '
1445	BINARY_ADD        None
1446	STORE_FAST        'oldstr'
1449	JUMP_FORWARD      '1452'
1452_0	COME_FROM         '1449'

1452	LOAD_FAST         'oldstr'
1455	LOAD_FAST         'stringtoadd'
1458	BINARY_ADD        None
1459	STORE_FAST        'oldstr'

1462	LOAD_FAST         'oldstr'
1465	LOAD_CONST        -1
1468	BINARY_SUBSCR     None
1469	LOAD_CONST        ' '
1472	COMPARE_OP        '!='
1475	POP_JUMP_IF_FALSE '1491'

1478	LOAD_FAST         'oldstr'
1481	LOAD_CONST        ' '
1484	BINARY_ADD        None
1485	STORE_FAST        'oldstr'
1488	JUMP_FORWARD      '1491'
1491_0	COME_FROM         '1488'

1491	LOAD_GLOBAL       'SetDialogItemText'
1494	LOAD_FAST         'h'
1497	LOAD_FAST         'oldstr'
1500	CALL_FUNCTION_2   None
1503	POP_TOP           None

1504	LOAD_FAST         'd'
1507	LOAD_ATTR         'SelectDialogItemText'
1510	LOAD_GLOBAL       'ARGV_CMDLINE_DATA'
1513	LOAD_CONST        32767
1516	LOAD_CONST        32767
1519	CALL_FUNCTION_3   None
1522	POP_TOP           None
1523	JUMP_BACK         '1333'
1526	POP_BLOCK         None
1527_0	COME_FROM         '1326'
1527	JUMP_BACK         '444'
1530	POP_BLOCK         None
1531_0	COME_FROM         '441'

1531	LOAD_FAST         'd'
1534	LOAD_ATTR         'GetDialogItemAsControl'
1537	LOAD_GLOBAL       'ARGV_CMDLINE_DATA'
1540	CALL_FUNCTION_1   None
1543	STORE_FAST        'h'

1546	LOAD_GLOBAL       'GetDialogItemText'
1549	LOAD_FAST         'h'
1552	CALL_FUNCTION_1   None
1555	STORE_FAST        'oldstr'

1558	LOAD_GLOBAL       'string'
1561	LOAD_ATTR         'split'
1564	LOAD_FAST         'oldstr'
1567	CALL_FUNCTION_1   None
1570	STORE_FAST        'tmplist'

1573	BUILD_LIST_0      None
1576	STORE_FAST        'newlist'

1579	SETUP_LOOP        '1818'
1582	LOAD_FAST         'tmplist'
1585	POP_JUMP_IF_FALSE '1817'

1588	LOAD_FAST         'tmplist'
1591	LOAD_CONST        0
1594	BINARY_SUBSCR     None
1595	STORE_FAST        'item'

1598	LOAD_FAST         'tmplist'
1601	LOAD_CONST        0
1604	DELETE_SUBSCR     None

1605	LOAD_FAST         'item'
1608	LOAD_CONST        0
1611	BINARY_SUBSCR     None
1612	LOAD_CONST        '"'
1615	COMPARE_OP        '=='
1618	POP_JUMP_IF_FALSE '1703'

1621	SETUP_LOOP        '1687'
1624	LOAD_FAST         'item'
1627	LOAD_CONST        -1
1630	BINARY_SUBSCR     None
1631	LOAD_CONST        '"'
1634	COMPARE_OP        '!='
1637	POP_JUMP_IF_FALSE '1686'

1640	LOAD_FAST         'tmplist'
1643	POP_JUMP_IF_TRUE  '1658'

1646	LOAD_GLOBAL       'RuntimeError'
1649	LOAD_CONST        'Unterminated quoted argument'
1652	RAISE_VARARGS_2   None
1655	JUMP_FORWARD      '1658'
1658_0	COME_FROM         '1655'

1658	LOAD_FAST         'item'
1661	LOAD_CONST        ' '
1664	BINARY_ADD        None
1665	LOAD_FAST         'tmplist'
1668	LOAD_CONST        0
1671	BINARY_SUBSCR     None
1672	BINARY_ADD        None
1673	STORE_FAST        'item'

1676	LOAD_FAST         'tmplist'
1679	LOAD_CONST        0
1682	DELETE_SUBSCR     None
1683	JUMP_BACK         '1624'
1686	POP_BLOCK         None
1687_0	COME_FROM         '1621'

1687	LOAD_FAST         'item'
1690	LOAD_CONST        1
1693	LOAD_CONST        -1
1696	SLICE+3           None
1697	STORE_FAST        'item'
1700	JUMP_FORWARD      '1703'
1703_0	COME_FROM         '1700'

1703	LOAD_FAST         'item'
1706	LOAD_CONST        0
1709	BINARY_SUBSCR     None
1710	LOAD_CONST        "'"
1713	COMPARE_OP        '=='
1716	POP_JUMP_IF_FALSE '1801'

1719	SETUP_LOOP        '1785'
1722	LOAD_FAST         'item'
1725	LOAD_CONST        -1
1728	BINARY_SUBSCR     None
1729	LOAD_CONST        "'"
1732	COMPARE_OP        '!='
1735	POP_JUMP_IF_FALSE '1784'

1738	LOAD_FAST         'tmplist'
1741	POP_JUMP_IF_TRUE  '1756'

1744	LOAD_GLOBAL       'RuntimeError'
1747	LOAD_CONST        'Unterminated quoted argument'
1750	RAISE_VARARGS_2   None
1753	JUMP_FORWARD      '1756'
1756_0	COME_FROM         '1753'

1756	LOAD_FAST         'item'
1759	LOAD_CONST        ' '
1762	BINARY_ADD        None
1763	LOAD_FAST         'tmplist'
1766	LOAD_CONST        0
1769	BINARY_SUBSCR     None
1770	BINARY_ADD        None
1771	STORE_FAST        'item'

1774	LOAD_FAST         'tmplist'
1777	LOAD_CONST        0
1780	DELETE_SUBSCR     None
1781	JUMP_BACK         '1722'
1784	POP_BLOCK         None
1785_0	COME_FROM         '1719'

1785	LOAD_FAST         'item'
1788	LOAD_CONST        1
1791	LOAD_CONST        -1
1794	SLICE+3           None
1795	STORE_FAST        'item'
1798	JUMP_FORWARD      '1801'
1801_0	COME_FROM         '1798'

1801	LOAD_FAST         'newlist'
1804	LOAD_ATTR         'append'
1807	LOAD_FAST         'item'
1810	CALL_FUNCTION_1   None
1813	POP_TOP           None
1814	JUMP_BACK         '1582'
1817	POP_BLOCK         None
1818_0	COME_FROM         '1579'

1818	LOAD_FAST         'newlist'
1821	RETURN_VALUE      None
1822	POP_BLOCK         None
1823	LOAD_CONST        None
1826_0	COME_FROM         '438'

1826	LOAD_GLOBAL       'hasattr'
1829	LOAD_GLOBAL       'MacOS'
1832	LOAD_CONST        'SchedParams'
1835	CALL_FUNCTION_2   None
1838	POP_JUMP_IF_FALSE '1857'

1841	LOAD_GLOBAL       'MacOS'
1844	LOAD_ATTR         'SchedParams'
1847	LOAD_FAST         'appsw'
1850	CALL_FUNCTION_VAR_0 None
1853	POP_TOP           None
1854	JUMP_FORWARD      '1857'
1857_0	COME_FROM         '1854'

1857	DELETE_FAST       'd'
1860	END_FINALLY       None
1861	LOAD_CONST        None
1864	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 1530


def _process_Nav_args(dftflags, **args):
    import Carbon.AppleEvents
    import Carbon.AE
    import Carbon.File
    for k in args.keys():
        if args[k] is None:
            del args[k]

    if 'dialogOptionFlags' not in args:
        args['dialogOptionFlags'] = dftflags
    if 'defaultLocation' in args and not isinstance(args['defaultLocation'], Carbon.AE.AEDesc):
        defaultLocation = args['defaultLocation']
        if isinstance(defaultLocation, Carbon.File.FSSpec):
            args['defaultLocation'] = Carbon.AE.AECreateDesc(Carbon.AppleEvents.typeFSS, defaultLocation.data)
        else:
            if not isinstance(defaultLocation, Carbon.File.FSRef):
                defaultLocation = Carbon.File.FSRef(defaultLocation)
            args['defaultLocation'] = Carbon.AE.AECreateDesc(Carbon.AppleEvents.typeFSRef, defaultLocation.data)
    if 'typeList' in args and not isinstance(args['typeList'], Carbon.Res.ResourceType):
        typeList = args['typeList'][:]
        if 'TEXT' in typeList and '\x00\x00\x00\x00' not in typeList:
            typeList = typeList + ('\x00\x00\x00\x00',)
        data = 'Pyth' + struct.pack('hh', 0, len(typeList))
        for type in typeList:
            data = data + type

        args['typeList'] = Carbon.Res.Handle(data)
    tpwanted = str
    if 'wanted' in args:
        tpwanted = args['wanted']
        del args['wanted']
    return (args, tpwanted)


def _dummy_Nav_eventproc(msg, data):
    pass


_default_Nav_eventproc = _dummy_Nav_eventproc

def SetDefaultEventProc(proc):
    global _default_Nav_eventproc
    rv = _default_Nav_eventproc
    if proc is None:
        proc = _dummy_Nav_eventproc
    _default_Nav_eventproc = proc
    return rv


def AskFileForOpen(message = None, typeList = None, version = None, defaultLocation = None, dialogOptionFlags = None, location = None, clientName = None, windowTitle = None, actionButtonLabel = None, cancelButtonLabel = None, preferenceKey = None, popupExtension = None, eventProc = _dummy_Nav_eventproc, previewProc = None, filterProc = None, wanted = None, multiple = None):
    """Display a dialog asking the user for a file to open.
    
    wanted is the return type wanted: FSSpec, FSRef, unicode or string (default)
    the other arguments can be looked up in Apple's Navigation Services documentation"""
    default_flags = 86
    args, tpwanted = _process_Nav_args(default_flags, version=version, defaultLocation=defaultLocation, dialogOptionFlags=dialogOptionFlags, location=location, clientName=clientName, windowTitle=windowTitle, actionButtonLabel=actionButtonLabel, cancelButtonLabel=cancelButtonLabel, message=message, preferenceKey=preferenceKey, popupExtension=popupExtension, eventProc=eventProc, previewProc=previewProc, filterProc=filterProc, typeList=typeList, wanted=wanted, multiple=multiple)
    _interact()
    try:
        rr = Nav.NavChooseFile(args)
        good = 1
    except Nav.error as arg:
        if arg[0] != -128:
            raise Nav.error, arg
        return None

    if not rr.validRecord or not rr.selection:
        return None
    elif issubclass(tpwanted, Carbon.File.FSRef):
        return tpwanted(rr.selection_fsr[0])
    elif issubclass(tpwanted, Carbon.File.FSSpec):
        return tpwanted(rr.selection[0])
    elif issubclass(tpwanted, str):
        return tpwanted(rr.selection_fsr[0].as_pathname())
    elif issubclass(tpwanted, unicode):
        return tpwanted(rr.selection_fsr[0].as_pathname(), 'utf8')
    else:
        raise TypeError, "Unknown value for argument 'wanted': %s" % repr(tpwanted)
        return None


def AskFileForSave(message = None, savedFileName = None, version = None, defaultLocation = None, dialogOptionFlags = None, location = None, clientName = None, windowTitle = None, actionButtonLabel = None, cancelButtonLabel = None, preferenceKey = None, popupExtension = None, eventProc = _dummy_Nav_eventproc, fileType = None, fileCreator = None, wanted = None, multiple = None):
    """Display a dialog asking the user for a filename to save to.
    
    wanted is the return type wanted: FSSpec, FSRef, unicode or string (default)
    the other arguments can be looked up in Apple's Navigation Services documentation"""
    default_flags = 7
    args, tpwanted = _process_Nav_args(default_flags, version=version, defaultLocation=defaultLocation, dialogOptionFlags=dialogOptionFlags, location=location, clientName=clientName, windowTitle=windowTitle, actionButtonLabel=actionButtonLabel, cancelButtonLabel=cancelButtonLabel, savedFileName=savedFileName, message=message, preferenceKey=preferenceKey, popupExtension=popupExtension, eventProc=eventProc, fileType=fileType, fileCreator=fileCreator, wanted=wanted, multiple=multiple)
    _interact()
    try:
        rr = Nav.NavPutFile(args)
        good = 1
    except Nav.error as arg:
        if arg[0] != -128:
            raise Nav.error, arg
        return None

    if not rr.validRecord or not rr.selection:
        return None
    else:
        if issubclass(tpwanted, Carbon.File.FSRef):
            raise TypeError, 'Cannot pass wanted=FSRef to AskFileForSave'
        if issubclass(tpwanted, Carbon.File.FSSpec):
            return tpwanted(rr.selection[0])
        if issubclass(tpwanted, (str, unicode)):
            vrefnum, dirid, name = rr.selection[0].as_tuple()
            pardir_fss = Carbon.File.FSSpec((vrefnum, dirid, ''))
            pardir_fsr = Carbon.File.FSRef(pardir_fss)
            pardir_path = pardir_fsr.FSRefMakePath()
            name_utf8 = unicode(name, 'macroman').encode('utf8')
            fullpath = os.path.join(pardir_path, name_utf8)
            if issubclass(tpwanted, unicode):
                return unicode(fullpath, 'utf8')
            return tpwanted(fullpath)
        raise TypeError, "Unknown value for argument 'wanted': %s" % repr(tpwanted)
        return None


def AskFolder(message = None, version = None, defaultLocation = None, dialogOptionFlags = None, location = None, clientName = None, windowTitle = None, actionButtonLabel = None, cancelButtonLabel = None, preferenceKey = None, popupExtension = None, eventProc = _dummy_Nav_eventproc, filterProc = None, wanted = None, multiple = None):
    """Display a dialog asking the user for select a folder.
    
    wanted is the return type wanted: FSSpec, FSRef, unicode or string (default)
    the other arguments can be looked up in Apple's Navigation Services documentation"""
    default_flags = 23
    args, tpwanted = _process_Nav_args(default_flags, version=version, defaultLocation=defaultLocation, dialogOptionFlags=dialogOptionFlags, location=location, clientName=clientName, windowTitle=windowTitle, actionButtonLabel=actionButtonLabel, cancelButtonLabel=cancelButtonLabel, message=message, preferenceKey=preferenceKey, popupExtension=popupExtension, eventProc=eventProc, filterProc=filterProc, wanted=wanted, multiple=multiple)
    _interact()
    try:
        rr = Nav.NavChooseFolder(args)
        good = 1
    except Nav.error as arg:
        if arg[0] != -128:
            raise Nav.error, arg
        return None

    if not rr.validRecord or not rr.selection:
        return None
    elif issubclass(tpwanted, Carbon.File.FSRef):
        return tpwanted(rr.selection_fsr[0])
    elif issubclass(tpwanted, Carbon.File.FSSpec):
        return tpwanted(rr.selection[0])
    elif issubclass(tpwanted, str):
        return tpwanted(rr.selection_fsr[0].as_pathname())
    elif issubclass(tpwanted, unicode):
        return tpwanted(rr.selection_fsr[0].as_pathname(), 'utf8')
    else:
        raise TypeError, "Unknown value for argument 'wanted': %s" % repr(tpwanted)
        return None


def test():
    import time
    Message('Testing EasyDialogs.')
    optionlist = (('v', 'Verbose'),
     ('verbose', 'Verbose as long option'),
     ('flags=', 'Valued option'),
     ('f:', 'Short valued option'))
    commandlist = (('start', 'Start something'), ('stop', 'Stop something'))
    argv = GetArgv(optionlist=optionlist, commandlist=commandlist, addoldfile=0)
    Message('Command line: %s' % ' '.join(argv))
    for i in range(len(argv)):
        print 'arg[%d] = %r' % (i, argv[i])

    ok = AskYesNoCancel('Do you want to proceed?')
    ok = AskYesNoCancel('Do you want to identify?', yes='Identify', no='No')
    if ok > 0:
        s = AskString('Enter your first name', 'Joe')
        s2 = AskPassword('Okay %s, tell us your nickname' % s, s, cancel='None')
        if not s2:
            Message('%s has no secret nickname' % s)
        else:
            Message('Hello everybody!!\nThe secret nickname of %s is %s!!!' % (s, s2))
    else:
        s = 'Anonymous'
    rv = AskFileForOpen(message='Gimme a file, %s' % s, wanted=Carbon.File.FSSpec)
    Message('rv: %s' % rv)
    rv = AskFileForSave(wanted=Carbon.File.FSRef, savedFileName='%s.txt' % s)
    Message('rv.as_pathname: %s' % rv.as_pathname())
    rv = AskFolder()
    Message('Folder name: %s' % rv)
    text = ('Working Hard...', 'Hardly Working...', 'So far, so good!', "Keep on truckin'")
    bar = ProgressBar('Progress, progress...', 0, label='Ramping up...')
    try:
        if hasattr(MacOS, 'SchedParams'):
            appsw = MacOS.SchedParams(1, 0)
        for i in xrange(20):
            bar.inc()
            time.sleep(0.05)

        bar.set(0, 100)
        for i in xrange(100):
            bar.set(i)
            time.sleep(0.05)
            if i % 10 == 0:
                bar.label(text[i / 10 % 4])

        bar.label('Done.')
        time.sleep(1.0)
    finally:
        del bar
        if hasattr(MacOS, 'SchedParams'):
            MacOS.SchedParams(*appsw)


if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        Message('Operation Canceled.')