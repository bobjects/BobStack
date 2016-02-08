try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
from sipStartLine import SIPStartLine


class SIPResponseStartLine(SIPStartLine):
    @classmethod
    def newForAttributes(cls, statusCode="", reasonPhrase=""):
        answer = cls()
        answer.statusCode = statusCode
        answer.reasonPhrase = reasonPhrase
        return answer

    def __init__(self):
        SIPStartLine.__init__(self)
        self._statusCode = None
        self._reasonPhrase = None

    @property
    def statusCode(self):
        if self._statusCode is None:
            self.parseAttributesFromRawString()
        return self._statusCode

    @statusCode.setter
    def statusCode(self, aString):
        self._statusCode = aString
        self.clearRawString()

    @property
    def reasonPhrase(self):
        if self._reasonPhrase is None:
            self.parseAttributesFromRawString()
        return self._reasonPhrase

    @reasonPhrase.setter
    def reasonPhrase(self, aString):
        self._reasonPhrase = aString
        self.clearRawString()

    def clearAttributes(self):
        self._statusCode = None
        self._reasonPhrase = None

    def parseAttributesFromRawString(self):
        self._statusCode = 500
        self._reasonPhrase = ""
        match = self.__class__.regexForParsing().search(self._rawString)
        if match:
            self._statusCode, self._reasonPhrase = match.group(1, 2)
            self._statusCode = int(self._statusCode)

    def renderRawStringFromAttributes(self):
        stringio = StringIO()
        stringio.write("SIP/2.0 ")
        stringio.write(str(self._statusCode))
        stringio.write(" ")
        stringio.write(str(self._reasonPhrase))
        self._rawString = stringio.getvalue()
        stringio.close()

    @classmethod
    def regexForMatching(cls):
        return cls.regexForParsing()

    @classmethod
    def regexForParsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile("^SIP/2.0\s+([\d]+)+\s+(.+)\s*$")
            return cls._regexForParsing

    @classmethod
    def canMatchString(cls, aString):
        return cls.regexForMatching().match(aString) is not None

    @property
    def isResponse(self):
        return True
