try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPHeaderField
from bobstack.sipmessaging import classproperty


class ViaSIPHeaderField(SIPHeaderField):
    @classmethod
    def newForAttributes(cls, fieldName="Via", fieldValue=""):
        return cls.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)

    @classproperty
    @classmethod
    def regexForMatchingFieldName(cls):
        try:
            return cls._regexForMatchingFieldName
        except AttributeError:
            cls._regexForMatchingFieldName = re.compile('^Via$', re.I)
            return cls._regexForMatchingFieldName

    @classproperty
    @classmethod
    def regexForMatching(cls):
        try:
            return cls._regexForMatching
        except AttributeError:
            cls._regexForMatching = re.compile('^Via\s*:', re.I)
            return cls._regexForMatching

    @classproperty
    @classmethod
    def regexForParsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile('^Via\s*:\s*(.*)', re.I)
            return cls._regexForParsing

    # TODO: when we do warnings, warn of branch that does not start with "z9hG4bKy", i.e. a non-RFC3261 message
    # TODO: need to test
    # TODO: need to cache
    @property
    def branch(self):
        return self.parameterNamed("branch")

    # TODO
    def generateBranch(self):
        pass

    @property
    def isVia(self):
        return True

