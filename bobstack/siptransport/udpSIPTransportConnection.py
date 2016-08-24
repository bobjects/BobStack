from sipTransportConnection import SIPTransportConnection


class UDPSIPTransportConnection(SIPTransportConnection):
    def __init__(self, bindAddressString, remoteAddressString, bindPortInteger, remotePortInteger):
        self.twistedProtocol = None
        super(UDPSIPTransportConnection, self).__init__(bindAddressString, remoteAddressString, bindPortInteger, remotePortInteger)

    @property
    def isReliable(self):
        return False

    @property
    def isStateful(self):
        return False

    def sendMessage(self, aSIPMessage):
        self.twistedProtocol.sendMessage(aSIPMessage)
