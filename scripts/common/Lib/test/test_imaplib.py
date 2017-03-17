# Embedded file name: scripts/common/Lib/test/test_imaplib.py
from test import test_support as support
threading = support.import_module('threading')
from contextlib import contextmanager
import imaplib
import os.path
import SocketServer
import time
from test_support import reap_threads, verbose, transient_internet
import unittest
try:
    import ssl
except ImportError:
    ssl = None

CERTFILE = None

class TestImaplib(unittest.TestCase):

    def test_that_Time2Internaldate_returns_a_result(self):
        timevalues = [2000000000,
         2000000000.0,
         time.localtime(2000000000),
         '"18-May-2033 05:33:20 +0200"']
        for t in timevalues:
            imaplib.Time2Internaldate(t)


if ssl:

    class SecureTCPServer(SocketServer.TCPServer):

        def get_request(self):
            global CERTFILE
            newsocket, fromaddr = self.socket.accept()
            connstream = ssl.wrap_socket(newsocket, server_side=True, certfile=CERTFILE)
            return (connstream, fromaddr)


    IMAP4_SSL = imaplib.IMAP4_SSL
else:

    class SecureTCPServer:
        pass


    IMAP4_SSL = None

class SimpleIMAPHandler(SocketServer.StreamRequestHandler):
    timeout = 1

    def _send(self, message):
        if verbose:
            print 'SENT:', message.strip()
        self.wfile.write(message)

    def handle--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         '_send'
6	LOAD_CONST        '* OK IMAP4rev1\r\n'
9	CALL_FUNCTION_1   None
12	POP_TOP           None

13	SETUP_LOOP        '264'

16	LOAD_CONST        ''
19	STORE_FAST        'line'

22	SETUP_LOOP        '117'

25	SETUP_EXCEPT      '76'

28	LOAD_FAST         'self'
31	LOAD_ATTR         'rfile'
34	LOAD_ATTR         'read'
37	LOAD_CONST        1
40	CALL_FUNCTION_1   None
43	STORE_FAST        'part'

46	LOAD_FAST         'part'
49	LOAD_CONST        ''
52	COMPARE_OP        '=='
55	POP_JUMP_IF_FALSE '62'

58	LOAD_CONST        None
61	RETURN_END_IF     None

62	LOAD_FAST         'line'
65	LOAD_FAST         'part'
68	INPLACE_ADD       None
69	STORE_FAST        'line'
72	POP_BLOCK         None
73	JUMP_FORWARD      '94'
76_0	COME_FROM         '25'

76	DUP_TOP           None
77	LOAD_GLOBAL       'IOError'
80	COMPARE_OP        'exception match'
83	POP_JUMP_IF_FALSE '93'
86	POP_TOP           None
87	POP_TOP           None
88	POP_TOP           None

89	LOAD_CONST        None
92	RETURN_VALUE      None
93	END_FINALLY       None
94_0	COME_FROM         '73'
94_1	COME_FROM         '93'

94	LOAD_FAST         'line'
97	LOAD_ATTR         'endswith'
100	LOAD_CONST        '\r\n'
103	CALL_FUNCTION_1   None
106	POP_JUMP_IF_FALSE '25'

109	BREAK_LOOP        None
110	JUMP_BACK         '25'
113	JUMP_BACK         '25'
116	POP_BLOCK         None
117_0	COME_FROM         '22'

117	LOAD_GLOBAL       'verbose'
120	POP_JUMP_IF_FALSE '141'
123	LOAD_CONST        'GOT:'
126	PRINT_ITEM        None
127	LOAD_FAST         'line'
130	LOAD_ATTR         'strip'
133	CALL_FUNCTION_0   None
136	PRINT_ITEM_CONT   None
137	PRINT_NEWLINE_CONT None
138	JUMP_FORWARD      '141'
141_0	COME_FROM         '138'

141	LOAD_FAST         'line'
144	LOAD_ATTR         'split'
147	CALL_FUNCTION_0   None
150	STORE_FAST        'splitline'

153	LOAD_FAST         'splitline'
156	LOAD_CONST        0
159	BINARY_SUBSCR     None
160	STORE_FAST        'tag'

163	LOAD_FAST         'splitline'
166	LOAD_CONST        1
169	BINARY_SUBSCR     None
170	STORE_FAST        'cmd'

173	LOAD_FAST         'splitline'
176	LOAD_CONST        2
179	SLICE+1           None
180	STORE_FAST        'args'

183	LOAD_GLOBAL       'hasattr'
186	LOAD_FAST         'self'
189	LOAD_CONST        'cmd_%s'
192	LOAD_FAST         'cmd'
195	BUILD_TUPLE_1     None
198	BINARY_MODULO     None
199	CALL_FUNCTION_2   None
202	POP_JUMP_IF_FALSE '237'

205	LOAD_GLOBAL       'getattr'
208	LOAD_FAST         'self'
211	LOAD_CONST        'cmd_%s'
214	LOAD_FAST         'cmd'
217	BUILD_TUPLE_1     None
220	BINARY_MODULO     None
221	CALL_FUNCTION_2   None
224	LOAD_FAST         'tag'
227	LOAD_FAST         'args'
230	CALL_FUNCTION_2   None
233	POP_TOP           None
234	JUMP_BACK         '16'

237	LOAD_FAST         'self'
240	LOAD_ATTR         '_send'
243	LOAD_CONST        '%s BAD %s unknown\r\n'
246	LOAD_FAST         'tag'
249	LOAD_FAST         'cmd'
252	BUILD_TUPLE_2     None
255	BINARY_MODULO     None
256	CALL_FUNCTION_1   None
259	POP_TOP           None
260	JUMP_BACK         '16'
263	POP_BLOCK         None
264_0	COME_FROM         '13'

Syntax error at or near `POP_BLOCK' token at offset 116

    def cmd_CAPABILITY(self, tag, args):
        self._send('* CAPABILITY IMAP4rev1\r\n')
        self._send('%s OK CAPABILITY completed\r\n' % (tag,))


class BaseThreadedNetworkedTests(unittest.TestCase):

    def make_server(self, addr, hdlr):

        class MyServer(self.server_class):

            def handle_error(self, request, client_address):
                self.close_request(request)
                self.server_close()
                raise

        if verbose:
            print 'creating server'
        server = MyServer(addr, hdlr)
        self.assertEqual(server.server_address, server.socket.getsockname())
        if verbose:
            print 'server created'
            print 'ADDR =', addr
            print 'CLASS =', self.server_class
            print 'HDLR =', server.RequestHandlerClass
        t = threading.Thread(name='%s serving' % self.server_class, target=server.serve_forever, kwargs={'poll_interval': 0.01})
        t.daemon = True
        t.start()
        if verbose:
            print 'server running'
        return (server, t)

    def reap_server(self, server, thread):
        if verbose:
            print 'waiting for server'
        server.shutdown()
        thread.join()
        if verbose:
            print 'done'

    @contextmanager
    def reaped_server(self, hdlr):
        server, thread = self.make_server((support.HOST, 0), hdlr)
        try:
            yield server
        finally:
            self.reap_server(server, thread)

    @reap_threads
    def test_connect(self):
        with self.reaped_server(SimpleIMAPHandler) as server:
            client = self.imap_class(*server.server_address)
            client.shutdown()

    @reap_threads
    def test_issue5949(self):

        class EOFHandler(SocketServer.StreamRequestHandler):

            def handle(self):
                self.wfile.write('* OK')

        with self.reaped_server(EOFHandler) as server:
            self.assertRaises(imaplib.IMAP4.abort, self.imap_class, *server.server_address)


class ThreadedNetworkedTests(BaseThreadedNetworkedTests):
    server_class = SocketServer.TCPServer
    imap_class = imaplib.IMAP4


@unittest.skipUnless(ssl, 'SSL not available')

class ThreadedNetworkedTestsSSL(BaseThreadedNetworkedTests):
    server_class = SecureTCPServer
    imap_class = IMAP4_SSL


class RemoteIMAPTest(unittest.TestCase):
    host = 'cyrus.andrew.cmu.edu'
    port = 143
    username = 'anonymous'
    password = 'pass'
    imap_class = imaplib.IMAP4

    def setUp(self):
        with transient_internet(self.host):
            self.server = self.imap_class(self.host, self.port)

    def tearDown(self):
        if self.server is not None:
            self.server.logout()
        return

    def test_logincapa(self):
        self.assertTrue('LOGINDISABLED' in self.server.capabilities)

    def test_anonlogin(self):
        self.assertTrue('AUTH=ANONYMOUS' in self.server.capabilities)
        rs = self.server.login(self.username, self.password)
        self.assertEqual(rs[0], 'OK')

    def test_logout(self):
        rs = self.server.logout()
        self.server = None
        self.assertEqual(rs[0], 'BYE')
        return


@unittest.skipUnless(ssl, 'SSL not available')

class RemoteIMAP_SSLTest(RemoteIMAPTest):
    port = 993
    imap_class = IMAP4_SSL

    def test_logincapa(self):
        self.assertFalse('LOGINDISABLED' in self.server.capabilities)
        self.assertTrue('AUTH=PLAIN' in self.server.capabilities)


def test_main():
    global CERTFILE
    tests = [TestImaplib]
    if support.is_resource_enabled('network'):
        if ssl:
            CERTFILE = os.path.join(os.path.dirname(__file__) or os.curdir, 'keycert.pem')
            if not os.path.exists(CERTFILE):
                raise support.TestFailed("Can't read certificate files!")
        tests.extend([ThreadedNetworkedTests,
         ThreadedNetworkedTestsSSL,
         RemoteIMAPTest,
         RemoteIMAP_SSLTest])
    support.run_unittest(*tests)


if __name__ == '__main__':
    support.use_resources = ['network']
    test_main()