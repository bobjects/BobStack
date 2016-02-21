try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import IntegerSIPHeaderField


class TimestampSIPHeaderField(IntegerSIPHeaderField):
    @classmethod
    def canonicalFieldName(cls):
        return 'Timestamp'

    @property
    def isTimestamp(self):
        return True

