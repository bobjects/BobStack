from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class UDPSIPTwistedProtocol(DatagramProtocol):
    def __init__(self, aUDPSIPTransport):
        self.sipTransport = aUDPSIPTransport

    def bind(self):
        # TODO:  exception handling.  If someone is already listening on our bindPort and bindAddress, this will presumably give a runtime error.
        reactor.listenUDP(self.sipTransport.bindPort, self, interface=self.sipTransport.bindAddress)
        reactor.run()
        self.sipTransport.triggerBound()
        # self.sipTransport.triggerBindFailed()

    def datagramReceived(self, dataString, (host, port)):
        # TODO:  edge cases.
        self.sipTransport.transportConnectionWithAddressAndPort(host, port).receivedString(dataString)

    def sendMessage(self, aSIPMessage):
        self.transport.write(aSIPMessage.rawString, (self.remoteAddress, self.remotePort))
