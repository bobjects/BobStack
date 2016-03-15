from sipTransport import SIPTransport
from testSIPTransportConnection import TestSIPTransportConnection


class TestSIPTransport(SIPTransport):
    @property
    def transportParameterName(self):
        return 'TST'

    def connectToAddressAndPort(self, addressString, portInteger):
        # TODO instantiate a TestSIPTransportConection, trigger event.
        connection = TestSIPTransportConnection(addressString, portInteger)
        self.subscribeToTransportConnectionEvents(connection)

    def bind(self):
        self.triggerBound()

