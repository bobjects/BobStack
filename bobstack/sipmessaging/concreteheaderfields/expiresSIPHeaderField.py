try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from ...sipmessaging import IntegerSIPHeaderField
from ...sipmessaging import classproperty


class ExpiresSIPHeaderField(IntegerSIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Expires'

    @property
    def is_expires(self):
        return True

