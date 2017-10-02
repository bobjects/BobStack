try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from sipHeaderField import SIPHeaderField
from classproperty import classproperty


class UnknownSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'NEVER-MATCH'

    @property
    def is_known(self):
        return False
