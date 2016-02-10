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
            startLine = MalformedSIPStartLine.newParsedFrom(line)
            self.assertFalse(startLine.isRequest)
            self.assertFalse(startLine.isResponse)
            self.assertTrue(startLine.isMalformed)
            self.assertEqual(startLine.rawString, line)


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
            startLine = SIPResponseStartLine.newParsedFrom(line)
            self.assertFalse(startLine.isRequest)
            self.assertTrue(startLine.isResponse)
            self.assertFalse(startLine.isMalformed)
            self.assertEqual(startLine.rawString, line)
            self.assertIsInstance(startLine.statusCode, (int, long))
            self.assertIsInstance(startLine.reasonPhrase, basestring)
            startLine.rawString = "SIP/2.0 200 OK"
            self.assertEqual(200, startLine.statusCode)
            self.assertEqual("OK", startLine.reasonPhrase)
            self.assertEqual("SIP/2.0 200 OK", startLine.rawString)
        self.assertEqual(100, SIPResponseStartLine.newParsedFrom(self.canonicalStrings[0]).statusCode)
        self.assertEqual('Trying', SIPResponseStartLine.newParsedFrom(self.canonicalStrings[0]).reasonPhrase)
        self.assertEqual(100, SIPResponseStartLine.newParsedFrom(self.canonicalStrings[1]).statusCode)
        self.assertEqual('Trying and trying and trying', SIPResponseStartLine.newParsedFrom(self.canonicalStrings[1]).reasonPhrase)

    def test_rendering(self):
        startLine = SIPResponseStartLine.newForAttributes(statusCode=401, reasonPhrase="Not Authorized")
        self.assertEqual(401, startLine.statusCode)
        self.assertEqual("Not Authorized", startLine.reasonPhrase)
        self.assertEqual("SIP/2.0 401 Not Authorized", startLine.rawString)
        startLine.statusCode = 200
        startLine.reasonPhrase = "OK"
        self.assertEqual(200, startLine.statusCode)
        self.assertEqual("OK", startLine.reasonPhrase)
        self.assertEqual("SIP/2.0 200 OK", startLine.rawString)


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
            startLine = SIPRequestStartLine.newParsedFrom(line)
            self.assertTrue(startLine.isRequest)
            self.assertFalse(startLine.isResponse)
            self.assertFalse(startLine.isMalformed)
            self.assertEqual(startLine.rawString, line)
            self.assertIsInstance(startLine.sipMethod, basestring)
            self.assertTrue(startLine.sipMethod.__len__() > 0)
            self.assertIsInstance(startLine.requestURI, basestring)
            self.assertTrue(startLine.requestURI.__len__() > 0)
            startLine.rawString = "BYE sip:1115252@127.0.0.1:5060 SIP/2.0"
            self.assertEqual("BYE", startLine.sipMethod)
            self.assertEqual("sip:1115252@127.0.0.1:5060", startLine.requestURI)
            self.assertEqual("BYE sip:1115252@127.0.0.1:5060 SIP/2.0", startLine.rawString)
        self.assertEqual('INVITE', SIPRequestStartLine.newParsedFrom(self.canonicalStrings[0]).sipMethod)
        self.assertEqual('sip:5551212@127.0.0.1:5060', SIPRequestStartLine.newParsedFrom(self.canonicalStrings[0]).requestURI)
        self.assertEqual('INVITE', SIPRequestStartLine.newParsedFrom(self.canonicalStrings[1]).sipMethod)
        self.assertEqual('sip:5551212@127.0.0.1:5060;transport=udp;user=phone;trusted;gw', SIPRequestStartLine.newParsedFrom(self.canonicalStrings[1]).requestURI)

    def test_rendering(self):
        startLine = SIPRequestStartLine.newForAttributes(sipMethod="INVITE", requestURI="sip:5551212@127.0.0.1:5060")
        self.assertEqual("INVITE", startLine.sipMethod)
        self.assertEqual("sip:5551212@127.0.0.1:5060", startLine.requestURI)
        self.assertEqual("INVITE sip:5551212@127.0.0.1:5060 SIP/2.0", startLine.rawString)
        startLine.sipMethod = "BYE"
        startLine.requestURI = "sip:1115252@127.0.0.1:5060"
        self.assertEqual("BYE", startLine.sipMethod)
        self.assertEqual("sip:1115252@127.0.0.1:5060", startLine.requestURI)
        self.assertEqual("BYE sip:1115252@127.0.0.1:5060 SIP/2.0", startLine.rawString)
