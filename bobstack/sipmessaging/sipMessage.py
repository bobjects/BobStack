try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from sipHeader import SIPHeader
from sipStartLineFactory import SIPStartLineFactory


class SIPMessage(object):
    @classmethod
    def newParsedFrom(cls, aString):
        answer = cls()
        answer.rawString = aString
        return answer

    @classmethod
    def _newForAttributes(cls, startLine=None, header=None, content=""):
        answer = cls()
        answer.startLine = startLine
        answer.header = header
        answer.content = content
        return answer

    def __init__(self):
        self._content = None
        self._startLine = None
        self._header = None
        self._rawString = None

    @property
    def rawString(self):
        if self._rawString is None:
            self.renderRawStringFromAttributes()
        return self._rawString

    @rawString.setter
    def rawString(self, aString):
        self._rawString = aString
        self.clearAttributes()

    def clearRawString(self):
        self._rawString = None

    def clearAttributes(self):
        self._content = None
        self._startLine = None
        self._header = None

    def parseAttributesFromRawString(self):
        self._content = ""
        stringIO = StringIO(self._rawString)
        self._startLine = SIPStartLineFactory().nextForStringIO(stringIO)
        self._header = SIPHeader(stringioToParse=stringIO)
        self._content = stringIO.read()
        stringIO.close()

    def renderRawStringFromAttributes(self):
        stringio = StringIO()
        stringio.write(self._startLine.rawString)
        stringio.write("\r\n")
        self._header.renderRawStringFromAttributes(stringio)
        stringio.write(self._content)
        self._rawString = stringio.getvalue()
        stringio.close()

    @property
    def startLine(self):
        if self._startLine is None:
            self.parseAttributesFromRawString()
        return self._startLine

    @startLine.setter
    def startLine(self, aSIPStartLine):
        self._startLine = aSIPStartLine
        self.clearRawString()

    @property
    def header(self):
        if self._header is None:
            self.parseAttributesFromRawString()
        return self._header

    @header.setter
    def header(self, aSIPHeader):
        self._header = aSIPHeader
        self.clearRawString()

    @property
    def content(self):
        if self._content is None:
            self.parseAttributesFromRawString()
        return self._content

    @content.setter
    def content(self, aString):
        self._content = aString
        self.clearRawString()

    @property
    def isValid(self):
        if self.isMalformed:
            return False
        else:
            # TODO: check if header fields include a valid Content-Length header field, and that the content is the correct length.
            return True

    @property
    def isUnknown(self):
        return not self.isKnown

    @property
    def isKnown(self):
        return False

    @property
    def isMalformed(self):
        return False

    @property
    def isRequest(self):
        return False

    @property
    def isResponse(self):
        return False

    @property
    def isOPTIONSRequest(self):
        return False

