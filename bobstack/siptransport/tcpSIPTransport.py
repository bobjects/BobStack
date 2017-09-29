from sipTransport import SIPTransport
from tcpSIPTransportConnection import TCPSIPTransportConnection


class TCPSIPTransport(SIPTransport):
    @property
    def transportParameterName(self):
        return 'TCP'

    def connectToAddressAndPort(self, address_string, port_integer):
        # TODO
        pass

    def bind(self):
        # TODO
        pass
