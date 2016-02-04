try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging.sipHeaderFieldFactory import SIPHeaderFieldFactory


class TestSIPHeaderFieldFactoryForUnknown(TestCase):
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
            headerField = SIPHeaderFieldFactory().nextForString(line)
            # TODO:  A couple of those canonical strings should not be considered valid.
            # I.e. this assertTrue should break.  Work on that.
            self.assertTrue(headerField.isValid)
            self.assertFalse(headerField.isContentLength)
            self.assertFalse(headerField.isKnown)
            self.assertEqual(headerField.rawString, line)
            if line:
                stringio = StringIO(line + '\r\n')
                headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
                # TODO:  A couple of those canonical strings should not be considered valid.
                # I.e. this assertTrue should break.  Work on that.
                self.assertTrue(headerField.isValid)
                self.assertFalse(headerField.isContentLength)
                self.assertFalse(headerField.isKnown)
                self.assertEqual(headerField.rawString, line)
                stringio.close()


class TestSIPHeaderFieldFactoryForContentLength(TestCase):
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
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContentLength, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.value, (int, long), line)
            self.assertEqual(headerField.value, 489, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            # TODO:  A couple of those canonical strings should not be considered valid.
            # I.e. this assertTrue should break.  Work on that.
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContentLength, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.value, (int, long), line)
            self.assertEqual(headerField.value, 489, line)
            stringio.close()

