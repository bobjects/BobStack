from sipMessage import SIPMessage
from sipRequestStartLine import SIPRequestStartLine


class SIPRequest(SIPMessage):
    @classmethod
    def new_for_attributes(cls, sip_method="", request_uri="", content="", header=None):
        start_line = SIPRequestStartLine.new_for_attributes(sip_method=sip_method, request_uri=request_uri)
        # SIPMessage._newForAttributes(cls, start_line=start_line, content=content, header=header)
        return cls._newForAttributes(start_line=start_line, content=content, header=header)

    @property
    def is_request(self):
        return True

    # TODO:  need to test
    @property
    def request_uri(self):
        return self.start_line.request_uri

    # TODO:  need to test
    @property
    def max_forwards(self):
        return self.header.max_forwards
