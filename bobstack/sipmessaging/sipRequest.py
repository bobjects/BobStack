from sipMessage import SIPMessage
from sipRequestStartLine import SIPRequestStartLine


class SIPRequest(SIPMessage):
    def __init__(self, stringToParse=None, alreadyParsedSIPStartLine=None, sipMethod="", requestURI="", content="", header=None):
        if stringToParse:
            # on the off chance that stringToParse and the other parameters are all specified,
            # ignore the other parameters, and populate our attributes by parsing.
            SIPMessage.__init__(self, stringToParse=stringToParse, alreadyParsedSIPStartLine=alreadyParsedSIPStartLine)
        else:
            startLine = SIPRequestStartLine(sipMethod=sipMethod, requestURI=requestURI)
            SIPMessage.__init__(self, startLine=startLine, content=content, header=header)

    @property
    def isRequest(self):
        return True
