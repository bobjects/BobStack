from sipTransport import SIPTransport
from tcpSIPTransportConnection import TCPSIPTransportConnection


class TCPSIPTransport(SIPTransport):
    @property
    def transport_parameter_name(self):
        return 'TCP'

    def connect_to_address_and_port(self, address_string, port_integer):
        # TODO
        pass

    def bind(self):
        # TODO
        pass
