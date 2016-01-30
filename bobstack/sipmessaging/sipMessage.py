from cStringIO import StringIO
from contentLengthSIPHeaderField import ContentLengthSIPHeaderField
from unknownSIPHeaderField import UnknownSIPHeaderField


class SIPMessage(object):
    def __init__(self, aString, aSIPStartLine):
        self.rawString = aString
        self.startLine = aSIPStartLine
        # TODO:  SIP messages are terminted by CRLF.  does readline strip both the CR and LF?  That's what we want.
        self.content = ""
        self.headerFieldLines = []
        with StringIO(aString) as stringIO:
            stringIO.readline()  # skip the first line.  We've already parsed it.
            lineString = stringIO.readline()
            while lineString.__len__() > 0:
                self.headerFieldLines.append(lineString)
                lineString = stringIO.readline()
            self.content = stringIO.read()
        self.headerFields = [self.headerFieldForLine(line) for line in self.headerFieldLines]

    @property
    def isValid(self):
        if self.isMalformed:
            return False
        else:
            # TODO: check if header fields include a valid Content-Length header field, and that the content is the correct length.
            return True

    @property
    def isKnown(self):
        return False

    @property
    def isMalformed(self):
        return False

    def headerFieldForLine(self, aString):
        if ContentLengthSIPHeaderField.matchesLine(aString):
            return ContentLengthSIPHeaderField(aString)
        # TODO - this will get fleshed out as we define more header fields.
        else:
            return UnknownSIPHeaderField(aString)
