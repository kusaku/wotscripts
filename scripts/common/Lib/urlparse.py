# Embedded file name: scripts/common/Lib/urlparse.py
"""Parse (absolute and relative) URLs.

urlparse module is based upon the following RFC specifications.

RFC 3986 (STD66): "Uniform Resource Identifiers" by T. Berners-Lee, R. Fielding
and L.  Masinter, January 2005.

RFC 2732 : "Format for Literal IPv6 Addresses in URL's by R.Hinden, B.Carpenter
and L.Masinter, December 1999.

RFC 2396:  "Uniform Resource Identifiers (URI)": Generic Syntax by T.
Berners-Lee, R. Fielding, and L. Masinter, August 1998.

RFC 2368: "The mailto URL scheme", by P.Hoffman , L Masinter, J. Zwinski, July 1998.

RFC 1808: "Relative Uniform Resource Locators", by R. Fielding, UC Irvine, June
1995.

RFC 1738: "Uniform Resource Locators (URL)" by T. Berners-Lee, L. Masinter, M.
McCahill, December 1994

RFC 3986 is considered the current standard and any future changes to
urlparse module should conform with it.  The urlparse module is
currently not entirely compliant with this RFC due to defacto
scenarios for parsing, and for backward compatibility purposes, some
parsing quirks from older RFCs are retained. The testcases in
test_urlparse.py provides a good indicator of parsing behavior.

"""
__all__ = ['urlparse',
 'urlunparse',
 'urljoin',
 'urldefrag',
 'urlsplit',
 'urlunsplit',
 'parse_qs',
 'parse_qsl']
uses_relative = ['ftp',
 'http',
 'gopher',
 'nntp',
 'imap',
 'wais',
 'file',
 'https',
 'shttp',
 'mms',
 'prospero',
 'rtsp',
 'rtspu',
 '',
 'sftp',
 'svn',
 'svn+ssh']
uses_netloc = ['ftp',
 'http',
 'gopher',
 'nntp',
 'telnet',
 'imap',
 'wais',
 'file',
 'mms',
 'https',
 'shttp',
 'snews',
 'prospero',
 'rtsp',
 'rtspu',
 'rsync',
 '',
 'svn',
 'svn+ssh',
 'sftp',
 'nfs',
 'git',
 'git+ssh']
non_hierarchical = ['gopher',
 'hdl',
 'mailto',
 'news',
 'telnet',
 'wais',
 'imap',
 'snews',
 'sip',
 'sips']
uses_params = ['ftp',
 'hdl',
 'prospero',
 'http',
 'imap',
 'https',
 'shttp',
 'rtsp',
 'rtspu',
 'sip',
 'sips',
 'mms',
 '',
 'sftp']
uses_query = ['http',
 'wais',
 'imap',
 'https',
 'shttp',
 'mms',
 'gopher',
 'rtsp',
 'rtspu',
 'sip',
 'sips',
 '']
uses_fragment = ['ftp',
 'hdl',
 'http',
 'gopher',
 'news',
 'nntp',
 'wais',
 'https',
 'shttp',
 'snews',
 'file',
 'prospero',
 '']
scheme_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.'
MAX_CACHE_SIZE = 20
_parse_cache = {}

def clear_cache():
    """Clear the parse cache."""
    _parse_cache.clear()


class ResultMixin(object):
    """Shared methods for the parsed result objects."""

    @property
    def username(self):
        netloc = self.netloc
        if '@' in netloc:
            userinfo = netloc.rsplit('@', 1)[0]
            if ':' in userinfo:
                userinfo = userinfo.split(':', 1)[0]
            return userinfo
        else:
            return None

    @property
    def password(self):
        netloc = self.netloc
        if '@' in netloc:
            userinfo = netloc.rsplit('@', 1)[0]
            if ':' in userinfo:
                return userinfo.split(':', 1)[1]
        return None

    @property
    def hostname(self):
        netloc = self.netloc.split('@')[-1]
        if '[' in netloc and ']' in netloc:
            return netloc.split(']')[0][1:].lower()
        elif ':' in netloc:
            return netloc.split(':')[0].lower()
        elif netloc == '':
            return None
        else:
            return netloc.lower()
            return None

    @property
    def port(self):
        netloc = self.netloc.split('@')[-1].split(']')[-1]
        if ':' in netloc:
            port = netloc.split(':')[1]
            return int(port, 10)
        else:
            return None
            return None


from collections import namedtuple

class SplitResult(namedtuple('SplitResult', 'scheme netloc path query fragment'), ResultMixin):
    __slots__ = ()

    def geturl(self):
        return urlunsplit(self)


class ParseResult(namedtuple('ParseResult', 'scheme netloc path params query fragment'), ResultMixin):
    __slots__ = ()

    def geturl(self):
        return urlunparse(self)


def urlparse(url, scheme = '', allow_fragments = True):
    """Parse a URL into 6 components:
    <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    Return a 6-tuple: (scheme, netloc, path, params, query, fragment).
    Note that we don't break the components up in smaller bits
    (e.g. netloc is a single string) and we don't expand % escapes."""
    tuple = urlsplit(url, scheme, allow_fragments)
    scheme, netloc, url, query, fragment = tuple
    if scheme in uses_params and ';' in url:
        url, params = _splitparams(url)
    else:
        params = ''
    return ParseResult(scheme, netloc, url, params, query, fragment)


def _splitparams(url):
    if '/' in url:
        i = url.find(';', url.rfind('/'))
        if i < 0:
            return (url, '')
    else:
        i = url.find(';')
    return (url[:i], url[i + 1:])


def _splitnetloc(url, start = 0):
    delim = len(url)
    for c in '/?#':
        wdelim = url.find(c, start)
        if wdelim >= 0:
            delim = min(delim, wdelim)

    return (url[start:delim], url[delim:])


def urlsplit(url, scheme = '', allow_fragments = True):
    """Parse a URL into 5 components:
    <scheme>://<netloc>/<path>?<query>#<fragment>
    Return a 5-tuple: (scheme, netloc, path, query, fragment).
    Note that we don't break the components up in smaller bits
    (e.g. netloc is a single string) and we don't expand % escapes."""
    allow_fragments = bool(allow_fragments)
    key = (url,
     scheme,
     allow_fragments,
     type(url),
     type(scheme))
    cached = _parse_cache.get(key, None)
    if cached:
        return cached
    else:
        if len(_parse_cache) >= MAX_CACHE_SIZE:
            clear_cache()
        netloc = query = fragment = ''
        i = url.find(':')
        if i > 0:
            if url[:i] == 'http':
                scheme = url[:i].lower()
                url = url[i + 1:]
                if url[:2] == '//':
                    netloc, url = _splitnetloc(url, 2)
                    if '[' in netloc and ']' not in netloc or ']' in netloc and '[' not in netloc:
                        raise ValueError('Invalid IPv6 URL')
                if allow_fragments and '#' in url:
                    url, fragment = url.split('#', 1)
                if '?' in url:
                    url, query = url.split('?', 1)
                v = SplitResult(scheme, netloc, url, query, fragment)
                _parse_cache[key] = v
                return v
            for c in url[:i]:
                if c not in scheme_chars:
                    break
            else:
                try:
                    _testportnum = int(url[i + 1:])
                except ValueError:
                    scheme, url = url[:i].lower(), url[i + 1:]

        if url[:2] == '//':
            netloc, url = _splitnetloc(url, 2)
            if '[' in netloc and ']' not in netloc or ']' in netloc and '[' not in netloc:
                raise ValueError('Invalid IPv6 URL')
        if allow_fragments and scheme in uses_fragment and '#' in url:
            url, fragment = url.split('#', 1)
        if scheme in uses_query and '?' in url:
            url, query = url.split('?', 1)
        v = SplitResult(scheme, netloc, url, query, fragment)
        _parse_cache[key] = v
        return v


def urlunparse(data):
    """Put a parsed URL back together again.  This may result in a
    slightly different, but equivalent URL, if the URL that was parsed
    originally had redundant delimiters, e.g. a ? with an empty query
    (the draft states that these are equivalent)."""
    scheme, netloc, url, params, query, fragment = data
    if params:
        url = '%s;%s' % (url, params)
    return urlunsplit((scheme,
     netloc,
     url,
     query,
     fragment))


def urlunsplit(data):
    """Combine the elements of a tuple as returned by urlsplit() into a
    complete URL as a string. The data argument can be any five-item iterable.
    This may result in a slightly different, but equivalent URL, if the URL that
    was parsed originally had unnecessary delimiters (for example, a ? with an
    empty query; the RFC states that these are equivalent)."""
    scheme, netloc, url, query, fragment = data
    if netloc or scheme and scheme in uses_netloc and url[:2] != '//':
        if url and url[:1] != '/':
            url = '/' + url
        url = '//' + (netloc or '') + url
    if scheme:
        url = scheme + ':' + url
    if query:
        url = url + '?' + query
    if fragment:
        url = url + '#' + fragment
    return url


def urljoin--- This code section failed: ---

0	LOAD_FAST         'base'
3	POP_JUMP_IF_TRUE  '10'

6	LOAD_FAST         'url'
9	RETURN_END_IF     None

10	LOAD_FAST         'url'
13	POP_JUMP_IF_TRUE  '20'

16	LOAD_FAST         'base'
19	RETURN_END_IF     None

20	LOAD_GLOBAL       'urlparse'
23	LOAD_FAST         'base'
26	LOAD_CONST        ''
29	LOAD_FAST         'allow_fragments'
32	CALL_FUNCTION_3   None
35	UNPACK_SEQUENCE_6 None
38	STORE_FAST        'bscheme'
41	STORE_FAST        'bnetloc'
44	STORE_FAST        'bpath'
47	STORE_FAST        'bparams'
50	STORE_FAST        'bquery'
53	STORE_FAST        'bfragment'

56	LOAD_GLOBAL       'urlparse'
59	LOAD_FAST         'url'
62	LOAD_FAST         'bscheme'
65	LOAD_FAST         'allow_fragments'
68	CALL_FUNCTION_3   None
71	UNPACK_SEQUENCE_6 None
74	STORE_FAST        'scheme'
77	STORE_FAST        'netloc'
80	STORE_FAST        'path'
83	STORE_FAST        'params'
86	STORE_FAST        'query'
89	STORE_FAST        'fragment'

92	LOAD_FAST         'scheme'
95	LOAD_FAST         'bscheme'
98	COMPARE_OP        '!='
101	POP_JUMP_IF_TRUE  '116'
104	LOAD_FAST         'scheme'
107	LOAD_GLOBAL       'uses_relative'
110	COMPARE_OP        'not in'
113_0	COME_FROM         '101'
113	POP_JUMP_IF_FALSE '120'

116	LOAD_FAST         'url'
119	RETURN_END_IF     None

120	LOAD_FAST         'scheme'
123	LOAD_GLOBAL       'uses_netloc'
126	COMPARE_OP        'in'
129	POP_JUMP_IF_FALSE '175'

132	LOAD_FAST         'netloc'
135	POP_JUMP_IF_FALSE '166'

138	LOAD_GLOBAL       'urlunparse'
141	LOAD_FAST         'scheme'
144	LOAD_FAST         'netloc'
147	LOAD_FAST         'path'

150	LOAD_FAST         'params'
153	LOAD_FAST         'query'
156	LOAD_FAST         'fragment'
159	BUILD_TUPLE_6     None
162	CALL_FUNCTION_1   None
165	RETURN_END_IF     None

166	LOAD_FAST         'bnetloc'
169	STORE_FAST        'netloc'
172	JUMP_FORWARD      '175'
175_0	COME_FROM         '172'

175	LOAD_FAST         'path'
178	LOAD_CONST        1
181	SLICE+2           None
182	LOAD_CONST        '/'
185	COMPARE_OP        '=='
188	POP_JUMP_IF_FALSE '219'

191	LOAD_GLOBAL       'urlunparse'
194	LOAD_FAST         'scheme'
197	LOAD_FAST         'netloc'
200	LOAD_FAST         'path'

203	LOAD_FAST         'params'
206	LOAD_FAST         'query'
209	LOAD_FAST         'fragment'
212	BUILD_TUPLE_6     None
215	CALL_FUNCTION_1   None
218	RETURN_END_IF     None

219	LOAD_FAST         'path'
222	UNARY_NOT         None
223	POP_JUMP_IF_FALSE '288'
226	LOAD_FAST         'params'
229	UNARY_NOT         None
230_0	COME_FROM         '223'
230	POP_JUMP_IF_FALSE '288'

233	LOAD_FAST         'bpath'
236	STORE_FAST        'path'

239	LOAD_FAST         'bparams'
242	STORE_FAST        'params'

245	LOAD_FAST         'query'
248	POP_JUMP_IF_TRUE  '260'

251	LOAD_FAST         'bquery'
254	STORE_FAST        'query'
257	JUMP_FORWARD      '260'
260_0	COME_FROM         '257'

260	LOAD_GLOBAL       'urlunparse'
263	LOAD_FAST         'scheme'
266	LOAD_FAST         'netloc'
269	LOAD_FAST         'path'

272	LOAD_FAST         'params'
275	LOAD_FAST         'query'
278	LOAD_FAST         'fragment'
281	BUILD_TUPLE_6     None
284	CALL_FUNCTION_1   None
287	RETURN_END_IF     None

288	LOAD_FAST         'bpath'
291	LOAD_ATTR         'split'
294	LOAD_CONST        '/'
297	CALL_FUNCTION_1   None
300	LOAD_CONST        -1
303	SLICE+2           None
304	LOAD_FAST         'path'
307	LOAD_ATTR         'split'
310	LOAD_CONST        '/'
313	CALL_FUNCTION_1   None
316	BINARY_ADD        None
317	STORE_FAST        'segments'

320	LOAD_FAST         'segments'
323	LOAD_CONST        -1
326	BINARY_SUBSCR     None
327	LOAD_CONST        '.'
330	COMPARE_OP        '=='
333	POP_JUMP_IF_FALSE '349'

336	LOAD_CONST        ''
339	LOAD_FAST         'segments'
342	LOAD_CONST        -1
345	STORE_SUBSCR      None
346	JUMP_FORWARD      '349'
349_0	COME_FROM         '346'

349	SETUP_LOOP        '381'
352	LOAD_CONST        '.'
355	LOAD_FAST         'segments'
358	COMPARE_OP        'in'
361	POP_JUMP_IF_FALSE '380'

364	LOAD_FAST         'segments'
367	LOAD_ATTR         'remove'
370	LOAD_CONST        '.'
373	CALL_FUNCTION_1   None
376	POP_TOP           None
377	JUMP_BACK         '352'
380	POP_BLOCK         None
381_0	COME_FROM         '349'

381	SETUP_LOOP        '498'

384	LOAD_CONST        1
387	STORE_FAST        'i'

390	LOAD_GLOBAL       'len'
393	LOAD_FAST         'segments'
396	CALL_FUNCTION_1   None
399	LOAD_CONST        1
402	BINARY_SUBTRACT   None
403	STORE_FAST        'n'

406	SETUP_LOOP        '494'
409	LOAD_FAST         'i'
412	LOAD_FAST         'n'
415	COMPARE_OP        '<'
418	POP_JUMP_IF_FALSE '492'

421	LOAD_FAST         'segments'
424	LOAD_FAST         'i'
427	BINARY_SUBSCR     None
428	LOAD_CONST        '..'
431	COMPARE_OP        '=='
434	POP_JUMP_IF_FALSE '479'

437	LOAD_FAST         'segments'
440	LOAD_FAST         'i'
443	LOAD_CONST        1
446	BINARY_SUBTRACT   None
447	BINARY_SUBSCR     None
448	LOAD_CONST        ('', '..')
451	COMPARE_OP        'not in'
454_0	COME_FROM         '434'
454	POP_JUMP_IF_FALSE '479'

457	LOAD_FAST         'segments'
460	LOAD_FAST         'i'
463	LOAD_CONST        1
466	BINARY_SUBTRACT   None
467	LOAD_FAST         'i'
470	LOAD_CONST        1
473	BINARY_ADD        None
474	DELETE_SLICE+3    None

475	BREAK_LOOP        None
476	JUMP_FORWARD      '479'
479_0	COME_FROM         '476'

479	LOAD_FAST         'i'
482	LOAD_CONST        1
485	BINARY_ADD        None
486	STORE_FAST        'i'
489	JUMP_BACK         '409'
492	POP_BLOCK         None

493	BREAK_LOOP        None
494_0	COME_FROM         '406'
494	JUMP_BACK         '384'
497	POP_BLOCK         None
498_0	COME_FROM         '381'

498	LOAD_FAST         'segments'
501	LOAD_CONST        ''
504	LOAD_CONST        '..'
507	BUILD_LIST_2      None
510	COMPARE_OP        '=='
513	POP_JUMP_IF_FALSE '529'

516	LOAD_CONST        ''
519	LOAD_FAST         'segments'
522	LOAD_CONST        -1
525	STORE_SUBSCR      None
526	JUMP_FORWARD      '579'

529	LOAD_GLOBAL       'len'
532	LOAD_FAST         'segments'
535	CALL_FUNCTION_1   None
538	LOAD_CONST        2
541	COMPARE_OP        '>='
544	POP_JUMP_IF_FALSE '579'
547	LOAD_FAST         'segments'
550	LOAD_CONST        -1
553	BINARY_SUBSCR     None
554	LOAD_CONST        '..'
557	COMPARE_OP        '=='
560_0	COME_FROM         '544'
560	POP_JUMP_IF_FALSE '579'

563	LOAD_CONST        ''
566	BUILD_LIST_1      None
569	LOAD_FAST         'segments'
572	LOAD_CONST        -2
575	STORE_SLICE+1     None
576	JUMP_FORWARD      '579'
579_0	COME_FROM         '526'
579_1	COME_FROM         '576'

579	LOAD_GLOBAL       'urlunparse'
582	LOAD_FAST         'scheme'
585	LOAD_FAST         'netloc'
588	LOAD_CONST        '/'
591	LOAD_ATTR         'join'
594	LOAD_FAST         'segments'
597	CALL_FUNCTION_1   None

600	LOAD_FAST         'params'
603	LOAD_FAST         'query'
606	LOAD_FAST         'fragment'
609	BUILD_TUPLE_6     None
612	CALL_FUNCTION_1   None
615	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 497


def urldefrag(url):
    """Removes any existing fragment from URL.
    
    Returns a tuple of the defragmented URL and the fragment.  If
    the URL contained no fragments, the second element is the
    empty string.
    """
    if '#' in url:
        s, n, p, a, q, frag = urlparse(url)
        defrag = urlunparse((s,
         n,
         p,
         a,
         q,
         ''))
        return (defrag, frag)
    else:
        return (url, '')


_hexdig = '0123456789ABCDEFabcdef'
_hextochr = dict(((a + b, chr(int(a + b, 16))) for a in _hexdig for b in _hexdig))

def unquote(s):
    """unquote('abc%20def') -> 'abc def'."""
    res = s.split('%')
    if len(res) == 1:
        return s
    s = res[0]
    for item in res[1:]:
        try:
            s += _hextochr[item[:2]] + item[2:]
        except KeyError:
            s += '%' + item
        except UnicodeDecodeError:
            s += unichr(int(item[:2], 16)) + item[2:]

    return s


def parse_qs(qs, keep_blank_values = 0, strict_parsing = 0):
    """Parse a query given as a string argument.
    
        Arguments:
    
        qs: percent-encoded query string to be parsed
    
        keep_blank_values: flag indicating whether blank values in
            percent-encoded queries should be treated as blank strings.
            A true value indicates that blanks should be retained as
            blank strings.  The default false value indicates that
            blank values are to be ignored and treated as if they were
            not included.
    
        strict_parsing: flag indicating what to do with parsing errors.
            If false (the default), errors are silently ignored.
            If true, errors raise a ValueError exception.
    """
    dict = {}
    for name, value in parse_qsl(qs, keep_blank_values, strict_parsing):
        if name in dict:
            dict[name].append(value)
        else:
            dict[name] = [value]

    return dict


def parse_qsl(qs, keep_blank_values = 0, strict_parsing = 0):
    """Parse a query given as a string argument.
    
    Arguments:
    
    qs: percent-encoded query string to be parsed
    
    keep_blank_values: flag indicating whether blank values in
        percent-encoded queries should be treated as blank strings.  A
        true value indicates that blanks should be retained as blank
        strings.  The default false value indicates that blank values
        are to be ignored and treated as if they were  not included.
    
    strict_parsing: flag indicating what to do with parsing errors. If
        false (the default), errors are silently ignored. If true,
        errors raise a ValueError exception.
    
    Returns a list, as G-d intended.
    """
    pairs = [ s2 for s1 in qs.split('&') for s2 in s1.split(';') ]
    r = []
    for name_value in pairs:
        if not name_value and not strict_parsing:
            continue
        nv = name_value.split('=', 1)
        if len(nv) != 2:
            if strict_parsing:
                raise ValueError, 'bad query field: %r' % (name_value,)
            if keep_blank_values:
                nv.append('')
            else:
                continue
        if len(nv[1]) or keep_blank_values:
            name = unquote(nv[0].replace('+', ' '))
            value = unquote(nv[1].replace('+', ' '))
            r.append((name, value))

    return r