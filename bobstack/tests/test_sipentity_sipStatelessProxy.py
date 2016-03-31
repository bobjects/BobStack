from unittest import TestCase
import unittest
import sys
sys.path.append("..")
sys.path.append("../..")
from bobstack.sipmessaging import SIPMessageFactory
from bobstack.siptransport import SimulatedSIPTransport
from bobstack.sipentity import SIPStatelessProxy
from bobstack.siptransport import SimulatedNetwork


class TestStatelessProxy(TestCase):
    def setUp(self):
        SimulatedNetwork.clear()
        self.atlanta = SIPStatelessProxy()
        self.atlanta.transports = [SimulatedSIPTransport(self.atlantaBindAddress, self.atlantaBindPort)]
        self.biloxi = SIPStatelessProxy()
        self.biloxi.transports = [SimulatedSIPTransport(self.biloxiBindAddress, self.biloxiBindPort)]
        self.aliceTransport = SimulatedSIPTransport(self.aliceBindAddress, self.aliceBindPort)
        self.bobTransport = SimulatedSIPTransport(self.bobBindAddress, self.bobBindPort)
        self.aliceTransport.connectToAddressAndPort(self.atlantaBindAddress, self.atlantaBindPort)
        # Let Biloxi connect to Bob.  Don't pre-connect Bob to Biloxi.
        # self.bobTransport.connectToAddressAndPort(self.biloxiBindAddress, self.biloxiBindPort)

    def test(self):
        self.run_01_atlantaToBiloxi()
        self.run_02_biloxiToAtlanta()

    def run_01_atlantaToBiloxi(self):
        pass

    def run_02_biloxiToAtlanta(self):
        pass

    @property
    def atlantaBindAddress(self):
        return '192.168.4.2'

    @property
    def atlantaBindPort(self):
        return 5060

    @property
    def biloxiBindAddress(self):
        return '192.168.4.3'

    @property
    def biloxiBindPort(self):
        return 5060

    @property
    def aliceBindAddress(self):
        return '192.168.4.4'

    @property
    def aliceBindPort(self):
        return 5060

    @property
    def bobBindAddress(self):
        return '192.168.4.5'

    @property
    def bobBindPort(self):
        return 5060

    @property
    def aliceRequestString(self):
        # TODO: need to fix up the addresses and transport type and stuff.
        messageString = ('INVITE sip:1002@192.168.0.97 SIP/2.0\r\n'
                         'Via: SIP/2.0/UDP 192.168.0.188:63354;branch=z9hG4bK-524287-1---7a462a5d1b6fe13b;rport\r\n'
                         'Max-Forwards: 70\r\n'
                         'Contact: <sip:alice@192.168.0.188:63354;rinstance=d875ce4fd8f72441>\r\n'
                         'To: <sip:1002@192.168.0.97>\r\n'
                         'From: "Alice"<sip:alice@192.168.0.97>;tag=9980376d\r\n'
                         'Call-ID: YjBhMDliMWMxNzQ4ZTc5Nzg1ZTcyYTExMWMzZDlhNmQ\r\n'
                         'CSeq: 1 INVITE\r\n'
                         'Allow: INVITE, ACK, CANCEL, BYE, REFER, INFO, NOTIFY, UPDATE, PRACK, MESSAGE, OPTIONS, SUBSCRIBE, OPTIONS\r\n'
                         'Content-Type: application/sdp\r\n'
                         'Supported: replaces, 100rel\r\n'
                         'User-Agent: Bria iOS release 3.6.2 stamp 33024\r\n'
                         'Content-Length: 189\r\n'
                         '\r\n'
                         'v=0\r\n'
                         'o=- 1457365987528724 1 IN IP4 192.168.0.188\r\n'
                         's=Cpc session\r\n'
                         'c=IN IP4 192.168.0.188\r\n'
                         't=0 0\r\n'
                         'm=audio 60668 RTP/AVP 0 101\r\n'
                         'a=rtpmap:101 telephone-event/8000\r\n'
                         'a=fmtp:101 0-15\r\n'
                         'a=sendrecv\r\n')
        return messageString

    @property
    def aliceResponseString(self):
        # TODO: need to fix up the addresses and transport type and stuff.
        messageString = ('SIP/2.0 180 Ringing\r\n'
                         'Via: SIP/2.0/UDP 192.168.0.97;branch=z9hG4bKeb83.c2fe646b6c2d21c6f9f113d37c474768.0\r\n'
                         'Via: SIP/2.0/UDP 192.168.0.188:56731;received=192.168.0.188;branch=z9hG4bK-524287-1---e500d061e354193a;rport=56731\r\n'
                         'Record-Route: <sip:192.168.0.96;lr>\r\n'
                         'Record-Route: <sip:192.168.0.97;lr>\r\n'
                         'Require: 100rel\r\n'
                         'Contact: <sip:1002@192.168.0.204:52909;rinstance=7caea32dab180286>\r\n'
                         'To: "Bob"<sip:1002@192.168.0.96>;tag=52e9ef73\r\n'
                         'From: "Alice"<sip:1001@192.168.0.96>;tag=2210ba44\r\n'
                         'Call-ID: NTM5YzAxN2YwZGRhYTg2YjBkNDgyNWQyNTI3ZGNmNTE\r\n'
                         'CSeq: 1 INVITE\r\n'
                         'Allow: INVITE, ACK, CANCEL, BYE, REFER, INFO, NOTIFY, UPDATE, PRACK, MESSAGE, OPTIONS, SUBSCRIBE, OPTIONS\r\n'
                         'Supported: replaces\r\n'
                         'User-Agent: Bria iOS release 3.6.2 stamp 33024\r\n'
                         'Allow-Events: talk, hold\r\n'
                         'RSeq: 1\r\n'
                         'Content-Length: 0\r\n'
                         '\r\n')
        return messageString

    @property
    def bobRequestString(self):
        # TODO: need to fix up the addresses and transport type and stuff.
        messageString = ('INVITE sip:1002@192.168.0.97 SIP/2.0\r\n'
                         'Via: SIP/2.0/UDP 192.168.0.188:63354;branch=z9hG4bK-524287-1---7a462a5d1b6fe13b;rport\r\n'
                         'Max-Forwards: 70\r\n'
                         'Contact: <sip:alice@192.168.0.188:63354;rinstance=d875ce4fd8f72441>\r\n'
                         'To: <sip:1002@192.168.0.97>\r\n'
                         'From: "Alice"<sip:alice@192.168.0.97>;tag=9980376d\r\n'
                         'Call-ID: YjBhMDliMWMxNzQ4ZTc5Nzg1ZTcyYTExMWMzZDlhNmQ\r\n'
                         'CSeq: 1 INVITE\r\n'
                         'Allow: INVITE, ACK, CANCEL, BYE, REFER, INFO, NOTIFY, UPDATE, PRACK, MESSAGE, OPTIONS, SUBSCRIBE, OPTIONS\r\n'
                         'Content-Type: application/sdp\r\n'
                         'Supported: replaces, 100rel\r\n'
                         'User-Agent: Bria iOS release 3.6.2 stamp 33024\r\n'
                         'Content-Length: 189\r\n'
                         '\r\n'
                         'v=0\r\n'
                         'o=- 1457365987528724 1 IN IP4 192.168.0.188\r\n'
                         's=Cpc session\r\n'
                         'c=IN IP4 192.168.0.188\r\n'
                         't=0 0\r\n'
                         'm=audio 60668 RTP/AVP 0 101\r\n'
                         'a=rtpmap:101 telephone-event/8000\r\n'
                         'a=fmtp:101 0-15\r\n'
                         'a=sendrecv\r\n')
        return messageString

    @property
    def bobResponseString(self):
        # TODO: need to fix up the addresses and transport type and stuff.
        messageString = ('SIP/2.0 180 Ringing\r\n'
                         'Via: SIP/2.0/UDP 192.168.0.97;branch=z9hG4bKeb83.c2fe646b6c2d21c6f9f113d37c474768.0\r\n'
                         'Via: SIP/2.0/UDP 192.168.0.188:56731;received=192.168.0.188;branch=z9hG4bK-524287-1---e500d061e354193a;rport=56731\r\n'
                         'Record-Route: <sip:192.168.0.96;lr>\r\n'
                         'Record-Route: <sip:192.168.0.97;lr>\r\n'
                         'Require: 100rel\r\n'
                         'Contact: <sip:1002@192.168.0.204:52909;rinstance=7caea32dab180286>\r\n'
                         'To: "Bob"<sip:1002@192.168.0.96>;tag=52e9ef73\r\n'
                         'From: "Alice"<sip:1001@192.168.0.96>;tag=2210ba44\r\n'
                         'Call-ID: NTM5YzAxN2YwZGRhYTg2YjBkNDgyNWQyNTI3ZGNmNTE\r\n'
                         'CSeq: 1 INVITE\r\n'
                         'Allow: INVITE, ACK, CANCEL, BYE, REFER, INFO, NOTIFY, UPDATE, PRACK, MESSAGE, OPTIONS, SUBSCRIBE, OPTIONS\r\n'
                         'Supported: replaces\r\n'
                         'User-Agent: Bria iOS release 3.6.2 stamp 33024\r\n'
                         'Allow-Events: talk, hold\r\n'
                         'RSeq: 1\r\n'
                         'Content-Length: 0\r\n'
                         '\r\n')
        return messageString

