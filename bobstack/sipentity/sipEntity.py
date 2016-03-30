

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
        aSIPTransport.whenEventDo('receivedValidConnectedRequest', self.receivedValidConnectedRequestEventHandler)
        aSIPTransport.whenEventDo('receivedValidConnectedResponse', self.receivedValidConnectedResponseEventHandler)
        aSIPTransport.whenEventDo('madeConnection', self.madeConnectionEventHandler)
        aSIPTransport.whenEventDo('lostConnection', self.lostConnectionEventHandler)

    def unSubscribeFromTransportEvents(self, aSIPTransport):
        aSIPTransport.whenEventDoNot('receivedValidConnectedRequest', self.receivedValidConnectedRequestEventHandler)
        aSIPTransport.whenEventDoNot('receivedValidConnectedResponse', self.receivedValidConnectedResponseEventHandler)
        aSIPTransport.whenEventDoNot('madeConnection', self.madeConnectionEventHandler)
        aSIPTransport.whenEventDoNot('lostConnection', self.lostConnectionEventHandler)

    def madeConnectionEventHandler(self, aSIPTransportConnection):
        pass

    def lostConnectionEventHandler(self, aSIPTransportConnction):
        pass

    def receivedValidConnectedRequestEventHandler(self, aConnectedSIPMessage):
        pass

    def receivedValidConnectedResponseEventHandler(self, aConnectedSIPMessage):
        pass

