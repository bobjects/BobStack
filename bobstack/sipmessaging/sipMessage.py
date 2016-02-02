try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from contentLengthSIPHeaderField import ContentLengthSIPHeaderField
from unknownSIPHeaderField import UnknownSIPHeaderField
from sipRequestStartLine import SIPRequestStartLine
from sipResponseStartLine import SIPResponseStartLine
from malformedSIPStartLine import MalformedSIPStartLine


class SIPMessage(object):
    def __init__(self, stringToParse=None, alreadyParsedSIPStartLine=None, startLine=None, content="", headerFields=None):
        self._rawString = stringToParse
        self.startLine = alreadyParsedSIPStartLine
        # on the off chance that stringToParse and the other parameters are all specified,
        # ignore the other parameters, and populate our attributes by parsing.
        if not stringToParse:
            self.content = content
            self.startLine = startLine
            if headerFields:
                self.headerFields = headerFields
            else:
                self.headerFields = []
        else:
            self.parseAttributesFromRawString()

    def parseAttributesFromRawString(self):
        self.content = ""
        self.headerFieldLines = []
        stringIO = StringIO(self._rawString)
        if self.startLine:
            stringIO.readline()  # skip the first line.  We've already parsed it.
        else:
            firstLine = stringIO.readline().rstrip('\r\n')
            self.startLine = self.sipStartLineClassForString(firstLine)(firstLine)
        lineString = stringIO.readline().rstrip('\r\n')
        while lineString.__len__() > 0:
            self.headerFieldLines.append(lineString)
            lineString = stringIO.readline().rstrip('\r\n')
        self.content = stringIO.read()
        stringIO.close()
        self.headerFields = [self.parseHeaderFieldFromLine(line) for line in self.headerFieldLines]

    def renderRawStringFromAttributes(self):
        stringio = StringIO()
        stringio.write(self.startLine.rawString)
        stringio.write("\r\n")
        for headerField in self.headerFields:
            stringio.write(headerField.rawString)
            stringio.write("\r\n")
        stringio.write("\r\n")
        stringio.write(self.content)
        self._rawString = stringio.getvalue()
        stringio.close()

    @property
    def rawString(self):
        if not self._rawString:
            self.renderRawStringFromAttributes()
            pass
        return self._rawString

    def parseHeaderFieldFromLine(self, aString):
        if ContentLengthSIPHeaderField.canParseString(aString):
            return ContentLengthSIPHeaderField(aString)
        # TODO - this will get fleshed out as we define more header fields.
        else:
            return UnknownSIPHeaderField(aString)

    # TODO:  This is copied / pasted in SIPMessage.  Refactor into a factory.
    def sipStartLineClassForString(self, aString):
        if SIPRequestStartLine.canParseString(aString):
            return SIPRequestStartLine
        elif SIPResponseStartLine.canParseString(aString):
            return SIPResponseStartLine
        else:
            return MalformedSIPStartLine

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

