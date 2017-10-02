from unittest import TestCase
import sys
sys.path.append("..")
sys.path.append("../..")
from bobstack.sipmessaging import SIPMessageFactory
from bobstack.siptransport import SimulatedSIPTransport
from bobstack.sipentity import SIPStatelessProxy
from bobstack.siptransport import SimulatedNetwork


class TestRFC5118SIPTortureTest(TestCase):
    def testValidSIPMessageWithAnIPv6Reference(self):
        # https://tools.ietf.org/html/rfc5118#section-4.1
        # ipv6-good.dat
        message_string = (
            'REGISTER sip:[2001:db8::10] SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:user@example.com;tag=81x2\r\n'
            'Via: SIP/2.0/UDP [2001:db8::9:1];branch=z9hG4bKas3-111\r\n'
            'Call-ID: SSG9559905523997077@hlau_4100\r\n'
            'Max-Forwards: 70\r\n'
            'Contact: "Caller" <sip:caller@[2001:db8::1]>\r\n'
            'CSeq: 98176 REGISTER\r\n'
            'Content-Length: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO

    def testInvalidSIPMessageWithAnIPv6Reference(self):
        # https://tools.ietf.org/html/rfc5118#section-4.2
        # ipv6-bad.dat
        message_string = (
            'REGISTER sip:2001:db8::10 SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:user@example.com;tag=81x2\r\n'
            'Via: SIP/2.0/UDP [2001:db8::9:1];branch=z9hG4bKas3-111\r\n'
            'Call-ID: SSG9559905523997077@hlau_4100\r\n'
            'Max-Forwards: 70\r\n'
            'Contact: "Caller" <sip:caller@[2001:db8::1]>\r\n'
            'CSeq: 98176 REGISTER\r\n'
            'Content-Length: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO

    def testPortAmbiguousInASIPURI(self):
        # https://tools.ietf.org/html/rfc5118#section-4.3
        # port-ambiguous.dat
        message_string = (
            'REGISTER sip:[2001:db8::10:5070] SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:user@example.com;tag=81x2\r\n'
            'Via: SIP/2.0/UDP [2001:db8::9:1];branch=z9hG4bKas3-111\r\n'
            'Call-ID: SSG9559905523997077@hlau_4100\r\n'
            'Contact: "Caller" <sip:caller@[2001:db8::1]>\r\n'
            'Max-Forwards: 70\r\n'
            'CSeq: 98176 REGISTER\r\n'
            'Content-Length: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO

    def testPortUnambiguousInASIPURI(self):
        # https://tools.ietf.org/html/rfc5118#section-4.4
        # port-unambiguous.dat
        message_string = (
            'REGISTER sip:[2001:db8::10]:5070 SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:user@example.com;tag=81x2\r\n'
            'Via: SIP/2.0/UDP [2001:db8::9:1];branch=z9hG4bKas3-111\r\n'
            'Call-ID: SSG9559905523997077@hlau_4100\r\n'
            'Contact: "Caller" <sip:caller@[2001:db8::1]>\r\n'
            'Max-Forwards: 70\r\n'
            'CSeq: 98176 REGISTER\r\n'
            'Content-Length: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO

    def testIPv6ReferenceDelimitersInViaHeader(self):
        # https://tools.ietf.org/html/rfc5118#section-4.5
        # via-received-param-with-delim.dat
        message_string = (
            'BYE sip:[2001:db8::10] SIP/2.0\r\n'
            'To: sip:user@example.com;tag=bd76ya\r\n'
            'From: sip:user@example.com;tag=81x2\r\n'
            'Via: SIP/2.0/UDP [2001:db8::9:1];received=[2001:db8::9:255];branch=z9hG4bKas3-111\r\n'
            'Call-ID: SSG9559905523997077@hlau_4100\r\n'
            'Max-Forwards: 70\r\n'
            'CSeq: 321 BYE\r\n'
            'Content-Length: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO

    def testIPv6ReferenceDelimitersInViaHeader2(self):
        # https://tools.ietf.org/html/rfc5118#section-4.5
        # via-received-param-no-delim.dat
        message_string = (
            'OPTIONS sip:[2001:db8::10] SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:user@example.com;tag=81x2\r\n'
            'Via: SIP/2.0/UDP [2001:db8::9:1];received=2001:db8::9:255;branch=z9hG4bKas3\r\n'
            'Call-ID: SSG95523997077@hlau_4100\r\n'
            'Max-Forwards: 70\r\n'
            'Contact: "Caller" <sip:caller@[2001:db8::9:1]>\r\n'
            'CSeq: 921 OPTIONS\r\n'
            'Content-Length: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO

    def testSIPRequestWithIPv6AddressesInSDPBody(self):
        # https://tools.ietf.org/html/rfc5118#section-4.6
        # ipv6-in-sdp.dat
        message_string = (
            'INVITE sip:user@[2001:db8::10] SIP/2.0\r\n'
            'To: sip:user@[2001:db8::10]\r\n'
            'From: sip:user@example.com;tag=81x2\r\n'
            'Via: SIP/2.0/UDP [2001:db8::20];branch=z9hG4bKas3-111\r\n'
            'Call-ID: SSG9559905523997077@hlau_4100\r\n'
            'Contact: "Caller" <sip:caller@[2001:db8::20]>\r\n'
            'CSeq: 8612 INVITE\r\n'
            'Max-Forwards: 70\r\n'
            'Content-Type: application/sdp\r\n'
            'Content-Length: 268\r\n'
            '\r\n'
            'v=0\r\n'
            'o=assistant 971731711378798081 0 IN IP6 2001:db8::20\r\n'
            "s=Live video feed for today's meeting\r\n"
            'c=IN IP6 2001:db8::20\r\n'
            't=3338481189 3370017201\r\n'
            'm=audio 6000 RTP/AVP 2\r\n'
            'a=rtpmap:2 G726-32/8000\r\n'
            'm=video 6024 RTP/AVP 107\r\n'
            'a=rtpmap:107 H263-1998/90000\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO

    def testMultipleIPAddressesInSIPHeaders(self):
        # https://tools.ietf.org/html/rfc5118#section-4.7
        # mult-ip-in-header.dat
        message_string = (
            'BYE sip:user@host.example.net SIP/2.0\r\n'
            'Via: SIP/2.0/UDP [2001:db8::9:1]:6050;branch=z9hG4bKas3-111\r\n'
            'Via: SIP/2.0/UDP 192.0.2.1;branch=z9hG4bKjhja8781hjuaij65144\r\n'
            'Via: SIP/2.0/TCP [2001:db8::9:255];branch=z9hG4bK451jj;received=192.0.2.200\r\n'
            'Call-ID: 997077@lau_4100\r\n'
            'Max-Forwards: 70\r\n'
            'CSeq: 89187 BYE\r\n'
            'To: sip:user@example.net;tag=9817--94\r\n'
            'From: sip:user@example.com;tag=81x2\r\n'
            'Content-Length: 0\r\n'
            '\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO

    def testMultipleIPAddressesInSDP(self):
        # https://tools.ietf.org/html/rfc5118#section-4.8
        # mult-ip-in-sdp.dat
        message_string = (
            'INVITE sip:user@[2001:db8::10] SIP/2.0\r\n'
            'To: sip:user@[2001:db8::10]\r\n'
            'From: sip:user@example.com;tag=81x2\r\n'
            'Via: SIP/2.0/UDP [2001:db8::9:1];branch=z9hG4bKas3-111\r\n'
            'Call-ID: SSG9559905523997077@hlau_4100\r\n'
            'Contact: "Caller" <sip:caller@[2001:db8::9:1]>\r\n'
            'Max-Forwards: 70\r\n'
            'CSeq: 8912 INVITE\r\n'
            'Content-Type: application/sdp\r\n'
            'Content-Length: 181\r\n'
            '\r\n'
            'v=0\r\n'
            'o=bob 280744730 28977631 IN IP4 host.example.com\r\n'
            's=\r\n'
            't=0 0\r\n'
            'm=audio 22334 RTP/AVP 0\r\n'
            'c=IN IP4 192.0.2.1\r\n'
            'm=video 6024 RTP/AVP 107\r\n'
            'c=IN IP6 2001:db8::1\r\n'
            'a=rtpmap:107 H263-1998/90000\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO

    def testIPv4MappedIPv6Addresses(self):
        # https://tools.ietf.org/html/rfc5118#section-4.9
        # ipv4-mapped-ipv6.dat
        message_string = (
            'INVITE sip:user@example.com SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:user@east.example.com;tag=81x2\r\n'
            'Via: SIP/2.0/UDP [::ffff:192.0.2.10]:19823;branch=z9hG4bKbh19\r\n'
            'Via: SIP/2.0/UDP [::ffff:192.0.2.2];branch=z9hG4bKas3-111\r\n'
            'Call-ID: SSG9559905523997077@hlau_4100\r\n'
            'Contact: "T. desk phone" <sip:ted@[::ffff:192.0.2.2]>\r\n'
            'CSeq: 612 INVITE\r\n'
            'Max-Forwards: 70\r\n'
            'Content-Type: application/sdp\r\n'
            'Content-Length: 236\r\n'
            '\r\n'
            'v=0\r\n'
            'o=assistant 971731711378798081 0 IN IP6 ::ffff:192.0.2.2\r\n'
            's=Call me soon, please!\r\n'
            'c=IN IP6 ::ffff:192.0.2.2\r\n'
            't=3338481189 3370017201\r\n'
            'm=audio 6000 RTP/AVP 2\r\n'
            'a=rtpmap:2 G726-32/8000\r\n'
            'm=video 6024 RTP/AVP 107\r\n'
            'a=rtpmap:107 H263-1998/90000\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO

    def testIPv6ReferenceBugInRFC3261ABNF(self):
        # https://tools.ietf.org/html/rfc5118#section-4.10
        # ipv6-bug-abnf-3-colons
        message_string = (
            'OPTIONS sip:user@[2001:db8:::192.0.2.1] SIP/2.0\r\n'
            'To: sip:user@[2001:db8:::192.0.2.1]\r\n'
            'From: sip:user@example.com;tag=810x2\r\n'
            'Via: SIP/2.0/UDP lab1.east.example.com;branch=z9hG4bKas3-111\r\n'
            'Call-ID: G9559905523997077@hlau_4100\r\n'
            'CSeq: 689 OPTIONS\r\n'
            'Max-Forwards: 70\r\n'
            'Content-Length: 0\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO

    def testIPv6ReferenceBugInRFC3261ABNF2(self):
        # https://tools.ietf.org/html/rfc5118#section-4.10
        # ipv6-correct-abnf-2-colons
        message_string = (
            'OPTIONS sip:user@[2001:db8::192.0.2.1] SIP/2.0\r\n'
            'To: sip:user@[2001:db8::192.0.2.1]\r\n'
            'From: sip:user@example.com;tag=810x2\r\n'
            'Via: SIP/2.0/UDP lab1.east.example.com;branch=z9hG4bKas3-111\r\n'
            'Call-ID: G9559905523997077@hlau_4100\r\n'
            'CSeq: 689 OPTIONS\r\n'
            'Max-Forwards: 70\r\n'
            'Content-Length: 0\r\n'
        )
        message = SIPMessageFactory().next_for_string(message_string)
        self.assertIsNotNone(message)
        self.assertIsInstance(message.is_valid, bool)
        # TODO

