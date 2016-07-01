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


class ContentTypeSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Content-Type'

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalCompactFieldName(cls):
        return 'c'

    @classmethod
    def newForAttributes(cls, fieldName="Content-Type", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

    @property
    def isContentType(self):
        return True

