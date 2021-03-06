try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from ...sipmessaging import SIPHeaderField
from ...sipmessaging import classproperty


class CallIDSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Call-ID'

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_compact_field_name(cls):
        return 'i'

    @classmethod
    def new_for_attributes(cls, field_name="Call-ID", field_value_string=""):
        return cls.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_call_id(self):
        return True

