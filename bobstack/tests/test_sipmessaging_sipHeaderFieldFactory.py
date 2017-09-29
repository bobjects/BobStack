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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            if line.split().__len__() < 2:
                self.assertFalse(header_field.isValid)
            else:
                if ":" not in line:
                    self.assertFalse(header_field.isValid)
                else:
                    self.assertTrue(header_field.isValid)
            self.assertFalse(header_field.isContentLength)
            self.assertFalse(header_field.isKnown)
            self.assertEqual(header_field.rawString, line)
            if line:
                stringio = StringIO(line + '\r\n')
                header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
                if line.split().__len__() < 2:
                    self.assertFalse(header_field.isValid)
                else:
                    if ":" not in line:
                        self.assertFalse(header_field.isValid)
                    else:
                        self.assertTrue(header_field.isValid)
                    self.assertFalse(header_field.isContentLength)
                    self.assertFalse(header_field.isKnown)
                    self.assertEqual(header_field.rawString, line)
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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isContentLength)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isContentLength)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isContentLength)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isContentLength)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.isContentLength)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isContentLength)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isAccept)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isAccept)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isAccept)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isAccept)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isAcceptEncoding)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isAcceptEncoding)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isAcceptEncoding)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isAcceptEncoding)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isAcceptLanguage)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isAcceptLanguage)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isAcceptLanguage)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isAcceptLanguage)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isAllow)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isAllow)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isAllow)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isAllow)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isAuthorization)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isAuthorization)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isAuthorization)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isAuthorization)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isCSeq)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isCSeq)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isCSeq)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isCSeq)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isCallID)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isCallID)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isCallID)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isCallID)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.isCallID)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isCallID)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isCallInfo)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isCallInfo)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isCallInfo)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isCallInfo)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isContact)
            self.assertTrue(header_field.isValid)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isContact)
            self.assertTrue(header_field.isValid)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isContact)
            self.assertFalse(header_field.isValid)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isContact)
            self.assertFalse(header_field.isValid)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.isContact)
            self.assertFalse(header_field.isValid)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isContact)
            self.assertFalse(header_field.isValid)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isContentDisposition)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isContentDisposition)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isContentDisposition)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isContentDisposition)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isContentType)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isContentType)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isContentType)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isContentType)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.isContentType)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isContentType)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isDate)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isDate)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isDate)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isDate)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isExpires)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isExpires)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isExpires)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isExpires)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isFrom)
            self.assertTrue(header_field.isValid)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isFrom)
            self.assertTrue(header_field.isValid)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isFrom)
            self.assertFalse(header_field.isValid)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isFrom)
            self.assertFalse(header_field.isValid)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.isFrom)
            self.assertFalse(header_field.isValid)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isFrom)
            self.assertFalse(header_field.isValid)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isMaxForwards)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isMaxForwards)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isMaxForwards)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isMaxForwards)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isRecordRoute)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isRecordRoute)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isRecordRoute)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isRecordRoute)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isRequire)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isRequire)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isRequire)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isRequire)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isRetryAfter)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isRetryAfter)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isRetryAfter)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isRetryAfter)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isRoute)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isRoute)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isRoute)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isRoute)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isServer)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isServer)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isServer)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isServer)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isSessionExpires)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isSessionExpires)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isSessionExpires)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isSessionExpires)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isSupported)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isSupported)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isSupported)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isSupported)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.isSupported)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isSupported)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isTimestamp)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isTimestamp)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isTimestamp)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isTimestamp)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isTo)
            self.assertTrue(header_field.isValid)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isTo)
            self.assertTrue(header_field.isValid)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isTo)
            self.assertFalse(header_field.isValid)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isTo)
            self.assertFalse(header_field.isValid)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.isTo)
            self.assertFalse(header_field.isValid)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isTo)
            self.assertFalse(header_field.isValid)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isUserAgent)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isUserAgent)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isUserAgent)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isUserAgent)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isWWWAuthenticate)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isWWWAuthenticate)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isWWWAuthenticate)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isWWWAuthenticate)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isWarning)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isWarning)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isWarning)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isWarning)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isSubject)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isSubject)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isSubject)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isSubject)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.isSubject)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isSubject)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isReferredBy)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isReferredBy)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isReferredBy)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isReferredBy)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.isReferredBy)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isReferredBy)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isReferTo)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isReferTo)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isReferTo)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isReferTo)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.isReferTo)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isReferTo)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isAllowEvents)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isAllowEvents)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isAllowEvents)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isAllowEvents)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.isAllowEvents)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isAllowEvents)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isEvent)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isEvent)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isEvent)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isEvent)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isContentEncoding)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isContentEncoding)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isContentEncoding)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isContentEncoding)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.isContentEncoding)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isContentEncoding)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isRAck)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isRAck)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isRAck)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isRAck)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isPCharge)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isPCharge)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isPCharge)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isPCharge)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isReplyTo)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isReplyTo)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isReplyTo)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isReplyTo)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isUnsupported)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isUnsupported)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isUnsupported)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isUnsupported)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isPAssertedIdentity)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isPAssertedIdentity)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isPAssertedIdentity)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isPAssertedIdentity)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isPPreferredIdentity)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isPPreferredIdentity)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isPPreferredIdentity)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isPPreferredIdentity)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isRemotePartyID)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isRemotePartyID)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isRemotePartyID)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isRemotePartyID)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isAlertInfo)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isAlertInfo)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isAlertInfo)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isAlertInfo)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isHistoryInfo)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isHistoryInfo)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isHistoryInfo)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isHistoryInfo)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isPCalledPartyId)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isPCalledPartyId)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isPCalledPartyId)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isPCalledPartyId)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isPRTPStat)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isPRTPStat)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isPRTPStat)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isPRTPStat)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isPrivacy)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isPrivacy)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isPrivacy)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isPrivacy)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isProxyAuthenticate)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isProxyAuthenticate)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isProxyAuthenticate)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isProxyAuthenticate)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isProxyAuthorization)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isProxyAuthorization)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isProxyAuthorization)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isProxyAuthorization)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isProxyRequire)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isProxyRequire)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isProxyRequire)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isProxyRequire)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isReason)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isReason)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isReason)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isReason)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isRecordSessionExpires)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isRecordSessionExpires)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isRecordSessionExpires)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isRecordSessionExpires)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isReplaces)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isReplaces)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isReplaces)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isReplaces)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isSubscriptionState)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isSubscriptionState)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isSubscriptionState)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isSubscriptionState)


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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isMinExpires)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isMinExpires)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isMinExpires)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isMinExpires)


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
    #         header_field = SIPHeaderFieldFactory().nextForString(line)
    #         self.assertTrue(header_field.isVia)
    #         stringio = StringIO(line + '\r\n')
    #         header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
    #         self.assertTrue(header_field.isVia)
    #         stringio.close()
    #         header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
    #         self.assertTrue(header_field.isVia)
    #         header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
    #         self.assertTrue(header_field.isVia)
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
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.isVia)
            self.assertTrue(header_field.isValid)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isVia)
            self.assertTrue(header_field.isValid)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.isVia)
            self.assertFalse(header_field.isValid)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isVia)
            self.assertFalse(header_field.isValid)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.isVia)
            self.assertFalse(header_field.isValid)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.isVia)
            self.assertFalse(header_field.isValid)
