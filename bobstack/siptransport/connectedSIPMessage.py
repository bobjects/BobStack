

class ConnectedSIPMessage(object):
    def __init__(self, a_sip_transport_connection, a_sip_message):
        self.connection = a_sip_transport_connection
        self.sip_message = a_sip_message

    @property
    def raw_string(self):
        if self.sip_message:
            return self.sip_message.raw_string
        else:
            return None
