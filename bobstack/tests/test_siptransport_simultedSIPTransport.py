from unittest import TestCase
import sys
sys.path.append("../..")
from bobstack.siptransport import SimulatedSIPTransport
from bobstack.siptransport import SimulatedSIPTransportConnection
from bobstack.siptransport import SimulatedNetwork
from abstractTransportConnectionTestCase import AbstractTransportConnectionTestCase


class TestSimulatedTransportConnection(AbstractTransportConnectionTestCase):
    # TODO:  will push most of this up.

    def setUp(self):
        SimulatedNetwork.clear()
        self.hasBound = False
        self.bindHasFailed = False
        self.connectedConnections = []
        self.notConnectedAddressesAndPorts = []
        self.receivedRequests = []
        self.receivedResponses = []
        self.transport1 = SimulatedSIPTransport(self.bindAddress1, self.bindPort1)
        self.transport1.whenEventDo("bound", self.boundEventHandler)
        self.transport1.whenEventDo("bindFailed", self.bindFailedEventHandler)
        self.transport1.whenEventDo("madeConnection", self.madeConnectionEventHandler)
        self.transport1.whenEventDo("couldNotMakeConnection", self.couldNotMakeConnectionEventHandler)
        self.transport1.whenEventDo("lostConnection", self.lostConnectionEventHandler)
        self.transport1.whenEventDo("receivedValidConnectedRequest", self.receivedValidConnectedRequestEventHandler)
        self.transport1.whenEventDo("receivedValidConnectedResponse", self.receivedValidConnectedResponseEventHandler)
        self.transport2 = SimulatedSIPTransport(self.bindAddress2, self.bindPort2)
        self.transport3 = SimulatedSIPTransport(self.bindAddress3, self.bindPort3)

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
        self.assertIsInstance(self.transport1, SimulatedSIPTransport)
        self.assertEqual(0, len(self.transport1.connections))
        self.assertEqual(0, len(self.connectedConnections))
        self.assertEqual(0, len(self.receivedRequests))
        self.assertEqual(0, len(self.receivedResponses))
        self.assertTrue(self.transport1.isReliable)
        self.assertEqual('SIM', self.transport1.transportParameterName)
        self.assertEqual(self.bindAddress1, self.transport1.bind_address)
        self.assertEqual(self.bindPort1, self.transport1.bind_port)
        self.assertFalse(self.hasBound)
        self.assertFalse(self.bindHasFailed)
        self.assertIsInstance(self.transport2, SimulatedSIPTransport)
        self.assertEqual(0, len(self.transport2.connections))
        self.assertTrue(self.transport2.isReliable)
        self.assertEqual('SIM', self.transport2.transportParameterName)
        self.assertEqual(self.bindAddress2, self.transport2.bind_address)
        self.assertEqual(self.bindPort2, self.transport2.bind_port)
        self.assertIsInstance(self.transport3, SimulatedSIPTransport)
        self.assertEqual(0, len(self.transport3.connections))
        self.assertTrue(self.transport3.isReliable)
        self.assertEqual('SIM', self.transport3.transportParameterName)
        self.assertEqual(self.bindAddress3, self.transport3.bind_address)
        self.assertEqual(self.bindPort3, self.transport3.bind_port)
        self.assertEqual(0, len(SimulatedNetwork.instance.boundTransports))

    def run_01_bind(self):
        self.transport1.bind()
        self.assertEqual(1, len(SimulatedNetwork.instance.boundTransports))
        self.assertTrue(self.hasBound)
        self.assertFalse(self.bindHasFailed)
        self.assertEqual(0, len(self.transport1.connections))
        self.assertEqual(0, len(self.connectedConnections))
        self.transport2.bind()
        self.assertEqual(2, len(SimulatedNetwork.instance.boundTransports))
        self.transport3.bind()
        self.assertEqual(3, len(SimulatedNetwork.instance.boundTransports))
        self.assertEqual(self.transport1, SimulatedNetwork.instance.boundTransports[0])
        self.assertEqual(self.transport2, SimulatedNetwork.instance.boundTransports[1])
        self.assertEqual(self.transport3, SimulatedNetwork.instance.boundTransports[2])
        self.assertIs(self.transport1, SimulatedNetwork.instance.boundTransportWithAddressAndPort(self.bindAddress1, self.bindPort1))
        self.assertIs(self.transport2, SimulatedNetwork.instance.boundTransportWithAddressAndPort(self.bindAddress2, self.bindPort2))
        self.assertIs(self.transport3, SimulatedNetwork.instance.boundTransportWithAddressAndPort(self.bindAddress3, self.bindPort3))

    def run_02_makeOutboundConnection(self):
        # Connect transport1 to transport2
        self.transport1.connectToAddressAndPort(self.bindAddress2, self.bindPort2)
        self.assertEqual(1, len(self.transport1.connections))
        self.assertEqual(1, len(self.connectedConnections))
        self.assertIs(self.connectedConnections[0], self.transport1.connections[0])
        self.assertEqual(self.bindAddress2, self.transport1.connections[0].remoteAddress)
        self.assertIsInstance(self.transport1.connections[0].bind_port, int)
        self.assertIsInstance(self.transport1.connections[0].id, basestring)
        self.assertEqual(self.bindPort2, self.transport1.connections[0].remotePort)
        self.assertEqual(1, len(self.transport2.connections))
        self.assertEqual(0, len(self.transport3.connections))
        self.assertEqual(self.bindAddress1, self.transport2.connections[0].remoteAddress)
        self.assertIsInstance(self.transport2.connections[0].remotePort, int)
        self.assertIsInstance(self.transport2.connections[0].id, basestring)
        self.assertEqual(self.bindPort2, self.transport2.connections[0].bind_port)

    def run_03_makeInboundConnection(self):
        # Connect transport3 to transport1
        self.transport3.connectToAddressAndPort(self.bindAddress1, self.bindPort1)
        self.assertEqual(2, len(self.transport1.connections))
        self.assertEqual(1, len(self.transport2.connections))
        self.assertEqual(1, len(self.transport3.connections))
        self.assertEqual(2, len(self.connectedConnections))
        self.assertIs(self.connectedConnections[1], self.transport1.connections[1])
        self.assertEqual(self.bindAddress3, self.transport1.connections[1].remoteAddress)
        self.assertIsInstance(self.transport3.connections[0].bind_port, int)
        self.assertIsInstance(self.transport3.connections[0].id, basestring)
        self.assertEqual(self.bindPort1, self.transport1.connections[0].bind_port)
        self.assertEqual(self.bindAddress1, self.transport3.connections[0].remoteAddress)
        self.assertIsInstance(self.transport1.connections[0].remotePort, int)
        self.assertEqual(self.bindPort1, self.transport3.connections[0].remotePort)

    def run_04_attemptSecondBind(self):
        self.assertFalse(self.bindHasFailed)
        transport = SimulatedSIPTransport(self.bindAddress1, self.bindPort1)
        transport.whenEventDo("bindFailed", self.bindFailedEventHandler)
        transport.bind()
        self.assertTrue(self.bindHasFailed)

    def run_05_attemptConnectToBogusAddressAndPort(self):
        self.assertEqual(0, len(self.notConnectedAddressesAndPorts))
        self.assertEqual(2, len(self.transport1.connections))
        self.transport1.connectToAddressAndPort('192.168.4.254', 5060)
        self.assertEqual(1, len(self.notConnectedAddressesAndPorts))
        self.assertEqual(2, len(self.transport1.connections))
        self.assertEqual(('192.168.4.254', 5060), self.notConnectedAddressesAndPorts[0])
        self.transport1.connectToAddressAndPort(self.bindAddress2, 5555)
        self.assertEqual(2, len(self.notConnectedAddressesAndPorts))
        self.assertEqual(2, len(self.transport1.connections))
        self.assertEqual((self.bindAddress2, 5555), self.notConnectedAddressesAndPorts[1])

    def run_06_attemptConnectToOwnAddressAndPort(self):
        self.assertEqual(2, len(self.notConnectedAddressesAndPorts))
        self.assertEqual(2, len(self.transport1.connections))
        self.transport1.connectToAddressAndPort(self.bindAddress1, self.bindPort1)
        self.assertEqual(3, len(self.notConnectedAddressesAndPorts))
        self.assertEqual(2, len(self.transport1.connections))
        self.assertEqual((self.bindAddress1, self.bindPort1), self.notConnectedAddressesAndPorts[2])

    def run_07_sendRequestsVerifyReceipt(self):
        self.assertTrue(self.sampleRequest.isRequest)
        self.assertTrue(self.sampleRequest2.isRequest)
        self.assertEqual(0, len(self.receivedRequests))
        self.assertEqual(0, len(self.receivedResponses))
        self.transport2.connections[0].sendMessage(self.sampleRequest)
        self.assertEqual(1, len(self.receivedRequests))
        self.assertEqual(0, len(self.receivedResponses))
        self.assertIs(self.sampleRequest.__class__, self.receivedRequests[0].sipMessage.__class__)
        self.assertEqual(self.sampleRequest.rawString, self.receivedRequests[0].sipMessage.rawString)
        self.transport3.connections[0].sendMessage(self.sampleRequest2)
        self.assertEqual(2, len(self.receivedRequests))
        self.assertEqual(0, len(self.receivedResponses))
        self.assertIs(self.sampleRequest2.__class__, self.receivedRequests[1].sipMessage.__class__)
        self.assertEqual(self.sampleRequest2.rawString, self.receivedRequests[1].sipMessage.rawString)

    def run_08_sendResponsesVerifyReceipt(self):
        self.assertTrue(self.sampleResponse.isResponse)
        self.assertTrue(self.sampleResponse2.isResponse)
        self.assertEqual(2, len(self.receivedRequests))
        self.assertEqual(0, len(self.receivedResponses))
        self.transport2.connections[0].sendMessage(self.sampleResponse)
        self.assertEqual(2, len(self.receivedRequests))
        self.assertEqual(1, len(self.receivedResponses))
        self.assertIs(self.sampleResponse.__class__, self.receivedResponses[0].sipMessage.__class__)
        self.assertEqual(self.sampleResponse.rawString, self.receivedResponses[0].sipMessage.rawString)
        self.transport3.connections[0].sendMessage(self.sampleResponse2)
        self.assertEqual(2, len(self.receivedRequests))
        self.assertEqual(2, len(self.receivedResponses))
        self.assertIs(self.sampleResponse2.__class__, self.receivedResponses[1].sipMessage.__class__)
        self.assertEqual(self.sampleResponse2.rawString, self.receivedResponses[1].sipMessage.rawString)

    def boundEventHandler(self):
        self.hasBound = True

    def bindFailedEventHandler(self):
        self.bindHasFailed = True

    def madeConnectionEventHandler(self, a_simulated_sip_transport_connection):
        self.connectedConnections.append(a_simulated_sip_transport_connection)

    def couldNotMakeConnectionEventHandler(self, bind_address_and_port):
        addressAndPort = bind_address_and_port
        self.notConnectedAddressesAndPorts.append(addressAndPort)

    def lostConnectionEventHandler(self, a_simulated_sip_transport_connection):
        if a_simulated_sip_transport_connection in self.connectedConnections:
            self.connectedConnections.remove(a_simulated_sip_transport_connection)

    def receivedValidConnectedRequestEventHandler(self, a_connected_aip_message):
        print("receivedValidConnectedRequestEventHandler")
        self.receivedRequests.append(a_connected_aip_message)

    def receivedValidConnectedResponseEventHandler(self, a_connected_aip_message):
        print("receivedValidConnectedResponseEventHandler")
        self.receivedResponses.append(a_connected_aip_message)

