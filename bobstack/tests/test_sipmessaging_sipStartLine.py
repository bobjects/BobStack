from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging import SIPRequestStartLine
from sipmessaging import SIPResponseStartLine
from sipmessaging import MalformedSIPStartLine


class TestMalformedSIPStartLine(TestCase):
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
            self.assertFalse(SIPRequestStartLine.canMatchString(line))
            self.assertFalse(SIPResponseStartLine.canMatchString(line))
            start_line = MalformedSIPStartLine.newParsedFrom(line)
            self.assertFalse(start_line.isRequest)
            self.assertFalse(start_line.isResponse)
            self.assertTrue(start_line.isMalformed)
            self.assertEqual(start_line.rawString, line)


class TestSIPResponseStartLine(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'SIP/2.0 100 Trying',
            'SIP/2.0 100 Trying and trying and trying']

    def test_parsing(self):
        for line in self.canonicalStrings:
            self.assertFalse(SIPRequestStartLine.canMatchString(line))
            self.assertTrue(SIPResponseStartLine.canMatchString(line))
            start_line = SIPResponseStartLine.newParsedFrom(line)
            self.assertFalse(start_line.isRequest)
            self.assertTrue(start_line.isResponse)
            self.assertFalse(start_line.isMalformed)
            self.assertEqual(start_line.rawString, line)
            self.assertIsInstance(start_line.status_code, (int, long))
            self.assertIsInstance(start_line.reason_phrase, basestring)
            start_line.rawString = "SIP/2.0 200 OK"
            self.assertEqual(200, start_line.status_code)
            self.assertEqual("OK", start_line.reason_phrase)
            self.assertEqual("SIP/2.0 200 OK", start_line.rawString)
        self.assertEqual(100, SIPResponseStartLine.newParsedFrom(self.canonicalStrings[0]).status_code)
        self.assertEqual('Trying', SIPResponseStartLine.newParsedFrom(self.canonicalStrings[0]).reason_phrase)
        self.assertEqual(100, SIPResponseStartLine.newParsedFrom(self.canonicalStrings[1]).status_code)
        self.assertEqual('Trying and trying and trying', SIPResponseStartLine.newParsedFrom(self.canonicalStrings[1]).reason_phrase)

    def test_rendering(self):
        start_line = SIPResponseStartLine.newForAttributes(status_code=401, reason_phrase="Not Authorized")
        self.assertEqual(401, start_line.status_code)
        self.assertEqual("Not Authorized", start_line.reason_phrase)
        self.assertEqual("SIP/2.0 401 Not Authorized", start_line.rawString)
        start_line.status_code = 200
        start_line.reason_phrase = "OK"
        self.assertEqual(200, start_line.status_code)
        self.assertEqual("OK", start_line.reason_phrase)
        self.assertEqual("SIP/2.0 200 OK", start_line.rawString)


class TestSIPRequestStartLine(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'INVITE sip:5551212@127.0.0.1:5060 SIP/2.0',
            'INVITE sip:5551212@127.0.0.1:5060;transport=udp;user=phone;trusted;gw SIP/2.0']

    def test_parsing(self):
        for line in self.canonicalStrings:
            self.assertTrue(SIPRequestStartLine.canMatchString(line))
            self.assertFalse(SIPResponseStartLine.canMatchString(line))
            start_line = SIPRequestStartLine.newParsedFrom(line)
            self.assertTrue(start_line.isRequest)
            self.assertFalse(start_line.isResponse)
            self.assertFalse(start_line.isMalformed)
            self.assertEqual(start_line.rawString, line)
            self.assertIsInstance(start_line.sip_method, basestring)
            self.assertTrue(start_line.sip_method.__len__() > 0)
            self.assertIsInstance(start_line.request_uri, basestring)
            self.assertTrue(start_line.request_uri.__len__() > 0)
            start_line.rawString = "BYE sip:1115252@127.0.0.1:5060 SIP/2.0"
            self.assertEqual("BYE", start_line.sip_method)
            self.assertEqual("sip:1115252@127.0.0.1:5060", start_line.request_uri)
            self.assertEqual("BYE sip:1115252@127.0.0.1:5060 SIP/2.0", start_line.rawString)
        self.assertEqual('INVITE', SIPRequestStartLine.newParsedFrom(self.canonicalStrings[0]).sip_method)
        self.assertEqual('sip:5551212@127.0.0.1:5060', SIPRequestStartLine.newParsedFrom(self.canonicalStrings[0]).request_uri)
        self.assertEqual('INVITE', SIPRequestStartLine.newParsedFrom(self.canonicalStrings[1]).sip_method)
        self.assertEqual('sip:5551212@127.0.0.1:5060;transport=udp;user=phone;trusted;gw', SIPRequestStartLine.newParsedFrom(self.canonicalStrings[1]).request_uri)

    def test_rendering(self):
        start_line = SIPRequestStartLine.newForAttributes(sip_method="INVITE", request_uri="sip:5551212@127.0.0.1:5060")
        self.assertEqual("INVITE", start_line.sip_method)
        self.assertEqual("sip:5551212@127.0.0.1:5060", start_line.request_uri)
        self.assertEqual("INVITE sip:5551212@127.0.0.1:5060 SIP/2.0", start_line.rawString)
        start_line.sip_method = "BYE"
        start_line.request_uri = "sip:1115252@127.0.0.1:5060"
        self.assertEqual("BYE", start_line.sip_method)
        self.assertEqual("sip:1115252@127.0.0.1:5060", start_line.request_uri)
        self.assertEqual("BYE sip:1115252@127.0.0.1:5060 SIP/2.0", start_line.rawString)
