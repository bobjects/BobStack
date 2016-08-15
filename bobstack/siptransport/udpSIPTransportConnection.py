from sipTransportConnection import SIPTransportConnection


class UDPSIPTransportConnection(SIPTransportConnection):
    @property
    def isReliable(self):
        return False

    @property
    def isStateful(self):
        return False

    def sendMessage(self, aSIPMessage):
        # TODO
        pass

