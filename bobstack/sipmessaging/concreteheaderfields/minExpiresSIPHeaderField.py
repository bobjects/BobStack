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


class MinExpiresSIPHeaderField(IntegerSIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Min-Expires'

    # @classmethod
    # def new_for_attributes(cls, field_name="Min-Expires", field_value_string=""):
    #     return cls.newForFieldNameAndValueString(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_min_expires(self):
        return True

