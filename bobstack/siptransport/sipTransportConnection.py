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
        # self.id = StrongRandomStringServer.instance.next32Bits
        self.messageFactory = ConnectedSIPMessageFactory(self)
        self.messageFactory.whenEventDo('receivedValidConnectedRequest', self.receivedValidConnectedRequestEventHandler)
        self.messageFactory.whenEventDo('receivedValidConnectedResponse', self.receivedValidConnectedResponseEventHandler)

    @property
    def isReliable(self):
        return True

    @property
    def isStateful(self):
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

    def sendMessage(self, a_sip_message):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def receivedString(self, a_string):
        self.messageFactory.nextForString(a_string)

    def receivedValidConnectedRequestEventHandler(self, a_connected_aip_message):
        print "(connection) receivedValidConnectedRequest event"
        self.triggerEvent("receivedValidConnectedRequest", a_connected_aip_message)

    def receivedValidConnectedResponseEventHandler(self, a_connected_aip_message):
        print "(connection) receivedValidConnectedResponse event"
        self.triggerEvent("receivedValidConnectedResponse", a_connected_aip_message)

    # TODO - need to get invalid messages as well, so that entities can deal with problems.
