try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from ...sipmessaging import SIPHeaderField
from ...sipmessaging import classproperty


class SubjectSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Subject'

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_compact_field_name(cls):
        return 's'

    @classmethod
    def new_for_attributes(cls, field_name="Subject", field_value_string=""):
        return cls.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_subject(self):
        return True

