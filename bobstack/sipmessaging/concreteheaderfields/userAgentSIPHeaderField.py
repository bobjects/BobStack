try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPHeaderField
# from bobstack.sipmessaging import classproperty
from sipmessaging import SIPHeaderField
from sipmessaging import classproperty


class UserAgentSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'User-Agent'

    @classmethod
    def newForAttributes(cls, fieldName="User-Agent", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

    @property
    def isUserAgent(self):
        return True

