from sipMessage import SIPMessage
from sipResponseStartLine import SIPResponseStartLine


class SIPResponse(SIPMessage):
    @classmethod
    def newForAttributes(cls, status_code=500, reason_phrase="", content="", header=None):
        start_line = SIPResponseStartLine.newForAttributes(status_code=status_code, reason_phrase=reason_phrase)
        # SIPMessage._newForAttributes(cls, start_line=start_line, content=content, header=header)
        return cls._newForAttributes(start_line=start_line, content=content, header=header)

    @property
    def isResponse(self):
        return True

    @property
    def isKnown(self):
        return True

    # TODO:  need to test.
    @property
    def isProvisional(self):
        return self.start_line.isProvisional

    # TODO:  need to test.
    @property
    def isFinal(self):
        return self.start_line.isFinal
