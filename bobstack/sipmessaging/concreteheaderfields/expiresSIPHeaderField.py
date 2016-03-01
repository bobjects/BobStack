try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import IntegerSIPHeaderField
from bobstack.sipmessaging import classproperty


class ExpiresSIPHeaderField(IntegerSIPHeaderField):
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Expires'

    @property
    def isExpires(self):
        return True

