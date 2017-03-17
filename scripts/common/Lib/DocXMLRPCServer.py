# Embedded file name: scripts/common/Lib/DocXMLRPCServer.py
"""Self documenting XML-RPC Server.

This module can be used to create XML-RPC servers that
serve pydoc-style documentation in response to HTTP
GET requests. This documentation is dynamically generated
based on the functions and methods registered with the
server.

This module is built upon the pydoc and SimpleXMLRPCServer
modules.
"""
import pydoc
import inspect
import re
import sys
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler, CGIXMLRPCRequestHandler, resolve_dotted_attribute

class ServerHTMLDoc(pydoc.HTMLDoc):
    """Class used to generate pydoc HTML document for a server"""

    def markup--- This code section failed: ---

0	LOAD_FAST         'escape'
3	JUMP_IF_TRUE_OR_POP '12'
6	LOAD_FAST         'self'
9	LOAD_ATTR         'escape'
12_0	COME_FROM         '3'
12	STORE_FAST        'escape'

15	BUILD_LIST_0      None
18	STORE_FAST        'results'

21	LOAD_CONST        0
24	STORE_FAST        'here'

27	LOAD_GLOBAL       're'
30	LOAD_ATTR         'compile'
33	LOAD_CONST        '\\b((http|ftp)://\\S+[\\w/]|RFC[- ]?(\\d+)|PEP[- ]?(\\d+)|(self\\.)?((?:\\w|\\.)+))\\b'
36	CALL_FUNCTION_1   None
39	STORE_FAST        'pattern'

42	SETUP_LOOP        '429'

45	LOAD_FAST         'pattern'
48	LOAD_ATTR         'search'
51	LOAD_FAST         'text'
54	LOAD_FAST         'here'
57	CALL_FUNCTION_2   None
60	STORE_FAST        'match'

63	LOAD_FAST         'match'
66	POP_JUMP_IF_TRUE  '73'
69	BREAK_LOOP        None
70	JUMP_FORWARD      '73'
73_0	COME_FROM         '70'

73	LOAD_FAST         'match'
76	LOAD_ATTR         'span'
79	CALL_FUNCTION_0   None
82	UNPACK_SEQUENCE_2 None
85	STORE_FAST        'start'
88	STORE_FAST        'end'

91	LOAD_FAST         'results'
94	LOAD_ATTR         'append'
97	LOAD_FAST         'escape'
100	LOAD_FAST         'text'
103	LOAD_FAST         'here'
106	LOAD_FAST         'start'
109	SLICE+3           None
110	CALL_FUNCTION_1   None
113	CALL_FUNCTION_1   None
116	POP_TOP           None

117	LOAD_FAST         'match'
120	LOAD_ATTR         'groups'
123	CALL_FUNCTION_0   None
126	UNPACK_SEQUENCE_6 None
129	STORE_FAST        'all'
132	STORE_FAST        'scheme'
135	STORE_FAST        'rfc'
138	STORE_FAST        'pep'
141	STORE_FAST        'selfdot'
144	STORE_FAST        'name'

147	LOAD_FAST         'scheme'
150	POP_JUMP_IF_FALSE '203'

153	LOAD_FAST         'escape'
156	LOAD_FAST         'all'
159	CALL_FUNCTION_1   None
162	LOAD_ATTR         'replace'
165	LOAD_CONST        '"'
168	LOAD_CONST        '&quot;'
171	CALL_FUNCTION_2   None
174	STORE_FAST        'url'

177	LOAD_FAST         'results'
180	LOAD_ATTR         'append'
183	LOAD_CONST        '<a href="%s">%s</a>'
186	LOAD_FAST         'url'
189	LOAD_FAST         'url'
192	BUILD_TUPLE_2     None
195	BINARY_MODULO     None
196	CALL_FUNCTION_1   None
199	POP_TOP           None
200	JUMP_FORWARD      '419'

203	LOAD_FAST         'rfc'
206	POP_JUMP_IF_FALSE '257'

209	LOAD_CONST        'http://www.rfc-editor.org/rfc/rfc%d.txt'
212	LOAD_GLOBAL       'int'
215	LOAD_FAST         'rfc'
218	CALL_FUNCTION_1   None
221	BINARY_MODULO     None
222	STORE_FAST        'url'

225	LOAD_FAST         'results'
228	LOAD_ATTR         'append'
231	LOAD_CONST        '<a href="%s">%s</a>'
234	LOAD_FAST         'url'
237	LOAD_FAST         'escape'
240	LOAD_FAST         'all'
243	CALL_FUNCTION_1   None
246	BUILD_TUPLE_2     None
249	BINARY_MODULO     None
250	CALL_FUNCTION_1   None
253	POP_TOP           None
254	JUMP_FORWARD      '419'

257	LOAD_FAST         'pep'
260	POP_JUMP_IF_FALSE '311'

263	LOAD_CONST        'http://www.python.org/dev/peps/pep-%04d/'
266	LOAD_GLOBAL       'int'
269	LOAD_FAST         'pep'
272	CALL_FUNCTION_1   None
275	BINARY_MODULO     None
276	STORE_FAST        'url'

279	LOAD_FAST         'results'
282	LOAD_ATTR         'append'
285	LOAD_CONST        '<a href="%s">%s</a>'
288	LOAD_FAST         'url'
291	LOAD_FAST         'escape'
294	LOAD_FAST         'all'
297	CALL_FUNCTION_1   None
300	BUILD_TUPLE_2     None
303	BINARY_MODULO     None
304	CALL_FUNCTION_1   None
307	POP_TOP           None
308	JUMP_FORWARD      '419'

311	LOAD_FAST         'text'
314	LOAD_FAST         'end'
317	LOAD_FAST         'end'
320	LOAD_CONST        1
323	BINARY_ADD        None
324	SLICE+3           None
325	LOAD_CONST        '('
328	COMPARE_OP        '=='
331	POP_JUMP_IF_FALSE '368'

334	LOAD_FAST         'results'
337	LOAD_ATTR         'append'
340	LOAD_FAST         'self'
343	LOAD_ATTR         'namelink'
346	LOAD_FAST         'name'
349	LOAD_FAST         'methods'
352	LOAD_FAST         'funcs'
355	LOAD_FAST         'classes'
358	CALL_FUNCTION_4   None
361	CALL_FUNCTION_1   None
364	POP_TOP           None
365	JUMP_FORWARD      '419'

368	LOAD_FAST         'selfdot'
371	POP_JUMP_IF_FALSE '394'

374	LOAD_FAST         'results'
377	LOAD_ATTR         'append'
380	LOAD_CONST        'self.<strong>%s</strong>'
383	LOAD_FAST         'name'
386	BINARY_MODULO     None
387	CALL_FUNCTION_1   None
390	POP_TOP           None
391	JUMP_FORWARD      '419'

394	LOAD_FAST         'results'
397	LOAD_ATTR         'append'
400	LOAD_FAST         'self'
403	LOAD_ATTR         'namelink'
406	LOAD_FAST         'name'
409	LOAD_FAST         'classes'
412	CALL_FUNCTION_2   None
415	CALL_FUNCTION_1   None
418	POP_TOP           None
419_0	COME_FROM         '200'
419_1	COME_FROM         '254'
419_2	COME_FROM         '308'
419_3	COME_FROM         '365'
419_4	COME_FROM         '391'

419	LOAD_FAST         'end'
422	STORE_FAST        'here'
425	JUMP_BACK         '45'
428	POP_BLOCK         None
429_0	COME_FROM         '42'

429	LOAD_FAST         'results'
432	LOAD_ATTR         'append'
435	LOAD_FAST         'escape'
438	LOAD_FAST         'text'
441	LOAD_FAST         'here'
444	SLICE+1           None
445	CALL_FUNCTION_1   None
448	CALL_FUNCTION_1   None
451	POP_TOP           None

452	LOAD_CONST        ''
455	LOAD_ATTR         'join'
458	LOAD_FAST         'results'
461	CALL_FUNCTION_1   None
464	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 428

    def docroutine(self, object, name, mod = None, funcs = {}, classes = {}, methods = {}, cl = None):
        """Produce HTML documentation for a function or method object."""
        anchor = (cl and cl.__name__ or '') + '-' + name
        note = ''
        title = '<a name="%s"><strong>%s</strong></a>' % (self.escape(anchor), self.escape(name))
        if inspect.ismethod(object):
            args, varargs, varkw, defaults = inspect.getargspec(object.im_func)
            argspec = inspect.formatargspec(args[1:], varargs, varkw, defaults, formatvalue=self.formatvalue)
        elif inspect.isfunction(object):
            args, varargs, varkw, defaults = inspect.getargspec(object)
            argspec = inspect.formatargspec(args, varargs, varkw, defaults, formatvalue=self.formatvalue)
        else:
            argspec = '(...)'
        if isinstance(object, tuple):
            argspec = object[0] or argspec
            docstring = object[1] or ''
        else:
            docstring = pydoc.getdoc(object)
        decl = title + argspec + (note and self.grey('<font face="helvetica, arial">%s</font>' % note))
        doc = self.markup(docstring, self.preformat, funcs, classes, methods)
        doc = doc and '<dd><tt>%s</tt></dd>' % doc
        return '<dl><dt>%s</dt>%s</dl>\n' % (decl, doc)

    def docserver(self, server_name, package_documentation, methods):
        """Produce HTML documentation for an XML-RPC server."""
        fdict = {}
        for key, value in methods.items():
            fdict[key] = '#-' + key
            fdict[value] = fdict[key]

        server_name = self.escape(server_name)
        head = '<big><big><strong>%s</strong></big></big>' % server_name
        result = self.heading(head, '#ffffff', '#7799ee')
        doc = self.markup(package_documentation, self.preformat, fdict)
        doc = doc and '<tt>%s</tt>' % doc
        result = result + '<p>%s</p>\n' % doc
        contents = []
        method_items = sorted(methods.items())
        for key, value in method_items:
            contents.append(self.docroutine(value, key, funcs=fdict))

        result = result + self.bigsection('Methods', '#ffffff', '#eeaa77', pydoc.join(contents))
        return result


class XMLRPCDocGenerator:
    """Generates documentation for an XML-RPC server.
    
    This class is designed as mix-in and should not
    be constructed directly.
    """

    def __init__(self):
        self.server_name = 'XML-RPC Server Documentation'
        self.server_documentation = 'This server exports the following methods through the XML-RPC protocol.'
        self.server_title = 'XML-RPC Server Documentation'

    def set_server_title(self, server_title):
        """Set the HTML title of the generated server documentation"""
        self.server_title = server_title

    def set_server_name(self, server_name):
        """Set the name of the generated HTML server documentation"""
        self.server_name = server_name

    def set_server_documentation(self, server_documentation):
        """Set the documentation string for the entire server."""
        self.server_documentation = server_documentation

    def generate_html_documentation(self):
        """generate_html_documentation() => html documentation for the server
        
        Generates HTML documentation for the server using introspection for
        installed functions and instances that do not implement the
        _dispatch method. Alternatively, instances can choose to implement
        the _get_method_argstring(method_name) method to provide the
        argument string used in the documentation and the
        _methodHelp(method_name) method to provide the help text used
        in the documentation."""
        methods = {}
        for method_name in self.system_listMethods():
            if method_name in self.funcs:
                method = self.funcs[method_name]
            elif self.instance is not None:
                method_info = [None, None]
                if hasattr(self.instance, '_get_method_argstring'):
                    method_info[0] = self.instance._get_method_argstring(method_name)
                if hasattr(self.instance, '_methodHelp'):
                    method_info[1] = self.instance._methodHelp(method_name)
                method_info = tuple(method_info)
                if method_info != (None, None):
                    method = method_info
                elif not hasattr(self.instance, '_dispatch'):
                    try:
                        method = resolve_dotted_attribute(self.instance, method_name)
                    except AttributeError:
                        method = method_info

                else:
                    method = method_info
            else:
                raise 0 or AssertionError('Could not find method in self.functions and no instance installed')
            methods[method_name] = method

        documenter = ServerHTMLDoc()
        documentation = documenter.docserver(self.server_name, self.server_documentation, methods)
        return documenter.page(self.server_title, documentation)


class DocXMLRPCRequestHandler(SimpleXMLRPCRequestHandler):
    """XML-RPC and documentation request handler class.
    
    Handles all HTTP POST requests and attempts to decode them as
    XML-RPC requests.
    
    Handles all HTTP GET requests and interprets them as requests
    for documentation.
    """

    def do_GET(self):
        """Handles the HTTP GET request.
        
        Interpret all HTTP GET requests as requests for server
        documentation.
        """
        if not self.is_rpc_path_valid():
            self.report_404()
            return
        response = self.server.generate_html_documentation()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-length', str(len(response)))
        self.end_headers()
        self.wfile.write(response)


class DocXMLRPCServer(SimpleXMLRPCServer, XMLRPCDocGenerator):
    """XML-RPC and HTML documentation server.
    
    Adds the ability to serve server documentation to the capabilities
    of SimpleXMLRPCServer.
    """

    def __init__(self, addr, requestHandler = DocXMLRPCRequestHandler, logRequests = 1, allow_none = False, encoding = None, bind_and_activate = True):
        SimpleXMLRPCServer.__init__(self, addr, requestHandler, logRequests, allow_none, encoding, bind_and_activate)
        XMLRPCDocGenerator.__init__(self)


class DocCGIXMLRPCRequestHandler(CGIXMLRPCRequestHandler, XMLRPCDocGenerator):
    """Handler for XML-RPC data and documentation requests passed through
    CGI"""

    def handle_get(self):
        """Handles the HTTP GET request.
        
        Interpret all HTTP GET requests as requests for server
        documentation.
        """
        response = self.generate_html_documentation()
        print 'Content-Type: text/html'
        print 'Content-Length: %d' % len(response)
        print
        sys.stdout.write(response)

    def __init__(self):
        CGIXMLRPCRequestHandler.__init__(self)
        XMLRPCDocGenerator.__init__(self)