from unittest import TestCase
import unittest
import sys
sys.path.append("../..")
from bobstack.siptransport import SimulatedSIPTransport
from bobstack.siptransport import SimulatedSIPTransportConnection

class TestSimulatedTransportConnection(TestCase):
    @property
    def bindAddress(self):
        return '192.168.4.2'

    @property
    def bindPort(self):
        return 5060

    @property
    def outboundConnectionAddress(self):
        return '192.168.4.3'

    @property
    def outboundConnectionPort(self):
        return 5062

    @property
    def inboundConnectionAddress(self):
        return '192.168.4.4'

    @property
    def inboundConnectionPort(self):
        return 5063

    def setUp(self):
        self.hasBound = False
        self.connectedConnections = []
        self.receivedRequests = []
        self.receivedResponses = []
        self.transport = SimulatedSIPTransport(self.bindAddress, self.bindPort)
        self.transport.whenEventDo("bound", self.boundEventHandler)
        self.transport.whenEventDo("madeConnection", self.madeConnectionEventHandler)
        self.transport.whenEventDo("lostConnection", self.lostConnectionEventHandler)
        self.transport.whenEventDo("receivedValidConnectedRequest", self.receivedValidConnectedRequestEventHandler)
        self.transport.whenEventDo("receivedValidConnectedResponse", self.receivedValidConnectedResponseEventHandler)


    # order of test execution matters, so use integers for specifying test execution order.

    def test_00_initialSanityCheck(self):
        self.assertIsInstance(self.transport, SimulatedSIPTransport)
        self.assertEqual(0, len(self.transport.connections))
        self.assertEqual(0, len(self.connectedConnections))
        self.assertEqual(0, len(self.receivedRequests))
        self.assertEqual(0, len(self.receivedResponses))
        self.assertTrue(self.transport.isReliable)
        self.assertEqual('SIM', self.transport.transportParameterName)
        self.assertEqual(self.bindAddress, self.transport.bindAddress)
        self.assertEqual(self.bindPort, self.transport.bindPort)
        self.assertFalse(self.hasBound)

    def test_01_bind(self):
        self.transport.bind()
        self.assertTrue(self.hasBound)
        self.assertEqual(0, len(self.transport.connections))
        self.assertEqual(0, len(self.connectedConnections))

    def test_02_makeOutboundConnection(self):
        self.transport.connectToAddressAndPort(self.outboundConnectionAddress, self.outboundConnectionPort)
        self.assertEqual(1, len(self.transport.connections))
        self.assertEqual(1, len(self.connectedConnections))
        self.assertIs(self.connectedConnections[0], self.transport.connections[0])
        self.assertEqual(self.outboundConnectionAddress, self.transport.connections[0].address)
        self.assertIsInstance(self.transport.connections[0].localPort, int)
        self.assertEqual(self.outboundConnectionPort, self.transport.connections[0].remotePort)

    def test_03_makeInboundConnection(self):
        self.transport.simulateConnectionFromAddressAndRemotePort(self.inboundConnectionAddress, self.inboundConnectionPort)
        self.assertEqual(2, len(self.transport.connections))
        self.assertEqual(2, len(self.connectedConnections))
        self.assertIs(self.connectedConnections[1], self.transport.connections[1])
        self.assertEqual(self.inboundConnectionAddress, self.transport.connections[1].address)
        self.assertEqual(self.bindPort, self.transport.connections[1].localPort)
        self.assertEqual(self.inboundConnectionPort, self.transport.connections[1].remotePort)

    # TODO:  next - send, receive messages, verify receipt.

    def boundEventHandler(self):
        self.hasBound = True

    def madeConnectionEventHandler(self, aSimulatedSIPTransportConnection):
        self.connectedConnections.append(aSimulatedSIPTransportConnection)

    def lostConnectionEventHandler(self, aSimulatedSIPTransportConnection):
        if aSimulatedSIPTransportConnection in self.connectedConnections:
            self.connectedConnections.remove(aSimulatedSIPTransportConnection)

    def receivedValidConnectedRequestEventHandler(self, aConnectedSIPMessage):
        self.receivedRequests.append(aConnectedSIPMessage)

    def receivedValidConnectedResponseEventHandler(self, aConnectedSIPMessage):
        self.receivedResponses.append(aConnectedSIPMessage)

