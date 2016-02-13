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
             'Accept: application/sdp,application/isup,application/dtmf,application/dtmf-relay,multipart/mixed\r\n'
             'Accept-Encoding: x-nortel-short\r\n'
             'Accept-Language: en-us,fr-fr\r\n'
             'Allow:  ACK,BYE,CANCEL,INFO,INVITE,OPTIONS,REGISTER,SUBSCRIBE,UPDATE\r\n'
             'Authorization: Digest username="3122221000",realm="SomeRealm",nonce="1111790769596",uri="sip:3122211004@example.com",response="9bf77d8238664fe08dafd4d2abb6f1cb",algorithm=MD5\r\n'
             'Call-Info: <https://lsc14pa.example.com:443/pa/direct/pictureServlet?user=3126805100@example.com>;Purpose=icon\r\n'
             'Content-Disposition: session;handling=required\r\n'
             'Content-Type: application/sdp\r\n'
             'Date: Sat, 01 Feb 2014 22:07:34 GMT\r\n'
             'Record-Route: <sip:200.25.3.230:5061;transport=tls;lr>\r\n'
             'Require: sdp-anat\r\n'
             'Retry-After: 30\r\n'
             'Server: Blargomatic 2.0\r\n'
             'Session-Expires: 1200;refresher=uac\r\n'
             'Supported: 100rel,histinfo,join,replaces,sdp-anat,timer\r\n'
             'Timestamp: 1392061773\r\n'
             'WWW-Authenticate: Digest algorithm=MD5,nonce="1111790769596",realm="SomeRealm"\r\n'
             'Warning: 370 200.21.3.10 "Insufficient Bandwidth"\r\n'
             'X-RTP-Stat:  PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048\r\n'
             'x-channel:  ds/ds1-3/12;IP=132.52.127.16\r\n'
             'Referred-By: <sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"\r\n'
             'Refer-To: <sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>\r\n'
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
            FromSIPHeaderField.newForAttributes(fieldValue='"3125551212"<sip:3125551212@example.com:5064;user=phone>;tag=e95a00000022137fe518'),
            ToSIPHeaderField.newForAttributes(fieldValue='"3125551313"<sip:3125551313@example.com:5064;user=phone>'),
            CallIDSIPHeaderField.newForAttributes(fieldValue='a12d6210342b0183745ef9750992682d90d7edce@200.23.3.241'),
            CSeqSIPHeaderField.newForAttributes(fieldValue='615 INVITE'),
            # UnknownSIPHeaderField.newForAttributes(fieldValue='70'),
            ViaSIPHeaderField.newForAttributes(fieldValue='SIP/2.0/UDP 200.23.3.241:5064;received=200.30.10.15;branch=z9hG4bK-3f04bd-f62a8381-4ebadacb-0x692748a8'),
            AcceptSIPHeaderField.newForAttributes(fieldValue='application/sdp,application/isup,application/dtmf,application/dtmf-relay,multipart/mixed'),
            AcceptEncodingSIPHeaderField.newForAttributes(fieldValue='x-nortel-short'),
            AcceptLanguageSIPHeaderField.newForAttributes(fieldValue='en-us,fr-fr'),
            AllowSIPHeaderField.newForAttributes(fieldValue=' ACK,BYE,CANCEL,INFO,INVITE,OPTIONS,REGISTER,SUBSCRIBE,UPDATE'),
            AuthorizationSIPHeaderField.newForAttributes(fieldValue='Digest username="3122221000",realm="SomeRealm",nonce="1111790769596",uri="sip:3122211004@example.com",response="9bf77d8238664fe08dafd4d2abb6f1cb",algorithm=MD5'),
            CallInfoSIPHeaderField.newForAttributes(fieldValue='<https://lsc14pa.example.com:443/pa/direct/pictureServlet?user=3126805100@example.com>;Purpose=icon'),
            ContentDispositionSIPHeaderField.newForAttributes(fieldValue='session;handling=required'),
            ContentTypeSIPHeaderField.newForAttributes(fieldValue='application/sdp'),
            DateSIPHeaderField.newForAttributes(fieldValue='Sat, 01 Feb 2014 22:07:34 GMT'),
            RecordRouteSIPHeaderField.newForAttributes(fieldValue='<sip:200.25.3.230:5061;transport=tls;lr>'),
            RequireSIPHeaderField.newForAttributes(fieldValue='sdp-anat'),
            RetryAfterSIPHeaderField.newForAttributes(fieldValue='30'),
            ServerSIPHeaderField.newForAttributes(fieldValue='Blargomatic 2.0'),
            SessionExpiresSIPHeaderField.newForAttributes(fieldValue='1200;refresher=uac'),
            SupportedSIPHeaderField.newForAttributes(fieldValue='100rel,histinfo,join,replaces,sdp-anat,timer'),
            TimestampSIPHeaderField.newForAttributes(fieldValue='1392061773'),
            WWWAuthenticateSIPHeaderField.newForAttributes(fieldValue='Digest algorithm=MD5,nonce="1111790769596",realm="SomeRealm"'),
            WarningSIPHeaderField.newForAttributes(fieldValue='370 200.21.3.10 "Insufficient Bandwidth"'),
            UnknownSIPHeaderField.newForAttributes(fieldName='X-RTP-Stat', fieldValue=' PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048'),
            UnknownSIPHeaderField.newForAttributes(fieldName='x-channel', fieldValue=' ds/ds1-3/12;IP=132.52.127.16'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Referred-By', fieldValue='<sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Refer-To', fieldValue='<sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>'),
            ContentLengthSIPHeaderField.newForAttributes(value=11)]
        response = SIPResponse.newForAttributes(statusCode=100, reasonPhrase='Trying', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForResponse(response)

    def test_rendering_from_one_big_header_string(self):
        headerFields = ('From: "3125551212"<sip:3125551212@example.com:5064;user=phone>;tag=e95a00000022137fe518\r\n'
                        'To: "3125551313"<sip:3125551313@example.com:5064;user=phone>\r\n'
                        'Call-ID: a12d6210342b0183745ef9750992682d90d7edce@200.23.3.241\r\n'
                        'CSeq: 615 INVITE\r\n'
                        # 'Max-Forwards: 70\r\n'
                        'Via: SIP/2.0/UDP 200.23.3.241:5064;received=200.30.10.15;branch=z9hG4bK-3f04bd-f62a8381-4ebadacb-0x692748a8\r\n'
                        'Accept: application/sdp,application/isup,application/dtmf,application/dtmf-relay,multipart/mixed\r\n'
                        'Accept-Encoding: x-nortel-short\r\n'
                        'Accept-Language: en-us,fr-fr\r\n'
                        'Allow:  ACK,BYE,CANCEL,INFO,INVITE,OPTIONS,REGISTER,SUBSCRIBE,UPDATE\r\n'
                        'Authorization: Digest username="3122221000",realm="SomeRealm",nonce="1111790769596",uri="sip:3122211004@example.com",response="9bf77d8238664fe08dafd4d2abb6f1cb",algorithm=MD5\r\n'
                        'Call-Info: <https://lsc14pa.example.com:443/pa/direct/pictureServlet?user=3126805100@example.com>;Purpose=icon\r\n'
                        'Content-Disposition: session;handling=required\r\n'
                        'Content-Type: application/sdp\r\n'
                        'Date: Sat, 01 Feb 2014 22:07:34 GMT\r\n'
                        'Record-Route: <sip:200.25.3.230:5061;transport=tls;lr>\r\n'
                        'Require: sdp-anat\r\n'
                        'Retry-After: 30\r\n'
                        'Server: Blargomatic 2.0\r\n'
                        'Session-Expires: 1200;refresher=uac\r\n'
                        'Supported: 100rel,histinfo,join,replaces,sdp-anat,timer\r\n'
                        'Timestamp: 1392061773\r\n'
                        'WWW-Authenticate: Digest algorithm=MD5,nonce="1111790769596",realm="SomeRealm"\r\n'
                        'Warning: 370 200.21.3.10 "Insufficient Bandwidth"\r\n'
                        'X-RTP-Stat:  PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048\r\n'
                        'x-channel:  ds/ds1-3/12;IP=132.52.127.16\r\n'
                        'Referred-By: <sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"\r\n'
                        'Refer-To: <sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>\r\n'
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
                        'Accept: application/sdp,application/isup,application/dtmf,application/dtmf-relay,multipart/mixed',
                        'Accept-Encoding: x-nortel-short',
                        'Accept-Language: en-us,fr-fr',
                        'Allow:  ACK,BYE,CANCEL,INFO,INVITE,OPTIONS,REGISTER,SUBSCRIBE,UPDATE',
                        'Authorization: Digest username="3122221000",realm="SomeRealm",nonce="1111790769596",uri="sip:3122211004@example.com",response="9bf77d8238664fe08dafd4d2abb6f1cb",algorithm=MD5',
                        'Call-Info: <https://lsc14pa.example.com:443/pa/direct/pictureServlet?user=3126805100@example.com>;Purpose=icon',
                        'Content-Disposition: session;handling=required',
                        'Content-Type: application/sdp',
                        'Date: Sat, 01 Feb 2014 22:07:34 GMT',
                        'Record-Route: <sip:200.25.3.230:5061;transport=tls;lr>',
                        'Require: sdp-anat',
                        'Retry-After: 30',
                        'Server: Blargomatic 2.0',
                        'Session-Expires: 1200;refresher=uac',
                        'Supported: 100rel,histinfo,join,replaces,sdp-anat,timer',
                        'Timestamp: 1392061773',
                        'WWW-Authenticate: Digest algorithm=MD5,nonce="1111790769596",realm="SomeRealm"',
                        'Warning: 370 200.21.3.10 "Insufficient Bandwidth"',
                        'X-RTP-Stat:  PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048',
                        'x-channel:  ds/ds1-3/12;IP=132.52.127.16',
                        'Referred-By: <sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"',
                        'Refer-To: <sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>',
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
                        ('Accept', 'application/sdp,application/isup,application/dtmf,application/dtmf-relay,multipart/mixed'),
                        ('Accept-Encoding', 'x-nortel-short'),
                        ('Accept-Language', 'en-us,fr-fr'),
                        ('Allow', ' ACK,BYE,CANCEL,INFO,INVITE,OPTIONS,REGISTER,SUBSCRIBE,UPDATE'),
                        ('Authorization', 'Digest username="3122221000",realm="SomeRealm",nonce="1111790769596",uri="sip:3122211004@example.com",response="9bf77d8238664fe08dafd4d2abb6f1cb",algorithm=MD5'),
                        ('Call-Info', '<https://lsc14pa.example.com:443/pa/direct/pictureServlet?user=3126805100@example.com>;Purpose=icon'),
                        ('Content-Disposition', 'session;handling=required'),
                        ('Content-Type', 'application/sdp'),
                        ('Date', 'Sat, 01 Feb 2014 22:07:34 GMT'),
                        ('Record-Route', '<sip:200.25.3.230:5061;transport=tls;lr>'),
                        ('Require', 'sdp-anat'),
                        ('Retry-After', '30'),
                        ('Server', 'Blargomatic 2.0'),
                        ('Session-Expires', '1200;refresher=uac'),
                        ('Supported', '100rel,histinfo,join,replaces,sdp-anat,timer'),
                        ('Timestamp', '1392061773'),
                        ('WWW-Authenticate', 'Digest algorithm=MD5,nonce="1111790769596",realm="SomeRealm"'),
                        ('Warning', '370 200.21.3.10 "Insufficient Bandwidth"'),
                        ('X-RTP-Stat', ' PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048'),
                        ('x-channel', ' ds/ds1-3/12;IP=132.52.127.16'),
                        ('Referred-By', '<sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"'),
                        ('Refer-To', '<sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>'),
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
                        ('Accept', 'application/sdp,application/isup,application/dtmf,application/dtmf-relay,multipart/mixed'),
                        ('Accept-Encoding', 'x-nortel-short'),
                        ('Accept-Language', 'en-us,fr-fr'),
                        ('Allow', ' ACK,BYE,CANCEL,INFO,INVITE,OPTIONS,REGISTER,SUBSCRIBE,UPDATE'),
                        ('Authorization', 'Digest username="3122221000",realm="SomeRealm",nonce="1111790769596",uri="sip:3122211004@example.com",response="9bf77d8238664fe08dafd4d2abb6f1cb",algorithm=MD5'),
                        ('Call-Info', '<https://lsc14pa.example.com:443/pa/direct/pictureServlet?user=3126805100@example.com>;Purpose=icon'),
                        ('Content-Disposition', 'session;handling=required'),
                        ('Content-Type', 'application/sdp'),
                        ('Date', 'Sat, 01 Feb 2014 22:07:34 GMT'),
                        ('Record-Route', '<sip:200.25.3.230:5061;transport=tls;lr>'),
                        ('Require', 'sdp-anat'),
                        ('Retry-After', '30'),
                        ('Server', 'Blargomatic 2.0'),
                        ('Session-Expires', '1200;refresher=uac'),
                        ('Supported', '100rel,histinfo,join,replaces,sdp-anat,timer'),
                        ('Timestamp', '1392061773'),
                        ('WWW-Authenticate', 'Digest algorithm=MD5,nonce="1111790769596",realm="SomeRealm"'),
                        ('Warning', '370 200.21.3.10 "Insufficient Bandwidth"'),
                        ('X-RTP-Stat', ' PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048'),
                        ('x-channel', ' ds/ds1-3/12;IP=132.52.127.16'),
                        ('Referred-By', '<sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"'),
                        ('Refer-To', '<sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>'),
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
        self.assertEqual(4, aSIPResponse.header.unknownHeaderFields.__len__())
        self.assertTrue(aSIPResponse.startLine.isResponse)
        self.assertFalse(aSIPResponse.startLine.isRequest)
        self.assertFalse(aSIPResponse.startLine.isMalformed)
        self.assertEqual('Foo Content', aSIPResponse.content)
        self.assertEqual(100, aSIPResponse.startLine.statusCode)
        self.assertEqual('Trying', aSIPResponse.startLine.reasonPhrase)



