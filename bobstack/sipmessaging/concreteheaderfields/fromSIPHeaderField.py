try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPHeaderField


class FromSIPHeaderField(SIPHeaderField):
    @classmethod
    def newForAttributes(cls, fieldName="From", fieldValue=""):
        return cls.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)

    @classmethod
    def regexForMatchingFieldName(cls):
        try:
            return cls._regexForMatchingFieldName
        except AttributeError:
            cls._regexForMatchingFieldName = re.compile('^From$', re.I)
            return cls._regexForMatchingFieldName

    @classmethod
    def regexForMatching(cls):
        try:
            return cls._regexForMatching
        except AttributeError:
            cls._regexForMatching = re.compile('^From\s*:', re.I)
            return cls._regexForMatching

    @classmethod
    def regexForParsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile('^From\s*:\s*(.*)', re.I)
            return cls._regexForParsing

    # TODO: need to test
    # TODO: need to cache
    @property
    def tag(self):
        return self.parameterNamed("tag")

    # TODO
    def generateTag(self):
        pass

    @property
    def isFrom(self):
        return True

