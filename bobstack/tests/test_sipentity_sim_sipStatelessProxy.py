# import sys
# sys.path.append("..")
# sys.path.append("../..")
from abstractStatelessProxyTestCase import AbstractStatelessProxyTestCase
from ..sipmessaging import SIPURI
from ..siptransport import SimulatedSIPTransport
from ..sipentity import SIPStatelessProxy
from ..siptransport import SimulatedNetwork


class TestStatelessProxyWithSimulatedTransport(AbstractStatelessProxyTestCase):
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
        self.atlanta.transports = [SimulatedSIPTransport(self.atlanta_bind_address, self.atlanta_bind_port)]
        self.biloxi = SIPStatelessProxy()
        self.biloxi.transports = [SimulatedSIPTransport(self.biloxi_bind_address, self.biloxi_bind_port)]
        self.alice_transport = SimulatedSIPTransport(self.alice_bind_address, self.aliceBindPort)
        self.bob_transport = SimulatedSIPTransport(self.bob_bind_address, self.bobBindPort)
        self.alice_transport.when_event_do("receivedValidConnectedRequest", self.aliceRequestEventHandler)
        self.alice_transport.when_event_do("receivedValidConnectedResponse", self.aliceResponseEventHandler)
        self.atlanta.transports[0].when_event_do("receivedValidConnectedRequest", self.atlantaRequestEventHandler)
        self.atlanta.transports[0].when_event_do("receivedValidConnectedResponse", self.atlantaResponseEventHandler)
        self.biloxi.transports[0].when_event_do("receivedValidConnectedRequest", self.biloxiRequestEventHandler)
        self.biloxi.transports[0].when_event_do("receivedValidConnectedResponse", self.biloxiResponseEventHandler)
        self.bob_transport.when_event_do("receivedValidConnectedRequest", self.bobRequestEventHandler)
        self.bob_transport.when_event_do("receivedValidConnectedResponse", self.bobResponseEventHandler)
        self.alice_transport.bind()
        self.bob_transport.bind()
        self.alice_transport.connect_to_address_and_port(self.atlanta_bind_address, self.atlanta_bind_port)
        # Let Biloxi connect to Bob.  Don't pre-connect Bob to Biloxi.
        # self.bob_transport.connect_to_address_and_port(self.biloxi_bind_address, self.biloxi_bind_port)
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
        self.assertEqual(self.atlanta_bind_address, self.atlanta.transports[0].bind_address)
        self.assertEqual(self.atlanta_bind_port, self.atlanta.transports[0].bind_port)
        self.assertEqual(self.atlanta_bind_address, self.atlanta.transports[0].connections[0].bind_address)
        self.assertEqual(self.atlanta_bind_port, self.atlanta.transports[0].connections[0].bind_port)
        self.assertEqual(self.atlanta_bind_address, self.alice_transport.connections[0].remoteAddress)
        self.assertEqual(self.atlanta_bind_port, self.alice_transport.connections[0].remotePort)
        self.assertEqual(self.alice_bind_address, self.atlanta.transports[0].connections[0].remoteAddress)
        self.assertEqual(self.aliceBindPort, self.atlanta.transports[0].connections[0].remotePort)
        self.assertEqual(self.biloxi_bind_address, self.biloxi.transports[0].bind_address)
        self.assertEqual(self.biloxi_bind_port, self.biloxi.transports[0].bind_port)
        self.assertEqual(0, len(self.aliceReceivedRequests))
        self.assertEqual(0, len(self.aliceReceivedResponses))
        self.assertEqual(0, len(self.atlantaReceivedRequests))
        self.assertEqual(0, len(self.atlantaReceivedResponses))
        self.assertEqual(0, len(self.biloxiReceivedRequests))
        self.assertEqual(0, len(self.biloxiReceivedResponses))
        self.assertEqual(0, len(self.bobReceivedRequests))
        self.assertEqual(0, len(self.bobReceivedResponses))

    def run_01_atlantaToBiloxi(self):
        self.alice_transport.connections[0].send_string(self.aliceRequestString)
        self.assertEqual(0, len(self.aliceReceivedRequests))
        # self.assertEqual(1, len(self.aliceReceivedResponses))
        self.assertEqual(1, len(self.atlantaReceivedRequests))
        self.assertEqual(1, len(self.biloxiReceivedRequests))
        self.assertEqual(1, len(self.atlantaReceivedResponses))
        self.assertEqual(0, len(self.biloxiReceivedResponses))
        self.assertEqual(0, len(self.bobReceivedRequests))
        self.assertEqual(0, len(self.bobReceivedResponses))

        self.assertEqual(self.alice_bind_address, self.atlantaReceivedRequests[0].connection.remoteAddress)
        self.assertEqual(self.aliceBindPort, self.atlantaReceivedRequests[0].connection.remotePort)
        self.assertEqual(self.atlanta_bind_address, self.atlantaReceivedRequests[0].connection.bind_address)
        self.assertEqual(self.atlanta_bind_port, self.atlantaReceivedRequests[0].connection.bind_port)
        atlanta_received_request = self.atlantaReceivedRequests[0].sip_message
        ruri = SIPURI.new_parsed_from(atlanta_received_request.start_line.request_uri)
        self.assertEqual(self.aliceRequestString, atlanta_received_request.raw_string)
        self.assertEqual('INVITE', atlanta_received_request.start_line.sip_method)
        self.assertEqual(self.biloxi_bind_address, ruri.host)
        self.assertEqual(1, len(atlanta_received_request.vias))
        self.assertEqual(self.aliceRequestString, atlanta_received_request.raw_string)
        self.assertIsNone(atlanta_received_request.header.to_tag)

        self.assertEqual(self.atlanta_bind_address, self.biloxiReceivedRequests[0].connection.remoteAddress)
        self.assertEqual(self.atlanta_bind_port, self.biloxiReceivedRequests[0].connection.remotePort)
        self.assertEqual(self.biloxi_bind_address, self.biloxiReceivedRequests[0].connection.bind_address)
        self.assertEqual(self.biloxi_bind_port, self.biloxiReceivedRequests[0].connection.bind_port)
        biloxi_received_request = self.biloxiReceivedRequests[0].sip_message
        self.assertEqual(atlanta_received_request.start_line.request_uri, biloxi_received_request.start_line.request_uri)
        self.assertEqual('INVITE', biloxi_received_request.start_line.sip_method)
        self.assertEqual(2, len(biloxi_received_request.vias))
        self.assertNotEqual(self.aliceRequestString, biloxi_received_request.raw_string)
        self.assertIsNone(biloxi_received_request.header.to_tag)

        self.assertEqual(self.biloxi_bind_address, self.atlantaReceivedResponses[0].connection.remoteAddress)
        self.assertEqual(self.biloxi_bind_port, self.atlantaReceivedResponses[0].connection.remotePort)
        self.assertEqual(self.atlanta_bind_address, self.atlantaReceivedResponses[0].connection.bind_address)
        self.assertEqual(self.atlanta_bind_port, self.atlantaReceivedResponses[0].connection.bind_port)
        atlanta_received_response = self.atlantaReceivedResponses[0].sip_message
        self.assertIsNotNone(atlanta_received_response.header.to_tag)
        self.assertEqual(2, len(atlanta_received_response.vias))

        self.assertEqual(self.atlanta_bind_address, self.aliceReceivedResponses[0].connection.remoteAddress)
        self.assertEqual(self.atlanta_bind_port, self.aliceReceivedResponses[0].connection.remotePort)
        self.assertEqual(self.alice_bind_address, self.aliceReceivedResponses[0].connection.bind_address)
        self.assertEqual(self.aliceBindPort, self.aliceReceivedResponses[0].connection.bind_port)
        alice_received_response = self.aliceReceivedResponses[0].sip_message
        self.assertIsNotNone(alice_received_response.header.to_tag)
        self.assertEqual(1, len(alice_received_response.vias))

        self.assertEqual(self.alice_bind_address, atlanta_received_request.via_header_fields[0].host)
        # TODO: This 404 nonsense is temporary.  Alice sends to a biloxi domain via atlanta, atlanta forwards her request to biloxi,
        # Biloxi sees that it is responsible for the request, and for right now, just answers 404.
        self.assertEqual(404, self.atlantaReceivedResponses[0].sip_message.start_line.status_code)
        self.assertEqual(404, self.aliceReceivedResponses[0].sip_message.start_line.status_code)

        # TODO:  Moar!!!

    def run_02_biloxiToAtlanta(self):
        pass

    @property
    def alice_bind_address(self):
        # return '192.168.4.4'
        return '127.0.0.2'

    @property
    def aliceBindPort(self):
        # Note the port in the Via header field...
        # return 5060
        return 63354

    @property
    def atlanta_bind_address(self):
        # return '192.168.4.2'
        return '127.0.0.3'

    @property
    def atlanta_bind_port(self):
        return 5060

    @property
    def biloxi_bind_address(self):
        # return '192.168.4.3'
        return '127.0.0.4'

    @property
    def biloxi_bind_port(self):
        return 5060

    @property
    def bob_bind_address(self):
        # return '192.168.4.5'
        return '127.0.0.5'

    @property
    def bobBindPort(self):
        return 5060

    @property
    def aliceRequestString(self):
        # Bob's extension is 1002
        # atlanta == .2 / .97
        # biloxi == .3 / .96
        # alice == .2 / .188
        # bob == .5 / .204
        # message_string = ('INVITE sip:1002@192.168.4.3 SIP/2.0\r\n'
        #                  'Via: SIP/2.0/UDP 192.168.4.4:63354;branch=z9hG4bK-524287-1---7a462a5d1b6fe13b;rport\r\n'
        #                  'Max-Forwards: 70\r\n'
        #                  'Contact: <sip:alice@192.168.4.4:63354;rinstance=d875ce4fd8f72441>\r\n'
        #                  'To: <sip:1002@192.168.4.3>\r\n'
        #                  'From: "Alice"<sip:alice@192.168.4.2>;tag=9980376d\r\n'
        #                  'Call-ID: YjBhMDliMWMxNzQ4ZTc5Nzg1ZTcyYTExMWMzZDlhNmQ\r\n'
        #                  'CSeq: 1 INVITE\r\n'
        #                  'Allow: INVITE, ACK, CANCEL, BYE, REFER, INFO, NOTIFY, UPDATE, PRACK, MESSAGE, OPTIONS, SUBSCRIBE, OPTIONS\r\n'
        #                  'Content-Type: application/sdp\r\n'
        #                  'Supported: replaces, 100rel\r\n'
        #                  'User-Agent: Bria iOS release 3.6.2 stamp 33024\r\n'
        #                  'Content-Length: 185\r\n'
        #                  '\r\n'
        #                  'v=0\r\n'
        #                  'o=- 1457365987528724 1 IN IP4 192.168.4.4\r\n'
        #                  's=Cpc session\r\n'
        #                  'c=IN IP4 192.168.4.4\r\n'
        #                  't=0 0\r\n'
        #                  'm=audio 60668 RTP/AVP 0 101\r\n'
        #                  'a=rtpmap:101 telephone-event/8000\r\n'
        #                  'a=fmtp:101 0-15\r\n'
        #                  'a=sendrecv\r\n')
        message_string = ('INVITE sip:1002@127.0.0.4 SIP/2.0\r\n'
                          'Via: SIP/2.0/UDP 127.0.0.2:63354;branch=z9hG4bK-524287-1---7a462a5d1b6fe13b;rport\r\n'
                          'Max-Forwards: 70\r\n'
                          'Contact: <sip:alice@127.0.0.2:63354;rinstance=d875ce4fd8f72441>\r\n'
                          'To: <sip:1002@127.0.0.4>\r\n'
                          'From: "Alice"<sip:alice@127.0.0.3>;tag=9980376d\r\n'
                          'Call-ID: YjBhMDliMWMxNzQ4ZTc5Nzg1ZTcyYTExMWMzZDlhNmQ\r\n'
                          'CSeq: 1 INVITE\r\n'
                          'Allow: INVITE, ACK, CANCEL, BYE, REFER, INFO, NOTIFY, UPDATE, PRACK, MESSAGE, OPTIONS, SUBSCRIBE, OPTIONS\r\n'
                          'Content-Type: application/sdp\r\n'
                          'Supported: replaces, 100rel\r\n'
                          'User-Agent: Bria iOS release 3.6.2 stamp 33024\r\n'
                          'Content-Length: 181\r\n'
                          '\r\n'
                          'v=0\r\n'
                          'o=- 1457365987528724 1 IN IP4 127.0.0.2\r\n'
                          's=Cpc session\r\n'
                          'c=IN IP4 127.0.0.2\r\n'
                          't=0 0\r\n'
                          'm=audio 60668 RTP/AVP 0 101\r\n'
                          'a=rtpmap:101 telephone-event/8000\r\n'
                          'a=fmtp:101 0-15\r\n'
                          'a=sendrecv\r\n')
        return message_string

    # @property
    # def aliceResponseString(self):
        # TODO: need to fix up the addresses and transport type and stuff.
        # atlanta == .2 / .97
        # biloxi == .3 / .96
        # alice == .4 / .188
        # bob == .5 / .204
        # message_string = ('SIP/2.0 180 Ringing\r\n'
        #                  'Via: SIP/2.0/UDP 192.168.4.2;branch=z9hG4bKeb83.c2fe646b6c2d21c6f9f113d37c474768.0\r\n'
        #                  'Via: SIP/2.0/UDP 192.168.4.3:56731;received=192.168.4.4;branch=z9hG4bK-524287-1---e500d061e354193a;rport=56731\r\n'
        #                  'Via: SIP/2.0/UDP 192.168.4.5;branch=z9hG4bKeb83.c2fe646b6c2d21c6f9f113d37c474768.0\r\n'
        #                  'Record-Route: <sip:192.168.4.2;lr>\r\n'
        #                  'Record-Route: <sip:192.168.4.3;lr>\r\n'
        #                  'Require: 100rel\r\n'
        #                  'Contact: <sip:1002@192.168.0.204:52909;rinstance=7caea32dab180286>\r\n'
        #                  'To: "Bob"<sip:1002@192.168.0.96>;tag=52e9ef73\r\n'
        #                  'From: "Alice"<sip:1001@192.168.0.96>;tag=2210ba44\r\n'
        #                  'Call-ID: NTM5YzAxN2YwZGRhYTg2YjBkNDgyNWQyNTI3ZGNmNTE\r\n'
        #                  'CSeq: 1 INVITE\r\n'
        #                  'Allow: INVITE, ACK, CANCEL, BYE, REFER, INFO, NOTIFY, UPDATE, PRACK, MESSAGE, OPTIONS, SUBSCRIBE, OPTIONS\r\n'
        #                  'Supported: replaces\r\n'
        #                  'User-Agent: Bria iOS release 3.6.2 stamp 33024\r\n'
        #                  'Allow-Events: talk, hold\r\n'
        #                  'RSeq: 1\r\n'
        #                  'Content-Length: 0\r\n'
        #                  '\r\n')
        # message_string = ('SIP/2.0 180 Ringing\r\n'
        #                  'Via: SIP/2.0/UDP 127.0.0.3;branch=z9hG4bKeb83.c2fe646b6c2d21c6f9f113d37c474768.0\r\n'
        #                  'Via: SIP/2.0/UDP 127.0.0.4:56731;received=127.0.0.2;branch=z9hG4bK-524287-1---e500d061e354193a;rport=56731\r\n'
        #                  'Via: SIP/2.0/UDP 127.0.0.5;branch=z9hG4bKeb83.c2fe646b6c2d21c6f9f113d37c474768.0\r\n'
        #                  'Record-Route: <sip:127.0.0.3;lr>\r\n'
        #                  'Record-Route: <sip:127.0.0.4;lr>\r\n'
        #                  'Require: 100rel\r\n'
        #                  'Contact: <sip:1002@192.168.0.204:52909;rinstance=7caea32dab180286>\r\n'
        #                  'To: "Bob"<sip:1002@192.168.0.96>;tag=52e9ef73\r\n'
        #                  'From: "Alice"<sip:1001@192.168.0.96>;tag=2210ba44\r\n'
        #                  'Call-ID: NTM5YzAxN2YwZGRhYTg2YjBkNDgyNWQyNTI3ZGNmNTE\r\n'
        #                  'CSeq: 1 INVITE\r\n'
        #                  'Allow: INVITE, ACK, CANCEL, BYE, REFER, INFO, NOTIFY, UPDATE, PRACK, MESSAGE, OPTIONS, SUBSCRIBE, OPTIONS\r\n'
        #                  'Supported: replaces\r\n'
        #                  'User-Agent: Bria iOS release 3.6.2 stamp 33024\r\n'
        #                  'Allow-Events: talk, hold\r\n'
        #                  'RSeq: 1\r\n'
        #                  'Content-Length: 0\r\n'
        #                  '\r\n')
        # return message_string

    @property
    def bobRequestString(self):
        # Alice's extension is 1001
        # atlanta == .2
        # biloxi == .3
        # alice == .4
        # bob == .5
        # message_string = ('INVITE sip:1001@192.168.4.2 SIP/2.0\r\n'
        #                  'Via: SIP/2.0/UDP 192.168.4.5:63354;branch=z9hG4bK-524287-1---7a462a5d1b6fe13b;rport\r\n'
        #                  'Max-Forwards: 70\r\n'
        #                  'Contact: <sip:bob@192.168.4.3:63354;rinstance=d875ce4fd8f72441>\r\n'
        #                  'To: <sip:1001@192.168.4.2>\r\n'
        #                  'From: "Alice"<sip:alice@192.168.4.2>;tag=9980376d\r\n'
        #                  'Call-ID: YjBhMDliMWMxNzQ4ZTc5Nzg1ZTcyYTExMWMzZDlhNmQ\r\n'
        #                  'CSeq: 1 INVITE\r\n'
        #                  'Allow: INVITE, ACK, CANCEL, BYE, REFER, INFO, NOTIFY, UPDATE, PRACK, MESSAGE, OPTIONS, SUBSCRIBE, OPTIONS\r\n'
        #                  'Content-Type: application/sdp\r\n'
        #                  'Supported: replaces, 100rel\r\n'
        #                  'User-Agent: Bria iOS release 3.6.2 stamp 33024\r\n'
        #                  'Content-Length: 185\r\n'
        #                  '\r\n'
        #                  'v=0\r\n'
        #                  'o=- 1457365987528724 1 IN IP4 192.168.4.5\r\n'
        #                  's=Cpc session\r\n'
        #                  'c=IN IP4 192.168.4.5\r\n'
        #                  't=0 0\r\n'
        #                  'm=audio 60668 RTP/AVP 0 101\r\n'
        #                  'a=rtpmap:101 telephone-event/8000\r\n'
        #                  'a=fmtp:101 0-15\r\n'
        #                  'a=sendrecv\r\n')
        message_string = ('INVITE sip:1001@127.0.0.3 SIP/2.0\r\n'
                          'Via: SIP/2.0/UDP 127.0.0.5:63354;branch=z9hG4bK-524287-1---7a462a5d1b6fe13b;rport\r\n'
                          'Max-Forwards: 70\r\n'
                          'Contact: <sip:bob@127.0.0.4:63354;rinstance=d875ce4fd8f72441>\r\n'
                          'To: <sip:1001@127.0.0.3>\r\n'
                          'From: "Alice"<sip:alice@127.0.0.3>;tag=9980376d\r\n'
                          'Call-ID: YjBhMDliMWMxNzQ4ZTc5Nzg1ZTcyYTExMWMzZDlhNmQ\r\n'
                          'CSeq: 1 INVITE\r\n'
                          'Allow: INVITE, ACK, CANCEL, BYE, REFER, INFO, NOTIFY, UPDATE, PRACK, MESSAGE, OPTIONS, SUBSCRIBE, OPTIONS\r\n'
                          'Content-Type: application/sdp\r\n'
                          'Supported: replaces, 100rel\r\n'
                          'User-Agent: Bria iOS release 3.6.2 stamp 33024\r\n'
                          'Content-Length: 181\r\n'
                          '\r\n'
                          'v=0\r\n'
                          'o=- 1457365987528724 1 IN IP4 127.0.0.5\r\n'
                          's=Cpc session\r\n'
                          'c=IN IP4 127.0.0.5\r\n'
                          't=0 0\r\n'
                          'm=audio 60668 RTP/AVP 0 101\r\n'
                          'a=rtpmap:101 telephone-event/8000\r\n'
                          'a=fmtp:101 0-15\r\n'
                          'a=sendrecv\r\n')
        return message_string

    # @property
    # def bobResponseString(self):
        # TODO: need to fix up the addresses and transport type and stuff.
        # atlanta == .2 / .97
        # biloxi == .3 / .96
        # alice == .4 / .188
        # bob == .5 / .204
        # message_string = ('SIP/2.0 180 Ringing\r\n'
        #                  'Via: SIP/2.0/UDP 192.168.4.3;branch=z9hG4bKeb83.c2fe646b6c2d21c6f9f113d37c474768.0\r\n'
        #                  'Via: SIP/2.0/UDP 192.168.4.2:56731;received=192.168.4.4;branch=z9hG4bK-524287-1---e500d061e354193a;rport=56731\r\n'
        #                  'Via: SIP/2.0/UDP 192.168.4.4;branch=z9hG4bKeb83.c2fe646b6c2d21c6f9f113d37c474768.0\r\n'
        #                  'Record-Route: <sip:192.168.4.3;lr>\r\n'
        #                  'Record-Route: <sip:192.168.4.2;lr>\r\n'
        #                  'Require: 100rel\r\n'
        #                  'Contact: <sip:1002@192.168.0.204:52909;rinstance=7caea32dab180286>\r\n'
        #                  'To: "Bob"<sip:1002@192.168.0.96>;tag=52e9ef73\r\n'
        #                  'From: "Alice"<sip:1001@192.168.0.96>;tag=2210ba44\r\n'
        #                  'Call-ID: NTM5YzAxN2YwZGRhYTg2YjBkNDgyNWQyNTI3ZGNmNTE\r\n'
        #                  'CSeq: 1 INVITE\r\n'
        #                  'Allow: INVITE, ACK, CANCEL, BYE, REFER, INFO, NOTIFY, UPDATE, PRACK, MESSAGE, OPTIONS, SUBSCRIBE, OPTIONS\r\n'
        #                  'Supported: replaces\r\n'
        #                  'User-Agent: Bria iOS release 3.6.2 stamp 33024\r\n'
        #                  'Allow-Events: talk, hold\r\n'
        #                  'RSeq: 1\r\n'
        #                  'Content-Length: 0\r\n'
        #                  '\r\n')
        # message_string = ('SIP/2.0 180 Ringing\r\n'
        #                  'Via: SIP/2.0/UDP 127.0.0.4;branch=z9hG4bKeb83.c2fe646b6c2d21c6f9f113d37c474768.0\r\n'
        #                  'Via: SIP/2.0/UDP 127.0.0.3:56731;received=127.0.0.2;branch=z9hG4bK-524287-1---e500d061e354193a;rport=56731\r\n'
        #                  'Via: SIP/2.0/UDP 127.0.0.2;branch=z9hG4bKeb83.c2fe646b6c2d21c6f9f113d37c474768.0\r\n'
        #                  'Record-Route: <sip:127.0.0.4;lr>\r\n'
        #                  'Record-Route: <sip:127.0.0.3;lr>\r\n'
        #                  'Require: 100rel\r\n'
        #                  'Contact: <sip:1002@192.168.0.204:52909;rinstance=7caea32dab180286>\r\n'
        #                  'To: "Bob"<sip:1002@192.168.0.96>;tag=52e9ef73\r\n'
        #                  'From: "Alice"<sip:1001@192.168.0.96>;tag=2210ba44\r\n'
        #                  'Call-ID: NTM5YzAxN2YwZGRhYTg2YjBkNDgyNWQyNTI3ZGNmNTE\r\n'
        #                  'CSeq: 1 INVITE\r\n'
        #                  'Allow: INVITE, ACK, CANCEL, BYE, REFER, INFO, NOTIFY, UPDATE, PRACK, MESSAGE, OPTIONS, SUBSCRIBE, OPTIONS\r\n'
        #                  'Supported: replaces\r\n'
        #                  'User-Agent: Bria iOS release 3.6.2 stamp 33024\r\n'
        #                  'Allow-Events: talk, hold\r\n'
        #                  'RSeq: 1\r\n'
        #                  'Content-Length: 0\r\n'
        #                  '\r\n')
        # return message_string

    def aliceRequestEventHandler(self, a_connected_aip_message):
        self.aliceReceivedRequests.append(a_connected_aip_message)

    def aliceResponseEventHandler(self, a_connected_aip_message):
        self.aliceReceivedResponses.append(a_connected_aip_message)

    def atlantaRequestEventHandler(self, a_connected_aip_message):
        self.atlantaReceivedRequests.append(a_connected_aip_message)

    def atlantaResponseEventHandler(self, a_connected_aip_message):
        self.atlantaReceivedResponses.append(a_connected_aip_message)

    def biloxiRequestEventHandler(self, a_connected_aip_message):
        self.biloxiReceivedRequests.append(a_connected_aip_message)

    def biloxiResponseEventHandler(self, a_connected_aip_message):
        self.biloxiReceivedResponses.append(a_connected_aip_message)

    def bobRequestEventHandler(self, a_connected_aip_message):
        self.bobReceivedRequests.append(a_connected_aip_message)

    def bobResponseEventHandler(self, a_connected_aip_message):
        self.bobReceivedResponses.append(a_connected_aip_message)


class TestStatelessProxyWithUDPTransport(AbstractStatelessProxyTestCase):
    pass


class TestStatelessProxyWithTCPTransport(AbstractStatelessProxyTestCase):
    pass


class TestStatelessProxyWithTLSTransport(AbstractStatelessProxyTestCase):
    pass

