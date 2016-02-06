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
        if self._value is None:
            return 0
        return self._value

    @value.setter
    def value(self, anInteger):
        self._value = anInteger
        self.clearRawString()

    def clearAttributes(self):
        self._value = None

    def parseAttributesFromRawString(self):
        # self._value = None
        self._value = None
        # TODO: globally replace search() with match()???
        match = self.__class__.regexForParsing().search(self._rawString)
        if match:
            matchGroup = match.group(1)
            if matchGroup:
                self._value = int(matchGroup)
            else:
                # Will get here is the Content-Length header field is present, but there is no value.
                self._value = None

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
        # Answer false if the value is not present.
        test = self.value  # Make sure the attributes are lazily initialized.
        return super(ContentLengthSIPHeaderField, self).isValid and self._value is not None

    @property
    def isContentLength(self):
        return True

