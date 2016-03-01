try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPHeaderField
from bobstack.sipmessaging import classproperty


class CSeqSIPHeaderField(SIPHeaderField):
    @classmethod
    def newForAttributes(cls, fieldName="CSeq", fieldValue=""):
        return cls.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)

    @classproperty
    @classmethod
    def regexForMatchingFieldName(cls):
        try:
            return cls._regexForMatchingFieldName
        except AttributeError:
            cls._regexForMatchingFieldName = re.compile('^CSeq$', re.I)
            return cls._regexForMatchingFieldName

    @classproperty
    @classmethod
    def regexForMatching(cls):
        try:
            return cls._regexForMatching
        except AttributeError:
            cls._regexForMatching = re.compile('^CSeq\s*:', re.I)
            return cls._regexForMatching

    @classproperty
    @classmethod
    def regexForParsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile('^CSeq\s*:\s*(.*)', re.I)
            return cls._regexForParsing

    @property
    def isCSeq(self):
        return True

