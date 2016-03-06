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
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isCallInfo)


class TestContactSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Contact', 'CONTACT', 'contact']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ContactSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isContact, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isContact)


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
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isExpires)


class TestFromSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['From', 'FROM', 'from']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return FromSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isFrom, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isFrom)


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
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isMaxForwards)

class TestRecordRouteSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Record-Route', 'RECORD-Route', 'record-route', 'Record-route', 'record-Route']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RecordRouteSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isRecordRoute, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isRecordRoute)


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
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isRetryAfter)


class TestRouteSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Route', 'ROUTE', 'route']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return RouteSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isRoute, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isRoute)


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
                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isTimestamp)

class TestToSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['To', 'TO', 'to']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ToSIPHeaderField

    # TODO:  way more test samples and assertions.  Lots of overridden canonicalFieldValues.
    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isTo, line)

    # TODO:  way more test samples.  Lots of overridden canonicalFieldValues.
    def test_rendering(self):
        pass
        headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(tag=None, displayName=None, sipURI=SIPURI.newParsedFrom('sip:example.com:5061'))
        # TODO: Now do a bunch of testing on this shiz.

        '''
        for fieldValueString in self.canonicalFieldValues:
            headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
            self.assertTrue(headerField.isValid)
            self.assertTrue(headerField.isKnown)
            self.assertEqual(headerField.rawString, self.canonicalFieldNames[0] + ': ' + fieldValueString)
            headerField.fieldValueString = "blooey"
            self.assertEqual("blooey", headerField.fieldValueString)
            self.assertEqual(headerField.rawString, self.canonicalFieldNames[0] + ': blooey')
        '''
        '''
        GENERIC, do not use.
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isTo)
        '''

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
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isWarning)


class TestViaSipHeaderField(AbstractSIPHeaderFieldTestCase):
    @property
    def canonicalFieldNames(self):
        return['Via', 'VIA', 'via']

    @property
    def sipHeaderFieldClassUnderTest(self):
        return ViaSIPHeaderField

    def test_parsing(self):
        self.basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isVia, line)

    def test_rendering(self):
        self.basic_test_rendering()
        for fieldName in self.canonicalFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
                self.assertTrue(headerField.isVia)
