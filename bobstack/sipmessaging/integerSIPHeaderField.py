try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
# sys.path.append("../../..")
# from bobstack.sipmessaging import SIPHeaderField
from classproperty import classproperty
from sipHeaderField import SIPHeaderField

# TODO: We will need to change our tests to exercise the new header fields that are subs of IntegerSIPHeaderField.
# But don't do that until we refactor the tests to alleviate copy/paste.

class IntegerSIPHeaderField(SIPHeaderField):
    regexForParsingInteger = re.compile("^(\d+)")

    @classmethod
    def newForAttributes(cls, value=0):
        answer = cls.newForFieldNameAndValueString(fieldName=cls.canonicalFieldName, fieldValueString=str(value))
        answer.value = value
        return answer

    # TODO:  testing.
    @classmethod
    def newForFieldNameAndValueString(cls, fieldName="", fieldValueString="0"):
        answer = cls()
        answer.fieldName = fieldName
        answer.fieldValueString = fieldValueString
        # TODO:  May need to parse out parameters as well here.
        # TODO:  need to cache.
        # match = re.match("^(\d+)", fieldValueString)
        match = cls.regexForParsingInteger.match(fieldValueString)
        if match:
            digits = match.group(0)
        else:
            digits = "0"
        answer.value = int(digits)
        return answer

    def __init__(self):
        SIPHeaderField.__init__(self)
        self._value = None

    @property
    def value(self):
        if self._value is None:
            self.parseAttributesFromRawString()
        if self._value is None:
            return 0
        return self._value

    @value.setter
    def value(self, anInteger):
        self._value = anInteger
        self.fieldValueString = str(anInteger)
        self.clearRawString()

    def clearAttributes(self):
        super(IntegerSIPHeaderField, self).clearAttributes()
        self._value = None

    def parseAttributesFromRawString(self):
        super(IntegerSIPHeaderField, self).parseAttributesFromRawString()
        self._value = None
        match = self.__class__.regexForParsing.match(self._rawString)
        if match:
            matchGroup = match.group(1)
            if matchGroup:
                self._value = int(matchGroup)
            else:
                # Will get here is the header field is present, but there is no value.
                self._value = None

    @classproperty
    @classmethod
    def regexForMatchingFieldName(cls):
        try:
            return cls._regexForMatchingFieldName
        except AttributeError:
            cls._regexForMatchingFieldName = re.compile('^' + cls.canonicalFieldName + '$', re.I)
            return cls._regexForMatchingFieldName

    @classproperty
    @classmethod
    def regexForMatching(cls):
        try:
            return cls._regexForMatching
        except AttributeError:
            cls._regexForMatching = re.compile('^' + cls.canonicalFieldName + '\s*:', re.I)
            return cls._regexForMatching

    @classproperty
    @classmethod
    def regexForParsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile('^' + cls.canonicalFieldName + '\s*:\s*(\d*)', re.I)
            return cls._regexForParsing

    @property
    def isValid(self):
        # Answer false if the value is not present.
        test = self.value  # Make sure the attributes are lazily initialized.
        return super(IntegerSIPHeaderField, self).isValid and self._value is not None
