import inspect
from eventSourceMixin import EventSourceMixin


class SIPTransportConnection(EventSourceMixin):
    def __init__(self, addressString, localPortInteger, remotePortInteger):
        EventSourceMixin.__init__(self)
        self.address = addressString
        self.localPort = localPortInteger
        self.remotePort = remotePortInteger

    def sendMessage(self, aSIPMessage):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

