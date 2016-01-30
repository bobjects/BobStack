from sipMessage import SIPMessage


class MalformedSIPMessage(SIPMessage):
    @property
    def isMalformed(self):
        return True

