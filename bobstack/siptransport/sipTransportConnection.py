

class SIPTransportConnection(object):
    def __init__(self, addressString, localPortInteger, remotePortInteger):
        self.address = addressString
        self.localPort = localPortInteger
        self.remotePort = remotePortInteger


