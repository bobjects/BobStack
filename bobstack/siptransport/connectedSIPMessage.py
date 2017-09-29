

class ConnectedSIPMessage(object):
    def __init__(self, a_sip_transport_connection, a_sip_message):
        self.connection = a_sip_transport_connection
        self.sipMessage = a_sip_message

    @property
    def rawString(self):
        if self.sipMessage:
            return self.sipMessage.rawString
        else:
            return None
