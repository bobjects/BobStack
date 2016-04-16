

class SIPEntity(object):
    def __init__(self):
        # TODO: still need to test homeDomains.
        self.homeDomains = []
        self._transports = []

    @property
    def transports(self):
        return self._transports

    @transports.setter
    def transports(self, sipTransports):
        newTransports = [t for t in sipTransports if t not in self._transports]
        oldTransports = [t for t in self._transports if t not in sipTransports]
        for t in newTransports:
            self.subscribeToTransportEvents(t)
            t.bind()
            self._transports.append(t)
        for t in oldTransports:
            self.unSubscribeFromTransportEvents(t)
            # TODO - will need to un-bind, and also probably break all connections.
            self._transports.remove(t)

    def subscribeToTransportEvents(self, aSIPTransport):
        aSIPTransport.whenEventDo('receivedValidConnectedRequest', self.receivedValidConnectedRequestEventHandler)
        aSIPTransport.whenEventDo('receivedValidConnectedResponse', self.receivedValidConnectedResponseEventHandler)
        aSIPTransport.whenEventDo('bound', self.boundEventHandler)
        aSIPTransport.whenEventDo('bindFailed', self.bindFailedEventHandler)
        aSIPTransport.whenEventDo('madeConnection', self.madeConnectionEventHandler)
        aSIPTransport.whenEventDo('couldNotMakeConnection', self.couldNotMakeConnectionEventHandler)
        aSIPTransport.whenEventDo('lostConnection', self.lostConnectionEventHandler)

    def unSubscribeFromTransportEvents(self, aSIPTransport):
        aSIPTransport.whenEventDoNot('receivedValidConnectedRequest', self.receivedValidConnectedRequestEventHandler)
        aSIPTransport.whenEventDoNot('receivedValidConnectedResponse', self.receivedValidConnectedResponseEventHandler)
        aSIPTransport.whenEventDoNot('bound', self.boundEventHandler)
        aSIPTransport.whenEventDoNot('bindFailed', self.bindFailedEventHandler)
        aSIPTransport.whenEventDoNot('madeConnection', self.madeConnectionEventHandler)
        aSIPTransport.whenEventDoNot('couldNotMakeConnection', self.couldNotMakeConnectionEventHandler)
        aSIPTransport.whenEventDoNot('lostConnection', self.lostConnectionEventHandler)

    def boundEventHandler(self):
        pass

    def bindFailedEventHandler(self):
        pass

    def madeConnectionEventHandler(self, aSIPTransportConnection):
        pass

    def couldNotMakeConnectionEventHandler(self, bindAddressAndPort):
        pass

    def lostConnectionEventHandler(self, aSIPTransportConnction):
        pass

    def receivedValidConnectedRequestEventHandler(self, aConnectedSIPMessage):
        pass

    def receivedValidConnectedResponseEventHandler(self, aConnectedSIPMessage):
        pass

