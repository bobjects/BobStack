try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
# import sys
# sys.path.append("../../..")
# from ..sipmessaging import SIPHeaderField
# from ..sipmessaging import classproperty
from ...sipmessaging import IntegerSIPHeaderField
from ...sipmessaging import classproperty


class RecordSessionExpiresSIPHeaderField(IntegerSIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Record-Session-Expires'

    # @classmethod
    # def new_for_attributes(cls, field_name="Record-Session-Expires", field_value_string=""):
    #     return cls.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_record_session_expires(self):
        return True

