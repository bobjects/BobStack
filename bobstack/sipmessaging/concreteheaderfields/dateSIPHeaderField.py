try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPHeaderField
from bobstack.sipmessaging import classproperty


class DateSIPHeaderField(SIPHeaderField):
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Date'

    @classmethod
    def newForAttributes(cls, fieldName="Date", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

    @property
    def isDate(self):
        return True

