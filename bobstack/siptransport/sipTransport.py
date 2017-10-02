import inspect
from eventSourceMixin import EventSourceMixin
from sipTransportConnection import SIPTransportConnection


class SIPTransport(EventSourceMixin):
    def __init__(self, bind_address, bind_port):
        EventSourceMixin.__init__(self)
        self.bind_address = bind_address
        self.bind_port = bind_port
        self.connections = []

    @property
    def is_reliable(self):
        return True

    @property
    def is_stateful(self):
        return True

    @property
    def transportParameterName(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def bind(self):
        pass

    def connect_to_address_and_port(self, address_string, port_integer):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def connectionWithAddressAndPort(self, address_string, port_integer):
        return next((c for c in self.connections if c.remoteAddress == address_string and c.remotePort == port_integer), None)

    def connectionWithID(self, idString):
        return next((c for c in self.connections if c.id == idString), None)

    def subscribeToTransportConnectionEvents(self, a_sip_transport_connection):
        a_sip_transport_connection.when_event_do('receivedValidConnectedRequest', self.received_valid_connected_request_event_handler)
        a_sip_transport_connection.when_event_do('receivedValidConnectedResponse', self.received_valid_connected_response_event_handler)
        a_sip_transport_connection.when_event_do('madeConnection', self.made_connection_event_handler)
        a_sip_transport_connection.when_event_do('lostConnection', self.lost_connection_event_handler)

    def unSubscribeFromTransportConnectionEvents(self, a_sip_transport_connection):
        a_sip_transport_connection.when_event_do_not('receivedValidConnectedRequest', self.received_valid_connected_request_event_handler)
        a_sip_transport_connection.when_event_do_not('receivedValidConnectedResponse', self.received_valid_connected_response_event_handler)
        a_sip_transport_connection.when_event_do_not('madeConnection', self.made_connection_event_handler)
        a_sip_transport_connection.when_event_do_not('lostConnection', self.lost_connection_event_handler)

    def made_connection_event_handler(self, a_sip_transport_connection):
        pass

    def lost_connection_event_handler(self, a_sip_transport_connction):
        pass

    def received_valid_connected_request_event_handler(self, a_connected_aip_message):
        print("(transport) receivedValidConnectedRequest event")
        self.trigger_event("receivedValidConnectedRequest", a_connected_aip_message)

    def received_valid_connected_response_event_handler(self, a_connected_aip_message):
        print("(transport) receivedValidConnectedResponse event")
        self.trigger_event("receivedValidConnectedResponse", a_connected_aip_message)

    def triggerBound(self):
        print("bound event")
        self.trigger_event("bound")

    def triggerBindFailed(self):
        print("bindFailed event")
        self.trigger_event("bindFailed")

    def triggerMadeConnection(self, a_sip_transport_connection):
        print("madeConnection event - " + str(a_sip_transport_connection))
        self.trigger_event("madeConnection", a_sip_transport_connection)

    def triggerCouldNotMakeConnection(self, address_string, port_integer):
        print("couldNotMakeConnection event - " + str((address_string, port_integer)))
        self.trigger_event("couldNotMakeConnection", (address_string, port_integer))

    def triggerLostConnection(self, a_sip_transport_connection):
        print("lostConnection event - " + str(a_sip_transport_connection))
        self.trigger_event("lostConnection", a_sip_transport_connection)

    def trigger_received_valid_connected_request(self, a_connected_aip_message):
        print("receivedValidConnectedRequest event - " + str(a_connected_aip_message))
        self.trigger_event("receivedValidConnectedRequest", a_connected_aip_message)

    def trigger_received_valid_connected_response(self, a_connected_aip_message):
        print("receivedValidConnectedResponse event - " + str(a_connected_aip_message))
        self.trigger_event("receivedValidConnectedResponse", a_connected_aip_message)

