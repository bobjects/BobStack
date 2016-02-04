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

    def test_parsing(self):
        for line in self.canonicalStrings:
            self.assertFalse(UnknownSIPHeaderField.canParseString(line))
            self.assertFalse(ContentLengthSIPHeaderField.canParseString(line))
            headerField = UnknownSIPHeaderField(stringToParse=line)
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

    def test_parsing(self):
        for line in self.canonicalStrings:
            self.assertFalse(UnknownSIPHeaderField.canParseString(line), line)
            self.assertTrue(ContentLengthSIPHeaderField.canParseString(line), line)
            headerField = ContentLengthSIPHeaderField(stringToParse=line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContentLength, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.value, (int, long), line)
            # TODO:  Right now, these objects are immutable.  Do we want to make them have setters for the rawString?  If so, uncomment:
            # headerField.rawString = 'Content-Length: 301'
            # self.assertEqual(301, headerField.value)
            # self.assertEqual('Content-Length: 301', headerField.rawString)
        for line in self.canonicalStrings:
            self.assertEqual(ContentLengthSIPHeaderField(stringToParse=line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = ContentLengthSIPHeaderField(value=300)
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isContentLength)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Content-Length: 300')
        self.assertIsInstance(headerField.value, (int, long))
        self.assertEqual(headerField.value, 300)
        # TODO:  Right now, these objects are immutable.  Do we want to make them have setters for the attributes?  If so, uncomment:
        # headerField.value = 301
        # self.assertEqual(301, headerField.value)
        # self.assertEqual('Content-Length: 301', headerField.rawString)
