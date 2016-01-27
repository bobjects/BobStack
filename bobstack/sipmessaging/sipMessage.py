from cStringIO import StringIO
from sipStartLine import SIPStartLine

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
        return False

    @property
    def isKnown(self):
        return False

    @property
    def isMalformed(self):
        return False

    def headerFieldForLine(self, aString):
        # TODO
        pass
