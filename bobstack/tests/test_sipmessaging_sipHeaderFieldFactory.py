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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            if line.split().__len__() < 2:
                self.assertFalse(header_field.is_valid)
            else:
                if ":" not in line:
                    self.assertFalse(header_field.is_valid)
                else:
                    self.assertTrue(header_field.is_valid)
            self.assertFalse(header_field.is_content_length)
            self.assertFalse(header_field.is_known)
            self.assertEqual(header_field.raw_string, line)
            if line:
                stringio = StringIO(line + '\r\n')
                header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
                if line.split().__len__() < 2:
                    self.assertFalse(header_field.is_valid)
                else:
                    if ":" not in line:
                        self.assertFalse(header_field.is_valid)
                    else:
                        self.assertTrue(header_field.is_valid)
                    self.assertFalse(header_field.is_content_length)
                    self.assertFalse(header_field.is_known)
                    self.assertEqual(header_field.raw_string, line)
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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_content_length)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_content_length)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_content_length)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_content_length)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.is_content_length)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_content_length)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_accept)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_accept)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_accept)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_accept)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_accept_encoding)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_accept_encoding)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_accept_encoding)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_accept_encoding)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_accept_language)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_accept_language)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_accept_language)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_accept_language)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_allow)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_allow)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_allow)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_allow)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_authorization)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_authorization)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_authorization)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_authorization)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_cseq)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_cseq)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_cseq)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_cseq)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_call_id)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_call_id)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_call_id)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_call_id)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.is_call_id)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_call_id)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_call_info)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_call_info)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_call_info)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_call_info)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_contact)
            self.assertTrue(header_field.is_valid)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_contact)
            self.assertTrue(header_field.is_valid)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_contact)
            self.assertFalse(header_field.is_valid)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_contact)
            self.assertFalse(header_field.is_valid)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.is_contact)
            self.assertFalse(header_field.is_valid)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_contact)
            self.assertFalse(header_field.is_valid)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_content_disposition)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_content_disposition)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_content_disposition)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_content_disposition)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_content_type)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_content_type)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_content_type)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_content_type)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.is_content_type)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_content_type)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_date)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_date)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_date)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_date)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_expires)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_expires)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_expires)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_expires)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_from)
            self.assertTrue(header_field.is_valid)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_from)
            self.assertTrue(header_field.is_valid)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_from)
            self.assertFalse(header_field.is_valid)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_from)
            self.assertFalse(header_field.is_valid)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.is_from)
            self.assertFalse(header_field.is_valid)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_from)
            self.assertFalse(header_field.is_valid)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_max_forwards)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_max_forwards)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_max_forwards)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_max_forwards)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_record_route)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_record_route)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_record_route)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_record_route)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_require)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_require)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_require)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_require)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_retry_after)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_retry_after)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_retry_after)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_retry_after)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_route)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_route)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_route)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_route)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_server)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_server)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_server)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_server)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_session_expires)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_session_expires)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_session_expires)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_session_expires)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_supported)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_supported)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_supported)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_supported)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.is_supported)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_supported)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_timestamp)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_timestamp)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_timestamp)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_timestamp)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_to)
            self.assertTrue(header_field.is_valid)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_to)
            self.assertTrue(header_field.is_valid)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_to)
            self.assertFalse(header_field.is_valid)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_to)
            self.assertFalse(header_field.is_valid)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.is_to)
            self.assertFalse(header_field.is_valid)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_to)
            self.assertFalse(header_field.is_valid)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_user_agent)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_user_agent)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_user_agent)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_user_agent)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_www_authenticate)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_www_authenticate)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_www_authenticate)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_www_authenticate)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_warning)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_warning)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_warning)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_warning)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_subject)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_subject)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_subject)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_subject)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.is_subject)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_subject)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_referred_by)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_referred_by)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_referred_by)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_referred_by)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.is_referred_by)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_referred_by)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_refer_to)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_refer_to)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_refer_to)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_refer_to)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.is_refer_to)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_refer_to)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_allow_events)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_allow_events)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_allow_events)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_allow_events)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.is_allow_events)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_allow_events)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_event)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_event)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_event)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_event)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_content_encoding)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_content_encoding)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_content_encoding)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_content_encoding)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.is_content_encoding)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_content_encoding)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_rack)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_rack)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_rack)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_rack)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_p_charge)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_p_charge)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_p_charge)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_p_charge)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_reply_to)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_reply_to)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_reply_to)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_reply_to)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_unsupported)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_unsupported)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_unsupported)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_unsupported)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_p_asserted_identity)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_p_asserted_identity)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_p_asserted_identity)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_p_asserted_identity)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_p_preferred_identity)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_p_preferred_identity)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_p_preferred_identity)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_p_preferred_identity)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_remote_party_id)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_remote_party_id)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_remote_party_id)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_remote_party_id)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_alert_info)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_alert_info)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_alert_info)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_alert_info)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_history_info)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_history_info)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_history_info)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_history_info)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_p_called_party_id)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_p_called_party_id)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_p_called_party_id)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_p_called_party_id)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_p_rtp_stat)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_p_rtp_stat)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_p_rtp_stat)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_p_rtp_stat)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_privacy)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_privacy)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_privacy)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_privacy)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_proxy_authenticate)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_proxy_authenticate)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_proxy_authenticate)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_proxy_authenticate)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_proxy_authorization)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_proxy_authorization)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_proxy_authorization)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_proxy_authorization)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_proxy_require)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_proxy_require)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_proxy_require)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_proxy_require)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_reason)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_reason)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_reason)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_reason)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_record_session_expires)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_record_session_expires)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_record_session_expires)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_record_session_expires)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_replaces)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_replaces)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_replaces)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_replaces)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_subscription_state)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_subscription_state)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_subscription_state)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_subscription_state)


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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_min_expires)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_min_expires)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_min_expires)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_min_expires)


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
    #         header_field = SIPHeaderFieldFactory().next_for_string(line)
    #         self.assertTrue(header_field.is_via)
    #         stringio = StringIO(line + '\r\n')
    #         header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
    #         self.assertTrue(header_field.is_via)
    #         stringio.close()
    #         header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
    #         self.assertTrue(header_field.is_via)
    #         header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
    #         self.assertTrue(header_field.is_via)
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
            header_field = SIPHeaderFieldFactory().next_for_string(line)
            self.assertTrue(header_field.is_via)
            self.assertTrue(header_field.is_valid)
            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]
            self.assertTrue(header_field.is_via)
            self.assertTrue(header_field.is_valid)
            stringio.close()
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(header_field.is_via)
            self.assertFalse(header_field.is_valid)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_via)
            self.assertFalse(header_field.is_valid)
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
            self.assertTrue(header_field.is_via)
            self.assertFalse(header_field.is_valid)
            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")
            self.assertTrue(header_field.is_via)
            self.assertFalse(header_field.is_valid)
