from sipTransportConnection import SIPTransportConnection
from simulatedNetwork import SimulatedNetwork


class SimulatedSIPTransportConnection(SIPTransportConnection):
    def send_message(self, a_sip_message):
        self.send_string(a_sip_message.raw_string)

    def send_string(self, a_string):
        other_connection = SimulatedNetwork.instance.connected_sip_transport_for_addresses_and_ports(self.remoteAddress, self.bind_address, self.remotePort, self.bind_port)
        if other_connection:
            other_connection.received_string(a_string)
        else:
            # TODO:  need to have an event for an unsuccessful send.
            pass
