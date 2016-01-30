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

    def test_01_wellFormed(self):
        for line in self.canonicalStrings:
            self.assertFalse(SIPRequestStartLine.matchesLine(line))
            self.assertFalse(SIPResponseStartLine.matchesLine(line))
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

    def test_01_wellFormed(self):
        for line in self.canonicalStrings:
            self.assertFalse(SIPRequestStartLine.matchesLine(line))
            self.assertTrue(SIPResponseStartLine.matchesLine(line))
            startLine = SIPResponseStartLine(line)
            self.assertFalse(startLine.isRequest)
            self.assertTrue(startLine.isResponse)
            self.assertFalse(startLine.isMalformed)
            self.assertEqual(startLine.rawString, line)
            self.assertIsInstance(startLine.statusCode, (int, long))
            self.assertIsInstance(startLine.reasonPhrase, basestring)

    def test_02_correctParsing(self):
        self.assertEqual(100, SIPResponseStartLine(self.canonicalStrings[0]).statusCode)
        self.assertEqual('Trying', SIPResponseStartLine(self.canonicalStrings[0]).reasonPhrase)
        self.assertEqual(100, SIPResponseStartLine(self.canonicalStrings[1]).statusCode)
        self.assertEqual('Trying and trying and trying', SIPResponseStartLine(self.canonicalStrings[1]).reasonPhrase)


class TestSIPRequestStartLine(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'INVITE sip:5551212@127.0.0.1:5060 SIP/2.0',
            'INVITE sip:5551212@127.0.0.1:5060;transport=udp;user=phone;trusted;gw SIP/2.0']

    def test_01_wellFormed(self):
        for line in self.canonicalStrings:
            self.assertTrue(SIPRequestStartLine.matchesLine(line))
            self.assertFalse(SIPResponseStartLine.matchesLine(line))
            startLine = SIPRequestStartLine(line)
            self.assertTrue(startLine.isRequest)
            self.assertFalse(startLine.isResponse)
            self.assertFalse(startLine.isMalformed)
            self.assertEqual(startLine.rawString, line)
            self.assertIsInstance(startLine.sipMethod, basestring)
            self.assertTrue(startLine.sipMethod.__len__() > 0)
            self.assertIsInstance(startLine.requestURI, basestring)
            self.assertTrue(startLine.requestURI.__len__() > 0)

    def test_02_correctParsing(self):
        self.assertEqual('INVITE', SIPRequestStartLine(self.canonicalStrings[0]).sipMethod)
        self.assertEqual('sip:5551212@127.0.0.1:5060', SIPRequestStartLine(self.canonicalStrings[0]).requestURI)
        self.assertEqual('INVITE', SIPRequestStartLine(self.canonicalStrings[1]).sipMethod)
        self.assertEqual('sip:5551212@127.0.0.1:5060;transport=udp;user=phone;trusted;gw', SIPRequestStartLine(self.canonicalStrings[1]).requestURI)
