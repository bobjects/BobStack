from sipTransport import SIPTransport
from udpSIPTransportConnection import UDPSIPTransportConnection
from udpSIPTwistedProtocol import UDPSIPTwistedProtocol


class UDPSIPTransport(SIPTransport):
    def __init__(self, bind_address, bind_port):
        super(UDPSIPTransport, self).__init__(bind_address, bind_port)
        self.twistedProtocol = UDPSIPTwistedProtocol(self)

    @property
    def is_reliable(self):
        return False

    @property
    def is_stateful(self):
        return False

    @property
    def transportParameterName(self):
        return 'UDP'

    def connect_to_address_and_port(self, address_string, port_integer):
        # UDP is not a connection-oriented protocol.  Just instantiate the connection
        # and treat it as a successful connection
        connection = self.connectionWithAddressAndPort(address_string, port_integer)
        if not connection:
            connection = UDPSIPTransportConnection(self.bind_address, address_string, self.bind_port, port_integer)
            connection.twistedProtocol = self.twistedProtocol
            self.connections.append(connection)
            self.subscribeToTransportConnectionEvents(connection)
            self.triggerMadeConnection(connection)
        return connection

    def bind(self):
        self.twistedProtocol.bind()
