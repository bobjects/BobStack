from sipTransport import SIPTransport
from udpSIPTransportConnection import UDPSIPTransportConnection


class UDPSIPTransport(SIPTransport):
    @property
    def isReliable(self):
        return False

    @property
    def isStateful(self):
        return False

    @property
    def transportParameterName(self):
        return 'UDP'

    def connectToAddressAndPort(self, addressString, portInteger):
        # TODO
        pass

    def bind(self):
        # TODO
        pass
