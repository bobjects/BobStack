import re
from sipStartLine import SIPStartLine

class SIPResponseStartLine(SIPStartLine):
    def __init__(self, aString=""):
        SIPStartLine.__init__(self, aString)
        self.statusCode = 500
        self.reasonPhrase = ""
        match = self.__class__.regexToMatch().search(aString)
        if match:
            self.statusCode, self.reasonPhrase = match.group(1, 2)
            self.statusCode = int(self.statusCode)

    @classmethod
    def regexToMatch(cls):
        if not cls._regexToMatch:
            cls._regexToMatch = re._compile('^SIP/2.0\s(+[^\s])+\s+(.+)$')
        return cls._regexToMatch

    @classmethod
    def matchesLine(cls, aString):
        return cls.regexToMatch().match(aString) is not None

    @property
    def isResponse(self):
        return True