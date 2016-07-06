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
from sipmessaging import SubjectSIPHeaderField
from sipmessaging import ReferredBySIPHeaderField
from sipmessaging import ReferToSIPHeaderField
from sipmessaging import AllowEventsSIPHeaderField
from sipmessaging import EventSIPHeaderField
from sipmessaging import ContentEncodingSIPHeaderField
from sipmessaging import RAckSIPHeaderField
from sipmessaging import PChargeSIPHeaderField
from sipmessaging import ReplyToSIPHeaderField
from sipmessaging import UnsupportedSIPHeaderField
from sipmessaging import PAssertedIdentitySIPHeaderField
from sipmessaging import PPreferredIdentitySIPHeaderField
from sipmessaging import RemotePartyIDSIPHeaderField
from sipmessaging import AlertInfoSIPHeaderField
from sipmessaging import HistoryInfoSIPHeaderField
from sipmessaging import PCalledPartyIdSIPHeaderField
from sipmessaging import PRTPStatSIPHeaderField
from sipmessaging import PrivacySIPHeaderField
from sipmessaging import ProxyAuthenticateSIPHeaderField
from sipmessaging import ProxyAuthorizationSIPHeaderField
from sipmessaging import ProxyRequireSIPHeaderField
from sipmessaging import ReasonSIPHeaderField
from sipmessaging import RecordSessionExpiresSIPHeaderField
from sipmessaging import ReplacesSIPHeaderField
from sipmessaging import SubscriptionStateSIPHeaderField
from sipmessaging import MinExpiresSIPHeaderField
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
            self.assertTrue(headerField.isContentLength)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isContentLength)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isContentLength)
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(headerField.isContentLength)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isContentLength)


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
            self.assertTrue(headerField.isAccept)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isAccept)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isAccept)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isAccept)


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
            self.assertTrue(headerField.isAcceptEncoding)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isAcceptEncoding)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isAcceptEncoding)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isAcceptEncoding)


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
            self.assertTrue(headerField.isAcceptLanguage)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isAcceptLanguage)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isAcceptLanguage)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isAcceptLanguage)


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
            self.assertTrue(headerField.isAllow)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isAllow)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isAllow)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isAllow)


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
            self.assertTrue(headerField.isAuthorization)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isAuthorization)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isAuthorization)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isAuthorization)


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
            self.assertTrue(headerField.isCSeq)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isCSeq)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isCSeq)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isCSeq)


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
            self.assertTrue(headerField.isCallID)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isCallID)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isCallID)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isCallID)
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(headerField.isCallID)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isCallID)


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
            self.assertTrue(headerField.isCallInfo)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isCallInfo)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isCallInfo)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isCallInfo)


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
            self.assertTrue(headerField.isContact)
            self.assertTrue(headerField.isValid)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isContact)
            self.assertTrue(headerField.isValid)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isContact)
            self.assertFalse(headerField.isValid)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isContact)
            self.assertFalse(headerField.isValid)
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(headerField.isContact)
            self.assertFalse(headerField.isValid)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isContact)
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
            self.assertTrue(headerField.isContentDisposition)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isContentDisposition)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isContentDisposition)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isContentDisposition)


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
            self.assertTrue(headerField.isContentType)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isContentType)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isContentType)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isContentType)
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(headerField.isContentType)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isContentType)


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
            self.assertTrue(headerField.isDate)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isDate)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isDate)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isDate)


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
            self.assertTrue(headerField.isExpires)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isExpires)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isExpires)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isExpires)


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
            self.assertTrue(headerField.isFrom)
            self.assertTrue(headerField.isValid)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isFrom)
            self.assertTrue(headerField.isValid)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isFrom)
            self.assertFalse(headerField.isValid)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isFrom)
            self.assertFalse(headerField.isValid)
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(headerField.isFrom)
            self.assertFalse(headerField.isValid)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isFrom)
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
            self.assertTrue(headerField.isMaxForwards)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isMaxForwards)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isMaxForwards)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isMaxForwards)


class TestSIPHeaderFieldFactoryForRecordRoute(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Record-Route', 'RECORD-Route', 'record-route', 'Record-route', 'record-Route']

    @property
    def canonicalFieldValues(self):
        return ['<sip:200.30.10.12:5061;transport=tls;lr>',
                '<sip:3122221000@200.23.3.241:5061;lr>',
                '<sip:3122221000@200.23.3.241:5061>'
                ]

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RecordRouteSIPHeaderField

    @property
    def emptyHeaderFieldBodyIsValid(self):
        return False

    # TODO:  MOAR TESTS!  Use To tests as a guide.

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isRecordRoute)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isRecordRoute)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isRecordRoute)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isRecordRoute)


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
            self.assertTrue(headerField.isRequire)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isRequire)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isRequire)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isRequire)


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
            self.assertTrue(headerField.isRetryAfter)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isRetryAfter)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isRetryAfter)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isRetryAfter)


class TestSIPHeaderFieldFactoryForRoute(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Route', 'ROUTE', 'route']

    @property
    def canonicalFieldValues(self):
        return ['<sip:200.30.10.12:5061;transport=tls;lr>',
                '<sip:3122221000@200.23.3.241:5061;lr>',
                '<sip:3122221000@200.23.3.241:5061>'
                ]

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RouteSIPHeaderField

    @property
    def emptyHeaderFieldBodyIsValid(self):
        return False

    # TODO:  MOAR TESTS!  Use To tests as a guide.

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isRoute)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isRoute)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isRoute)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isRoute)


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
            self.assertTrue(headerField.isServer)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isServer)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isServer)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isServer)


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
            self.assertTrue(headerField.isSessionExpires)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isSessionExpires)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isSessionExpires)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isSessionExpires)


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
            self.assertTrue(headerField.isSupported)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isSupported)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isSupported)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isSupported)
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(headerField.isSupported)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isSupported)


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
            self.assertTrue(headerField.isTimestamp)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isTimestamp)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isTimestamp)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isTimestamp)


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
            self.assertTrue(headerField.isTo)
            self.assertTrue(headerField.isValid)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isTo)
            self.assertTrue(headerField.isValid)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isTo)
            self.assertFalse(headerField.isValid)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isTo)
            self.assertFalse(headerField.isValid)
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(headerField.isTo)
            self.assertFalse(headerField.isValid)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isTo)
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
            self.assertTrue(headerField.isUserAgent)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isUserAgent)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isUserAgent)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isUserAgent)


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
            self.assertTrue(headerField.isWWWAuthenticate)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isWWWAuthenticate)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isWWWAuthenticate)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isWWWAuthenticate)


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
            self.assertTrue(headerField.isWarning)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isWarning)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isWarning)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isWarning)


class TestSIPHeaderFieldFactoryForSubject(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Subject', 'SUBJECT', 'subject']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return SubjectSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isSubject)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isSubject)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isSubject)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isSubject)
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(headerField.isSubject)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isSubject)


class TestSIPHeaderFieldFactoryForReferredBy(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Referred-By', 'REFERRED-BY', 'referred-by']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ReferredBySIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isReferredBy)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isReferredBy)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isReferredBy)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isReferredBy)
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(headerField.isReferredBy)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isReferredBy)


class TestSIPHeaderFieldFactoryForReferTo(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Refer-To', 'REFER-TO', 'refer-to']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ReferToSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isReferTo)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isReferTo)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isReferTo)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isReferTo)
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(headerField.isReferTo)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isReferTo)


class TestSIPHeaderFieldFactoryForAllowEvents(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Allow-Events', 'ALLOW-EVENTS', 'allow-events']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return AllowEventsSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isAllowEvents)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isAllowEvents)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isAllowEvents)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isAllowEvents)
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(headerField.isAllowEvents)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isAllowEvents)


class TestSIPHeaderFieldFactoryForEvent(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Event', 'EVENT', 'event']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return EventSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isEvent)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isEvent)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isEvent)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isEvent)


class TestSIPHeaderFieldFactoryForContentEncoding(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Content-Encoding', 'CONTENT-ENCODING', 'content-encoding']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ContentEncodingSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isContentEncoding)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isContentEncoding)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isContentEncoding)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isContentEncoding)
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(headerField.isContentEncoding)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isContentEncoding)


class TestSIPHeaderFieldFactoryForRAck(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['RAck', 'RACK', 'rack']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RAckSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isRAck)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isRAck)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isRAck)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isRAck)


class TestSIPHeaderFieldFactoryForPCharge(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['P-Charge', 'P-CHARGE', 'p-charge']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return PChargeSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isPCharge)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isPCharge)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isPCharge)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isPCharge)


class TestSIPHeaderFieldFactoryForReplyTo(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Reply-To', 'REPLY-TO', 'reply-to']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ReplyToSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isReplyTo)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isReplyTo)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isReplyTo)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isReplyTo)


class TestSIPHeaderFieldFactoryForUnsupported(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Unsupported', 'UNSUPPORTED', 'unsupported']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return UnsupportedSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isUnsupported)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isUnsupported)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isUnsupported)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isUnsupported)


class TestSIPHeaderFieldFactoryForPAssertedIdentity(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['P-Asserted-Identity', 'P-ASSERTED-IDENTITY', 'p-asserted-identity']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return PAssertedIdentitySIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isPAssertedIdentity)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isPAssertedIdentity)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isPAssertedIdentity)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isPAssertedIdentity)


class TestSIPHeaderFieldFactoryForPPreferredIdentity(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['P-Preferred-Identity', 'P-PREFERRED-IDENTITY', 'p-preferred-identity']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return PPreferredIdentitySIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isPPreferredIdentity)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isPPreferredIdentity)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isPPreferredIdentity)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isPPreferredIdentity)


class TestSIPHeaderFieldFactoryForRemotePartyID(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Remote-Party-ID', 'REMOTE-PARTY-ID', 'remote-party-id']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RemotePartyIDSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isRemotePartyID)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isRemotePartyID)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isRemotePartyID)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isRemotePartyID)


class TestSIPHeaderFieldFactoryForAlertInfo(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Alert-Info', 'ALERT-INFO', 'alert-info']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return AlertInfoSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isAlertInfo)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isAlertInfo)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isAlertInfo)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isAlertInfo)


class TestSIPHeaderFieldFactoryForHistoryInfo(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['History-Info', 'HISTORY-INFO', 'history-info']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return HistoryInfoSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isHistoryInfo)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isHistoryInfo)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isHistoryInfo)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isHistoryInfo)


class TestSIPHeaderFieldFactoryForPCalledPartyId(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['P-Called-Party-Id', 'P-CALLED-PARTY-ID', 'p-called-party-id']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return PCalledPartyIdSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isPCalledPartyId)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isPCalledPartyId)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isPCalledPartyId)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isPCalledPartyId)


class TestSIPHeaderFieldFactoryForPRTPStat(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['P-RTP-Stat', 'P-RTP-STAT', 'p-rtp-stat']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return PRTPStatSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isPRTPStat)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isPRTPStat)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isPRTPStat)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isPRTPStat)


class TestSIPHeaderFieldFactoryForPrivacy(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Privacy', 'PRIVACY', 'privacy']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return PrivacySIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isPrivacy)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isPrivacy)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isPrivacy)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isPrivacy)


class TestSIPHeaderFieldFactoryForProxyAuthenticate(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Proxy-Authenticate', 'PROXY-AUTHENTICATE', 'proxy-authenticate']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ProxyAuthenticateSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isProxyAuthenticate)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isProxyAuthenticate)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isProxyAuthenticate)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isProxyAuthenticate)


class TestSIPHeaderFieldFactoryForProxyAuthorization(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Proxy-Authorization', 'PROXY-AUTHORIZATION', 'proxy-authorization']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ProxyAuthorizationSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isProxyAuthorization)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isProxyAuthorization)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isProxyAuthorization)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isProxyAuthorization)


class TestSIPHeaderFieldFactoryForProxyRequire(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Proxy-Require', 'PROXY-REQUIRE', 'proxy-require']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ProxyRequireSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isProxyRequire)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isProxyRequire)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isProxyRequire)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isProxyRequire)


class TestSIPHeaderFieldFactoryForReason(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Reason', 'REASON', 'reason']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ReasonSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isReason)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isReason)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isReason)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isReason)


class TestSIPHeaderFieldFactoryForRecordSessionExpires(AbstractIntegerSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Record-Session-Expires', 'RECORD-SESSION-EXPIRES', 'record-session-expires']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RecordSessionExpiresSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isRecordSessionExpires)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isRecordSessionExpires)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isRecordSessionExpires)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isRecordSessionExpires)


class TestSIPHeaderFieldFactoryForReplaces(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Replaces', 'REPLACES', 'replaces']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ReplacesSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isReplaces)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isReplaces)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isReplaces)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isReplaces)


class TestSIPHeaderFieldFactoryForSubscriptionState(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Subscription-State', 'SUBSCRIPTION-STATE', 'subscription-state']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return SubscriptionStateSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isSubscriptionState)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isSubscriptionState)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isSubscriptionState)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isSubscriptionState)


class TestSIPHeaderFieldFactoryForMinExpires(AbstractIntegerSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Min-Expires', 'MIN-EXPIRES', 'min-expires']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return MinExpiresSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isMinExpires)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isMinExpires)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isMinExpires)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isMinExpires)


class TestSIPHeaderFieldFactoryForVia(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldNames(self):
        return['Via', 'VIA', 'via']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ViaSIPHeaderField

    @property
    def emptyHeaderFieldBodyIsValid(self):
        return False

    # def test_parsing(self):
    #     self.basic_test_parsing()
    #     for line in self.canonicalStrings:
    #         headerField = SIPHeaderFieldFactory().nextForString(line)
    #         self.assertTrue(headerField.isVia)
    #         stringio = StringIO(line + '\r\n')
    #         headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
    #         self.assertTrue(headerField.isVia)
    #         stringio.close()
    #         headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
    #         self.assertTrue(headerField.isVia)
    #         headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
    #         self.assertTrue(headerField.isVia)
    #
    @property
    def canonicalFieldValues(self):
        return ['SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500',
                'SIP/2.0/TLS 200.25.3.250:5061;branch=z9hG4bKfdkajhdiruyalkghjladksjf',
                'SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf'
                ]

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isVia)
            self.assertTrue(headerField.isValid)
            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isVia)
            self.assertTrue(headerField.isValid)
            stringio.close()
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isVia)
            self.assertFalse(headerField.isValid)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isVia)
            self.assertFalse(headerField.isValid)
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(headerField.isVia)
            self.assertFalse(headerField.isValid)
            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(headerField.isVia)
            self.assertFalse(headerField.isValid)
