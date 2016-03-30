from singleton import Singleton
import simulatedSIPTransportConnection


class SimulatedNetwork(Singleton):
    def __init__(self):
        self.boundTransports = []

    def boundTransportWithAddressAndPort(self, bindAddressString, bindPortInteger):
        with self._lock:
            return next((t for t in self.boundTransports if t.bindAddress == bindAddressString and t.bindPort == bindPortInteger), None)

    def bindTransport(self, aSimulatedSIPTransport):
        with self._lock:
            if self.boundTransportWithAddressAndPort(aSimulatedSIPTransport.bindAddress, aSimulatedSIPTransport.bindPort) is None:
                self.boundTransports.append(aSimulatedSIPTransport)
                return True
            else:
                return False

    def connectedSIPTransportForAddressesAndPorts(self, bindAddressString, remoteAddressString, bindPortInteger, remotePortInteger):
        with self._lock:
            transport = self.boundTransportWithAddressAndPort(bindAddressString, bindPortInteger)
            return next((c for c in transport.connections if c.remoteAddress == remoteAddressString and c.remotePort == remotePortInteger), None)
