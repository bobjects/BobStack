import re
from sipStartLine import SIPStartLine

class SIPRequestStartLine(SIPStartLine):
    def __init__(self, aString=""):
        SIPStartLine.__init__(self, aString)
        self.sipMethod = ""
        self.requestURI = ""
        match = self.__class__.regexToMatch().search(aString)
        if match:
            self.sipMethod, self.requestURI = match.group(1, 2)

    @classmethod
    def regexToMatch(cls):
        try:
            return cls._regexToMatch
        except AttributeError:
            cls._regexToMatch = re.compile('^([^\s]+)\s+([^\s]+)\s+SIP/2.0$')
            return cls._regexToMatch

    @classmethod
    def matchesLine(cls, aString):
        return cls.regexToMatch().match(aString) is not None

    @property
    def isRequest(self):
        return True

