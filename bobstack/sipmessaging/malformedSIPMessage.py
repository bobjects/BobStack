from sipMessage import SIPMessage


class MalformedSIPMessage(SIPMessage):
    @classmethod
    def newForAttributes(cls, startLine=None, content="", header=None):
        return cls._newForAttributes(startLine=startLine, content=content, header=header)

    @property
    def isMalformed(self):
        return True

