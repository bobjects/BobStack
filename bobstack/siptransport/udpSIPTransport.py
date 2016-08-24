from sipTransport import SIPTransport
from udpSIPTransportConnection import UDPSIPTransportConnection
from udpSIPTwistedProtocol import UDPSIPTwistedProtocol



class UDPSIPTransport(SIPTransport):
    def __init__(self, bindAddress, bindPort):
        super(UDPSIPTransport, self).__init__(bindAddress, bindPort)
        self.twistedProtocol = UDPSIPTwistedProtocol(self)

    @property
    def isReliable(self):
        return False

    @property
    def isStateful(self):
        return False

    @property
    def transportParameterName(self):
        return 'UDP'

    def connectToAddressAndPort(self, addressString, portInteger):
        # UDP is not a connection-oriented protocol.  Just instantiate the connection
        # and treat it as a successful connection
        connection = self.connectionWithAddressAndPort(addressString, portInteger)
        if not connection:
            connection = UDPSIPTransportConnection(self.bindAddress, addressString, self.bindPort, portInteger)
            connection.twistedProtocol = self.twistedProtocol
            self.connections.append(connection)
            self.subscribeToTransportConnectionEvents(connection)
            self.triggerMadeConnection(connection)
        return connection

    def bind(self):
        self.twistedProtocol.bind()
