from sipTransportConnection import SIPTransportConnection


class UDPSIPTransportConnection(SIPTransportConnection):
    def __init__(self, bind_address_string, remote_address_string, bind_port_integer, remote_port_integer):
        self.twistedProtocol = None
        super(UDPSIPTransportConnection, self).__init__(bind_address_string, remote_address_string, bind_port_integer, remote_port_integer)

    @property
    def isReliable(self):
        return False

    @property
    def isStateful(self):
        return False

    def sendMessage(self, a_sip_message):
        self.twistedProtocol.sendMessage(a_sip_message)
