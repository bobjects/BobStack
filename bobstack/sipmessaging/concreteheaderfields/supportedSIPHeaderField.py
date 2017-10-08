try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
# import sys
# sys.path.append("../../..")
# from ..sipmessaging import SIPHeaderField
# from ..sipmessaging import classproperty
from ...sipmessaging import SIPHeaderField
from ...sipmessaging import classproperty


class SupportedSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Supported'

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_compact_field_name(cls):
        return 'k'

    @classmethod
    def new_for_attributes(cls, field_name="Supported", field_value_string=""):
        return cls.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_supported(self):
        return True

