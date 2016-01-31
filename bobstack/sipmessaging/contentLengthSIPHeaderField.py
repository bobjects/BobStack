try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
from sipHeaderField import SIPHeaderField


class ContentLengthSIPHeaderField(SIPHeaderField):
    def __init__(self, stringToParse=None, value=0):
        SIPHeaderField.__init__(self, stringToParse=stringToParse)
        # on the off chance that stringToParse and the other parameters are all specified,
        # ignore the other parameters, and populate our attributes by parsing.
        if not stringToParse:
            self.value = value
        else:
            self.parseAttributesFromRawString()

    def parseAttributesFromRawString(self):
        self.value = 0
        match = self.__class__.regexForParsing().search(self._rawString)
        if match:
            self.value = int(match.group(1))

    def renderRawStringFromAttributes(self):
        stringio = StringIO()
        stringio.write("Content-Length: ")
        stringio.write(str(self.value))
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
        # TODO: Can we call the superclass property like this?  Hmm...
        # return SIPHeaderField.isValid(self) and self.value is not None
        return super(ContentLengthSIPHeaderField, self).isValid and self.value is not None

    @property
    def isContentLength(self):
        return True

