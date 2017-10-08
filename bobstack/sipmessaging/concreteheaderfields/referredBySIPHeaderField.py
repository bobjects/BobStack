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


class ReferredBySIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Referred-By'

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_compact_field_name(cls):
        return 'b'

    @classmethod
    def new_for_attributes(cls, field_name="Referred-By", field_value_string=""):
        return cls.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_referred_by(self):
        return True

