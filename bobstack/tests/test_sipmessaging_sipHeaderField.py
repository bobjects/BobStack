from unittest import TestCase
# import sys
# sys.path.append("..")
from abstractSIPHeaderFieldTestCase import AbstractSIPHeaderFieldTestCase
from abstractIntegerSIPHeaderFieldTestCase import AbstractIntegerSIPHeaderFieldTestCase
from ..sipmessaging import SIPURI
from ..sipmessaging import UnknownSIPHeaderField
from ..sipmessaging import ContentLengthSIPHeaderField
from ..sipmessaging import AcceptSIPHeaderField
from ..sipmessaging import AcceptEncodingSIPHeaderField
from ..sipmessaging import AcceptLanguageSIPHeaderField
from ..sipmessaging import AllowSIPHeaderField
from ..sipmessaging import AuthorizationSIPHeaderField
from ..sipmessaging import CSeqSIPHeaderField
from ..sipmessaging import CallIDSIPHeaderField
from ..sipmessaging import CallInfoSIPHeaderField
from ..sipmessaging import ContactSIPHeaderField
from ..sipmessaging import ContentDispositionSIPHeaderField
from ..sipmessaging import ContentTypeSIPHeaderField
from ..sipmessaging import DateSIPHeaderField
from ..sipmessaging import ExpiresSIPHeaderField
from ..sipmessaging import FromSIPHeaderField
from ..sipmessaging import MaxForwardsSIPHeaderField
from ..sipmessaging import RecordRouteSIPHeaderField
from ..sipmessaging import RequireSIPHeaderField
from ..sipmessaging import RetryAfterSIPHeaderField
from ..sipmessaging import RouteSIPHeaderField
from ..sipmessaging import ServerSIPHeaderField
from ..sipmessaging import SessionExpiresSIPHeaderField
from ..sipmessaging import SupportedSIPHeaderField
from ..sipmessaging import TimestampSIPHeaderField
from ..sipmessaging import ToSIPHeaderField
from ..sipmessaging import UserAgentSIPHeaderField
from ..sipmessaging import ViaSIPHeaderField
from ..sipmessaging import WWWAuthenticateSIPHeaderField
from ..sipmessaging import WarningSIPHeaderField
from ..sipmessaging import SubjectSIPHeaderField
from ..sipmessaging import ReferredBySIPHeaderField
from ..sipmessaging import ReferToSIPHeaderField
from ..sipmessaging import AllowEventsSIPHeaderField
from ..sipmessaging import EventSIPHeaderField
from ..sipmessaging import ContentEncodingSIPHeaderField
from ..sipmessaging import RAckSIPHeaderField
from ..sipmessaging import PChargeSIPHeaderField
from ..sipmessaging import ReplyToSIPHeaderField
from ..sipmessaging import UnsupportedSIPHeaderField
from ..sipmessaging import PAssertedIdentitySIPHeaderField
from ..sipmessaging import PPreferredIdentitySIPHeaderField
from ..sipmessaging import RemotePartyIDSIPHeaderField
from ..sipmessaging import AlertInfoSIPHeaderField
from ..sipmessaging import HistoryInfoSIPHeaderField
from ..sipmessaging import PCalledPartyIdSIPHeaderField
from ..sipmessaging import PRTPStatSIPHeaderField
from ..sipmessaging import PrivacySIPHeaderField
from ..sipmessaging import ProxyAuthenticateSIPHeaderField
from ..sipmessaging import ProxyAuthorizationSIPHeaderField
from ..sipmessaging import ProxyRequireSIPHeaderField
from ..sipmessaging import ReasonSIPHeaderField
from ..sipmessaging import RecordSessionExpiresSIPHeaderField
from ..sipmessaging import ReplacesSIPHeaderField
from ..sipmessaging import SubscriptionStateSIPHeaderField
from ..sipmessaging import MinExpiresSIPHeaderField


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
            self.assertFalse(UnknownSIPHeaderField.can_match_string(line))
            self.assertFalse(ContentLengthSIPHeaderField.can_match_string(line))
            header_field = UnknownSIPHeaderField.new_parsed_from(line)
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
            self.assertIsInstance(header_field.field_name, basestring)
            self.assertIsInstance(header_field.field_value_string, basestring)


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_content_length, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_content_length)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_content_length)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_content_length)

    def testIANAStandardParameters(self):
        # TODO
        pass


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_accept, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_accept)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_accept)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_accept)

    def testIANAStandardParameters(self):
        # TODO
        pass


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_accept_encoding, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_accept_encoding)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_accept_encoding)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_accept_encoding)

    def testIANAStandardParameters(self):
        # TODO
        pass


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_accept_language, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_accept_language)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_accept_language)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_accept_language)

    def testIANAStandardParameters(self):
        # TODO
        pass


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_allow, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_allow)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_allow)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_allow)


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_authorization, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_authorization)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_authorization)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_authorization)

    def testIANAStandardParameters(self):
        # TODO
        pass


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_cseq, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_cseq)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_cseq)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_cseq)


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_call_id, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_call_id)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_call_id)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_call_id)


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_call_info, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_call_info)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_call_info)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_call_info)

    def testIANAStandardParameters(self):
        # TODO
        pass


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
        header_field_string = 'Contact: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;expires=1000'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'expires': '1000'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')
        header_field.display_name = 'foo'
        self.assertEqual(header_field.raw_string, 'Contact: "foo"<sip:3122221000@200.23.3.241:5061;user=phone>;expires=1000')
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.display_name, 'foo')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'expires': '1000'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')
        header_field.sip_uri = SIPURI.new_parsed_from('sip:0.0.0.0')
        self.assertEqual(header_field.raw_string, 'Contact: "foo"<sip:0.0.0.0>;expires=1000')
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.display_name, 'foo')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'expires': '1000'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:0.0.0.0')
        self.assertEqual(header_field.sip_uri.host, '0.0.0.0')
        self.assertEqual(header_field.sip_uri.port, None)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.user, None)

    def test_parseValid001(self):
        header_field_string = 'Contact: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid002(self):
        header_field_string = 'Contact: <sip:3122221000@200.23.3.241:5061;user=phone>'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.display_name, '')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid003(self):
        header_field_string = 'Contact: "3122221000"<sip:200.23.3.241:5061;user=phone>'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, None)

    def test_parseValid004(self):
        header_field_string = 'Contact: "3122221000"<sip:3122221000@200.23.3.241;user=phone>'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, None)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid005(self):
        header_field_string = 'Contact: "3122221000"<sip:3122221000@200.23.3.241:5061>'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid006(self):
        header_field_string = 'Contact: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid007(self):
        header_field_string = 'Contact: <sip:3122221000@200.23.3.241:5061;user=phone>'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.display_name, '')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid008(self):
        header_field_string = 'Contact: sip:3122221000@200.23.3.241:5061'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.display_name, None)
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_contact, line)

    def test_rendering(self):
        header_field_string = 'Contact: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>'
        header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(display_name='3122221000', sip_uri=SIPURI.new_parsed_from('sip:3122221000@200.23.3.241:5061;user=phone'))
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.display_name, '3122221000')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def testIANAStandardParameters(self):
        # TODO
        pass


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_content_disposition, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_content_disposition)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_content_disposition)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_content_disposition)

    def testIANAStandardParameters(self):
        # TODO
        pass


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_content_type, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_content_type)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_content_type)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_content_type)


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_date, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_date)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_date)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_date)


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_expires, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_expires)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_expires)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_expires)


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
        header_field_string = 'From: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')
        header_field.display_name = 'foo'
        self.assertEqual(header_field.raw_string, 'From: "foo"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(header_field.display_name, 'foo')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')
        header_field.tag = 'TESTTAG'
        self.assertEqual(header_field.raw_string, 'From: "foo"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=TESTTAG')
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, 'TESTTAG')
        self.assertEqual(header_field.display_name, 'foo')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': 'TESTTAG'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')
        header_field.sip_uri = SIPURI.new_parsed_from('sip:0.0.0.0')
        self.assertEqual(header_field.raw_string, 'From: "foo"<sip:0.0.0.0>;tag=TESTTAG')
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, 'TESTTAG')
        self.assertEqual(header_field.display_name, 'foo')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': 'TESTTAG'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:0.0.0.0')
        self.assertEqual(header_field.sip_uri.host, '0.0.0.0')
        self.assertEqual(header_field.sip_uri.port, None)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.user, None)

    def test_parseValid001(self):
        header_field_string = 'From: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid002(self):
        header_field_string = 'From: <sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(header_field.display_name, '')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid003(self):
        header_field_string = 'From: "3122221000"<sip:200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, None)

    def test_parseValid004(self):
        header_field_string = 'From: "3122221000"<sip:3122221000@200.23.3.241;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, None)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid005(self):
        header_field_string = 'From: "3122221000"<sip:3122221000@200.23.3.241:5061>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid006(self):
        header_field_string = 'From: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, None)
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid007(self):
        header_field_string = 'From: <sip:3122221000@200.23.3.241:5061;user=phone>'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, None)
        self.assertEqual(header_field.display_name, '')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid008(self):
        header_field_string = 'From: sip:3122221000@200.23.3.241:5061'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, None)
        self.assertEqual(header_field.display_name, None)
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_from, line)

    def test_rendering(self):
        header_field_string = 'From: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(display_name='3122221000', tag='29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875', sip_uri=SIPURI.new_parsed_from('sip:3122221000@200.23.3.241:5061;user=phone'))
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(header_field.display_name, '3122221000')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_tagGeneration(self):
        header_field_string = 'From: sip:3122221000@200.23.3.241:5061'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.tag, None)
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        header_field.generate_tag()
        self.assertIsInstance(header_field.tag, basestring)
        self.assertTrue('tag' in header_field.parameter_names_and_value_strings)

    def testIANAStandardParameters(self):
        # TODO
        pass


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_max_forwards, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_max_forwards)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_max_forwards)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_max_forwards)


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
        header_field_string = 'Record-Route: <sip:3122221000@200.23.3.241:5061;transport=TLS>'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;transport=TLS')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        header_field.sip_uri = SIPURI.new_parsed_from('sip:0.0.0.0')
        self.assertEqual(header_field.raw_string, 'Record-Route: <sip:0.0.0.0>')
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:0.0.0.0')
        self.assertEqual(header_field.sip_uri.host, '0.0.0.0')
        self.assertEqual(header_field.sip_uri.port, None)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_record_route)

    def test_rendering(self):
        header_field_string = 'Record-Route: <sip:3122221000@200.23.3.241:5061;transport=TLS>'
        header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(sip_uri=SIPURI.new_parsed_from('sip:3122221000@200.23.3.241:5061;transport=TLS'))
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;transport=TLS')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.user, '3122221000')


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_require, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_require)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_require)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_require)


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_retry_after, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_retry_after)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_retry_after)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_retry_after)

    def testIANAStandardParameters(self):
        # TODO
        pass


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
        header_field_string = 'Route: <sip:3122221000@200.23.3.241:5061;transport=TLS>'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;transport=TLS')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        header_field.sip_uri = SIPURI.new_parsed_from('sip:0.0.0.0')
        self.assertEqual(header_field.raw_string, 'Route: <sip:0.0.0.0>')
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:0.0.0.0')
        self.assertEqual(header_field.sip_uri.host, '0.0.0.0')
        self.assertEqual(header_field.sip_uri.port, None)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_route)

    def test_rendering(self):
        header_field_string = 'Route: <sip:3122221000@200.23.3.241:5061;transport=TLS>'
        header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(sip_uri=SIPURI.new_parsed_from('sip:3122221000@200.23.3.241:5061;transport=TLS'))
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;transport=TLS')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.user, '3122221000')


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_server, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_server)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_server)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_server)


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_session_expires, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_session_expires)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_session_expires)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_session_expires)


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_supported, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_supported)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_supported)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_supported)


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_timestamp, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_timestamp)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_timestamp)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_timestamp)


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
        header_field_string = 'To: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')
        header_field.display_name = 'foo'
        self.assertEqual(header_field.raw_string, 'To: "foo"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(header_field.display_name, 'foo')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')
        header_field.tag = 'TESTTAG'
        self.assertEqual(header_field.raw_string, 'To: "foo"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=TESTTAG')
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, 'TESTTAG')
        self.assertEqual(header_field.display_name, 'foo')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': 'TESTTAG'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')
        header_field.sip_uri = SIPURI.new_parsed_from('sip:0.0.0.0')
        self.assertEqual(header_field.raw_string, 'To: "foo"<sip:0.0.0.0>;tag=TESTTAG')
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, 'TESTTAG')
        self.assertEqual(header_field.display_name, 'foo')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': 'TESTTAG'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:0.0.0.0')
        self.assertEqual(header_field.sip_uri.host, '0.0.0.0')
        self.assertEqual(header_field.sip_uri.port, None)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.user, None)

    def test_parseValid001(self):
        header_field_string = 'To: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid002(self):
        header_field_string = 'To: <sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(header_field.display_name, '')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid003(self):
        header_field_string = 'To: "3122221000"<sip:200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, None)

    def test_parseValid004(self):
        header_field_string = 'To: "3122221000"<sip:3122221000@200.23.3.241;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, None)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid005(self):
        header_field_string = 'To: "3122221000"<sip:3122221000@200.23.3.241:5061>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid006(self):
        header_field_string = 'To: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, None)
        self.assertEqual(header_field.display_name, '"3122221000"')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid007(self):
        header_field_string = 'To: <sip:3122221000@200.23.3.241:5061;user=phone>'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, None)
        self.assertEqual(header_field.display_name, '')
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parseValid008(self):
        header_field_string = 'To: sip:3122221000@200.23.3.241:5061'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, None)
        self.assertEqual(header_field.display_name, None)
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_to, line)

    def test_rendering(self):
        header_field_string = 'To: "3122221000"<sip:3122221000@200.23.3.241:5061;user=phone>;tag=29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'
        header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(display_name='3122221000', tag='29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875', sip_uri=SIPURI.new_parsed_from('sip:3122221000@200.23.3.241:5061;user=phone'))
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.tag, '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875')
        self.assertEqual(header_field.display_name, '3122221000')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'tag': '29de2c8-f0a1ec8-13c5-50029-98875-169ed655-98875'})
        self.assertEqual(header_field.sip_uri.raw_string, 'sip:3122221000@200.23.3.241:5061;user=phone')
        self.assertEqual(header_field.sip_uri.host, '200.23.3.241')
        self.assertEqual(header_field.sip_uri.port, 5061)
        self.assertEqual(header_field.sip_uri.scheme, 'sip')
        self.assertEqual(header_field.sip_uri.parameter_names_and_value_strings, {'user': 'phone'})
        self.assertEqual(header_field.sip_uri.user, '3122221000')

    def test_tagGeneration(self):
        header_field_string = 'To: sip:3122221000@200.23.3.241:5061'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.tag, None)
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        header_field.generate_tag()
        self.assertIsInstance(header_field.tag, basestring)
        self.assertTrue('tag' in header_field.parameter_names_and_value_strings)

    def testIANAStandardParameters(self):
        # TODO
        pass


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_user_agent, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_user_agent)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_user_agent)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_user_agent)


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_www_authenticate, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_www_authenticate)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_www_authenticate)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_www_authenticate)

    def testIANAStandardParameters(self):
        # TODO
        pass


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
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_warning, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_warning)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_warning)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_warning)


class TestSubjectSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Subject', 'SUBJECT', 'subject']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return SubjectSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_subject, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_subject)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_subject)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_subject)


class TestReferredBySIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Referred-By', 'REFERRED-BY', 'referred-by']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ReferredBySIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_referred_by, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_referred_by)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_referred_by)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_referred_by)


class TestReferToSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Refer-To', 'REFER-TO', 'refer-to']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ReferToSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_refer_to, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_refer_to)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_refer_to)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_refer_to)


class TestAllowEventsSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Allow-Events', 'ALLOW-EVENTS', 'allow-events']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return AllowEventsSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_allow_events, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_allow_events)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_allow_events)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_allow_events)


class TestEventSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Event', 'EVENT', 'event']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return EventSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_event, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_event)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_event)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_event)

    def testIANAStandardParameters(self):
        # TODO
        pass


class TestContentEncodingSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Content-Encoding', 'CONTENT-ENCODING', 'content-encoding']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ContentEncodingSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_content_encoding, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_content_encoding)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_content_encoding)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_content_encoding)


class TestRAckSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['RAck', 'RACK', 'rack']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RAckSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_rack, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_rack)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_rack)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_rack)


class TestPChargeSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['P-Charge', 'P-CHARGE', 'p-charge']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return PChargeSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_p_charge, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_p_charge)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_p_charge)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_p_charge)


class TestReplyToSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Reply-To', 'REPLY-TO', 'reply-to']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ReplyToSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_reply_to, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_reply_to)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_reply_to)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_reply_to)


class TestUnsupportedSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Unsupported', 'UNSUPPORTED', 'unsupported']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return UnsupportedSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_unsupported, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_unsupported)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_unsupported)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_unsupported)


class TestPAssertedIdentitySIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['P-Asserted-Identity', 'P-ASSERTED-IDENTITY', 'p-asserted-identity']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return PAssertedIdentitySIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_p_asserted_identity, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_p_asserted_identity)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_p_asserted_identity)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_p_asserted_identity)


class TestPPreferredIdentitySIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['P-Preferred-Identity', 'P-PREFERRED-IDENTITY', 'p-preferred-identity']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return PPreferredIdentitySIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_p_preferred_identity, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_p_preferred_identity)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_p_preferred_identity)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_p_preferred_identity)


class TestRemotePartyIDSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Remote-Party-ID', 'REMOTE-PARTY-ID', 'remote-party-id']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RemotePartyIDSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_remote_party_id, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_remote_party_id)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_remote_party_id)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_remote_party_id)


class TestAlertInfoSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Alert-Info', 'ALERT-INFO', 'alert-info']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return AlertInfoSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_alert_info, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_alert_info)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_alert_info)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_alert_info)

    def testIANAStandardParameters(self):
        # TODO
        pass


class TestHistoryInfoSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['History-Info', 'HISTORY-INFO', 'history-info']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return HistoryInfoSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_history_info, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_history_info)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_history_info)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_history_info)

    def testIANAStandardParameters(self):
        # TODO
        pass


class TestPCalledPartyIdSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['P-Called-Party-Id', 'P-CALLED-PARTY-ID', 'p-called-party-id']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return PCalledPartyIdSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_p_called_party_id, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_p_called_party_id)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_p_called_party_id)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_p_called_party_id)


class TestPRTPStatSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['P-RTP-Stat', 'P-RTP-STAT', 'p-rtp-stat']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return PRTPStatSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_p_rtp_stat, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_p_rtp_stat)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_p_rtp_stat)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_p_rtp_stat)


class TestPrivacySIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Privacy', 'PRIVACY', 'privacy']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return PrivacySIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_privacy, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_privacy)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_privacy)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_privacy)


class TestProxyAuthenticateSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Proxy-Authenticate', 'PROXY-AUTHENTICATE', 'proxy-authenticate']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ProxyAuthenticateSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_proxy_authenticate, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_proxy_authenticate)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_proxy_authenticate)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_proxy_authenticate)

    def testIANAStandardParameters(self):
        # TODO
        pass


class TestProxyAuthorizationSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Proxy-Authorization', 'PROXY-AUTHORIZATION', 'proxy-authorization']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ProxyAuthorizationSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_proxy_authorization, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_proxy_authorization)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_proxy_authorization)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_proxy_authorization)

    def testIANAStandardParameters(self):
        # TODO
        pass


class TestProxyRequireSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Proxy-Require', 'PROXY-REQUIRE', 'proxy-require']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ProxyRequireSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_proxy_require, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_proxy_require)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_proxy_require)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_proxy_require)


class TestReasonSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Reason', 'REASON', 'reason']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ReasonSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_reason, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_reason)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_reason)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_reason)

    def testIANAStandardParameters(self):
        # TODO
        pass


class TestRecordSessionExpiresSIPHeaderField(AbstractIntegerSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Record-Session-Expires', 'RECORD-SESSION-EXPIRES', 'record-session-expires']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RecordSessionExpiresSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_record_session_expires, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_record_session_expires)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_record_session_expires)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_record_session_expires)


class TestReplacesSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Replaces', 'REPLACES', 'replaces']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ReplacesSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_replaces, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_replaces)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_replaces)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_replaces)


class TestSubscriptionStateSIPHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Subscription-State', 'SUBSCRIPTION-STATE', 'subscription-state']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return SubscriptionStateSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_subscription_state, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_subscription_state)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_subscription_state)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
                self.assertTrue(header_field.is_subscription_state)


class TestMinExpiresSIPHeaderField(AbstractIntegerSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Min-Expires', 'MIN-EXPIRES', 'min-expires']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return MinExpiresSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_min_expires, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for field_name in self.canonicalFieldNames:
            # TODO:  we will extend this once we render compact headers.
            for field_value_string in self.canonicalFieldValues:
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
                self.assertTrue(header_field.is_min_expires)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_min_expires)
                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_value_string=field_value_string)
                self.assertTrue(header_field.is_min_expires)


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
        header_field_string = 'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(header_field.transport, 'TLS')
        self.assertEqual(header_field.host, '200.25.3.150')
        self.assertEqual(header_field.port, None)
        header_field.host = '192.168.0.5'
        self.assertEqual(header_field.raw_string, 'Via: SIP/2.0/TLS 192.168.0.5;branch=z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(header_field.transport, 'TLS')
        self.assertEqual(header_field.host, '192.168.0.5')
        self.assertEqual(header_field.port, None)
        header_field.port = 5061
        self.assertEqual(header_field.raw_string, 'Via: SIP/2.0/TLS 192.168.0.5:5061;branch=z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(header_field.transport, 'TLS')
        self.assertEqual(header_field.host, '192.168.0.5')
        self.assertEqual(header_field.port, 5061)
        header_field.transport = 'UDP'
        self.assertEqual(header_field.raw_string, 'Via: SIP/2.0/UDP 192.168.0.5:5061;branch=z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(header_field.transport, 'UDP')
        self.assertEqual(header_field.host, '192.168.0.5')
        self.assertEqual(header_field.port, 5061)
        header_field.branch = 'z9hG4bKblarg'
        self.assertEqual(header_field.raw_string, 'Via: SIP/2.0/UDP 192.168.0.5:5061;branch=z9hG4bKblarg')
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.branch, 'z9hG4bKblarg')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'branch': 'z9hG4bKblarg'})
        self.assertEqual(header_field.transport, 'UDP')
        self.assertEqual(header_field.host, '192.168.0.5')
        self.assertEqual(header_field.port, 5061)

    def test_parseValid001(self):
        header_field_string = 'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(header_field.transport, 'TLS')
        self.assertEqual(header_field.host, '200.25.3.150')
        self.assertEqual(header_field.port, None)

    def test_parseValid002(self):
        header_field_string = 'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(header_field.transport, 'TLS')
        self.assertEqual(header_field.host, '200.25.3.150')
        self.assertEqual(header_field.port, None)

    def test_parseValid003(self):
        header_field_string = 'Via: SIP/2.0/TLS 192.168.0.5:5061;branch=z9hG4bK0ee8d3e272e31ca195299efc500'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(header_field.transport, 'TLS')
        self.assertEqual(header_field.host, '192.168.0.5')
        self.assertEqual(header_field.port, 5061)

    def test_parseValid004(self):
        header_field_string = 'Via: SIP/2.0/UDP 192.168.0.5:5061;branch=z9hG4bK0ee8d3e272e31ca195299efc500'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(header_field.transport, 'UDP')
        self.assertEqual(header_field.host, '192.168.0.5')
        self.assertEqual(header_field.port, 5061)

    def test_parseValid005(self):
        header_field_string = 'Via: SIP/2.0/UDP 192.168.0.5:5061;branch=z9hG4bKblarg'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.branch, 'z9hG4bKblarg')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'branch': 'z9hG4bKblarg'})
        self.assertEqual(header_field.transport, 'UDP')
        self.assertEqual(header_field.host, '192.168.0.5')
        self.assertEqual(header_field.port, 5061)

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.is_via, line)

    def test_rendering(self):
        header_field_string = 'Via: SIP/2.0/UDP 192.168.0.5:5061;branch=z9hG4bK0ee8d3e272e31ca195299efc500'
        header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(host='192.168.0.5', port=5061, transport='UDP', branch='z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(header_field.raw_string, header_field_string)
        self.assertTrue(header_field.is_valid)
        self.assertEqual(header_field.branch, 'z9hG4bK0ee8d3e272e31ca195299efc500')
        self.assertEqual(header_field.parameter_names_and_value_strings, {'branch': 'z9hG4bK0ee8d3e272e31ca195299efc500'})
        self.assertEqual(header_field.transport, 'UDP')
        self.assertEqual(header_field.host, '192.168.0.5')
        self.assertEqual(header_field.port, 5061)
        self.assertIsInstance(header_field.branch, basestring)

    def test_branchGeneration(self):
        header_field_string = 'Via: SIP/2.0/UDP 192.168.0.5:5061'
        header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(header_field_string)
        self.assertTrue(header_field.is_via)
        self.assertEqual(header_field.branch, None)
        self.assertEqual(header_field.parameter_names_and_value_strings, {})
        header_field.generate_branch()
        self.assertIsInstance(header_field.branch, basestring)
        self.assertTrue('branch' in header_field.parameter_names_and_value_strings)

    def testIANAStandardParameters(self):
        # TODO
        pass
