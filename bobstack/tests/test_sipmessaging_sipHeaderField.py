from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging import UnknownSIPHeaderField
from sipmessaging import ContentLengthSIPHeaderField
from sipmessaging import AcceptSIPHeaderField
from sipmessaging import AcceptEncodingSIPHeaderField
from sipmessaging import AcceptLanguageSIPHeaderField
from sipmessaging import AllowSIPHeaderField
from sipmessaging import AuthorizationSIPHeaderField
from sipmessaging import CSeqSIPHeaderField
from sipmessaging import CallIDSIPHeaderField
from sipmessaging import CallInfoSIPHeaderField
from sipmessaging import ContactSIPHeaderField
from sipmessaging import ContentDispositionSIPHeaderField
from sipmessaging import ContentTypeSIPHeaderField
from sipmessaging import DateSIPHeaderField
from sipmessaging import ExpiresSIPHeaderField
from sipmessaging import FromSIPHeaderField
from sipmessaging import MaxForwardsSIPHeaderField
from sipmessaging import RecordRouteSIPHeaderField
from sipmessaging import RequireSIPHeaderField
from sipmessaging import RetryAfterSIPHeaderField
from sipmessaging import RouteSIPHeaderField
from sipmessaging import ServerSIPHeaderField
from sipmessaging import SessionExpiresSIPHeaderField
from sipmessaging import SupportedSIPHeaderField
from sipmessaging import TimestampSIPHeaderField
from sipmessaging import ToSIPHeaderField
from sipmessaging import UserAgentSIPHeaderField
from sipmessaging import ViaSIPHeaderField
from sipmessaging import WWWAuthenticateSIPHeaderField
from sipmessaging import WarningSIPHeaderField

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


class TestAcceptSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(AcceptSIPHeaderField.canMatchString(line), line)
            headerField = AcceptSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAccept, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Accept".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Accept: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Accept".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Accept: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(AcceptSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = AcceptSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isAccept)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Accept: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Accept: blooey', headerField.rawString)

class TestAcceptEncodingSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(AcceptEncodingSIPHeaderField.canMatchString(line), line)
            headerField = AcceptEncodingSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAcceptEncoding, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Accept-Encoding".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Accept-Encoding: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Accept-Encoding".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Accept-Encoding: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(AcceptEncodingSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = AcceptEncodingSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isAcceptEncoding)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Accept-Encoding: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Accept-Encoding: blooey', headerField.rawString)

class TestAcceptLanguageSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(AcceptLanguageSIPHeaderField.canMatchString(line), line)
            headerField = AcceptLanguageSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAcceptLanguage, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Accept-Language".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Accept-Language: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Accept-Language".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Accept-Language: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(AcceptLanguageSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = AcceptLanguageSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isAcceptLanguage)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Accept-Language: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Accept-Language: blooey', headerField.rawString)

class TestAllowSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(AllowSIPHeaderField.canMatchString(line), line)
            headerField = AllowSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAllow, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Allow".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Allow: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Allow".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Allow: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(AllowSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = AllowSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isAllow)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Allow: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Allow: blooey', headerField.rawString)

class TestAuthorizationSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(AuthorizationSIPHeaderField.canMatchString(line), line)
            headerField = AuthorizationSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isAuthorization, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Authorization".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Authorization: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Authorization".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Authorization: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(AuthorizationSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = AuthorizationSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isAuthorization)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Authorization: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Authorization: blooey', headerField.rawString)

class TestCSeqSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(CSeqSIPHeaderField.canMatchString(line), line)
            headerField = CSeqSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isCSeq, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "CSeq".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'CSeq: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "CSeq".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('CSeq: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(CSeqSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = CSeqSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isCSeq)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'CSeq: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('CSeq: blooey', headerField.rawString)

class TestCallIDSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(CallIDSIPHeaderField.canMatchString(line), line)
            headerField = CallIDSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isCallID, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Call-ID".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Call-ID: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Call-ID".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Call-ID: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(CallIDSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = CallIDSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isCallID)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Call-ID: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Call-ID: blooey', headerField.rawString)

class TestCallInfoSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(CallInfoSIPHeaderField.canMatchString(line), line)
            headerField = CallInfoSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isCallInfo, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Call-Info".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Call-Info: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Call-Info".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Call-Info: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(CallInfoSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = CallInfoSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isCallInfo)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Call-Info: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Call-Info: blooey', headerField.rawString)

class TestContactSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(ContactSIPHeaderField.canMatchString(line), line)
            headerField = ContactSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContact, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Contact".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Contact: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Contact".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Contact: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(ContactSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = ContactSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isContact)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Contact: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Contact: blooey', headerField.rawString)

class TestContentDispositionSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(ContentDispositionSIPHeaderField.canMatchString(line), line)
            headerField = ContentDispositionSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContentDisposition, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Content-Disposition".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Content-Disposition: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Content-Disposition".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Content-Disposition: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(ContentDispositionSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = ContentDispositionSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isContentDisposition)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Content-Disposition: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Content-Disposition: blooey', headerField.rawString)

class TestContentTypeSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(ContentTypeSIPHeaderField.canMatchString(line), line)
            headerField = ContentTypeSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isContentType, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Content-Type".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Content-Type: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Content-Type".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Content-Type: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(ContentTypeSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = ContentTypeSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isContentType)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Content-Type: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Content-Type: blooey', headerField.rawString)

class TestDateSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(DateSIPHeaderField.canMatchString(line), line)
            headerField = DateSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isDate, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Date".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Date: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Date".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Date: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(DateSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = DateSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isDate)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Date: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Date: blooey', headerField.rawString)

class TestExpiresSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(ExpiresSIPHeaderField.canMatchString(line), line)
            headerField = ExpiresSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isExpires, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Expires".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Expires: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Expires".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Expires: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(ExpiresSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = ExpiresSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isExpires)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Expires: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Expires: blooey', headerField.rawString)

class TestFromSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(FromSIPHeaderField.canMatchString(line), line)
            headerField = FromSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isFrom, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "From".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'From: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "From".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('From: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(FromSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = FromSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isFrom)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'From: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('From: blooey', headerField.rawString)

class TestMaxForwardsSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(MaxForwardsSIPHeaderField.canMatchString(line), line)
            headerField = MaxForwardsSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isMaxForwards, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Max-Forwards".lower())
            self.assertIsInstance(headerField.value, (int, long), line)
            self.assertEqual(headerField.value, 70)
            self.assertEqual(headerField.fieldValue, "70")
            headerField.rawString = 'Max-Forwards: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Max-Forwards".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Max-Forwards: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(MaxForwardsSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = MaxForwardsSIPHeaderField.newForAttributes(value=70)
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isMaxForwards)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Max-Forwards: 70')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Max-Forwards: blooey', headerField.rawString)

class TestRecordRouteSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(RecordRouteSIPHeaderField.canMatchString(line), line)
            headerField = RecordRouteSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRecordRoute, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Record-Route".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Record-Route: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Record-Route".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Record-Route: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(RecordRouteSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = RecordRouteSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isRecordRoute)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Record-Route: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Record-Route: blooey', headerField.rawString)

class TestRequireSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(RequireSIPHeaderField.canMatchString(line), line)
            headerField = RequireSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRequire, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Require".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Require: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Require".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Require: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(RequireSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = RequireSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isRequire)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Require: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Require: blooey', headerField.rawString)

class TestRetryAfterSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(RetryAfterSIPHeaderField.canMatchString(line), line)
            headerField = RetryAfterSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRetryAfter, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Retry-After".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Retry-After: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Retry-After".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Retry-After: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(RetryAfterSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = RetryAfterSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isRetryAfter)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Retry-After: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Retry-After: blooey', headerField.rawString)

class TestRouteSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(RouteSIPHeaderField.canMatchString(line), line)
            headerField = RouteSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isRoute, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Route".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Route: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Route".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Route: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(RouteSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = RouteSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isRoute)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Route: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Route: blooey', headerField.rawString)

class TestServerSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(ServerSIPHeaderField.canMatchString(line), line)
            headerField = ServerSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isServer, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Server".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Server: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Server".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Server: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(ServerSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = ServerSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isServer)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Server: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Server: blooey', headerField.rawString)

class TestSessionExpiresSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(SessionExpiresSIPHeaderField.canMatchString(line), line)
            headerField = SessionExpiresSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isSessionExpires, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Session-Expires".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Session-Expires: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Session-Expires".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Session-Expires: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(SessionExpiresSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = SessionExpiresSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isSessionExpires)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Session-Expires: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Session-Expires: blooey', headerField.rawString)

class TestSupportedSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(SupportedSIPHeaderField.canMatchString(line), line)
            headerField = SupportedSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isSupported, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Supported".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Supported: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Supported".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Supported: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(SupportedSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = SupportedSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isSupported)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Supported: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Supported: blooey', headerField.rawString)

class TestTimestampSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(TimestampSIPHeaderField.canMatchString(line), line)
            headerField = TimestampSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isTimestamp, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Timestamp".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Timestamp: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Timestamp".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Timestamp: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(TimestampSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = TimestampSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isTimestamp)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Timestamp: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Timestamp: blooey', headerField.rawString)

class TestToSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(ToSIPHeaderField.canMatchString(line), line)
            headerField = ToSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isTo, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "To".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'To: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "To".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('To: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(ToSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = ToSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isTo)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'To: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('To: blooey', headerField.rawString)

class TestUserAgentSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(UserAgentSIPHeaderField.canMatchString(line), line)
            headerField = UserAgentSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isUserAgent, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "User-Agent".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'User-Agent: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "User-Agent".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('User-Agent: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(UserAgentSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = UserAgentSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isUserAgent)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'User-Agent: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('User-Agent: blooey', headerField.rawString)

class TestWWWAuthenticateSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(WWWAuthenticateSIPHeaderField.canMatchString(line), line)
            headerField = WWWAuthenticateSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isWWWAuthenticate, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "WWW-Authenticate".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'WWW-Authenticate: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "WWW-Authenticate".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('WWW-Authenticate: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(WWWAuthenticateSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = WWWAuthenticateSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isWWWAuthenticate)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'WWW-Authenticate: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('WWW-Authenticate: blooey', headerField.rawString)

class TestWarningSipHeaderField(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(WarningSIPHeaderField.canMatchString(line), line)
            headerField = WarningSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isWarning, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Warning".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Warning: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Warning".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Warning: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(WarningSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = WarningSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isWarning)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Warning: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Warning: blooey', headerField.rawString)

class TestViaSipHeaderField(TestCase):
    @property
    def canonicalStrings(self):
        return [
            'Via: baz blarg blonk',
            'via: baz blarg blonk',
            'VIA: baz blarg blonk',
            'Via:      baz blarg blonk',
            'via:      baz blarg blonk',
            'VIA:      baz blarg blonk',
            'Via     : baz blarg blonk',
            'via     : baz blarg blonk',
            'VIA     : baz blarg blonk',
            'Via     :      baz blarg blonk',
            'via     :      baz blarg blonk',
            'VIA     :      baz blarg blonk',
        ]

    def test_parsing(self):
        for line in self.canonicalStrings:
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line), line)
            self.assertTrue(ViaSIPHeaderField.canMatchString(line), line)
            headerField = ViaSIPHeaderField.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isVia, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertIsInstance(headerField.value, (int, long), line)
            # self.assertEqual(headerField.value, 489, "Info: line is " + line)
            self.assertEqual(headerField.fieldName.lower(), "Via".lower())
            self.assertEqual(headerField.fieldValue, "baz blarg blonk")
            headerField.rawString = 'Via: blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), "Via".lower())
            self.assertEqual(headerField.fieldValue, "blooey")
            self.assertEqual('Via: blooey', headerField.rawString)
        # for line in self.canonicalStrings:
        #     self.assertEqual(ViaSIPHeaderField.newParsedFrom(line).value, 489, "Info: line is " + line)

    def test_rendering(self):
        headerField = ViaSIPHeaderField.newForAttributes(fieldValue='baz blarg blonk')
        self.assertTrue(headerField.isValid)
        self.assertTrue(headerField.isVia)
        self.assertTrue(headerField.isKnown)
        self.assertEqual(headerField.rawString, 'Via: baz blarg blonk')
        # self.assertIsInstance(headerField.value, (int, long))
        # self.assertEqual(headerField.value, 300)
        headerField.fieldValue = "blooey"
        self.assertEqual("blooey", headerField.fieldValue)
        self.assertEqual('Via: blooey', headerField.rawString)

