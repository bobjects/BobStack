

class SIPEntity(object):
    def __init__(self):
        # TODO: still need to test homeDomains.
        self._homeDomains = []
        self._transports = []

    @property
    def homeDomains(self):
        # TODO: Is this correct?  We are deriving domains for each bind address, and letting the user add additional domains.
        return [t.bind_address for t in self.transports] + self._homeDomains

    @property
    def transports(self):
        return self._transports

    @transports.setter
    def transports(self, sip_transports):
        new_transports = [t for t in sip_transports if t not in self._transports]
        old_transports = [t for t in self._transports if t not in sip_transports]
        for t in new_transports:
            self.subscribeToTransportEvents(t)
            t.bind()
            self._transports.append(t)
        for t in old_transports:
            self.unSubscribeFromTransportEvents(t)
            # TODO - will need to un-bind, and also probably break all connections.
            self._transports.remove(t)

    def subscribeToTransportEvents(self, a_sip_transport):
        a_sip_transport.whenEventDo('receivedValidConnectedRequest', self.receivedValidConnectedRequestEventHandler)
        a_sip_transport.whenEventDo('receivedValidConnectedResponse', self.receivedValidConnectedResponseEventHandler)
        a_sip_transport.whenEventDo('bound', self.boundEventHandler)
        a_sip_transport.whenEventDo('bindFailed', self.bindFailedEventHandler)
        a_sip_transport.whenEventDo('madeConnection', self.madeConnectionEventHandler)
        a_sip_transport.whenEventDo('couldNotMakeConnection', self.couldNotMakeConnectionEventHandler)
        a_sip_transport.whenEventDo('lostConnection', self.lostConnectionEventHandler)

    def unSubscribeFromTransportEvents(self, a_sip_transport):
        a_sip_transport.whenEventDoNot('receivedValidConnectedRequest', self.receivedValidConnectedRequestEventHandler)
        a_sip_transport.whenEventDoNot('receivedValidConnectedResponse', self.receivedValidConnectedResponseEventHandler)
        a_sip_transport.whenEventDoNot('bound', self.boundEventHandler)
        a_sip_transport.whenEventDoNot('bindFailed', self.bindFailedEventHandler)
        a_sip_transport.whenEventDoNot('madeConnection', self.madeConnectionEventHandler)
        a_sip_transport.whenEventDoNot('couldNotMakeConnection', self.couldNotMakeConnectionEventHandler)
        a_sip_transport.whenEventDoNot('lostConnection', self.lostConnectionEventHandler)

    def boundEventHandler(self):
        pass

    def bindFailedEventHandler(self):
        pass

    def madeConnectionEventHandler(self, a_sip_transport_connection):
        pass

    def couldNotMakeConnectionEventHandler(self, bind_address_and_port):
        pass

    def lostConnectionEventHandler(self, a_sip_transport_connction):
        pass

    def receivedValidConnectedRequestEventHandler(self, a_connected_aip_message):
        pass

    def receivedValidConnectedResponseEventHandler(self, a_connected_aip_message):
        pass

