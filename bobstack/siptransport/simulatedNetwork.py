from singleton import Singleton
import simulatedSIPTransportConnection


class SimulatedNetwork(Singleton):
    def __init__(self):
        self.boundTransports = []

    def boundTransportWithAddressAndPort(self, bind_address_string, bind_port_integer):
        with self._lock:
            return next((t for t in self.boundTransports if t.bind_address == bind_address_string and t.bind_port == bind_port_integer), None)

    def bindTransport(self, a_simulated_sip_transport):
        with self._lock:
            if self.boundTransportWithAddressAndPort(a_simulated_sip_transport.bind_address, a_simulated_sip_transport.bind_port) is None:
                self.boundTransports.append(a_simulated_sip_transport)
                return True
            else:
                return False

    def connectedSIPTransportForAddressesAndPorts(self, bind_address_string, remote_address_string, bind_port_integer, remote_port_integer):
        with self._lock:
            transport = self.boundTransportWithAddressAndPort(bind_address_string, bind_port_integer)
            return next((c for c in transport.connections if c.remoteAddress == remote_address_string and c.remotePort == remote_port_integer), None)
