from unittest import TestCase
import unittest
import sys
sys.path.append("../..")
from bobstack.siptransport import SimulatedSIPTransport
from bobstack.siptransport import SimulatedSIPTransportConnection

class TestSimulatedTransportConnection(TestCase):
    @property
    def bindAddress1(self):
        return '192.168.4.2'

    @property
    def bindPort1(self):
        return 5060

    @property
    def bindAddress2(self):
        return '192.168.4.3'

    @property
    def bindPort2(self):
        return 5062

    @property
    def bindAddress3(self):
        return '192.168.4.4'

    @property
    def bindPort3(self):
        return 5063

    # @property
    # def outboundConnectionAddress(self):
    #     return '192.168.4.4'
    #
    # @property
    # def outboundConnectionPort(self):
    #     return 5063
    #
    # @property
    # def inboundConnectionAddress(self):
    #     return '192.168.4.5'
    #
    # @property
    # def inboundConnectionPort(self):
    #     return 5064

    # TODO - should verify failure of binding to address/port that's already bound to.

    def setUp(self):
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


    # order of test execution matters, so use integers for specifying test execution order.

    def test_00_initialSanityCheck(self):
        self.assertIsInstance(self.transport1, SimulatedSIPTransport)
        self.assertEqual(0, len(self.transport1.connections))
        self.assertEqual(0, len(self.connectedConnections))
        self.assertEqual(0, len(self.receivedRequests))
        self.assertEqual(0, len(self.receivedResponses))
        self.assertTrue(self.transport1.isReliable)
        self.assertEqual('SIM', self.transport1.transportParameterName)
        self.assertEqual(self.bindAddress1, self.transport1.bindAddress)
        self.assertEqual(self.bindPort1, self.transport1.bindPort)
        self.assertFalse(self.hasBound)
        self.assertFalse(self.bindHasFailed)
        self.assertIsInstance(self.transport2, SimulatedSIPTransport)
        self.assertEqual(0, len(self.transport2.connections))
        self.assertTrue(self.transport2.isReliable)
        self.assertEqual('SIM', self.transport2.transportParameterName)
        self.assertEqual(self.bindAddress2, self.transport2.bindAddress)
        self.assertEqual(self.bindPort2, self.transport2.bindPort)
        self.assertIsInstance(self.transport3, SimulatedSIPTransport)
        self.assertEqual(0, len(self.transport3.connections))
        self.assertTrue(self.transport3.isReliable)
        self.assertEqual('SIM', self.transport3.transportParameterName)
        self.assertEqual(self.bindAddress2, self.transport3.bindAddress)
        self.assertEqual(self.bindPort2, self.transport3.bindPort)

    def test_01_bind(self):
        self.transport1.bind()
        self.assertTrue(self.hasBound)
        self.assertFalse(self.bindHasFailed)
        self.assertEqual(0, len(self.transport1.connections))
        self.assertEqual(0, len(self.connectedConnections))
        self.transport2.bind()
        self.transport3.bind()

    def test_02_makeOutboundConnection(self):
        # Connect transport1 to transport2
        self.transport1.connectToAddressAndPort(self.bindAddress2, self.bindPort2)
        self.assertEqual(1, len(self.transport1.connections))
        self.assertEqual(1, len(self.transport2.connections))
        self.assertEqual(0, len(self.transport2.connections))
        self.assertEqual(1, len(self.connectedConnections))
        self.assertIs(self.connectedConnections[0], self.transport1.connections[0])
        self.assertEqual(self.bindAddress2, self.transport1.connections[0].address)
        self.assertIsInstance(self.transport1.connections[0].localPort, int)
        self.assertEqual(self.bindPort2, self.transport1.connections[0].remotePort)
        self.assertEqual(self.bindAddress1, self.transport2.connections[0].address)
        self.assertIsInstance(self.transport2.connections[0].remotePort, int)
        self.assertEqual(self.bindPort2, self.transport2.connections[0].localPort)

    def test_03_makeInboundConnection(self):
        # Connect transport3 to transport1
        self.transport3.connectToAddressAndPort(self.bindAddress1, self.bindPort1)
        self.assertEqual(2, len(self.transport1.connections))
        self.assertEqual(1, len(self.transport2.connections))
        self.assertEqual(1, len(self.transport3.connections))
        self.assertEqual(2, len(self.connectedConnections))
        self.assertIs(self.connectedConnections[1], self.transport3.connections[0])
        self.assertEqual(self.bindAddress3, self.transport1.connections[1].address)
        self.assertIsInstance(self.transport3.connections[0].localPort, int)
        self.assertEqual(self.bindPort1, self.transport1.connections[0].localPort)
        self.assertEqual(self.bindAddress1, self.transport3.connections[0].address)
        self.assertIsInstance(self.transport1.connections[0].remotePort, int)
        self.assertEqual(self.bindPort1, self.transport3.connections[0].remotePort)

    def test_04_attemptSecondBind(self):
        self.assertFalse(self.bindHasFailed)
        transport = SimulatedSIPTransport(self.bindAddress1, self.bindPort1)
        transport.whenEventDo("bindFailed", self.bindFailedEventHandler)
        transport.bind()
        self.assertTrue(self.bindHasFailed)

    def test_05_attemptConnectToBogusAddressAndPort(self):
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

    def test_05_attemptConnectToOwnAddressAndPort(self):
        self.assertEqual(2, len(self.notConnectedAddressesAndPorts))
        self.assertEqual(2, len(self.transport1.connections))
        self.transport1.connectToAddressAndPort(self.bindAddress1, self.bindPort1)
        self.assertEqual(3, len(self.notConnectedAddressesAndPorts))
        self.assertEqual(2, len(self.transport1.connections))
        self.assertEqual((self.bindAddress1, self.bindAddress1), self.notConnectedAddressesAndPorts[2])

    # TODO:  next - send, receive messages, verify receipt.

    def boundEventHandler(self):
        self.hasBound = True

    def bindFailedEventHandler(self):
        self.bindHasFailed = True

    def madeConnectionEventHandler(self, aSimulatedSIPTransportConnection):
        self.connectedConnections.append(aSimulatedSIPTransportConnection)

    def couldNotMakeConnectionEventHandler(self, bindAddressAndPort):
        addressAndPort = bindAddressAndPort
        self.notConnectedAddressesAndPorts.append(addressAndPort)

    def lostConnectionEventHandler(self, aSimulatedSIPTransportConnection):
        if aSimulatedSIPTransportConnection in self.connectedConnections:
            self.connectedConnections.remove(aSimulatedSIPTransportConnection)

    def receivedValidConnectedRequestEventHandler(self, aConnectedSIPMessage):
        self.receivedRequests.append(aConnectedSIPMessage)

    def receivedValidConnectedResponseEventHandler(self, aConnectedSIPMessage):
        self.receivedResponses.append(aConnectedSIPMessage)

