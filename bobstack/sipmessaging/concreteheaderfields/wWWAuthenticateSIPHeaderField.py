try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPHeaderField


class WWWAuthenticateSIPHeaderField(SIPHeaderField):
    @classmethod
    def newForAttributes(cls, fieldName="WWW-Authenticate", fieldValue=""):
        return cls.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)

    @classmethod
    def regexForMatchingFieldName(cls):
        try:
            return cls._regexForMatchingFieldName
        except AttributeError:
            cls._regexForMatchingFieldName = re.compile('^WWW-Authenticate$', re.I)
            return cls._regexForMatchingFieldName

    @classmethod
    def regexForMatching(cls):
        try:
            return cls._regexForMatching
        except AttributeError:
            cls._regexForMatching = re.compile('^WWW-Authenticate\s*:', re.I)
            return cls._regexForMatching

    @classmethod
    def regexForParsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile('^WWW-Authenticate\s*:\s*(.*)', re.I)
            return cls._regexForParsing

    @property
    def isWWWAuthenticate(self):
        return True

