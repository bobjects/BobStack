try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
# import sys
# sys.path.append("../../..")
# from ..sipmessaging import IntegerSIPHeaderField
# from ..sipmessaging import classproperty
from ...sipmessaging import IntegerSIPHeaderField
from ...sipmessaging import classproperty


class TimestampSIPHeaderField(IntegerSIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Timestamp'

    @property
    def is_timestamp(self):
        return True

