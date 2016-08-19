from sipTransportConnection import SIPTransportConnection
from udpSIPTwistedProtocol import UDPSIPTwistedProtocol


class UDPSIPTransportConnection(SIPTransportConnection):
    def __init__(self, bindAddressString, remoteAddressString, bindPortInteger, remotePortInteger):
        super(UDPSIPTransportConnection, self).__init__(bindAddressString, remoteAddressString, bindPortInteger, remotePortInteger)
        self.twistedProtocol = UDPSIPTransportConnection(self)

    @property
    def isReliable(self):
        return False

    @property
    def isStateful(self):
        return False

    def sendMessage(self, aSIPMessage):
        self.twistedProtocol.sendMessage(aSIPMessage)
