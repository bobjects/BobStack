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
        self.subscribeToSIPMessageFactoryEvents()

    def subscribeToSIPMessageFactoryEvents(self):
        self.sipMessageFactory.whenEventDo("validSIPRequest", self.receivedValidSIPRequestEventHandler)
        self.sipMessageFactory.whenEventDo("validSIPResponse", self.receivedValidSIPResponseEventHandler)

    def nextForString(self, a_string):
        self.sipMessageFactory.nextForString(a_string)

    def receivedValidSIPRequestEventHandler(self, a_sip_request):
        self.triggerReceivedValidConnectedRequest(ConnectedSIPMessage(self.connection, a_sip_request))

    def triggerReceivedValidConnectedRequest(self, a_conected_sip_message):
        print "receivedValidConnectedRequest event - " + str(a_conected_sip_message)
        self.triggerEvent("receivedValidConnectedRequest", a_conected_sip_message)

    def receivedValidSIPResponseEventHandler(self, a_sip_response):
        self.triggerReceivedValidConnectedResponse(ConnectedSIPMessage(self.connection, a_sip_response))

    def triggerReceivedValidConnectedResponse(self, a_conected_sip_message):
        print "receivedValidConnectedResponse event - " + str(a_conected_sip_message)
        self.triggerEvent("receivedValidConnectedResponse", a_conected_sip_message)
