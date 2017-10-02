from sipTransport import SIPTransport
from tlsSIPTransportConnection import TLSSIPTransportConnection


class TLSSIPTransport(SIPTransport):
    @property
    def transportParameterName(self):
        return 'TLS'

    def connect_to_address_and_port(self, address_string, port_integer):
        # TODO
        pass

    def bind(self):
        # TODO
        pass
