try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from ...sipmessaging import IntegerSIPHeaderField
from ...sipmessaging import classproperty


class ContentLengthSIPHeaderField(IntegerSIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Content-Length'

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_compact_field_name(cls):
        return 'l'

    @property
    def is_content_length(self):
        return True

