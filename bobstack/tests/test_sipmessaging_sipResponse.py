from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging import SIPResponse
from sipmessaging import SIPHeader
from sipmessaging import ContentLengthSIPHeaderField
from sipmessaging import ViaSIPHeaderField
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
from sipmessaging import WWWAuthenticateSIPHeaderField
from sipmessaging import WarningSIPHeaderField
from sipmessaging import UnknownSIPHeaderField
# from sipmessaging.sipResponseStartLine import SIPResponseStartLine


class TestSIPResponse(TestCase):
    @property
    def canonicalStrings(self):
        return [
            ('SIP/2.0 100 Trying\r\n'
             'From: "3125551212"<sip:3125551212@example.com:5064;user=phone>;tag=e95a00000022137fe518\r\n'
             'To: "3125551313"<sip:3125551313@example.com:5064;user=phone>\r\n'
             'Call-ID: a12d6210342b0183745ef9750992682d90d7edce@200.23.3.241\r\n'
             'CSeq: 615 INVITE\r\n'
             'Via: SIP/2.0/UDP 200.23.3.241:5064;received=200.30.10.15;branch=z9hG4bK-3f04bd-f62a8381-4ebadacb-0x692748a8\r\n'
             'Content-Length: 11\r\n'
             '\r\n'
             'Foo Content')
        ]

    def test_parsing(self):
        for messageString in self.canonicalStrings:
            response = SIPResponse.newParsedFrom(messageString)
            self.runAssertionsForResponse(response)

    def test_rendering_from_list_of_header_fields(self):
        headerFields = [
            FromSIPHeaderField.newForAttributes(fieldName='From', fieldValue='"3125551212"<sip:3125551212@example.com:5064;user=phone>;tag=e95a00000022137fe518'),
            ToSIPHeaderField.newForAttributes(fieldName='To', fieldValue='"3125551313"<sip:3125551313@example.com:5064;user=phone>'),
            CallIDSIPHeaderField.newForAttributes(fieldName='Call-ID', fieldValue='a12d6210342b0183745ef9750992682d90d7edce@200.23.3.241'),
            CSeqSIPHeaderField.newForAttributes(fieldName='CSeq', fieldValue='615 INVITE'),
            # UnknownSIPHeaderField.newForAttributes(fieldName='Max-Forwards', fieldValue='70'),
            ViaSIPHeaderField.newForAttributes(fieldName='Via', fieldValue='SIP/2.0/UDP 200.23.3.241:5064;received=200.30.10.15;branch=z9hG4bK-3f04bd-f62a8381-4ebadacb-0x692748a8'),
            ContentLengthSIPHeaderField.newForAttributes(value=11)]
        response = SIPResponse.newForAttributes(statusCode=100, reasonPhrase='Trying', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForResponse(response)

    def test_rendering_from_one_big_header_strings(self):
        headerFields = ('From: "3125551212"<sip:3125551212@example.com:5064;user=phone>;tag=e95a00000022137fe518\r\n'
                        'To: "3125551313"<sip:3125551313@example.com:5064;user=phone>\r\n'
                        'Call-ID: a12d6210342b0183745ef9750992682d90d7edce@200.23.3.241\r\n'
                        'CSeq: 615 INVITE\r\n'
                        # 'Max-Forwards: 70\r\n'
                        'Via: SIP/2.0/UDP 200.23.3.241:5064;received=200.30.10.15;branch=z9hG4bK-3f04bd-f62a8381-4ebadacb-0x692748a8\r\n'
                        'Content-Length: 11')  # This last one actually instantiates a ContentLengthSIPHeaderField.
        response = SIPResponse.newForAttributes(statusCode=100, reasonPhrase='Trying', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForResponse(response)

    def test_rendering_from_list_of_header_field_strings(self):
        headerFields = ['From: "3125551212"<sip:3125551212@example.com:5064;user=phone>;tag=e95a00000022137fe518',
                        'To: "3125551313"<sip:3125551313@example.com:5064;user=phone>',
                        'Call-ID: a12d6210342b0183745ef9750992682d90d7edce@200.23.3.241',
                        'CSeq: 615 INVITE',
                        # 'Max-Forwards: 70',
                        'Via: SIP/2.0/UDP 200.23.3.241:5064;received=200.30.10.15;branch=z9hG4bK-3f04bd-f62a8381-4ebadacb-0x692748a8',
                        'Content-Length: 11']  # This last one actually instantiates a ContentLengthSIPHeaderField.
        response = SIPResponse.newForAttributes(statusCode=100, reasonPhrase='Trying', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForResponse(response)

    def test_rendering_from_list_of_field_names_and_values(self):
        headerFields = [('From', '"3125551212"<sip:3125551212@example.com:5064;user=phone>;tag=e95a00000022137fe518'),
                        ('To', '"3125551313"<sip:3125551313@example.com:5064;user=phone>'),
                        ('Call-ID', 'a12d6210342b0183745ef9750992682d90d7edce@200.23.3.241'),
                        ('CSeq', '615 INVITE'),
                        # ('Max-Forwards', '70'),
                        ('Via', 'SIP/2.0/UDP 200.23.3.241:5064;received=200.30.10.15;branch=z9hG4bK-3f04bd-f62a8381-4ebadacb-0x692748a8'),
                        ('Content-Length', 11)]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        response = SIPResponse.newForAttributes(statusCode=100, reasonPhrase='Trying', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForResponse(response)

    def test_rendering_from_list_of_field_names_and_values_including_property_dict(self):
        headerFields = [('From', '"3125551212"<sip:3125551212@example.com:5064;user=phone>;tag=e95a00000022137fe518'),
                        ('To', '"3125551313"<sip:3125551313@example.com:5064;user=phone>'),
                        ('Call-ID', 'a12d6210342b0183745ef9750992682d90d7edce@200.23.3.241'),
                        ('CSeq', '615 INVITE'),
                        # ('Max-Forwards', '70'),
                        ('Via', 'SIP/2.0/UDP 200.23.3.241:5064;received=200.30.10.15;branch=z9hG4bK-3f04bd-f62a8381-4ebadacb-0x692748a8'),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        response = SIPResponse.newForAttributes(statusCode=100, reasonPhrase='Trying', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForResponse(response)

    def runAssertionsForResponse(self, aSIPResponse):
        self.assertEqual(aSIPResponse.rawString, self.canonicalStrings[0])
        self.assertTrue(aSIPResponse.isKnown)
        self.assertFalse(aSIPResponse.isUnknown)
        self.assertTrue(aSIPResponse.isValid)
        self.assertFalse(aSIPResponse.isRequest)
        self.assertTrue(aSIPResponse.isResponse)
        self.assertFalse(aSIPResponse.isACKRequest)
        self.assertFalse(aSIPResponse.isBYERequest)
        self.assertFalse(aSIPResponse.isCANCELRequest)
        self.assertFalse(aSIPResponse.isINFORequest)
        self.assertFalse(aSIPResponse.isINVITERequest)
        self.assertFalse(aSIPResponse.isNOTIFYRequest)
        self.assertFalse(aSIPResponse.isOPTIONSRequest)
        self.assertFalse(aSIPResponse.isREFERRequest)
        self.assertFalse(aSIPResponse.isREGISTERRequest)
        self.assertFalse(aSIPResponse.isSUBSCRIBERequest)
        self.assertFalse(aSIPResponse.isUPDATERequest)
        self.assertFalse(aSIPResponse.isMalformed)
        # self.assertEqual(1, [headerField for headerField in aSIPResponse.header.headerFields if headerField.isContentLength].__len__())
        # self.assertEqual(11, next(headerField for headerField in aSIPResponse.header.headerFields if headerField.isContentLength).value)
        # self.assertEqual(5, [headerField for headerField in aSIPResponse.header.headerFields if headerField.isUnknown].__len__())
        self.assertIsNotNone(aSIPResponse.header.contentLengthHeaderField)
        self.assertEqual(11, aSIPResponse.header.contentLength)
        self.assertEqual(1, aSIPResponse.header.viaHeaderFields.__len__())
        self.assertEqual(1, aSIPResponse.header.vias.__len__())
        self.assertEqual('SIP/2.0/UDP 200.23.3.241:5064;received=200.30.10.15;branch=z9hG4bK-3f04bd-f62a8381-4ebadacb-0x692748a8', aSIPResponse.header.vias[0])
        self.assertEqual(0, aSIPResponse.header.unknownHeaderFields.__len__())
        self.assertTrue(aSIPResponse.startLine.isResponse)
        self.assertFalse(aSIPResponse.startLine.isRequest)
        self.assertFalse(aSIPResponse.startLine.isMalformed)
        self.assertEqual('Foo Content', aSIPResponse.content)
        self.assertEqual(100, aSIPResponse.startLine.statusCode)
        self.assertEqual('Trying', aSIPResponse.startLine.reasonPhrase)



