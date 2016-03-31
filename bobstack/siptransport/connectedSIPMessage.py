

class ConnectedSIPMessage(object):
    def __init__(self, aSIPTransportConnection, aSIPMessage):
        self.connection = aSIPTransportConnection
        self.sipMessage = aSIPMessage
