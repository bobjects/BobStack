from ...sipmessaging import SIPHeaderField
from ...sipmessaging import classproperty
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class AllowEventsSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Allow-Events'

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_compact_field_name(cls):
        return 'u'

    @classmethod
    def new_for_attributes(cls, field_name="Allow-Events", field_value_string=""):
        return cls.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_allow_events(self):
        return True

