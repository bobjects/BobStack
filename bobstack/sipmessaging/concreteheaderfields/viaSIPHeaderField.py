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
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Via'

    @classmethod
    def newForAttributes(cls, fieldName="Via", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

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

