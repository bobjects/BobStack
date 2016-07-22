from unittest import TestCase
import sys
sys.path.append("..")
sys.path.append("../..")
from bobstack.sipmessaging import SIPURI
from bobstack.siptransport import SimulatedSIPTransport
from bobstack.sipentity import SIPStatelessProxy
from bobstack.siptransport import SimulatedNetwork


class TestStatelessProxy(TestCase):
    def setUp(self):
        SimulatedNetwork.clear()
        self.aliceReceivedRequests = []
        self.aliceReceivedResponses = []
        self.atlantaReceivedRequests = []
        self.atlantaReceivedResponses = []
        self.biloxiReceivedRequests = []
        self.biloxiReceivedResponses = []
        self.bobReceivedRequests = []
        self.bobReceivedResponses = []
        self.atlanta = SIPStatelessProxy()
        self.atlanta.transports = [SimulatedSIPTransport(self.atlantaBindAddress, self.atlantaBindPort)]
        self.biloxi = SIPStatelessProxy()
        self.biloxi.transports = [SimulatedSIPTransport(self.biloxiBindAddress, self.biloxiBindPort)]
        self.aliceTransport = SimulatedSIPTransport(self.aliceBindAddress, self.aliceBindPort)
        self.bobTransport = SimulatedSIPTransport(self.bobBindAddress, self.bobBindPort)
        self.aliceTransport.whenEventDo("receivedValidConnectedRequest", self.aliceRequestEventHandler)
        self.aliceTransport.whenEventDo("receivedValidConnectedResponse", self.aliceResponseEventHandler)
        self.atlanta.transports[0].whenEventDo("receivedValidConnectedRequest", self.atlantaRequestEventHandler)
        self.atlanta.transports[0].whenEventDo("receivedValidConnectedResponse", self.atlantaResponseEventHandler)
        self.biloxi.transports[0].whenEventDo("receivedValidConnectedRequest", self.biloxiRequestEventHandler)
        self.biloxi.transports[0].whenEventDo("receivedValidConnectedResponse", self.biloxiResponseEventHandler)
        self.bobTransport.whenEventDo("receivedValidConnectedRequest", self.bobRequestEventHandler)
        self.bobTransport.whenEventDo("receivedValidConnectedResponse", self.bobResponseEventHandler)
        self.aliceTransport.bind()
        self.bobTransport.bind()
        self.aliceTransport.connectToAddressAndPort(self.atlantaBindAddress, self.atlantaBindPort)
        # Let Biloxi connect to Bob.  Don't pre-connect Bob to Biloxi.
        # self.bobTransport.connectToAddressAndPort(self.biloxiBindAddress, self.biloxiBindPort)
        # TODO:  need to bind?

    def test(self):
        self.run_00_initialSanityCheck()
        self.run_01_atlantaToBiloxi()
        self.run_02_biloxiToAtlanta()

    def run_00_initialSanityCheck(self):
        self.assertEqual(1, len(self.atlanta.transports))
        self.assertEqual(1, len(self.biloxi.transports))
        self.assertEqual(1, len(self.atlanta.transports[0].connections))
        self.assertEqual(0, len(self.biloxi.transports[0].connections))
        self.assertEqual(self.atlantaBindAddress, self.atlanta.transports[0].bindAddress)
        self.assertEqual(self.atlantaBindPort, self.atlanta.transports[0].bindPort)
        self.assertEqual(self.atlantaBindAddress, self.atlanta.transports[0].connections[0].bindAddress)
        self.assertEqual(self.atlantaBindPort, self.atlanta.transports[0].connections[0].bindPort)
        self.assertEqual(self.atlantaBindAddress, self.aliceTransport.connections[0].remoteAddress)
        self.assertEqual(self.atlantaBindPort, self.aliceTransport.connections[0].remotePort)
        self.assertEqual(self.aliceBindAddress, self.atlanta.transports[0].connections[0].remoteAddress)
        self.assertEqual(self.aliceBindPort, self.atlanta.transports[0].connections[0].remotePort)
        self.assertEqual(self.biloxiBindAddress, self.biloxi.transports[0].bindAddress)
        self.assertEqual(self.biloxiBindPort, self.biloxi.transports[0].bindPort)
        self.assertEqual(0, len(self.aliceReceivedRequests))
        self.assertEqual(0, len(self.aliceReceivedResponses))
        self.assertEqual(0, len(self.atlantaReceivedRequests))
        self.assertEqual(0, len(self.atlantaReceivedResponses))
        self.assertEqual(0, len(self.biloxiReceivedRequests))
        self.assertEqual(0, len(self.biloxiReceivedResponses))
        self.assertEqual(0, len(self.bobReceivedRequests))
        self.assertEqual(0, len(self.bobReceivedResponses))

    def run_01_atlantaToBiloxi(self):
        self.aliceTransport.connections[0].sendString(self.aliceRequestString)
        self.assertEqual(0, len(self.aliceReceivedRequests))
        # TODO: Once we implement reply processing, this next line will be 1.
        self.assertEqual(0, len(self.aliceReceivedResponses))
        self.assertEqual(1, len(self.atlantaReceivedRequests))
        self.assertEqual(1, len(self.atlantaReceivedResponses))
        self.assertEqual(1, len(self.biloxiReceivedRequests))
        self.assertEqual(0, len(self.biloxiReceivedResponses))
        self.assertEqual(0, len(self.bobReceivedRequests))
        self.assertEqual(0, len(self.bobReceivedResponses))
        self.assertEqual(self.aliceBindAddress, self.atlantaReceivedRequests[0].connection.remoteAddress)
        self.assertEqual(self.aliceBindPort, self.atlantaReceivedRequests[0].connection.remotePort)
        self.assertEqual(self.atlantaBindAddress, self.atlantaReceivedRequests[0].connection.bindAddress)
        self.assertEqual(self.atlantaBindPort, self.atlantaReceivedRequests[0].connection.bindPort)
        atlantaReceivedRequest = self.atlantaReceivedRequests[0].sipMessage
        rURI = SIPURI.newParsedFrom(atlantaReceivedRequest.startLine.requestURI)
        self.assertEqual(self.aliceRequestString, atlantaReceivedRequest.rawString)
        self.assertEqual('INVITE', atlantaReceivedRequest.startLine.sipMethod)
        self.assertEqual(self.biloxiBindAddress, rURI.host)
        self.assertEqual(1, len(atlantaReceivedRequest.vias))
        self.assertEqual(self.aliceBindAddress, atlantaReceivedRequest.viaHeaderFields[0].host)
        # TODO: This 404 nonsense is temporary.  Alice sends to a biloxi domain via atlanta, atlanta forwards her request to biloxi,
        # Biloxi sees that it is responsible for the request, and for right now, just answers 404.
        self.assertEqual(404, self.atlantaReceivedResponses[0].sipMessage.startLine.statusCode)

        # TODO:  Once we implement reply processing, alice will get 404.
        # self.assertEqual(404, self.aliceReceivedResponses[0].sipMessage.startLine.statusCode)

        # TODO:  Moar!!!

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
        # Bob's extension is 1002
        # atlanta == .2 / .97
        # biloxi == .3 / .96
        # alice == .4 / .188
        # bob == .5 / .204
        messageString = ('INVITE sip:1002@192.168.4.3 SIP/2.0\r\n'
                         'Via: SIP/2.0/UDP 192.168.4.4:63354;branch=z9hG4bK-524287-1---7a462a5d1b6fe13b;rport\r\n'
                         'Max-Forwards: 70\r\n'
                         'Contact: <sip:alice@192.168.4.4:63354;rinstance=d875ce4fd8f72441>\r\n'
                         'To: <sip:1002@192.168.4.3>\r\n'
                         'From: "Alice"<sip:alice@192.168.4.2>;tag=9980376d\r\n'
                         'Call-ID: YjBhMDliMWMxNzQ4ZTc5Nzg1ZTcyYTExMWMzZDlhNmQ\r\n'
                         'CSeq: 1 INVITE\r\n'
                         'Allow: INVITE, ACK, CANCEL, BYE, REFER, INFO, NOTIFY, UPDATE, PRACK, MESSAGE, OPTIONS, SUBSCRIBE, OPTIONS\r\n'
                         'Content-Type: application/sdp\r\n'
                         'Supported: replaces, 100rel\r\n'
                         'User-Agent: Bria iOS release 3.6.2 stamp 33024\r\n'
                         'Content-Length: 185\r\n'
                         '\r\n'
                         'v=0\r\n'
                         'o=- 1457365987528724 1 IN IP4 192.168.4.4\r\n'
                         's=Cpc session\r\n'
                         'c=IN IP4 192.168.4.4\r\n'
                         't=0 0\r\n'
                         'm=audio 60668 RTP/AVP 0 101\r\n'
                         'a=rtpmap:101 telephone-event/8000\r\n'
                         'a=fmtp:101 0-15\r\n'
                         'a=sendrecv\r\n')
        return messageString

    @property
    def aliceResponseString(self):
        # TODO: need to fix up the addresses and transport type and stuff.
        # atlanta == .2 / .97
        # biloxi == .3 / .96
        # alice == .4 / .188
        # bob == .5 / .204
        messageString = ('SIP/2.0 180 Ringing\r\n'
                         'Via: SIP/2.0/UDP 192.168.4.2;branch=z9hG4bKeb83.c2fe646b6c2d21c6f9f113d37c474768.0\r\n'
                         'Via: SIP/2.0/UDP 192.168.4.3:56731;received=192.168.4.4;branch=z9hG4bK-524287-1---e500d061e354193a;rport=56731\r\n'
                         'Via: SIP/2.0/UDP 192.168.4.5;branch=z9hG4bKeb83.c2fe646b6c2d21c6f9f113d37c474768.0\r\n'
                         'Record-Route: <sip:192.168.4.2;lr>\r\n'
                         'Record-Route: <sip:192.168.4.3;lr>\r\n'
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
        # Alice's extension is 1001
        # atlanta == .2
        # biloxi == .3
        # alice == .4
        # bob == .5
        messageString = ('INVITE sip:1001@192.168.4.2 SIP/2.0\r\n'
                         'Via: SIP/2.0/UDP 192.168.4.5:63354;branch=z9hG4bK-524287-1---7a462a5d1b6fe13b;rport\r\n'
                         'Max-Forwards: 70\r\n'
                         'Contact: <sip:bob@192.168.4.3:63354;rinstance=d875ce4fd8f72441>\r\n'
                         'To: <sip:1001@192.168.4.2>\r\n'
                         'From: "Alice"<sip:alice@192.168.4.2>;tag=9980376d\r\n'
                         'Call-ID: YjBhMDliMWMxNzQ4ZTc5Nzg1ZTcyYTExMWMzZDlhNmQ\r\n'
                         'CSeq: 1 INVITE\r\n'
                         'Allow: INVITE, ACK, CANCEL, BYE, REFER, INFO, NOTIFY, UPDATE, PRACK, MESSAGE, OPTIONS, SUBSCRIBE, OPTIONS\r\n'
                         'Content-Type: application/sdp\r\n'
                         'Supported: replaces, 100rel\r\n'
                         'User-Agent: Bria iOS release 3.6.2 stamp 33024\r\n'
                         'Content-Length: 185\r\n'
                         '\r\n'
                         'v=0\r\n'
                         'o=- 1457365987528724 1 IN IP4 192.168.4.5\r\n'
                         's=Cpc session\r\n'
                         'c=IN IP4 192.168.4.5\r\n'
                         't=0 0\r\n'
                         'm=audio 60668 RTP/AVP 0 101\r\n'
                         'a=rtpmap:101 telephone-event/8000\r\n'
                         'a=fmtp:101 0-15\r\n'
                         'a=sendrecv\r\n')
        return messageString

    @property
    def bobResponseString(self):
        # TODO: need to fix up the addresses and transport type and stuff.
        # atlanta == .2 / .97
        # biloxi == .3 / .96
        # alice == .4 / .188
        # bob == .5 / .204
        messageString = ('SIP/2.0 180 Ringing\r\n'
                         'Via: SIP/2.0/UDP 192.168.4.3;branch=z9hG4bKeb83.c2fe646b6c2d21c6f9f113d37c474768.0\r\n'
                         'Via: SIP/2.0/UDP 192.168.4.2:56731;received=192.168.4.4;branch=z9hG4bK-524287-1---e500d061e354193a;rport=56731\r\n'
                         'Via: SIP/2.0/UDP 192.168.4.4;branch=z9hG4bKeb83.c2fe646b6c2d21c6f9f113d37c474768.0\r\n'
                         'Record-Route: <sip:192.168.4.3;lr>\r\n'
                         'Record-Route: <sip:192.168.4.2;lr>\r\n'
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

    def aliceRequestEventHandler(self, aConnectedSIPMessage):
        self.aliceReceivedRequests.append(aConnectedSIPMessage)

    def aliceResponseEventHandler(self, aConnectedSIPMessage):
        self.aliceReceivedResponses.append(aConnectedSIPMessage)

    def atlantaRequestEventHandler(self, aConnectedSIPMessage):
        self.atlantaReceivedRequests.append(aConnectedSIPMessage)

    def atlantaResponseEventHandler(self, aConnectedSIPMessage):
        self.atlantaReceivedResponses.append(aConnectedSIPMessage)

    def biloxiRequestEventHandler(self, aConnectedSIPMessage):
        self.biloxiReceivedRequests.append(aConnectedSIPMessage)

    def biloxiResponseEventHandler(self, aConnectedSIPMessage):
        self.biloxiReceivedResponses.append(aConnectedSIPMessage)

    def bobRequestEventHandler(self, aConnectedSIPMessage):
        self.bobReceivedRequests.append(aConnectedSIPMessage)

    def bobResponseEventHandler(self, aConnectedSIPMessage):
        self.bobReceivedResponses.append(aConnectedSIPMessage)

