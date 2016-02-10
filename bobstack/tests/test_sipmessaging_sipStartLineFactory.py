try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging import SIPStartLineFactory


class TestSIPStartLineFactoryForResponse(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'SIP/2.0 100 Trying',
            'SIP/2.0 100 Trying and trying and trying']

    def test_parsing(self):
        for line in self.canonicalStrings:
            startLine = SIPStartLineFactory().nextForString(line)
            self.assertFalse(startLine.isRequest)
            self.assertTrue(startLine.isResponse)
            self.assertFalse(startLine.isMalformed)
            self.assertEqual(startLine.rawString, line)
            self.assertIsInstance(startLine.statusCode, (int, long))
            self.assertIsInstance(startLine.reasonPhrase, basestring)
        self.assertEqual(100, SIPStartLineFactory().nextForString(self.canonicalStrings[0]).statusCode)
        self.assertEqual('Trying', SIPStartLineFactory().nextForString(self.canonicalStrings[0]).reasonPhrase)
        self.assertEqual(100, SIPStartLineFactory().nextForString(self.canonicalStrings[1]).statusCode)
        self.assertEqual('Trying and trying and trying', SIPStartLineFactory().nextForString(self.canonicalStrings[1]).reasonPhrase)
        stringio = StringIO(self.canonicalStrings[1] + '\r\n')
        self.assertEqual('Trying and trying and trying', SIPStartLineFactory().nextForStringIO(stringio).reasonPhrase)
        stringio.close()


class TestSIPStartLineFactoryForRequest(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'INVITE sip:5551212@127.0.0.1:5060 SIP/2.0',
            'INVITE sip:5551212@127.0.0.1:5060;transport=udp;user=phone;trusted;gw SIP/2.0']

    def test_parsing(self):
        for line in self.canonicalStrings:
            startLine = SIPStartLineFactory().nextForString(line)
            self.assertTrue(startLine.isRequest)
            self.assertFalse(startLine.isResponse)
            self.assertFalse(startLine.isMalformed)
            self.assertEqual(startLine.rawString, line)
            self.assertIsInstance(startLine.sipMethod, basestring)
            self.assertTrue(startLine.sipMethod.__len__() > 0)
            self.assertIsInstance(startLine.requestURI, basestring)
            self.assertTrue(startLine.requestURI.__len__() > 0)
        self.assertEqual('INVITE', SIPStartLineFactory().nextForString(self.canonicalStrings[0]).sipMethod)
        self.assertEqual('sip:5551212@127.0.0.1:5060', SIPStartLineFactory().nextForString(self.canonicalStrings[0]).requestURI)
        self.assertEqual('INVITE', SIPStartLineFactory().nextForString(self.canonicalStrings[1]).sipMethod)
        self.assertEqual('sip:5551212@127.0.0.1:5060;transport=udp;user=phone;trusted;gw', SIPStartLineFactory().nextForString(self.canonicalStrings[1]).requestURI)
        stringio = StringIO(self.canonicalStrings[1] + '\r\n')
        self.assertEqual('sip:5551212@127.0.0.1:5060;transport=udp;user=phone;trusted;gw', SIPStartLineFactory().nextForStringIO(stringio).requestURI)
        stringio.close()


class TestSIPStartLineFactoryForMalformed(TestCase):
    @property
    def canonicalStrings(self):
        return [
            '',
            'fajdoutawledsuloiur',
            'fdfoisfoisdjfljdsf dfdsfjsdilj dfljd',
            'INVITE sip:5551212@127.0.0.1:5060 SUP/2.0',
            'SUP/2.0 100 Trying',
            'SIP/2.0 foo Trying',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            startLine = SIPStartLineFactory().nextForString(line)
            self.assertFalse(startLine.isRequest)
            self.assertFalse(startLine.isResponse)
            self.assertTrue(startLine.isMalformed)
            self.assertEqual(startLine.rawString, line)
            if line:
                stringio = StringIO(line + '\r\n')
                startLine = SIPStartLineFactory().nextForStringIO(stringio)
                self.assertFalse(startLine.isRequest)
                self.assertFalse(startLine.isResponse)
                self.assertTrue(startLine.isMalformed)
                self.assertEqual(startLine.rawString, line)
                stringio.close()

