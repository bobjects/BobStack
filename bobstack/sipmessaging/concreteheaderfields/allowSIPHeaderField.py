from ...sipmessaging import SIPHeaderField
from ...sipmessaging import classproperty
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class AllowSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Allow'

    @classmethod
    def new_for_attributes(cls, field_name="Allow", field_value_string=""):
        return cls.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_allow(self):
        return True

