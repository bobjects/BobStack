try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPHeaderField


class ServerSIPHeaderField(SIPHeaderField):
    @classmethod
    def newForAttributes(cls, fieldName="Server", fieldValue=""):
        return cls.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)

    @classmethod
    def regexForMatchingFieldName(cls):
        try:
            return cls._regexForMatchingFieldName
        except AttributeError:
            cls._regexForMatchingFieldName = re.compile('^Server$', re.I)
            return cls._regexForMatchingFieldName

    @classmethod
    def regexForMatching(cls):
        try:
            return cls._regexForMatching
        except AttributeError:
            cls._regexForMatching = re.compile('^Server\s*:', re.I)
            return cls._regexForMatching

    @classmethod
    def regexForParsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile('^Server\s*:\s*(.*)', re.I)
            return cls._regexForParsing

    @property
    def isServer(self):
        return True

