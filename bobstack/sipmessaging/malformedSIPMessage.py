from sipMessage import SIPMessage


class MalformedSIPMessage(SIPMessage):
    @classmethod
    def new_for_attributes(cls, start_line=None, content="", header=None):
        return cls._newForAttributes(start_line=start_line, content=content, header=header)

    @property
    def is_malformed(self):
        return True

