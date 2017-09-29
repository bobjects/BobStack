from twisted.internet.protocol import DatagramProtocol
# from twisted.internet import reactor
from twistedMultiService import TwistedMultiService

class UDPSIPTwistedProtocol(DatagramProtocol):
    def __init__(self, a_udp_sip_transport):
        # cannot user super - old style class.  Grrr...
        # TODO:  Working on this - What is init protocol for DatagramProtocol?  Look at docs when we get to Internet.
        DatagramProtocol.__init__(self)
        self.sipTransport = a_udp_sip_transport

    def bind(self):
        # TODO:  exception handling.  If someone is already listening on our bind_port and bind_address, this will presumably give a runtime error.
        # reactor.listenUDP(self.sipTransport.bind_port, self, interface=self.sipTransport.bind_address)
        # reactor.run()
        TwistedMultiService.instance.registerTwistedUDPProtocol(self, self.sipTransport.bind_port, self.sipTransport.bind_address)
        self.sipTransport.triggerBound()
        # self.sipTransport.triggerBindFailed()

    def datagramReceived(self, data_string, (host, port)):
        # TODO:  edge cases.
        self.sipTransport.transportConnectionWithAddressAndPort(host, port).receivedString(data_string)

    def sendMessage(self, a_sip_message):
        self.transport.write(a_sip_message.rawString, (self.remoteAddress, self.remotePort))
