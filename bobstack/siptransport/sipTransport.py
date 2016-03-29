import inspect
from eventSourceMixin import EventSourceMixin
from sipTransportConnection import SIPTransportConnection


class SIPTransport(EventSourceMixin):
    def __init__(self, bindAddress, bindPort):
        EventSourceMixin.__init__(self)
        self.bindAddress = bindAddress
        self.bindPort = bindPort
        self.connections = []

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

    def subscribeToTransportConnectionEvents(self, aSIPTransportConnection):
        aSIPTransportConnection.whenEventDo('receivedValidConnectedRequest', self.receivedValidConnectedRequest)
        aSIPTransportConnection.whenEventDo('receivedValidConnectedResponse', self.receivedValidConnectedResponse)
        aSIPTransportConnection.whenEventDo('madeConnection', self.madeConnection)
        aSIPTransportConnection.whenEventDo('lostConnection', self.lostConnection)

    def unSubscribeFromTransportConnectionEvents(self, aSIPTransportConnection):
        aSIPTransportConnection.whenEventDoNot('receivedValidConnectedRequest', self.receivedValidConnectedRequest)
        aSIPTransportConnection.whenEventDoNot('receivedValidConnectedResponse', self.receivedValidConnectedResponse)
        aSIPTransportConnection.whenEventDoNot('madeConnection', self.madeConnection)
        aSIPTransportConnection.whenEventDoNot('lostConnection', self.lostConnection)

    def madeConnection(self, aSIPTransportConnection):
        pass

    def lostConnection(self, aSIPTransportConnction):
        pass

    def receivedValidConnectedRequest(self, aConnectedSIPMessage):
        pass

    def receivedValidConnectedResponse(self, aConnectedSIPMessage):
        pass

    def triggerBound(self):
        print "bound event"
        self.triggerEvent("bound")

    def triggerBindFailed(self):
        print "bindFailed event"
        self.triggerEvent("bindFailed")

    def triggerMadeConnection(self, aSIPTransportConnection):
        print "madeConnection event - " + str(aSIPTransportConnection)
        self.triggerEvent("madeConnection", aSIPTransportConnection)

    def triggerCouldNotMakeConnection(self, addressString, portInteger):
        print "couldNotMakeConnection event - " + str((addressString, portInteger))
        self.triggerEvent("couldNotMakeConnection", (addressString, portInteger))

    def triggerLostConnection(self, aSIPTransportConnection):
        print "lostConnection event - " + str(aSIPTransportConnection)
        self.triggerEvent("lostConnection", aSIPTransportConnection)

    def triggerReceivedValidConnectedRequest(self, aConnectedSIPMessage):
        print "receivedValidConnectedRequest event - " + str(aConnectedSIPMessage)
        self.triggerEvent("receivedValidConnectedRequest", aConnectedSIPMessage)

    def triggerReceivedValidConnectedResponse(self, aConnectedSIPMessage):
        print "receivedValidConnectedResponse event - " + str(aConnectedSIPMessage)
        self.triggerEvent("receivedValidConnectedResponse", aConnectedSIPMessage)

