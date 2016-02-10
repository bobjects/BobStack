from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging import UnknownSIPHeaderField
from sipmessaging import ContentLengthSIPHeaderField


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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line))
            self.assertFalse(ContentLengthSIPHeaderField.canMatchString(line))
            headerField = UnknownSIPHeaderField.newParsedFrom(line)
            if line.split().__len__() < 2:
                self.assertFalse(headerField.isValid)
            else:
                if ":" not in line:
                    self.assertFalse(headerField.isValid)
                else:
                    self.assertTrue(headerField.isValid)
            self.assertFalse(headerField.isContentLength)
            self.assertFalse(headerField.isKnown)
            self.assertEqual(headerField.rawString, line)
            self.assertIsInstance(headerField.fieldName, basestring)
            self.assertIsInstance(headerField.fieldValue, basestring)


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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(ContentLengthSIPHeaderField.canMatchString(line), line)
            headerField = ContentLengthSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContentLength, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.value, (int, long), line)
            self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Content-Length".lower())
            self.assertEqual(headerField.fieldValue, "489")
            headerField.rawString = 'Content-Length: 301'
            self.assertEqual(301, headerField.value)
            self.assertEqual(headerField.fieldName.lower(), "Content-Length".lower())
            self.assertEqual(headerField.fieldValue, "301")
            self.assertEqual('Content-Length: 301', headerField.rawString)
        for line in self.canonicalStrings:
            self.assertEqual(ContentLengthSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = ContentLengthSIPHeaderField.newForAttributes(value=300)
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isContentLength)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Content-Length: 300')
        self.assertIsInstance(headerField.value, (int, long))
        self.assertEqual(headerField.value, 300)
        headerField.value = 301
        self.assertEqual(301, headerField.value)
        self.assertEqual('Content-Length: 301', headerField.rawString)
