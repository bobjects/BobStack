from sipMessage import SIPMessage
from sipRequestStartLine import SIPRequestStartLine


class SIPRequest(SIPMessage):
    @classmethod
    def newForAttributes(cls, sipMethod="", requestURI="", content="", header=None):
        startLine = SIPRequestStartLine.newForAttributes(sipMethod=sipMethod, requestURI=requestURI)
        # SIPMessage._newForAttributes(cls, startLine=startLine, content=content, header=header)
        return cls._newForAttributes(startLine=startLine, content=content, header=header)

    @property
    def isRequest(self):
        return True
