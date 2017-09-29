from sipMessage import SIPMessage
from sipRequestStartLine import SIPRequestStartLine


class SIPRequest(SIPMessage):
    @classmethod
    def newForAttributes(cls, sip_method="", request_uri="", content="", header=None):
        start_line = SIPRequestStartLine.newForAttributes(sip_method=sip_method, request_uri=request_uri)
        # SIPMessage._newForAttributes(cls, start_line=start_line, content=content, header=header)
        return cls._newForAttributes(start_line=start_line, content=content, header=header)

    @property
    def isRequest(self):
        return True

    # TODO:  need to test
    @property
    def request_uri(self):
        return self.start_line.request_uri

    # TODO:  need to test
    @property
    def maxForwards(self):
        return self.header.maxForwards
