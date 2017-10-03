import unittest
from unittest import TestCase
import sys
sys.path.append("../..")
from bobstack.sipmessaging import SIPMessageFactory
from bobstack.siptransport import UDPSIPTransport
from bobstack.siptransport import UDPSIPTransportConnection
from abstractTransportConnectionTestCase import AbstractTransportConnectionTestCase


# TODO
@unittest.skip("temporarily skipping.")
class TestUDPTransportConnection(AbstractTransportConnectionTestCase):
    # TODO - need to implement!
    # TODO:  will push most of this up.

    def setUp(self):
        self.hasBound = False
        self.bindHasFailed = False
        self.connectedConnections = []
        self.notConnectedAddressesAndPorts = []
        self.receivedRequests = []
        self.receivedResponses = []
        self.transport1 = UDPSIPTransport(self.bindAddress1, self.bindPort1)
        self.transport1.when_event_do("bound", self.bound_event_handler)
        self.transport1.when_event_do("bindFailed", self.bind_failed_event_handler)
        self.transport1.when_event_do("madeConnection", self.made_connection_event_handler)
        self.transport1.when_event_do("couldNotMakeConnection", self.could_not_make_connection_event_handler)
        self.transport1.when_event_do("lostConnection", self.lost_connection_event_handler)
        self.transport1.when_event_do("receivedValidConnectedRequest", self.received_valid_connected_request_event_handler)
        self.transport1.when_event_do("receivedValidConnectedResponse", self.received_valid_connected_response_event_handler)
        self.transport2 = UDPSIPTransport(self.bindAddress2, self.bindPort2)
        self.transport3 = UDPSIPTransport(self.bindAddress3, self.bindPort3)

    def test(self):
        self.run_00_initialSanityCheck()
        self.run_01_bind()
        self.run_02_makeOutboundConnection()
        self.run_03_makeInboundConnection()
        self.run_04_attemptSecondBind()
        self.run_05_attemptConnectToBogusAddressAndPort()
        self.run_06_attemptConnectToOwnAddressAndPort()
        self.run_07_sendRequestsVerifyReceipt()
        self.run_08_sendResponsesVerifyReceipt()

    def run_00_initialSanityCheck(self):
        self.assertIsInstance(self.transport1, UDPSIPTransport)
        self.assertEqual(0, len(self.transport1.connections))
        self.assertEqual(0, len(self.connectedConnections))
        self.assertEqual(0, len(self.receivedRequests))
        self.assertEqual(0, len(self.receivedResponses))
        self.assertFalse(self.transport1.is_reliable)
        self.assertEqual('UDP', self.transport1.transport_parameter_name)
        self.assertEqual(self.bindAddress1, self.transport1.bind_address)
        self.assertEqual(self.bindPort1, self.transport1.bind_port)
        self.assertFalse(self.hasBound)
        self.assertFalse(self.bindHasFailed)
        self.assertIsInstance(self.transport2, UDPSIPTransport)
        self.assertEqual(0, len(self.transport2.connections))
        self.assertFalse(self.transport2.is_reliable)
        # TODO:  LEFT OFF HERE.
        self.assertEqual('UDP', self.transport2.transport_parameter_name)
        self.assertEqual(self.bindAddress2, self.transport2.bind_address)
        self.assertEqual(self.bindPort2, self.transport2.bind_port)
        self.assertIsInstance(self.transport3, UDPSIPTransport)
        self.assertEqual(0, len(self.transport3.connections))
        self.assertFalse(self.transport3.is_reliable)
        self.assertEqual('UDP', self.transport3.transport_parameter_name)
        self.assertEqual(self.bindAddress3, self.transport3.bind_address)
        self.assertEqual(self.bindPort3, self.transport3.bind_port)
        # self.assertEqual(0, len(SimulatedNetwork.instance.boundTransports))

    def run_01_bind(self):
        self.transport1.bind()
        # self.assertEqual(1, len(SimulatedNetwork.instance.boundTransports))
        self.assertTrue(self.hasBound)
        self.assertFalse(self.bindHasFailed)
        self.assertEqual(0, len(self.transport1.connections))
        self.assertEqual(0, len(self.connectedConnections))
        self.transport2.bind()
        # self.assertEqual(2, len(SimulatedNetwork.instance.boundTransports))
        self.transport3.bind()
        # self.assertEqual(3, len(SimulatedNetwork.instance.boundTransports))
        # self.assertEqual(self.transport1, SimulatedNetwork.instance.boundTransports[0])
        # self.assertEqual(self.transport2, SimulatedNetwork.instance.boundTransports[1])
        # self.assertEqual(self.transport3, SimulatedNetwork.instance.boundTransports[2])
        # self.assertIs(self.transport1, SimulatedNetwork.instance.bound_transport_with_address_and_port(self.bindAddress1, self.bindPort1))
        # self.assertIs(self.transport2, SimulatedNetwork.instance.bound_transport_with_address_and_port(self.bindAddress2, self.bindPort2))
        # self.assertIs(self.transport3, SimulatedNetwork.instance.bound_transport_with_address_and_port(self.bindAddress3, self.bindPort3))

    def run_02_makeOutboundConnection(self):
        # Connect transport1 to transport2
        self.transport1.connect_to_address_and_port(self.bindAddress2, self.bindPort2)
        self.assertEqual(1, len(self.transport1.connections))
        self.assertEqual(1, len(self.connectedConnections))
        self.assertIs(self.connectedConnections[0], self.transport1.connections[0])
        self.assertEqual(self.bindAddress2, self.transport1.connections[0].remoteAddress)
        self.assertIsInstance(self.transport1.connections[0].bind_port, int)
        self.assertIsInstance(self.transport1.connections[0].id, basestring)
        self.assertEqual(self.bindPort2, self.transport1.connections[0].remotePort)
        # Not with UDP...
        # self.assertEqual(1, len(self.transport2.connections))
        self.assertEqual(0, len(self.transport3.connections))
        # self.assertEqual(self.bindAddress1, self.transport2.connections[0].remoteAddress)
        # self.assertIsInstance(self.transport2.connections[0].remotePort, int)
        # self.assertIsInstance(self.transport2.connections[0].id, basestring)
        # self.assertEqual(self.bindPort2, self.transport2.connections[0].bind_port)

    def run_03_makeInboundConnection(self):
        # Connect transport3 to transport1
        self.transport3.connect_to_address_and_port(self.bindAddress1, self.bindPort1)
        # self.assertEqual(2, len(self.transport1.connections))
        # self.assertEqual(1, len(self.transport2.connections))
        self.assertEqual(1, len(self.transport3.connections))
        # self.assertEqual(2, len(self.connectedConnections))
        # self.assertIs(self.connectedConnections[1], self.transport1.connections[1])
        # self.assertEqual(self.bindAddress3, self.transport1.connections[1].remoteAddress)
        self.assertIsInstance(self.transport3.connections[0].bind_port, int)
        self.assertIsInstance(self.transport3.connections[0].id, basestring)
        self.assertEqual(self.bindPort1, self.transport1.connections[0].bind_port)
        self.assertEqual(self.bindAddress1, self.transport3.connections[0].remoteAddress)
        self.assertIsInstance(self.transport1.connections[0].remotePort, int)
        self.assertEqual(self.bindPort1, self.transport3.connections[0].remotePort)

    def run_04_attemptSecondBind(self):
        self.assertFalse(self.bindHasFailed)
        transport = UDPSIPTransport(self.bindAddress1, self.bindPort1)
        transport.when_event_do("bindFailed", self.bind_failed_event_handler)
        transport.bind()
        # TODO:  The bind should have failed...
        # self.assertTrue(self.bindHasFailed)

    def run_05_attemptConnectToBogusAddressAndPort(self):
        self.assertEqual(0, len(self.notConnectedAddressesAndPorts))
        # self.assertEqual(2, len(self.transport1.connections))
        # self.transport1.connect_to_address_and_port('192.168.4.254', 5060)
        # self.assertEqual(1, len(self.notConnectedAddressesAndPorts))
        # self.assertEqual(2, len(self.transport1.connections))
        # self.assertEqual(('192.168.4.254', 5060), self.notConnectedAddressesAndPorts[0])
        # self.transport1.connect_to_address_and_port(self.bindAddress2, 5555)
        # self.assertEqual(2, len(self.notConnectedAddressesAndPorts))
        # self.assertEqual(2, len(self.transport1.connections))
        # self.assertEqual((self.bindAddress2, 5555), self.notConnectedAddressesAndPorts[1])

    def run_06_attemptConnectToOwnAddressAndPort(self):
        # self.assertEqual(2, len(self.notConnectedAddressesAndPorts))
        # self.assertEqual(2, len(self.transport1.connections))
        # self.transport1.connect_to_address_and_port(self.bindAddress1, self.bindPort1)
        # self.assertEqual(3, len(self.notConnectedAddressesAndPorts))
        # self.assertEqual(2, len(self.transport1.connections))
        # self.assertEqual((self.bindAddress1, self.bindPort1), self.notConnectedAddressesAndPorts[2])
        pass

    def run_07_sendRequestsVerifyReceipt(self):
        self.assertTrue(self.sampleRequest.is_request)
        self.assertTrue(self.sampleRequest2.is_request)
        self.assertEqual(0, len(self.receivedRequests))
        self.assertEqual(0, len(self.receivedResponses))
        # self.transport2.connections[0].send_message(self.sampleRequest)
        self.transport1.connections[0].send_message(self.sampleRequest)
        self.assertEqual(1, len(self.receivedRequests))
        self.assertEqual(0, len(self.receivedResponses))
        self.assertIs(self.sampleRequest.__class__, self.receivedRequests[0].sip_message.__class__)
        self.assertEqual(self.sampleRequest.raw_string, self.receivedRequests[0].sip_message.raw_string)
        self.transport3.connections[0].send_message(self.sampleRequest2)
        self.assertEqual(2, len(self.receivedRequests))
        self.assertEqual(0, len(self.receivedResponses))
        self.assertIs(self.sampleRequest2.__class__, self.receivedRequests[1].sip_message.__class__)
        self.assertEqual(self.sampleRequest2.raw_string, self.receivedRequests[1].sip_message.raw_string)

    def run_08_sendResponsesVerifyReceipt(self):
        self.assertTrue(self.sampleResponse.is_response)
        self.assertTrue(self.sampleResponse2.is_response)
        self.assertEqual(2, len(self.receivedRequests))
        self.assertEqual(0, len(self.receivedResponses))
        self.transport2.connections[0].send_message(self.sampleResponse)
        self.assertEqual(2, len(self.receivedRequests))
        self.assertEqual(1, len(self.receivedResponses))
        self.assertIs(self.sampleResponse.__class__, self.receivedResponses[0].sip_message.__class__)
        self.assertEqual(self.sampleResponse.raw_string, self.receivedResponses[0].sip_message.raw_string)
        self.transport3.connections[0].send_message(self.sampleResponse2)
        self.assertEqual(2, len(self.receivedRequests))
        self.assertEqual(2, len(self.receivedResponses))
        self.assertIs(self.sampleResponse2.__class__, self.receivedResponses[1].sip_message.__class__)
        self.assertEqual(self.sampleResponse2.raw_string, self.receivedResponses[1].sip_message.raw_string)

    def bound_event_handler(self):
        self.hasBound = True

    def bind_failed_event_handler(self):
        self.bindHasFailed = True

    def made_connection_event_handler(self, a_udp_sip_transport_connection):
        self.connectedConnections.append(a_udp_sip_transport_connection)

    def could_not_make_connection_event_handler(self, bind_address_and_port):
        address_and_port = bind_address_and_port
        self.notConnectedAddressesAndPorts.append(address_and_port)

    def lost_connection_event_handler(self, a_udp_sip_transport_connection):
        if a_udp_sip_transport_connection in self.connectedConnections:
            self.connectedConnections.remove(a_udp_sip_transport_connection)

    def received_valid_connected_request_event_handler(self, a_connected_aip_message):
        print("received_valid_connected_request_event_handler")
        self.receivedRequests.append(a_connected_aip_message)

    def received_valid_connected_response_event_handler(self, a_connected_aip_message):
        print("received_valid_connected_response_event_handler")
        self.receivedResponses.append(a_connected_aip_message)

