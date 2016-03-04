try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPHeaderField
from bobstack.sipmessaging import classproperty


class ToSIPHeaderField(SIPHeaderField):
    # https://tools.ietf.org/html/rfc3261#section-20.39

    @classmethod
    def newForAttributes(cls, fieldName="To", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

    @classproperty
    @classmethod
    def regexForMatchingFieldName(cls):
        try:
            return cls._regexForMatchingFieldName
        except AttributeError:
            cls._regexForMatchingFieldName = re.compile('^To$', re.I)
            return cls._regexForMatchingFieldName

    @classproperty
    @classmethod
    def regexForMatching(cls):
        try:
            return cls._regexForMatching
        except AttributeError:
            cls._regexForMatching = re.compile('^To\s*:', re.I)
            return cls._regexForMatching

    @classproperty
    @classmethod
    def regexForParsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile('^To\s*:\s*(.*)', re.I)
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
    def isTo(self):
        return True

