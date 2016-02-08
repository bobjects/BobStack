try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
from sipStartLine import SIPStartLine


class SIPRequestStartLine(SIPStartLine):
    @classmethod
    def newForAttributes(cls, sipMethod="", requestURI=""):
        answer = cls()
        answer.sipMethod = sipMethod
        answer.requestURI = requestURI
        return answer

    def __init__(self):
        SIPStartLine.__init__(self)
        self._sipMethod = None
        self._requestURI = None

    @property
    def sipMethod(self):
        if self._sipMethod is None:
            self.parseAttributesFromRawString()
        return self._sipMethod

    @sipMethod.setter
    def sipMethod(self, aString):
        self._sipMethod = aString
        self.clearRawString()

    @property
    def requestURI(self):
        if self._requestURI is None:
            self.parseAttributesFromRawString()
        return self._requestURI

    @requestURI.setter
    def requestURI(self, aString):
        self._requestURI = aString
        self.clearRawString()

    def clearAttributes(self):
        self._sipMethod = None
        self._requestURI = None

    def parseAttributesFromRawString(self):
        self._sipMethod = ""
        self._requestURI = ""
        match = self.__class__.regexForParsing().search(self._rawString)
        if match:
            self._sipMethod, self._requestURI = match.group(1, 2)

    def renderRawStringFromAttributes(self):
        stringio = StringIO()
        stringio.write(str(self._sipMethod))
        stringio.write(" ")
        stringio.write(str(self._requestURI))
        stringio.write(" SIP/2.0")
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
            cls._regexForParsing = re.compile('^([^\s]+)\s+([^\s]+)\s+SIP/2.0\s*$')
            return cls._regexForParsing

    @classmethod
    def canMatchString(cls, aString):
        return cls.regexForMatching().match(aString) is not None

    @property
    def isRequest(self):
        return True

