import sys
from hashlib import sha1
sys.path.append("../..")
# from bobstack.sipmessaging import StrongRandomStringServer
import inspect
from eventSourceMixin import EventSourceMixin
from connectedSIPMessageFactory import ConnectedSIPMessageFactory


class SIPTransportConnection(EventSourceMixin):
    def __init__(self, bindAddressString, remoteAddressString, bindPortInteger, remotePortInteger):
        EventSourceMixin.__init__(self)
        self.bindAddress = bindAddressString
        self.bindPort = bindPortInteger
        self.remoteAddress = remoteAddressString
        self.remotePort = remotePortInteger
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
        answer.update(str(self.bindPort))
        answer.update(str(self.bindAddress))
        answer.update(str(self.remotePort))
        answer.update(str(self.remoteAddress))
        return answer.hexdigest()

    def sendMessage(self, aSIPMessage):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def receivedString(self, aString):
        self.messageFactory.nextForString(aString)

    def receivedValidConnectedRequestEventHandler(self, aConnectedSIPMessage):
        print "(connection) receivedValidConnectedRequest event"
        self.triggerEvent("receivedValidConnectedRequest", aConnectedSIPMessage)

    def receivedValidConnectedResponseEventHandler(self, aConnectedSIPMessage):
        print "(connection) receivedValidConnectedResponse event"
        self.triggerEvent("receivedValidConnectedResponse", aConnectedSIPMessage)

    # TODO - need to get invalid messages as well, so that entities can deal with problems.
