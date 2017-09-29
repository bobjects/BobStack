try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPHeaderField
# from bobstack.sipmessaging import classproperty
from sipmessaging import IntegerSIPHeaderField
from sipmessaging import classproperty


class RecordSessionExpiresSIPHeaderField(IntegerSIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Record-Session-Expires'

    # @classmethod
    # def newForAttributes(cls, field_name="Record-Session-Expires", field_value_string=""):
    #     return cls.newForFieldNameAndValueString(field_name=field_name, field_value_string=field_value_string)

    @property
    def isRecordSessionExpires(self):
        return True

