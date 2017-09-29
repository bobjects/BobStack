try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from unittest import TestCase
import inspect
import sys
sys.path.append("..")
from sipmessaging import SIPURI
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
from sipmessaging import UnknownSIPHeaderField


class AbstractSIPMessageTestCase(TestCase):
    @property
    def canonicalStrings(self):
        answer = []
        for startLineString in self.canonicalStartLineStrings:
            message_string_io = StringIO()
            message_string_io.write(startLineString)
            message_string_io.write("\r\n")
            for header_field_string in self.canonicalHeaderFieldStrings:
                message_string_io.write(header_field_string)
                message_string_io.write("\r\n")
            message_string_io.write("\r\n")
            message_string_io.write(self.canonicalContent)
            answer.append(message_string_io.getvalue())
        return answer

    @property
    def sipMethodString(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    @property
    def sipMessageClassUnderTest(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    @property
    def canonicalStartLineStrings(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    @property
    def canonicalHeaderFieldStrings(self):
        return ['From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500',
                'To: <sip:example.com:5061>',
                'Call-ID: 0ee8d3e272e31c9195299efc500',
                'CSeq: 6711 ' + self.sipMethodString,
                'Max-Forwards: 70',
                'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500',
                'Via: SIP/2.0/TLS 200.25.3.250;branch=z9hG4bKfdkajhdiruyalkghjladksjf',
                'Via: SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf',
                'User-Agent: Example User Agent',
                'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>',
                'Route: <sip:200.25.3.230:5061;transport=tls;lr>',
                'Route: <sip:200.25.3.231:5061;transport=tls;lr>',
                'Route: <sip:200.25.3.232:5061;transport=tls;lr>',
                'Expires: 0',
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
                'Record-Route: <sip:200.25.3.231:5061;transport=tls;lr>',
                'Record-Route: <sip:200.25.3.232:5061;transport=tls;lr>',
                'Require: sdp-anat',
                'Retry-After: 30',
                'Server: Blargomatic 2.0',
                # TODO:  We will need to deal with the refresher parameter, i.e. we will need to
                # be able to specify parameter dictionaries to the newForAttributes method for
                # Integer header fields.  Maybe even more generically; for all SIP header fields.
                # 'Session-Expires: 1200;refresher=uac',
                'Session-Expires: 1200',
                'Supported: 100rel,histinfo,join,replaces,sdp-anat,timer',
                'Timestamp: 1392061773',
                'WWW-Authenticate: Digest algorithm=MD5,nonce="1111790769596",realm="SomeRealm"',
                'Warning: 370 200.21.3.10 "Insufficient Bandwidth"',
                'X-RTP-Stat:  PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048',
                'x-channel:  ds/ds1-3/12;IP=132.52.127.16',
                'Referred-By: <sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"',
                'Refer-To: <sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>',
                'Subject: Need more boxes',
                'Referred-By: <sip:5556785103@example.com;user=phone> ; CorrelationID="348058f0947acec8745efd367e33542c5cb01436@192.168.0.3"',
                'Refer-To: <sip:5556645204@example.com:5064;user=phone;transport=udp>',
                'Allow-Events: dialog,message-summary',
                'Event: refer;id=10498',
                'Content-Encoding: gzip',
                'RAck: 1 1 INVITE',
                'P-Charge: <sip:6425555555@10.10.10.10>;npi=ISDN;noa=2',
                'Reply-To: Bob <sip:bob@biloxi.com>',
                'Unsupported: foo',
                'P-Asserted-Identity: "500 - SIP Test" <sip:500@192.168.0.3>',
                'P-Preferred-Identity: "User 5103" <sip:3126705103@192.168.0.3:5060>',
                'Remote-Party-ID: "1234567890" <sip:1234567890@192.168.1.195>;party=calling;privacy=off;screen=no',
                'Alert-Info: <cid:internal@example.com>;alert-type=internal',
                'History-Info: "555122221002" <sip:555122221002@example.com>;index=1.1',
                'P-Called-Party-Id: <sip:2135881@example.com;user=phone>',
                'P-RTP-Stat: PS=0,OS=0,PR=5429,OR=955504,PL=0,JI=0,LA=0,DU=108',
                'Privacy: id',
                'Proxy-Authenticate: Digest realm="1.1.1.1", nonce="8dd33eb2-e3c4-11e5-a55b-83b175043a03", algorithm=MD5, qop="auth"',
                'Proxy-Authorization: Digest username="100",realm="209.105.255.124",nonce="7bebcf02-e01d-11e5-931d-83b175043a03",uri="sip:90011@209.105.255.124",response="63faaa2604cae36e9b38f2d5cd0abba4",cnonce="4b41f53e6f00c05",nc=00000001,qop="auth",algorithm=MD5',
                'Proxy-Require: foo',
                'Reason: Q.850; cause=16; reason=Terminated',
                'Record-Session-Expires: 1200;refresher=uac',
                'Replaces: 19cd9bf094ff5f0c1745ef975c1cf65d34beb908f@192.168.0.3;to-tag=29bd570-f0a1ec8-13c5-50029-aa872-7d78286-aa872;from-tag=7ca31b4791',
                'Subscription-State: active;reason=deactivated;expires=50',
                'Min-Expires: 1800',
                'Content-Length: 11']  # This last one actually instantiates a ContentLengthSIPHeaderField.

    # TODO:  Do we want to test different contents?  If so, our assertions need to be aware of that.
    @property
    def canonicalContent(self):
        return 'Foo Content'

    @property
    def oneBigHeaderStringForAssertion(self):
        answer =   ('From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                    'To: <sip:example.com:5061>\r\n'
                    'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                    'CSeq: 6711 SIPMETHODTOREPLACE\r\n'
                    'Max-Forwards: 70\r\n'
                    'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                    'Via: SIP/2.0/TLS 200.25.3.250;branch=z9hG4bKfdkajhdiruyalkghjladksjf\r\n'
                    'Via: SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf\r\n'
                    'User-Agent: Example User Agent\r\n'
                    'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                    'Route: <sip:200.25.3.230:5061;transport=tls;lr>\r\n'
                    'Route: <sip:200.25.3.231:5061;transport=tls;lr>\r\n'
                    'Route: <sip:200.25.3.232:5061;transport=tls;lr>\r\n'
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
                    'Record-Route: <sip:200.25.3.231:5061;transport=tls;lr>\r\n'
                    'Record-Route: <sip:200.25.3.232:5061;transport=tls;lr>\r\n'
                    'Require: sdp-anat\r\n'
                    'Retry-After: 30\r\n'
                    'Server: Blargomatic 2.0\r\n'
                    # TODO:  We will need to deal with the refresher parameter, i.e. we will need to
                    # be able to specify parameter dictionaries to the newForAttributes method for
                    # Integer header fields.  Maybe even more generically; for all SIP header fields.
                    # 'Session-Expires: 1200;refresher=uac\r\n'
                    'Session-Expires: 1200\r\n'
                    'Supported: 100rel,histinfo,join,replaces,sdp-anat,timer\r\n'
                    'Timestamp: 1392061773\r\n'
                    'WWW-Authenticate: Digest algorithm=MD5,nonce="1111790769596",realm="SomeRealm"\r\n'
                    'Warning: 370 200.21.3.10 "Insufficient Bandwidth"\r\n'
                    'X-RTP-Stat:  PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048\r\n'
                    'x-channel:  ds/ds1-3/12;IP=132.52.127.16\r\n'
                    'Referred-By: <sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"\r\n'
                    'Refer-To: <sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>\r\n'
                    'Subject: Need more boxes\r\n'
                    'Referred-By: <sip:5556785103@example.com;user=phone> ; CorrelationID="348058f0947acec8745efd367e33542c5cb01436@192.168.0.3"\r\n'
                    'Refer-To: <sip:5556645204@example.com:5064;user=phone;transport=udp>\r\n'
                    'Allow-Events: dialog,message-summary\r\n'
                    'Event: refer;id=10498\r\n'
                    'Content-Encoding: gzip\r\n'
                    'RAck: 1 1 INVITE\r\n'
                    'P-Charge: <sip:6425555555@10.10.10.10>;npi=ISDN;noa=2\r\n'
                    'Reply-To: Bob <sip:bob@biloxi.com>\r\n'
                    'Unsupported: foo\r\n'
                    'P-Asserted-Identity: "500 - SIP Test" <sip:500@192.168.0.3>\r\n'
                    'P-Preferred-Identity: "User 5103" <sip:3126705103@192.168.0.3:5060>\r\n'
                    'Remote-Party-ID: "1234567890" <sip:1234567890@192.168.1.195>;party=calling;privacy=off;screen=no\r\n'
                    'Alert-Info: <cid:internal@example.com>;alert-type=internal\r\n'
                    'History-Info: "555122221002" <sip:555122221002@example.com>;index=1.1\r\n'
                    'P-Called-Party-Id: <sip:2135881@example.com;user=phone>\r\n'
                    'P-RTP-Stat: PS=0,OS=0,PR=5429,OR=955504,PL=0,JI=0,LA=0,DU=108\r\n'
                    'Privacy: id\r\n'
                    'Proxy-Authenticate: Digest realm="1.1.1.1", nonce="8dd33eb2-e3c4-11e5-a55b-83b175043a03", algorithm=MD5, qop="auth"\r\n'
                    'Proxy-Authorization: Digest username="100",realm="209.105.255.124",nonce="7bebcf02-e01d-11e5-931d-83b175043a03",uri="sip:90011@209.105.255.124",response="63faaa2604cae36e9b38f2d5cd0abba4",cnonce="4b41f53e6f00c05",nc=00000001,qop="auth",algorithm=MD5\r\n'
                    'Proxy-Require: foo\r\n'
                    'Reason: Q.850; cause=16; reason=Terminated\r\n'
                    'Record-Session-Expires: 1200;refresher=uac\r\n'
                    'Replaces: 19cd9bf094ff5f0c1745ef975c1cf65d34beb908f@192.168.0.3;to-tag=29bd570-f0a1ec8-13c5-50029-aa872-7d78286-aa872;from-tag=7ca31b4791\r\n'
                    'Subscription-State: active;reason=deactivated;expires=50\r\n'
                    'Min-Expires: 1800\r\n'
                    'Content-Length: 11')  # This last one actually instantiates a ContentLengthSIPHeaderField.
        return answer.replace("SIPMETHODTOREPLACE", self.sipMethodString)

    # TODO:  need to do this folding test.  Wrote the folded message, need to write the test.
    @property
    def oneBigHeaderStringWithFoldingForAssertion(self):
        answer =   ('From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                    'To: <sip:example.com:5061>\r\n'
                    'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                    'CSeq: 6711\r\n'
                    ' SIPMETHODTOREPLACE\r\n'
                    'Max-Forwards: 70\r\n'
                    'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                    'Via:\r\n'
                    ' SIP/2.0/TLS 200.25.3.250;branch=z9hG4bKfdkajhdiruyalkghjladksjf\r\n'
                    'Via: SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf\r\n'
                    'User-Agent:\r\n'
                    ' Example User Agent\r\n'
                    'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                    'Route: <sip:200.25.3.230:5061;transport=tls;lr>\r\n'
                    'Route: <sip:200.25.3.231:5061;transport=tls;lr>\r\n'
                    'Route: <sip:200.25.3.232:5061;transport=tls;lr>\r\n'
                    'Expires: 0\r\n'
                    'Accept: application/sdp,application/isup,application/dtmf,application/dtmf-relay,multipart/mixed\r\n'
                    'Accept-Encoding: x-nortel-short\r\n'
                    'Accept-Language: en-us,fr-fr\r\n'
                    'Allow:  ACK,BYE,CANCEL,INFO,INVITE,OPTIONS,REGISTER,SUBSCRIBE,UPDATE\r\n'
                    'Authorization: Digest\r\n'
                    ' username="3122221000",realm="SomeRealm",nonce="1111790769596",uri="sip:3122211004@example.com",response="9bf77d8238664fe08dafd4d2abb6f1cb",algorithm=MD5\r\n'
                    'Call-Info: <https://lsc14pa.example.com:443/pa/direct/pictureServlet?user=3126805100@example.com>;Purpose=icon\r\n'
                    'Content-Disposition: session;handling=required\r\n'
                    'Content-Type: application/sdp\r\n'
                    'Date: Sat, 01 Feb 2014 22:07:34 GMT\r\n'
                    'Record-Route: <sip:200.25.3.230:5061;transport=tls;lr>\r\n'
                    'Record-Route: <sip:200.25.3.231:5061;transport=tls;lr>\r\n'
                    'Record-Route: <sip:200.25.3.232:5061;transport=tls;lr>\r\n'
                    'Require: sdp-anat\r\n'
                    'Retry-After: 30\r\n'
                    'Server: Blargomatic 2.0\r\n'
                    # TODO:  We will need to deal with the refresher parameter, i.e. we will need to
                    # be able to specify parameter dictionaries to the newForAttributes method for
                    # Integer header fields.  Maybe even more generically; for all SIP header fields.
                    # 'Session-Expires: 1200;refresher=uac\r\n'
                    'Session-Expires: 1200\r\n'
                    'Supported: 100rel,histinfo,join,replaces,sdp-anat,timer\r\n'
                    'Timestamp: 1392061773\r\n'
                    'WWW-Authenticate:\r\n'
                    ' Digest\r\n'
                    ' algorithm=MD5,nonce="1111790769596",realm="SomeRealm"\r\n'
                    'Warning:\r\n'
                    ' 370\r\n'
                    ' 200.21.3.10\r\n'
                    ' "Insufficient Bandwidth"\r\n'
                    'X-RTP-Stat:  PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048\r\n'
                    'x-channel:  ds/ds1-3/12;IP=132.52.127.16\r\n'
                    'Referred-By: <sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"\r\n'
                    'Refer-To: <sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>\r\n'
                    'Subject: Need more\r\n'
                    ' boxes\r\n'
                    'Referred-By: <sip:5556785103@example.com;user=phone> ;\r\n'
                    ' CorrelationID="348058f0947acec8745efd367e33542c5cb01436@192.168.0.3"\r\n'
                    'Refer-To: <sip:5556645204@example.com:5064;user=phone;transport=udp>\r\n'
                    'Allow-Events: dialog,message-summary\r\n'
                    'Event: refer;id=10498\r\n'
                    'Content-Encoding: gzip\r\n'
                    'RAck: 1 1\r\n'
                    ' INVITE\r\n'
                    'P-Charge: <sip:6425555555@10.10.10.10>;npi=ISDN;noa=2\r\n'
                    'Reply-To: Bob <sip:bob@biloxi.com>\r\n'
                    'Unsupported: foo\r\n'
                    'P-Asserted-Identity: "500 - SIP\r\n'
                    ' Test" <sip:500@192.168.0.3>\r\n'
                    'P-Preferred-Identity: "User 5103" <sip:3126705103@192.168.0.3:5060>\r\n'
                    'Remote-Party-ID: "1234567890" <sip:1234567890@192.168.1.195>;party=calling;privacy=off;screen=no\r\n'
                    'Alert-Info: <cid:internal@example.com>;alert-type=internal\r\n'
                    'History-Info: "555122221002" <sip:555122221002@example.com>;index=1.1\r\n'
                    'P-Called-Party-Id: <sip:2135881@example.com;user=phone>\r\n'
                    'P-RTP-Stat: PS=0,OS=0,PR=5429,OR=955504,PL=0,JI=0,LA=0,DU=108\r\n'
                    'Privacy: id\r\n'
                    'Proxy-Authenticate: Digest realm="1.1.1.1",\r\n'
                    ' nonce="8dd33eb2-e3c4-11e5-a55b-83b175043a03", algorithm=MD5, qop="auth"\r\n'
                    'Proxy-Authorization: Digest username="100",realm="209.105.255.124",nonce="7bebcf02-e01d-11e5-931d-83b175043a03",uri="sip:90011@209.105.255.124",response="63faaa2604cae36e9b38f2d5cd0abba4",cnonce="4b41f53e6f00c05",nc=00000001,qop="auth",algorithm=MD5\r\n'
                    'Proxy-Require:\r\n'
                    ' foo\r\n'
                    'Reason: Q.850; cause=16; reason=Terminated\r\n'
                    'Record-Session-Expires:\r\n'
                    ' 1200;refresher=uac\r\n'
                    'Replaces: 19cd9bf094ff5f0c1745ef975c1cf65d34beb908f@192.168.0.3;to-tag=29bd570-f0a1ec8-13c5-50029-aa872-7d78286-aa872;from-tag=7ca31b4791\r\n'
                    'Subscription-State:\r\n'
                    ' active;reason=deactivated;expires=50\r\n'
                    'Min-Expires: 1800\r\n'
                    'Content-Length: 11')  # This last one actually instantiates a ContentLengthSIPHeaderField.
        return answer.replace("SIPMETHODTOREPLACE", self.sipMethodString)

    @property
    def listOfHeaderFieldsForAssertion(self):
        return [
            # FromSIPHeaderField.newForAttributes(field_value_string='<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
            FromSIPHeaderField.newForAttributes(tag='0ee8d3e272e31c9195299efc500', display_name=None, sip_uri=SIPURI.newParsedFrom('sip:200.25.3.150:5061')),
            # ToSIPHeaderField.newForAttributes(field_value_string='<sip:example.com:5061>'),
            ToSIPHeaderField.newForAttributes(tag=None, display_name=None, sip_uri=SIPURI.newParsedFrom('sip:example.com:5061')),
            CallIDSIPHeaderField.newForAttributes(field_value_string='0ee8d3e272e31c9195299efc500'),
            CSeqSIPHeaderField.newForAttributes(field_value_string='6711 ' + self.sipMethodString),
            MaxForwardsSIPHeaderField.newForAttributes(value=70),
            # ViaSIPHeaderField.newForAttributes(field_value_string='SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
            ViaSIPHeaderField.newForAttributes(transport='TLS', host='200.25.3.150', branch='z9hG4bK0ee8d3e272e31ca195299efc500'),
            # ViaSIPHeaderField.newForAttributes(field_value_string='SIP/2.0/TLS 200.25.3.250;branch=z9hG4bKfdkajhdiruyalkghjladksjf'),
            ViaSIPHeaderField.newForAttributes(transport='TLS', host='200.25.3.250', branch='z9hG4bKfdkajhdiruyalkghjladksjf'),
            # ViaSIPHeaderField.newForAttributes(field_value_string='SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf'),
            ViaSIPHeaderField.newForAttributes(transport='TLS', host='200.25.3.255', branch='z9hG4bKduyroiuryaludhgviukfhlasf'),
            UserAgentSIPHeaderField.newForAttributes(field_value_string='Example User Agent'),
            # ContactSIPHeaderField.newForAttributes(field_value_string='<sip:invalid@200.25.3.150:5061;transport=tls>'),
            ContactSIPHeaderField.newForAttributes(display_name=None, sip_uri=SIPURI.newParsedFrom('sip:invalid@200.25.3.150:5061;transport=tls')),
            RouteSIPHeaderField.newForAttributes(sip_uri=SIPURI.newParsedFrom('sip:200.25.3.230:5061;transport=tls;lr')),
            RouteSIPHeaderField.newForAttributes(sip_uri=SIPURI.newParsedFrom('sip:200.25.3.231:5061;transport=tls;lr')),
            RouteSIPHeaderField.newForAttributes(sip_uri=SIPURI.newParsedFrom('sip:200.25.3.232:5061;transport=tls;lr')),
            ExpiresSIPHeaderField.newForAttributes(value=0),
            AcceptSIPHeaderField.newForAttributes(field_value_string='application/sdp,application/isup,application/dtmf,application/dtmf-relay,multipart/mixed'),
            AcceptEncodingSIPHeaderField.newForAttributes(field_value_string='x-nortel-short'),
            AcceptLanguageSIPHeaderField.newForAttributes(field_value_string='en-us,fr-fr'),
            AllowSIPHeaderField.newForAttributes(field_value_string=' ACK,BYE,CANCEL,INFO,INVITE,OPTIONS,REGISTER,SUBSCRIBE,UPDATE'),
            AuthorizationSIPHeaderField.newForAttributes(field_value_string='Digest username="3122221000",realm="SomeRealm",nonce="1111790769596",uri="sip:3122211004@example.com",response="9bf77d8238664fe08dafd4d2abb6f1cb",algorithm=MD5'),
            CallInfoSIPHeaderField.newForAttributes(field_value_string='<https://lsc14pa.example.com:443/pa/direct/pictureServlet?user=3126805100@example.com>;Purpose=icon'),
            ContentDispositionSIPHeaderField.newForAttributes(field_value_string='session;handling=required'),
            ContentTypeSIPHeaderField.newForAttributes(field_value_string='application/sdp'),
            DateSIPHeaderField.newForAttributes(field_value_string='Sat, 01 Feb 2014 22:07:34 GMT'),
            RecordRouteSIPHeaderField.newForAttributes(sip_uri=SIPURI.newParsedFrom('sip:200.25.3.230:5061;transport=tls;lr')),
            RecordRouteSIPHeaderField.newForAttributes(sip_uri=SIPURI.newParsedFrom('sip:200.25.3.231:5061;transport=tls;lr')),
            RecordRouteSIPHeaderField.newForAttributes(sip_uri=SIPURI.newParsedFrom('sip:200.25.3.232:5061;transport=tls;lr')),
            RequireSIPHeaderField.newForAttributes(field_value_string='sdp-anat'),
            RetryAfterSIPHeaderField.newForAttributes(value=30),
            ServerSIPHeaderField.newForAttributes(field_value_string='Blargomatic 2.0'),
            # TODO:  We will need to deal with the refresher parameter, i.e. we will need to
            # be able to specify parameter dictionaries to the newForAttributes method for
            # Integer header fields.  Maybe even more generically; for all SIP header fields.
            # SessionExpiresSIPHeaderField.newForAttributes(field_value_string='1200;refresher=uac'),
            SessionExpiresSIPHeaderField.newForAttributes(value=1200),
            SupportedSIPHeaderField.newForAttributes(field_value_string='100rel,histinfo,join,replaces,sdp-anat,timer'),
            TimestampSIPHeaderField.newForAttributes(value=1392061773),
            WWWAuthenticateSIPHeaderField.newForAttributes(field_value_string='Digest algorithm=MD5,nonce="1111790769596",realm="SomeRealm"'),
            WarningSIPHeaderField.newForAttributes(field_value_string='370 200.21.3.10 "Insufficient Bandwidth"'),
            UnknownSIPHeaderField.newForFieldNameAndValueString(field_name='X-RTP-Stat', field_value_string=' PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048'),
            UnknownSIPHeaderField.newForFieldNameAndValueString(field_name='x-channel', field_value_string=' ds/ds1-3/12;IP=132.52.127.16'),
            ReferredBySIPHeaderField.newForAttributes(field_value_string='<sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"'),
            ReferToSIPHeaderField.newForAttributes(field_value_string='<sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>'),

            SubjectSIPHeaderField.newForAttributes(field_value_string='Need more boxes'),
            ReferredBySIPHeaderField.newForAttributes(field_value_string='<sip:5556785103@example.com;user=phone> ; CorrelationID="348058f0947acec8745efd367e33542c5cb01436@192.168.0.3"'),
            ReferToSIPHeaderField.newForAttributes(field_value_string='<sip:5556645204@example.com:5064;user=phone;transport=udp>'),
            AllowEventsSIPHeaderField.newForAttributes(field_value_string='dialog,message-summary'),
            EventSIPHeaderField.newForAttributes(field_value_string='refer;id=10498'),
            ContentEncodingSIPHeaderField.newForAttributes(field_value_string='gzip'),
            RAckSIPHeaderField.newForAttributes(field_value_string='1 1 INVITE'),
            PChargeSIPHeaderField.newForAttributes(field_value_string='<sip:6425555555@10.10.10.10>;npi=ISDN;noa=2'),
            ReplyToSIPHeaderField.newForAttributes(field_value_string='Bob <sip:bob@biloxi.com>'),
            UnsupportedSIPHeaderField.newForAttributes(field_value_string='foo'),
            PAssertedIdentitySIPHeaderField.newForAttributes(field_value_string='"500 - SIP Test" <sip:500@192.168.0.3>'),
            PPreferredIdentitySIPHeaderField.newForAttributes(field_value_string='"User 5103" <sip:3126705103@192.168.0.3:5060>'),
            RemotePartyIDSIPHeaderField.newForAttributes(field_value_string='"1234567890" <sip:1234567890@192.168.1.195>;party=calling;privacy=off;screen=no'),
            AlertInfoSIPHeaderField.newForAttributes(field_value_string='<cid:internal@example.com>;alert-type=internal'),
            HistoryInfoSIPHeaderField.newForAttributes(field_value_string='"555122221002" <sip:555122221002@example.com>;index=1.1'),
            PCalledPartyIdSIPHeaderField.newForAttributes(field_value_string='<sip:2135881@example.com;user=phone>'),
            PRTPStatSIPHeaderField.newForAttributes(field_value_string='PS=0,OS=0,PR=5429,OR=955504,PL=0,JI=0,LA=0,DU=108'),
            PrivacySIPHeaderField.newForAttributes(field_value_string='id'),
            ProxyAuthenticateSIPHeaderField.newForAttributes(field_value_string='Digest realm="1.1.1.1", nonce="8dd33eb2-e3c4-11e5-a55b-83b175043a03", algorithm=MD5, qop="auth"'),
            ProxyAuthorizationSIPHeaderField.newForAttributes(field_value_string='Digest username="100",realm="209.105.255.124",nonce="7bebcf02-e01d-11e5-931d-83b175043a03",uri="sip:90011@209.105.255.124",response="63faaa2604cae36e9b38f2d5cd0abba4",cnonce="4b41f53e6f00c05",nc=00000001,qop="auth",algorithm=MD5'),
            ProxyRequireSIPHeaderField.newForAttributes(field_value_string='foo'),
            ReasonSIPHeaderField.newForAttributes(field_value_string='Q.850; cause=16; reason=Terminated'),
            RecordSessionExpiresSIPHeaderField.newForValueString(field_value_string='1200;refresher=uac'),
            ReplacesSIPHeaderField.newForAttributes(field_value_string='19cd9bf094ff5f0c1745ef975c1cf65d34beb908f@192.168.0.3;to-tag=29bd570-f0a1ec8-13c5-50029-aa872-7d78286-aa872;from-tag=7ca31b4791'),
            SubscriptionStateSIPHeaderField.newForAttributes(field_value_string='active;reason=deactivated;expires=50'),
            MinExpiresSIPHeaderField.newForAttributes(value=1800),

            ContentLengthSIPHeaderField.newForAttributes(value=11)]

    @property
    def listOfHeaderFieldStringsForAssertion(self):
        return ['From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500',
                'To: <sip:example.com:5061>',
                'Call-ID: 0ee8d3e272e31c9195299efc500',
                'CSeq: 6711 ' + self.sipMethodString,
                'Max-Forwards: 70',
                'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500',
                'Via: SIP/2.0/TLS 200.25.3.250;branch=z9hG4bKfdkajhdiruyalkghjladksjf',
                'Via: SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf',
                'User-Agent: Example User Agent',
                'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>',
                'Route: <sip:200.25.3.230:5061;transport=tls;lr>',
                'Route: <sip:200.25.3.231:5061;transport=tls;lr>',
                'Route: <sip:200.25.3.232:5061;transport=tls;lr>',
                'Expires: 0',
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
                'Record-Route: <sip:200.25.3.231:5061;transport=tls;lr>',
                'Record-Route: <sip:200.25.3.232:5061;transport=tls;lr>',
                'Require: sdp-anat',
                'Retry-After: 30',
                'Server: Blargomatic 2.0',
                # TODO:  We will need to deal with the refresher parameter, i.e. we will need to
                # be able to specify parameter dictionaries to the newForAttributes method for
                # Integer header fields.  Maybe even more generically; for all SIP header fields.
                # 'Session-Expires: 1200;refresher=uac',
                'Session-Expires: 1200',
                'Supported: 100rel,histinfo,join,replaces,sdp-anat,timer',
                'Timestamp: 1392061773',
                'WWW-Authenticate: Digest algorithm=MD5,nonce="1111790769596",realm="SomeRealm"',
                'Warning: 370 200.21.3.10 "Insufficient Bandwidth"',
                'X-RTP-Stat:  PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048',
                'x-channel:  ds/ds1-3/12;IP=132.52.127.16',
                'Referred-By: <sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"',
                'Refer-To: <sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>',
                'Subject: Need more boxes',
                'Referred-By: <sip:5556785103@example.com;user=phone> ; CorrelationID="348058f0947acec8745efd367e33542c5cb01436@192.168.0.3"',
                'Refer-To: <sip:5556645204@example.com:5064;user=phone;transport=udp>',
                'Allow-Events: dialog,message-summary',
                'Event: refer;id=10498',
                'Content-Encoding: gzip',
                'RAck: 1 1 INVITE',
                'P-Charge: <sip:6425555555@10.10.10.10>;npi=ISDN;noa=2',
                'Reply-To: Bob <sip:bob@biloxi.com>',
                'Unsupported: foo',
                'P-Asserted-Identity: "500 - SIP Test" <sip:500@192.168.0.3>',
                'P-Preferred-Identity: "User 5103" <sip:3126705103@192.168.0.3:5060>',
                'Remote-Party-ID: "1234567890" <sip:1234567890@192.168.1.195>;party=calling;privacy=off;screen=no',
                'Alert-Info: <cid:internal@example.com>;alert-type=internal',
                'History-Info: "555122221002" <sip:555122221002@example.com>;index=1.1',
                'P-Called-Party-Id: <sip:2135881@example.com;user=phone>',
                'P-RTP-Stat: PS=0,OS=0,PR=5429,OR=955504,PL=0,JI=0,LA=0,DU=108',
                'Privacy: id',
                'Proxy-Authenticate: Digest realm="1.1.1.1", nonce="8dd33eb2-e3c4-11e5-a55b-83b175043a03", algorithm=MD5, qop="auth"',
                'Proxy-Authorization: Digest username="100",realm="209.105.255.124",nonce="7bebcf02-e01d-11e5-931d-83b175043a03",uri="sip:90011@209.105.255.124",response="63faaa2604cae36e9b38f2d5cd0abba4",cnonce="4b41f53e6f00c05",nc=00000001,qop="auth",algorithm=MD5',
                'Proxy-Require: foo',
                'Reason: Q.850; cause=16; reason=Terminated',
                'Record-Session-Expires: 1200;refresher=uac',
                'Replaces: 19cd9bf094ff5f0c1745ef975c1cf65d34beb908f@192.168.0.3;to-tag=29bd570-f0a1ec8-13c5-50029-aa872-7d78286-aa872;from-tag=7ca31b4791',
                'Subscription-State: active;reason=deactivated;expires=50',
                'Min-Expires: 1800',
                'Content-Length: 11']  # This last one actually instantiates a ContentLengthSIPHeaderField.

    @property
    def listOfHeaderFieldNamesAndValuesForAssertion(self):
        return [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                ('To', '<sip:example.com:5061>'),
                ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                ('CSeq', '6711 ' + self.sipMethodString),
                ('Max-Forwards', 70),  # note the integer value.
                ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                ('Via', 'SIP/2.0/TLS 200.25.3.250;branch=z9hG4bKfdkajhdiruyalkghjladksjf'),
                ('Via', 'SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf'),
                ('User-Agent', 'Example User Agent'),
                ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                ('Route', '<sip:200.25.3.230:5061;transport=tls;lr>'),
                ('Route', '<sip:200.25.3.231:5061;transport=tls;lr>'),
                ('Route', '<sip:200.25.3.232:5061;transport=tls;lr>'),
                ('Expires', 0),
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
                ('Record-Route', '<sip:200.25.3.231:5061;transport=tls;lr>'),
                ('Record-Route', '<sip:200.25.3.232:5061;transport=tls;lr>'),
                ('Require', 'sdp-anat'),
                ('Retry-After', '30'),
                ('Server', 'Blargomatic 2.0'),
                # TODO:  We will need to deal with the refresher parameter, i.e. we will need to
                # be able to specify parameter dictionaries to the newForAttributes method for
                # Integer header fields.  Maybe even more generically; for all SIP header fields.
                # ('Session-Expires', '1200;refresher=uac'),
                ('Session-Expires', 1200),
                ('Supported', '100rel,histinfo,join,replaces,sdp-anat,timer'),
                ('Timestamp', '1392061773'),
                ('WWW-Authenticate', 'Digest algorithm=MD5,nonce="1111790769596",realm="SomeRealm"'),
                ('Warning', '370 200.21.3.10 "Insufficient Bandwidth"'),
                ('X-RTP-Stat', ' PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048'),
                ('x-channel', ' ds/ds1-3/12;IP=132.52.127.16'),
                ('Referred-By', '<sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"'),
                ('Refer-To', '<sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>'),

                ('Subject', 'Need more boxes'),
                ('Referred-By', '<sip:5556785103@example.com;user=phone> ; CorrelationID="348058f0947acec8745efd367e33542c5cb01436@192.168.0.3"'),
                ('Refer-To', '<sip:5556645204@example.com:5064;user=phone;transport=udp>'),
                ('Allow-Events', 'dialog,message-summary'),
                ('Event', 'refer;id=10498'),
                ('Content-Encoding', 'gzip'),
                ('RAck', '1 1 INVITE'),
                ('P-Charge', '<sip:6425555555@10.10.10.10>;npi=ISDN;noa=2'),
                ('Reply-To', 'Bob <sip:bob@biloxi.com>'),
                ('Unsupported', 'foo'),
                ('P-Asserted-Identity', '"500 - SIP Test" <sip:500@192.168.0.3>'),
                ('P-Preferred-Identity', '"User 5103" <sip:3126705103@192.168.0.3:5060>'),
                ('Remote-Party-ID', '"1234567890" <sip:1234567890@192.168.1.195>;party=calling;privacy=off;screen=no'),
                ('Alert-Info', '<cid:internal@example.com>;alert-type=internal'),
                ('History-Info', '"555122221002" <sip:555122221002@example.com>;index=1.1'),
                ('P-Called-Party-Id', '<sip:2135881@example.com;user=phone>'),
                ('P-RTP-Stat', 'PS=0,OS=0,PR=5429,OR=955504,PL=0,JI=0,LA=0,DU=108'),
                ('Privacy', 'id'),
                ('Proxy-Authenticate', 'Digest realm="1.1.1.1", nonce="8dd33eb2-e3c4-11e5-a55b-83b175043a03", algorithm=MD5, qop="auth"'),
                ('Proxy-Authorization', 'Digest username="100",realm="209.105.255.124",nonce="7bebcf02-e01d-11e5-931d-83b175043a03",uri="sip:90011@209.105.255.124",response="63faaa2604cae36e9b38f2d5cd0abba4",cnonce="4b41f53e6f00c05",nc=00000001,qop="auth",algorithm=MD5'),
                ('Proxy-Require', 'foo'),
                ('Reason', 'Q.850; cause=16; reason=Terminated'),
                ('Record-Session-Expires', '1200;refresher=uac'),
                ('Replaces', '19cd9bf094ff5f0c1745ef975c1cf65d34beb908f@192.168.0.3;to-tag=29bd570-f0a1ec8-13c5-50029-aa872-7d78286-aa872;from-tag=7ca31b4791'),
                ('Subscription-State', 'active;reason=deactivated;expires=50'),
                ('Min-Expires', '1800'),

                ('Content-Length', 11)]  # This last one actually instantiates a ContentLengthSIPHeaderField.

    @property
    def listOfHeaderFieldNamesAndValuesUsingPropertyDictForAssertion(self):
        return [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                ('To', '<sip:example.com:5061>'),
                ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                ('CSeq', '6711 ' + self.sipMethodString),
                ('Max-Forwards', 70),  # note the integer value.
                ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                ('Via', 'SIP/2.0/TLS 200.25.3.250;branch=z9hG4bKfdkajhdiruyalkghjladksjf'),
                ('Via', 'SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf'),
                ('User-Agent', 'Example User Agent'),
                ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                ('Route', '<sip:200.25.3.230:5061;transport=tls;lr>'),
                ('Route', '<sip:200.25.3.231:5061;transport=tls;lr>'),
                ('Route', '<sip:200.25.3.232:5061;transport=tls;lr>'),
                ('Expires', 0),
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
                ('Record-Route', '<sip:200.25.3.231:5061;transport=tls;lr>'),
                ('Record-Route', '<sip:200.25.3.232:5061;transport=tls;lr>'),
                ('Require', 'sdp-anat'),
                ('Retry-After', '30'),
                ('Server', 'Blargomatic 2.0'),
                # TODO:  We will need to deal with the refresher parameter, i.e. we will need to
                # be able to specify parameter dictionaries to the newForAttributes method for
                # Integer header fields.  Maybe even more generically; for all SIP header fields.
                # ('Session-Expires', '1200;refresher=uac'),
                ('Session-Expires', {"value": 1200}),
                ('Supported', '100rel,histinfo,join,replaces,sdp-anat,timer'),
                ('Timestamp', '1392061773'),
                ('WWW-Authenticate', 'Digest algorithm=MD5,nonce="1111790769596",realm="SomeRealm"'),
                ('Warning', '370 200.21.3.10 "Insufficient Bandwidth"'),
                ('X-RTP-Stat', ' PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048'),
                ('x-channel', ' ds/ds1-3/12;IP=132.52.127.16'),
                ('Referred-By', '<sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"'),
                ('Refer-To', '<sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>'),
                ('Subject', 'Need more boxes'),
                ('Referred-By', '<sip:5556785103@example.com;user=phone> ; CorrelationID="348058f0947acec8745efd367e33542c5cb01436@192.168.0.3"'),
                ('Refer-To', '<sip:5556645204@example.com:5064;user=phone;transport=udp>'),
                ('Allow-Events', 'dialog,message-summary'),
                ('Event', 'refer;id=10498'),
                ('Content-Encoding', 'gzip'),
                ('RAck', '1 1 INVITE'),
                ('P-Charge', '<sip:6425555555@10.10.10.10>;npi=ISDN;noa=2'),
                ('Reply-To', 'Bob <sip:bob@biloxi.com>'),
                ('Unsupported', 'foo'),
                ('P-Asserted-Identity', '"500 - SIP Test" <sip:500@192.168.0.3>'),
                ('P-Preferred-Identity', '"User 5103" <sip:3126705103@192.168.0.3:5060>'),
                ('Remote-Party-ID', '"1234567890" <sip:1234567890@192.168.1.195>;party=calling;privacy=off;screen=no'),
                ('Alert-Info', '<cid:internal@example.com>;alert-type=internal'),
                ('History-Info', '"555122221002" <sip:555122221002@example.com>;index=1.1'),
                ('P-Called-Party-Id', '<sip:2135881@example.com;user=phone>'),
                ('P-RTP-Stat', 'PS=0,OS=0,PR=5429,OR=955504,PL=0,JI=0,LA=0,DU=108'),
                ('Privacy', 'id'),
                ('Proxy-Authenticate', 'Digest realm="1.1.1.1", nonce="8dd33eb2-e3c4-11e5-a55b-83b175043a03", algorithm=MD5, qop="auth"'),
                ('Proxy-Authorization', 'Digest username="100",realm="209.105.255.124",nonce="7bebcf02-e01d-11e5-931d-83b175043a03",uri="sip:90011@209.105.255.124",response="63faaa2604cae36e9b38f2d5cd0abba4",cnonce="4b41f53e6f00c05",nc=00000001,qop="auth",algorithm=MD5'),
                ('Proxy-Require', 'foo'),
                ('Reason', 'Q.850; cause=16; reason=Terminated'),
                ('Record-Session-Expires', '1200;refresher=uac'),
                ('Replaces', '19cd9bf094ff5f0c1745ef975c1cf65d34beb908f@192.168.0.3;to-tag=29bd570-f0a1ec8-13c5-50029-aa872-7d78286-aa872;from-tag=7ca31b4791'),
                ('Subscription-State', 'active;reason=deactivated;expires=50'),
                ('Min-Expires', '1800'),
                ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.

    def runAssertionsForSIPMessage(self, a_sip_message):
        self.assertEqual(a_sip_message.rawString, self.canonicalStrings[0])
        self.assertIsNotNone(a_sip_message.header.contentLengthHeaderField)
        self.assertEqual(11, a_sip_message.header.contentLength)
        self.assertEqual(3, a_sip_message.header.viaHeaderFields.__len__())
        self.assertEqual(3, a_sip_message.header.vias.__len__())
        self.assertEqual(3, a_sip_message.vias.__len__())
        self.assertEqual(3, a_sip_message.header.routeHeaderFields.__len__())
        self.assertEqual(3, a_sip_message.header.routeURIs.__len__())
        self.assertEqual(3, a_sip_message.routeURIs.__len__())
        self.assertEqual(3, a_sip_message.header.recordRouteHeaderFields.__len__())
        self.assertEqual(3, a_sip_message.header.recordRouteURIs.__len__())
        self.assertEqual(3, a_sip_message.recordRouteURIs.__len__())
        self.assertIsInstance(a_sip_message.transactionHash, basestring)
        self.assertIsInstance(a_sip_message.dialogHash, (basestring, type(None)))
        self.assertIsInstance(a_sip_message.header.invariantBranchHash, (basestring, type(None)))
        self.assertIsInstance(a_sip_message.header.callID, basestring)
        self.assertIsInstance(a_sip_message.header.cSeq, basestring)
        self.assertIsInstance(a_sip_message.header.toTag, (basestring, type(None)))
        self.assertIsInstance(a_sip_message.header.fromTag, basestring)
        self.assertIsInstance(a_sip_message.header.maxForwards, int)
        self.assertIsInstance(a_sip_message.header.routeURIs, list)
        self.assertIsInstance(a_sip_message.header.recordRouteURIs, list)

        # TODO: assert other headers besides just content-length and via.
        self.assertEqual('SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500', a_sip_message.header.vias[0])
        self.assertEqual('SIP/2.0/TLS 200.25.3.250;branch=z9hG4bKfdkajhdiruyalkghjladksjf', a_sip_message.header.vias[1])
        self.assertEqual('SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf', a_sip_message.header.vias[2])
        self.assertIsInstance(a_sip_message.routeURIs[0], SIPURI)
        self.assertEqual(a_sip_message.routeURIs[0].host, '200.25.3.230')
        self.assertIsInstance(a_sip_message.routeURIs[1], SIPURI)
        self.assertEqual(a_sip_message.routeURIs[1].host, '200.25.3.231')
        self.assertIsInstance(a_sip_message.routeURIs[2], SIPURI)
        self.assertEqual(a_sip_message.routeURIs[2].host, '200.25.3.232')
        self.assertIsInstance(a_sip_message.recordRouteURIs[0], SIPURI)
        self.assertEqual(a_sip_message.recordRouteURIs[0].host, '200.25.3.230')
        self.assertIsInstance(a_sip_message.recordRouteURIs[1], SIPURI)
        self.assertEqual(a_sip_message.recordRouteURIs[1].host, '200.25.3.231')
        self.assertIsInstance(a_sip_message.recordRouteURIs[2], SIPURI)
        self.assertEqual(a_sip_message.recordRouteURIs[2].host, '200.25.3.232')
        self.assertEqual(2, a_sip_message.header.unknownHeaderFields.__len__())
        self.assertEqual('Foo Content', a_sip_message.content)
        self.assertEqual(65, len(a_sip_message.header.header_fields))
        self.assertTrue(a_sip_message.header.header_fields[0].isFrom)
        self.assertTrue(a_sip_message.header.header_fields[1].isTo)
        self.assertTrue(a_sip_message.header.header_fields[2].isCallID)
        self.assertTrue(a_sip_message.header.header_fields[3].isCSeq)
        self.assertTrue(a_sip_message.header.header_fields[4].isMaxForwards)
        self.assertTrue(a_sip_message.header.header_fields[5].isVia)
        self.assertTrue(a_sip_message.header.header_fields[6].isVia)
        self.assertTrue(a_sip_message.header.header_fields[7].isVia)
        self.assertTrue(a_sip_message.header.header_fields[8].isUserAgent)
        self.assertTrue(a_sip_message.header.header_fields[9].isContact)
        self.assertTrue(a_sip_message.header.header_fields[10].isRoute)
        self.assertTrue(a_sip_message.header.header_fields[11].isRoute)
        self.assertTrue(a_sip_message.header.header_fields[12].isRoute)
        self.assertTrue(a_sip_message.header.header_fields[13].isExpires)
        self.assertTrue(a_sip_message.header.header_fields[14].isAccept)
        self.assertTrue(a_sip_message.header.header_fields[15].isAcceptEncoding)
        self.assertTrue(a_sip_message.header.header_fields[16].isAcceptLanguage)
        self.assertTrue(a_sip_message.header.header_fields[17].isAllow)
        self.assertTrue(a_sip_message.header.header_fields[18].isAuthorization)
        self.assertTrue(a_sip_message.header.header_fields[19].isCallInfo)
        self.assertTrue(a_sip_message.header.header_fields[20].isContentDisposition)
        self.assertTrue(a_sip_message.header.header_fields[21].isContentType)
        self.assertTrue(a_sip_message.header.header_fields[22].isDate)
        self.assertTrue(a_sip_message.header.header_fields[23].isRecordRoute)
        self.assertTrue(a_sip_message.header.header_fields[24].isRecordRoute)
        self.assertTrue(a_sip_message.header.header_fields[25].isRecordRoute)
        self.assertTrue(a_sip_message.header.header_fields[26].isRequire)
        self.assertTrue(a_sip_message.header.header_fields[27].isRetryAfter)
        self.assertTrue(a_sip_message.header.header_fields[28].isServer)
        self.assertTrue(a_sip_message.header.header_fields[29].isSessionExpires)
        self.assertTrue(a_sip_message.header.header_fields[30].isSupported)
        self.assertTrue(a_sip_message.header.header_fields[31].isTimestamp)
        self.assertTrue(a_sip_message.header.header_fields[32].isWWWAuthenticate)
        self.assertTrue(a_sip_message.header.header_fields[33].isWarning)
        self.assertTrue(a_sip_message.header.header_fields[34].isUnknown)
        self.assertTrue(a_sip_message.header.header_fields[35].isUnknown)
        self.assertTrue(a_sip_message.header.header_fields[36].isReferredBy)
        self.assertTrue(a_sip_message.header.header_fields[37].isReferTo)

        self.assertTrue(a_sip_message.header.header_fields[38].isSubject)
        self.assertTrue(a_sip_message.header.header_fields[39].isReferredBy)
        self.assertTrue(a_sip_message.header.header_fields[40].isReferTo)
        self.assertTrue(a_sip_message.header.header_fields[41].isAllowEvents)
        self.assertTrue(a_sip_message.header.header_fields[42].isEvent)
        self.assertTrue(a_sip_message.header.header_fields[43].isContentEncoding)
        self.assertTrue(a_sip_message.header.header_fields[44].isRAck)
        self.assertTrue(a_sip_message.header.header_fields[45].isPCharge)
        self.assertTrue(a_sip_message.header.header_fields[46].isReplyTo)
        self.assertTrue(a_sip_message.header.header_fields[47].isUnsupported)
        self.assertTrue(a_sip_message.header.header_fields[48].isPAssertedIdentity)
        self.assertTrue(a_sip_message.header.header_fields[49].isPPreferredIdentity)
        self.assertTrue(a_sip_message.header.header_fields[50].isRemotePartyID)
        self.assertTrue(a_sip_message.header.header_fields[51].isAlertInfo)
        self.assertTrue(a_sip_message.header.header_fields[52].isHistoryInfo)
        self.assertTrue(a_sip_message.header.header_fields[53].isPCalledPartyId)
        self.assertTrue(a_sip_message.header.header_fields[54].isPRTPStat)
        self.assertTrue(a_sip_message.header.header_fields[55].isPrivacy)
        self.assertTrue(a_sip_message.header.header_fields[56].isProxyAuthenticate)
        self.assertTrue(a_sip_message.header.header_fields[57].isProxyAuthorization)
        self.assertTrue(a_sip_message.header.header_fields[58].isProxyRequire)
        self.assertTrue(a_sip_message.header.header_fields[59].isReason)
        self.assertTrue(a_sip_message.header.header_fields[60].isRecordSessionExpires)
        self.assertTrue(a_sip_message.header.header_fields[61].isReplaces)
        self.assertTrue(a_sip_message.header.header_fields[62].isSubscriptionState)
        self.assertTrue(a_sip_message.header.header_fields[63].isMinExpires)
        self.assertTrue(a_sip_message.header.header_fields[64].isContentLength)

        self.assertTrue(3, len(a_sip_message.vias))
        self.assertTrue(a_sip_message.header.header_fields[4].isMaxForwards)
        self.assertTrue(a_sip_message.header.header_fields[5].isVia)
        self.assertTrue(a_sip_message.header.header_fields[6].isVia)
        self.assertTrue(a_sip_message.header.header_fields[7].isVia)
        self.assertTrue(a_sip_message.header.header_fields[8].isUserAgent)
        self.assertEqual('SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500', a_sip_message.vias[0])
        self.assertEqual('SIP/2.0/TLS 200.25.3.250;branch=z9hG4bKfdkajhdiruyalkghjladksjf', a_sip_message.vias[1])
        self.assertEqual('SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf', a_sip_message.vias[2])

        a_sip_message.header.addHeaderFieldAfterHeaderFieldsOfSameClass(ViaSIPHeaderField.newForAttributes(host='localhost', transport='TLS'))
        self.assertTrue(4, len(a_sip_message.vias))
        self.assertTrue(a_sip_message.header.header_fields[4].isMaxForwards)
        self.assertTrue(a_sip_message.header.header_fields[5].isVia)
        self.assertTrue(a_sip_message.header.header_fields[6].isVia)
        self.assertTrue(a_sip_message.header.header_fields[7].isVia)
        self.assertTrue(a_sip_message.header.header_fields[8].isVia)
        self.assertTrue(a_sip_message.header.header_fields[9].isUserAgent)
        self.assertEqual('SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500', a_sip_message.vias[0])
        self.assertEqual('SIP/2.0/TLS 200.25.3.250;branch=z9hG4bKfdkajhdiruyalkghjladksjf', a_sip_message.vias[1])
        self.assertEqual('SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf', a_sip_message.vias[2])
        self.assertEqual('SIP/2.0/TLS localhost', a_sip_message.vias[3])

        a_sip_message.header.addHeaderFieldBeforeHeaderFieldsOfSameClass(ViaSIPHeaderField.newForAttributes(host='localhost', transport='TCP'))
        self.assertTrue(5, len(a_sip_message.vias))
        self.assertTrue(a_sip_message.header.header_fields[4].isMaxForwards)
        self.assertTrue(a_sip_message.header.header_fields[5].isVia)
        self.assertTrue(a_sip_message.header.header_fields[6].isVia)
        self.assertTrue(a_sip_message.header.header_fields[7].isVia)
        self.assertTrue(a_sip_message.header.header_fields[8].isVia)
        self.assertTrue(a_sip_message.header.header_fields[9].isVia)
        self.assertTrue(a_sip_message.header.header_fields[10].isUserAgent)
        self.assertEqual('SIP/2.0/TCP localhost', a_sip_message.vias[0])
        self.assertEqual('SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500', a_sip_message.vias[1])
        self.assertEqual('SIP/2.0/TLS 200.25.3.250;branch=z9hG4bKfdkajhdiruyalkghjladksjf', a_sip_message.vias[2])
        self.assertEqual('SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf', a_sip_message.vias[3])
        self.assertEqual('SIP/2.0/TLS localhost', a_sip_message.vias[4])

        a_sip_message.header.removeFirstHeaderFieldOfClass(ViaSIPHeaderField)
        self.assertTrue(4, len(a_sip_message.vias))
        self.assertTrue(a_sip_message.header.header_fields[4].isMaxForwards)
        self.assertTrue(a_sip_message.header.header_fields[5].isVia)
        self.assertTrue(a_sip_message.header.header_fields[6].isVia)
        self.assertTrue(a_sip_message.header.header_fields[7].isVia)
        self.assertTrue(a_sip_message.header.header_fields[8].isVia)
        self.assertTrue(a_sip_message.header.header_fields[9].isUserAgent)
        self.assertEqual('SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500', a_sip_message.vias[0])
        self.assertEqual('SIP/2.0/TLS 200.25.3.250;branch=z9hG4bKfdkajhdiruyalkghjladksjf', a_sip_message.vias[1])
        self.assertEqual('SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf', a_sip_message.vias[2])
        self.assertEqual('SIP/2.0/TLS localhost', a_sip_message.vias[3])

        # TODO:  test adding and removing header field of class that doesn't already exist in header.

        for via in a_sip_message.header.viaHeaderFields:
            via.generateInvariantBranchForSIPHeader(a_sip_message.header)
            self.assertIsInstance(via.branch, basestring)


