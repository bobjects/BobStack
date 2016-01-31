from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging.sipRequestStartLine import SIPRequestStartLine
from sipmessaging.sipResponseStartLine import SIPResponseStartLine
from sipmessaging.malformedSIPStartLine import MalformedSIPStartLine


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
            self.assertFalse(SIPRequestStartLine.canParseString(line))
            self.assertFalse(SIPResponseStartLine.canParseString(line))
            startLine = MalformedSIPStartLine(line)
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
            self.assertFalse(SIPRequestStartLine.canParseString(line))
            self.assertTrue(SIPResponseStartLine.canParseString(line))
            startLine = SIPResponseStartLine(stringToParse=line)
            self.assertFalse(startLine.isRequest)
            self.assertTrue(startLine.isResponse)
            self.assertFalse(startLine.isMalformed)
            self.assertEqual(startLine.rawString, line)
            self.assertIsInstance(startLine.statusCode, (int, long))
            self.assertIsInstance(startLine.reasonPhrase, basestring)
            # TODO:  Right now, these objects are immutable.  Do we want to make them have setters for the attributes?  If so, uncomment:
            # startLine.rawString = "SIP/2.0 200 OK"
            # self.assertEqual(200, startLine.statusCode)
            # self.assertEqual("OK", startLine.reasonPhrase)
            # self.assertEqual("SIP/2.0 200 OK", startLine.rawString)
        self.assertEqual(100, SIPResponseStartLine(stringToParse=self.canonicalStrings[0]).statusCode)
        self.assertEqual('Trying', SIPResponseStartLine(stringToParse=self.canonicalStrings[0]).reasonPhrase)
        self.assertEqual(100, SIPResponseStartLine(stringToParse=self.canonicalStrings[1]).statusCode)
        self.assertEqual('Trying and trying and trying', SIPResponseStartLine(stringToParse=self.canonicalStrings[1]).reasonPhrase)

    def test_rendering(self):
        startLine = SIPResponseStartLine(statusCode=401, reasonPhrase="Not Authorized")
        self.assertEqual(401, startLine.statusCode)
        self.assertEqual("Not Authorized", startLine.reasonPhrase)
        self.assertEqual("SIP/2.0 401 Not Authorized", startLine.rawString)
        # TODO:  Right now, these objects are immutable.  Do we want to make them have setters for the attributes?  If so, uncomment:
        # startLine.statusCode = 200
        # startLine.reasonPhrase = "OK"
        # self.assertEqual(200, startLine.statusCode)
        # self.assertEqual("OK", startLine.reasonPhrase)
        # self.assertEqual("SIP/2.0 200 OK", startLine.rawString)


class TestSIPRequestStartLine(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'INVITE sip:5551212@127.0.0.1:5060 SIP/2.0',
            'INVITE sip:5551212@127.0.0.1:5060;transport=udp;user=phone;trusted;gw SIP/2.0']

    def test_parsing(self):
        for line in self.canonicalStrings:
            self.assertTrue(SIPRequestStartLine.canParseString(line))
            self.assertFalse(SIPResponseStartLine.canParseString(line))
            startLine = SIPRequestStartLine(stringToParse=line)
            self.assertTrue(startLine.isRequest)
            self.assertFalse(startLine.isResponse)
            self.assertFalse(startLine.isMalformed)
            self.assertEqual(startLine.rawString, line)
            self.assertIsInstance(startLine.sipMethod, basestring)
            self.assertTrue(startLine.sipMethod.__len__() > 0)
            self.assertIsInstance(startLine.requestURI, basestring)
            self.assertTrue(startLine.requestURI.__len__() > 0)
            # TODO:  Right now, these objects are immutable.  Do we want to make them have a setter for the rawString?  If so, uncomment:
            # startLine.rawString = "BYE sip:1115252@127.0.0.1:5060 SIP/2.0"
            # self.assertEqual("BYE", startLine.sipMethod)
            # self.assertEqual("sip:1115252@127.0.0.1:5060", startLine.requestURI)
            # self.assertEqual("BYE sip:1115252@127.0.0.1:5060 SIP/2.0", startLine.rawString)
        self.assertEqual('INVITE', SIPRequestStartLine(stringToParse=self.canonicalStrings[0]).sipMethod)
        self.assertEqual('sip:5551212@127.0.0.1:5060', SIPRequestStartLine(stringToParse=self.canonicalStrings[0]).requestURI)
        self.assertEqual('INVITE', SIPRequestStartLine(stringToParse=self.canonicalStrings[1]).sipMethod)
        self.assertEqual('sip:5551212@127.0.0.1:5060;transport=udp;user=phone;trusted;gw', SIPRequestStartLine(stringToParse=self.canonicalStrings[1]).requestURI)

    def test_rendering(self):
        startLine = SIPRequestStartLine(sipMethod="INVITE", requestURI="sip:5551212@127.0.0.1:5060")
        self.assertEqual("INVITE", startLine.sipMethod)
        self.assertEqual("sip:5551212@127.0.0.1:5060", startLine.requestURI)
        self.assertEqual("INVITE sip:5551212@127.0.0.1:5060 SIP/2.0", startLine.rawString)
        # TODO:  Right now, these objects are immutable.  Do we want to make them have setters for the attributes?  If so, uncomment:
        # startLine.sipMethod = "BYE"
        # startLine.requestURI = "sip:1115252@127.0.0.1:5060"
        # self.assertEqual("BYE", startLine.sipMethod)
        # self.assertEqual("sip:1115252@127.0.0.1:5060", startLine.requestURI)
        # self.assertEqual("BYE sip:1115252@127.0.0.1:5060 SIP/2.0", startLine.rawString)
