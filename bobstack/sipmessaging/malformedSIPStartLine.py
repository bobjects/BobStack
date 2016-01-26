import re
from sipStartLine import SIPStartLine

class MalformedSIPStartLine(SIPStartLine):
    @property
    def isMalformed(self):
        return True