try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from sipHeader import SIPHeader
from sipStartLineFactory import SIPStartLineFactory


class SIPMessage(object):
    def __init__(self, stringToParse=None, alreadyParsedSIPStartLine=None, startLine=None, content="", header=None):
        self._rawString = stringToParse
        self.startLine = alreadyParsedSIPStartLine
        # on the off chance that stringToParse and the other parameters are all specified,
        # ignore the other parameters, and populate our attributes by parsing.
        if not stringToParse:
            self.content = content
            self.startLine = startLine
            if header:
                self.header = header
            else:
                self.header = SIPHeader()
        else:
            self.parseAttributesFromRawString()

    def parseAttributesFromRawString(self):
        self.content = ""
        stringIO = StringIO(self._rawString)
        if self.startLine:
            stringIO.readline()  # skip the first line.  We've already parsed it.
        else:
            self.startLine = SIPStartLineFactory().nextForStringIO(stringIO)
        self.header = SIPHeader(stringioToParse=stringIO)
        self.content = stringIO.read()
        stringIO.close()

    def renderRawStringFromAttributes(self):
        stringio = StringIO()
        stringio.write(self.startLine.rawString)
        stringio.write("\r\n")
        self.header.renderRawStringFromAttributes(stringio)
        stringio.write(self.content)
        self._rawString = stringio.getvalue()
        stringio.close()

    @property
    def rawString(self):
        if not self._rawString:
            self.renderRawStringFromAttributes()
            pass
        return self._rawString

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

