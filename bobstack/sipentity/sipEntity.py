

class SIPEntity(object):
    def __init__(self):
        # TODO: still need to test home_domains.
        self._homeDomains = []
        self._transports = []

    @property
    def home_domains(self):
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
            self.subscribe_to_transport_events(t)
            t.bind()
            self._transports.append(t)
        for t in old_transports:
            self.unsubscribe_from_transport_events(t)
            # TODO - will need to un-bind, and also probably break all connections.
            self._transports.remove(t)

    def subscribe_to_transport_events(self, a_sip_transport):
        a_sip_transport.when_event_do('receivedValidConnectedRequest', self.received_valid_connected_request_event_handler)
        a_sip_transport.when_event_do('receivedValidConnectedResponse', self.received_valid_connected_response_event_handler)
        a_sip_transport.when_event_do('bound', self.bound_event_handler)
        a_sip_transport.when_event_do('bindFailed', self.bind_failed_event_handler)
        a_sip_transport.when_event_do('madeConnection', self.made_connection_event_handler)
        a_sip_transport.when_event_do('couldNotMakeConnection', self.could_not_make_connection_event_handler)
        a_sip_transport.when_event_do('lostConnection', self.lost_connection_event_handler)

    def unsubscribe_from_transport_events(self, a_sip_transport):
        a_sip_transport.when_event_do_not('receivedValidConnectedRequest', self.received_valid_connected_request_event_handler)
        a_sip_transport.when_event_do_not('receivedValidConnectedResponse', self.received_valid_connected_response_event_handler)
        a_sip_transport.when_event_do_not('bound', self.bound_event_handler)
        a_sip_transport.when_event_do_not('bindFailed', self.bind_failed_event_handler)
        a_sip_transport.when_event_do_not('madeConnection', self.made_connection_event_handler)
        a_sip_transport.when_event_do_not('couldNotMakeConnection', self.could_not_make_connection_event_handler)
        a_sip_transport.when_event_do_not('lostConnection', self.lost_connection_event_handler)

    def bound_event_handler(self):
        pass

    def bind_failed_event_handler(self):
        pass

    def made_connection_event_handler(self, a_sip_transport_connection):
        pass

    def could_not_make_connection_event_handler(self, bind_address_and_port):
        pass

    def lost_connection_event_handler(self, a_sip_transport_connction):
        pass

    def received_valid_connected_request_event_handler(self, a_connected_aip_message):
        pass

    def received_valid_connected_response_event_handler(self, a_connected_aip_message):
        pass

