from connectedSIPMessage import ConnectedSIPMessage
import sys
sys.path.append("../..")
from bobstack.sipmessaging import SIPMessageFactory
from eventSourceMixin import EventSourceMixin
from connectedSIPMessage import ConnectedSIPMessage


class ConnectedSIPMessageFactory(EventSourceMixin):
    def __init__(self, aSIPTransportConnection):
        EventSourceMixin.__init__(self)
        self.connection = aSIPTransportConnection
        self.sipMessageFactory = SIPMessageFactory()
        self.subscribeToSIPMessageFactoryEvents()

    def subscribeToSIPMessageFactoryEvents(self):
        self.sipMessageFactory.whenEventDo("validSIPRequest", self.receivedValidSIPRequestEventHandler)
        self.sipMessageFactory.whenEventDo("validSIPResponse", self.receivedValidSIPResponseEventHandler)

    def nextForString(self, aString):
        self.sipMessageFactory.nextForString(aString)

    def receivedValidSIPRequestEventHandler(self, aSIPRequest):
        self.triggerReceivedValidConnectedRequest(ConnectedSIPMessage(self.connection, aSIPRequest))

    def triggerReceivedValidConnectedRequest(self, aConectedSIPMessage):
        print "receivedValidConnectedRequest event - " + str(aConectedSIPMessage)
        self.triggerEvent("receivedValidConnectedRequest", aConectedSIPMessage)

    def receivedValidSIPResponseEventHandler(self, aSIPResponse):
        self.triggerReceivedValidConnectedResponse(ConnectedSIPMessage(self.connection, aSIPResponse))

    def triggerReceivedValidConnectedResponse(self, aConectedSIPMessage):
        print "receivedValidConnectedResponse event - " + str(aConectedSIPMessage)
        self.triggerEvent("receivedValidConnectedResponse", aConectedSIPMessage)
