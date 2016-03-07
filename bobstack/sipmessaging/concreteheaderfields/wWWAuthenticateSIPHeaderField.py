try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPHeaderField
from bobstack.sipmessaging import classproperty


class WWWAuthenticateSIPHeaderField(SIPHeaderField):
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'WWW-Authenticate'

    @classmethod
    def newForAttributes(cls, fieldName="WWW-Authenticate", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

    @property
    def isWWWAuthenticate(self):
        return True

