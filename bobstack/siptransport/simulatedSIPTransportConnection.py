from sipTransportConnection import SIPTransportConnection
from simulatedNetwork import SimulatedNetwork


class SimulatedSIPTransportConnection(SIPTransportConnection):
    def sendMessage(self, a_sip_message):
        self.sendString(a_sip_message.rawString)

    def sendString(self, a_string):
        other_connection = SimulatedNetwork.instance.connectedSIPTransportForAddressesAndPorts(self.remoteAddress, self.bind_address, self.remotePort, self.bind_port)
        if other_connection:
            other_connection.receivedString(a_string)
        else:
            # TODO:  need to have an event for an unsuccessful send.
            pass
