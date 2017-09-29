from sipTransport import SIPTransport
from simulatedSIPTransportConnection import SimulatedSIPTransportConnection
from simulatedNetwork import SimulatedNetwork


class SimulatedSIPTransport(SIPTransport):
    @property
    def transportParameterName(self):
        return 'SIM'

    def connectToAddressAndPort(self, address_string, port_integer):
        # TODO: need to make (and test) exception handlers, not just events.
        connected_transport = SimulatedNetwork.instance.boundTransportWithAddressAndPort(address_string, port_integer)
        if connected_transport:
            if connected_transport is not self:
                answer = self.basicConnectToAddressAndPort(address_string, port_integer)
                connected_transport.basicConnectToAddressAndPort(self.bind_address, self.bind_port)
                return answer
            else:
                self.triggerCouldNotMakeConnection(address_string, port_integer)
        else:
            self.triggerCouldNotMakeConnection(address_string, port_integer)

    def basicConnectToAddressAndPort(self, address_string, port_integer):
        # TODO: the local port is not necessarily our bind port, it may be a random upper port.
        connection = SimulatedSIPTransportConnection(self.bind_address, address_string, self.bind_port, port_integer)
        self.connections.append(connection)
        self.subscribeToTransportConnectionEvents(connection)
        self.triggerMadeConnection(connection)
        return connection

    def bind(self):
        if SimulatedNetwork.instance.bindTransport(self):
            self.triggerBound()
        else:
            self.triggerBindFailed()
