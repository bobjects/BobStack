try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
from sipHeaderField import SIPHeaderField


class ContentLengthSIPHeaderField(SIPHeaderField):
    @classmethod
    def newForAttributes(cls, value=0):
        answer = cls()
        answer.value = value
        return answer

    def __init__(self):
        SIPHeaderField.__init__(self)
        self._value = None

    @property
    def value(self):
        if self._value is None:
            self.parseAttributesFromRawString()
        return self._value

    @value.setter
    def value(self, anInteger):
        self._value = anInteger
        self.clearRawString()

    def clearAttributes(self):
        self._value = None

    def parseAttributesFromRawString(self):
        self._value = 0
        match = self.__class__.regexForParsing().search(self._rawString)
        if match:
            self._value = int(match.group(1))

    def renderRawStringFromAttributes(self):
        stringio = StringIO()
        stringio.write("Content-Length: ")
        stringio.write(str(self._value))
        self._rawString = stringio.getvalue()
        stringio.close()

    @classmethod
    def regexForParsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile('^Content-Length\s*:\s*(\d*)', re.I)
            # cls._regexForParsing = re.compile('Content', re.I)
            return cls._regexForParsing

    @property
    def isValid(self):
        return super(ContentLengthSIPHeaderField, self).isValid and self.value is not None

    @property
    def isContentLength(self):
        return True

