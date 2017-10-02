import sys
sys.path.append("../..")
from bobstack.sipmessaging import SIPMessageFactory
from eventSourceMixin import EventSourceMixin
from connectedSIPMessage import ConnectedSIPMessage


class ConnectedSIPMessageFactory(EventSourceMixin):
    def __init__(self, a_sip_transport_connection):
        EventSourceMixin.__init__(self)
        self.connection = a_sip_transport_connection
        self.sipMessageFactory = SIPMessageFactory()
        self.subscribe_to_sip_message_factory_events()

    def subscribe_to_sip_message_factory_events(self):
        self.sipMessageFactory.when_event_do("validSIPRequest", self.received_valid_sip_request_event_handler)
        self.sipMessageFactory.when_event_do("validSIPResponse", self.received_valid_sip_response_event_handler)

    def next_for_string(self, a_string):
        self.sipMessageFactory.next_for_string(a_string)

    def received_valid_sip_request_event_handler(self, a_sip_request):
        self.trigger_received_valid_connected_request(ConnectedSIPMessage(self.connection, a_sip_request))

    def trigger_received_valid_connected_request(self, a_conected_sip_message):
        print("receivedValidConnectedRequest event - " + str(a_conected_sip_message))
        self.trigger_event("receivedValidConnectedRequest", a_conected_sip_message)

    def received_valid_sip_response_event_handler(self, a_sip_response):
        self.trigger_received_valid_connected_response(ConnectedSIPMessage(self.connection, a_sip_response))

    def trigger_received_valid_connected_response(self, a_conected_sip_message):
        print("receivedValidConnectedResponse event - " + str(a_conected_sip_message))
        self.trigger_event("receivedValidConnectedResponse", a_conected_sip_message)
