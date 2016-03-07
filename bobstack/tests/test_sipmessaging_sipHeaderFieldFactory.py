try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
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
from sipmessaging import SIPHeaderFieldFactory
from abstractSIPHeaderFieldFromFactoryTestCase import AbstractSIPHeaderFieldFromFactoryTestCase
from abstractIntegerSIPHeaderFieldFromFactoryTestCase import AbstractIntegerSIPHeaderFieldFromFactoryTestCase

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


class TestSIPHeaderFieldFactoryForContentLength(AbstractIntegerSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Content-Length', 'CONTENT-Length', 'content-length', 'Content-length', 'content-Length']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ContentLengthSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isContentLength)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isContentLength, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isContentLength, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isContentLength, line)

class TestSIPHeaderFieldFactoryForAccept(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Accept', 'ACCEPT', 'accept']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return AcceptSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isAccept, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isAccept, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isAccept, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isAccept, line)

class TestSIPHeaderFieldFactoryForAcceptEncoding(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Accept-Encoding', 'ACCEPT-Encoding', 'accept-encoding', 'Accept-encoding', 'accept-Encoding']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return AcceptEncodingSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isAcceptEncoding, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isAcceptEncoding, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isAcceptEncoding, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isAcceptEncoding, line)


class TestSIPHeaderFieldFactoryForAcceptLanguage(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Accept-Language', 'ACCEPT-Language', 'accept-language', 'Accept-language', 'accept-Language']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return AcceptLanguageSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isAcceptLanguage, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isAcceptLanguage, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isAcceptLanguage, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isAcceptLanguage, line)


class TestSIPHeaderFieldFactoryForAllow(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Allow', 'ALLOW', 'allow']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return AllowSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isAllow, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isAllow, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isAllow, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isAllow, line)


class TestSIPHeaderFieldFactoryForAuthorization(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Authorization', 'AUTHORIZATION', 'authorization']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return AuthorizationSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isAuthorization, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isAuthorization, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isAuthorization, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isAuthorization, line)


class TestSIPHeaderFieldFactoryForCSeq(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['CSeq', 'CSEQ', 'cseq']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return CSeqSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isCSeq, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isCSeq, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isCSeq, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isCSeq, line)


class TestSIPHeaderFieldFactoryForCallID(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Call-ID', 'CALL-Id', 'call-id', 'Call-id', 'call-ID']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return CallIDSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isCallID, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isCallID, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isCallID, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isCallID, line)

class TestSIPHeaderFieldFactoryForCallInfo(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Call-Info', 'CALL-Info', 'call-info', 'Call-info', 'call-Info']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return CallInfoSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isCallInfo, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isCallInfo, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isCallInfo, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isCallInfo, line)

class TestSIPHeaderFieldFactoryForContact(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Contact', 'CONTACT', 'contact']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ContactSIPHeaderField

    @property
    def emptyHeaderFieldBodyIsValid(self):
        return False

    @property
    def canonicalFieldValues(self):
        return ['"3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;expires=1000',
                '"3122221000"<sip:200.23.3.241;user=phone>',
                'sip:3122221000@200.23.3.241',
                'sip:200.23.3.241',
                'sip:200.23.3.241:5061',
                'sip:200.23.3.241:5061'
                ]

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isContact, line)
            self.assertTrue(headerField.isValid)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isContact, line)
            self.assertTrue(headerField.isValid)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isContact, line)
            self.assertFalse(headerField.isValid)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isContact, line)
            self.assertFalse(headerField.isValid)

class TestSIPHeaderFieldFactoryForContentDisposition(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Content-Disposition', 'CONTENT-Disposition', 'content-disposition', 'Content-disposition', 'content-Disposition']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ContentDispositionSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isContentDisposition, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isContentDisposition, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isContentDisposition, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isContentDisposition, line)

class TestSIPHeaderFieldFactoryForContentType(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Content-Type', 'CONTENT-Type', 'content-type', 'Content-type', 'content-Type']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ContentTypeSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isContentType, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isContentType, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isContentType, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isContentType, line)

class TestSIPHeaderFieldFactoryForDate(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Date', 'DATE', 'date']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return DateSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isDate, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isDate, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isDate, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isDate, line)

class TestSIPHeaderFieldFactoryForExpires(AbstractIntegerSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Expires', 'EXPIRES', 'expires']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ExpiresSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isExpires, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isExpires, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isExpires, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isExpires, line)


class TestSIPHeaderFieldFactoryForFrom(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['From', 'FROM', 'from']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return FromSIPHeaderField

    @property
    def emptyHeaderFieldBodyIsValid(self):
        return False

    @property
    def canonicalFieldValues(self):
        return ['"3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                '"3122221000"<sip:200.23.3.241;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                'sip:3122221000@200.23.3.241',
                'sip:200.23.3.241',
                'sip:200.23.3.241:5061',
                'sip:200.23.3.241:5061;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
                ]

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isFrom, line)
            self.assertTrue(headerField.isValid)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isFrom, line)
            self.assertTrue(headerField.isValid)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isFrom, line)
            self.assertFalse(headerField.isValid)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isFrom, line)
            self.assertFalse(headerField.isValid)


class TestSIPHeaderFieldFactoryForMaxForwards(AbstractIntegerSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Max-Forwards', 'MAX-Forwards', 'max-forwards', 'Max-forwards', 'max-Forwards']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return MaxForwardsSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isMaxForwards, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isMaxForwards, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isMaxForwards, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isMaxForwards, line)

class TestSIPHeaderFieldFactoryForRecordRoute(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Record-Route', 'RECORD-Route', 'record-route', 'Record-route', 'record-Route']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RecordRouteSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isRecordRoute, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isRecordRoute, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isRecordRoute, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isRecordRoute, line)


class TestSIPHeaderFieldFactoryForRequire(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Require', 'REQUIRE', 'require']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RequireSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isRequire, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isRequire, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isRequire, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isRequire, line)


class TestSIPHeaderFieldFactoryForRetryAfter(AbstractIntegerSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Retry-After', 'RETRY-After', 'retry-after', 'Retry-after', 'retry-After']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RetryAfterSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isRetryAfter, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isRetryAfter, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isRetryAfter, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isRetryAfter, line)


class TestSIPHeaderFieldFactoryForRoute(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Route', 'ROUTE', 'route']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RouteSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isRoute, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isRoute, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isRoute, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isRoute, line)


class TestSIPHeaderFieldFactoryForServer(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Server', 'SERVER', 'server']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ServerSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isServer, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isServer, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isServer, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isServer, line)


class TestSIPHeaderFieldFactoryForSessionExpires(AbstractIntegerSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Session-Expires', 'SESSION-Expires', 'session-expires', 'Session-expires', 'session-Expires']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return SessionExpiresSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isSessionExpires, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isSessionExpires, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isSessionExpires, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isSessionExpires, line)


class TestSIPHeaderFieldFactoryForSupported(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Supported', 'SUPPORTED', 'supported']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return SupportedSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isSupported, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isSupported, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isSupported, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isSupported, line)


class TestSIPHeaderFieldFactoryForTimestamp(AbstractIntegerSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Timestamp', 'TIMESTAMP', 'timestamp']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return TimestampSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isTimestamp, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isTimestamp, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isTimestamp, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isTimestamp, line)


class TestSIPHeaderFieldFactoryForTo(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['To', 'TO', 'to']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ToSIPHeaderField

    @property
    def emptyHeaderFieldBodyIsValid(self):
        return False

    @property
    def canonicalFieldValues(self):
        return ['"3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                '"3122221000"<sip:200.23.3.241;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875',
                'sip:3122221000@200.23.3.241',
                'sip:200.23.3.241',
                'sip:200.23.3.241:5061',
                'sip:200.23.3.241:5061;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
                ]

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isTo, line)
            self.assertTrue(headerField.isValid)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isTo, line)
            self.assertTrue(headerField.isValid)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isTo, line)
            self.assertFalse(headerField.isValid)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isTo, line)
            self.assertFalse(headerField.isValid)


class TestSIPHeaderFieldFactoryForUserAgent(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['User-Agent', 'USER-Agent', 'user-agent', 'User-agent', 'user-Agent']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return UserAgentSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isUserAgent, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isUserAgent, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isUserAgent, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isUserAgent, line)


class TestSIPHeaderFieldFactoryForWWWAuthenticate(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['WWW-Authenticate', 'Www-Authenticate', 'www-authenticate', 'Www-authenticate', 'www-Authenticate']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return WWWAuthenticateSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isWWWAuthenticate, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isWWWAuthenticate, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isWWWAuthenticate, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isWWWAuthenticate, line)


class TestSIPHeaderFieldFactoryForWarning(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Warning', 'WARNING', 'warning']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return WarningSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isWarning, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isWarning, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isWarning, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isWarning, line)


class TestSIPHeaderFieldFactoryForVia(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Via', 'VIA', 'via']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ViaSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isVia, line)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isVia, line)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isVia, line)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isVia, line)
