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


class SupportedSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Supported'

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalCompactFieldName(cls):
        return 'k'

    @classmethod
    def newForAttributes(cls, fieldName="Supported", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

    @property
    def isSupported(self):
        return True

