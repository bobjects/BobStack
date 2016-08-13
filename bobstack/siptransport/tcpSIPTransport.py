from sipTransport import SIPTransport
from tcpSIPTransportConnection import TCPSIPTransportConnection


class TCPSIPTransport(SIPTransport):
    @property
    def transportParameterName(self):
        return 'TCP'

    def connectToAddressAndPort(self, addressString, portInteger):
        # TODO
        pass

    def bind(self):
        # TODO
        pass
