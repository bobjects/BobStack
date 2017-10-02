import sys
from hashlib import sha1
sys.path.append("../..")
# from bobstack.sipmessaging import StrongRandomStringServer
import inspect
from eventSourceMixin import EventSourceMixin
from connectedSIPMessageFactory import ConnectedSIPMessageFactory


class SIPTransportConnection(EventSourceMixin):
    def __init__(self, bind_address_string, remote_address_string, bind_port_integer, remote_port_integer):
        EventSourceMixin.__init__(self)
        self.bind_address = bind_address_string
        self.bind_port = bind_port_integer
        self.remoteAddress = remote_address_string
        self.remotePort = remote_port_integer
        # self.id = StrongRandomStringServer.instance.next_32_bits
        self.messageFactory = ConnectedSIPMessageFactory(self)
        self.messageFactory.when_event_do('receivedValidConnectedRequest', self.received_valid_connected_request_event_handler)
        self.messageFactory.when_event_do('receivedValidConnectedResponse', self.received_valid_connected_response_event_handler)

    @property
    def is_reliable(self):
        return True

    @property
    def is_stateful(self):
        return True

    @property
    def id(self):
        answer = sha1()
        answer.update(str(self.__class__))
        answer.update(str(self.bind_port))
        answer.update(str(self.bind_address))
        answer.update(str(self.remotePort))
        answer.update(str(self.remoteAddress))
        return answer.hexdigest()

    def send_message(self, a_sip_message):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def received_string(self, a_string):
        self.messageFactory.next_for_string(a_string)

    def received_valid_connected_request_event_handler(self, a_connected_aip_message):
        print("(connection) receivedValidConnectedRequest event")
        self.trigger_event("receivedValidConnectedRequest", a_connected_aip_message)

    def received_valid_connected_response_event_handler(self, a_connected_aip_message):
        print("(connection) receivedValidConnectedResponse event")
        self.trigger_event("receivedValidConnectedResponse", a_connected_aip_message)

    # TODO - need to get invalid messages as well, so that entities can deal with problems.
