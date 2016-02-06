import re


class SIPHeaderField(object):
    @classmethod
    def newParsedFrom(cls, aString):
        answer = cls()
        answer.rawString = aString
        return answer

    def __init__(self):
        self._rawString = None

    @property
    def rawString(self):
        if self._rawString is None:
            self.renderRawStringFromAttributes()
        return self._rawString

    @rawString.setter
    def rawString(self, aString):
        self._rawString = aString
        self.clearAttributes()

    def clearRawString(self):
        self._rawString = None

    def clearAttributes(self):
        pass

    def parseAttributesFromRawString(self):
        pass

    def renderRawStringFromAttributes(self):
        pass

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

