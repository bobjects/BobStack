

class ConnectedSIPMessage(object):
    def __init__(self, aSIPTransportConnection, aSIPMessage):
        self.connection = aSIPTransportConnection
        self.sipMessage = aSIPMessage

    @property
    def rawString(self):
        if self.sipMessage:
            return self.sipMessage.rawString
        else:
            return None
