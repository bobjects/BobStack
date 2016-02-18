try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging import SIPHeaderFieldFactory

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
            if line:
                stringio = StringIO(line + '\r\n')
                headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
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
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContentLength, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.value, (int, long), line)
            self.assertEqual(headerField.value, 489, line)
            stringio.close()

class TestSIPHeaderFieldFactoryForAccept(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Accept: baz blarg blonk',
            'accept: baz blarg blonk',
            'ACCEPT: baz blarg blonk',
            'Accept:      baz blarg blonk',
            'accept:      baz blarg blonk',
            'ACCEPT:      baz blarg blonk',
            'Accept     : baz blarg blonk',
            'accept     : baz blarg blonk',
            'ACCEPT     : baz blarg blonk',
            'Accept     :      baz blarg blonk',
            'accept     :      baz blarg blonk',
            'ACCEPT     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAccept, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAccept, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Accept")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAccept, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Accept: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Accept", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAccept, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Accept: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForAcceptEncoding(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Accept-Encoding: baz blarg blonk',
            'accept-encoding: baz blarg blonk',
            'ACCEPT-ENCODING: baz blarg blonk',
            'Accept-Encoding:      baz blarg blonk',
            'accept-encoding:      baz blarg blonk',
            'ACCEPT-ENCODING:      baz blarg blonk',
            'Accept-Encoding     : baz blarg blonk',
            'accept-encoding     : baz blarg blonk',
            'ACCEPT-ENCODING     : baz blarg blonk',
            'Accept-Encoding     :      baz blarg blonk',
            'accept-encoding     :      baz blarg blonk',
            'ACCEPT-ENCODING     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAcceptEncoding, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAcceptEncoding, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Accept-Encoding")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAcceptEncoding, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Accept-Encoding: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Accept-Encoding", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAcceptEncoding, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Accept-Encoding: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForAcceptLanguage(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Accept-Language: baz blarg blonk',
            'accept-language: baz blarg blonk',
            'ACCEPT-LANGUAGE: baz blarg blonk',
            'Accept-Language:      baz blarg blonk',
            'accept-language:      baz blarg blonk',
            'ACCEPT-LANGUAGE:      baz blarg blonk',
            'Accept-Language     : baz blarg blonk',
            'accept-language     : baz blarg blonk',
            'ACCEPT-LANGUAGE     : baz blarg blonk',
            'Accept-Language     :      baz blarg blonk',
            'accept-language     :      baz blarg blonk',
            'ACCEPT-LANGUAGE     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAcceptLanguage, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAcceptLanguage, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Accept-Language")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAcceptLanguage, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Accept-Language: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Accept-Language", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAcceptLanguage, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Accept-Language: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForAllow(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Allow: baz blarg blonk',
            'allow: baz blarg blonk',
            'ALLOW: baz blarg blonk',
            'Allow:      baz blarg blonk',
            'allow:      baz blarg blonk',
            'ALLOW:      baz blarg blonk',
            'Allow     : baz blarg blonk',
            'allow     : baz blarg blonk',
            'ALLOW     : baz blarg blonk',
            'Allow     :      baz blarg blonk',
            'allow     :      baz blarg blonk',
            'ALLOW     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAllow, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAllow, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Allow")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAllow, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Allow: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Allow", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAllow, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Allow: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForAuthorization(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Authorization: baz blarg blonk',
            'authorization: baz blarg blonk',
            'AUTHORIZATION: baz blarg blonk',
            'Authorization:      baz blarg blonk',
            'authorization:      baz blarg blonk',
            'AUTHORIZATION:      baz blarg blonk',
            'Authorization     : baz blarg blonk',
            'authorization     : baz blarg blonk',
            'AUTHORIZATION     : baz blarg blonk',
            'Authorization     :      baz blarg blonk',
            'authorization     :      baz blarg blonk',
            'AUTHORIZATION     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAuthorization, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAuthorization, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Authorization")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAuthorization, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Authorization: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Authorization", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAuthorization, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Authorization: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForCSeq(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'CSeq: baz blarg blonk',
            'cseq: baz blarg blonk',
            'CSEQ: baz blarg blonk',
            'CSeq:      baz blarg blonk',
            'cseq:      baz blarg blonk',
            'CSEQ:      baz blarg blonk',
            'CSeq     : baz blarg blonk',
            'cseq     : baz blarg blonk',
            'CSEQ     : baz blarg blonk',
            'CSeq     :      baz blarg blonk',
            'cseq     :      baz blarg blonk',
            'CSEQ     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isCSeq, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isCSeq, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("CSeq")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isCSeq, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "CSeq: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("CSeq", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isCSeq, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "CSeq: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForCallID(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Call-ID: baz blarg blonk',
            'call-id: baz blarg blonk',
            'CALL-ID: baz blarg blonk',
            'Call-ID:      baz blarg blonk',
            'call-id:      baz blarg blonk',
            'CALL-ID:      baz blarg blonk',
            'Call-ID     : baz blarg blonk',
            'call-id     : baz blarg blonk',
            'CALL-ID     : baz blarg blonk',
            'Call-ID     :      baz blarg blonk',
            'call-id     :      baz blarg blonk',
            'CALL-ID     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isCallID, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isCallID, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Call-ID")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isCallID, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Call-ID: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Call-ID", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isCallID, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Call-ID: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForCallInfo(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Call-Info: baz blarg blonk',
            'call-info: baz blarg blonk',
            'CALL-INFO: baz blarg blonk',
            'Call-Info:      baz blarg blonk',
            'call-info:      baz blarg blonk',
            'CALL-INFO:      baz blarg blonk',
            'Call-Info     : baz blarg blonk',
            'call-info     : baz blarg blonk',
            'CALL-INFO     : baz blarg blonk',
            'Call-Info     :      baz blarg blonk',
            'call-info     :      baz blarg blonk',
            'CALL-INFO     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isCallInfo, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isCallInfo, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Call-Info")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isCallInfo, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Call-Info: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Call-Info", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isCallInfo, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Call-Info: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForContact(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Contact: baz blarg blonk',
            'contact: baz blarg blonk',
            'CONTACT: baz blarg blonk',
            'Contact:      baz blarg blonk',
            'contact:      baz blarg blonk',
            'CONTACT:      baz blarg blonk',
            'Contact     : baz blarg blonk',
            'contact     : baz blarg blonk',
            'CONTACT     : baz blarg blonk',
            'Contact     :      baz blarg blonk',
            'contact     :      baz blarg blonk',
            'CONTACT     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContact, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContact, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Contact")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContact, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Contact: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Contact", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContact, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Contact: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForContentDisposition(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Content-Disposition: baz blarg blonk',
            'content-disposition: baz blarg blonk',
            'CONTENT-DISPOSITION: baz blarg blonk',
            'Content-Disposition:      baz blarg blonk',
            'content-disposition:      baz blarg blonk',
            'CONTENT-DISPOSITION:      baz blarg blonk',
            'Content-Disposition     : baz blarg blonk',
            'content-disposition     : baz blarg blonk',
            'CONTENT-DISPOSITION     : baz blarg blonk',
            'Content-Disposition     :      baz blarg blonk',
            'content-disposition     :      baz blarg blonk',
            'CONTENT-DISPOSITION     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContentDisposition, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContentDisposition, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Content-Disposition")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContentDisposition, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Content-Disposition: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Content-Disposition", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContentDisposition, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Content-Disposition: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForContentType(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Content-Type: baz blarg blonk',
            'content-type: baz blarg blonk',
            'CONTENT-TYPE: baz blarg blonk',
            'Content-Type:      baz blarg blonk',
            'content-type:      baz blarg blonk',
            'CONTENT-TYPE:      baz blarg blonk',
            'Content-Type     : baz blarg blonk',
            'content-type     : baz blarg blonk',
            'CONTENT-TYPE     : baz blarg blonk',
            'Content-Type     :      baz blarg blonk',
            'content-type     :      baz blarg blonk',
            'CONTENT-TYPE     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContentType, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContentType, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Content-Type")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContentType, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Content-Type: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Content-Type", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContentType, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Content-Type: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForDate(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Date: baz blarg blonk',
            'date: baz blarg blonk',
            'DATE: baz blarg blonk',
            'Date:      baz blarg blonk',
            'date:      baz blarg blonk',
            'DATE:      baz blarg blonk',
            'Date     : baz blarg blonk',
            'date     : baz blarg blonk',
            'DATE     : baz blarg blonk',
            'Date     :      baz blarg blonk',
            'date     :      baz blarg blonk',
            'DATE     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isDate, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isDate, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Date")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isDate, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Date: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Date", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isDate, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Date: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForExpires(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Expires: baz blarg blonk',
            'expires: baz blarg blonk',
            'EXPIRES: baz blarg blonk',
            'Expires:      baz blarg blonk',
            'expires:      baz blarg blonk',
            'EXPIRES:      baz blarg blonk',
            'Expires     : baz blarg blonk',
            'expires     : baz blarg blonk',
            'EXPIRES     : baz blarg blonk',
            'Expires     :      baz blarg blonk',
            'expires     :      baz blarg blonk',
            'EXPIRES     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isExpires, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isExpires, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Expires")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isExpires, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Expires: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Expires", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isExpires, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Expires: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForFrom(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'From: baz blarg blonk',
            'from: baz blarg blonk',
            'FROM: baz blarg blonk',
            'From:      baz blarg blonk',
            'from:      baz blarg blonk',
            'FROM:      baz blarg blonk',
            'From     : baz blarg blonk',
            'from     : baz blarg blonk',
            'FROM     : baz blarg blonk',
            'From     :      baz blarg blonk',
            'from     :      baz blarg blonk',
            'FROM     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isFrom, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isFrom, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("From")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isFrom, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "From: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("From", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isFrom, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "From: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForMaxForwards(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Max-Forwards: 70',
            'max-forwards: 70',
            'MAX-FORWARDS: 70',
            'Max-Forwards:      70',
            'max-forwards:      70',
            'MAX-FORWARDS:      70',
            'Max-Forwards     : 70',
            'max-forwards     : 70',
            'MAX-FORWARDS     : 70',
            'Max-Forwards     :      70',
            'max-forwards     :      70',
            'MAX-FORWARDS     :      70',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isMaxForwards, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.value, 70, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isMaxForwards, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertIsInstance(headerField.value, (int, long), line)
            self.assertEqual(headerField.value, 70)
            self.assertEqual(headerField.fieldValue, "70", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Max-Forwards")
            self.assertEqual(headerField.fieldValue, "0", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "70"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isMaxForwards, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Max-Forwards: 70")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "70", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Max-Forwards", "0")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "70"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isMaxForwards, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Max-Forwards: 70")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "70", line)
class TestSIPHeaderFieldFactoryForRecordRoute(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Record-Route: baz blarg blonk',
            'record-route: baz blarg blonk',
            'RECORD-ROUTE: baz blarg blonk',
            'Record-Route:      baz blarg blonk',
            'record-route:      baz blarg blonk',
            'RECORD-ROUTE:      baz blarg blonk',
            'Record-Route     : baz blarg blonk',
            'record-route     : baz blarg blonk',
            'RECORD-ROUTE     : baz blarg blonk',
            'Record-Route     :      baz blarg blonk',
            'record-route     :      baz blarg blonk',
            'RECORD-ROUTE     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRecordRoute, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRecordRoute, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Record-Route")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRecordRoute, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Record-Route: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Record-Route", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRecordRoute, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Record-Route: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForRequire(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Require: baz blarg blonk',
            'require: baz blarg blonk',
            'REQUIRE: baz blarg blonk',
            'Require:      baz blarg blonk',
            'require:      baz blarg blonk',
            'REQUIRE:      baz blarg blonk',
            'Require     : baz blarg blonk',
            'require     : baz blarg blonk',
            'REQUIRE     : baz blarg blonk',
            'Require     :      baz blarg blonk',
            'require     :      baz blarg blonk',
            'REQUIRE     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRequire, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRequire, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Require")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRequire, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Require: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Require", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRequire, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Require: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForRetryAfter(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Retry-After: baz blarg blonk',
            'retry-after: baz blarg blonk',
            'RETRY-AFTER: baz blarg blonk',
            'Retry-After:      baz blarg blonk',
            'retry-after:      baz blarg blonk',
            'RETRY-AFTER:      baz blarg blonk',
            'Retry-After     : baz blarg blonk',
            'retry-after     : baz blarg blonk',
            'RETRY-AFTER     : baz blarg blonk',
            'Retry-After     :      baz blarg blonk',
            'retry-after     :      baz blarg blonk',
            'RETRY-AFTER     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRetryAfter, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRetryAfter, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Retry-After")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRetryAfter, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Retry-After: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Retry-After", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRetryAfter, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Retry-After: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForRoute(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Route: baz blarg blonk',
            'route: baz blarg blonk',
            'ROUTE: baz blarg blonk',
            'Route:      baz blarg blonk',
            'route:      baz blarg blonk',
            'ROUTE:      baz blarg blonk',
            'Route     : baz blarg blonk',
            'route     : baz blarg blonk',
            'ROUTE     : baz blarg blonk',
            'Route     :      baz blarg blonk',
            'route     :      baz blarg blonk',
            'ROUTE     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRoute, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRoute, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Route")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRoute, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Route: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Route", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRoute, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Route: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForServer(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Server: baz blarg blonk',
            'server: baz blarg blonk',
            'SERVER: baz blarg blonk',
            'Server:      baz blarg blonk',
            'server:      baz blarg blonk',
            'SERVER:      baz blarg blonk',
            'Server     : baz blarg blonk',
            'server     : baz blarg blonk',
            'SERVER     : baz blarg blonk',
            'Server     :      baz blarg blonk',
            'server     :      baz blarg blonk',
            'SERVER     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isServer, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isServer, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Server")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isServer, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Server: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Server", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isServer, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Server: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForSessionExpires(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Session-Expires: baz blarg blonk',
            'session-expires: baz blarg blonk',
            'SESSION-EXPIRES: baz blarg blonk',
            'Session-Expires:      baz blarg blonk',
            'session-expires:      baz blarg blonk',
            'SESSION-EXPIRES:      baz blarg blonk',
            'Session-Expires     : baz blarg blonk',
            'session-expires     : baz blarg blonk',
            'SESSION-EXPIRES     : baz blarg blonk',
            'Session-Expires     :      baz blarg blonk',
            'session-expires     :      baz blarg blonk',
            'SESSION-EXPIRES     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isSessionExpires, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isSessionExpires, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Session-Expires")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isSessionExpires, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Session-Expires: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Session-Expires", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isSessionExpires, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Session-Expires: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForSupported(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Supported: baz blarg blonk',
            'supported: baz blarg blonk',
            'SUPPORTED: baz blarg blonk',
            'Supported:      baz blarg blonk',
            'supported:      baz blarg blonk',
            'SUPPORTED:      baz blarg blonk',
            'Supported     : baz blarg blonk',
            'supported     : baz blarg blonk',
            'SUPPORTED     : baz blarg blonk',
            'Supported     :      baz blarg blonk',
            'supported     :      baz blarg blonk',
            'SUPPORTED     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isSupported, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isSupported, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Supported")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isSupported, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Supported: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Supported", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isSupported, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Supported: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForTimestamp(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Timestamp: baz blarg blonk',
            'timestamp: baz blarg blonk',
            'TIMESTAMP: baz blarg blonk',
            'Timestamp:      baz blarg blonk',
            'timestamp:      baz blarg blonk',
            'TIMESTAMP:      baz blarg blonk',
            'Timestamp     : baz blarg blonk',
            'timestamp     : baz blarg blonk',
            'TIMESTAMP     : baz blarg blonk',
            'Timestamp     :      baz blarg blonk',
            'timestamp     :      baz blarg blonk',
            'TIMESTAMP     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isTimestamp, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isTimestamp, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Timestamp")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isTimestamp, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Timestamp: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Timestamp", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isTimestamp, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Timestamp: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForTo(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'To: baz blarg blonk',
            'to: baz blarg blonk',
            'TO: baz blarg blonk',
            'To:      baz blarg blonk',
            'to:      baz blarg blonk',
            'TO:      baz blarg blonk',
            'To     : baz blarg blonk',
            'to     : baz blarg blonk',
            'TO     : baz blarg blonk',
            'To     :      baz blarg blonk',
            'to     :      baz blarg blonk',
            'TO     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isTo, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isTo, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("To")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isTo, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "To: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("To", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isTo, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "To: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForUserAgent(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'User-Agent: baz blarg blonk',
            'user-agent: baz blarg blonk',
            'USER-AGENT: baz blarg blonk',
            'User-Agent:      baz blarg blonk',
            'user-agent:      baz blarg blonk',
            'USER-AGENT:      baz blarg blonk',
            'User-Agent     : baz blarg blonk',
            'user-agent     : baz blarg blonk',
            'USER-AGENT     : baz blarg blonk',
            'User-Agent     :      baz blarg blonk',
            'user-agent     :      baz blarg blonk',
            'USER-AGENT     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isUserAgent, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isUserAgent, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("User-Agent")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isUserAgent, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "User-Agent: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("User-Agent", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isUserAgent, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "User-Agent: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForWWWAuthenticate(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'WWW-Authenticate: baz blarg blonk',
            'www-authenticate: baz blarg blonk',
            'WWW-AUTHENTICATE: baz blarg blonk',
            'WWW-Authenticate:      baz blarg blonk',
            'www-authenticate:      baz blarg blonk',
            'WWW-AUTHENTICATE:      baz blarg blonk',
            'WWW-Authenticate     : baz blarg blonk',
            'www-authenticate     : baz blarg blonk',
            'WWW-AUTHENTICATE     : baz blarg blonk',
            'WWW-Authenticate     :      baz blarg blonk',
            'www-authenticate     :      baz blarg blonk',
            'WWW-AUTHENTICATE     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isWWWAuthenticate, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isWWWAuthenticate, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("WWW-Authenticate")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isWWWAuthenticate, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "WWW-Authenticate: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("WWW-Authenticate", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isWWWAuthenticate, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "WWW-Authenticate: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
class TestSIPHeaderFieldFactoryForWarning(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Warning: baz blarg blonk',
            'warning: baz blarg blonk',
            'WARNING: baz blarg blonk',
            'Warning:      baz blarg blonk',
            'warning:      baz blarg blonk',
            'WARNING:      baz blarg blonk',
            'Warning     : baz blarg blonk',
            'warning     : baz blarg blonk',
            'WARNING     : baz blarg blonk',
            'Warning     :      baz blarg blonk',
            'warning     :      baz blarg blonk',
            'WARNING     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isWarning, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isWarning, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName("Warning")
            self.assertEqual(headerField.fieldValue, "", line)
            # Hmm, really?  An empty but non-None fieldValue is valid?
            # self.assertFalse(headerField.isValid, line)
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isWarning, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Warning: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue("Warning", "foo bar baz blarg")
            self.assertTrue(headerField.isValid, line)
            headerField.fieldValue = "baz blarg blonk"
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isWarning, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, "Warning: baz blarg blonk")
            self.assertIsInstance(headerField.fieldValue, basestring)
            self.assertEqual(headerField.fieldValue, "baz blarg blonk", line)
