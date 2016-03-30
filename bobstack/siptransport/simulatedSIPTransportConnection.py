from sipTransportConnection import SIPTransportConnection
from simulatedNetwork import SimulatedNetwork


class SimulatedSIPTransportConnection(SIPTransportConnection):
    def sendMessage(self, aSIPMessage):
        otherConnection = SimulatedNetwork.instance.connectedSIPTransportForAddressesAndPorts(self.remoteAddress, self.bindAddress, self.remotePort, self.bindPort)
        if otherConnection:
            otherConnection.receivedString(aSIPMessage.rawString)
        else:
            # TODO:  need to have an event for an unsuccessful send.
            pass