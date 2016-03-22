from sipTransport import SIPTransport
from simulatedSIPTransportConnection import SimulatedSIPTransportConnection


class SimulatedSIPTransport(SIPTransport):
    @property
    def transportParameterName(self):
        return 'SIM'

    def connectToAddressAndPort(self, addressString, portInteger):
        connection = SimulatedSIPTransportConnection(addressString, portInteger)
        self.connections.append(connection)
        self.subscribeToTransportConnectionEvents(connection)
        self.triggerMadeConnection(connection)

    def bind(self):
        self.triggerBound()

