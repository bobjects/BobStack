try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
from sipStartLine import SIPStartLine


class SIPResponseStartLine(SIPStartLine):
    def __init__(self, stringToParse=None, statusCode=500, reasonPhrase=""):
        SIPStartLine.__init__(self, stringToParse=stringToParse)
        # on the off chance that stringToParse and the other parameters are all specified,
        # ignore the other parameters, and populate our attributes by parsing.
        if not stringToParse:
            self.statusCode = statusCode
            self.reasonPhrase = reasonPhrase
        else:
            self.parseAttributesFromRawString()

    def parseAttributesFromRawString(self):
        self.statusCode = 500
        self.reasonPhrase = ""
        match = self.__class__.regexForParsing().search(self._rawString)
        if match:
            self.statusCode, self.reasonPhrase = match.group(1, 2)
            self.statusCode = int(self.statusCode)

    def renderRawStringFromAttributes(self):
        stringio = StringIO()
        stringio.write("SIP/2.0 ")
        stringio.write(str(self.statusCode))
        stringio.write(" ")
        stringio.write(str(self.reasonPhrase))
        self._rawString = stringio.getvalue()
        stringio.close()

    @classmethod
    def regexForParsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile("^SIP/2.0\s+([\d]+)+\s+(.+)$")
            return cls._regexForParsing

    @classmethod
    def canParseString(cls, aString):
        return cls.regexForParsing().match(aString) is not None

    @property
    def isResponse(self):
        return True
