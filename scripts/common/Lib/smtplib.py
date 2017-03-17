# Embedded file name: scripts/common/Lib/smtplib.py
--- This code section failed: ---

0	LOAD_CONST        'SMTP/ESMTP client class.\n\nThis should follow RFC 821 (SMTP), RFC 1869 (ESMTP), RFC 2554 (SMTP\nAuthentication) and RFC 2487 (Secure SMTP over TLS).\n\nNotes:\n\nPlease remember, when doing ESMTP, that the names of the SMTP service\nextensions are NOT the same thing as the option keywords for the RCPT\nand MAIL commands!\n\nExample:\n\n  >>> import smtplib\n  >>> s=smtplib.SMTP("localhost")\n  >>> print s.help()\n  This is Sendmail version 8.8.4\n  Topics:\n      HELO    EHLO    MAIL    RCPT    DATA\n      RSET    NOOP    QUIT    HELP    VRFY\n      EXPN    VERB    ETRN    DSN\n  For more info use "HELP <topic>".\n  To report bugs in the implementation send email to\n      sendmail-bugs@sendmail.org.\n  For local information send email to Postmaster at your site.\n  End of HELP info\n  >>> s.putcmd("vrfy","someone@here")\n  >>> s.getreply()\n  (250, "Somebody OverHere <somebody@here.my.org>")\n  >>> s.quit()\n'
3	STORE_NAME        '__doc__'

6	LOAD_CONST        -1
9	LOAD_CONST        None
12	IMPORT_NAME       'socket'
15	STORE_NAME        'socket'

18	LOAD_CONST        -1
21	LOAD_CONST        None
24	IMPORT_NAME       're'
27	STORE_NAME        're'

30	LOAD_CONST        -1
33	LOAD_CONST        None
36	IMPORT_NAME       'email.utils'
39	STORE_NAME        'email'

42	LOAD_CONST        -1
45	LOAD_CONST        None
48	IMPORT_NAME       'base64'
51	STORE_NAME        'base64'

54	LOAD_CONST        -1
57	LOAD_CONST        None
60	IMPORT_NAME       'hmac'
63	STORE_NAME        'hmac'

66	LOAD_CONST        -1
69	LOAD_CONST        ('encode',)
72	IMPORT_NAME       'email.base64mime'
75	IMPORT_FROM       'encode'
78	STORE_NAME        'encode_base64'
81	POP_TOP           None

82	LOAD_CONST        -1
85	LOAD_CONST        ('stderr',)
88	IMPORT_NAME       'sys'
91	IMPORT_FROM       'stderr'
94	STORE_NAME        'stderr'
97	POP_TOP           None

98	LOAD_CONST        'SMTPException'
101	LOAD_CONST        'SMTPServerDisconnected'
104	LOAD_CONST        'SMTPResponseException'

107	LOAD_CONST        'SMTPSenderRefused'
110	LOAD_CONST        'SMTPRecipientsRefused'
113	LOAD_CONST        'SMTPDataError'

116	LOAD_CONST        'SMTPConnectError'
119	LOAD_CONST        'SMTPHeloError'
122	LOAD_CONST        'SMTPAuthenticationError'

125	LOAD_CONST        'quoteaddr'
128	LOAD_CONST        'quotedata'
131	LOAD_CONST        'SMTP'
134	BUILD_LIST_12     None
137	STORE_NAME        '__all__'

140	LOAD_CONST        25
143	STORE_NAME        'SMTP_PORT'

146	LOAD_CONST        465
149	STORE_NAME        'SMTP_SSL_PORT'

152	LOAD_CONST        '\r\n'
155	STORE_NAME        'CRLF'

158	LOAD_NAME         're'
161	LOAD_ATTR         'compile'
164	LOAD_CONST        'auth=(.*)'
167	LOAD_NAME         're'
170	LOAD_ATTR         'I'
173	CALL_FUNCTION_2   None
176	STORE_NAME        'OLDSTYLE_AUTH'

179	LOAD_CONST        'SMTPException'
182	LOAD_NAME         'Exception'
185	BUILD_TUPLE_1     None
188	LOAD_CONST        '<code_object SMTPException>'
191	MAKE_FUNCTION_0   None
194	CALL_FUNCTION_0   None
197	BUILD_CLASS       None
198	STORE_NAME        'SMTPException'

201	LOAD_CONST        'SMTPServerDisconnected'
204	LOAD_NAME         'SMTPException'
207	BUILD_TUPLE_1     None
210	LOAD_CONST        '<code_object SMTPServerDisconnected>'
213	MAKE_FUNCTION_0   None
216	CALL_FUNCTION_0   None
219	BUILD_CLASS       None
220	STORE_NAME        'SMTPServerDisconnected'

223	LOAD_CONST        'SMTPResponseException'
226	LOAD_NAME         'SMTPException'
229	BUILD_TUPLE_1     None
232	LOAD_CONST        '<code_object SMTPResponseException>'
235	MAKE_FUNCTION_0   None
238	CALL_FUNCTION_0   None
241	BUILD_CLASS       None
242	STORE_NAME        'SMTPResponseException'

245	LOAD_CONST        'SMTPSenderRefused'
248	LOAD_NAME         'SMTPResponseException'
251	BUILD_TUPLE_1     None
254	LOAD_CONST        '<code_object SMTPSenderRefused>'
257	MAKE_FUNCTION_0   None
260	CALL_FUNCTION_0   None
263	BUILD_CLASS       None
264	STORE_NAME        'SMTPSenderRefused'

267	LOAD_CONST        'SMTPRecipientsRefused'
270	LOAD_NAME         'SMTPException'
273	BUILD_TUPLE_1     None
276	LOAD_CONST        '<code_object SMTPRecipientsRefused>'
279	MAKE_FUNCTION_0   None
282	CALL_FUNCTION_0   None
285	BUILD_CLASS       None
286	STORE_NAME        'SMTPRecipientsRefused'

289	LOAD_CONST        'SMTPDataError'
292	LOAD_NAME         'SMTPResponseException'
295	BUILD_TUPLE_1     None
298	LOAD_CONST        '<code_object SMTPDataError>'
301	MAKE_FUNCTION_0   None
304	CALL_FUNCTION_0   None
307	BUILD_CLASS       None
308	STORE_NAME        'SMTPDataError'

311	LOAD_CONST        'SMTPConnectError'
314	LOAD_NAME         'SMTPResponseException'
317	BUILD_TUPLE_1     None
320	LOAD_CONST        '<code_object SMTPConnectError>'
323	MAKE_FUNCTION_0   None
326	CALL_FUNCTION_0   None
329	BUILD_CLASS       None
330	STORE_NAME        'SMTPConnectError'

333	LOAD_CONST        'SMTPHeloError'
336	LOAD_NAME         'SMTPResponseException'
339	BUILD_TUPLE_1     None
342	LOAD_CONST        '<code_object SMTPHeloError>'
345	MAKE_FUNCTION_0   None
348	CALL_FUNCTION_0   None
351	BUILD_CLASS       None
352	STORE_NAME        'SMTPHeloError'

355	LOAD_CONST        'SMTPAuthenticationError'
358	LOAD_NAME         'SMTPResponseException'
361	BUILD_TUPLE_1     None
364	LOAD_CONST        '<code_object SMTPAuthenticationError>'
367	MAKE_FUNCTION_0   None
370	CALL_FUNCTION_0   None
373	BUILD_CLASS       None
374	STORE_NAME        'SMTPAuthenticationError'

377	LOAD_CONST        '<code_object quoteaddr>'
380	MAKE_FUNCTION_0   None
383	STORE_NAME        'quoteaddr'

386	LOAD_CONST        '<code_object _addr_only>'
389	MAKE_FUNCTION_0   None
392	STORE_NAME        '_addr_only'

395	LOAD_CONST        '<code_object quotedata>'
398	MAKE_FUNCTION_0   None
401	STORE_NAME        'quotedata'

404	SETUP_EXCEPT      '423'

407	LOAD_CONST        -1
410	LOAD_CONST        None
413	IMPORT_NAME       'ssl'
416	STORE_NAME        'ssl'
419	POP_BLOCK         None
420	JUMP_FORWARD      '446'
423_0	COME_FROM         '404'

423	DUP_TOP           None
424	LOAD_NAME         'ImportError'
427	COMPARE_OP        'exception match'
430	POP_JUMP_IF_FALSE '445'
433	POP_TOP           None
434	POP_TOP           None
435	POP_TOP           None

436	LOAD_NAME         'False'
439	STORE_NAME        '_have_ssl'
442	JUMP_FORWARD      '471'
445	END_FINALLY       None
446_0	COME_FROM         '420'

446	LOAD_CONST        'SSLFakeFile'
449	BUILD_TUPLE_0     None
452	LOAD_CONST        '<code_object SSLFakeFile>'
455	MAKE_FUNCTION_0   None
458	CALL_FUNCTION_0   None
461	BUILD_CLASS       None
462	STORE_NAME        'SSLFakeFile'

465	LOAD_NAME         'True'
468	STORE_NAME        '_have_ssl'
471_0	COME_FROM         '445'

471	LOAD_CONST        'SMTP'
474	BUILD_TUPLE_0     None
477	LOAD_CONST        '<code_object SMTP>'
480	MAKE_FUNCTION_0   None
483	CALL_FUNCTION_0   None
486	BUILD_CLASS       None
487	STORE_NAME        'SMTP'

490	LOAD_NAME         '_have_ssl'
493	POP_JUMP_IF_FALSE '534'

496	LOAD_CONST        'SMTP_SSL'
499	LOAD_NAME         'SMTP'
502	BUILD_TUPLE_1     None
505	LOAD_CONST        '<code_object SMTP_SSL>'
508	MAKE_FUNCTION_0   None
511	CALL_FUNCTION_0   None
514	BUILD_CLASS       None
515	STORE_NAME        'SMTP_SSL'

518	LOAD_NAME         '__all__'
521	LOAD_ATTR         'append'
524	LOAD_CONST        'SMTP_SSL'
527	CALL_FUNCTION_1   None
530	POP_TOP           None
531	JUMP_FORWARD      '534'
534_0	COME_FROM         '531'

534	LOAD_CONST        2003
537	STORE_NAME        'LMTP_PORT'

540	LOAD_CONST        'LMTP'
543	LOAD_NAME         'SMTP'
546	BUILD_TUPLE_1     None
549	LOAD_CONST        '<code_object LMTP>'
552	MAKE_FUNCTION_0   None
555	CALL_FUNCTION_0   None
558	BUILD_CLASS       None
559	STORE_NAME        'LMTP'

562	LOAD_NAME         '__name__'
565	LOAD_CONST        '__main__'
568	COMPARE_OP        '=='
571	POP_JUMP_IF_FALSE '754'

574	LOAD_CONST        -1
577	LOAD_CONST        None
580	IMPORT_NAME       'sys'
583	STORE_NAME        'sys'

586	LOAD_CONST        '<code_object prompt>'
589	MAKE_FUNCTION_0   None
592	STORE_NAME        'prompt'

595	LOAD_NAME         'prompt'
598	LOAD_CONST        'From'
601	CALL_FUNCTION_1   None
604	STORE_NAME        'fromaddr'

607	LOAD_NAME         'prompt'
610	LOAD_CONST        'To'
613	CALL_FUNCTION_1   None
616	LOAD_ATTR         'split'
619	LOAD_CONST        ','
622	CALL_FUNCTION_1   None
625	STORE_NAME        'toaddrs'

628	LOAD_CONST        'Enter message, end with ^D:'
631	PRINT_ITEM        None
632	PRINT_NEWLINE_CONT None

633	LOAD_CONST        ''
636	STORE_NAME        'msg'

639	SETUP_LOOP        '682'

642	LOAD_NAME         'sys'
645	LOAD_ATTR         'stdin'
648	LOAD_ATTR         'readline'
651	CALL_FUNCTION_0   None
654	STORE_NAME        'line'

657	LOAD_NAME         'line'
660	UNARY_NOT         None
661	POP_JUMP_IF_FALSE '668'

664	BREAK_LOOP        None
665	JUMP_FORWARD      '668'
668_0	COME_FROM         '665'

668	LOAD_NAME         'msg'
671	LOAD_NAME         'line'
674	BINARY_ADD        None
675	STORE_NAME        'msg'
678	JUMP_BACK         '642'
681	POP_BLOCK         None
682_0	COME_FROM         '639'

682	LOAD_CONST        'Message length is %d'
685	LOAD_NAME         'len'
688	LOAD_NAME         'msg'
691	CALL_FUNCTION_1   None
694	BINARY_MODULO     None
695	PRINT_ITEM        None
696	PRINT_NEWLINE_CONT None

697	LOAD_NAME         'SMTP'
700	LOAD_CONST        'localhost'
703	CALL_FUNCTION_1   None
706	STORE_NAME        'server'

709	LOAD_NAME         'server'
712	LOAD_ATTR         'set_debuglevel'
715	LOAD_CONST        1
718	CALL_FUNCTION_1   None
721	POP_TOP           None

722	LOAD_NAME         'server'
725	LOAD_ATTR         'sendmail'
728	LOAD_NAME         'fromaddr'
731	LOAD_NAME         'toaddrs'
734	LOAD_NAME         'msg'
737	CALL_FUNCTION_3   None
740	POP_TOP           None

741	LOAD_NAME         'server'
744	LOAD_ATTR         'quit'
747	CALL_FUNCTION_0   None
750	POP_TOP           None
751	JUMP_FORWARD      '754'
754_0	COME_FROM         '751'

Syntax error at or near `POP_BLOCK' token at offset 681

