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
        self.messageFactory = ConnectedSIPMessageFactory(self)
        self.messageFactory.whenEventDo('receivedValidConnectedRequest', self.receivedValidConnectedRequestEventHandler)
        self.messageFactory.whenEventDo('receivedValidConnectedResponse', self.receivedValidConnectedResponseEventHandler)

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

