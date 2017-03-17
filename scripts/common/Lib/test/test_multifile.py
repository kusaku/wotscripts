# Embedded file name: scripts/common/Lib/test/test_multifile.py
from test import test_support
mimetools = test_support.import_module('mimetools', deprecated=True)
multifile = test_support.import_module('multifile', deprecated=True)
import cStringIO
msg = 'Mime-Version: 1.0\nContent-Type: multipart/mixed;\n        boundary="=====================_590453667==_"\nX-OriginalArrivalTime: 05 Feb 2002 03:43:23.0310 (UTC) FILETIME=[42D88CE0:01C1ADF7]\n\n--=====================_590453667==_\nContent-Type: multipart/alternative;\n        boundary="=====================_590453677==_.ALT"\n\n--=====================_590453677==_.ALT\nContent-Type: text/plain; charset="us-ascii"; format=flowed\n\ntest A\n--=====================_590453677==_.ALT\nContent-Type: text/html; charset="us-ascii"\n\n<html>\n<b>test B</font></b></html>\n\n--=====================_590453677==_.ALT--\n\n--=====================_590453667==_\nContent-Type: text/plain; charset="us-ascii"\nContent-Disposition: attachment; filename="att.txt"\n\nAttached Content.\nAttached Content.\nAttached Content.\nAttached Content.\n\n--=====================_590453667==_--\n\n'

def getMIMEMsg(mf):
    global boundaries
    global linecount
    msg = mimetools.Message(mf)
    if msg.getmaintype() == 'multipart':
        boundary = msg.getparam('boundary')
        boundaries += 1
        mf.push(boundary)
        while mf.next():
            getMIMEMsg(mf)

        mf.pop()
    else:
        lines = mf.readlines()
        linecount += len(lines)


def test_main():
    global boundaries
    global linecount
    boundaries = 0
    linecount = 0
    f = cStringIO.StringIO(msg)
    getMIMEMsg(multifile.MultiFile(f))
    raise boundaries == 2 or AssertionError
    raise linecount == 9 or AssertionError


if __name__ == '__main__':
    test_main()