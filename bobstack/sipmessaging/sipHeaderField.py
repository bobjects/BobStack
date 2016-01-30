import re


class SIPHeaderField(object):
    def __init__(self, aString=""):
        self.rawString = aString

    @classmethod
    def regexToMatch(cls):
        return cls.regexToNeverMatch()

    @classmethod
    def regexToNeverMatch(cls):
        try:
            return cls._regexToNeverMatch
        except AttributeError:
            cls._regexToNeverMatch = re.compile('^NEVERMATCH')
            return cls._regexToNeverMatch

    @classmethod
    def matchesLine(cls, aString):
        return cls.regexToMatch().match(aString) is not None

    @property
    def isValid(self):
        # TODO - test if it's well-formed.
        return True

    @property
    def isContentLength(self):
        return False

    @property
    def isKnown(self):
        return True


