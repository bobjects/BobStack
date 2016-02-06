from sipMessage import SIPMessage
from sipResponseStartLine import SIPResponseStartLine


class SIPResponse(SIPMessage):
    @classmethod
    def newForAttributes(cls, statusCode=500, reasonPhrase="", content="", header=None):
        startLine = SIPResponseStartLine.newForAttributes(statusCode=statusCode, reasonPhrase=reasonPhrase)
        # SIPMessage._newForAttributes(cls, startLine=startLine, content=content, header=header)
        return cls._newForAttributes(startLine=startLine, content=content, header=header)

    @property
    def isResponse(self):
        return True

    @property
    def isKnown(self):
        return True
