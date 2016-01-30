from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging.unknownSIPHeaderField import UnknownSIPHeaderField
from sipmessaging.contentLengthSIPHeaderField import ContentLengthSIPHeaderField


class TestUnknownSipHeaderField(TestCase):
    @property
    def canonicalStrings(self):
        return [
            '',
            'fajdoutawledsuloiur',
            'fdfoisfoisdjfljdsf dfdsfjsdilj dfljd',
            'UnknownHeaderField: and here is some data',
        ]

    def test_01_wellFormed(self):
        for line in self.canonicalStrings:
            self.assertFalse(UnknownSIPHeaderField.matchesLine(line))
            self.assertFalse(ContentLengthSIPHeaderField.matchesLine(line))
            headerField = UnknownSIPHeaderField(line)
            self.assertTrue(headerField.isValid)
            self.assertFalse(headerField.isContentLength)
            self.assertFalse(headerField.isKnown)
            self.assertEqual(headerField.rawString, line)


class TestContentLengthSipHeaderField(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Content-Length: 489',
            'content-length: 489',
            'CONTENT-LENGTH: 489',
            'Content-Length:      489',
            'content-length:      489',
            'CONTENT-LENGTH:      489',
            'Content-Length     : 489',
            'content-length     : 489',
            'CONTENT-LENGTH     : 489',
            'Content-Length     :      489',
            'content-length     :      489',
            'CONTENT-LENGTH     :      489',
        ]

    def test_01_wellFormed(self):
        for line in self.canonicalStrings:
            self.assertFalse(UnknownSIPHeaderField.matchesLine(line), line)
            self.assertTrue(ContentLengthSIPHeaderField.matchesLine(line), line)
            headerField = ContentLengthSIPHeaderField(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContentLength, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.value, (int, long), line)

    def test_02_correctParsing(self):
        for line in self.canonicalStrings:
            self.assertEqual(ContentLengthSIPHeaderField(line).value, 489, "Info: line is " + line)
