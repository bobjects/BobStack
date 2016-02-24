try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from unittest import TestCase
import inspect
import sys
sys.path.append("..")
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


class AbstractSIPMessageTestCase(TestCase):
    @property
    def canonicalStrings(self):
        answer = []
        for startLineString in self.canonicalStartLineStrings:
            messageStringIO = StringIO()
            messageStringIO.write(startLineString)
            messageStringIO.write("\r\n")
            for headerFieldString in self.canonicalHeaderFieldStrings:
                messageStringIO.write(headerFieldString)
                messageStringIO.write("\r\n")
            messageStringIO.write("\r\n")
            messageStringIO.write(self.canonicalContent)
            answer.append(messageStringIO.getvalue())
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
                'Via: SIP/2.0/TLS 200.25.3.250;branch=fdkajhdiruyalkghjladksjf',
                'Via: SIP/2.0/TLS 200.25.3.255;branch=duyroiuryaludhgviukfhlasf',
                'User-Agent: Example User Agent',
                'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>',
                'Route: <sip:200.30.10.12:5061;transport=tls;lr>',
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
                'Content-Length: 11']  # This last one actually instantiates a ContentLengthSIPHeaderField.

    # TODO:  Do we want to test different contents?  If so, our assertions need to be aware of that.
    @property
    def canonicalContent(self):
        return 'Foo Content'

    @property
    def oneBigHeaderStringForAssertion(self):
        answer = ('From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                    'To: <sip:example.com:5061>\r\n'
                    'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                    'CSeq: 6711 SIPMETHODTOREPLACE\r\n'
                    'Max-Forwards: 70\r\n'
                    'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                    'Via: SIP/2.0/TLS 200.25.3.250;branch=fdkajhdiruyalkghjladksjf\r\n'
                    'Via: SIP/2.0/TLS 200.25.3.255;branch=duyroiuryaludhgviukfhlasf\r\n'
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
                    'Content-Length: 11')  # This last one actually instantiates a ContentLengthSIPHeaderField.
        return answer.replace("SIPMETHODTOREPLACE", self.sipMethodString)


    @property
    def listOfHeaderFieldsForAssertion(self):
        return [
            FromSIPHeaderField.newForAttributes(fieldValue='<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
            ToSIPHeaderField.newForAttributes(fieldValue='<sip:example.com:5061>'),
            CallIDSIPHeaderField.newForAttributes(fieldValue='0ee8d3e272e31c9195299efc500'),
            CSeqSIPHeaderField.newForAttributes(fieldValue='6711 ' + self.sipMethodString),
            MaxForwardsSIPHeaderField.newForAttributes(value=70),
            ViaSIPHeaderField.newForAttributes(fieldValue='SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
            ViaSIPHeaderField.newForAttributes(fieldValue='SIP/2.0/TLS 200.25.3.250;branch=fdkajhdiruyalkghjladksjf'),
            ViaSIPHeaderField.newForAttributes(fieldValue='SIP/2.0/TLS 200.25.3.255;branch=duyroiuryaludhgviukfhlasf'),
            UserAgentSIPHeaderField.newForAttributes(fieldValue='Example User Agent'),
            ContactSIPHeaderField.newForAttributes(fieldValue='<sip:invalid@200.25.3.150:5061;transport=tls>'),
            RouteSIPHeaderField.newForAttributes(fieldValue='<sip:200.30.10.12:5061;transport=tls;lr>'),
            ExpiresSIPHeaderField.newForAttributes(value=0),
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
            RetryAfterSIPHeaderField.newForAttributes(value=30),
            ServerSIPHeaderField.newForAttributes(fieldValue='Blargomatic 2.0'),
            # TODO:  We will need to deal with the refresher parameter, i.e. we will need to
            # be able to specify parameter dictionaries to the newForAttributes method for
            # Integer header fields.  Maybe even more generically; for all SIP header fields.
            # SessionExpiresSIPHeaderField.newForAttributes(fieldValue='1200;refresher=uac'),
            SessionExpiresSIPHeaderField.newForAttributes(value=1200),
            SupportedSIPHeaderField.newForAttributes(fieldValue='100rel,histinfo,join,replaces,sdp-anat,timer'),
            TimestampSIPHeaderField.newForAttributes(value=1392061773),
            WWWAuthenticateSIPHeaderField.newForAttributes(fieldValue='Digest algorithm=MD5,nonce="1111790769596",realm="SomeRealm"'),
            WarningSIPHeaderField.newForAttributes(fieldValue='370 200.21.3.10 "Insufficient Bandwidth"'),
            UnknownSIPHeaderField.newForAttributes(fieldName='X-RTP-Stat', fieldValue=' PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048'),
            UnknownSIPHeaderField.newForAttributes(fieldName='x-channel', fieldValue=' ds/ds1-3/12;IP=132.52.127.16'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Referred-By', fieldValue='<sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Refer-To', fieldValue='<sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>'),
            ContentLengthSIPHeaderField.newForAttributes(value=11)]

    @property
    def listOfHeaderFieldStringsForAssertion(self):
        return ['From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500',
                        'To: <sip:example.com:5061>',
                        'Call-ID: 0ee8d3e272e31c9195299efc500',
                        'CSeq: 6711 ' + self.sipMethodString,
                        'Max-Forwards: 70',
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500',
                        'Via: SIP/2.0/TLS 200.25.3.250;branch=fdkajhdiruyalkghjladksjf',
                        'Via: SIP/2.0/TLS 200.25.3.255;branch=duyroiuryaludhgviukfhlasf',
                        'User-Agent: Example User Agent',
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>',
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>',
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
                        'Content-Length: 11']  # This last one actually instantiates a ContentLengthSIPHeaderField.

    @property
    def listOfHeaderFieldNamesAndValuesForAssertion(self):
        return [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 ' + self.sipMethodString),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('Via', 'SIP/2.0/TLS 200.25.3.250;branch=fdkajhdiruyalkghjladksjf'),
                        ('Via', 'SIP/2.0/TLS 200.25.3.255;branch=duyroiuryaludhgviukfhlasf'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
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
                        ('Content-Length', 11)]  # This last one actually instantiates a ContentLengthSIPHeaderField.

    @property
    def listOfHeaderFieldNamesAndValuesUsingPropertyDictForAssertion(self):
        return [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 ' + self.sipMethodString),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('Via', 'SIP/2.0/TLS 200.25.3.250;branch=fdkajhdiruyalkghjladksjf'),
                        ('Via', 'SIP/2.0/TLS 200.25.3.255;branch=duyroiuryaludhgviukfhlasf'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
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
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.

    def runAssertionsForSIPMessage(self, aSIPMessage):
        self.assertEqual(aSIPMessage.rawString, self.canonicalStrings[0])
        self.assertIsNotNone(aSIPMessage.header.contentLengthHeaderField)
        self.assertEqual(11, aSIPMessage.header.contentLength)
        self.assertEqual(3, aSIPMessage.header.viaHeaderFields.__len__())
        self.assertEqual(3, aSIPMessage.header.vias.__len__())
        # TODO: assert other headers besides just content-length and via.
        self.assertEqual('SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500', aSIPMessage.header.vias[0])
        self.assertEqual('SIP/2.0/TLS 200.25.3.250;branch=fdkajhdiruyalkghjladksjf', aSIPMessage.header.vias[1])
        self.assertEqual('SIP/2.0/TLS 200.25.3.255;branch=duyroiuryaludhgviukfhlasf', aSIPMessage.header.vias[2])
        self.assertEqual(4, aSIPMessage.header.unknownHeaderFields.__len__())
        self.assertEqual('Foo Content', aSIPMessage.content)
