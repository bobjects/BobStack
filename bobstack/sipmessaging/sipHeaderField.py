import re


class SIPHeaderField(object):
    def __init__(self, stringToParse=None):
        self._rawString = stringToParse

    @classmethod
    def regexForParsing(cls):
        return cls.regexToNeverMatch()

    @classmethod
    def regexToNeverMatch(cls):
        try:
            return cls._regexToNeverMatch
        except AttributeError:
            cls._regexToNeverMatch = re.compile('^NEVERMATCH')
            return cls._regexToNeverMatch

    @classmethod
    def canParseString(cls, aString):
        return cls.regexForParsing().match(aString) is not None

    @property
    def isUnknown(self):
        return not self.isKnown

    @property
    def isKnown(self):
        return True

    @property
    def isValid(self):
        # TODO - test if it's well-formed.
        return True

    @property
    def isContentLength(self):
        return False

    @property
    def rawString(self):
        if self._rawString is None:
            self.renderRawStringFromAttributes()
            pass
        return self._rawString

    def renderRawStringFromAttributes(self):
        pass

