try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPHeaderField
from bobstack.sipmessaging import classproperty


class AllowSIPHeaderField(SIPHeaderField):
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Allow'

    @classmethod
    def newForAttributes(cls, fieldName="Allow", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

    @property
    def isAllow(self):
        return True

