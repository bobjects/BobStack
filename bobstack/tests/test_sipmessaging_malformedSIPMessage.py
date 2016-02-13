from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging import MalformedSIPStartLine
from sipmessaging import MalformedSIPMessage
from sipmessaging import ContentLengthSIPHeaderField
from sipmessaging import UnknownSIPHeaderField
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
from sipmessaging import SIPHeader


class TestMalformedSipMessage(TestCase):
    @property
    def canonicalStrings(self):
        return [
            ('Malformed start line\r\n'
             'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
             'To: <sip:example.com:5061>\r\n'
             'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
             'CSeq: 6711 OPTIONS\r\n'
             'Max-Forwards: 70\r\n'
             'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
             'User-Agent: Example User Agent\r\n'
             'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
             'Route: <sip:200.30.10.12:5061;transport=tls;lr>\r\n'
             'Expires: 0\r\n'
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
            request = MalformedSIPMessage.newParsedFrom(messageString)
            self.runAssertionsForRequest(request)

    def test_rendering(self):
        headerFields = [
            FromSIPHeaderField.newForAttributes(fieldValue='<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
            ToSIPHeaderField.newForAttributes( fieldValue='<sip:example.com:5061>'),
            CallIDSIPHeaderField.newForAttributes(fieldValue='0ee8d3e272e31c9195299efc500'),
            CSeqSIPHeaderField.newForAttributes(fieldValue='6711 OPTIONS'),
            MaxForwardsSIPHeaderField.newForAttributes(fieldValue='70'),
            ViaSIPHeaderField.newForAttributes(fieldValue='SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
            UserAgentSIPHeaderField.newForAttributes(fieldValue='Example User Agent'),
            ContactSIPHeaderField.newForAttributes(fieldValue='<sip:invalid@200.25.3.150:5061;transport=tls>'),
            RouteSIPHeaderField.newForAttributes(fieldValue='<sip:200.30.10.12:5061;transport=tls;lr>'),
            ExpiresSIPHeaderField.newForAttributes(fieldValue='0'),
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
        request = MalformedSIPMessage._newForAttributes(startLine=MalformedSIPStartLine.newParsedFrom('Malformed start line'), content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def runAssertionsForRequest(self, aSIPRequest):
        self.assertEqual(aSIPRequest.rawString, self.canonicalStrings[0])
        self.assertFalse(aSIPRequest.isKnown)
        self.assertTrue(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isValid)
        self.assertFalse(aSIPRequest.isRequest)
        self.assertFalse(aSIPRequest.isResponse)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)
        self.assertTrue(aSIPRequest.isMalformed)
        self.assertIsNotNone(aSIPRequest.header.contentLengthHeaderField)
        self.assertEqual(11, aSIPRequest.header.contentLength)
        self.assertEqual(1, aSIPRequest.header.viaHeaderFields.__len__())
        self.assertEqual(1, aSIPRequest.header.vias.__len__())
        self.assertEqual('SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500', aSIPRequest.header.vias[0])
        self.assertEqual(4, aSIPRequest.header.unknownHeaderFields.__len__())
        self.assertFalse(aSIPRequest.startLine.isRequest)
        self.assertFalse(aSIPRequest.startLine.isResponse)
        self.assertTrue(aSIPRequest.startLine.isMalformed)
        self.assertEqual('Foo Content', aSIPRequest.content)
        self.assertEqual('Malformed start line', aSIPRequest.startLine.rawString)


