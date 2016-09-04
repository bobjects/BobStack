from twisted.internet.protocol import DatagramProtocol
# from twisted.internet import reactor
from twistedMultiService import TwistedMultiService

class UDPSIPTwistedProtocol(DatagramProtocol):
    def __init__(self, aUDPSIPTransport):
        # cannot user super - old style class.  Grrr...
        # TODO:  Working on this - What is init protocol for DatagramProtocol?  Look at docs when we get to Internet.
        DatagramProtocol.__init__(self)
        self.sipTransport = aUDPSIPTransport

    def bind(self):
        # TODO:  exception handling.  If someone is already listening on our bindPort and bindAddress, this will presumably give a runtime error.
        # reactor.listenUDP(self.sipTransport.bindPort, self, interface=self.sipTransport.bindAddress)
        # reactor.run()
        TwistedMultiService.instance.registerTwistedUDPProtocol(self, self.sipTransport.bindPort, self.sipTransport.bindAddress)
        self.sipTransport.triggerBound()
        # self.sipTransport.triggerBindFailed()

    def datagramReceived(self, dataString, (host, port)):
        # TODO:  edge cases.
        self.sipTransport.transportConnectionWithAddressAndPort(host, port).receivedString(dataString)

    def sendMessage(self, aSIPMessage):
        self.transport.write(aSIPMessage.rawString, (self.remoteAddress, self.remotePort))
