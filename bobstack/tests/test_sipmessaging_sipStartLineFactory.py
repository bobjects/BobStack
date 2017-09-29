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
            start_line = SIPStartLineFactory().nextForString(line)
            self.assertFalse(start_line.isRequest)
            self.assertTrue(start_line.isResponse)
            self.assertFalse(start_line.isMalformed)
            self.assertEqual(start_line.rawString, line)
            self.assertIsInstance(start_line.status_code, (int, long))
            self.assertIsInstance(start_line.reason_phrase, basestring)
        self.assertEqual(100, SIPStartLineFactory().nextForString(self.canonicalStrings[0]).status_code)
        self.assertEqual('Trying', SIPStartLineFactory().nextForString(self.canonicalStrings[0]).reason_phrase)
        self.assertEqual(100, SIPStartLineFactory().nextForString(self.canonicalStrings[1]).status_code)
        self.assertEqual('Trying and trying and trying', SIPStartLineFactory().nextForString(self.canonicalStrings[1]).reason_phrase)
        stringio = StringIO(self.canonicalStrings[1] + '\r\n')
        self.assertEqual('Trying and trying and trying', SIPStartLineFactory().nextForStringIO(stringio).reason_phrase)
        stringio.close()


class TestSIPStartLineFactoryForRequest(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'INVITE sip:5551212@127.0.0.1:5060 SIP/2.0',
            'INVITE sip:5551212@127.0.0.1:5060;transport=udp;user=phone;trusted;gw SIP/2.0']

    def test_parsing(self):
        for line in self.canonicalStrings:
            start_line = SIPStartLineFactory().nextForString(line)
            self.assertTrue(start_line.isRequest)
            self.assertFalse(start_line.isResponse)
            self.assertFalse(start_line.isMalformed)
            self.assertEqual(start_line.rawString, line)
            self.assertIsInstance(start_line.sip_method, basestring)
            self.assertTrue(start_line.sip_method.__len__() > 0)
            self.assertIsInstance(start_line.request_uri, basestring)
            self.assertTrue(start_line.request_uri.__len__() > 0)
        self.assertEqual('INVITE', SIPStartLineFactory().nextForString(self.canonicalStrings[0]).sip_method)
        self.assertEqual('sip:5551212@127.0.0.1:5060', SIPStartLineFactory().nextForString(self.canonicalStrings[0]).request_uri)
        self.assertEqual('INVITE', SIPStartLineFactory().nextForString(self.canonicalStrings[1]).sip_method)
        self.assertEqual('sip:5551212@127.0.0.1:5060;transport=udp;user=phone;trusted;gw', SIPStartLineFactory().nextForString(self.canonicalStrings[1]).request_uri)
        stringio = StringIO(self.canonicalStrings[1] + '\r\n')
        self.assertEqual('sip:5551212@127.0.0.1:5060;transport=udp;user=phone;trusted;gw', SIPStartLineFactory().nextForStringIO(stringio).request_uri)
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
            start_line = SIPStartLineFactory().nextForString(line)
            self.assertFalse(start_line.isRequest)
            self.assertFalse(start_line.isResponse)
            self.assertTrue(start_line.isMalformed)
            self.assertEqual(start_line.rawString, line)
            if line:
                stringio = StringIO(line + '\r\n')
                start_line = SIPStartLineFactory().nextForStringIO(stringio)
                self.assertFalse(start_line.isRequest)
                self.assertFalse(start_line.isResponse)
                self.assertTrue(start_line.isMalformed)
                self.assertEqual(start_line.rawString, line)
                stringio.close()

