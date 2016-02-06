try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
from sipHeaderField import SIPHeaderField


class UnknownSIPHeaderField(SIPHeaderField):
    @classmethod
    def newForAttributes(cls, fieldName="", fieldValue=""):
        answer = cls()
        answer.fieldName = fieldName
        answer.fieldValue = fieldValue
        return answer

    def __init__(self):
        SIPHeaderField.__init__(self)
        self._fieldName = None
        self._fieldValue = None

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

    def clearAttributes(self):
        self._fieldName = None
        self._fieldValue = None

    def parseAttributesFromRawString(self):
        self._fieldName = ""
        self._fieldValue = ""
        match = self.__class__.regexForParsingFieldAndValue().search(self._rawString)
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
    def regexForParsingFieldAndValue(cls):
        try:
            return cls._regexForParsingFieldAndValue
        except AttributeError:
            cls._regexForParsingFieldAndValue = re.compile('^([^\s:]+)\s*:\s*(.*)$')
            return cls._regexForParsingFieldAndValue

    @classmethod
    def regexForParsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile('^NEVERMATCH')
            return cls._regexForParsing

    @property
    def isKnown(self):
        return False
