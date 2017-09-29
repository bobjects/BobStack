from sipTransport import SIPTransport
from tlsSIPTransportConnection import TLSSIPTransportConnection


class TLSSIPTransport(SIPTransport):
    @property
    def transportParameterName(self):
        return 'TLS'

    def connectToAddressAndPort(self, address_string, port_integer):
        # TODO
        pass

    def bind(self):
        # TODO
        pass
