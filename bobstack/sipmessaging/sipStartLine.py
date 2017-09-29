class SIPStartLine(object):
    @classmethod
    def newParsedFrom(cls, a_string):
        answer = cls()
        answer.rawString = a_string
        return answer

    def __init__(self):
        self._rawString = None

    @property
    def rawString(self):
        if self._rawString is None:
            self.renderRawStringFromAttributes()
        return self._rawString

    @rawString.setter
    def rawString(self, a_string):
        self._rawString = a_string
        self.clearAttributes()

    def clearRawString(self):
        self._rawString = None

    def clearAttributes(self):
        pass

    def parseAttributesFromRawString(self):
        pass

    def renderRawStringFromAttributes(self):
        pass

    @property
    def isResponse(self):
        return False

    @property
    def isRequest(self):
        return False

    @property
    def isMalformed(self):
        return False

