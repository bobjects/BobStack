from sipTransport import SIPTransport


class TestSIPTransport(SIPTransport):
    @property
    def transportParameterName(self):
        return 'TST'

    def connectToAddressAndPort(self, addressString, portInteger):
        # TODO instantiate a TestSIPTransportConection, trigger event.
        pass

    def bind(self):
        self.triggerBound()

