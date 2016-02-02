try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
from sipHeaderField import SIPHeaderField


class UnknownSIPHeaderField(SIPHeaderField):
    def __init__(self, stringToParse=None, fieldName="", fieldValue=""):
        SIPHeaderField.__init__(self, stringToParse=stringToParse)
        # on the off chance that stringToParse and the other parameters are all specified,
        # ignore the other parameters, and populate our attributes by parsing.
        if not stringToParse:
            self.fieldName = fieldName
            self.fieldValue = fieldValue
        else:
            self.parseAttributesFromRawString()

    def parseAttributesFromRawString(self):
        self.fieldName = ""
        self.fieldValue = ""
        match = self.__class__.regexForParsingFieldAndValue().search(self._rawString)
        if match:
            self.fieldName, self.fieldValue = match.group(1, 2)

    def renderRawStringFromAttributes(self):
        stringio = StringIO()
        stringio.write(str(self.fieldName))
        stringio.write(": ")
        stringio.write(str(self.fieldValue))
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
