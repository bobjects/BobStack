from sipTransportConnection import SIPTransportConnection


class UDPSIPTransportConnection(SIPTransportConnection):
    def __init__(self, bind_address_string, remote_address_string, bind_port_integer, remote_port_integer):
        self.twistedProtocol = None
        super(UDPSIPTransportConnection, self).__init__(bind_address_string, remote_address_string, bind_port_integer, remote_port_integer)

    @property
    def is_reliable(self):
        return False

    @property
    def is_stateful(self):
        return False

    def send_message(self, a_sip_message):
        self.twistedProtocol.send_message(a_sip_message)
