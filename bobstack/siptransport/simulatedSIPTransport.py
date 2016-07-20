from sipTransport import SIPTransport
from simulatedSIPTransportConnection import SimulatedSIPTransportConnection
from simulatedNetwork import SimulatedNetwork


class SimulatedSIPTransport(SIPTransport):
    @property
    def transportParameterName(self):
        return 'SIM'

    def connectToAddressAndPort(self, addressString, portInteger):
        # TODO: need to make (and test) exception handlers, not just events.
        connectedTransport = SimulatedNetwork.instance.boundTransportWithAddressAndPort(addressString, portInteger)
        if connectedTransport:
            if connectedTransport is not self:
                answer = self.basicConnectToAddressAndPort(addressString, portInteger)
                connectedTransport.basicConnectToAddressAndPort(self.bindAddress, self.bindPort)
                return answer
            else:
                self.triggerCouldNotMakeConnection(addressString, portInteger)
        else:
            self.triggerCouldNotMakeConnection(addressString, portInteger)

    def basicConnectToAddressAndPort(self, addressString, portInteger):
        # TODO: the local port is not necessarily our bind port, it may be a random upper port.
        connection = SimulatedSIPTransportConnection(self.bindAddress, addressString, self.bindPort, portInteger)
        self.connections.append(connection)
        self.subscribeToTransportConnectionEvents(connection)
        self.triggerMadeConnection(connection)
        return connection

    def bind(self):
        if SimulatedNetwork.instance.bindTransport(self):
            self.triggerBound()
        else:
            self.triggerBindFailed()
