from sipTransport import SIPTransport
from simulatedSIPTransportConnection import SimulatedSIPTransportConnection
from simulatedNetwork import SimulatedNetwork

class SimulatedSIPTransport(SIPTransport):
    @property
    def transportParameterName(self):
        return 'SIM'

    def connectToAddressAndPort(self, addressString, portInteger):
        connectedTransport = SimulatedNetwork.instance.boundTransportWithAddressAndPort(addressString, portInteger)
        if connectedTransport:
            self.basicConnectToAddressAndPort(addressString, portInteger)
            connectedTransport.basicConnectToAddressAndPort(self.bindAddress, self.bindPort)
        else:
            self.triggerCouldNotMakeConnection(addressString, portInteger)

    def basicConnectToAddressAndPort(self, addressString, portInteger):
        # TODO: the local port is not necessarily our bind port, it may be a random upper port.
        connection = SimulatedSIPTransportConnection(addressString, self.bindPort, portInteger)
        self.connections.append(connection)
        self.subscribeToTransportConnectionEvents(connection)
        self.triggerMadeConnection(connection)

    def bind(self):
        if SimulatedNetwork.instance.bindTransport(self):
            self.triggerBound()
        else:
            self.triggerBindFailed()
