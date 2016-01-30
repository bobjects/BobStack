class SIPStartLine(object):
    def __init__(self, aString=""):
        self.rawString = aString

    @property
    def isResponse(self):
        return False

    @property
    def isRequest(self):
        return False

    @property
    def isMalformed(self):
        return False
