try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPHeaderField
from bobstack.sipmessaging import classproperty


class RouteSIPHeaderField(SIPHeaderField):
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Route'

    @classmethod
    def newForAttributes(cls, fieldName="Route", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

    @property
    def isRoute(self):
        return True

