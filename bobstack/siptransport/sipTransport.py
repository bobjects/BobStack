import inspect
from eventSourceMixin import EventSourceMixin


class SIPTransport(EventSourceMixin):
    def __init__(self, bindAddress, bindPort):
        EventSourceMixin.__init__(self)
        self.bindAddress = bindAddress
        self.bindPort = bindPort
        self.bind()

    @property
    def isReliable(self):
        return True

    @property
    def transportParameterName(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def bind(self):
        pass

    def connectToAddressAndPort(self, addressString, portInteger):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def triggerBound(self):
        self.triggerEvent("bound")

    def triggerMadeConnection(self, aSIPTransportConnection):
        self.triggerEvent("madeConnection", aSIPTransportConnection)

    def triggerLostConnection(self, aSIPTransportConnection):
        self.triggerEvent("lostConnection", aSIPTransportConnection)

    def triggerReceivedValidConnectedRequest(self, aConnectedSIPMessage):
        self.triggerEvent("receivedValidConnectedRequest", aConnectedSIPMessage)

    def triggerReceivedValidConnectedResponse(self, aConnectedSIPMessage):
        self.triggerEvent("receivedValidConnectedResponse", aConnectedSIPMessage)

