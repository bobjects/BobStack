try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
from sipStartLine import SIPStartLine
from classproperty import classproperty


# TODO: We need to make request_uri first class, not a string.  Do that soon, including changing a plethora of tests.

class SIPRequestStartLine(SIPStartLine):
    @classmethod
    def newForAttributes(cls, sip_method="", request_uri=""):
        answer = cls()
        answer.sip_method = sip_method
        answer.request_uri = request_uri
        return answer

    def __init__(self):
        SIPStartLine.__init__(self)
        self._sipMethod = None
        self._requestURI = None

    @property
    def sip_method(self):
        if self._sipMethod is None:
            self.parseAttributesFromRawString()
        return self._sipMethod

    @sip_method.setter
    def sip_method(self, a_string):
        self._sipMethod = a_string
        self.clearRawString()

    @property
    def request_uri(self):
        if self._requestURI is None:
            self.parseAttributesFromRawString()
        return self._requestURI

    @request_uri.setter
    def request_uri(self, a_string):
        self._requestURI = a_string
        self.clearRawString()

    def clearAttributes(self):
        self._sipMethod = None
        self._requestURI = None

    def parseAttributesFromRawString(self):
        self._sipMethod = ""
        self._requestURI = ""
        match = self.__class__.regexForParsing.match(self._rawString)
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

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def regexForMatching(cls):
        return cls.regexForParsing

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def regexForParsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile('^([^\s]+)\s+([^\s]+)\s+SIP/2.0\s*$')
            return cls._regexForParsing

    @classmethod
    def canMatchString(cls, a_string):
        return cls.regexForMatching.match(a_string) is not None

    @property
    def isRequest(self):
        return True

