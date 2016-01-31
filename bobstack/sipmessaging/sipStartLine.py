class SIPStartLine(object):
    def __init__(self, stringToParse=None):
        self._rawString = stringToParse

    @property
    def isResponse(self):
        return False

    @property
    def isRequest(self):
        return False

    @property
    def isMalformed(self):
        return False

    @property
    def rawString(self):
        if not self._rawString:
            self.renderRawStringFromAttributes()
            pass
        return self._rawString

    def renderRawStringFromAttributes(self):
        pass
