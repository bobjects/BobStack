from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class UDPSIPTwistedProtocol(DatagramProtocol):
    def __init__(self, aUDPSIPTransportConnection):
        self.transportConnection = aUDPSIPTransportConnection
        reactor.listenUDP(self.transportConnection.bindPort, self, interface=self.transportConnection.bindAddress)
        reactor.run()

    def datagramReceived(self, dataString, (host, port)):
        self.transportConnection.receivedString(dataString)

    def sendMessage(self, aSIPMessage):
        self.transport.write(aSIPMessage.rawString, (self.remoteAddress, self.remotePort))
