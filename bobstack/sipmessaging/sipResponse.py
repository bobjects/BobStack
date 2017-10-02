from sipMessage import SIPMessage
from sipResponseStartLine import SIPResponseStartLine


class SIPResponse(SIPMessage):
    @classmethod
    def new_for_attributes(cls, status_code=500, reason_phrase="", content="", header=None):
        start_line = SIPResponseStartLine.new_for_attributes(status_code=status_code, reason_phrase=reason_phrase)
        # SIPMessage._newForAttributes(cls, start_line=start_line, content=content, header=header)
        return cls._newForAttributes(start_line=start_line, content=content, header=header)

    @property
    def is_response(self):
        return True

    @property
    def is_known(self):
        return True

    # TODO:  need to test.
    @property
    def is_provisional(self):
        return self.start_line.is_provisional

    # TODO:  need to test.
    @property
    def is_final(self):
        return self.start_line.is_final
