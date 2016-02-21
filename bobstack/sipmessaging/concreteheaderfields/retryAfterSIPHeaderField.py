try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import IntegerSIPHeaderField


class RetryAfterSIPHeaderField(IntegerSIPHeaderField):
    @classmethod
    def canonicalFieldName(cls):
        return 'Retry-After'

    @property
    def isRetryAfter(self):
        return True

