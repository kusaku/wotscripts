# Embedded file name: scripts/common/Lib/test/test_MimeWriter.py
"""Test program for MimeWriter module.

The test program was too big to comfortably fit in the MimeWriter
class, so it's here in its own file.

This should generate Barry's example, modulo some quotes and newlines.

"""
import unittest, StringIO
from test.test_support import run_unittest, import_module
import_module('MimeWriter', deprecated=True)
from MimeWriter import MimeWriter
SELLER = 'INTERFACE Seller-1;\n\nTYPE Seller = OBJECT\n    DOCUMENTATION "A simple Seller interface to test ILU"\n    METHODS\n            price():INTEGER,\n    END;\n'
BUYER = 'class Buyer:\n    def __setup__(self, maxprice):\n        self._maxprice = maxprice\n\n    def __main__(self, kos):\n        """Entry point upon arrival at a new KOS."""\n        broker = kos.broker()\n        # B4 == Barry\'s Big Bass Business :-)\n        seller = broker.lookup(\'Seller_1.Seller\', \'B4\')\n        if seller:\n            price = seller.price()\n            print \'Seller wants $\', price, \'... \'\n            if price > self._maxprice:\n                print \'too much!\'\n            else:\n                print "I\'ll take it!"\n        else:\n            print \'no seller found here\'\n'
STATE = '# instantiate a buyer instance and put it in a magic place for the KOS\n# to find.\n__kp__ = Buyer()\n__kp__.__setup__(500)\n'
SIMPLE_METADATA = [('Interpreter', 'python'),
 ('Interpreter-Version', '1.3'),
 ('Owner-Name', 'Barry Warsaw'),
 ('Owner-Rendezvous', 'bwarsaw@cnri.reston.va.us'),
 ('Home-KSS', 'kss.cnri.reston.va.us'),
 ('Identifier', 'hdl://cnri.kss/my_first_knowbot'),
 ('Launch-Date', 'Mon Feb 12 16:39:03 EST 1996')]
COMPLEX_METADATA = [('Metadata-Type', 'complex'),
 ('Metadata-Key', 'connection'),
 ('Access', 'read-only'),
 ('Connection-Description', "Barry's Big Bass Business"),
 ('Connection-Id', 'B4'),
 ('Connection-Direction', 'client')]
EXTERNAL_METADATA = [('Metadata-Type', 'complex'),
 ('Metadata-Key', 'generic-interface'),
 ('Access', 'read-only'),
 ('Connection-Description', 'Generic Interface for All Knowbots'),
 ('Connection-Id', 'generic-kp'),
 ('Connection-Direction', 'client')]
OUTPUT = 'From: bwarsaw@cnri.reston.va.us\nDate: Mon Feb 12 17:21:48 EST 1996\nTo: kss-submit@cnri.reston.va.us\nMIME-Version: 1.0\nContent-Type: multipart/knowbot;\n    boundary="801spam999";\n    version="0.1"\n\nThis is a multi-part message in MIME format.\n\n--801spam999\nContent-Type: multipart/knowbot-metadata;\n    boundary="802spam999"\n\n\n--802spam999\nContent-Type: message/rfc822\nKP-Metadata-Type: simple\nKP-Access: read-only\n\nKPMD-Interpreter: python\nKPMD-Interpreter-Version: 1.3\nKPMD-Owner-Name: Barry Warsaw\nKPMD-Owner-Rendezvous: bwarsaw@cnri.reston.va.us\nKPMD-Home-KSS: kss.cnri.reston.va.us\nKPMD-Identifier: hdl://cnri.kss/my_first_knowbot\nKPMD-Launch-Date: Mon Feb 12 16:39:03 EST 1996\n\n--802spam999\nContent-Type: text/isl\nKP-Metadata-Type: complex\nKP-Metadata-Key: connection\nKP-Access: read-only\nKP-Connection-Description: Barry\'s Big Bass Business\nKP-Connection-Id: B4\nKP-Connection-Direction: client\n\nINTERFACE Seller-1;\n\nTYPE Seller = OBJECT\n    DOCUMENTATION "A simple Seller interface to test ILU"\n    METHODS\n            price():INTEGER,\n    END;\n\n--802spam999\nContent-Type: message/external-body;\n    access-type="URL";\n    URL="hdl://cnri.kss/generic-knowbot"\n\nContent-Type: text/isl\nKP-Metadata-Type: complex\nKP-Metadata-Key: generic-interface\nKP-Access: read-only\nKP-Connection-Description: Generic Interface for All Knowbots\nKP-Connection-Id: generic-kp\nKP-Connection-Direction: client\n\n\n--802spam999--\n\n--801spam999\nContent-Type: multipart/knowbot-code;\n    boundary="803spam999"\n\n\n--803spam999\nContent-Type: text/plain\nKP-Module-Name: BuyerKP\n\nclass Buyer:\n    def __setup__(self, maxprice):\n        self._maxprice = maxprice\n\n    def __main__(self, kos):\n        """Entry point upon arrival at a new KOS."""\n        broker = kos.broker()\n        # B4 == Barry\'s Big Bass Business :-)\n        seller = broker.lookup(\'Seller_1.Seller\', \'B4\')\n        if seller:\n            price = seller.price()\n            print \'Seller wants $\', price, \'... \'\n            if price > self._maxprice:\n                print \'too much!\'\n            else:\n                print "I\'ll take it!"\n        else:\n            print \'no seller found here\'\n\n--803spam999--\n\n--801spam999\nContent-Type: multipart/knowbot-state;\n    boundary="804spam999"\nKP-Main-Module: main\n\n\n--804spam999\nContent-Type: text/plain\nKP-Module-Name: main\n\n# instantiate a buyer instance and put it in a magic place for the KOS\n# to find.\n__kp__ = Buyer()\n__kp__.__setup__(500)\n\n--804spam999--\n\n--801spam999--\n'

class MimewriterTest(unittest.TestCase):

    def test(self):
        buf = StringIO.StringIO()
        toplevel = MimeWriter(buf)
        toplevel.addheader('From', 'bwarsaw@cnri.reston.va.us')
        toplevel.addheader('Date', 'Mon Feb 12 17:21:48 EST 1996')
        toplevel.addheader('To', 'kss-submit@cnri.reston.va.us')
        toplevel.addheader('MIME-Version', '1.0')
        f = toplevel.startmultipartbody('knowbot', '801spam999', [('version', '0.1')], prefix=0)
        f.write('This is a multi-part message in MIME format.\n')
        md = toplevel.nextpart()
        md.startmultipartbody('knowbot-metadata', '802spam999')
        md1 = md.nextpart()
        md1.addheader('KP-Metadata-Type', 'simple')
        md1.addheader('KP-Access', 'read-only')
        m = MimeWriter(md1.startbody('message/rfc822'))
        for key, value in SIMPLE_METADATA:
            m.addheader('KPMD-' + key, value)

        m.flushheaders()
        del md1
        md2 = md.nextpart()
        for key, value in COMPLEX_METADATA:
            md2.addheader('KP-' + key, value)

        f = md2.startbody('text/isl')
        f.write(SELLER)
        del md2
        md3 = md.nextpart()
        f = md3.startbody('message/external-body', [('access-type', 'URL'), ('URL', 'hdl://cnri.kss/generic-knowbot')])
        m = MimeWriter(f)
        for key, value in EXTERNAL_METADATA:
            md3.addheader('KP-' + key, value)

        md3.startbody('text/isl')
        md.lastpart()
        code = toplevel.nextpart()
        code.startmultipartbody('knowbot-code', '803spam999')
        buyer = code.nextpart()
        buyer.addheader('KP-Module-Name', 'BuyerKP')
        f = buyer.startbody('text/plain')
        f.write(BUYER)
        code.lastpart()
        state = toplevel.nextpart()
        state.addheader('KP-Main-Module', 'main')
        state.startmultipartbody('knowbot-state', '804spam999')
        st = state.nextpart()
        st.addheader('KP-Module-Name', 'main')
        f = st.startbody('text/plain')
        f.write(STATE)
        state.lastpart()
        toplevel.lastpart()
        self.assertEqual(buf.getvalue(), OUTPUT)


def test_main():
    run_unittest(MimewriterTest)


if __name__ == '__main__':
    test_main()