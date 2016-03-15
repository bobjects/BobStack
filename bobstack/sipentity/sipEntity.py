

class SIPEntity(object):
    def __init__(self):
        self.homeDomain = None
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
        for t in oldTransports:
            self.unSubscribeFromTransportEvents(t)

    def subscribeToTransportEvents(self, aSIPTransport):
        aSIPTransport.whenEventDo('receivedValidConnectedRequest', self.receivedValidConnectedRequest)
        aSIPTransport.whenEventDo('receivedValidConnectedResponse', self.receivedValidConnectedResponse)
        aSIPTransport.whenEventDo('madeConnection', self.madeConnection)
        aSIPTransport.whenEventDo('lostConnection', self.lostConnection)

    def unSubscribeFromTransportEvents(self, aSIPTransport):
        aSIPTransport.whenEventDoNot('receivedValidConnectedRequest', self.receivedValidConnectedRequest)
        aSIPTransport.whenEventDoNot('receivedValidConnectedResponse', self.receivedValidConnectedResponse)
        aSIPTransport.whenEventDoNot('madeConnection', self.madeConnection)
        aSIPTransport.whenEventDoNot('lostConnection', self.lostConnection)

    def madeConnection(self, aSIPTransportConnection):
        pass

    def lostConnection(self, aSIPTransportConnction):
        pass

    def receivedValidConnectedRequest(self, aConnectedSIPMessage):
        pass

    def receivedValidConnectedResponse(self, aConnectedSIPMessage):
        pass

