from unittest import TestCase
import unittest
import sys
sys.path.append("../..")
from bobstack.sipmessaging import SIPMessageFactory
from bobstack.siptransport import SimulatedSIPTransport
from bobstack.siptransport import SimulatedSIPTransportConnection


class TestSimulatedTransportConnection(TestCase):
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
        self.assertEqual(self.bindAddress3, self.transport3.bindAddress)
        self.assertEqual(self.bindPort3, self.transport3.bindPort)

    def test_01_bind(self):
        self.transport1.bind()
        self.assertTrue(self.hasBound)
        self.assertFalse(self.bindHasFailed)
        self.assertEqual(0, len(self.transport1.connections))
        self.assertEqual(0, len(self.connectedConnections))
        self.transport2.bind()
        self.transport3.bind()

    # TODO
    @unittest.skip("TODO\n")
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

    # TODO
    @unittest.skip("TODO\n")
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

    # TODO
    @unittest.skip("TODO\n")
    def test_04_attemptSecondBind(self):
        self.assertFalse(self.bindHasFailed)
        transport = SimulatedSIPTransport(self.bindAddress1, self.bindPort1)
        transport.whenEventDo("bindFailed", self.bindFailedEventHandler)
        transport.bind()
        self.assertTrue(self.bindHasFailed)

    # TODO
    @unittest.skip("TODO\n")
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

    # TODO
    @unittest.skip("TODO\n")
    def test_06_attemptConnectToOwnAddressAndPort(self):
        self.assertEqual(2, len(self.notConnectedAddressesAndPorts))
        self.assertEqual(2, len(self.transport1.connections))
        self.transport1.connectToAddressAndPort(self.bindAddress1, self.bindPort1)
        self.assertEqual(3, len(self.notConnectedAddressesAndPorts))
        self.assertEqual(2, len(self.transport1.connections))
        self.assertEqual((self.bindAddress1, self.bindPort1), self.notConnectedAddressesAndPorts[2])

    # TODO
    @unittest.skip("TODO\n")
    def test_07_sendRequestsVerifyReceipt(self):
        self.assertTrue(self.sampleRequest.isRequest)
        self.assertTrue(self.sampleRequest2.isRequest)
        self.assertEqual(0, len(self.receivedRequests))
        self.assertEqual(0, len(self.receivedResponses))
        self.transport2.connections[0].sendMessage(self.sampleRequest)
        self.assertEqual(1, len(self.receivedRequests))
        self.assertEqual(0, len(self.receivedResponses))
        self.assertIs(self.sampleRequest.__class__, self.receivedRequests[0].__class__)
        self.assertEqual(self.sampleRequest.rawString, self.receivedRequests[0].rawString)
        self.transport3.connections[0].sendMessage(self.sampleRequest2)
        self.assertEqual(2, len(self.receivedRequests))
        self.assertEqual(0, len(self.receivedResponses))
        self.assertIs(self.sampleRequest2.__class__, self.receivedRequests[1].__class__)
        self.assertEqual(self.sampleRequest2.rawString, self.receivedRequests[1].rawString)

    # TODO
    @unittest.skip("TODO\n")
    def test_08_sendResponsesVerifyReceipt(self):
        self.assertTrue(self.sampleResponse.isResponse)
        self.assertTrue(self.sampleResponse2.isResponse)
        self.assertEqual(2, len(self.receivedRequests))
        self.assertEqual(0, len(self.receivedResponses))
        self.transport2.connections[0].sendMessage(self.sampleResponse)
        self.assertEqual(2, len(self.receivedRequests))
        self.assertEqual(1, len(self.receivedResponses))
        self.assertIs(self.sampleResponse.__class__, self.receivedResponses[0].__class__)
        self.assertEqual(self.sampleResponse.rawString, self.receivedResponses[0].rawString)
        self.transport3.connections[0].sendMessage(self.sampleResponse2)
        self.assertEqual(2, len(self.receivedRequests))
        self.assertEqual(2, len(self.receivedResponses))
        self.assertIs(self.sampleResponse2.__class__, self.receivedResponses[1].__class__)
        self.assertEqual(self.sampleResponse2.rawString, self.receivedResponses[1].rawString)

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

    @property
    def sampleRequest(self):
        messageString = ('INVITE sip:3122221000@example.com:5061;user=phone;transport=TLS SIP/2.0\r\n'
                         'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                         'To: <sip:example.com:5061>\r\n'
                         'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                         'CSeq: 6711 SIPMETHODTOREPLACE\r\n'
                         'Max-Forwards: 70\r\n'
                         'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                         'Via: SIP/2.0/TLS 200.25.3.250;branch=z9hG4bKfdkajhdiruyalkghjladksjf\r\n'
                         'Via: SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf\r\n'
                         'User-Agent: Example User Agent\r\n'
                         'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                         'Route: <sip:200.25.3.230:5061;transport=tls;lr>\r\n'
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
                         'Session-Expires: 1200\r\n'
                         'Supported: 100rel,histinfo,join,replaces,sdp-anat,timer\r\n'
                         'Timestamp: 1392061773\r\n'
                         'WWW-Authenticate: Digest algorithm=MD5,nonce="1111790769596",realm="SomeRealm"\r\n'
                         'Warning: 370 200.21.3.10 "Insufficient Bandwidth"\r\n'
                         'X-RTP-Stat:  PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048\r\n'
                         'x-channel:  ds/ds1-3/12;IP=132.52.127.16\r\n'
                         'Referred-By: <sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"\r\n'
                         'Refer-To: <sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>\r\n'
                         'Content-Length: 0')
        return SIPMessageFactory().nextForString(messageString)

    @property
    def sampleRequest2(self):
        messageString = ('BYE sip:3122221000@example.com:5061;user=phone;transport=TLS SIP/2.0\r\n'
                         'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                         'To: <sip:example.com:5061>\r\n'
                         'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                         'CSeq: 6711 SIPMETHODTOREPLACE\r\n'
                         'Max-Forwards: 70\r\n'
                         'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                         'Via: SIP/2.0/TLS 200.25.3.250;branch=z9hG4bKfdkajhdiruyalkghjladksjf\r\n'
                         'Via: SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf\r\n'
                         'User-Agent: Example User Agent\r\n'
                         'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                         'Route: <sip:200.25.3.230:5061;transport=tls;lr>\r\n'
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
                         'Session-Expires: 1200\r\n'
                         'Supported: 100rel,histinfo,join,replaces,sdp-anat,timer\r\n'
                         'Timestamp: 1392061773\r\n'
                         'WWW-Authenticate: Digest algorithm=MD5,nonce="1111790769596",realm="SomeRealm"\r\n'
                         'Warning: 370 200.21.3.10 "Insufficient Bandwidth"\r\n'
                         'X-RTP-Stat:  PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048\r\n'
                         'x-channel:  ds/ds1-3/12;IP=132.52.127.16\r\n'
                         'Referred-By: <sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"\r\n'
                         'Refer-To: <sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>\r\n'
                         'Content-Length: 0')
        return SIPMessageFactory().nextForString(messageString)

    @property
    def sampleResponse(self):
        messageString = ('SIP/2.0 200 OK\r\n'
                         'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                         'To: <sip:example.com:5061>\r\n'
                         'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                         'CSeq: 6711 SIPMETHODTOREPLACE\r\n'
                         'Max-Forwards: 70\r\n'
                         'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                         'Via: SIP/2.0/TLS 200.25.3.250;branch=z9hG4bKfdkajhdiruyalkghjladksjf\r\n'
                         'Via: SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf\r\n'
                         'User-Agent: Example User Agent\r\n'
                         'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                         'Route: <sip:200.25.3.230:5061;transport=tls;lr>\r\n'
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
                         'Session-Expires: 1200\r\n'
                         'Supported: 100rel,histinfo,join,replaces,sdp-anat,timer\r\n'
                         'Timestamp: 1392061773\r\n'
                         'WWW-Authenticate: Digest algorithm=MD5,nonce="1111790769596",realm="SomeRealm"\r\n'
                         'Warning: 370 200.21.3.10 "Insufficient Bandwidth"\r\n'
                         'X-RTP-Stat:  PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048\r\n'
                         'x-channel:  ds/ds1-3/12;IP=132.52.127.16\r\n'
                         'Referred-By: <sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"\r\n'
                         'Refer-To: <sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>\r\n'
                         'Content-Length: 0')
        return SIPMessageFactory().nextForString(messageString)

    @property
    def sampleResponse2(self):
        messageString = ('SIP/2.0 180 Ringing\r\n'
                         'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                         'To: <sip:example.com:5061>\r\n'
                         'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                         'CSeq: 6711 SIPMETHODTOREPLACE\r\n'
                         'Max-Forwards: 70\r\n'
                         'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                         'Via: SIP/2.0/TLS 200.25.3.250;branch=z9hG4bKfdkajhdiruyalkghjladksjf\r\n'
                         'Via: SIP/2.0/TLS 200.25.3.255;branch=z9hG4bKduyroiuryaludhgviukfhlasf\r\n'
                         'User-Agent: Example User Agent\r\n'
                         'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                         'Route: <sip:200.25.3.230:5061;transport=tls;lr>\r\n'
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
                         'Session-Expires: 1200\r\n'
                         'Supported: 100rel,histinfo,join,replaces,sdp-anat,timer\r\n'
                         'Timestamp: 1392061773\r\n'
                         'WWW-Authenticate: Digest algorithm=MD5,nonce="1111790769596",realm="SomeRealm"\r\n'
                         'Warning: 370 200.21.3.10 "Insufficient Bandwidth"\r\n'
                         'X-RTP-Stat:  PR=0;ER=0;PL=0;RB=0/0;DE=PCMU;EN=PCMU;JI=0;DL=0,0;IP=10.1.0.33:16384,132.52.127.200:20048\r\n'
                         'x-channel:  ds/ds1-3/12;IP=132.52.127.16\r\n'
                         'Referred-By: <sip:6006665100@example.com;user=phone> ; CorrelationID="0508817f84e7ce64745ef9753e2fbff4664321a4@200.23.3.240"\r\n'
                         'Refer-To: <sip:6006665499;rfrid=28661859@example.com;user=phone?x-nt-resource-priority=YNBvf.2j00qao>\r\n'
                         'Content-Length: 0')
        return SIPMessageFactory().nextForString(messageString)

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

