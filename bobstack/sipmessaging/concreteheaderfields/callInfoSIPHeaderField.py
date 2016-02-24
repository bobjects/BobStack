try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPHeaderField


class CallInfoSIPHeaderField(SIPHeaderField):
    @classmethod
    def newForAttributes(cls, fieldName="Call-Info", fieldValue=""):
        return cls.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)

    @classmethod
    def regexForMatchingFieldName(cls):
        try:
            return cls._regexForMatchingFieldName
        except AttributeError:
            cls._regexForMatchingFieldName = re.compile('^Call-Info$', re.I)
            return cls._regexForMatchingFieldName

    @classmethod
    def regexForMatching(cls):
        try:
            return cls._regexForMatching
        except AttributeError:
            cls._regexForMatching = re.compile('^Call-Info\s*:', re.I)
            return cls._regexForMatching

    @classmethod
    def regexForParsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile('^Call-Info\s*:\s*(.*)', re.I)
            return cls._regexForParsing

    @property
    def isCallInfo(self):
        return True

