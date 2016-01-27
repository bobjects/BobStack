import re


class SIPHeaderField:
    def __init__(self, aString=""):
        self.rawString = aString

    @classmethod
    def regexToMatch(cls):
        return re._compile('^NEVERMATCH')

    @classmethod
    def matchesLine(cls, aString):
        return cls.regexToMatch().match(aString, re.I) is not None

    @property
    def isValid(self):
        return True
