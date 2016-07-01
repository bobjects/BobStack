try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import IntegerSIPHeaderField
# from bobstack.sipmessaging import classproperty
from sipmessaging import IntegerSIPHeaderField
from sipmessaging import classproperty


class ContentLengthSIPHeaderField(IntegerSIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Content-Length'

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalCompactFieldName(cls):
        return 'l'

    @property
    def isContentLength(self):
        return True

