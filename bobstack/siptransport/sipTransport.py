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
    def isStateful(self):
        return True

    @property
    def transportParameterName(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def bind(self):
        pass

    def connectToAddressAndPort(self, addressString, portInteger):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def connectionWithAddressAndPort(self, addressString, portInteger):
        return next((c for c in self.connections if c.remoteAddress == addressString and c.remotePort == portInteger), None)

    def subscribeToTransportConnectionEvents(self, aSIPTransportConnection):
        aSIPTransportConnection.whenEventDo('receivedValidConnectedRequest', self.receivedValidConnectedRequestEventHandler)
        aSIPTransportConnection.whenEventDo('receivedValidConnectedResponse', self.receivedValidConnectedResponseEventHandler)
        aSIPTransportConnection.whenEventDo('madeConnection', self.madeConnectionEventHandler)
        aSIPTransportConnection.whenEventDo('lostConnection', self.lostConnectionEventHandler)

    def unSubscribeFromTransportConnectionEvents(self, aSIPTransportConnection):
        aSIPTransportConnection.whenEventDoNot('receivedValidConnectedRequest', self.receivedValidConnectedRequestEventHandler)
        aSIPTransportConnection.whenEventDoNot('receivedValidConnectedResponse', self.receivedValidConnectedResponseEventHandler)
        aSIPTransportConnection.whenEventDoNot('madeConnection', self.madeConnectionEventHandler)
        aSIPTransportConnection.whenEventDoNot('lostConnection', self.lostConnectionEventHandler)

    def madeConnectionEventHandler(self, aSIPTransportConnection):
        pass

    def lostConnectionEventHandler(self, aSIPTransportConnction):
        pass

    def receivedValidConnectedRequestEventHandler(self, aConnectedSIPMessage):
        print "(transport) receivedValidConnectedRequest event"
        self.triggerEvent("receivedValidConnectedRequest", aConnectedSIPMessage)

    def receivedValidConnectedResponseEventHandler(self, aConnectedSIPMessage):
        print "(transport) receivedValidConnectedResponse event"
        self.triggerEvent("receivedValidConnectedResponse", aConnectedSIPMessage)

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

