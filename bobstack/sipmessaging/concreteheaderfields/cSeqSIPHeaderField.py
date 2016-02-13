try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPHeaderField


class CSeqSIPHeaderField(SIPHeaderField):
    @classmethod
    def newForAttributes(cls, fieldName="CSeq", fieldValue=""):
        return cls.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)

    # @classmethod
    # def newForAttributes(cls, value=0):
    #     answer = cls.newForFieldAttributes(fieldName="CSeq", fieldValue=str(value))
    #     answer.value = value
    #     return answer

    # def __init__(self):
    #     SIPHeaderField.__init__(self)
    #     self._value = None

    # @property
    # def value(self):
    #     if self._value is None:
    #         self.parseAttributesFromRawString()
    #     if self._value is None:
    #         return 0
    #     return self._value

    # @value.setter
    # def value(self, anInteger):
    #     self._value = anInteger
    #     self.fieldValue = str(anInteger)
    #     self.clearRawString()

    # def clearAttributes(self):
    #     super(CSeqSIPHeaderField, self).clearAttributes()
    #     self._value = None

    # def parseAttributesFromRawString(self):
    #     super(CSeqSIPHeaderField, self).parseAttributesFromRawString()
    #     self._value = None
    #     match = self.__class__.regexForParsing().match(self._rawString)
    #     if match:
    #         matchGroup = match.group(1)
    #         if matchGroup:
    #             self._value = int(matchGroup)
    #         else:
    #             # Will get here is the CSeq header field is present, but there is no value.
    #             self._value = None

    @classmethod
    def regexForMatchingFieldName(cls):
        try:
            return cls._regexForMatchingFieldName
        except AttributeError:
            cls._regexForMatchingFieldName = re.compile('^CSeq$', re.I)
            return cls._regexForMatchingFieldName

    @classmethod
    def regexForMatching(cls):
        try:
            return cls._regexForMatching
        except AttributeError:
            cls._regexForMatching = re.compile('^CSeq\s*:', re.I)
            return cls._regexForMatching

    @classmethod
    def regexForParsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile('^CSeq\s*:\s*(.*)', re.I)
            return cls._regexForParsing

    # @property
    # def isValid(self):
    #     # Answer false if the value is not present.
    #     test = self.value  # Make sure the attributes are lazily initialized.
    #     return super(CSeqSIPHeaderField, self).isValid and self._value is not None

    @property
    def isCSeq(self):
        return True

