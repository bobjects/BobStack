from unittest import TestCase
import sys
sys.path.append("../..")
from bobstack.sipmessaging import SIPMessageFactory
from bobstack.siptransport import SimulatedSIPTransport
from bobstack.siptransport import SimulatedSIPTransportConnection
from bobstack.siptransport import SimulatedNetwork
from abstractTransportConnectionTestCase import AbstractTransportConnectionTestCase


class TestSimulatedTransportConnection(AbstractTransportConnectionTestCase):
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
        self.assertIsInstance(self.transport1.connections[0].bindPort, int)
        self.assertIsInstance(self.transport1.connections[0].id, basestring)
        self.assertEqual(self.bindPort2, self.transport1.connections[0].remotePort)
        self.assertEqual(1, len(self.transport2.connections))
        self.assertEqual(0, len(self.transport3.connections))
        self.assertEqual(self.bindAddress1, self.transport2.connections[0].remoteAddress)
        self.assertIsInstance(self.transport2.connections[0].remotePort, int)
        self.assertIsInstance(self.transport2.connections[0].id, basestring)
        self.assertEqual(self.bindPort2, self.transport2.connections[0].bindPort)

    def run_03_makeInboundConnection(self):
        # Connect transport3 to transport1
        self.transport3.connectToAddressAndPort(self.bindAddress1, self.bindPort1)
        self.assertEqual(2, len(self.transport1.connections))
        self.assertEqual(1, len(self.transport2.connections))
        self.assertEqual(1, len(self.transport3.connections))
        self.assertEqual(2, len(self.connectedConnections))
        self.assertIs(self.connectedConnections[1], self.transport1.connections[1])
        self.assertEqual(self.bindAddress3, self.transport1.connections[1].remoteAddress)
        self.assertIsInstance(self.transport3.connections[0].bindPort, int)
        self.assertIsInstance(self.transport3.connections[0].id, basestring)
        self.assertEqual(self.bindPort1, self.transport1.connections[0].bindPort)
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

    def madeConnectionEventHandler(self, aSimulatedSIPTransportConnection):
        self.connectedConnections.append(aSimulatedSIPTransportConnection)

    def couldNotMakeConnectionEventHandler(self, bindAddressAndPort):
        addressAndPort = bindAddressAndPort
        self.notConnectedAddressesAndPorts.append(addressAndPort)

    def lostConnectionEventHandler(self, aSimulatedSIPTransportConnection):
        if aSimulatedSIPTransportConnection in self.connectedConnections:
            self.connectedConnections.remove(aSimulatedSIPTransportConnection)

    def receivedValidConnectedRequestEventHandler(self, aConnectedSIPMessage):
        print "receivedValidConnectedRequestEventHandler"
        self.receivedRequests.append(aConnectedSIPMessage)

    def receivedValidConnectedResponseEventHandler(self, aConnectedSIPMessage):
        print "receivedValidConnectedResponseEventHandler"
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
                         'Subject: Need more boxes\r\n'
                         'Referred-By: <sip:5556785103@example.com;user=phone> ; CorrelationID="348058f0947acec8745efd367e33542c5cb01436@192.168.0.3"\r\n'
                         'Refer-To: <sip:5556645204@example.com:5064;user=phone;transport=udp>\r\n'
                         'Allow-Events: dialog,message-summary\r\n'
                         'Event: refer;id=10498\r\n'
                         'Content-Encoding: gzip\r\n'
                         'RAck: 1 1 INVITE\r\n'
                         'P-Charge: <sip:6425555555@10.10.10.10>;npi=ISDN;noa=2\r\n'
                         'Reply-To: Bob <sip:bob@biloxi.com>\r\n'
                         'Unsupported: foo\r\n'
                         'P-Asserted-Identity: "500 - SIP Test" <sip:500@192.168.0.3>\r\n'
                         'P-Preferred-Identity: "User 5103" <sip:3126705103@192.168.0.3:5060>\r\n'
                         'Remote-Party-ID: "1234567890" <sip:1234567890@192.168.1.195>;party=calling;privacy=off;screen=no\r\n'
                         'Alert-Info: <cid:internal@example.com>;alert-type=internal\r\n'
                         'History-Info: "555122221002" <sip:555122221002@example.com>;index=1.1\r\n'
                         'P-Called-Party-Id: <sip:2135881@example.com;user=phone>\r\n'
                         'P-RTP-Stat: PS=0,OS=0,PR=5429,OR=955504,PL=0,JI=0,LA=0,DU=108\r\n'
                         'Privacy: id\r\n'
                         'Proxy-Authenticate: Digest realm="1.1.1.1", nonce="8dd33eb2-e3c4-11e5-a55b-83b175043a03", algorithm=MD5, qop="auth"\r\n'
                         'Proxy-Authorization: Digest username="100",realm="209.105.255.124",nonce="7bebcf02-e01d-11e5-931d-83b175043a03",uri="sip:90011@209.105.255.124",response="63faaa2604cae36e9b38f2d5cd0abba4",cnonce="4b41f53e6f00c05",nc=00000001,qop="auth",algorithm=MD5\r\n'
                         'Proxy-Require: foo\r\n'
                         'Reason: Q.850; cause=16; reason=Terminated\r\n'
                         'Record-Session-Expires: 1200;refresher=uac\r\n'
                         'Replaces: 19cd9bf094ff5f0c1745ef975c1cf65d34beb908f@192.168.0.3;to-tag=29bd570-f0a1ec8-13c5-50029-aa872-7d78286-aa872;from-tag=7ca31b4791\r\n'
                         'Subscription-State: active;reason=deactivated;expires=50\r\n'
                         'Min-Expires: 1800\r\n'
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
                         'Subject: Need more boxes\r\n'
                         'Referred-By: <sip:5556785103@example.com;user=phone> ; CorrelationID="348058f0947acec8745efd367e33542c5cb01436@192.168.0.3"\r\n'
                         'Refer-To: <sip:5556645204@example.com:5064;user=phone;transport=udp>\r\n'
                         'Allow-Events: dialog,message-summary\r\n'
                         'Event: refer;id=10498\r\n'
                         'Content-Encoding: gzip\r\n'
                         'RAck: 1 1 INVITE\r\n'
                         'P-Charge: <sip:6425555555@10.10.10.10>;npi=ISDN;noa=2\r\n'
                         'Reply-To: Bob <sip:bob@biloxi.com>\r\n'
                         'Unsupported: foo\r\n'
                         'P-Asserted-Identity: "500 - SIP Test" <sip:500@192.168.0.3>\r\n'
                         'P-Preferred-Identity: "User 5103" <sip:3126705103@192.168.0.3:5060>\r\n'
                         'Remote-Party-ID: "1234567890" <sip:1234567890@192.168.1.195>;party=calling;privacy=off;screen=no\r\n'
                         'Alert-Info: <cid:internal@example.com>;alert-type=internal\r\n'
                         'History-Info: "555122221002" <sip:555122221002@example.com>;index=1.1\r\n'
                         'P-Called-Party-Id: <sip:2135881@example.com;user=phone>\r\n'
                         'P-RTP-Stat: PS=0,OS=0,PR=5429,OR=955504,PL=0,JI=0,LA=0,DU=108\r\n'
                         'Privacy: id\r\n'
                         'Proxy-Authenticate: Digest realm="1.1.1.1", nonce="8dd33eb2-e3c4-11e5-a55b-83b175043a03", algorithm=MD5, qop="auth"\r\n'
                         'Proxy-Authorization: Digest username="100",realm="209.105.255.124",nonce="7bebcf02-e01d-11e5-931d-83b175043a03",uri="sip:90011@209.105.255.124",response="63faaa2604cae36e9b38f2d5cd0abba4",cnonce="4b41f53e6f00c05",nc=00000001,qop="auth",algorithm=MD5\r\n'
                         'Proxy-Require: foo\r\n'
                         'Reason: Q.850; cause=16; reason=Terminated\r\n'
                         'Record-Session-Expires: 1200;refresher=uac\r\n'
                         'Replaces: 19cd9bf094ff5f0c1745ef975c1cf65d34beb908f@192.168.0.3;to-tag=29bd570-f0a1ec8-13c5-50029-aa872-7d78286-aa872;from-tag=7ca31b4791\r\n'
                         'Subscription-State: active;reason=deactivated;expires=50\r\n'
                         'Min-Expires: 1800\r\n'
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
                         'Subject: Need more boxes\r\n'
                         'Referred-By: <sip:5556785103@example.com;user=phone> ; CorrelationID="348058f0947acec8745efd367e33542c5cb01436@192.168.0.3"\r\n'
                         'Refer-To: <sip:5556645204@example.com:5064;user=phone;transport=udp>\r\n'
                         'Allow-Events: dialog,message-summary\r\n'
                         'Event: refer;id=10498\r\n'
                         'Content-Encoding: gzip\r\n'
                         'RAck: 1 1 INVITE\r\n'
                         'P-Charge: <sip:6425555555@10.10.10.10>;npi=ISDN;noa=2\r\n'
                         'Reply-To: Bob <sip:bob@biloxi.com>\r\n'
                         'Unsupported: foo\r\n'
                         'P-Asserted-Identity: "500 - SIP Test" <sip:500@192.168.0.3>\r\n'
                         'P-Preferred-Identity: "User 5103" <sip:3126705103@192.168.0.3:5060>\r\n'
                         'Remote-Party-ID: "1234567890" <sip:1234567890@192.168.1.195>;party=calling;privacy=off;screen=no\r\n'
                         'Alert-Info: <cid:internal@example.com>;alert-type=internal\r\n'
                         'History-Info: "555122221002" <sip:555122221002@example.com>;index=1.1\r\n'
                         'P-Called-Party-Id: <sip:2135881@example.com;user=phone>\r\n'
                         'P-RTP-Stat: PS=0,OS=0,PR=5429,OR=955504,PL=0,JI=0,LA=0,DU=108\r\n'
                         'Privacy: id\r\n'
                         'Proxy-Authenticate: Digest realm="1.1.1.1", nonce="8dd33eb2-e3c4-11e5-a55b-83b175043a03", algorithm=MD5, qop="auth"\r\n'
                         'Proxy-Authorization: Digest username="100",realm="209.105.255.124",nonce="7bebcf02-e01d-11e5-931d-83b175043a03",uri="sip:90011@209.105.255.124",response="63faaa2604cae36e9b38f2d5cd0abba4",cnonce="4b41f53e6f00c05",nc=00000001,qop="auth",algorithm=MD5\r\n'
                         'Proxy-Require: foo\r\n'
                         'Reason: Q.850; cause=16; reason=Terminated\r\n'
                         'Record-Session-Expires: 1200;refresher=uac\r\n'
                         'Replaces: 19cd9bf094ff5f0c1745ef975c1cf65d34beb908f@192.168.0.3;to-tag=29bd570-f0a1ec8-13c5-50029-aa872-7d78286-aa872;from-tag=7ca31b4791\r\n'
                         'Subscription-State: active;reason=deactivated;expires=50\r\n'
                         'Min-Expires: 1800\r\n'
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
                         'Subject: Need more boxes\r\n'
                         'Referred-By: <sip:5556785103@example.com;user=phone> ; CorrelationID="348058f0947acec8745efd367e33542c5cb01436@192.168.0.3"\r\n'
                         'Refer-To: <sip:5556645204@example.com:5064;user=phone;transport=udp>\r\n'
                         'Allow-Events: dialog,message-summary\r\n'
                         'Event: refer;id=10498\r\n'
                         'Content-Encoding: gzip\r\n'
                         'RAck: 1 1 INVITE\r\n'
                         'P-Charge: <sip:6425555555@10.10.10.10>;npi=ISDN;noa=2\r\n'
                         'Reply-To: Bob <sip:bob@biloxi.com>\r\n'
                         'Unsupported: foo\r\n'
                         'P-Asserted-Identity: "500 - SIP Test" <sip:500@192.168.0.3>\r\n'
                         'P-Preferred-Identity: "User 5103" <sip:3126705103@192.168.0.3:5060>\r\n'
                         'Remote-Party-ID: "1234567890" <sip:1234567890@192.168.1.195>;party=calling;privacy=off;screen=no\r\n'
                         'Alert-Info: <cid:internal@example.com>;alert-type=internal\r\n'
                         'History-Info: "555122221002" <sip:555122221002@example.com>;index=1.1\r\n'
                         'P-Called-Party-Id: <sip:2135881@example.com;user=phone>\r\n'
                         'P-RTP-Stat: PS=0,OS=0,PR=5429,OR=955504,PL=0,JI=0,LA=0,DU=108\r\n'
                         'Privacy: id\r\n'
                         'Proxy-Authenticate: Digest realm="1.1.1.1", nonce="8dd33eb2-e3c4-11e5-a55b-83b175043a03", algorithm=MD5, qop="auth"\r\n'
                         'Proxy-Authorization: Digest username="100",realm="209.105.255.124",nonce="7bebcf02-e01d-11e5-931d-83b175043a03",uri="sip:90011@209.105.255.124",response="63faaa2604cae36e9b38f2d5cd0abba4",cnonce="4b41f53e6f00c05",nc=00000001,qop="auth",algorithm=MD5\r\n'
                         'Proxy-Require: foo\r\n'
                         'Reason: Q.850; cause=16; reason=Terminated\r\n'
                         'Record-Session-Expires: 1200;refresher=uac\r\n'
                         'Replaces: 19cd9bf094ff5f0c1745ef975c1cf65d34beb908f@192.168.0.3;to-tag=29bd570-f0a1ec8-13c5-50029-aa872-7d78286-aa872;from-tag=7ca31b4791\r\n'
                         'Subscription-State: active;reason=deactivated;expires=50\r\n'
                         'Min-Expires: 1800\r\n'
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


