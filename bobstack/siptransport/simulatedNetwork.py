from singleton import Singleton
import simulatedSIPTransportConnection

class SimulatedNetwork(Singleton):
    # TODO: need to make a serialization lock; this will surely be used by multiple threads.

    def __init__(self):
        self.boundTransports = []

    def boundTransportWithAddressAndPort(self, boundAddressString, boundPortInteger):
        return next((t for t in self.boundTransports if t.bindAddress == boundAddressString and t.bindPort == boundPortInteger), None)

    def bindTransport(self, aSimulatedSIPTransport):
        if self.boundTransportWithAddressAndPort(aSimulatedSIPTransport.bindAddress, aSimulatedSIPTransport.bindPort) is None:
            self.boundTransports.append(aSimulatedSIPTransport)
            return True
        else:
            return False
