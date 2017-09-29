try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
from sipStartLine import SIPStartLine
from classproperty import classproperty


class SIPResponseStartLine(SIPStartLine):
    @classmethod
    def newForAttributes(cls, status_code="", reason_phrase=""):
        answer = cls()
        answer.status_code = status_code
        answer.reason_phrase = reason_phrase
        return answer

    def __init__(self):
        SIPStartLine.__init__(self)
        self._statusCode = None
        self._reasonPhrase = None

    @property
    def status_code(self):
        if self._statusCode is None:
            self.parseAttributesFromRawString()
        return self._statusCode

    @status_code.setter
    def status_code(self, a_string):
        self._statusCode = a_string
        self.clearRawString()

    @property
    def reason_phrase(self):
        if self._reasonPhrase is None:
            self.parseAttributesFromRawString()
        return self._reasonPhrase

    @reason_phrase.setter
    def reason_phrase(self, a_string):
        self._reasonPhrase = a_string
        self.clearRawString()

    def clearAttributes(self):
        self._statusCode = None
        self._reasonPhrase = None

    def parseAttributesFromRawString(self):
        self._statusCode = 500
        self._reasonPhrase = ""
        match = self.__class__.regexForParsing.match(self._rawString)
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
            cls._regexForParsing = re.compile("^SIP/2.0\s+([\d]+)+\s+(.+)\s*$")
            return cls._regexForParsing

    @classmethod
    def canMatchString(cls, a_string):
        return cls.regexForMatching.match(a_string) is not None

    @property
    def isResponse(self):
        return True

    # TODO:  need to test.
    @property
    def isProvisional(self):
        # True if 1xx
        return self.status_code.startsWith('1')

    # TODO:  need to test.
    @property
    def isFinal(self):
        return not self.isProvisional
