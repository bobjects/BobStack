from sipMessage import SIPMessage
from sipResponseStartLine import SIPResponseStartLine


class SIPResponse(SIPMessage):
    def __init__(self, stringToParse=None, alreadyParsedSIPStartLine=None, statusCode=500, reasonPhrase="", content="", headerFields=None):
        if stringToParse:
            # on the off chance that stringToParse and the other parameters are all specified,
            # ignore the other parameters, and populate our attributes by parsing.
            SIPMessage.__init__(self, stringToParse=stringToParse, alreadyParsedSIPStartLine=alreadyParsedSIPStartLine)
        else:
            startLine = SIPResponseStartLine(statusCode=statusCode, reasonPhrase=reasonPhrase)
            SIPMessage.__init__(self, startLine=startLine, content=content, headerFields=headerFields)

    @property
    def isResponse(self):
        return True

    @property
    def isKnown(self):
        return True
