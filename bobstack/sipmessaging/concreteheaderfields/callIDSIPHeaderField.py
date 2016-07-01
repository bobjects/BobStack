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


class CallIDSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Call-ID'

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalCompactFieldName(cls):
        return 'i'

    @classmethod
    def newForAttributes(cls, fieldName="Call-ID", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

    @property
    def isCallID(self):
        return True

