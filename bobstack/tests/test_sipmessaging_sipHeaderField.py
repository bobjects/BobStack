from unittest import TestCase
import sys
sys.path.append("..")
from abstractSIPHeaderFieldTestCase import AbstractSIPHeaderFieldTestCase
from abstractIntegerSIPHeaderFieldTestCase import AbstractIntegerSIPHeaderFieldTestCase
from sipmessaging import SIPURI
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
            self.assertIsInstance(headerField.fieldValueString, basestring)


class TestContentLengthSipHeaderField(AbstractIntegerSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Content-Length', 'CONTENT-Length', 'content-length', 'Content-length', 'content-Length']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ContentLengthSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isContentLength, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isContentLength)
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isContentLength)


class TestAcceptSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Accept', 'ACCEPT', 'accept']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return AcceptSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isAccept, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isAccept)
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isAccept)


class TestAcceptEncodingSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Accept-Encoding', 'ACCEPT-Encoding', 'accept-encoding', 'Accept-encoding', 'accept-Encoding']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return AcceptEncodingSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isAcceptEncoding, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isAcceptEncoding)
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isAcceptEncoding)


class TestAcceptLanguageSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Accept-Language', 'ACCEPT-Language', 'accept-language', 'Accept-language', 'accept-Language']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return AcceptLanguageSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isAcceptLanguage, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isAcceptLanguage)
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isAcceptLanguage)


class TestAllowSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Allow', 'ALLOW', 'allow']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return AllowSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isAllow, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isAllow)
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isAllow)


class TestAuthorizationSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Authorization', 'AUTHORIZATION', 'authorization']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return AuthorizationSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isAuthorization, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isAuthorization)
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isAuthorization)


class TestCSeqSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['CSeq', 'CSEQ', 'cseq']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return CSeqSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isCSeq, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isCSeq)
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isCSeq)


class TestCallIDSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Call-ID', 'CALL-Id', 'call-id', 'Call-id', 'call-ID']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return CallIDSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isCallID, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isCallID)
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isCallID)


class TestCallInfoSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Call-Info', 'CALL-Info', 'call-info', 'Call-info', 'call-Info']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return CallInfoSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isCallInfo, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isCallInfo)
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isCallInfo)


class TestContactSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Contact', 'CONTACT', 'contact']

    @property
    def canonicalFieldValues(self):
        return ['"3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;expires=1000',
                '<sip:3122221000@200.23.3.241:5061;user=phone>',
                '"3122221000"<sip:200.23.3.241:5061;user=phone>',
                '"3122221000"<sip:3122221000@200.23.3.241;user=phone>',
                '"3122221000"<sip:3122221000@200.23.3.241:5061>',
                '"3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>',
                '<sip:3122221000@200.23.3.241:5061;user=phone>',
                'sip:3122221000@200.23.3.241:5061',
                '"3122221000"<sip:3122221000@200.23.3.241:5061>',
                '"3122221000"<sip:200.23.3.241>',
                '"3122221000"<sip:200.23.3.241',
                'sip:3122221000@200.23.3.241',
                'sip:200.23.3.241',
                'sip:200.23.3.241:5061']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ContactSIPHeaderField

    def test_parseSetValuesAndReParse(self):
        headerFieldString = 'Contact: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;expires=1000'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'expires': '1000'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')
        headerField.displayName = 'foo'
        self.assertEqual(headerField.rawString, 'Contact: "foo"<sip:3122221000@200.23.3.241:5061;user=phone>;expires=1000')
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.displayName, 'foo')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'expires': '1000'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')
        headerField.sipURI = SIPURI.newParsedFrom('sip:0.0.0.0')
        self.assertEqual(headerField.rawString, 'Contact: "foo"<sip:0.0.0.0>;expires=1000')
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.displayName, 'foo')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'expires': '1000'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:0.0.0.0')
        self.assertEqual(headerField.sipURI.host, '0.0.0.0')
        self.assertEqual(headerField.sipURI.port, None)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.user, None)

    def test_parseValid001(self):
        headerFieldString = 'Contact: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid002(self):
        headerFieldString = 'Contact: <sip:3122221000@200.23.3.241:5061;user=phone>'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.displayName, '')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid003(self):
        headerFieldString = 'Contact: "3122221000"<sip:200.23.3.241:5061;user=phone>'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, None)

    def test_parseValid004(self):
        headerFieldString = 'Contact: "3122221000"<sip:3122221000@200.23.3.241;user=phone>'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, None)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid005(self):
        headerFieldString = 'Contact: "3122221000"<sip:3122221000@200.23.3.241:5061>'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid006(self):
        headerFieldString = 'Contact: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid007(self):
        headerFieldString = 'Contact: <sip:3122221000@200.23.3.241:5061;user=phone>'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.displayName, '')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid008(self):
        headerFieldString = 'Contact: sip:3122221000@200.23.3.241:5061'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.displayName, None)
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isContact, line)

    def test_rendering(self):
        headerFieldString = 'Contact: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>'
        headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(displayName='3122221000', sipURI=SIPURI.newParsedFrom('sip:3122221000@200.23.3.241:5061;user=phone'))
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.displayName, '3122221000')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')


class TestContentDispositionSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Content-Disposition', 'CONTENT-Disposition', 'content-disposition', 'Content-disposition', 'content-Disposition']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ContentDispositionSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isContentDisposition, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isContentDisposition)
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isContentDisposition)


class TestContentTypeSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Content-Type', 'CONTENT-Type', 'content-type', 'Content-type', 'content-Type']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ContentTypeSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isContentType, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isContentType)
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isContentType)


class TestDateSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Date', 'DATE', 'date']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return DateSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isDate, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isDate)
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isDate)


class TestExpiresSipHeaderField(AbstractIntegerSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Expires', 'EXPIRES', 'expires']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ExpiresSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isExpires, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isExpires)
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isExpires)


class TestFromSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['From', 'FROM', 'from']

    @property
    def canonicalFieldValues(self):
        return ['"3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                '<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                '"3122221000"<sip:200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                '"3122221000"<sip:3122221000@200.23.3.241;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                '"3122221000"<sip:3122221000@200.23.3.241:5061>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                '"3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>',
                '<sip:3122221000@200.23.3.241:5061;user=phone>',
                'sip:3122221000@200.23.3.241:5061;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                'sip:3122221000@200.23.3.241:5061',
                '"3122221000"<sip:3122221000@200.23.3.241:5061>',
                '"3122221000"<sip:200.23.3.241>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                '"3122221000"<sip:200.23.3.241>',
                '"3122221000"<sip:200.23.3.241;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                'sip:3122221000@200.23.3.241',
                'sip:200.23.3.241',
                'sip:200.23.3.241:5061']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return FromSIPHeaderField

    def test_parseSetValuesAndReParse(self):
        headerFieldString = 'From: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')
        headerField.displayName = 'foo'
        self.assertEqual(headerField.rawString, 'From: "foo"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(headerField.displayName, 'foo')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')
        headerField.tag = 'TESTTAG'
        self.assertEqual(headerField.rawString, 'From: "foo"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=TESTTAG')
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, 'TESTTAG')
        self.assertEqual(headerField.displayName, 'foo')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': 'TESTTAG'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')
        headerField.sipURI = SIPURI.newParsedFrom('sip:0.0.0.0')
        self.assertEqual(headerField.rawString, 'From: "foo"<sip:0.0.0.0>;tag=TESTTAG')
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, 'TESTTAG')
        self.assertEqual(headerField.displayName, 'foo')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': 'TESTTAG'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:0.0.0.0')
        self.assertEqual(headerField.sipURI.host, '0.0.0.0')
        self.assertEqual(headerField.sipURI.port, None)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.user, None)

    def test_parseValid001(self):
        headerFieldString = 'From: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid002(self):
        headerFieldString = 'From: <sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(headerField.displayName, '')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid003(self):
        headerFieldString = 'From: "3122221000"<sip:200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, None)

    def test_parseValid004(self):
        headerFieldString = 'From: "3122221000"<sip:3122221000@200.23.3.241;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, None)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid005(self):
        headerFieldString = 'From: "3122221000"<sip:3122221000@200.23.3.241:5061>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid006(self):
        headerFieldString = 'From: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, None)
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid007(self):
        headerFieldString = 'From: <sip:3122221000@200.23.3.241:5061;user=phone>'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, None)
        self.assertEqual(headerField.displayName, '')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid008(self):
        headerFieldString = 'From: sip:3122221000@200.23.3.241:5061'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, None)
        self.assertEqual(headerField.displayName, None)
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isFrom, line)

    def test_rendering(self):
        headerFieldString = 'From: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(displayName='3122221000', tag='29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875', sipURI=SIPURI.newParsedFrom('sip:3122221000@200.23.3.241:5061;user=phone'))
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(headerField.displayName, '3122221000')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_tagGeneration(self):
        headerFieldString = 'From: sip:3122221000@200.23.3.241:5061'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.tag, None)
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        headerField.generateTag()
        self.assertIsInstance(headerField.tag, basestring)
        self.assertTrue('tag' in headerField.parameterNamesAndValueStrings)


class TestMaxForwardsSipHeaderField(AbstractIntegerSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Max-Forwards', 'MAX-Forwards', 'max-forwards', 'Max-forwards', 'max-Forwards']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return MaxForwardsSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isMaxForwards, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isMaxForwards)
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isMaxForwards)


class TestRecordRouteSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Record-Route', 'RECORD-Route', 'record-route', 'Record-route', 'record-Route']

    @property
    def canonicalFieldValues(self):
        return ['<sip:3122221000@200.23.3.241:5061;lr>',
                '<sip:3122221000@200.23.3.241:5061>'
                ]

    @property
    def canonicalFieldValues(self):
        return ['<sip:3122221000@200.23.3.241:5061;lr>',
                '<sip:3122221000@200.23.3.241:5061>'
                ]

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RecordRouteSIPHeaderField

    def test_parseSetValuesAndReParse(self):
        headerFieldString = 'Record-Route: <sip:3122221000@200.23.3.241:5061;transport=TLS>'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;transport=TLS')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        headerField.sipURI = SIPURI.newParsedFrom('sip:0.0.0.0')
        self.assertEqual(headerField.rawString, 'Record-Route: <sip:0.0.0.0>')
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:0.0.0.0')
        self.assertEqual(headerField.sipURI.host, '0.0.0.0')
        self.assertEqual(headerField.sipURI.port, None)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isRecordRoute)

    def test_rendering(self):
        headerFieldString = 'Record-Route: <sip:3122221000@200.23.3.241:5061;transport=TLS>'
        headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(sipURI=SIPURI.newParsedFrom('sip:3122221000@200.23.3.241:5061;transport=TLS'))
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;transport=TLS')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.user, '3122221000')


class TestRequireSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Require', 'REQUIRE', 'require']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RequireSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isRequire, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isRequire)
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isRequire)


class TestRetryAfterSipHeaderField(AbstractIntegerSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Retry-After', 'RETRY-After', 'retry-after', 'Retry-after', 'retry-After']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RetryAfterSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isRetryAfter, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isRetryAfter)
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isRetryAfter)


class TestRouteSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldValues(self):
        return ['<sip:3122221000@200.23.3.241:5061;lr>',
                '<sip:3122221000@200.23.3.241:5061>'
                ]

    @property
    def canonicalFieldNames(self):
        return['Route', 'ROUTE', 'route']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RouteSIPHeaderField

    def test_parseSetValuesAndReParse(self):
        headerFieldString = 'Route: <sip:3122221000@200.23.3.241:5061;transport=TLS>'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;transport=TLS')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        headerField.sipURI = SIPURI.newParsedFrom('sip:0.0.0.0')
        self.assertEqual(headerField.rawString, 'Route: <sip:0.0.0.0>')
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:0.0.0.0')
        self.assertEqual(headerField.sipURI.host, '0.0.0.0')
        self.assertEqual(headerField.sipURI.port, None)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isRoute)

    def test_rendering(self):
        headerFieldString = 'Route: <sip:3122221000@200.23.3.241:5061;transport=TLS>'
        headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(sipURI=SIPURI.newParsedFrom('sip:3122221000@200.23.3.241:5061;transport=TLS'))
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;transport=TLS')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.user, '3122221000')


class TestServerSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Server', 'SERVER', 'server']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ServerSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isServer, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isServer)
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isServer)


class TestSessionExpiresSipHeaderField(AbstractIntegerSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Session-Expires', 'SESSION-Expires', 'session-expires', 'Session-expires', 'session-Expires']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return SessionExpiresSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isSessionExpires, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isSessionExpires)
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isSessionExpires)


class TestSupportedSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Supported', 'SUPPORTED', 'supported']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return SupportedSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isSupported, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isSupported)
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isSupported)


class TestTimestampSipHeaderField(AbstractIntegerSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Timestamp', 'TIMESTAMP', 'timestamp']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return TimestampSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isTimestamp, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isTimestamp)
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isTimestamp)


class TestToSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['To', 'TO', 'to']

    @property
    def canonicalFieldValues(self):
        return ['"3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                '<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                '"3122221000"<sip:200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                '"3122221000"<sip:3122221000@200.23.3.241;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                '"3122221000"<sip:3122221000@200.23.3.241:5061>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                '"3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>',
                '<sip:3122221000@200.23.3.241:5061;user=phone>',
                'sip:3122221000@200.23.3.241:5061;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                'sip:3122221000@200.23.3.241:5061',
                '"3122221000"<sip:3122221000@200.23.3.241:5061>',
                '"3122221000"<sip:200.23.3.241>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                '"3122221000"<sip:200.23.3.241>',
                '"3122221000"<sip:200.23.3.241;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                'sip:3122221000@200.23.3.241',
                'sip:200.23.3.241',
                'sip:200.23.3.241:5061']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ToSIPHeaderField

    def test_parseSetValuesAndReParse(self):
        headerFieldString = 'To: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')
        headerField.displayName = 'foo'
        self.assertEqual(headerField.rawString, 'To: "foo"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(headerField.displayName, 'foo')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')
        headerField.tag = 'TESTTAG'
        self.assertEqual(headerField.rawString, 'To: "foo"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=TESTTAG')
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, 'TESTTAG')
        self.assertEqual(headerField.displayName, 'foo')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': 'TESTTAG'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')
        headerField.sipURI = SIPURI.newParsedFrom('sip:0.0.0.0')
        self.assertEqual(headerField.rawString, 'To: "foo"<sip:0.0.0.0>;tag=TESTTAG')
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, 'TESTTAG')
        self.assertEqual(headerField.displayName, 'foo')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': 'TESTTAG'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:0.0.0.0')
        self.assertEqual(headerField.sipURI.host, '0.0.0.0')
        self.assertEqual(headerField.sipURI.port, None)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.user, None)

    def test_parseValid001(self):
        headerFieldString = 'To: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid002(self):
        headerFieldString = 'To: <sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(headerField.displayName, '')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid003(self):
        headerFieldString = 'To: "3122221000"<sip:200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, None)

    def test_parseValid004(self):
        headerFieldString = 'To: "3122221000"<sip:3122221000@200.23.3.241;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, None)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid005(self):
        headerFieldString = 'To: "3122221000"<sip:3122221000@200.23.3.241:5061>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid006(self):
        headerFieldString = 'To: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, None)
        self.assertEqual(headerField.displayName, '"3122221000"')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid007(self):
        headerFieldString = 'To: <sip:3122221000@200.23.3.241:5061;user=phone>'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, None)
        self.assertEqual(headerField.displayName, '')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parseValid008(self):
        headerFieldString = 'To: sip:3122221000@200.23.3.241:5061'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, None)
        self.assertEqual(headerField.displayName, None)
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isTo, line)

    def test_rendering(self):
        headerFieldString = 'To: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(displayName='3122221000', tag='29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875', sipURI=SIPURI.newParsedFrom('sip:3122221000@200.23.3.241:5061;user=phone'))
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(headerField.displayName, '3122221000')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(headerField.sipURI.rawString, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(headerField.sipURI.host, '200.23.3.241')
        self.assertEqual(headerField.sipURI.port, 5061)
        self.assertEqual(headerField.sipURI.scheme, 'sip')
        self.assertEqual(headerField.sipURI.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(headerField.sipURI.user, '3122221000')

    def test_tagGeneration(self):
        headerFieldString = 'To: sip:3122221000@200.23.3.241:5061'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.tag, None)
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        headerField.generateTag()
        self.assertIsInstance(headerField.tag, basestring)
        self.assertTrue('tag' in headerField.parameterNamesAndValueStrings)


class TestUserAgentSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['User-Agent', 'USER-Agent', 'user-agent', 'User-agent', 'user-Agent']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return UserAgentSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isUserAgent, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isUserAgent)
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isUserAgent)


class TestWWWAuthenticateSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['WWW-Authenticate', 'Www-Authenticate', 'www-authenticate', 'Www-authenticate', 'www-Authenticate']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return WWWAuthenticateSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isWWWAuthenticate, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isWWWAuthenticate)
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isWWWAuthenticate)


class TestWarningSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Warning', 'WARNING', 'warning']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return WarningSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isWarning, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
                self.assertTrue(headerField.isWarning)
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isWarning)


class TestViaSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def sipHeaderFieldClassUnderTest(self):
        return ViaSIPHeaderField

    @property
    def canonicalFieldNames(self):
        return['Via', 'VIA', 'via']

    @property
    def canonicalFieldValues(self):
        return ['SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500',
                'SIP/2.0/TLS 200.25.3.250:5061;branch=z9hG4bKfdkajhdiruyalkghjladksjf',
                'SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf'
                ]

    def test_parseSetValuesAndReParse(self):
        headerFieldString = 'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(headerField.transport, 'TLS')
        self.assertEqual(headerField.host, '200.25.3.150')
        self.assertEqual(headerField.port, None)
        headerField.host = '192.168.0.5'
        self.assertEqual(headerField.rawString, 'Via: SIP/2.0/TLS 192.168.0.5;branch=z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(headerField.transport, 'TLS')
        self.assertEqual(headerField.host, '192.168.0.5')
        self.assertEqual(headerField.port, None)
        headerField.port = 5061
        self.assertEqual(headerField.rawString, 'Via: SIP/2.0/TLS 192.168.0.5:5061;branch=z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(headerField.transport, 'TLS')
        self.assertEqual(headerField.host, '192.168.0.5')
        self.assertEqual(headerField.port, 5061)
        headerField.transport = 'UDP'
        self.assertEqual(headerField.rawString, 'Via: SIP/2.0/UDP 192.168.0.5:5061;branch=z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(headerField.transport, 'UDP')
        self.assertEqual(headerField.host, '192.168.0.5')
        self.assertEqual(headerField.port, 5061)
        headerField.branch = 'z9hG4bKblarg'
        self.assertEqual(headerField.rawString, 'Via: SIP/2.0/UDP 192.168.0.5:5061;branch=z9hG4bKblarg')
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.branch, 'z9hG4bKblarg')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'branch': 'z9hG4bKblarg'})
        self.assertEqual(headerField.transport, 'UDP')
        self.assertEqual(headerField.host, '192.168.0.5')
        self.assertEqual(headerField.port, 5061)

    def test_parseValid001(self):
        headerFieldString = 'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(headerField.transport, 'TLS')
        self.assertEqual(headerField.host, '200.25.3.150')
        self.assertEqual(headerField.port, None)

    def test_parseValid002(self):
        headerFieldString = 'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(headerField.transport, 'TLS')
        self.assertEqual(headerField.host, '200.25.3.150')
        self.assertEqual(headerField.port, None)

    def test_parseValid003(self):
        headerFieldString = 'Via: SIP/2.0/TLS 192.168.0.5:5061;branch=z9hG4bK0ee8d3e272e31ca195299efc500'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(headerField.transport, 'TLS')
        self.assertEqual(headerField.host, '192.168.0.5')
        self.assertEqual(headerField.port, 5061)

    def test_parseValid004(self):
        headerFieldString = 'Via: SIP/2.0/UDP 192.168.0.5:5061;branch=z9hG4bK0ee8d3e272e31ca195299efc500'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(headerField.transport, 'UDP')
        self.assertEqual(headerField.host, '192.168.0.5')
        self.assertEqual(headerField.port, 5061)

    def test_parseValid005(self):
        headerFieldString = 'Via: SIP/2.0/UDP 192.168.0.5:5061;branch=z9hG4bKblarg'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.branch, 'z9hG4bKblarg')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'branch': 'z9hG4bKblarg'})
        self.assertEqual(headerField.transport, 'UDP')
        self.assertEqual(headerField.host, '192.168.0.5')
        self.assertEqual(headerField.port, 5061)

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isVia, line)

    def test_rendering(self):
        headerFieldString = 'Via: SIP/2.0/UDP 192.168.0.5:5061;branch=z9hG4bK0ee8d3e272e31ca195299efc500'
        headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(host='192.168.0.5', port=5061, transport='UDP', branch='z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(headerField.rawString, headerFieldString)
        self.assertTrue(headerField.isValid)
        self.assertEqual(headerField.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(headerField.parameterNamesAndValueStrings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(headerField.transport, 'UDP')
        self.assertEqual(headerField.host, '192.168.0.5')
        self.assertEqual(headerField.port, 5061)

    def test_branchGeneration(self):
        headerFieldString = 'Via: SIP/2.0/UDP 192.168.0.5:5061'
        headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(headerFieldString)
        self.assertTrue(headerField.isVia)
        self.assertEqual(headerField.branch, None)
        self.assertEqual(headerField.parameterNamesAndValueStrings, {})
        headerField.generateBranch()
        self.assertIsInstance(headerField.branch, basestring)
        self.assertTrue('branch' in headerField.parameterNamesAndValueStrings)
