from sipStartLine import SIPStartLine


class MalformedSIPStartLine(SIPStartLine):
    @property
    def is_malformed(self):
        return True
