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
    def isReliable(self):
        return True

    @property
    def isStateful(self):
        return True

    @property
    def transportParameterName(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def bind(self):
        pass

    def connectToAddressAndPort(self, address_string, port_integer):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def connectionWithAddressAndPort(self, address_string, port_integer):
        return next((c for c in self.connections if c.remoteAddress == address_string and c.remotePort == port_integer), None)

    def connectionWithID(self, idString):
        return next((c for c in self.connections if c.id == idString), None)

    def subscribeToTransportConnectionEvents(self, a_sip_transport_connection):
        a_sip_transport_connection.whenEventDo('receivedValidConnectedRequest', self.receivedValidConnectedRequestEventHandler)
        a_sip_transport_connection.whenEventDo('receivedValidConnectedResponse', self.receivedValidConnectedResponseEventHandler)
        a_sip_transport_connection.whenEventDo('madeConnection', self.madeConnectionEventHandler)
        a_sip_transport_connection.whenEventDo('lostConnection', self.lostConnectionEventHandler)

    def unSubscribeFromTransportConnectionEvents(self, a_sip_transport_connection):
        a_sip_transport_connection.whenEventDoNot('receivedValidConnectedRequest', self.receivedValidConnectedRequestEventHandler)
        a_sip_transport_connection.whenEventDoNot('receivedValidConnectedResponse', self.receivedValidConnectedResponseEventHandler)
        a_sip_transport_connection.whenEventDoNot('madeConnection', self.madeConnectionEventHandler)
        a_sip_transport_connection.whenEventDoNot('lostConnection', self.lostConnectionEventHandler)

    def madeConnectionEventHandler(self, a_sip_transport_connection):
        pass

    def lostConnectionEventHandler(self, a_sip_transport_connction):
        pass

    def receivedValidConnectedRequestEventHandler(self, a_connected_aip_message):
        print "(transport) receivedValidConnectedRequest event"
        self.triggerEvent("receivedValidConnectedRequest", a_connected_aip_message)

    def receivedValidConnectedResponseEventHandler(self, a_connected_aip_message):
        print "(transport) receivedValidConnectedResponse event"
        self.triggerEvent("receivedValidConnectedResponse", a_connected_aip_message)

    def triggerBound(self):
        print "bound event"
        self.triggerEvent("bound")

    def triggerBindFailed(self):
        print "bindFailed event"
        self.triggerEvent("bindFailed")

    def triggerMadeConnection(self, a_sip_transport_connection):
        print "madeConnection event - " + str(a_sip_transport_connection)
        self.triggerEvent("madeConnection", a_sip_transport_connection)

    def triggerCouldNotMakeConnection(self, address_string, port_integer):
        print "couldNotMakeConnection event - " + str((address_string, port_integer))
        self.triggerEvent("couldNotMakeConnection", (address_string, port_integer))

    def triggerLostConnection(self, a_sip_transport_connection):
        print "lostConnection event - " + str(a_sip_transport_connection)
        self.triggerEvent("lostConnection", a_sip_transport_connection)

    def triggerReceivedValidConnectedRequest(self, a_connected_aip_message):
        print "receivedValidConnectedRequest event - " + str(a_connected_aip_message)
        self.triggerEvent("receivedValidConnectedRequest", a_connected_aip_message)

    def triggerReceivedValidConnectedResponse(self, a_connected_aip_message):
        print "receivedValidConnectedResponse event - " + str(a_connected_aip_message)
        self.triggerEvent("receivedValidConnectedResponse", a_connected_aip_message)

