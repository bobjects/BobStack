try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
from sipStartLine import SIPStartLine


class SIPRequestStartLine(SIPStartLine):
    def __init__(self, stringToParse=None, sipMethod="", requestURI=""):
        SIPStartLine.__init__(self, stringToParse=stringToParse)
        # on the off chance that stringToParse and the other parameters are all specified,
        # ignore the other parameters, and populate our attributes by parsing.
        if not stringToParse:
            self.sipMethod = sipMethod
            self.requestURI = requestURI
        else:
            self.parseAttributesFromRawString()

    def parseAttributesFromRawString(self):
        self.sipMethod = ""
        self.requestURI = ""
        match = self.__class__.regexForParsing().search(self._rawString)
        if match:
            self.sipMethod, self.requestURI = match.group(1, 2)

    def renderRawStringFromAttributes(self):
        stringio = StringIO()
        stringio.write(str(self.sipMethod))
        stringio.write(" ")
        stringio.write(str(self.requestURI))
        stringio.write(" SIP/2.0")
        self._rawString = stringio.getvalue()
        stringio.close()

    @classmethod
    def regexForParsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile('^([^\s]+)\s+([^\s]+)\s+SIP/2.0$')
            return cls._regexForParsing

    @classmethod
    def canParseString(cls, aString):
        return cls.regexForParsing().match(aString) is not None

    @property
    def isRequest(self):
        return True

