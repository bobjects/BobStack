try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re


class SIPHeaderField(object):
    @classmethod
    def newParsedFrom(cls, aString):
        answer = cls()
        answer.rawString = aString
        return answer

    @classmethod
    def newForAttributes(cls, fieldName="", fieldValue=""):
        return cls.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)

    @classmethod
    def newForFieldAttributes(cls, fieldName="", fieldValue=""):
        answer = cls()
        answer.fieldName = fieldName
        answer.fieldValue = fieldValue
        return answer

    def __init__(self):
        self._rawString = None
        self._fieldName = None
        self._fieldValue = None

    @property
    def rawString(self):
        if self._rawString is None:
            self.renderRawStringFromAttributes()
        return self._rawString

    @rawString.setter
    def rawString(self, aString):
        self._rawString = aString
        self.clearAttributes()

    @property
    def fieldName(self):
        if self._fieldName is None:
            self.parseAttributesFromRawString()
        return self._fieldName

    @fieldName.setter
    def fieldName(self, aString):
        self._fieldName = aString
        self.clearRawString()

    @property
    def fieldValue(self):
        if self._fieldValue is None:
            self.parseAttributesFromRawString()
        return self._fieldValue

    @fieldValue.setter
    def fieldValue(self, aString):
        self._fieldValue = aString
        self.clearRawString()

    def clearRawString(self):
        self._rawString = None

    def clearAttributes(self):
        self._fieldName = None
        self._fieldValue = None

    def parseAttributesFromRawString(self):
        self._fieldName = ""
        self._fieldValue = ""
        match = self.__class__.regexForParsingFieldAndValue().match(self._rawString)
        if match:
            self._fieldName, self._fieldValue = match.group(1, 2)

    def renderRawStringFromAttributes(self):
        stringio = StringIO()
        stringio.write(str(self._fieldName))
        stringio.write(": ")
        stringio.write(str(self._fieldValue))
        self._rawString = stringio.getvalue()
        stringio.close()

    @classmethod
    def regexForMatchingFieldName(cls):
        return cls.regexToNeverMatch()

    @classmethod
    def regexForMatching(cls):
        return cls.regexForParsing()

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
    def regexForParsingFieldAndValue(cls):
        try:
            return cls._regexForParsingFieldAndValue
        except AttributeError:
            cls._regexForParsingFieldAndValue = re.compile('^([^\s:]+)\s*:\s*(.*)$')
            return cls._regexForParsingFieldAndValue

    @classmethod
    def canMatchString(cls, aString):
        return cls.regexForMatching().match(aString) is not None

    @classmethod
    def canMatchFieldName(cls, aString):
        return cls.regexForMatchingFieldName().match(aString) is not None

    @property
    def isUnknown(self):
        return not self.isKnown

    @property
    def isKnown(self):
        return True

    @property
    def isValid(self):
        if not self.fieldName:  # fail if None or empty fieldName.
            return False
        if self.fieldValue is None:
            return False
        return True

    @property
    def isContentLength(self):
        return False

