try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from sipHeaderField import SIPHeaderField
from bobstack.sipmessaging import classproperty


class UnknownSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'NEVER-MATCH'

    @property
    def isKnown(self):
        return False
