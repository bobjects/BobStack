from unittest import TestCase
from ..sipmessaging import SIPMessageFactory
from ..siptransport import SimulatedSIPTransport
from ..sipentity import SIPStatelessProxy
from ..siptransport import SimulatedNetwork


class TestRFC4475SIPTortureTest(TestCase):
    @property
    def weHaveImplementedCompactHeaders(self):
        return True

    def testShortTortuousINVITE(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.1.1
        # wsinv.dat
        message_string = (
            'INVITE sip:vivekg@chair-dnrc.example.com;unknownparam SIP/2.0\r\n'
            'TO :\r\n'
            ' sip:vivekg@chair-dnrc.example.com ;   tag    = 1918181833n\r\n'
            'from   : "J Rosenberg \\\""       <sip:jdrosen@example.com>\r\n'
            '  ;\r\n'
            '  tag = 98asjd8\r\n'
            'MaX-fOrWaRdS: 0068\r\n'
            'Call-ID: wsinv.ndaksdj@192.0.2.1\r\n'
            'Content-Length   : 150\r\n'
            'cseq: 0009\r\n'
            '  INVITE\r\n'
            'Via  : SIP  /   2.0\r\n'
            ' /UDP\r\n'
            '    192.0.2.2;branch=390skdjuw\r\n'
            's :\r\n'
            'NewFangledHeader:   newfangled value\r\n'
            ' continued newfangled value\r\n'
            'UnknownHeaderWithUnusualValue: ;;,,;;,;\r\n'
            'Content-Type: application/sdp\r\n'
            'Route:\r\n'
            ' <sip:services.example.com;lr;unknownwith=value;unknown-no-value>\r\n'
            'v:  SIP  / 2.0  / TCP     spindle.example.com   ;\r\n'
            '  branch  =   z9hG4bK9ikj8  ,\r\n'
            ' SIP  /    2.0   / UDP  192.168.255.111   ; branch=\r\n'
            ' z9hG4bK30239\r\n'
            'm:"Quoted string \"\"" <sip:jdrosen@example.com> ; newparam =\r\n'
            '      newvalue ;\r\n'
            '  secondparam ; q = 0.33\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.3\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.4\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # is this valid?  It was considered valid before we implemented compact headers.
        # TODO: Looks like we're not parsing that Contact header well.
        # self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 14)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_content_length)
        self.assertTrue(message.header.header_fields[5].is_cseq)
        self.assertTrue(message.header.header_fields[6].is_via)
        self.assertTrue(message.header.header_fields[7].is_subject)
        self.assertTrue(message.header.header_fields[8].is_unknown)
        self.assertTrue(message.header.header_fields[9].is_unknown)
        self.assertTrue(message.header.header_fields[10].is_content_type)
        self.assertTrue(message.header.header_fields[11].is_route)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[12].is_via)
            self.assertTrue(message.header.header_fields[13].is_contact)
        self.assertEqual('TO : sip:vivekg@chair-dnrc.example.com ;   tag    = 1918181833n', message.header.to_header_field.raw_string)
        # TODO: To tag is not being parsed correctly?
        # self.assertEqual('1918181833n', message.header.to_tag)
        # TODO - more.

    def testWideRangeOfValidCharacters(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.1.2
        # intmeth
        # Note:  this message string has weird characters.  Need to deal with that.
        pass
        # TODO - more.

    def testValidUseOfThePercentEscapingMechanism(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.1.3
        # esc01
        message_string = (
            'INVITE sip:sips%3Auser%40example.com@example.net SIP/2.0\r\n'
            'To: sip:%75se%72@example.com\r\n'
            'From: <sip:I%20have%20spaces@example.net>;tag=938\r\n'
            'Max-Forwards: 87\r\n'
            'i: esc01.239409asdfakjkn23onasd0-3234\r\n'
            'CSeq: 234234 INVITE\r\n'
            'Via: SIP/2.0/UDP host5.example.net;branch=z9hG4bKkdjuw\r\n'
            'C: application/sdp\r\n'
            'Contact:\r\n'
            '  <sip:cal%6Cer@host5.example.net;%6C%72;n%61me=v%61lue%25%34%31>\r\n'
            'Content-Length: 150\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.1\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.1\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 9)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_via)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[6].is_content_type)
        self.assertTrue(message.header.header_fields[7].is_contact)
        self.assertTrue(message.header.header_fields[8].is_content_length)
        # TODO - more.

    def testEscapedNullsInURIs(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.1.4
        # escnull
        message_string = (
            'REGISTER sip:example.com SIP/2.0\r\n'
            'To: sip:null-%00-null@example.com\r\n'
            'From: sip:null-%00-null@example.com;tag=839923423\r\n'
            'Max-Forwards: 70\r\n'
            'Call-ID: escnull.39203ndfvkjdasfkq3w4otrq0adsfdfnavd\r\n'
            'CSeq: 14398234 REGISTER\r\n'
            'Via: SIP/2.0/UDP host5.example.com;branch=z9hG4bKkdjuw\r\n'
            'Contact: <sip:%00@host5.example.com>\r\n'
            'Contact: <sip:%00%00@host5.example.com>\r\n'
            'L:0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 9)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_via)
        self.assertTrue(message.header.header_fields[6].is_contact)
        self.assertTrue(message.header.header_fields[7].is_contact)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[8].is_content_length)
        # TODO - more.

    def testUseOfPercentWhenItIsNotAnEscape(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.1.5
        # esc02
        message_string = (
            'RE%47IST%45R sip:registrar.example.com SIP/2.0\r\n'
            'To: "%Z%45" <sip:resource@example.com>\r\n'
            'From: "%Z%45" <sip:resource@example.com>;tag=f232jadfj23\r\n'
            'Call-ID: esc02.asdfnqwo34rq23i34jrjasdcnl23nrlknsdf\r\n'
            'Via: SIP/2.0/TCP host.example.com;branch=z9hG4bK209%fzsnel234\r\n'
            'CSeq: 29344 RE%47IST%45R\r\n'
            'Max-Forwards: 70\r\n'
            'Contact: <sip:alias1@host1.example.com>\r\n'
            'C%6Fntact: <sip:alias2@host2.example.com>\r\n'
            'Contact: <sip:alias3@host3.example.com>\r\n'
            'l: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 10)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_call_id)
        self.assertTrue(message.header.header_fields[3].is_via)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_max_forwards)
        self.assertTrue(message.header.header_fields[6].is_contact)
        # TODO:  Looks like we need to handle character escaping...
        # self.assertTrue(message.header.header_fields[7].is_contact)
        self.assertTrue(message.header.header_fields[8].is_contact)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[9].is_content_length)
        # TODO - more.

    def testMessageWithNoLWSBetweenDisplayNameAndAngleBracket(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.1.6
        # lwsdisp
        message_string = (
            'OPTIONS sip:user@example.com SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: caller<sip:caller@example.com>;tag=323\r\n'
            'Max-Forwards: 70\r\n'
            'Call-ID: lwsdisp.1234abcd@funky.example.com\r\n'
            'CSeq: 60 OPTIONS\r\n'
            'Via: SIP/2.0/UDP funky.example.com;branch=z9hG4bKkdjuw\r\n'
            'l: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 7)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_via)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[6].is_content_length)
        # TODO - more.

    def testLongValuesInHeaderFields(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.1.7
        # longreq
        message_string = (
            'INVITE sip:user@example.com SIP/2.0\r\n'
            'To: "I have a user name of extremeextremeextremeextremeextremeextremeextremeextremeextremeextreme proportion"<sip:user@example.com:6000;unknownparam1=verylonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglongvalue;longparamnamenamenamenamenamenamenamenamenamenamenamenamenamenamenamenamenamenamenamenamenamenamenamenamename=shortvalue;verylonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglongParameterNameWithNoValue>\r\n'
            'F: sip:amazinglylongcallernameamazinglylongcallernameamazinglylongcallernameamazinglylongcallernameamazinglylongcallername@example.net;tag=12982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982982424;unknownheaderparamnamenamenamenamenamenamenamenamenamenamenamenamenamenamenamenamenamenamenamename=unknowheaderparamvaluevaluevaluevaluevaluevaluevaluevaluevaluevaluevaluevaluevaluevaluevalue;unknownValuelessparamnameparamnameparamnameparamnameparamnameparamnameparamnameparamnameparamnameparamname\r\n'
            'Call-ID: longreq.onereallyreallyreallyreallyreallyreallyreallyreallyreallyreallyreallyreallyreallyreallyreallyreallyreallyreallyreallyreallylongcallid\r\n'
            'CSeq: 3882340 INVITE\r\n'
            'Unknown-LongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLong-Name: unknown-longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong-value; unknown-longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong-parameter-name = unknown-longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong-parameter-value\r\n'
            'Via: SIP/2.0/TCP sip33.example.com\r\n'
            'v: SIP/2.0/TCP sip32.example.com\r\n'
            'V: SIP/2.0/TCP sip31.example.com\r\n'
            'Via: SIP/2.0/TCP sip30.example.com\r\n'
            'ViA: SIP/2.0/TCP sip29.example.com\r\n'
            'VIa: SIP/2.0/TCP sip28.example.com\r\n'
            'VIA: SIP/2.0/TCP sip27.example.com\r\n'
            'via: SIP/2.0/TCP sip26.example.com\r\n'
            'viA: SIP/2.0/TCP sip25.example.com\r\n'
            'vIa: SIP/2.0/TCP sip24.example.com\r\n'
            'vIA: SIP/2.0/TCP sip23.example.com\r\n'
            'V :  SIP/2.0/TCP sip22.example.com\r\n'
            'v :  SIP/2.0/TCP sip21.example.com\r\n'
            'V  : SIP/2.0/TCP sip20.example.com\r\n'
            'v  : SIP/2.0/TCP sip19.example.com\r\n'
            'Via : SIP/2.0/TCP sip18.example.com\r\n'
            'Via  : SIP/2.0/TCP sip17.example.com\r\n'
            'Via: SIP/2.0/TCP sip16.example.com\r\n'
            'Via: SIP/2.0/TCP sip15.example.com\r\n'
            'Via: SIP/2.0/TCP sip14.example.com\r\n'
            'Via: SIP/2.0/TCP sip13.example.com\r\n'
            'Via: SIP/2.0/TCP sip12.example.com\r\n'
            'Via: SIP/2.0/TCP sip11.example.com\r\n'
            'Via: SIP/2.0/TCP sip10.example.com\r\n'
            'Via: SIP/2.0/TCP sip9.example.com\r\n'
            'Via: SIP/2.0/TCP sip8.example.com\r\n'
            'Via: SIP/2.0/TCP sip7.example.com\r\n'
            'Via: SIP/2.0/TCP sip6.example.com\r\n'
            'Via: SIP/2.0/TCP sip5.example.com\r\n'
            'Via: SIP/2.0/TCP sip4.example.com\r\n'
            'Via: SIP/2.0/TCP sip3.example.com\r\n'
            'Via: SIP/2.0/TCP sip2.example.com\r\n'
            'Via: SIP/2.0/TCP sip1.example.com\r\n'
            'Via: SIP/2.0/TCP host.example.com;received=192.0.2.5;branch=verylonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglongbranchvalue\r\n'
            'Max-Forwards: 70\r\n'
            'Contact: <sip:amazinglylongcallernameamazinglylongcallernameamazinglylongcallernameamazinglylongcallernameamazinglylongcallername@host5.example.net>\r\n'
            'Content-Type: application/sdp\r\n'
            'l: 150\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.1\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.1\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO - should this be considered valid?
        # self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 43)
        self.assertTrue(message.header.header_fields[0].is_to)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_call_id)
        self.assertTrue(message.header.header_fields[3].is_cseq)
        self.assertTrue(message.header.header_fields[4].is_unknown)
        self.assertTrue(message.header.header_fields[5].is_via)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[6].is_via)
            self.assertTrue(message.header.header_fields[7].is_via)
        self.assertTrue(message.header.header_fields[8].is_via)
        self.assertTrue(message.header.header_fields[9].is_via)
        self.assertTrue(message.header.header_fields[10].is_via)
        self.assertTrue(message.header.header_fields[11].is_via)
        self.assertTrue(message.header.header_fields[12].is_via)
        self.assertTrue(message.header.header_fields[13].is_via)
        self.assertTrue(message.header.header_fields[14].is_via)
        self.assertTrue(message.header.header_fields[15].is_via)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[16].is_via)
            self.assertTrue(message.header.header_fields[17].is_via)
            self.assertTrue(message.header.header_fields[18].is_via)
            self.assertTrue(message.header.header_fields[19].is_via)
        self.assertTrue(message.header.header_fields[20].is_via)
        self.assertTrue(message.header.header_fields[21].is_via)
        self.assertTrue(message.header.header_fields[22].is_via)
        self.assertTrue(message.header.header_fields[23].is_via)
        self.assertTrue(message.header.header_fields[24].is_via)
        self.assertTrue(message.header.header_fields[25].is_via)
        self.assertTrue(message.header.header_fields[26].is_via)
        self.assertTrue(message.header.header_fields[27].is_via)
        self.assertTrue(message.header.header_fields[28].is_via)
        self.assertTrue(message.header.header_fields[29].is_via)
        self.assertTrue(message.header.header_fields[30].is_via)
        self.assertTrue(message.header.header_fields[31].is_via)
        self.assertTrue(message.header.header_fields[32].is_via)
        self.assertTrue(message.header.header_fields[33].is_via)
        self.assertTrue(message.header.header_fields[34].is_via)
        self.assertTrue(message.header.header_fields[35].is_via)
        self.assertTrue(message.header.header_fields[36].is_via)
        self.assertTrue(message.header.header_fields[37].is_via)
        self.assertTrue(message.header.header_fields[38].is_via)
        self.assertTrue(message.header.header_fields[39].is_max_forwards)
        self.assertTrue(message.header.header_fields[40].is_contact)
        self.assertTrue(message.header.header_fields[41].is_content_type)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[42].is_content_length)
        # TODO - more.

    def testExtraTrailingOctetsInAUDPDatagram(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.1.8
        # dblreq
        message_string = (
            'REGISTER sip:example.com SIP/2.0\r\n'
            'To: sip:j.user@example.com\r\n'
            'From: sip:j.user@example.com;tag=43251j3j324\r\n'
            'Max-Forwards: 8\r\n'
            'I: dblreq.0ha0isndaksdj99sdfafnl3lk233412\r\n'
            'Contact: sip:j.user@host.example.com\r\n'
            'CSeq: 8 REGISTER\r\n'
            'Via: SIP/2.0/UDP 192.0.2.125;branch=z9hG4bKkdjuw23492\r\n'
            'Content-Length: 0\r\n'
            '\r\n'
            '\r\n'
            'INVITE sip:joe@example.com SIP/2.0\r\n'
            't: sip:joe@example.com\r\n'
            'From: sip:caller@example.net;tag=141334\r\n'
            'Max-Forwards: 8\r\n'
            'Call-ID: dblreq.0ha0isnda977644900765@192.0.2.15\r\n'
            'CSeq: 8 INVITE\r\n'
            'Via: SIP/2.0/UDP 192.0.2.15;branch=z9hG4bKkdjuw380234\r\n'
            'Content-Type: application/sdp\r\n'
            'Content-Length: 150\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.15\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.15\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm =video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertFalse(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 8)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_contact)
        self.assertTrue(message.header.header_fields[5].is_cseq)
        self.assertTrue(message.header.header_fields[6].is_via)
        self.assertTrue(message.header.header_fields[7].is_content_length)
        # TODO - more.

    def testSemicolonSeparatedParametersInURIUserPart(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.1.9
        # semiuri
        message_string = (
            'OPTIONS sip:user;par=u%40example.net@example.com SIP/2.0\r\n'
            'To: sip:j_user@example.com\r\n'
            'From: sip:caller@example.org;tag=33242\r\n'
            'Max-Forwards: 3\r\n'
            'Call-ID: semiuri.0ha0isndaksdj\r\n'
            'CSeq: 8 OPTIONS\r\n'
            'Accept: application/sdp, application/pkcs7-mime,\r\n'
            '        multipart/mixed, multipart/signed,\r\n'
            '        message/sip, message/sipfrag\r\n'
            'Via: SIP/2.0/UDP 192.0.2.1;branch=z9hG4bKkdjuw\r\n'
            'l: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 8)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_accept)
        self.assertTrue(message.header.header_fields[6].is_via)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[7].is_content_length)
        # TODO - more.

    def testVariedAndUnknownTransportTypes(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.1.10
        # transports
        message_string = (
            'OPTIONS sip:user@example.com SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: <sip:caller@example.com>;tag=323\r\n'
            'Max-Forwards: 70\r\n'
            'Call-ID:  transports.kijh4akdnaqjkwendsasfdj\r\n'
            'Accept: application/sdp\r\n'
            'CSeq: 60 OPTIONS\r\n'
            'Via: SIP/2.0/UDP t1.example.com;branch=z9hG4bKkdjuw\r\n'
            'Via: SIP/2.0/SCTP t2.example.com;branch=z9hG4bKklasjdhf\r\n'
            'Via: SIP/2.0/TLS t3.example.com;branch=z9hG4bK2980unddj\r\n'
            'Via: SIP/2.0/UNKNOWN t4.example.com;branch=z9hG4bKasd0f3en\r\n'
            'Via: SIP/2.0/TCP t5.example.com;branch=z9hG4bK0a9idfnee\r\n'
            'l: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 12)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_accept)
        self.assertTrue(message.header.header_fields[5].is_cseq)
        self.assertTrue(message.header.header_fields[6].is_via)
        self.assertTrue(message.header.header_fields[7].is_via)
        self.assertTrue(message.header.header_fields[8].is_via)
        self.assertTrue(message.header.header_fields[9].is_via)
        self.assertTrue(message.header.header_fields[10].is_via)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[11].is_content_length)
        # TODO - more.

    def testMultipartMIMEMessage(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.1.11
        # mpart01
        # Note:  this message string has weird characters.  Need to deal with that.
        pass
        # TODO - more.

    def testUnusualReasonPhrase(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.1.12
        # unreason
        # Note:  this message string has weird characters.  Need to deal with that.
        pass
        # TODO - more.

    def testEmptyReasonPhrase(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.1.13
        # noreason
        message_string = (
            'SIP/2.0 100 \r\n'
            'Via: SIP/2.0/UDP 192.0.2.105;branch=z9hG4bK2398ndaoe\r\n'
            'Call-ID: noreason.asndj203insdf99223ndf\r\n'
            'CSeq: 35 INVITE\r\n'
            'From: <sip:user@example.com>;tag=39ansfi3\r\n'
            'To: <sip:user@example.edu>;tag=902jndnke3\r\n'
            'Content-Length: 0\r\n'
            'Contact: <sip:user@host105.example.com>\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO - is this valid?
        # self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 7)
        self.assertTrue(message.header.header_fields[0].is_via)
        self.assertTrue(message.header.header_fields[1].is_call_id)
        self.assertTrue(message.header.header_fields[2].is_cseq)
        self.assertTrue(message.header.header_fields[3].is_from)
        self.assertTrue(message.header.header_fields[4].is_to)
        self.assertTrue(message.header.header_fields[5].is_content_length)
        self.assertTrue(message.header.header_fields[6].is_contact)
        # TODO - more.

    def testExtraneousHeaderFieldSeparators(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.1
        # badinv01
        message_string = (
            'INVITE sip:user@example.com SIP/2.0\r\n'
            'To: sip:j.user@example.com\r\n'
            'From: sip:caller@example.net;tag=134161461246\r\n'
            'Max-Forwards: 7\r\n'
            'Call-ID: badinv01.0ha0isndaksdjasdf3234nas\r\n'
            'CSeq: 8 INVITE\r\n'
            'Via: SIP/2.0/UDP 192.0.2.15;;,;,,\r\n'
            'Contact: "Joe" <sip:joe@example.org>;;;;\r\n'
            'Content-Length: 152\r\n'
            'Content-Type: application/sdp\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.15\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.15\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO - is this valid?
        # self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 9)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_via)
        self.assertTrue(message.header.header_fields[6].is_contact)
        self.assertTrue(message.header.header_fields[7].is_content_length)
        self.assertTrue(message.header.header_fields[8].is_content_type)
        # TODO - more.

    def testContentLengthLargerThanMessage(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.2
        # clerr
        message_string = (
            'INVITE sip:user@example.com SIP/2.0\r\n'
            'Max-Forwards: 80\r\n'
            'To: sip:j.user@example.com\r\n'
            'From: sip:caller@example.net;tag=93942939o2\r\n'
            'Contact: <sip:caller@hungry.example.net>\r\n'
            'Call-ID: clerr.0ha0isndaksdjweiafasdk3\r\n'
            'CSeq: 8 INVITE\r\n'
            'Via: SIP/2.0/UDP host5.example.com;branch=z9hG4bK-39234-23523\r\n'
            'Content-Type: application/sdp\r\n'
            'Content-Length: 9999\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.155\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.155\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO - is this valid?
        # self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 9)
        self.assertTrue(message.header.header_fields[0].is_max_forwards)
        self.assertTrue(message.header.header_fields[1].is_to)
        self.assertTrue(message.header.header_fields[2].is_from)
        self.assertTrue(message.header.header_fields[3].is_contact)
        self.assertTrue(message.header.header_fields[4].is_call_id)
        self.assertTrue(message.header.header_fields[5].is_cseq)
        self.assertTrue(message.header.header_fields[6].is_via)
        self.assertTrue(message.header.header_fields[7].is_content_type)
        self.assertTrue(message.header.header_fields[8].is_content_length)
        # TODO - more.

    def testNegativeContentLength(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.3
        # ncl
        message_string = (
            'INVITE sip:user@example.com SIP/2.0\r\n'
            'Max-Forwards: 254\r\n'
            'To: sip:j.user@example.com\r\n'
            'From: sip:caller@example.net;tag=32394234\r\n'
            'Call-ID: ncl.0ha0isndaksdj2193423r542w35\r\n'
            'CSeq: 0 INVITE\r\n'
            'Via: SIP/2.0/UDP 192.0.2.53;branch=z9hG4bKkdjuw\r\n'
            'Contact: <sip:caller@example53.example.net>\r\n'
            'Content-Type: application/sdp\r\n'
            'Content-Length: -999\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.53\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.53\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO - is this valid?
        # self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 9)
        self.assertTrue(message.header.header_fields[0].is_max_forwards)
        self.assertTrue(message.header.header_fields[1].is_to)
        self.assertTrue(message.header.header_fields[2].is_from)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_via)
        self.assertTrue(message.header.header_fields[6].is_contact)
        self.assertTrue(message.header.header_fields[7].is_content_type)
        self.assertTrue(message.header.header_fields[8].is_content_length)
        # TODO - more.

    def testRequestScalarFieldsWithOverlargeValues(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.4
        # scalar02
        message_string = (
            'REGISTER sip:example.com SIP/2.0\r\n'
            'Via: SIP/2.0/TCP host129.example.com;branch=z9hG4bK342sdfoi3\r\n'
            'To: <sip:user@example.com>\r\n'
            'From: <sip:user@example.com>;tag=239232jh3\r\n'
            'CSeq: 36893488147419103232 REGISTER\r\n'
            'Call-ID: scalar02.23o0pd9vanlq3wnrlnewofjas9ui32\r\n'
            'Max-Forwards: 300\r\n'
            'Expires: 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\r\n'
            'Contact: <sip:user@host129.example.com>\r\n'
            '  ;expires=280297596632815\r\n'
            'Content-Length: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 9)
        self.assertTrue(message.header.header_fields[0].is_via)
        self.assertTrue(message.header.header_fields[1].is_to)
        self.assertTrue(message.header.header_fields[2].is_from)
        self.assertTrue(message.header.header_fields[3].is_cseq)
        self.assertTrue(message.header.header_fields[4].is_call_id)
        self.assertTrue(message.header.header_fields[5].is_max_forwards)
        self.assertTrue(message.header.header_fields[6].is_expires)
        self.assertTrue(message.header.header_fields[7].is_contact)
        self.assertTrue(message.header.header_fields[8].is_content_length)
        # TODO - more.

    def testResponseScalarFieldsWithOverlargeValues(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.5
        # scalarlg
        message_string = (
            'SIP/2.0 503 Service Unavailable\r\n'
            'Via: SIP/2.0/TCP host129.example.com;branch=z9hG4bKzzxdiwo34sw;received=192.0.2.129\r\n'
            'To: <sip:user@example.com>\r\n'
            'From: <sip:other@example.net>;tag=2easdjfejw\r\n'
            'CSeq: 9292394834772304023312 OPTIONS\r\n'
            'Call-ID: scalarlg.noase0of0234hn2qofoaf0232aewf2394r\r\n'
            'Retry-After: 949302838503028349304023988\r\n'
            'Warning: 1812 overture "In Progress"\r\n'
            'Content-Length: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 8)
        self.assertTrue(message.header.header_fields[0].is_via)
        self.assertTrue(message.header.header_fields[1].is_to)
        self.assertTrue(message.header.header_fields[2].is_from)
        self.assertTrue(message.header.header_fields[3].is_cseq)
        self.assertTrue(message.header.header_fields[4].is_call_id)
        self.assertTrue(message.header.header_fields[5].is_retry_after)
        self.assertTrue(message.header.header_fields[6].is_warning)
        self.assertTrue(message.header.header_fields[7].is_content_length)
        # TODO - more.

    def testUnterminatedQuotedStringInDisplayName(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.6
        # quotbal
        message_string = (
            'INVITE sip:user@example.com SIP/2.0\r\n'
            'To: "Mr. J. User <sip:j.user@example.com>\r\n'
            'From: sip:caller@example.net;tag=93334\r\n'
            'Max-Forwards: 10\r\n'
            'Call-ID: quotbal.aksdj\r\n'
            'Contact: <sip:caller@host59.example.net>\r\n'
            'CSeq: 8 INVITE\r\n'
            'Via: SIP/2.0/UDP 192.0.2.59:5050;branch=z9hG4bKkdjuw39234\r\n'
            'Content-Type: application/sdp\r\n'
            'Content-Length: 152\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.15\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.15\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 9)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_contact)
        self.assertTrue(message.header.header_fields[5].is_cseq)
        self.assertTrue(message.header.header_fields[6].is_via)
        self.assertTrue(message.header.header_fields[7].is_content_type)
        self.assertTrue(message.header.header_fields[8].is_content_length)
        # TODO - more.

    def testAngleBracketEnclosingRequestURI(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.7
        # ltgtruri
        message_string = (
            'INVITE <sip:user@example.com> SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:caller@example.net;tag=39291\r\n'
            'Max-Forwards: 23\r\n'
            'Call-ID: ltgtruri.1@192.0.2.5\r\n'
            'CSeq: 1 INVITE\r\n'
            'Via: SIP/2.0/UDP 192.0.2.5\r\n'
            'Contact: <sip:caller@host5.example.net>\r\n'
            'Content-Type: application/sdp\r\n'
            'Content-Length: 159\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.5\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.5\r\n'
            't=3149328700 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO - is this valid?
        # self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 9)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_via)
        self.assertTrue(message.header.header_fields[6].is_contact)
        self.assertTrue(message.header.header_fields[7].is_content_type)
        self.assertTrue(message.header.header_fields[8].is_content_length)
        # TODO - more.

    def testMalformedSIPRequestURIEmbeddedLWS(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.8
        # lwsruri
        message_string = (
            'INVITE sip:user@example.com; lr SIP/2.0\r\n'
            'To: sip:user@example.com;tag=3xfe-9921883-z9f\r\n'
            'From: sip:caller@example.net;tag=231413434\r\n'
            'Max-Forwards: 5\r\n'
            'Call-ID: lwsruri.asdfasdoeoi2323-asdfwrn23-asd834rk423\r\n'
            'CSeq: 2130706432 INVITE\r\n'
            'Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bKkdjuw2395\r\n'
            'Contact: <sip:caller@host1.example.net>\r\n'
            'Content-Type: application/sdp\r\n'
            'Content-Length: 159\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.1\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.1\r\n'
            't=3149328700 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO - is this valid?
        # self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 9)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_via)
        self.assertTrue(message.header.header_fields[6].is_contact)
        self.assertTrue(message.header.header_fields[7].is_content_type)
        self.assertTrue(message.header.header_fields[8].is_content_length)
        # TODO - more.

    def testMultipleSPSeparatingRequestLineElements(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.9
        # lwsstart
        message_string = (
            'INVITE  sip:user@example.com  SIP/2.0\r\n'
            'Max-Forwards: 8\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:caller@example.net;tag=8814\r\n'
            'Call-ID: lwsstart.dfknq234oi243099adsdfnawe3@example.com\r\n'
            'CSeq: 1893884 INVITE\r\n'
            'Via: SIP/2.0/UDP host1.example.com;branch=z9hG4bKkdjuw3923\r\n'
            'Contact: <sip:caller@host1.example.net>\r\n'
            'Content-Type: application/sdp\r\n'
            'Content-Length: 150\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.1\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.1\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 9)
        self.assertTrue(message.header.header_fields[0].is_max_forwards)
        self.assertTrue(message.header.header_fields[1].is_to)
        self.assertTrue(message.header.header_fields[2].is_from)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_via)
        self.assertTrue(message.header.header_fields[6].is_contact)
        self.assertTrue(message.header.header_fields[7].is_content_type)
        self.assertTrue(message.header.header_fields[8].is_content_length)
        # TODO - more.

    def testSPCharactersAtEndOfRequestLine(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.10
        # trws
        message_string = (
            'OPTIONS sip:remote-target@example.com SIP/2.0  \r\n'
            'Via: SIP/2.0/TCP host1.examle.com;branch=z9hG4bK299342093\r\n'
            'To: <sip:remote-target@example.com>\r\n'
            'From: <sip:local-resource@example.com>;tag=329429089\r\n'
            'Call-ID: trws.oicu34958239neffasdhr2345r\r\n'
            'Accept: application/sdp\r\n'
            'CSeq: 238923 OPTIONS\r\n'
            'Max-Forwards: 70\r\n'
            'Content-Length: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 8)
        self.assertTrue(message.header.header_fields[0].is_via)
        self.assertTrue(message.header.header_fields[1].is_to)
        self.assertTrue(message.header.header_fields[2].is_from)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_accept)
        self.assertTrue(message.header.header_fields[5].is_cseq)
        self.assertTrue(message.header.header_fields[6].is_max_forwards)
        self.assertTrue(message.header.header_fields[7].is_content_length)
        # TODO - more.

    def testEscapedHeadersInSIPRequestURI(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.11
        # escruri
        message_string = (
            'INVITE sip:user@example.com?Route=%3Csip:example.com%3E SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:caller@example.net;tag=341518\r\n'
            'Max-Forwards: 7\r\n'
            'Contact: <sip:caller@host39923.example.net>\r\n'
            'Call-ID: escruri.23940-asdfhj-aje3br-234q098w-fawerh2q-h4n5\r\n'
            'CSeq: 149209342 INVITE\r\n'
            'Via: SIP/2.0/UDP host-of-the-hour.example.com;branch=z9hG4bKkdjuw\r\n'
            'Content-Type: application/sdp\r\n'
            'Content-Length: 150\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.1\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.1\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 9)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_contact)
        self.assertTrue(message.header.header_fields[4].is_call_id)
        self.assertTrue(message.header.header_fields[5].is_cseq)
        self.assertTrue(message.header.header_fields[6].is_via)
        self.assertTrue(message.header.header_fields[7].is_content_type)
        self.assertTrue(message.header.header_fields[8].is_content_length)
        # TODO - more.

    def testInvalidTimezoneInDateHeaderField(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.12
        # baddate
        message_string = (
            'INVITE sip:user@example.com SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:caller@example.net;tag=2234923\r\n'
            'Max-Forwards: 70\r\n'
            'Call-ID: baddate.239423mnsadf3j23lj42--sedfnm234\r\n'
            'CSeq: 1392934 INVITE\r\n'
            'Via: SIP/2.0/UDP host.example.com;branch=z9hG4bKkdjuw\r\n'
            'Date: Fri, 01 Jan 2010 16:00:00 EST\r\n'
            'Contact: <sip:caller@host5.example.net>\r\n'
            'Content-Type: application/sdp\r\n'
            'Content-Length: 150\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.5\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.5\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 10)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_via)
        self.assertTrue(message.header.header_fields[6].is_date)
        self.assertTrue(message.header.header_fields[7].is_contact)
        self.assertTrue(message.header.header_fields[8].is_content_type)
        self.assertTrue(message.header.header_fields[9].is_content_length)
        # TODO - more.

    def testFailureToEncloseNameAddrURIInAngleBrackets(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.13
        # regbadct
        message_string = (
            'REGISTER sip:example.com SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:user@example.com;tag=998332\r\n'
            'Max-Forwards: 70\r\n'
            'Call-ID: regbadct.k345asrl3fdbv@10.0.0.1\r\n'
            'CSeq: 1 REGISTER\r\n'
            'Via: SIP/2.0/UDP 135.180.130.133:5060;branch=z9hG4bKkdjuw\r\n'
            'Contact: sip:user@example.com?Route=%3Csip:sip.example.com%3E\r\n'
            'l: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO - is this valid?
        # self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 8)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_via)
        self.assertTrue(message.header.header_fields[6].is_contact)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[7].is_content_length)
        # TODO - more.

    def testSpacesWithinAddrSpec(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.14
        # badaspec
        message_string = (
            'OPTIONS sip:user@example.org SIP/2.0\r\n'
            'Via: SIP/2.0/UDP host4.example.com:5060;branch=z9hG4bKkdju43234\r\n'
            'Max-Forwards: 70\r\n'
            'From: "Bell, Alexander" <sip:a.g.bell@example.com>;tag=433423\r\n'
            'To: "Watson, Thomas" < sip:t.watson@example.org >\r\n'
            'Call-ID: badaspec.sdf0234n2nds0a099u23h3hnnw009cdkne3\r\n'
            'Accept: application/sdp\r\n'
            'CSeq: 3923239 OPTIONS\r\n'
            'l: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 8)
        self.assertTrue(message.header.header_fields[0].is_via)
        self.assertTrue(message.header.header_fields[1].is_max_forwards)
        self.assertTrue(message.header.header_fields[2].is_from)
        self.assertTrue(message.header.header_fields[3].is_to)
        self.assertTrue(message.header.header_fields[4].is_call_id)
        self.assertTrue(message.header.header_fields[5].is_accept)
        self.assertTrue(message.header.header_fields[6].is_cseq)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[7].is_content_length)
        # TODO - more.

    def testNonTokenCharactersInDisplayName(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.15
        # baddn
        message_string = (
            'OPTIONS sip:t.watson@example.org SIP/2.0\r\n'
            'Via:     SIP/2.0/UDP c.example.com:5060;branch=z9hG4bKkdjuw\r\n'
            'Max-Forwards:      70\r\n'
            'From:    Bell, Alexander <sip:a.g.bell@example.com>;tag=43\r\n'
            'To:      Watson, Thomas <sip:t.watson@example.org>\r\n'
            'Call-ID: baddn.31415@c.example.com\r\n'
            'Accept: application/sdp\r\n'
            'CSeq:    3923239 OPTIONS\r\n'
            'l: 0\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 8)
        self.assertTrue(message.header.header_fields[0].is_via)
        self.assertTrue(message.header.header_fields[1].is_max_forwards)
        self.assertTrue(message.header.header_fields[2].is_from)
        self.assertTrue(message.header.header_fields[3].is_to)
        self.assertTrue(message.header.header_fields[4].is_call_id)
        self.assertTrue(message.header.header_fields[5].is_accept)
        self.assertTrue(message.header.header_fields[6].is_cseq)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[7].is_content_length)
        # TODO - more.

    def testUnknownProtocolVersion(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.16
        # badvers
        message_string = (
            'OPTIONS sip:t.watson@example.org SIP/7.0\r\n'
            'Via:     SIP/7.0/UDP c.example.com;branch=z9hG4bKkdjuw\r\n'
            'Max-Forwards:     70\r\n'
            'From:    A. Bell <sip:a.g.bell@example.com>;tag=qweoiqpe\r\n'
            'To:      T. Watson <sip:t.watson@example.org>\r\n'
            'Call-ID: badvers.31417@c.example.com\r\n'
            'CSeq:    1 OPTIONS\r\n'
            'l: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO - is this valid?
        # self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 7)
        self.assertTrue(message.header.header_fields[0].is_via)
        self.assertTrue(message.header.header_fields[1].is_max_forwards)
        self.assertTrue(message.header.header_fields[2].is_from)
        self.assertTrue(message.header.header_fields[3].is_to)
        self.assertTrue(message.header.header_fields[4].is_call_id)
        self.assertTrue(message.header.header_fields[5].is_cseq)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[6].is_content_length)
        # TODO - more.

    def testStartLineAndCSeqMethodMismatch(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.17
        # mismatch01
        message_string = (
            'OPTIONS sip:user@example.com SIP/2.0\r\n'
            'To: sip:j.user@example.com\r\n'
            'From: sip:caller@example.net;tag=34525\r\n'
            'Max-Forwards: 6\r\n'
            'Call-ID: mismatch01.dj0234sxdfl3\r\n'
            'CSeq: 8 INVITE\r\n'
            'Via: SIP/2.0/UDP host.example.com;branch=z9hG4bKkdjuw\r\n'
            'l: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 7)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_via)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[6].is_content_length)
        # TODO - more.

    def testUnknownMethodWithCSeqMethodMismatch(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.18
        # mismatch02
        message_string = (
            'NEWMETHOD sip:user@example.com SIP/2.0\r\n'
            'To: sip:j.user@example.com\r\n'
            'From: sip:caller@example.net;tag=34525\r\n'
            'Max-Forwards: 6\r\n'
            'Call-ID: mismatch02.dj0234sxdfl3\r\n'
            'CSeq: 8 INVITE\r\n'
            'Contact: <sip:caller@host.example.net>\r\n'
            'Via: SIP/2.0/UDP host.example.net;branch=z9hG4bKkdjuw\r\n'
            'Content-Type: application/sdp\r\n'
            'l: 138\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.1\r\n'
            'c=IN IP4 192.0.2.1\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO - is this valid?
        # self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 9)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_contact)
        self.assertTrue(message.header.header_fields[6].is_via)
        self.assertTrue(message.header.header_fields[7].is_content_type)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[8].is_content_length)
        # TODO - more.

    def testOverlargeResponseCode(self):
        # https://tools.ietf.org/html/rfc4475#section-3.1.2.19
        # bigcode
        message_string = (
            'SIP/2.0 4294967301 better not break the receiver\r\n'
            'Via: SIP/2.0/UDP 192.0.2.105;branch=z9hG4bK2398ndaoe\r\n'
            'Call-ID: bigcode.asdof3uj203asdnf3429uasdhfas3ehjasdfas9i\r\n'
            'CSeq: 353494 INVITE\r\n'
            'From: <sip:user@example.com>;tag=39ansfi3\r\n'
            'To: <sip:user@example.edu>;tag=902jndnke3\r\n'
            'Content-Length: 0\r\n'
            'Contact: <sip:user@host105.example.com>\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 7)
        self.assertTrue(message.header.header_fields[0].is_via)
        self.assertTrue(message.header.header_fields[1].is_call_id)
        self.assertTrue(message.header.header_fields[2].is_cseq)
        self.assertTrue(message.header.header_fields[3].is_from)
        self.assertTrue(message.header.header_fields[4].is_to)
        self.assertTrue(message.header.header_fields[5].is_content_length)
        self.assertTrue(message.header.header_fields[6].is_contact)
        # TODO - more.

    def testMissingTransactionIdentifier(self):
        # https://tools.ietf.org/html/rfc4475#section-3.2.1
        # badbranch
        message_string = (
            'OPTIONS sip:user@example.com SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:caller@example.org;tag=33242\r\n'
            'Max-Forwards: 3\r\n'
            'Via: SIP/2.0/UDP 192.0.2.1;branch=z9hG4bK\r\n'
            'Accept: application/sdp\r\n'
            'Call-ID: badbranch.sadonfo23i420jv0as0derf3j3n\r\n'
            'CSeq: 8 OPTIONS\r\n'
            'l: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 8)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_via)
        self.assertTrue(message.header.header_fields[4].is_accept)
        self.assertTrue(message.header.header_fields[5].is_call_id)
        self.assertTrue(message.header.header_fields[6].is_cseq)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[7].is_content_length)
        # TODO - more.

    def testMissingRequiredHeaderFields(self):
        # https://tools.ietf.org/html/rfc4475#section-3.3.1
        # insuf
        message_string = (
            'INVITE sip:user@example.com SIP/2.0\r\n'
            'CSeq: 193942 INVITE\r\n'
            'Via: SIP/2.0/UDP 192.0.2.95;branch=z9hG4bKkdj.insuf\r\n'
            'Content-Type: application/sdp\r\n'
            'l: 152\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.95\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.95\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO - is this valid?
        # self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 4)
        self.assertTrue(message.header.header_fields[0].is_cseq)
        self.assertTrue(message.header.header_fields[1].is_via)
        self.assertTrue(message.header.header_fields[2].is_content_type)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[3].is_content_length)
        # TODO - more.

    def testRequestURIWithUnknownScheme(self):
        # https://tools.ietf.org/html/rfc4475#section-3.3.2
        # unkscm
        message_string = (
            'OPTIONS nobodyKnowsThisScheme:totallyopaquecontent SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:caller@example.net;tag=384\r\n'
            'Max-Forwards: 3\r\n'
            'Call-ID: unkscm.nasdfasser0q239nwsdfasdkl34\r\n'
            'CSeq: 3923423 OPTIONS\r\n'
            'Via: SIP/2.0/TCP host9.example.com;branch=z9hG4bKkdjuw39234\r\n'
            'Content-Length: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 7)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_via)
        self.assertTrue(message.header.header_fields[6].is_content_length)
        # TODO - more.

    def testRequestURIWithKnownButAtypicalScheme(self):
        # https://tools.ietf.org/html/rfc4475#section-3.3.3
        # novelsc
        message_string = (
            'OPTIONS soap.beep://192.0.2.103:3002 SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:caller@example.net;tag=384\r\n'
            'Max-Forwards: 3\r\n'
            'Call-ID: novelsc.asdfasser0q239nwsdfasdkl34\r\n'
            'CSeq: 3923423 OPTIONS\r\n'
            'Via: SIP/2.0/TCP host9.example.com;branch=z9hG4bKkdjuw39234\r\n'
            'Content-Length: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 7)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_via)
        self.assertTrue(message.header.header_fields[6].is_content_length)
        # TODO - more.

    def testUnknownURISchemesInHeaderFields(self):
        # https://tools.ietf.org/html/rfc4475#section-3.3.4
        # unksm2
        message_string = (
            'REGISTER sip:example.com SIP/2.0\r\n'
            'To: isbn:2983792873\r\n'
            'From: <http://www.example.com>;tag=3234233\r\n'
            'Call-ID: unksm2.daksdj@hyphenated-host.example.com\r\n'
            'CSeq: 234902 REGISTER\r\n'
            'Max-Forwards: 70\r\n'
            'Via: SIP/2.0/UDP 192.0.2.21:5060;branch=z9hG4bKkdjuw\r\n'
            'Contact: <name:John_Smith>\r\n'
            'l: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 8)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_call_id)
        self.assertTrue(message.header.header_fields[3].is_cseq)
        self.assertTrue(message.header.header_fields[4].is_max_forwards)
        self.assertTrue(message.header.header_fields[5].is_via)
        self.assertTrue(message.header.header_fields[6].is_contact)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[7].is_content_length)
        # TODO - more.

    def testProxyRequireAndRequire(self):
        # https://tools.ietf.org/html/rfc4475#section-3.3.5
        # bext01
        message_string = (
            'OPTIONS sip:user@example.com SIP/2.0\r\n'
            'To: sip:j_user@example.com\r\n'
            'From: sip:caller@example.net;tag=242etr\r\n'
            'Max-Forwards: 6\r\n'
            'Call-ID: bext01.0ha0isndaksdj\r\n'
            'Require: nothingSupportsThis, nothingSupportsThisEither\r\n'
            'Proxy-Require: noProxiesSupportThis, norDoAnyProxiesSupportThis\r\n'
            'CSeq: 8 OPTIONS\r\n'
            'Via: SIP/2.0/TLS fold-and-staple.example.com;branch=z9hG4bKkdjuw\r\n'
            'Content-Length: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 9)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_require)
        self.assertTrue(message.header.header_fields[5].is_proxy_require)
        self.assertTrue(message.header.header_fields[6].is_cseq)
        self.assertTrue(message.header.header_fields[7].is_via)
        self.assertTrue(message.header.header_fields[8].is_content_length)
        # TODO - more.

    def testUnknownContentType(self):
        # https://tools.ietf.org/html/rfc4475#section-3.3.6
        # invut
        message_string = (
            'INVITE sip:user@example.com SIP/2.0\r\n'
            'Contact: <sip:caller@host5.example.net>\r\n'
            'To: sip:j.user@example.com\r\n'
            'From: sip:caller@example.net;tag=8392034\r\n'
            'Max-Forwards: 70\r\n'
            'Call-ID: invut.0ha0isndaksdjadsfij34n23d\r\n'
            'CSeq: 235448 INVITE\r\n'
            'Via: SIP/2.0/UDP somehost.example.com;branch=z9hG4bKkdjuw\r\n'
            'Content-Type: application/unknownformat\r\n'
            'Content-Length: 40\r\n'
            '\r\n'
            '<audio>\r\n'
            ' <pcmu port="443"/>\r\n'
            '</audio>\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 9)
        self.assertTrue(message.header.header_fields[0].is_contact)
        self.assertTrue(message.header.header_fields[1].is_to)
        self.assertTrue(message.header.header_fields[2].is_from)
        self.assertTrue(message.header.header_fields[3].is_max_forwards)
        self.assertTrue(message.header.header_fields[4].is_call_id)
        self.assertTrue(message.header.header_fields[5].is_cseq)
        self.assertTrue(message.header.header_fields[6].is_via)
        self.assertTrue(message.header.header_fields[7].is_content_type)
        self.assertTrue(message.header.header_fields[8].is_content_length)
        # TODO - more.

    def testUnknownAuthorizationScheme(self):
        # https://tools.ietf.org/html/rfc4475#section-3.3.7
        # regaut01
        message_string = (
            'REGISTER sip:example.com SIP/2.0\r\n'
            'To: sip:j.user@example.com\r\n'
            'From: sip:j.user@example.com;tag=87321hj23128\r\n'
            'Max-Forwards: 8\r\n'
            'Call-ID: regaut01.0ha0isndaksdj\r\n'
            'CSeq: 9338 REGISTER\r\n'
            'Via: SIP/2.0/TCP 192.0.2.253;branch=z9hG4bKkdjuw\r\n'
            'Authorization: NoOneKnowsThisScheme opaque-data=here\r\n'
            'Content-Length:0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 8)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_via)
        self.assertTrue(message.header.header_fields[6].is_authorization)
        self.assertTrue(message.header.header_fields[7].is_content_length)
        # TODO - more.

    def testMultipleValuesInSingleValueRequiredFields(self):
        # https://tools.ietf.org/html/rfc4475#section-3.3.8
        # multi01
        message_string = (
            'INVITE sip:user@company.com SIP/2.0\r\n'
            'Contact: <sip:caller@host25.example.net>\r\n'
            'Via: SIP/2.0/UDP 192.0.2.25;branch=z9hG4bKkdjuw\r\n'
            'Max-Forwards: 70\r\n'
            'CSeq: 5 INVITE\r\n'
            'Call-ID: multi01.98asdh@192.0.2.1\r\n'
            'CSeq: 59 INVITE\r\n'
            'Call-ID: multi01.98asdh@192.0.2.2\r\n'
            'From: sip:caller@example.com;tag=3413415\r\n'
            'To: sip:user@example.com\r\n'
            'To: sip:other@example.net\r\n'
            'From: sip:caller@example.net;tag=2923420123\r\n'
            'Content-Type: application/sdp\r\n'
            'l: 154\r\n'
            'Contact: <sip:caller@host36.example.net>\r\n'
            'Max-Forwards: 5\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.25\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.25\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO - is this valid?
        # self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 15)
        self.assertTrue(message.header.header_fields[0].is_contact)
        self.assertTrue(message.header.header_fields[1].is_via)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_cseq)
        self.assertTrue(message.header.header_fields[4].is_call_id)
        self.assertTrue(message.header.header_fields[5].is_cseq)
        self.assertTrue(message.header.header_fields[6].is_call_id)
        self.assertTrue(message.header.header_fields[7].is_from)
        self.assertTrue(message.header.header_fields[8].is_to)
        self.assertTrue(message.header.header_fields[9].is_to)
        self.assertTrue(message.header.header_fields[10].is_from)
        self.assertTrue(message.header.header_fields[11].is_content_type)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[12].is_content_length)
        self.assertTrue(message.header.header_fields[13].is_contact)
        self.assertTrue(message.header.header_fields[14].is_max_forwards)
        # TODO - more.

    def testMultipleContentLengthValues(self):
        # https://tools.ietf.org/html/rfc4475#section-3.3.9
        # mcl01
        message_string = (
            'OPTIONS sip:user@example.com SIP/2.0\r\n'
            'Via: SIP/2.0/UDP host5.example.net;branch=z9hG4bK293423\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:other@example.net;tag=3923942\r\n'
            'Call-ID: mcl01.fhn2323orihawfdoa3o4r52o3irsdf\r\n'
            'CSeq: 15932 OPTIONS\r\n'
            'Content-Length: 13\r\n'
            'Max-Forwards: 60\r\n'
            'Content-Length: 5\r\n'
            'Content-Type: text/plain\r\n'
            '\r\n'
            "There's no way to know how many octets are supposed to be here.\r\n"
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO - is this valid?
        # self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 9)
        self.assertTrue(message.header.header_fields[0].is_via)
        self.assertTrue(message.header.header_fields[1].is_to)
        self.assertTrue(message.header.header_fields[2].is_from)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_content_length)
        self.assertTrue(message.header.header_fields[6].is_max_forwards)
        self.assertTrue(message.header.header_fields[7].is_content_length)
        self.assertTrue(message.header.header_fields[8].is_content_type)
        # TODO - more.

    def test200OKResponseWithBroadcastViaHeaderFieldValue(self):
        # https://tools.ietf.org/html/rfc4475#section-3.3.10
        # bcast
        message_string = (
            'SIP/2.0 200 OK\r\n'
            'Via: SIP/2.0/UDP 192.0.2.198;branch=z9hG4bK1324923\r\n'
            'Via: SIP/2.0/UDP 255.255.255.255;branch=z9hG4bK1saber23\r\n'
            'Call-ID: bcast.0384840201234ksdfak3j2erwedfsASdf\r\n'
            'CSeq: 35 INVITE\r\n'
            'From: sip:user@example.com;tag=11141343\r\n'
            'To: sip:user@example.edu;tag=2229\r\n'
            'Content-Length: 154\r\n'
            'Content-Type: application/sdp\r\n'
            'Contact: <sip:user@host28.example.com>\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.198\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.198\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 9)
        self.assertTrue(message.header.header_fields[0].is_via)
        self.assertTrue(message.header.header_fields[1].is_via)
        self.assertTrue(message.header.header_fields[2].is_call_id)
        self.assertTrue(message.header.header_fields[3].is_cseq)
        self.assertTrue(message.header.header_fields[4].is_from)
        self.assertTrue(message.header.header_fields[5].is_to)
        self.assertTrue(message.header.header_fields[6].is_content_length)
        self.assertTrue(message.header.header_fields[7].is_content_type)
        self.assertTrue(message.header.header_fields[8].is_contact)
        # TODO - more.

    def testMaxForwardsOfZero(self):
        # https://tools.ietf.org/html/rfc4475#section-3.3.11
        # zeromf
        message_string = (
            'OPTIONS sip:user@example.com SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:caller@example.net;tag=3ghsd41\r\n'
            'Call-ID: zeromf.jfasdlfnm2o2l43r5u0asdfas\r\n'
            'CSeq: 39234321 OPTIONS\r\n'
            'Via: SIP/2.0/UDP host1.example.com;branch=z9hG4bKkdjuw2349i\r\n'
            'Max-Forwards: 0\r\n'
            'Content-Length: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 7)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_call_id)
        self.assertTrue(message.header.header_fields[3].is_cseq)
        self.assertTrue(message.header.header_fields[4].is_via)
        self.assertTrue(message.header.header_fields[5].is_max_forwards)
        self.assertTrue(message.header.header_fields[6].is_content_length)
        # TODO - more.

    def testREGISTERwithAContactHeaderParameter(self):
        # https://tools.ietf.org/html/rfc4475#section-3.3.12
        # cparam01
        message_string = (
            'REGISTER sip:example.com SIP/2.0\r\n'
            'Via: SIP/2.0/UDP saturn.example.com:5060;branch=z9hG4bKkdjuw\r\n'
            'Max-Forwards: 70\r\n'
            'From: sip:watson@example.com;tag=DkfVgjkrtMwaerKKpe\r\n'
            'To: sip:watson@example.com\r\n'
            'Call-ID: cparam01.70710@saturn.example.com\r\n'
            'CSeq: 2 REGISTER\r\n'
            'Contact: sip:+19725552222@gw1.example.net;unknownparam\r\n'
            'l: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 8)
        self.assertTrue(message.header.header_fields[0].is_via)
        self.assertTrue(message.header.header_fields[1].is_max_forwards)
        self.assertTrue(message.header.header_fields[2].is_from)
        self.assertTrue(message.header.header_fields[3].is_to)
        self.assertTrue(message.header.header_fields[4].is_call_id)
        self.assertTrue(message.header.header_fields[5].is_cseq)
        self.assertTrue(message.header.header_fields[6].is_contact)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[7].is_content_length)
        # TODO - more.

    def testREGISTERWithAURLParameter(self):
        # https://tools.ietf.org/html/rfc4475#section-3.3.13
        # cparam02
        message_string = (
            'REGISTER sip:example.com SIP/2.0\r\n'
            'Via: SIP/2.0/UDP saturn.example.com:5060;branch=z9hG4bKkdjuw\r\n'
            'Max-Forwards: 70\r\n'
            'From: sip:watson@example.com;tag=838293\r\n'
            'To: sip:watson@example.com\r\n'
            'Call-ID: cparam02.70710@saturn.example.com\r\n'
            'CSeq: 3 REGISTER\r\n'
            'Contact: <sip:+19725552222@gw1.example.net;unknownparam>\r\n'
            'l: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 8)
        self.assertTrue(message.header.header_fields[0].is_via)
        self.assertTrue(message.header.header_fields[1].is_max_forwards)
        self.assertTrue(message.header.header_fields[2].is_from)
        self.assertTrue(message.header.header_fields[3].is_to)
        self.assertTrue(message.header.header_fields[4].is_call_id)
        self.assertTrue(message.header.header_fields[5].is_cseq)
        self.assertTrue(message.header.header_fields[6].is_contact)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[7].is_content_length)
        # TODO - more.

    def testREGISTERWithAURLEscapedHeader(self):
        # https://tools.ietf.org/html/rfc4475#section-3.3.14
        # regescrt
        message_string = (
            'REGISTER sip:example.com SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:user@example.com;tag=8\r\n'
            'Max-Forwards: 70\r\n'
            'Call-ID: regescrt.k345asrl3fdbv@192.0.2.1\r\n'
            'CSeq: 14398234 REGISTER\r\n'
            'Via: SIP/2.0/UDP host5.example.com;branch=z9hG4bKkdjuw\r\n'
            'M: <sip:user@example.com?Route=%3Csip:sip.example.com%3E>\r\n'
            'L:0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # is this valid?  It was considered valid before we implemented compact headers.
        # TODO: Looks like we need to handle % escaped strings in SIP URIs.
        # self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 8)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_max_forwards)
        self.assertTrue(message.header.header_fields[3].is_call_id)
        self.assertTrue(message.header.header_fields[4].is_cseq)
        self.assertTrue(message.header.header_fields[5].is_via)
        if self.weHaveImplementedCompactHeaders:
            self.assertTrue(message.header.header_fields[6].is_contact)
            self.assertTrue(message.header.header_fields[7].is_content_length)
        # TODO - more.

    def testUnacceptableAcceptOffering(self):
        # https://tools.ietf.org/html/rfc4475#section-3.3.15
        # sdp01
        message_string = (
            'INVITE sip:user@example.com SIP/2.0\r\n'
            'To: sip:j_user@example.com\r\n'
            'Contact: <sip:caller@host15.example.net>\r\n'
            'From: sip:caller@example.net;tag=234\r\n'
            'Max-Forwards: 5\r\n'
            'Call-ID: sdp01.ndaksdj9342dasdd\r\n'
            'Accept: text/nobodyKnowsThis\r\n'
            'CSeq: 8 INVITE\r\n'
            'Via: SIP/2.0/UDP 192.0.2.15;branch=z9hG4bKkdjuw\r\n'
            'Content-Length: 150\r\n'
            'Content-Type: application/sdp\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.5\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.5\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 10)
        self.assertTrue(message.header.header_fields[0].is_to)
        self.assertTrue(message.header.header_fields[1].is_contact)
        self.assertTrue(message.header.header_fields[2].is_from)
        self.assertTrue(message.header.header_fields[3].is_max_forwards)
        self.assertTrue(message.header.header_fields[4].is_call_id)
        self.assertTrue(message.header.header_fields[5].is_accept)
        self.assertTrue(message.header.header_fields[6].is_cseq)
        self.assertTrue(message.header.header_fields[7].is_via)
        self.assertTrue(message.header.header_fields[8].is_content_length)
        self.assertTrue(message.header.header_fields[9].is_content_type)
        # TODO - more.

    def testINVITEWithRFC2543Syntax(self):
        # https://tools.ietf.org/html/rfc4475#section-3.4.1
        # inv2543
        message_string = (
            'INVITE sip:UserB@example.com SIP/2.0\r\n'
            'Via: SIP/2.0/UDP iftgw.example.com\r\n'
            'From: <sip:+13035551111@ift.client.example.net;user=phone>\r\n'
            'Record-Route: <sip:UserB@example.com;maddr=ss1.example.com>\r\n'
            'To: sip:+16505552222@ss1.example.net;user=phone\r\n'
            'Call-ID: inv2543.1717@ift.client.example.com\r\n'
            'CSeq: 56 INVITE\r\n'
            'Content-Type: application/sdp\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.5\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.5\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO - is this valid?
        # self.assertTrue(message.is_valid)
        self.assertEqual(len(message.header.header_fields), 7)
        self.assertTrue(message.header.header_fields[0].is_via)
        self.assertTrue(message.header.header_fields[1].is_from)
        self.assertTrue(message.header.header_fields[2].is_record_route)
        self.assertTrue(message.header.header_fields[3].is_to)
        self.assertTrue(message.header.header_fields[4].is_call_id)
        self.assertTrue(message.header.header_fields[5].is_cseq)
        self.assertTrue(message.header.header_fields[6].is_content_type)
        # TODO - more.
