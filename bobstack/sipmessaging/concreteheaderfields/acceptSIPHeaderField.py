try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPHeaderField


class AcceptSIPHeaderField(SIPHeaderField):
    @classmethod
    def newForAttributes(cls, fieldName="Accept", fieldValue=""):
        return cls.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)

    @classmethod
    def regexForMatchingFieldName(cls):
        try:
            return cls._regexForMatchingFieldName
        except AttributeError:
            cls._regexForMatchingFieldName = re.compile('^Accept$', re.I)
            return cls._regexForMatchingFieldName

    @classmethod
    def regexForMatching(cls):
        try:
            return cls._regexForMatching
        except AttributeError:
            cls._regexForMatching = re.compile('^Accept\s*:', re.I)
            return cls._regexForMatching

    @classmethod
    def regexForParsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile('^Accept\s*:\s*(.*)', re.I)
            return cls._regexForParsing

    @property
    def isAccept(self):
        return True
