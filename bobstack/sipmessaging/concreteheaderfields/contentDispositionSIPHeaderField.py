try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPHeaderField
from bobstack.sipmessaging import classproperty


class ContentDispositionSIPHeaderField(SIPHeaderField):
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Content-Disposition'

    @classmethod
    def newForAttributes(cls, fieldName="Content-Disposition", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

    @property
    def isContentDisposition(self):
        return True

